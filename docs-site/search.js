/* search.js — client-side full-text search powered by lunr.js
 *
 * Reads docs-site/search_index/manifest.json, loads the index file of each
 * selected domain (search_index/<slug>.json) in parallel, merges them, builds
 * the lunr indices (papers, skills, workflows, tools) and renders grouped,
 * debounced live results. The selection starts from ?domains=a,b or the
 * manifest's default_domains and is kept in the URL.
 *
 * No backend. No build step. lunr is served from docs-site/vendor/ (see search.html).
 * Result links stay on this site: a skill, workflow or tool of a released
 * collection opens the Browse page filtered to it, a paper opens paper.html.
 * The SKILL.md files are in the domain repositories and are never linked.
 */

const INDEX_BASE = "./search_index/";
const MANIFEST_URL = INDEX_BASE + "manifest.json";
const PER_GROUP_LIMIT = 50;
const DEBOUNCE_MS = 150;
const SNIPPET_RADIUS = 60; // chars on either side of a match

let DATA = null;        // merged payload of the loaded domains: { papers, skills, tools, ... }
let IDX = null;         // { papers: lunr.Index, skills: lunr.Index, tools: lunr.Index }
let DEBOUNCE_TIMER = null;
let MANIFEST = null;    // search_index/manifest.json
let SELECTED = [];      // selected domain slugs, sorted
const DOMAIN_STATE = new Map();  // slug -> { status: "idle"|"loading"|"loaded"|"error", payload, error }

/* ---- Pure helpers (exercised with node; no DOM) ------------------------- */

/** Merge per-domain payloads into the single shape the rest of this file reads. */
function mergeDomainPayloads(payloads) {
  const merged = {
    collections: [], collection_status: {}, collection_commits: {},
    papers: [], skills: [], workflows: [], tools: [], domains: [],
  };
  const collections = new Set();
  for (const p of payloads) {
    if (!p) continue;
    if (p.domain) merged.domains.push(p.domain);
    for (const c of p.collections || []) collections.add(c);
    Object.assign(merged.collection_status, p.collection_status || {});
    Object.assign(merged.collection_commits, p.collection_commits || {});
    for (const key of ["papers", "skills", "workflows", "tools"]) {
      for (const row of p[key] || []) merged[key].push(row);
    }
  }
  merged.collections = [...collections].sort();
  return merged;
}

/**
 * The initial selection: the ?domains= list when it names indexed domains,
 * otherwise the manifest's default_domains. Returns { selected, unknown }.
 */
function initialSelection(domainsParam, available, defaults) {
  const known = new Set(available);
  if (domainsParam === null || domainsParam === undefined) {
    return { selected: (defaults || []).filter((d) => known.has(d)).sort(), unknown: [] };
  }
  const asked = domainsParam.split(",").map((d) => d.trim()).filter(Boolean);
  const unknown = asked.filter((d) => !known.has(d));
  const selected = [...new Set(asked.filter((d) => known.has(d)))].sort();
  if (asked.length && !selected.length) {
    return { selected: (defaults || []).filter((d) => known.has(d)).sort(), unknown };
  }
  return { selected, unknown };
}

/** Human-readable size: 34990781 -> "35.0 MB". */
function formatBytes(n) {
  if (!Number.isFinite(n)) return "";
  if (n >= 1e6) return `${(n / 1e6).toFixed(1)} MB`;
  if (n >= 1e3) return `${Math.round(n / 1e3)} kB`;
  return `${n} B`;
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { mergeDomainPayloads, initialSelection, formatBytes };
}

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k === "html") node.innerHTML = v;
    else if (k.startsWith("on")) node.addEventListener(k.slice(2).toLowerCase(), v);
    else if (v === true) node.setAttribute(k, "");
    else if (v !== false && v != null) node.setAttribute(k, v);
  }
  for (const c of children) {
    if (c == null) continue;
    node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
  }
  return node;
}

function escapeHTML(s) {
  return String(s ?? "").replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
  })[c]);
}

function escapeRegExp(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/** Build snippet around the first occurrence of any query term. */
function snippet(text, terms) {
  if (!text) return "";
  const lower = text.toLowerCase();
  let hitAt = -1;
  for (const t of terms) {
    if (!t) continue;
    const i = lower.indexOf(t.toLowerCase());
    if (i !== -1 && (hitAt === -1 || i < hitAt)) hitAt = i;
  }
  let start, end;
  if (hitAt === -1) {
    start = 0;
    end = Math.min(text.length, SNIPPET_RADIUS * 2);
  } else {
    start = Math.max(0, hitAt - SNIPPET_RADIUS);
    end = Math.min(text.length, hitAt + SNIPPET_RADIUS);
  }
  const prefix = start > 0 ? "…" : "";
  const suffix = end < text.length ? "…" : "";
  return prefix + text.slice(start, end) + suffix;
}

function highlight(snippetText, terms) {
  let html = escapeHTML(snippetText);
  for (const t of terms) {
    if (!t || t.length < 2) continue;
    const re = new RegExp(`(${escapeRegExp(t)})`, "gi");
    html = html.replace(re, '<mark>$1</mark>');
  }
  return html;
}

/** Extract lowercased term tokens from a raw user query. */
function tokensFromQuery(q) {
  return q
    .toLowerCase()
    .split(/[\s,;:+]+/)
    .map((t) => t.replace(/[^\w./@-]/g, ""))
    .filter((t) => t.length >= 2);
}

function buildLunrIndices(data) {
  const papersIdx = lunr(function () {
    this.ref("doi");
    this.field("doi", { boost: 5 });
    this.field("title", { boost: 3 });
    this.field("search_text");
    this.field("collection");
    for (const p of data.papers) this.add(p);
  });
  const skillsIdx = lunr(function () {
    this.ref("name");
    this.field("name", { boost: 5 });
    this.field("description", { boost: 3 });
    this.field("when_to_use_negative");
    this.field("summary");
    this.field("search_text");
    this.field("collection");
    for (const s of data.skills) this.add(s);
  });
  const workflowsIdx = lunr(function () {
    this.ref("slug");
    this.field("name", { boost: 5 });
    this.field("description", { boost: 3 });
    this.field("summary");
    this.field("search_text");
    this.field("collection");
    for (const w of data.workflows || []) this.add(w);
  });
  const toolsIdx = lunr(function () {
    this.ref("slug");
    this.field("slug", { boost: 5 });
    this.field("name", { boost: 4 });
    this.field("license_spdx", { boost: 2 });
    this.field("evidence_text");
    this.field("search_text");
    this.field("collection");
    for (const t of data.tools) this.add(t);
  });
  return { papers: papersIdx, skills: skillsIdx, workflows: workflowsIdx, tools: toolsIdx };
}

/** Run a tolerant lunr query: try exact, then prefix-match fallback. */
function runLunr(index, q) {
  if (!q) return [];
  // Tolerant search: prefix wildcards on every term, lowercase
  const tokens = tokensFromQuery(q);
  if (!tokens.length) return [];
  const expanded = tokens.map((t) => `${t}* ${t}`).join(" ");
  try {
    return index.search(expanded);
  } catch (_) {
    // Fall back to plain
    try {
      return index.search(q);
    } catch (_) {
      return [];
    }
  }
}

// "<slug>/v<N>", followed by a "staged" chip when the index marks that
// collection as staged (in the repository, not part of a release).
function collectionNode(collection) {
  const staged = ((DATA && DATA.collection_status) || {})[collection] === "staged";
  return el("span", {}, collection || "",
    staged ? " " : null,
    staged ? el("span", { class: "badge badge-staged" }, "staged") : null);
}

function paperResultNode(paper, terms) {
  const doiHref = `./paper.html?doi=${encodeURIComponent(paper.doi || "")}&collection=${encodeURIComponent(paper.collection || "")}`;
  const snip = snippet(paper.rationale || paper.search_text || "", terms);
  return el("div", { class: "result-item" },
    el("a", { href: doiHref, class: "result-title" }, paper.title || paper.doi || "(untitled)"),
    el("div", { class: "result-meta" },
      el("span", { class: "badge badge-paper" }, "paper"),
      " ",
      el("code", {}, paper.doi || "—"),
      " · ",
      collectionNode(paper.collection),
      " · ",
      el("span", {}, paper.status || ""),
      " · ",
      el("span", {}, paper.access_type || "unknown"),
    ),
    snip ? el("div", { class: "result-snippet", html: highlight(snip, terms) }) : null,
  );
}

/**
 * Browse-page link for a row of a released collection, filtered to that item;
 * null for a staged collection, which the Browse page does not offer.
 */
function browseHref(row, tab, q) {
  const status = ((DATA && DATA.collection_status) || {})[row.collection];
  const m = String(row.collection || "").match(/^([^/]+)\/v(\d+)$/);
  if (status !== "released" || !m) return null;
  return `./collections.html?c=${encodeURIComponent(m[1])}&v=${m[2]}&tab=${tab}&q=${encodeURIComponent(q || "")}`;
}

function titleNode(href, text) {
  return href
    ? el("a", { href, class: "result-title" }, text)
    : el("span", { class: "result-title" }, text);
}

function skillResultNode(skill, terms) {
  // Staged rows have no Browse page; their source paper page still lists them.
  const firstDoi = (skill.source_dois || [])[0];
  const href = browseHref(skill, "skills", skill.name) || (firstDoi
    ? `./paper.html?doi=${encodeURIComponent(firstDoi)}&collection=${encodeURIComponent(skill.collection || "")}`
    : null);
  const snip = snippet(skill.description || skill.summary || skill.search_text || "", terms);
  return el("div", { class: "result-item" },
    titleNode(href, skill.name),
    el("div", { class: "result-meta" },
      el("span", { class: "badge badge-skill" }, "skill"),
      " ",
      collectionNode(skill.collection),
      skill.source_dois && skill.source_dois.length
        ? el("span", {}, " · derived from ", el("a", {
            href: `./paper.html?doi=${encodeURIComponent(skill.source_dois[0])}&collection=${encodeURIComponent(skill.collection || "")}`,
          }, el("code", {}, skill.source_dois[0])))
        : null,
    ),
    snip ? el("div", { class: "result-snippet", html: highlight(snip, terms) }) : null,
  );
}

function workflowResultNode(wf, terms) {
  const href = browseHref(wf, "workflows", wf.slug || wf.name);
  const snip = snippet(wf.description || wf.summary || wf.search_text || "", terms);
  return el("div", { class: "result-item" },
    titleNode(href, wf.name || wf.slug),
    el("div", { class: "result-meta" },
      el("span", { class: "badge" }, "workflow"),
      " ",
      collectionNode(wf.collection),
      wf.stage_count ? el("span", {}, ` · ${wf.stage_count} stages`) : null,
    ),
    snip ? el("div", { class: "result-snippet", html: highlight(snip, terms) }) : null,
  );
}

function toolResultNode(tool, terms) {
  const href = browseHref(tool, "tools", tool.slug);
  const snip = snippet(tool.evidence_text || tool.search_text || "", terms);
  return el("div", { class: "result-item" },
    titleNode(href, tool.name || tool.slug),
    el("div", { class: "result-meta" },
      el("span", { class: "badge badge-tool" }, "tool"),
      " ",
      el("code", {}, tool.slug),
      tool.license_spdx ? el("span", {}, " · ", tool.license_spdx) : null,
      " · ",
      collectionNode(tool.collection),
      tool.source_doi ? el("span", {}, " · src ", el("code", {}, tool.source_doi)) : null,
    ),
    snip ? el("div", { class: "result-snippet", html: highlight(snip, terms) }) : null,
  );
}

function render(query) {
  const wantPapers = document.getElementById("filter-papers").checked;
  const wantSkills = document.getElementById("filter-skills").checked;
  const wantWorkflows = document.getElementById("filter-workflows").checked;
  const wantTools = document.getElementById("filter-tools").checked;

  const emptyEl = document.getElementById("empty-state");
  const noResEl = document.getElementById("no-results");
  const groups = {
    papers: document.getElementById("results-papers"),
    skills: document.getElementById("results-skills"),
    workflows: document.getElementById("results-workflows"),
    tools: document.getElementById("results-tools"),
  };
  for (const g of Object.values(groups)) {
    g.innerHTML = "";
    g.hidden = true;
  }
  noResEl.hidden = true;

  if (!query.trim()) {
    emptyEl.hidden = false;
    return;
  }
  emptyEl.hidden = true;
  if (!IDX) return;  // the selected domains are still loading; loadSelection renders again

  const terms = tokensFromQuery(query);

  const paperHits = wantPapers ? runLunr(IDX.papers, query) : [];
  const skillHits = wantSkills ? runLunr(IDX.skills, query) : [];
  const workflowHits = wantWorkflows ? runLunr(IDX.workflows, query) : [];
  const toolHits = wantTools ? runLunr(IDX.tools, query) : [];

  const total = paperHits.length + skillHits.length + workflowHits.length + toolHits.length;
  if (total === 0) {
    noResEl.hidden = false;
    return;
  }

  if (paperHits.length) {
    const g = groups.papers;
    g.hidden = false;
    g.appendChild(el("h2", {}, `Papers (${paperHits.length})`));
    const byDoi = new Map(DATA.papers.map((p) => [p.doi, p]));
    for (const hit of paperHits.slice(0, PER_GROUP_LIMIT)) {
      const p = byDoi.get(hit.ref);
      if (p) g.appendChild(paperResultNode(p, terms));
    }
  }
  if (skillHits.length) {
    const g = groups.skills;
    g.hidden = false;
    g.appendChild(el("h2", {}, `Skills (${skillHits.length})`));
    const byName = new Map(DATA.skills.map((s) => [s.name, s]));
    for (const hit of skillHits.slice(0, PER_GROUP_LIMIT)) {
      const s = byName.get(hit.ref);
      if (s) g.appendChild(skillResultNode(s, terms));
    }
  }
  if (workflowHits.length) {
    const g = groups.workflows;
    g.hidden = false;
    g.appendChild(el("h2", {}, `Workflows (${workflowHits.length})`));
    const bySlug = new Map((DATA.workflows || []).map((w) => [w.slug, w]));
    for (const hit of workflowHits.slice(0, PER_GROUP_LIMIT)) {
      const w = bySlug.get(hit.ref);
      if (w) g.appendChild(workflowResultNode(w, terms));
    }
  }
  if (toolHits.length) {
    const g = groups.tools;
    g.hidden = false;
    g.appendChild(el("h2", {}, `Tools (${toolHits.length})`));
    const bySlug = new Map(DATA.tools.map((t) => [t.slug, t]));
    for (const hit of toolHits.slice(0, PER_GROUP_LIMIT)) {
      const t = bySlug.get(hit.ref);
      if (t) g.appendChild(toolResultNode(t, terms));
    }
  }
}

function onInput() {
  clearTimeout(DEBOUNCE_TIMER);
  const q = document.getElementById("search-input").value;
  DEBOUNCE_TIMER = setTimeout(() => render(q), DEBOUNCE_MS);
}

/* ---- Domain selection ---------------------------------------------------- */

function domainChipLabel(slug) {
  const entry = MANIFEST.domains[slug] || {};
  const counts = entry.counts || {};
  const state = DOMAIN_STATE.get(slug) || { status: "idle" };
  const status =
    state.status === "loading" ? " · loading…" :
    state.status === "error" ? " · failed to load" : "";
  return `${slug} · ${formatBytes(entry.bytes)} · ${(counts.skills || 0).toLocaleString("en")} skills${status}`;
}

function renderDomainChips() {
  const box = document.getElementById("domain-chips");
  if (!box || !MANIFEST) return;  // only search.html carries the chips
  box.innerHTML = "";
  for (const slug of Object.keys(MANIFEST.domains).sort()) {
    const entry = MANIFEST.domains[slug];
    const counts = entry.counts || {};
    const pressed = SELECTED.includes(slug);
    const state = (DOMAIN_STATE.get(slug) || {}).status;
    const button = el("button", {
      type: "button",
      class: "tier-btn domain-chip" + (pressed ? " is-active" : "") + (state === "error" ? " is-failed" : ""),
      "aria-pressed": pressed ? "true" : "false",
      "data-domain": slug,
      title: `${(counts.papers || 0).toLocaleString("en")} papers, ${(counts.skills || 0).toLocaleString("en")} skills, ` +
        `${(counts.workflows || 0).toLocaleString("en")} workflows, ${(counts.tools || 0).toLocaleString("en")} tools ` +
        `(${(entry.collections || []).map((c) => c.label).join(", ")}); ${formatBytes(entry.bytes)} to download`,
      onclick: () => toggleDomain(slug),
    }, domainChipLabel(slug));
    box.appendChild(button);
  }
}

function writeSelectionToURL() {
  const url = new URL(window.location.href);
  url.searchParams.set("domains", SELECTED.join(","));
  window.history.replaceState(null, "", url.toString());
}

function toggleDomain(slug) {
  SELECTED = SELECTED.includes(slug)
    ? SELECTED.filter((d) => d !== slug)
    : [...SELECTED, slug].sort();
  // Free the memory of a deselected domain; a failed one is retried when selected again.
  for (const [d, state] of DOMAIN_STATE) {
    if (!SELECTED.includes(d) && state.status !== "loading") DOMAIN_STATE.delete(d);
  }
  writeSelectionToURL();
  loadSelection();
}

async function fetchDomain(slug) {
  const entry = MANIFEST.domains[slug];
  // The sha256 in the query lets the browser cache a file until it changes.
  const url = `${INDEX_BASE}${encodeURIComponent(entry.file)}?v=${encodeURIComponent((entry.sha256 || "").slice(0, 16))}`;
  const r = await fetch(url);
  if (!r.ok) throw new Error(`${r.status} ${entry.file}`);
  return r.json();
}

async function loadSelection() {
  const hintEl = document.getElementById("search-hint");
  const pending = SELECTED.filter((slug) => {
    const state = DOMAIN_STATE.get(slug);
    return !state || state.status === "idle" || state.status === "error";
  });
  for (const slug of pending) DOMAIN_STATE.set(slug, { status: "loading" });
  renderDomainChips();
  if (pending.length) {
    const size = pending.reduce((n, slug) => n + (MANIFEST.domains[slug].bytes || 0), 0);
    hintEl.textContent = `Loading ${pending.join(", ")} (${formatBytes(size)})…`;
  }
  const results = await Promise.allSettled(pending.map((slug) => fetchDomain(slug)));
  results.forEach((result, i) => {
    const slug = pending[i];
    if (!SELECTED.includes(slug)) { DOMAIN_STATE.delete(slug); return; }
    DOMAIN_STATE.set(slug, result.status === "fulfilled"
      ? { status: "loaded", payload: result.value }
      : { status: "error", error: String(result.reason && result.reason.message || result.reason) });
  });
  // Another load still running for the selection finishes the job when it settles.
  if (SELECTED.some((slug) => (DOMAIN_STATE.get(slug) || {}).status === "loading")) return;
  renderDomainChips();
  const loaded = SELECTED.filter((slug) => (DOMAIN_STATE.get(slug) || {}).status === "loaded");
  const failed = SELECTED.filter((slug) => (DOMAIN_STATE.get(slug) || {}).status === "error");
  DATA = mergeDomainPayloads(loaded.map((slug) => DOMAIN_STATE.get(slug).payload));
  IDX = buildLunrIndices(DATA);
  const failure = failed.length
    ? " " + failed.map((slug) => `Could not load ${slug}: ${DOMAIN_STATE.get(slug).error}.`).join(" ")
    : "";
  if (!SELECTED.length) {
    hintEl.textContent = "No domain selected: choose one or more above.";
  } else {
    const stagedCount = Object.values(DATA.collection_status || {}).filter(v => v === "staged").length;
    hintEl.textContent =
      `Searching ${DATA.papers.length} papers, ${DATA.skills.length} skills, ` +
      `${(DATA.workflows || []).length} workflows, ${DATA.tools.length} tools ` +
      `across ${(DATA.collections || []).length} collections in ${loaded.length} ` +
      `domain${loaded.length === 1 ? "" : "s"}` +
      (stagedCount ? ` (${stagedCount} staged, not part of a release).` : ".");
  }
  if (failure) hintEl.appendChild(el("span", { class: "error" }, failure));
  render(document.getElementById("search-input").value);
}

if (typeof document !== "undefined" && document.getElementById("search-input")) (async function init() {
  const hintEl = document.getElementById("search-hint");
  hintEl.textContent = "Loading index…";
  if (typeof lunr !== "function") {
    hintEl.innerHTML = `<span class="error">lunr.js failed to load.</span>`;
    return;
  }
  try {
    const r = await fetch(MANIFEST_URL, { cache: "no-store" });
    if (!r.ok) throw new Error(`${r.status} ${MANIFEST_URL}`);
    MANIFEST = await r.json();
  } catch (e) {
    hintEl.innerHTML = `<span class="error">Could not load the search index manifest: ${escapeHTML(e.message)}.</span>`;
    return;
  }
  const params = new URLSearchParams(window.location.search);
  const { selected, unknown } = initialSelection(
    params.get("domains"), Object.keys(MANIFEST.domains || {}), MANIFEST.default_domains);
  SELECTED = selected;
  if (unknown.length) {
    document.getElementById("domain-note").textContent =
      `Not in the index: ${unknown.join(", ")}.`;
  }
  if (params.has("domains")) writeSelectionToURL();

  const input = document.getElementById("search-input");
  input.addEventListener("input", onInput);
  for (const id of ["filter-papers", "filter-skills", "filter-workflows", "filter-tools"]) {
    document.getElementById(id).addEventListener("change", () => render(input.value));
  }
  // Honor ?q= deep link; results appear once the selected domains are loaded.
  const q0 = params.get("q");
  if (q0) input.value = q0;
  await loadSelection();
})();
