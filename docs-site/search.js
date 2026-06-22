/* search.js — client-side full-text search powered by lunr.js
 *
 * Loads docs-site/search_index.json, builds three lunr indices (papers,
 * skills, tools), and renders grouped, debounced live results.
 *
 * No backend. No build step. CDN-loaded lunr from search.html.
 */

const RAW_BASE = "https://raw.githubusercontent.com/HolobiomicsLab/asb-skill-collections/main";
const INDEX_URL = "./search_index.json";
const PER_GROUP_LIMIT = 50;
const DEBOUNCE_MS = 150;
const SNIPPET_RADIUS = 60; // chars on either side of a match

let DATA = null;        // { papers, skills, tools, ... }
let IDX = null;         // { papers: lunr.Index, skills: lunr.Index, tools: lunr.Index }
let DEBOUNCE_TIMER = null;

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
  return { papers: papersIdx, skills: skillsIdx, tools: toolsIdx };
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
      el("span", {}, paper.collection || ""),
      " · ",
      el("span", {}, paper.status || ""),
      " · ",
      el("span", {}, paper.access_type || "unknown"),
    ),
    snip ? el("div", { class: "result-snippet", html: highlight(snip, terms) }) : null,
  );
}

function skillResultNode(skill, terms) {
  // GitHub raw URL of the SKILL.md
  const href = skill.md_path
    ? `${RAW_BASE}/${skill.md_path}`
    : `${RAW_BASE}/staged-collections/${skill.collection}/skills/${skill.name}/SKILL.md`;
  const snip = snippet(skill.description || skill.summary || skill.search_text || "", terms);
  return el("div", { class: "result-item" },
    el("a", { href, target: "_blank", rel: "noopener", class: "result-title" }, skill.name),
    el("div", { class: "result-meta" },
      el("span", { class: "badge badge-skill" }, "skill"),
      " ",
      el("span", {}, skill.collection || ""),
      skill.source_dois && skill.source_dois.length
        ? el("span", {}, " · derived from ", el("code", {}, skill.source_dois[0]))
        : null,
    ),
    snip ? el("div", { class: "result-snippet", html: highlight(snip, terms) }) : null,
  );
}

function toolResultNode(tool, terms) {
  const href = tool.yaml_path
    ? `${RAW_BASE}/${tool.yaml_path}`
    : `${RAW_BASE}/staged-collections/${tool.collection}/tools/${tool.slug}.yaml`;
  const snip = snippet(tool.evidence_text || tool.search_text || "", terms);
  return el("div", { class: "result-item" },
    el("a", { href, target: "_blank", rel: "noopener", class: "result-title" }, tool.name || tool.slug),
    el("div", { class: "result-meta" },
      el("span", { class: "badge badge-tool" }, "tool"),
      " ",
      el("code", {}, tool.slug),
      tool.license_spdx ? el("span", {}, " · ", tool.license_spdx) : null,
      " · ",
      el("span", {}, tool.collection || ""),
      tool.source_doi ? el("span", {}, " · src ", el("code", {}, tool.source_doi)) : null,
    ),
    snip ? el("div", { class: "result-snippet", html: highlight(snip, terms) }) : null,
  );
}

function render(query) {
  const wantPapers = document.getElementById("filter-papers").checked;
  const wantSkills = document.getElementById("filter-skills").checked;
  const wantTools = document.getElementById("filter-tools").checked;

  const emptyEl = document.getElementById("empty-state");
  const noResEl = document.getElementById("no-results");
  const groups = {
    papers: document.getElementById("results-papers"),
    skills: document.getElementById("results-skills"),
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

  const terms = tokensFromQuery(query);

  const paperHits = wantPapers ? runLunr(IDX.papers, query) : [];
  const skillHits = wantSkills ? runLunr(IDX.skills, query) : [];
  const toolHits = wantTools ? runLunr(IDX.tools, query) : [];

  const total = paperHits.length + skillHits.length + toolHits.length;
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

(async function init() {
  const hintEl = document.getElementById("search-hint");
  hintEl.textContent = "Loading index…";
  try {
    const r = await fetch(INDEX_URL, { cache: "no-store" });
    if (!r.ok) throw new Error(`${r.status} ${INDEX_URL}`);
    DATA = await r.json();
  } catch (e) {
    hintEl.innerHTML = `<span class="error">Could not load search index: ${escapeHTML(e.message)}.</span>`;
    return;
  }
  if (typeof lunr !== "function") {
    hintEl.innerHTML = `<span class="error">lunr.js failed to load from CDN.</span>`;
    return;
  }
  IDX = buildLunrIndices(DATA);
  hintEl.textContent =
    `Searching ${DATA.papers.length} papers, ${DATA.skills.length} skills, ` +
    `${DATA.tools.length} tools across ${(DATA.collections || []).length} collections.`;

  const input = document.getElementById("search-input");
  input.addEventListener("input", onInput);
  for (const id of ["filter-papers", "filter-skills", "filter-tools"]) {
    document.getElementById(id).addEventListener("change", () => render(input.value));
  }

  // Honor ?q= deep link
  const params = new URLSearchParams(window.location.search);
  const q0 = params.get("q");
  if (q0) {
    input.value = q0;
    render(q0);
  }
})();
