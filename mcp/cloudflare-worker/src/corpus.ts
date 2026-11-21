export interface CorpusDoc {
  kind: "chapter" | "directive" | "research" | "meta";
  slug: string;
  id: string;
  path: string;
  title: string;
  lines: number;
  words: number;
  content: string;
}

export interface SkillEntry {
  name: string;
  description: string;
  uri: string;
  digest: string;
  words: number;
  content: string;
}

export interface EvidenceIndex {
  files: string[];
  total_entries: number;
  entries: Array<{
    id: string;
    receipt: string;
    collection: string;
    target: string | null;
    status: string | null;
  }>;
}

export interface SearchMatch {
  path: string;
  title: string;
  score: number;
  matched_terms: string[];
  snippets: Array<{ line: number; text: string }>;
}

const ALIASES: Record<string, string[]> = {
  "default parameter": ["21"],
  "default parameters": ["21"],
  "параметры по умолчанию": ["21"],
  "property default": ["27"],
  "reference to": ["23"],
  "variant record": ["12", "54"],
  "class property": ["27"],
  "array of const": ["10"],
  "dynamic array": ["10"],
  "dynamic arrays": ["10"],
  "динамический массив": ["10"],
  "динамические массивы": ["10"],
  "open array": ["10"],
  "open arrays": ["10"],
  "открытый массив": ["10"],
  "открытые массивы": ["10"],
  "managed record": ["13"],
  "managed records": ["13"],
  "управляемая запись": ["13"],
  "управляемые записи": ["13"],
  "inline variable": ["16"],
  "inline variables": ["16"],
  nameof: ["67"],
  extended: ["70", "07"],
  hasweakref: ["31", "35"],
  isconstvalue: ["72", "31"],
  gettypekind: ["31"],
  returnaddress: ["34"],
  hidden_virtual: ["41", "59"],
  hiding_member: ["41", "59"],
};

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

export function normalized(text: string): string {
  return text.toLowerCase().replace(/-/g, " ").replace(/\s+/g, " ").trim();
}

function visible(text: string): string {
  return text.replace(/https?:\/\/\S+/g, " ");
}

function stem(term: string, lang: "en" | "ru"): string | null {
  if (lang === "ru" && term.length >= 5) {
    return term.slice(0, Math.max(5, term.length - 2));
  }
  return null;
}

function termPattern(term: string, lang: "en" | "ru", openEnd = false): string {
  const s = stem(term, lang);
  if (s) {
    return `(?<![\\p{L}\\p{N}_])${escapeRegExp(s)}[\\p{L}\\p{N}_]*`;
  }
  return `(?<![\\p{L}\\p{N}_])${escapeRegExp(term)}${openEnd ? "[\\p{L}\\p{N}_]*" : "(?![\\p{L}\\p{N}_])"}`;
}

export function extractWords(phrase: string): string[] {
  return phrase.match(/[\p{L}\p{N}_]+/gu) ?? [];
}

// Read-only in-isolate asset cache (immutable packaged corpus files only)
const assetJsonCache = new Map<string, unknown>();

async function loadAssetJson<T>(assets: Fetcher, assetPath: string): Promise<T> {
  const cached = assetJsonCache.get(assetPath);
  if (cached !== undefined) {
    return cached as T;
  }
  const resp = await assets.fetch(`https://assets.local${assetPath}`);
  if (!resp.ok) {
    throw new Error(`Corpus asset not found: ${assetPath} (${resp.status})`);
  }
  const data = (await resp.json()) as T;
  assetJsonCache.set(assetPath, data);
  return data;
}

export async function getDocs(assets: Fetcher, lang: "en" | "ru"): Promise<CorpusDoc[]> {
  const payload = await loadAssetJson<{ lang: string; docs: CorpusDoc[] }>(assets, `/corpus/docs-${lang}.json`);
  return payload.docs;
}

export async function getSkills(assets: Fetcher): Promise<SkillEntry[]> {
  const payload = await loadAssetJson<{ skills: SkillEntry[] }>(assets, "/corpus/skills.json");
  return payload.skills;
}

export async function getCoverage(assets: Fetcher): Promise<Record<string, unknown>> {
  return loadAssetJson<Record<string, unknown>>(assets, "/corpus/coverage.json");
}

export async function getSourceIssues(assets: Fetcher): Promise<{ issues: Array<Record<string, unknown>> }> {
  return loadAssetJson<{ issues: Array<Record<string, unknown>> }>(assets, "/corpus/source_issues.json");
}

export async function getEvidenceIndex(assets: Fetcher): Promise<EvidenceIndex> {
  return loadAssetJson<EvidenceIndex>(assets, "/corpus/evidence-index.json");
}

export async function getEvidenceReceipt(assets: Fetcher, filename: string): Promise<unknown> {
  const clean = filename.replace(/^evidence\/compiler\//, "").replace(/^\/+/, "");
  if (!/^[A-Za-z0-9._-]+\.json$/.test(clean)) {
    throw new Error(`Invalid evidence filename: ${filename}`);
  }
  return loadAssetJson<unknown>(assets, `/corpus/evidence/${clean}`);
}

export async function searchCorpus(
  assets: Fetcher,
  query: string,
  lang: "en" | "ru" = "en",
  limit = 8,
  includeIssues = false,
): Promise<SearchMatch[]> {
  const docs = await getDocs(assets, lang);
  const phrase = normalized(query);
  const rawTerms = extractWords(phrase);
  const terms = [...new Set(rawTerms)];
  if (terms.length === 0) return [];

  const cappedLimit = Math.max(1, Math.min(limit, 30));
  const patterns = new Map<string, RegExp>();
  for (const t of terms) {
    patterns.set(t, new RegExp(termPattern(t, lang, false), "gu"));
  }
  const phraseRx = new RegExp(
    rawTerms.map((t) => termPattern(t, lang, true)).join("\\s+"),
    "u",
  );
  const directiveName = phrase.replace(/^[{}$ ]+|[{}$ ]+$/g, "");
  const aliasList = ALIASES[phrase] ?? [];

  const matches: SearchMatch[] = [];
  for (const doc of docs) {
    if (!includeIssues && doc.kind !== "chapter" && doc.kind !== "directive") {
      continue;
    }
    if (doc.kind === "directive" && doc.slug === "INDEX") continue;

    const lines = doc.content.split(/\r?\n/);
    const body = normalized(visible(lines.join(" ")));
    const counts: Record<string, number> = {};
    let totalFound = 0;
    for (const t of terms) {
      const m = body.match(patterns.get(t)!);
      const c = m ? m.length : 0;
      counts[t] = c;
      totalFound += c;
    }
    const headings = normalized(lines.filter((l) => l.startsWith("#")).join(" "));
    const aliasIdx = doc.kind === "chapter" ? aliasList.indexOf(doc.id) : -1;
    const isAlias = aliasIdx !== -1;
    const isExactDirective =
      doc.kind === "directive" && doc.slug.split("-").includes(directiveName);

    if (!isAlias && totalFound === 0) continue;

    let score = 0;
    let allPresent = true;
    for (const t of terms) {
      score += Math.min(counts[t], 10);
      if (counts[t] === 0) allPresent = false;
    }
    if (allPresent) score += 35;
    if (phraseRx.test(body)) score += 120;
    if (phraseRx.test(headings)) score += 70;
    if (isExactDirective) score += 400;
    if (isAlias) score += 220 - 10 * aliasIdx;
    if (doc.kind === "chapter" && (doc.id === "48" || doc.id === "49")) {
      score *= 0.12;
    }

    const snippetCands: Array<{ rank: number; line: number; text: string }> = [];
    for (let i = 0; i < lines.length; i++) {
      const lineText = normalized(visible(lines[i]));
      let present = 0;
      for (const t of terms) {
        if (patterns.get(t)!.test(lineText)) {
          present += 1;
          patterns.get(t)!.lastIndex = 0;
        }
      }
      if (present > 0) {
        const rank = (phraseRx.test(lineText) ? 100 : 0) + present;
        snippetCands.push({ rank, line: i + 1, text: lines[i] });
      }
    }
    snippetCands.sort((a, b) => b.rank - a.rank || a.line - b.line);
    matches.push({
      path: doc.path,
      title: doc.title,
      score: Math.round(score * 100) / 100,
      matched_terms: terms.filter((t) => counts[t] > 0),
      snippets: snippetCands.slice(0, 4).map(({ line, text }) => ({ line, text })),
    });
  }

  matches.sort((a, b) => b.score - a.score || a.path.localeCompare(b.path));
  return matches.slice(0, cappedLimit);
}

export async function resolveDoc(
  assets: Fetcher,
  ref: string,
  lang: "en" | "ru" = "en",
): Promise<CorpusDoc> {
  const docs = await getDocs(assets, lang);
  const clean = ref.trim().replace(/^\/+/, "");
  const cleanNoExt = clean.replace(/\.md$/i, "");
  const cleanDirective = cleanNoExt.toLowerCase().replace(/^[{}$ ]+|[{}$ ]+$/g, "");

  // Exact path match across requested language first
  let hit = docs.find((d) => d.path === clean || d.slug === cleanNoExt || d.id === clean);
  if (!hit && /^\d{2}$/.test(clean)) {
    hit = docs.find((d) => d.kind === "chapter" && d.id === clean);
  }
  if (!hit) {
    hit = docs.find(
      (d) =>
        d.kind === "directive" &&
        (d.slug === cleanDirective || d.slug.split("-").includes(cleanDirective)),
    );
  }
  if (!hit) {
    hit = docs.find((d) => d.path.endsWith(`/${clean}`) || d.path.endsWith(`/${clean}.md`));
  }
  // Cross-language fallback if caller passed explicit references/ru/... while lang='en'
  if (!hit && (clean.startsWith("references/ru/") || clean.startsWith("references/en/"))) {
    const otherLang = clean.startsWith("references/ru/") ? "ru" : "en";
    const otherDocs = await getDocs(assets, otherLang);
    hit = otherDocs.find((d) => d.path === clean);
  }
  if (!hit) {
    throw new Error(`Document not found: ${ref} (lang=${lang})`);
  }
  return hit;
}
