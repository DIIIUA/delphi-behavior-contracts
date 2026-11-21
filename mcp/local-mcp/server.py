#!/usr/bin/env python3
"""Delphi Behavior Contracts — Universal Local MCP Server (stdio + Streamable HTTP).

Zero external dependencies (Python 3.8+ standard library only).
Supports:
  - MCP 2025-03-26 JSON-RPC 2.0 over stdio (newline-delimited & Content-Length framing)
    and over Streamable HTTP (--http --host 127.0.0.1 --port 8788).
  - Code Mode (`delphi_execute`): AST-restricted read-only Python execution against
    the `delphi` corpus SDK so agents can cross-query 74 chapters, 89 directives,
    30 source issues and 879+ compiler receipts in a single tool call.
  - Direct tools (`delphi_search`, `delphi_read`, `delphi_skill`).
  - MCP Resources (`delphi://...`, `skill://...`), Prompts (5 specialist skills),
    and SEP-2640 Skills over MCP (`skills/list`, `skills/get`).

Usage:
  python server.py                          # stdio MCP (default)
  python server.py --root /path/to/core     # explicit corpus root
  python server.py --http --port 8788       # local Streamable HTTP MCP
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse
import ast
import hashlib
import hmac
import json
import os
import re
import sys
import urllib.parse

SERVER_INFO = {
    'name': 'delphi-behavior-contracts-mcp',
    'version': '1.0.0',
}
PROTOCOL_VERSION = '2025-03-26'

ALIASES = {
    'default parameter': ('21',), 'default parameters': ('21',),
    'параметры по умолчанию': ('21',), 'property default': ('27',),
    'reference to': ('23',), 'variant record': ('12', '54'),
    'class property': ('27',), 'array of const': ('10',),
    'dynamic array': ('10',), 'dynamic arrays': ('10',),
    'динамический массив': ('10',), 'динамические массивы': ('10',),
    'open array': ('10',), 'open arrays': ('10',),
    'открытый массив': ('10',), 'открытые массивы': ('10',),
    'managed record': ('13',), 'managed records': ('13',),
    'управляемая запись': ('13',), 'управляемые записи': ('13',),
    'inline variable': ('16',), 'inline variables': ('16',),
    'nameof': ('67',), 'extended': ('70', '07'),
    'hasweakref': ('31', '35'), 'isconstvalue': ('72', '31'),
    'gettypekind': ('31',), 'returnaddress': ('34',),
    'hidden_virtual': ('41', '59'), 'hiding_member': ('41', '59'),
}


def resolve_roots(explicit_root=None):
    """Locate (core_root, skills_root) cleanly from any install layout."""
    here = Path(__file__).resolve()
    candidates = []
    if explicit_root:
        candidates.append(Path(explicit_root).resolve())
    env_root = os.environ.get('DELPHI_CONTRACTS_ROOT')
    if env_root:
        candidates.append(Path(env_root).resolve())
    # Unified suite layout: <suite>/mcp/local-mcp/server.py -> <suite>/core
    ups = list(here.parents)[:3]  # works for short paths such as /app/server.py
    for up in reversed(ups[1:]):
        candidates.append(up / 'core')
    candidates.append(here.parent / 'core')
    candidates.extend(reversed(ups))
    core_root = None
    for c in candidates:
        if (c / 'references' / 'en' / 'chapters').is_dir():
            core_root = c
            break
    if core_root is None:
        raise FileNotFoundError(
            'Could not locate Delphi Behavior Contracts corpus (references/en/chapters). '
            'Pass --root <path> or set DELPHI_CONTRACTS_ROOT.'
        )
    skill_candidates = [
        core_root / 'skills',
        ups[-1] / 'platforms' / '01-claude-code-plugin' / 'skills',
        ups[-1] / 'skills',
        core_root.parent / 'skills',
    ]
    skills_root = None
    for sc in skill_candidates:
        if sc.is_dir() and any(sc.glob('*/SKILL.md')):
            skills_root = sc
            break
    return core_root, skills_root


def normalized(text):
    return ' '.join(text.casefold().replace('-', ' ').split())


def visible(text):
    return re.sub(r'https?://\S+', ' ', text)


def stem(term, lang):
    if lang == 'ru' and len(term) >= 5:
        return term[:max(5, len(term) - 2)]
    return None


def term_pattern(term, lang, open_end=False):
    s = stem(term, lang)
    if s:
        return r'(?<!\w)' + re.escape(s) + r'\w*'
    return r'(?<!\w)' + re.escape(term) + (r'\w*' if open_end else r'(?!\w)')


def parse_frontmatter(md_text):
    meta = {}
    body = md_text
    if md_text.startswith('---\n') or md_text.startswith('---\r\n'):
        parts = re.split(r'^---\s*$', md_text, maxsplit=2, flags=re.M)
        if len(parts) == 3:
            for line in parts[1].splitlines():
                if ':' in line:
                    k, v = line.split(':', 1)
                    meta[k.strip()] = v.strip().strip('"').strip("'")
            body = parts[2].lstrip('\r\n')
    return meta, body


class DelphiCorpus:
    """Read-only indexed access to the entire Delphi Behavior Contracts package."""

    def __init__(self, core_root: Path, skills_root: Path | None):
        self.core_root = core_root
        self.skills_root = skills_root
        self._doc_cache = {}
        self._json_cache = {}
        self._skills_cache = None

    def _safe_path(self, rel_path: str) -> Path:
        p = (self.core_root / rel_path.lstrip('/')).resolve()
        if not p.is_relative_to(self.core_root):
            raise ValueError(f'Path escapes corpus root: {rel_path}')
        if not p.is_file():
            raise FileNotFoundError(f'Not found in corpus: {rel_path}')
        return p

    def _read_text(self, path: Path) -> str:
        key = str(path)
        if key not in self._doc_cache:
            self._doc_cache[key] = path.read_text(encoding='utf-8', errors='replace')
        return self._doc_cache[key]

    def _read_json(self, rel_path: str):
        if rel_path not in self._json_cache:
            p = self._safe_path(rel_path)
            self._json_cache[rel_path] = json.loads(self._read_text(p))
        return self._json_cache[rel_path]

    def _load_skills(self):
        if self._skills_cache is not None:
            return self._skills_cache
        skills = {}
        if self.skills_root and self.skills_root.is_dir():
            for p in sorted(self.skills_root.glob('*/SKILL.md')):
                raw = p.read_text(encoding='utf-8')
                meta, _ = parse_frontmatter(raw)
                name = meta.get('name') or p.parent.name
                skills[name] = {
                    'name': name,
                    'description': meta.get('description', ''),
                    'uri': f'skill://{name}/SKILL.md',
                    'digest': 'sha256:' + hashlib.sha256(raw.encode('utf-8')).hexdigest(),
                    'words': len(raw.split()),
                    'content': raw,
                }
        elif (self.core_root / 'SKILL.md').is_file():
            raw = (self.core_root / 'SKILL.md').read_text(encoding='utf-8')
            meta, _ = parse_frontmatter(raw)
            name = meta.get('name') or 'delphi-behavior-contracts'
            skills[name] = {
                'name': name,
                'description': meta.get('description', ''),
                'uri': f'skill://{name}/SKILL.md',
                'digest': 'sha256:' + hashlib.sha256(raw.encode('utf-8')).hexdigest(),
                'words': len(raw.split()),
                'content': raw,
            }
        self._skills_cache = skills
        return skills

    def skills(self):
        return [
            {k: v for k, v in s.items() if k != 'content'}
            for s in self._load_skills().values()
        ]

    def skill(self, name: str):
        sk = self._load_skills().get(name)
        if not sk:
            raise KeyError(f'Unknown skill: {name}. Available: {sorted(self._load_skills().keys())}')
        return sk

    def chapters(self, lang='en'):
        lang = 'ru' if str(lang).lower() == 'ru' else 'en'
        out = []
        for p in sorted((self.core_root / 'references' / lang / 'chapters').glob('*.md')):
            txt = self._read_text(p)
            first = txt.splitlines()[0] if txt else p.stem
            out.append({
                'id': p.name[:2],
                'slug': p.stem,
                'path': p.relative_to(self.core_root).as_posix(),
                'title': first.lstrip('# ').strip(),
                'lines': txt.count('\n') + 1,
                'words': len(txt.split()),
            })
        return out

    def directives(self, lang='en'):
        lang = 'ru' if str(lang).lower() == 'ru' else 'en'
        out = []
        for p in sorted((self.core_root / 'references' / lang / 'directives').glob('*.md')):
            if p.name == 'INDEX.md':
                continue
            txt = self._read_text(p)
            first = txt.splitlines()[0] if txt else p.stem
            out.append({
                'slug': p.stem,
                'path': p.relative_to(self.core_root).as_posix(),
                'title': first.lstrip('# ').strip(),
                'words': len(txt.split()),
            })
        return out

    def search(self, query: str, lang='en', limit=8, include_issues=False):
        lang = 'ru' if str(lang).lower() == 'ru' else 'en'
        limit = max(1, min(int(limit), 30))
        root = self.core_root / 'references' / lang
        phrase = normalized(query)
        terms = list(dict.fromkeys(re.findall(r'\w+', phrase)))
        if not terms:
            return []
        patterns = {t: re.compile(term_pattern(t, lang)) for t in terms}
        phrase_rx = re.compile(r'\s+'.join(term_pattern(t, lang, open_end=True) for t in re.findall(r'\w+', phrase)))
        files = sorted(list((root / 'chapters').glob('*.md')) + list((root / 'directives').glob('*.md')))
        if include_issues:
            for extra in (root / 'SOURCE_ISSUES.md', root / 'VERIFICATION.md'):
                if extra.is_file():
                    files.append(extra)
            rdir = root / 'research'
            if rdir.is_dir():
                files.extend(sorted(rdir.glob('*.md')))
        matches = []
        for p in files:
            lines = self._read_text(p).splitlines()
            body = normalized(visible(' '.join(lines)))
            counts = {t: len(patterns[t].findall(body)) for t in terms}
            headings = normalized(' '.join(s for s in lines if s.startswith('#')))
            alias = p.parent.name == 'chapters' and p.name[:2] in ALIASES.get(phrase, ())
            directive_name = phrase.strip('{}$ ')
            exact_directive = p.parent.name == 'directives' and directive_name in p.stem.split('-')
            if not alias and not any(counts.values()):
                continue
            score = sum(min(n, 10) for n in counts.values())
            if all(counts.values()):
                score += 35
            if phrase_rx.search(body):
                score += 120
            if phrase_rx.search(headings):
                score += 70
            if exact_directive:
                score += 400
            if alias:
                score += 220 - 10 * ALIASES[phrase].index(p.name[:2])
            if p.name[:2] in {'48', '49'} or p.name == 'INDEX.md':
                score *= 0.12
            snippets = []
            for i, line in enumerate(lines):
                text = normalized(visible(line))
                present = sum(bool(patterns[t].search(text)) for t in terms)
                if present:
                    snippets.append((100 * bool(phrase_rx.search(text)) + present, i, line))
            selected = sorted(snippets, key=lambda x: (-x[0], x[1]))[:4]
            matches.append({
                'path': p.relative_to(self.core_root).as_posix(),
                'title': lines[0].lstrip('# ').strip() if lines else p.stem,
                'score': round(score, 2),
                'matched_terms': [t for t in terms if counts[t]],
                'snippets': [{'line': i + 1, 'text': s} for _, i, s in selected],
            })
        return sorted(matches, key=lambda r: (-r['score'], r['path']))[:limit]

    def resolve_doc_path(self, ref: str, lang='en') -> str:
        lang = 'ru' if str(lang).lower() == 'ru' else 'en'
        clean = ref.strip().lstrip('/')
        if (self.core_root / clean).is_file():
            return clean
        # Shorthand chapter number ("31" or "31-generics")
        if re.fullmatch(r'\d{2}', clean):
            hits = list((self.core_root / 'references' / lang / 'chapters').glob(f'{clean}-*.md'))
            if hits:
                return hits[0].relative_to(self.core_root).as_posix()
        for prefix in (
            f'references/{lang}/chapters/',
            f'references/{lang}/directives/',
            f'references/{lang}/research/',
            f'references/{lang}/',
            'evidence/compiler/',
            'evidence/',
            'examples/',
        ):
            for cand in (prefix + clean, prefix + clean + '.md', prefix + clean.lower().strip('{}$ ') + '.md'):
                if (self.core_root / cand).is_file():
                    return cand
        # Match directive by name inside manifest or stem split
        dname = clean.lower().strip('{}$ ')
        for p in (self.core_root / 'references' / lang / 'directives').glob('*.md'):
            if dname in p.stem.split('-'):
                return p.relative_to(self.core_root).as_posix()
        raise FileNotFoundError(f'Document not found: {ref} (lang={lang})')

    def read(self, ref: str, lang='en', start_line=1, end_line=250):
        rel = self.resolve_doc_path(ref, lang=lang)
        p = self._safe_path(rel)
        lines = self._read_text(p).splitlines()
        total = len(lines)
        s = max(1, int(start_line))
        e = min(total, max(s, int(end_line)))
        return {
            'path': rel,
            'total_lines': total,
            'start_line': s,
            'end_line': e,
            'truncated': e < total,
            'content': '\n'.join(lines[s - 1:e]),
        }

    def chapter(self, id_or_slug: str, lang='en', start_line=1, end_line=400):
        return self.read(str(id_or_slug), lang=lang, start_line=start_line, end_line=end_line)

    def directive(self, name: str, lang='en'):
        return self.read(name.strip('{}$ '), lang=lang, start_line=1, end_line=300)

    def verification(self, lang='en'):
        lang = 'ru' if str(lang).lower() == 'ru' else 'en'
        return self.read(f'references/{lang}/VERIFICATION.md', lang=lang, start_line=1, end_line=400)

    def research(self, name: str, lang='en', start_line=1, end_line=400):
        lang = 'ru' if str(lang).lower() == 'ru' else 'en'
        return self.read(f'references/{lang}/research/{name}', lang=lang, start_line=start_line, end_line=end_line)

    def coverage(self):
        return self._read_json('evidence/coverage.json')

    def issues(self, status=None):
        items = self._read_json('evidence/source_issues.json').get('issues', [])
        if status:
            st = str(status).upper()
            items = [x for x in items if str(x.get('status', '')).upper() == st]
        return items

    def issue(self, issue_id: str):
        needle = issue_id.upper()
        for x in self.issues():
            if str(x.get('id', '')).upper() == needle:
                return x
        raise KeyError(f'Source issue not found: {issue_id}')

    def evidence_files(self):
        cdir = self.core_root / 'evidence' / 'compiler'
        return sorted(p.relative_to(self.core_root).as_posix() for p in cdir.glob('*.json'))

    def evidence(self, file_or_probe_id: str):
        # Direct json file match
        if file_or_probe_id.endswith('.json'):
            rel = file_or_probe_id if file_or_probe_id.startswith('evidence/') else f'evidence/compiler/{file_or_probe_id}'
            return self._read_json(rel)
        # Search probe/case ID across all compiler evidence files
        needle = file_or_probe_id.casefold()
        found = []
        for rel in self.evidence_files():
            data = self._read_json(rel)
            if not isinstance(data, dict):
                continue
            for key in ('probes', 'cases', 'positive_examples', 'negative_cases', 'observations'):
                arr = data.get(key)
                if isinstance(arr, list):
                    for item in arr:
                        if not isinstance(item, dict):
                            continue
                        iid = str(item.get('id') or item.get('case_id') or item.get('name') or '')
                        if needle in iid.casefold():
                            found.append({'receipt': rel, 'collection': key, 'entry': item})
                            if len(found) >= 15:
                                return found
        return found


# ---------------- Restricted AST Code Mode Sandbox ----------------

ALLOWED_BUILTINS = {
    'abs': abs, 'all': all, 'any': any, 'bool': bool, 'dict': dict,
    'enumerate': enumerate, 'filter': filter, 'float': float, 'int': int,
    'isinstance': isinstance, 'len': len, 'list': list, 'map': map,
    'max': max, 'min': min, 'range': range, 'reversed': reversed,
    'round': round, 'set': set, 'sorted': sorted, 'str': str, 'sum': sum,
    'tuple': tuple, 'zip': zip, 'True': True, 'False': False, 'None': None,
}

FORBIDDEN_AST = (
    ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal,
    ast.Delete, ast.AsyncFunctionDef, ast.AsyncFor, ast.AsyncWith,
    ast.Await, ast.With, ast.ClassDef, ast.Yield, ast.YieldFrom,
)

FORBIDDEN_NAMES = {
    '__import__', '__builtins__', '__loader__', '__spec__', '__name__',
    '__file__', '__class__', '__bases__', '__subclasses__', '__mro__',
    '__globals__', '__code__', '__closure__', '__dict__', '__getattribute__',
    'eval', 'exec', 'compile', 'open', 'input', 'getattr', 'setattr', 'delattr',
    'globals', 'locals', 'vars', 'dir', 'breakpoint', 'help', 'memoryview', 'type',
}


def validate_ast(tree: ast.AST):
    node_count = 0
    for node in ast.walk(tree):
        node_count += 1
        if node_count > 600:
            raise ValueError('Code exceeds sandbox AST node budget (max 600 nodes).')
        if isinstance(node, FORBIDDEN_AST):
            raise ValueError(f'Forbidden construct in sandbox: {type(node).__name__}')
        if isinstance(node, ast.Name) and (node.id in FORBIDDEN_NAMES or node.id.startswith('__')):
            raise ValueError(f'Forbidden identifier in sandbox: {node.id}')
        if isinstance(node, ast.Attribute) and node.attr.startswith('_'):
            raise ValueError(f'Private/dunder attribute access forbidden: .{node.attr}')


class SafeDelphiSDK:
    """Strict read-only proxy exposed as `delphi` inside Code Mode."""

    def __init__(self, corpus: DelphiCorpus):
        self._c = corpus

    def search(self, query, lang='en', limit=8, include_issues=False):
        return self._c.search(query, lang=lang, limit=limit, include_issues=include_issues)

    def chapters(self, lang='en'):
        return self._c.chapters(lang=lang)

    def chapter(self, id_or_slug, lang='en', start_line=1, end_line=400):
        return self._c.chapter(id_or_slug, lang=lang, start_line=start_line, end_line=end_line)

    def directives(self, lang='en'):
        return self._c.directives(lang=lang)

    def directive(self, name, lang='en'):
        return self._c.directive(name, lang=lang)

    def read(self, ref, lang='en', start_line=1, end_line=250):
        return self._c.read(ref, lang=lang, start_line=start_line, end_line=end_line)

    def verification(self, lang='en'):
        return self._c.verification(lang=lang)

    def research(self, name, lang='en', start_line=1, end_line=400):
        return self._c.research(name, lang=lang, start_line=start_line, end_line=end_line)

    def coverage(self):
        return self._c.coverage()

    def issues(self, status=None):
        return self._c.issues(status=status)

    def issue(self, issue_id):
        return self._c.issue(issue_id)

    def evidence_files(self):
        return self._c.evidence_files()

    def evidence(self, file_or_probe_id):
        return self._c.evidence(file_or_probe_id)

    def skills(self):
        return self._c.skills()

    def skill(self, name):
        return self._c.skill(name)


def run_code_mode(corpus: DelphiCorpus, code: str, truncate: bool = True):
    code = code.strip()
    if not code:
        raise ValueError('Empty code payload.')
    if len(code) > 12000:
        raise ValueError('Code payload too large (max 12,000 chars).')
    tree = ast.parse(code, mode='exec')
    validate_ast(tree)
    sdk = SafeDelphiSDK(corpus)
    env = {'__builtins__': ALLOWED_BUILTINS, 'delphi': sdk, 're': None}
    # Safe regex helpers without exposing re module internals
    env['regex_find'] = lambda pat, text: re.findall(str(pat), str(text))[:200]
    env['regex_match'] = lambda pat, text: bool(re.search(str(pat), str(text)))
    # If the last statement is a bare expression, capture its value as `_expr_result`
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        last_expr = tree.body.pop()
        tree.body.append(ast.Assign(targets=[ast.Name(id='_expr_result', ctx=ast.Store())], value=last_expr.value))
        ast.fix_missing_locations(tree)
    compiled = compile(tree, '<delphi-codemode>', 'exec')
    exec(compiled, env, env)
    if 'run' in env and callable(env['run']):
        out = env['run'](sdk)
    elif 'result' in env:
        out = env['result']
    elif '_expr_result' in env:
        out = env['_expr_result']
    else:
        out = {'status': 'executed', 'note': 'Assign to `result`, write a final expression, or define `def run(delphi): ...`.'}
    rendered = json.dumps(out, ensure_ascii=False, indent=2, default=str)
    if truncate and len(rendered) > 24000:
        rendered = rendered[:24000] + '\n... [truncated; pass truncate=false or narrow your query]'
    return rendered


# ---------------- MCP Protocol Dispatcher ----------------

TOOLS = [
    {
        'name': 'delphi_search',
        'description': (
            'Search Delphi Behavior Contracts (74 chapters + 89 directive cards, EN/RU, '
            'optionally SOURCE_ISSUES & research passes). Returns ranked paths, titles, scores and line snippets.'
        ),
        'inputSchema': {
            'type': 'object',
            'properties': {
                'query': {'type': 'string', 'description': 'Topic, syntax, directive, or error code (e.g. "dynamic array", "HasWeakRef", "$WARN", "динамический массив").'},
                'lang': {'type': 'string', 'enum': ['en', 'ru'], 'default': 'en'},
                'limit': {'type': 'integer', 'minimum': 1, 'maximum': 30, 'default': 8},
                'include_issues': {'type': 'boolean', 'default': False, 'description': 'Also search SOURCE_ISSUES.md, VERIFICATION.md and research/.'},
            },
            'required': ['query'],
        },
    },
    {
        'name': 'delphi_read',
        'description': (
            'Read a specific chapter, directive card, verification record, source issue doc, or example file by path or shorthand '
            '(e.g. "31", "10-arrays.md", "warn", "VERIFICATION.md", "references/en/chapters/73-evolution-old-to-new.md").'
        ),
        'inputSchema': {
            'type': 'object',
            'properties': {
                'path': {'type': 'string'},
                'lang': {'type': 'string', 'enum': ['en', 'ru'], 'default': 'en'},
                'start_line': {'type': 'integer', 'minimum': 1, 'default': 1},
                'end_line': {'type': 'integer', 'minimum': 1, 'default': 250},
            },
            'required': ['path'],
        },
    },
    {
        'name': 'delphi_skill',
        'description': (
            'Load one of the 5 specialist Delphi Behavior Contracts skills (or list all skills): '
            'delphi-behavior-contracts, delphi-migration, delphi-legacy-upgrade, delphi-directives, delphi-code-review.'
        ),
        'inputSchema': {
            'type': 'object',
            'properties': {
                'name': {'type': 'string', 'description': 'Skill name; omit or set list_only=true to list available skills.'},
                'list_only': {'type': 'boolean', 'default': False},
            },
        },
    },
    {
        'name': 'delphi_execute',
        'description': (
            'Code Mode: run a short read-only Python snippet in an AST-restricted sandbox against the `delphi` SDK '
            'to query multiple chapters, directives, source_issues and 879+ compiler evidence receipts in one call '
            'and return only the distilled result. Available on `delphi`: search(query, lang, limit, include_issues), '
            'chapters(lang), chapter(id, lang, start_line, end_line), directives(lang), directive(name, lang), '
            'read(ref, lang, start_line, end_line), verification(lang), research(name, lang), coverage(), '
            'issues(status), issue(id), evidence_files(), evidence(file_or_probe_id), skills(), skill(name). '
            'Helpers: regex_find(pat, text), regex_match(pat, text). Assign `result = ...`, end with an expression, or define `def run(delphi): ...`.'
        ),
        'inputSchema': {
            'type': 'object',
            'properties': {
                'code': {'type': 'string', 'description': 'Read-only Python code using `delphi`.'},
                'truncate': {'type': 'boolean', 'default': True},
            },
            'required': ['code'],
        },
    },
]


class McpDispatcher:
    def __init__(self, corpus: DelphiCorpus):
        self.corpus = corpus

    def handle(self, req: dict):
        if not isinstance(req, dict):
            return self._err(None, -32600, 'Invalid Request')
        req_id = req.get('id')
        method = req.get('method', '')
        params = req.get('params') or {}

        # Notifications have no id and expect no response
        if req_id is None and method.startswith('notifications/'):
            return None

        try:
            if method == 'initialize':
                return self._ok(req_id, {
                    'protocolVersion': PROTOCOL_VERSION,
                    'serverInfo': SERVER_INFO,
                    'capabilities': {
                        'tools': {'listChanged': False},
                        'resources': {'subscribe': False, 'listChanged': False},
                        'prompts': {'listChanged': False},
                        'experimental': {
                            'io.modelcontextprotocol/skills': {'listChanged': False},
                        },
                    },
                    'instructions': (
                        'Delphi Behavior Contracts MCP Server (v1.0.0, edition 1.5.2). '
                        'Use `delphi_search` or `delphi_execute` (Code Mode) to verify exact compiler-measured Delphi behavior '
                        'before explaining, reviewing, upgrading, or porting Delphi code. Load specialist playbooks via `delphi_skill` or `skills/list`.'
                    ),
                })

            if method == 'ping':
                return self._ok(req_id, {})

            if method == 'tools/list':
                return self._ok(req_id, {'tools': TOOLS})

            if method == 'tools/call':
                name = params.get('name')
                args = params.get('arguments') or {}
                if name == 'delphi_search':
                    data = self.corpus.search(
                        args['query'],
                        lang=args.get('lang', 'en'),
                        limit=args.get('limit', 8),
                        include_issues=bool(args.get('include_issues', False)),
                    )
                    return self._tool_text(req_id, json.dumps({'query': args['query'], 'matches': data}, ensure_ascii=False, indent=2))
                if name == 'delphi_read':
                    data = self.corpus.read(
                        args['path'],
                        lang=args.get('lang', 'en'),
                        start_line=args.get('start_line', 1),
                        end_line=args.get('end_line', 250),
                    )
                    return self._tool_text(req_id, json.dumps(data, ensure_ascii=False, indent=2))
                if name == 'delphi_skill':
                    if args.get('list_only') or not args.get('name'):
                        return self._tool_text(req_id, json.dumps({'skills': self.corpus.skills()}, ensure_ascii=False, indent=2))
                    sk = self.corpus.skill(args['name'])
                    return self._tool_text(req_id, sk['content'])
                if name == 'delphi_execute':
                    out = run_code_mode(self.corpus, args['code'], truncate=bool(args.get('truncate', True)))
                    return self._tool_text(req_id, out)
                return self._err(req_id, -32601, f'Unknown tool: {name}')

            # SEP-2640 Skills over MCP
            if method == 'skills/list':
                return self._ok(req_id, {'skills': self.corpus.skills()})

            if method == 'skills/get':
                name = params.get('name', '')
                sk = self.corpus.skill(name)
                return self._ok(req_id, sk)

            if method == 'resources/list':
                res = []
                for sk in self.corpus.skills():
                    res.append({
                        'uri': sk['uri'],
                        'name': sk['name'],
                        'description': sk['description'],
                        'mimeType': 'text/markdown',
                    })
                for uri, title, mime in [
                    ('delphi://en/INDEX.md', 'Topic Map (EN, 74 chapters)', 'text/markdown'),
                    ('delphi://ru/INDEX.md', 'Topic Map (RU, 74 chapters)', 'text/markdown'),
                    ('delphi://en/VERIFICATION.md', 'Verification Record (EN)', 'text/markdown'),
                    ('delphi://ru/VERIFICATION.md', 'Verification Record (RU)', 'text/markdown'),
                    ('delphi://en/SOURCE_ISSUES.md', 'Source Issues Registry (EN)', 'text/markdown'),
                    ('delphi://ru/SOURCE_ISSUES.md', 'Source Issues Registry (RU)', 'text/markdown'),
                    ('delphi://evidence/coverage.json', 'Coverage Baseline JSON', 'application/json'),
                    ('delphi://evidence/source_issues.json', 'Source Issues Machine JSON', 'application/json'),
                ]:
                    res.append({'uri': uri, 'name': title, 'mimeType': mime})
                return self._ok(req_id, {'resources': res})

            if method == 'resources/read':
                uri = params.get('uri', '')
                if uri.startswith('skill://'):
                    parts = uri[len('skill://'):].split('/', 1)
                    sk = self.corpus.skill(parts[0])
                    return self._ok(req_id, {'contents': [{'uri': uri, 'mimeType': 'text/markdown', 'text': sk['content']}]})
                if uri.startswith('delphi://'):
                    sub = uri[len('delphi://'):]
                    if sub.startswith(('en/', 'ru/')):
                        rel = 'references/' + sub
                    else:
                        rel = sub
                    p = self.corpus._safe_path(rel)
                    mime = 'application/json' if p.suffix == '.json' else 'text/markdown'
                    return self._ok(req_id, {'contents': [{'uri': uri, 'mimeType': mime, 'text': self.corpus._read_text(p)}]})
                return self._err(req_id, -32602, f'Unsupported URI: {uri}')

            if method == 'prompts/list':
                prompts = [
                    {
                        'name': sk['name'],
                        'description': sk['description'],
                        'arguments': [{'name': 'task', 'description': 'Delphi code, question, or migration target', 'required': False}],
                    }
                    for sk in self.corpus.skills()
                ]
                return self._ok(req_id, {'prompts': prompts})

            if method == 'prompts/get':
                name = params.get('name', '')
                task = (params.get('arguments') or {}).get('task', '')
                sk = self.corpus.skill(name)
                text = sk['content'] + (f'\n\n## User Task\n{task}\n' if task else '')
                return self._ok(req_id, {
                    'description': sk['description'],
                    'messages': [{'role': 'user', 'content': {'type': 'text', 'text': text}}],
                })

            return self._err(req_id, -32601, f'Method not found: {method}')
        except Exception as exc:
            if method == 'tools/call':
                return self._ok(req_id, {
                    'isError': True,
                    'content': [{'type': 'text', 'text': f'Error: {type(exc).__name__}: {exc}'}],
                })
            return self._err(req_id, -32000, f'{type(exc).__name__}: {exc}')

    @staticmethod
    def _ok(req_id, result):
        return {'jsonrpc': '2.0', 'id': req_id, 'result': result}

    @staticmethod
    def _err(req_id, code, message):
        return {'jsonrpc': '2.0', 'id': req_id, 'error': {'code': code, 'message': message}}

    @staticmethod
    def _tool_text(req_id, text):
        return {
            'jsonrpc': '2.0',
            'id': req_id,
            'result': {'content': [{'type': 'text', 'text': text}]},
        }


# ---------------- stdio & Streamable HTTP Transports ----------------

def run_stdio(dispatcher: McpDispatcher):
    stdin = sys.stdin.buffer
    stdout = sys.stdout.buffer
    use_lsp_framing = False

    def send(msg):
        raw = json.dumps(msg, ensure_ascii=False).encode('utf-8')
        if use_lsp_framing:
            stdout.write(f'Content-Length: {len(raw)}\r\n\r\n'.encode('ascii') + raw)
        else:
            stdout.write(raw + b'\n')
        stdout.flush()

    while True:
        line = stdin.readline()
        if not line:
            break
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.lower().startswith(b'content-length:'):
            use_lsp_framing = True
            length = int(stripped.split(b':', 1)[1].strip())
            while True:
                h = stdin.readline()
                if not h or h in (b'\r\n', b'\n'):
                    break
            body = stdin.read(length)
        else:
            body = stripped
        try:
            req = json.loads(body.decode('utf-8'))
        except Exception as exc:
            send(dispatcher._err(None, -32700, f'Parse error: {exc}'))
            continue
        resp = dispatcher.handle(req)
        if resp is not None:
            send(resp)


def run_http(dispatcher: McpDispatcher, host: str, port: int, api_key: str | None):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        def _check_auth(self):
            if not api_key:
                return True
            auth = self.headers.get('Authorization', '')
            token = auth[7:].strip() if auth.startswith('Bearer ') else ''
            if not token:
                qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                token = (qs.get('key') or [''])[0]
            return hmac.compare_digest(token.encode('utf-8'), api_key.encode('utf-8'))

        def _send_json(self, status, payload):
            raw = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(raw)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, Mcp-Session-Id')
            self.end_headers()
            self.wfile.write(raw)

        def do_OPTIONS(self):
            self.send_response(204)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, Mcp-Session-Id')
            self.end_headers()

        def do_GET(self):
            path = urllib.parse.urlparse(self.path).path
            if path in ('/', '/health'):
                self._send_json(200, {
                    'status': 'ok',
                    'server': SERVER_INFO,
                    'endpoint': '/mcp',
                    'tools': [t['name'] for t in TOOLS],
                    'skills_over_mcp': True,
                })
                return
            self._send_json(404, {'error': 'Not found. Use POST /mcp.'})

        def do_POST(self):
            path = urllib.parse.urlparse(self.path).path
            if path != '/mcp':
                self._send_json(404, {'error': 'Use POST /mcp'})
                return
            if not self._check_auth():
                self._send_json(401, {'error': 'Unauthorized'})
                return
            length = int(self.headers.get('Content-Length', '0'))
            body = self.rfile.read(length)
            try:
                req = json.loads(body.decode('utf-8'))
            except Exception as exc:
                self._send_json(400, dispatcher._err(None, -32700, f'Parse error: {exc}'))
                return
            if isinstance(req, list):
                replies = [r for r in (dispatcher.handle(item) for item in req) if r is not None]
                self._send_json(200, replies)
                return
            resp = dispatcher.handle(req)
            if resp is None:
                self.send_response(202)
                self.end_headers()
                return
            self._send_json(200, resp)

    server = ThreadingHTTPServer((host, port), Handler)
    print(json.dumps({'status': 'listening', 'url': f'http://{host}:{port}/mcp', 'core': str(dispatcher.corpus.core_root)}), flush=True)
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description='Delphi Behavior Contracts Local MCP Server')
    parser.add_argument('--root', help='Path to corpus root (contains references/en/chapters)')
    parser.add_argument('--http', action='store_true', help='Serve Streamable HTTP instead of stdio')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8788)
    parser.add_argument('--api-key', default=os.environ.get('DELPHI_MCP_API_KEY'))
    args = parser.parse_args()

    core_root, skills_root = resolve_roots(args.root)
    corpus = DelphiCorpus(core_root, skills_root)
    dispatcher = McpDispatcher(corpus)
    if args.http:
        run_http(dispatcher, args.host, args.port, args.api_key)
    else:
        run_stdio(dispatcher)


if __name__ == '__main__':
    main()
