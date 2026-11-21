import { WorkerEntrypoint } from "cloudflare:workers";
import {
  getCoverage,
  getDocs,
  getEvidenceIndex,
  getEvidenceReceipt,
  getSkills,
  getSourceIssues,
  resolveDoc,
  searchCorpus,
} from "./corpus";

export interface WorkerLoaderBinding {
  load(config: {
    compatibilityDate: string;
    mainModule: string;
    modules: Record<string, string>;
    env?: Record<string, unknown>;
    globalOutbound?: null | Fetcher;
  }): {
    getEntrypoint<T = unknown>(name?: string): T;
  };
}

export interface Env {
  ASSETS: Fetcher;
  LOADER: WorkerLoaderBinding;
  MCP_ACCESS_KEY?: string;
  ACCESS_MODE?: string; // "open" | "freemium" | "strict"
}

interface CorpusRpcProps {
  accessLevel: "full" | "preview";
}

interface SandboxRunner {
  run(): Promise<{ ok: boolean; value?: unknown; error?: string }>;
}

const SERVER_INFO = {
  name: "delphi-behavior-contracts-mcp",
  version: "1.0.0",
};
const PROTOCOL_VERSION = "2025-03-26";

/**
 * Read-only RPC Entrypoint exposed to ephemeral Dynamic Worker sandboxes
 * via `ctx.exports.DelphiCorpusRpc({ props: { accessLevel } })`.
 * Dynamic Worker isolates have `globalOutbound: null` (zero network access)
 * and can only call these read-only corpus methods.
 */
export class DelphiCorpusRpc extends WorkerEntrypoint<Env, CorpusRpcProps> {
  private isFull(): boolean {
    return (this.ctx.props?.accessLevel ?? "full") === "full";
  }

  async search(query: string, opts?: { lang?: "en" | "ru"; limit?: number; includeIssues?: boolean }) {
    const lang = opts?.lang === "ru" ? "ru" : "en";
    const results = await searchCorpus(
      this.env.ASSETS,
      query,
      lang,
      opts?.limit ?? 8,
      Boolean(opts?.includeIssues),
    );
    if (!this.isFull()) {
      return results.map((r) => ({ path: r.path, title: r.title, score: r.score, matched_terms: r.matched_terms }));
    }
    return results;
  }

  async chapters(lang: "en" | "ru" = "en") {
    const docs = await getDocs(this.env.ASSETS, lang === "ru" ? "ru" : "en");
    return docs
      .filter((d) => d.kind === "chapter")
      .map(({ id, slug, path, title, lines, words }) => ({ id, slug, path, title, lines, words }));
  }

  async directives(lang: "en" | "ru" = "en") {
    const docs = await getDocs(this.env.ASSETS, lang === "ru" ? "ru" : "en");
    return docs
      .filter((d) => d.kind === "directive" && d.slug !== "INDEX")
      .map(({ slug, path, title, words }) => ({ slug, path, title, words }));
  }

  async read(ref: string, opts?: { lang?: "en" | "ru"; startLine?: number; endLine?: number }) {
    const lang = opts?.lang === "ru" ? "ru" : "en";
    const doc = await resolveDoc(this.env.ASSETS, ref, lang);
    const previewAllowed = doc.kind === "meta" && (doc.slug === "INDEX" || doc.slug === "VERIFICATION");
    if (!this.isFull() && !previewAllowed) {
      throw new Error("Full document access requires a valid license key (Authorization: Bearer <key>).");
    }
    const lines = doc.content.split(/\r?\n/);
    const total = lines.length;
    const s = Math.max(1, Math.floor(opts?.startLine ?? 1));
    const e = Math.min(total, Math.max(s, Math.floor(opts?.endLine ?? 250)));
    return {
      path: doc.path,
      title: doc.title,
      total_lines: total,
      start_line: s,
      end_line: e,
      truncated: e < total,
      content: lines.slice(s - 1, e).join("\n"),
    };
  }

  async chapter(idOrSlug: string, opts?: { lang?: "en" | "ru"; startLine?: number; endLine?: number }) {
    return this.read(String(idOrSlug), { lang: opts?.lang, startLine: opts?.startLine ?? 1, endLine: opts?.endLine ?? 400 });
  }

  async directive(name: string, lang: "en" | "ru" = "en") {
    return this.read(name, { lang, startLine: 1, endLine: 300 });
  }

  async verification(lang: "en" | "ru" = "en") {
    return this.read(`references/${lang === "ru" ? "ru" : "en"}/VERIFICATION.md`, { lang, startLine: 1, endLine: 400 });
  }

  async coverage() {
    return getCoverage(this.env.ASSETS);
  }

  async issues(status?: string) {
    const data = await getSourceIssues(this.env.ASSETS);
    if (!status) return data.issues;
    const wanted = status.toUpperCase();
    return data.issues.filter((i) => String(i.status ?? "").toUpperCase() === wanted);
  }

  async issue(id: string) {
    const data = await getSourceIssues(this.env.ASSETS);
    const wanted = id.toUpperCase();
    const hit = data.issues.find((i) => String(i.id ?? "").toUpperCase() === wanted);
    if (!hit) throw new Error(`Source issue not found: ${id}`);
    return hit;
  }

  async evidenceFiles() {
    const idx = await getEvidenceIndex(this.env.ASSETS);
    return idx.files;
  }

  async evidence(fileOrProbeId: string) {
    if (!this.isFull()) {
      throw new Error("Compiler receipts require a valid license key.");
    }
    if (fileOrProbeId.endsWith(".json")) {
      return getEvidenceReceipt(this.env.ASSETS, fileOrProbeId);
    }
    const idx = await getEvidenceIndex(this.env.ASSETS);
    const needle = fileOrProbeId.toLowerCase();
    const hits = idx.entries.filter((e) => e.id.toLowerCase().includes(needle)).slice(0, 12);
    const byFile = new Map<string, typeof hits>();
    for (const h of hits) {
      const list = byFile.get(h.receipt) ?? [];
      list.push(h);
      byFile.set(h.receipt, list);
    }
    const detailed: Array<{ receipt: string; collection: string; entry: unknown }> = [];
    for (const [receiptFile, fileHits] of byFile.entries()) {
      const fullReceipt = (await getEvidenceReceipt(this.env.ASSETS, receiptFile)) as Record<string, unknown>;
      for (const h of fileHits) {
        const arr = fullReceipt?.[h.collection];
        if (!Array.isArray(arr)) continue;
        const entry = arr.find(
          (item: Record<string, unknown>) =>
            String(item?.id ?? item?.case_id ?? item?.name ?? "").toLowerCase() === h.id.toLowerCase(),
        );
        if (entry) {
          detailed.push({ receipt: `evidence/compiler/${receiptFile}`, collection: h.collection, entry });
        }
      }
    }
    return detailed;
  }

  async skills() {
    const all = await getSkills(this.env.ASSETS);
    return all.map(({ name, description, uri, digest, words }) => ({ name, description, uri, digest, words }));
  }

  async skill(name: string) {
    const all = await getSkills(this.env.ASSETS);
    const hit = all.find((s) => s.name === name);
    if (!hit) throw new Error(`Unknown skill: ${name}`);
    if (!this.isFull() && name !== "delphi-behavior-contracts") {
      throw new Error("Specialist skills require a valid license key.");
    }
    return hit;
  }
}

async function timingSafeKeyEquals(candidate: string, expected: string): Promise<boolean> {
  const enc = new TextEncoder();
  const [h1, h2] = await Promise.all([
    crypto.subtle.digest("SHA-256", enc.encode(candidate)),
    crypto.subtle.digest("SHA-256", enc.encode(expected)),
  ]);
  const a = new Uint8Array(h1);
  const b = new Uint8Array(h2);
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a[i] ^ b[i];
  return diff === 0;
}

async function resolveAccessLevel(request: Request, env: Env): Promise<"full" | "preview" | "denied"> {
  const configuredKey = env.MCP_ACCESS_KEY?.trim();
  const mode = (env.ACCESS_MODE ?? "freemium").toLowerCase();
  if (!configuredKey || mode === "open") {
    return "full";
  }
  const auth = request.headers.get("Authorization") ?? "";
  let token = auth.startsWith("Bearer ") ? auth.slice(7).trim() : "";
  if (!token) {
    token = new URL(request.url).searchParams.get("key")?.trim() ?? "";
  }
  if (token && (await timingSafeKeyEquals(token, configuredKey))) {
    return "full";
  }
  return mode === "strict" ? "denied" : "preview";
}

function buildSandboxModule(userCode: string): string {
  const trimmed = userCode.trim();
  // Accept either `async () => { ... }`, `async (delphi) => { ... }`, or bare async statements
  const isArrow = /^(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>/.test(trimmed);
  const body = isArrow
    ? `const __fn = (${trimmed});\nconst __res = await __fn(delphi);`
    : `const __fn = async (delphi) => {\n${trimmed}\n};\nconst __res = await __fn(delphi);`;

  return `
import { WorkerEntrypoint } from "cloudflare:workers";

export class Sandbox extends WorkerEntrypoint {
  async run() {
    const rpc = this.env.DELPHI;
    const delphi = {
      search: (query, opts) => rpc.search(query, opts),
      chapters: (lang = "en") => rpc.chapters(lang),
      directives: (lang = "en") => rpc.directives(lang),
      read: (ref, opts) => rpc.read(ref, opts),
      chapter: (idOrSlug, opts) => rpc.chapter(idOrSlug, opts),
      directive: (name, lang = "en") => rpc.directive(name, lang),
      verification: (lang = "en") => rpc.verification(lang),
      coverage: () => rpc.coverage(),
      issues: (status) => rpc.issues(status),
      issue: (id) => rpc.issue(id),
      evidenceFiles: () => rpc.evidenceFiles(),
      evidence: (fileOrProbeId) => rpc.evidence(fileOrProbeId),
      skills: () => rpc.skills(),
      skill: (name) => rpc.skill(name),
    };
    try {
      ${body}
      return { ok: true, value: __res };
    } catch (err) {
      return { ok: false, error: err instanceof Error ? err.message : String(err) };
    }
  }
}
`;
}

const TOOLS = [
  {
    name: "delphi_search",
    description:
      "Search Delphi Behavior Contracts (74 chapters + 89 directive cards, EN/RU, optionally SOURCE_ISSUES and research). Returns ranked paths, titles, scores and matching line snippets.",
    inputSchema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: 'Topic, syntax, directive, or error code (e.g. "dynamic array", "HasWeakRef", "$WARN", "динамический массив").',
        },
        lang: { type: "string", enum: ["en", "ru"], default: "en" },
        limit: { type: "integer", minimum: 1, maximum: 30, default: 8 },
        include_issues: { type: "boolean", default: false },
      },
      required: ["query"],
    },
  },
  {
    name: "delphi_read",
    description:
      'Read a chapter, directive card, verification record, or research pass by path or shorthand (e.g. "31", "10-arrays.md", "warn", "VERIFICATION.md").',
    inputSchema: {
      type: "object",
      properties: {
        path: { type: "string" },
        lang: { type: "string", enum: ["en", "ru"], default: "en" },
        start_line: { type: "integer", minimum: 1, default: 1 },
        end_line: { type: "integer", minimum: 1, default: 250 },
      },
      required: ["path"],
    },
  },
  {
    name: "delphi_skill",
    description:
      "Load one of the 5 specialist Delphi Behavior Contracts skills (or omit name to list): delphi-behavior-contracts, delphi-migration, delphi-legacy-upgrade, delphi-directives, delphi-code-review.",
    inputSchema: {
      type: "object",
      properties: {
        name: { type: "string" },
        list_only: { type: "boolean", default: false },
      },
    },
  },
  {
    name: "delphi_execute",
    description:
      "Cloudflare Code Mode: execute a JavaScript async arrow function inside an isolated ephemeral V8 Dynamic Worker (`globalOutbound: null`, zero network access) with the read-only `delphi` corpus SDK. Query multiple chapters, directives, source issues and 879+ compiler receipts in one round-trip and return only the distilled result.\n\nAvailable `delphi` SDK methods (all async):\n- delphi.search(query, { lang?, limit?, includeIssues? })\n- delphi.chapters(lang?) / delphi.chapter(idOrSlug, { lang?, startLine?, endLine? })\n- delphi.directives(lang?) / delphi.directive(name, lang?)\n- delphi.read(path, { lang?, startLine?, endLine? })\n- delphi.verification(lang?) / delphi.coverage()\n- delphi.issues(status?) / delphi.issue(id)\n- delphi.evidenceFiles() / delphi.evidence(fileOrProbeId)\n- delphi.skills() / delphi.skill(name)\n\nExample:\nasync (delphi) => {\n  const hits = await delphi.search('HasWeakRef', { lang: 'en', limit: 3 });\n  const ev = await delphi.evidence('P15_HasWeakRef_RecWeak32');\n  return { top: hits[0]?.path, evidenceCount: ev.length };\n}",
    inputSchema: {
      type: "object",
      properties: {
        code: { type: "string", description: "JavaScript async arrow function `async (delphi) => { ... }` or async statements returning a JSON-serializable value." },
        truncate: { type: "boolean", default: true },
      },
      required: ["code"],
    },
  },
];

function ok(id: unknown, result: unknown) {
  return { jsonrpc: "2.0", id, result };
}

function err(id: unknown, code: number, message: string) {
  return { jsonrpc: "2.0", id, error: { code, message } };
}

function toolText(id: unknown, text: string, isError = false) {
  return ok(id, {
    ...(isError ? { isError: true } : {}),
    content: [{ type: "text", text }],
  });
}

async function dispatchMcp(
  req: Record<string, unknown>,
  env: Env,
  ctx: ExecutionContext,
  accessLevel: "full" | "preview",
): Promise<unknown | null> {
  const id = req.id;
  const method = String(req.method ?? "");
  const params = (req.params ?? {}) as Record<string, unknown>;

  if (id === undefined && method.startsWith("notifications/")) {
    return null;
  }

  const rpcStub = (ctx.exports as unknown as {
    DelphiCorpusRpc: (opts: { props: CorpusRpcProps }) => DelphiCorpusRpc;
  }).DelphiCorpusRpc({ props: { accessLevel } });

  try {
    if (method === "initialize") {
      return ok(id, {
        protocolVersion: PROTOCOL_VERSION,
        serverInfo: SERVER_INFO,
        capabilities: {
          tools: { listChanged: false },
          resources: { subscribe: false, listChanged: false },
          prompts: { listChanged: false },
          experimental: {
            "io.modelcontextprotocol/skills": { listChanged: false },
          },
        },
        instructions:
          "Delphi Behavior Contracts Remote MCP (Cloudflare Workers + Code Mode + Skills over MCP). " +
          "Use `delphi_search` or `delphi_execute` to inspect compiler-measured Delphi behavior (74 chapters, 89 directives, 879+ receipts) " +
          "and `delphi_skill` / `skills/list` to load specialist workflows.",
      });
    }

    if (method === "ping") return ok(id, {});
    if (method === "tools/list") return ok(id, { tools: TOOLS });

    if (method === "tools/call") {
      const name = String(params.name ?? "");
      const args = (params.arguments ?? {}) as Record<string, unknown>;

      if (name === "delphi_search") {
        const query = String(args.query ?? "");
        const lang = args.lang === "ru" ? "ru" : "en";
        const limit = Number(args.limit ?? 8);
        const includeIssues = Boolean(args.include_issues ?? false);
        const matches = await rpcStub.search(query, { lang, limit, includeIssues });
        return toolText(id, JSON.stringify({ query, language: lang, access: accessLevel, matches }, null, 2));
      }

      if (name === "delphi_read") {
        const res = await rpcStub.read(String(args.path ?? ""), {
          lang: args.lang === "ru" ? "ru" : "en",
          startLine: Number(args.start_line ?? 1),
          endLine: Number(args.end_line ?? 250),
        });
        return toolText(id, JSON.stringify(res, null, 2));
      }

      if (name === "delphi_skill") {
        if (args.list_only || !args.name) {
          const list = await rpcStub.skills();
          return toolText(id, JSON.stringify({ skills: list }, null, 2));
        }
        const sk = await rpcStub.skill(String(args.name));
        return toolText(id, sk.content);
      }

      if (name === "delphi_execute") {
        if (accessLevel !== "full") {
          return toolText(id, "Code Mode (`delphi_execute`) requires a valid license key (Authorization: Bearer <key>).", true);
        }
        const code = String(args.code ?? "");
        if (!code.trim() || code.length > 16000) {
          return toolText(id, "Code must be non-empty and <= 16,000 characters.", true);
        }
        const truncate = args.truncate !== false;
        const sandbox = env.LOADER.load({
          compatibilityDate: "2026-10-01",
          mainModule: "sandbox.js",
          modules: {
            "sandbox.js": buildSandboxModule(code),
          },
          env: {
            DELPHI: rpcStub,
          },
          globalOutbound: null,
        });
        const runner = sandbox.getEntrypoint<SandboxRunner>("Sandbox");
        const execResult = await runner.run();
        if (!execResult.ok) {
          return toolText(id, `Sandbox execution error: ${execResult.error}`, true);
        }
        let rendered = JSON.stringify(execResult.value ?? null, null, 2);
        if (truncate && rendered.length > 24000) {
          rendered = rendered.slice(0, 24000) + "\n... [truncated; pass truncate=false or narrow the return value]";
        }
        return toolText(id, rendered);
      }

      return err(id, -32601, `Unknown tool: ${name}`);
    }

    // SEP-2640 Skills over MCP
    if (method === "skills/list") {
      return ok(id, { skills: await rpcStub.skills() });
    }
    if (method === "skills/get") {
      return ok(id, await rpcStub.skill(String(params.name ?? "")));
    }

    if (method === "resources/list") {
      const sks = await rpcStub.skills();
      const resources = [
        ...sks.map((s) => ({
          uri: s.uri,
          name: s.name,
          description: s.description,
          mimeType: "text/markdown",
        })),
        { uri: "delphi://en/INDEX.md", name: "Topic Map (EN)", mimeType: "text/markdown" },
        { uri: "delphi://ru/INDEX.md", name: "Topic Map (RU)", mimeType: "text/markdown" },
        { uri: "delphi://en/VERIFICATION.md", name: "Verification Record (EN)", mimeType: "text/markdown" },
        { uri: "delphi://ru/VERIFICATION.md", name: "Verification Record (RU)", mimeType: "text/markdown" },
        { uri: "delphi://en/SOURCE_ISSUES.md", name: "Source Issues (EN)", mimeType: "text/markdown" },
        { uri: "delphi://ru/SOURCE_ISSUES.md", name: "Source Issues (RU)", mimeType: "text/markdown" },
        { uri: "delphi://evidence/coverage.json", name: "Coverage JSON", mimeType: "application/json" },
        { uri: "delphi://evidence/source_issues.json", name: "Source Issues JSON", mimeType: "application/json" },
      ];
      return ok(id, { resources });
    }

    if (method === "resources/read") {
      const uri = String(params.uri ?? "");
      if (uri.startsWith("skill://")) {
        const skillName = uri.slice("skill://".length).split("/")[0];
        const sk = await rpcStub.skill(skillName);
        return ok(id, { contents: [{ uri, mimeType: "text/markdown", text: sk.content }] });
      }
      if (uri === "delphi://evidence/coverage.json") {
        return ok(id, { contents: [{ uri, mimeType: "application/json", text: JSON.stringify(await rpcStub.coverage(), null, 2) }] });
      }
      if (uri === "delphi://evidence/source_issues.json") {
        return ok(id, { contents: [{ uri, mimeType: "application/json", text: JSON.stringify({ issues: await rpcStub.issues() }, null, 2) }] });
      }
      if (uri.startsWith("delphi://")) {
        const sub = uri.slice("delphi://".length);
        const lang = sub.startsWith("ru/") ? "ru" : "en";
        const ref = sub.startsWith("en/") || sub.startsWith("ru/") ? `references/${sub}` : sub;
        const doc = await rpcStub.read(ref, { lang, startLine: 1, endLine: 2000 });
        return ok(id, { contents: [{ uri, mimeType: "text/markdown", text: doc.content }] });
      }
      return err(id, -32602, `Unsupported URI: ${uri}`);
    }

    if (method === "prompts/list") {
      const sks = await rpcStub.skills();
      return ok(id, {
        prompts: sks.map((s) => ({
          name: s.name,
          description: s.description,
          arguments: [{ name: "task", description: "Delphi code, question, or migration goal", required: false }],
        })),
      });
    }

    if (method === "prompts/get") {
      const name = String(params.name ?? "");
      const task = String(((params.arguments ?? {}) as Record<string, unknown>).task ?? "");
      const sk = await rpcStub.skill(name);
      const text = sk.content + (task ? `\n\n## User Task\n${task}\n` : "");
      return ok(id, {
        description: sk.description,
        messages: [{ role: "user", content: { type: "text", text } }],
      });
    }

    return err(id, -32601, `Method not found: ${method}`);
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    if (method === "tools/call") {
      return toolText(id, `Error: ${msg}`, true);
    }
    return err(id, -32000, msg);
  }
}

const CORS_HEADERS: Record<string, string> = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, Mcp-Session-Id",
};

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...CORS_HEADERS },
  });
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    // Never expose raw /corpus/* static assets publicly
    if (url.pathname.startsWith("/corpus")) {
      return new Response("Not found", { status: 404 });
    }

    if (request.method === "GET" && (url.pathname === "/" || url.pathname === "/health")) {
      return jsonResponse({
        status: "ok",
        server: SERVER_INFO,
        endpoint: `${url.origin}/mcp`,
        transport: "streamable-http",
        features: {
          code_mode: "Cloudflare Dynamic Worker Loader (env.LOADER, globalOutbound=null)",
          skills_over_mcp: "SEP-2640 (skills/list, skills/get + skill:// resources)",
          languages: ["en", "ru"],
          tools: TOOLS.map((t) => t.name),
        },
        auth: env.MCP_ACCESS_KEY ? { mode: env.ACCESS_MODE ?? "freemium", key_required: true } : { mode: "open", key_required: false },
      });
    }

    if (url.pathname === "/mcp" && request.method === "POST") {
      const accessLevel = await resolveAccessLevel(request, env);
      if (accessLevel === "denied") {
        return jsonResponse({ error: "Unauthorized. Provide Authorization: Bearer <key>." }, 401);
      }
      let body: unknown;
      try {
        body = await request.json();
      } catch {
        return jsonResponse(err(null, -32700, "Parse error"), 400);
      }

      if (Array.isArray(body)) {
        const out = [];
        for (const item of body) {
          const r = await dispatchMcp(item as Record<string, unknown>, env, ctx, accessLevel);
          if (r !== null) out.push(r);
        }
        return jsonResponse(out);
      }

      const reply = await dispatchMcp(body as Record<string, unknown>, env, ctx, accessLevel);
      if (reply === null) {
        return new Response(null, { status: 202, headers: CORS_HEADERS });
      }
      return jsonResponse(reply);
    }

    return jsonResponse({ error: "Not found. Use POST /mcp or GET /health." }, 404);
  },
} satisfies ExportedHandler<Env>;
