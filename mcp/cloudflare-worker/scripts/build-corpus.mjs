import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WORKER_ROOT = path.resolve(__dirname, "..");

function findCoreRoot() {
  const explicit = process.env.DELPHI_CONTRACTS_ROOT;
  const candidates = [
    explicit ? path.resolve(explicit) : null,
    path.resolve(WORKER_ROOT, "../../core"),
    path.resolve(WORKER_ROOT, "../../core_src/plugin_unpacked/delphi-behavior-contracts"),
    path.resolve(WORKER_ROOT, "../.."),
  ].filter(Boolean);
  for (const c of candidates) {
    if (fs.existsSync(path.join(c, "references", "en", "chapters"))) {
      return c;
    }
  }
  throw new Error("Could not locate Delphi Behavior Contracts corpus root. Set DELPHI_CONTRACTS_ROOT.");
}

function findSkillsRoot(coreRoot) {
  const candidates = [
    path.join(coreRoot, "skills"),
    path.resolve(WORKER_ROOT, "../../platforms/01-claude-code-plugin/skills"),
    path.resolve(WORKER_ROOT, "../../core_src/plugin_unpacked/delphi-behavior-contracts/skills"),
  ];
  for (const c of candidates) {
    if (fs.existsSync(c)) return c;
  }
  return null;
}

function parseFrontmatter(md) {
  const meta = {};
  if (md.startsWith("---\n") || md.startsWith("---\r\n")) {
    const parts = md.split(/^---\s*$/m);
    if (parts.length >= 3) {
      for (const line of parts[1].split(/\r?\n/)) {
        const idx = line.indexOf(":");
        if (idx > 0) {
          meta[line.slice(0, idx).trim()] = line.slice(idx + 1).trim().replace(/^["']|["']$/g, "");
        }
      }
    }
  }
  return meta;
}

function collectDocsForLang(coreRoot, lang) {
  const docs = [];
  const base = path.join(coreRoot, "references", lang);
  const dirs = [
    ["chapter", path.join(base, "chapters")],
    ["directive", path.join(base, "directives")],
    ["research", path.join(base, "research")],
  ];
  for (const [kind, dir] of dirs) {
    if (!fs.existsSync(dir)) continue;
    for (const file of fs.readdirSync(dir).sort()) {
      if (!file.endsWith(".md")) continue;
      const full = path.join(dir, file);
      const content = fs.readFileSync(full, "utf8");
      const lines = content.split(/\r?\n/);
      const rel = path.relative(coreRoot, full).replace(/\\/g, "/");
      const stem = file.replace(/\.md$/i, "");
      docs.push({
        kind,
        slug: stem,
        id: kind === "chapter" ? stem.slice(0, 2) : stem,
        path: rel,
        title: (lines[0] || stem).replace(/^#+\s*/, "").trim(),
        lines: lines.length,
        words: content.split(/\s+/).filter(Boolean).length,
        content,
      });
    }
  }
  for (const topFile of ["INDEX.md", "VERIFICATION.md", "SOURCE_ISSUES.md", "SOURCES.md"]) {
    const full = path.join(base, topFile);
    if (!fs.existsSync(full)) continue;
    const content = fs.readFileSync(full, "utf8");
    const lines = content.split(/\r?\n/);
    docs.push({
      kind: "meta",
      slug: topFile.replace(/\.md$/i, ""),
      id: topFile,
      path: `references/${lang}/${topFile}`,
      title: (lines[0] || topFile).replace(/^#+\s*/, "").trim(),
      lines: lines.length,
      words: content.split(/\s+/).filter(Boolean).length,
      content,
    });
  }
  return docs;
}

function collectSkills(skillsRoot) {
  const skills = [];
  if (!skillsRoot) return skills;
  for (const entry of fs.readdirSync(skillsRoot).sort()) {
    const skFile = path.join(skillsRoot, entry, "SKILL.md");
    if (!fs.existsSync(skFile)) continue;
    const content = fs.readFileSync(skFile, "utf8");
    const meta = parseFrontmatter(content);
    const name = meta.name || entry;
    skills.push({
      name,
      description: meta.description || "",
      uri: `skill://${name}/SKILL.md`,
      digest: "sha256:" + crypto.createHash("sha256").update(content, "utf8").digest("hex"),
      words: content.split(/\s+/).filter(Boolean).length,
      content,
    });
  }
  return skills;
}

function main() {
  const coreRoot = findCoreRoot();
  const skillsRoot = findSkillsRoot(coreRoot);
  const outDir = path.join(WORKER_ROOT, "public", "corpus");
  fs.rmSync(outDir, { recursive: true, force: true });
  fs.mkdirSync(path.join(outDir, "evidence"), { recursive: true });

  for (const lang of ["en", "ru"]) {
    const docs = collectDocsForLang(coreRoot, lang);
    fs.writeFileSync(path.join(outDir, `docs-${lang}.json`), JSON.stringify({ lang, docs }), "utf8");
  }

  const skills = collectSkills(skillsRoot);
  fs.writeFileSync(path.join(outDir, "skills.json"), JSON.stringify({ skills }), "utf8");

  // Copy core evidence JSONs
  for (const name of ["coverage.json", "source_issues.json", "directives_manifest.json"]) {
    const src = path.join(coreRoot, "evidence", name);
    if (fs.existsSync(src)) {
      fs.copyFileSync(src, path.join(outDir, name));
    }
  }

  // Copy compiler evidence receipts & build a lightweight probe index
  const compDir = path.join(coreRoot, "evidence", "compiler");
  const evidenceFiles = [];
  const probeIndex = [];
  if (fs.existsSync(compDir)) {
    for (const file of fs.readdirSync(compDir).sort()) {
      if (!file.endsWith(".json")) continue;
      const src = path.join(compDir, file);
      if (!fs.statSync(src).isFile()) continue;
      fs.copyFileSync(src, path.join(outDir, "evidence", file));
      evidenceFiles.push(file);
      try {
        const parsed = JSON.parse(fs.readFileSync(src, "utf8"));
        for (const key of ["probes", "cases", "positive_examples", "negative_cases", "observations"]) {
          const arr = parsed?.[key];
          if (!Array.isArray(arr)) continue;
          for (const item of arr) {
            if (!item || typeof item !== "object") continue;
            const id = String(item.id || item.case_id || item.name || "");
            if (id) {
              probeIndex.push({
                id,
                receipt: file,
                collection: key,
                target: item.target || null,
                status: item.compiler_result || item.status || item.outcome || null,
              });
            }
          }
        }
      } catch {
        // Ignore unparseable
      }
    }
  }
  fs.writeFileSync(
    path.join(outDir, "evidence-index.json"),
    JSON.stringify({ files: evidenceFiles, total_entries: probeIndex.length, entries: probeIndex }),
    "utf8",
  );

  const summary = {
    coreRoot,
    skills: skills.length,
    evidenceFiles: evidenceFiles.length,
    probeIndexEntries: probeIndex.length,
  };
  console.log("CORPUS_BUILT:", JSON.stringify(summary));
}

main();
