#!/usr/bin/env python3
"""Universal installer and standalone-zip exporter for Delphi Behavior Contracts Suite (v1.0.1).

Explicitly distinguishes PLUGINS (`--plugin` / `--export-plugin`) from pure SKILLS (`--skill` / `--export-skill`)!
Zero external dependencies (Python 3.8+ standard library only).

Examples:
  python install.py --list
  # Install a NATIVE PLUGIN:
  python install.py --plugin antigravity
  python install.py --plugin codex
  python install.py --plugin claude
  python install.py --plugin gemini
  python install.py --plugin cursor --scope project --project-dir /path/to/delphi-repo
  python install.py --plugin copilot --scope project --project-dir /path/to/delphi-repo
  # Install PURE SKILLS (without plugin wrapper):
  python install.py --skill antigravity
  python install.py --skill codex
  python install.py --skill claude
  python install.py --skill windsurf --scope project --project-dir /path/to/delphi-repo
  python install.py --skill all --scope project --project-dir /path/to/delphi-repo
  # Export self-contained standalone zips (for direct UI upload):
  python install.py --export-plugin claude ./delphi-claude-plugin.zip
  python install.py --export-plugin antigravity ./delphi-antigravity-plugin.zip
  python install.py --export-plugin codex ./delphi-codex-plugin.zip
  python install.py --export-skill single ./delphi-single-skill.zip
  python install.py --export-skill 5-skills ./delphi-5-skills.zip
"""
from pathlib import Path
import argparse
import json
import re
import shutil
import tempfile
import zipfile

SUITE_ROOT = Path(__file__).resolve().parent
CORE_DIR = SUITE_ROOT / 'core'
PLUGINS_DIR = SUITE_ROOT / 'plugins'
SKILLS_DIR = SUITE_ROOT / 'skills'

PLUGINS = {
    'claude':             ('claude-code',           'Claude Code / Claude Desktop plugin (.claude-plugin + .mcp.json + 5 skills)'),
    'claude-marketplace': ('claude-marketplace',    'Claude Code Marketplace (.claude-plugin/marketplace.json + plugin)'),
    'codex':              ('codex',                 'OpenAI Codex plugin (.codex-plugin/plugin.json + interface + .mcp.json + 5 skills)'),
    'codex-marketplace':  ('codex-marketplace',     'OpenAI Codex Marketplace (.agents/plugins/marketplace.json + plugin)'),
    'antigravity':        ('antigravity',           'Google Antigravity plugin (plugin.json + logo + rules + mcp_config.json + 5 skills)'),
    'gemini':             ('gemini-cli-extension',  'Google Gemini CLI extension (gemini-extension.json + GEMINI.md + commands/*.toml + 5 skills)'),
    'cursor':             ('cursor-plugin',         'Cursor plugin (.cursor-plugin/plugin.json + .cursor/rules/*.mdc + skills + mcp.json)'),
    'copilot':            ('copilot-vscode-bundle', 'GitHub Copilot & VS Code bundle (instructions + 5 agents + skills + .vscode/mcp.json + .mcp.json)'),
}

SKILLS = {
    'single':       ('single-skill',                         'Universal AAIF single skill (SKILL.md + agents/openai.yaml — Claude App / skills.sh)'),
    '5-skills':     ('5-specialist-skills',                  '5 pure AAIF specialist skills (no plugin manifest)'),
    'claude':       ('by-platform/claude-skills',            'Pure Claude skills (.claude/skills/<5 skills>)'),
    'codex':        ('by-platform/codex-skills',             'Pure Codex skills (.agents/skills/<5 skills> + AGENTS.md)'),
    'antigravity':  ('by-platform/antigravity-skills',       'Pure Antigravity skills (.gemini/skills/<5 skills>)'),
    'gemini':       ('by-platform/gemini-cli-skills',        'Pure Gemini CLI skills (.gemini/skills/<5 skills> + GEMINI.md)'),
    'cursor':       ('by-platform/cursor-rules-skills',      'Pure Cursor rules & skills (.cursor/rules/*.mdc + .cursor/skills)'),
    'copilot':      ('by-platform/copilot-skills',           'Pure Copilot skills & instructions (.github/skills + instructions)'),
    'windsurf':     ('by-platform/windsurf-rules-skills',    'Windsurf rules, skills & workflows (.windsurf/)'),
    'cline-roo':    ('by-platform/cline-roo-kilo',           'Cline / Roo Code / Kilo Code rules & skills'),
    'opencode':     ('by-platform/opencode-amp-droid',       'OpenCode / Amp / Factory Droid skills & AGENTS.md'),
    'jetbrains':    ('by-platform/jetbrains-junie-ai',       'JetBrains Junie & AI Assistant rules'),
    'kiro':         ('by-platform/kiro-amazon-q',            'AWS Kiro steering & Amazon Q rules'),
    'aider-continue-goose': ('by-platform/aider-continue-goose', 'Aider / Continue / Goose rules'),
    'web-chats':    ('by-platform/web-chats',                'ChatGPT Custom GPT, Claude Projects, Gemini Gems, NotebookLM prompts'),
}


def materialize_text(text: str, suite_path: Path, mcp_mode: str, api_key: str | None) -> str:
    sp = suite_path.as_posix()
    text = text.replace('<SUITE_PATH>', sp)
    text = text.replace('${CLAUDE_PLUGIN_ROOT}/mcp/local-mcp/server.py', f'{sp}/mcp/local-mcp/server.py')
    text = text.replace('${extensionPath}/mcp/local-mcp/server.py', f'{sp}/mcp/local-mcp/server.py')
    if mcp_mode and mcp_mode.startswith(('http://', 'https://')):
        text = re.sub(r'https://delphi-behavior-contracts-mcp\.<your-subdomain>\.workers\.dev/mcp', mcp_mode, text)
    if api_key:
        text = text.replace('${DELPHI_MCP_KEY}', api_key).replace('${env:DELPHI_MCP_KEY}', api_key).replace('{env:DELPHI_MCP_KEY}', api_key)
    return text


def copy_tree_materialized(src: Path, dst: Path, suite_path: Path, mcp_mode: str, api_key: str | None):
    core_posix = (suite_path / 'core').as_posix()
    for p in sorted(src.rglob('*')):
        rel = p.relative_to(src)
        target = dst / rel
        if p.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix.lower() in {'.md', '.mdc', '.json', '.toml', '.yaml', '.yml', '.goosehints', '.txt'}:
            txt = materialize_text(p.read_text(encoding='utf-8'), suite_path, mcp_mode, api_key)
            txt = re.sub(r'(?:\.\./)+core/', core_posix + '/', txt)
            txt = txt.replace('python scripts/lookup.py', f'python "{core_posix}/scripts/lookup.py"')
            target.write_text(txt, encoding='utf-8', newline='\n')
        else:
            shutil.copy2(p, target)


def default_plugin_user_dest(name: str) -> Path:
    home = Path.home()
    return {
        'antigravity': home / '.gemini' / 'config' / 'plugins' / 'delphi-behavior-contracts',
        'gemini': home / '.gemini' / 'extensions' / 'delphi-behavior-contracts',
        'codex': home / '.codex' / 'plugins' / 'delphi-behavior-contracts',
        'codex-marketplace': home / '.codex' / 'marketplaces' / 'delphi-behavior-contracts',
        'claude': home / '.claude' / 'plugins' / 'delphi-behavior-contracts',
        'claude-marketplace': home / '.claude' / 'marketplaces' / 'delphi-behavior-contracts',
    }.get(name, home / '.agents' / 'plugins' / 'delphi-behavior-contracts' / name)


def default_skill_user_dest(name: str) -> Path:
    home = Path.home()
    return {
        'single': home / '.agents' / 'skills' / 'delphi-behavior-contracts',
        '5-skills': home / '.agents' / 'skills',
        'claude': home / '.claude' / 'skills',
        'codex': home / '.codex' / 'skills',
        'antigravity': home / '.gemini' / 'antigravity' / 'skills',
        'gemini': home / '.gemini' / 'skills',
    }.get(name, home / '.agents' / 'skills' / 'delphi-behavior-contracts' / name)


def _populate_standalone(src: Path, dst: Path, include_mcp: bool, mcp_mode: str, api_key: str | None):
    shutil.copytree(CORE_DIR, dst, dirs_exist_ok=True)
    if include_mcp:
        shutil.copytree(SUITE_ROOT / 'mcp' / 'local-mcp', dst / 'mcp' / 'local-mcp', dirs_exist_ok=True)
    for p in sorted(src.rglob('*')):
        if not p.is_file():
            continue
        rel = p.relative_to(src)
        target_file = dst / rel
        target_file.parent.mkdir(parents=True, exist_ok=True)
        if p.suffix.lower() in {'.md', '.mdc', '.json', '.toml', '.yaml', '.yml', '.goosehints', '.txt'}:
            txt = p.read_text(encoding='utf-8')
            depth = len(rel.parts) - 1
            up = ('../' * depth) if depth > 0 else ''
            txt = re.sub(r'(?:\.\./)+core/', up, txt)
            txt = txt.replace('<SUITE_PATH>/mcp/local-mcp/server.py', './mcp/local-mcp/server.py')
            if mcp_mode and mcp_mode.startswith(('http://', 'https://')):
                txt = re.sub(r'https://delphi-behavior-contracts-mcp\.<your-subdomain>\.workers\.dev/mcp', mcp_mode, txt)
            if api_key:
                txt = txt.replace('${DELPHI_MCP_KEY}', api_key).replace('${env:DELPHI_MCP_KEY}', api_key)
            target_file.write_text(txt, encoding='utf-8', newline='\n')
        else:
            shutil.copy2(p, target_file)


def export_zip(kind: str, name: str, out_zip: Path, mcp_mode: str, api_key: str | None):
    out_zip = out_zip.resolve()
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        if kind == 'plugin':
            rel_folder, _ = PLUGINS[name]
            src = PLUGINS_DIR / rel_folder
            if name == 'claude-marketplace':
                root_name = 'delphi-behavior-contracts-marketplace'
                shutil.copytree(src, td_path / root_name)
                _populate_standalone(PLUGINS_DIR / 'claude-code', td_path / root_name / 'plugins' / 'delphi-behavior-contracts', True, mcp_mode, api_key)
            elif name == 'codex-marketplace':
                root_name = 'delphi-behavior-contracts-codex-marketplace'
                shutil.copytree(src, td_path / root_name)
                _populate_standalone(PLUGINS_DIR / 'codex', td_path / root_name / 'plugins' / 'delphi-behavior-contracts', True, mcp_mode, api_key)
            else:
                root_name = 'delphi-behavior-contracts'
                _populate_standalone(src, td_path / root_name, True, mcp_mode, api_key)
        else:
            rel_folder, _ = SKILLS[name]
            src = SKILLS_DIR / rel_folder
            root_name = 'delphi-behavior-contracts'
            _populate_standalone(src, td_path / root_name, False, mcp_mode, api_key)

        if out_zip.exists():
            out_zip.unlink()
        count = 0
        with zipfile.ZipFile(out_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
            for p in sorted((td_path / root_name).rglob('*')):
                if p.is_file():
                    zf.write(p, p.relative_to(td_path).as_posix())
                    count += 1
        print(json.dumps({'status': 'EXPORTED', 'kind': kind, 'name': name, 'zip': str(out_zip), 'files': count, 'bytes': out_zip.stat().st_size}, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description='Install or export Delphi Behavior Contracts PLUGINS or pure SKILLS.')
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--plugin', help='Install a native plugin (see --list, or "all")')
    parser.add_argument('--skill', help='Install pure standalone skills/rules (see --list, or "all")')
    parser.add_argument('--scope', choices=('user', 'project'), default='user')
    parser.add_argument('--project-dir', help='Target Delphi repository directory when --scope project')
    parser.add_argument('--mcp', default='local')
    parser.add_argument('--api-key')
    parser.add_argument('--standalone', action='store_true', help='Copy core/ (and local-mcp for plugins) directly into target dir instead of referencing the extracted suite path (no symlinks)')
    parser.add_argument('--export-plugin', nargs=2, metavar=('NAME', 'OUT_ZIP'))
    parser.add_argument('--export-skill', nargs=2, metavar=('NAME', 'OUT_ZIP'))
    args = parser.parse_args()

    if args.list:
        print('=== NATIVE PLUGINS (`plugins/`) ===')
        for k, (f, d) in PLUGINS.items():
            print(f'  --plugin {k:20s} | plugins/{f:24s} | {d}')
        print('\n=== PURE STANDALONE SKILLS & RULES (`skills/`) ===')
        for k, (f, d) in SKILLS.items():
            print(f'  --skill  {k:20s} | skills/{f:32s} | {d}')
        return

    if args.export_plugin:
        name, oz = args.export_plugin
        if name not in PLUGINS:
            parser.error(f'Unknown plugin: {name}')
        export_zip('plugin', name, Path(oz), args.mcp, args.api_key)
        return

    if args.export_skill:
        name, oz = args.export_skill
        if name not in SKILLS:
            parser.error(f'Unknown skill: {name}')
        export_zip('skill', name, Path(oz), args.mcp, args.api_key)
        return

    if args.plugin:
        names = ['antigravity', 'codex', 'claude', 'gemini'] if (args.plugin == 'all' and args.scope == 'user') else (
            ['cursor', 'copilot'] if (args.plugin == 'all' and args.scope == 'project') else [args.plugin]
        )
        for n in names:
            if n not in PLUGINS:
                parser.error(f'Unknown plugin: {n}')
            src = PLUGINS_DIR / PLUGINS[n][0]
            dst = Path(args.project_dir).resolve() if args.scope == 'project' else default_plugin_user_dest(n)
            if args.standalone:
                if n == 'claude-marketplace':
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                    _populate_standalone(PLUGINS_DIR / 'claude-code', dst / 'plugins' / 'delphi-behavior-contracts', True, args.mcp, args.api_key)
                elif n == 'codex-marketplace':
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                    _populate_standalone(PLUGINS_DIR / 'codex', dst / 'plugins' / 'delphi-behavior-contracts', True, args.mcp, args.api_key)
                else:
                    _populate_standalone(src, dst, True, args.mcp, args.api_key)
            else:
                copy_tree_materialized(src, dst, SUITE_ROOT, args.mcp, args.api_key)
            print(f'[PLUGIN INSTALLED] {n} -> {dst}')

    if args.skill:
        names = ['single', 'claude', 'codex', 'antigravity', 'gemini'] if (args.skill == 'all' and args.scope == 'user') else (
            [k for k in SKILLS if k not in {'single', '5-skills', 'web-chats'}] if (args.skill == 'all' and args.scope == 'project') else [args.skill]
        )
        for n in names:
            if n not in SKILLS:
                parser.error(f'Unknown skill: {n}')
            rel_f = SKILLS[n][0]
            src = SKILLS_DIR / rel_f
            if args.scope == 'user' and n in {'claude', 'codex', 'antigravity', 'gemini'}:
                # Copy inner skill folders directly into user skills dir (~/.claude/skills, ~/.codex/skills, etc.)
                inner = {'claude': '.claude/skills', 'codex': '.agents/skills', 'antigravity': '.gemini/skills', 'gemini': '.gemini/skills'}[n]
                src = src / inner
            dst = Path(args.project_dir).resolve() if args.scope == 'project' else default_skill_user_dest(n)
            if args.standalone:
                _populate_standalone(src, dst, False, args.mcp, args.api_key)
            else:
                copy_tree_materialized(src, dst, SUITE_ROOT, args.mcp, args.api_key)
            print(f'[SKILL INSTALLED] {n} -> {dst}')

    if not args.plugin and not args.skill:
        parser.print_help()


if __name__ == '__main__':
    main()
