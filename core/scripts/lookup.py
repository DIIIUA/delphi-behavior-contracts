"""Local topic search over the Delphi Behavior Contracts reference.

    python scripts/lookup.py "dynamic array"
    python scripts/lookup.py --lang ru "динамический массив"
    python scripts/lookup.py --limit 3 "const out"

Python 3.8+ standard library only. Prints JSON: matching chapters and directive
cards with relative paths, the query terms each match contains, and the
best-matching lines. A result whose matched_terms is shorter than the query matched
only part of it.
"""
from pathlib import Path
import argparse, json, re, sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
# phrase -> chapter numbers, most relevant first (keys are already normalized)
ALIASES = {
    'default parameter': ('21',), 'default parameters': ('21',),
    'параметры по умолчанию': ('21',), 'property default': ('27',),
    'reference to': ('23',), 'variant record': ('12', '54'),
    'class property': ('27',), 'array of const': ('10',),
    'dynamic array': ('10',), 'dynamic arrays': ('10',),
    'динамический массив': ('10',), 'динамические массивы': ('10',),
    'open array': ('10',), 'open arrays': ('10',),
    'открытый массив': ('10',), 'открытые массивы': ('10',),
}


def normalized(text):
    # a hyphen joins words in headings ("Dynamic-array memory"); treat it as a space
    return ' '.join(text.casefold().replace('-', ' ').split())


def visible(text):
    return re.sub(r'https?://\S+', ' ', text)


def stem(term, lang):
    """Russian words change endings by case and number: compare by a prefix stem."""
    if lang == 'ru' and len(term) >= 5:
        return term[:max(5, len(term) - 2)]
    return None


def term_pattern(term, lang, open_end=False):
    """Whole word for counting; open_end lets a phrase word take an ending (record -> records)."""
    s = stem(term, lang)
    if s:
        return r'(?<!\w)' + re.escape(s) + r'\w*'
    return r'(?<!\w)' + re.escape(term) + (r'\w*' if open_end else r'(?!\w)')


def search(query, lang='en', limit=8):
    root = PACKAGE_ROOT / 'references' / lang
    phrase = normalized(query)
    terms = list(dict.fromkeys(re.findall(r'\w+', phrase)))
    if not terms:
        return []
    patterns = {t: re.compile(term_pattern(t, lang)) for t in terms}
    phrase_rx = re.compile(r'\s+'.join(term_pattern(t, lang, open_end=True) for t in re.findall(r'\w+', phrase)))
    matches = []
    files = sorted(list((root / 'chapters').glob('*.md')) + list((root / 'directives').glob('*.md')))
    for p in files:
        lines = p.read_text(encoding='utf-8').splitlines()
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
            score *= .12
        snippets = []
        for i, line in enumerate(lines):
            text = normalized(visible(line))
            present = sum(bool(patterns[t].search(text)) for t in terms)
            if present:
                snippets.append((100 * bool(phrase_rx.search(text)) + present, i, line))
        selected = sorted(snippets, key=lambda x: (-x[0], x[1]))[:4]
        matches.append({
            'path': p.relative_to(PACKAGE_ROOT).as_posix(),
            'title': lines[0][2:] if lines else p.stem,
            'score': round(score, 2),
            'matched_terms': [t for t in terms if counts[t]],
            'snippets': [{'line': i + 1, 'text': s} for _, i, s in selected],
        })
    return sorted(matches, key=lambda r: (-r['score'], r['path']))[:max(1, min(limit, 30))]


if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    a = argparse.ArgumentParser(description='Search the Delphi Behavior Contracts reference.')
    a.add_argument('query')
    a.add_argument('--lang', choices=('en', 'ru'), default='en')
    a.add_argument('--limit', type=int, default=8)
    x = a.parse_args()
    print(json.dumps({'query': x.query, 'language': x.lang, 'terms': list(dict.fromkeys(re.findall(r'\w+', normalized(x.query)))),
                      'matches': search(x.query, x.lang, x.limit)}, ensure_ascii=False, indent=2))
