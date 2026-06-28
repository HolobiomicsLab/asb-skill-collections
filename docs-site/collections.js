// collections.js — per-collection browser for skills / workflows (super-skills) / tools.
// Reads the collection's machine indexes from GitHub raw (decoupled from the search
// index) and links every item back to its source on GitHub for direct contribution.
const REPO = "HolobiomicsLab/asb-skill-collections";
const BRANCH = "main";
const RAW = `https://raw.githubusercontent.com/${REPO}/${BRANCH}`;
const BLOB = `https://github.com/${REPO}/blob/${BRANCH}`;
const EDIT = `https://github.com/${REPO}/edit/${BRANCH}`;
const MAX_RENDER = 60; // cap rendered cards; refine the filter to narrow

const state = { collection: null, tab: "skills", data: {}, loading: {} };

function el(tag, attrs = {}, ...children) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "html") e.innerHTML = v;
    else e.setAttribute(k, v);
  }
  for (const c of children) {
    if (c == null) continue;
    e.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
  }
  return e;
}

async function fetchJSON(path) {
  const resp = await fetch(`${RAW}/${path}`);
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
  return resp.json();
}

// Escape text before it goes into innerHTML. Index data is trusted (curated repo)
// but descriptions/tool names contain '<', '>', '&' (e.g. "Python >= 3.8",
// "mzspec:<ns>:<id>") that would otherwise be parsed as tags and dropped.
function esc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, c =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

function collDir(c) {
  return `collections/${c.slug}/v${c.version}`;
}

function indexPath(c, tab) {
  const d = collDir(c);
  if (tab === "workflows") return `${d}/workflows/workflows_index.json`;
  if (tab === "tools") return `${d}/tools_index.json`;
  return `${d}/skills_index.json`;
}

// ---- summary card with a simple inline-SVG bar chart (basic graphics) ----
function barChart(pairs) {
  const max = Math.max(1, ...pairs.map(([, n]) => n));
  const rowH = 22, w = 460, labelW = 150, barW = w - labelW - 50;
  const svg = [`<svg viewBox="0 0 ${w} ${pairs.length * rowH + 8}" class="chart" role="img">`];
  pairs.forEach(([label, n], i) => {
    const y = i * rowH + 4;
    const len = Math.max(2, Math.round((n / max) * barW));
    svg.push(
      `<text x="0" y="${y + 13}" class="chart-label">${esc(label)}</text>`,
      `<rect x="${labelW}" y="${y + 3}" width="${len}" height="14" rx="3" class="chart-bar"></rect>`,
      `<text x="${labelW + len + 6}" y="${y + 13}" class="chart-num">${n}</text>`
    );
  });
  svg.push("</svg>");
  return svg.join("");
}

function renderSummary() {
  const c = state.collection;
  const box = document.getElementById("summary");
  if (!c) { box.innerHTML = ""; return; }
  const stats = [
    ["Skills", c.skills_count || "—"],
    ["Tools", c.tools_count || "—"],
    ["Workflows", c.workflows_count != null ? c.workflows_count : "—"],
  ];
  const doi = c.doi
    ? `<a href="https://doi.org/${c.doi}" target="_blank" rel="noopener">${c.doi}</a>` : "—";
  box.innerHTML =
    `<div class="card summary-card">
       <div class="stat-row">
         ${stats.map(([k, v]) => `<div class="stat"><div class="stat-n">${v}</div><div class="stat-k">${k}</div></div>`).join("")}
       </div>
       <p class="muted">Version ${c.version} · DOI ${doi} ·
         <a href="${BLOB}/${collDir(c)}" target="_blank" rel="noopener">source on GitHub</a></p>
       <div id="summary-chart"></div>
     </div>`;
}

function techniqueCounts(rows) {
  const counts = {};
  for (const r of rows) for (const t of (r.techniques || [])) counts[t] = (counts[t] || 0) + 1;
  return Object.entries(counts).sort((a, b) => b[1] - a[1]);
}

function populateTechniqueFilter(rows) {
  const sel = document.getElementById("filter-technique");
  const techs = techniqueCounts(rows).map(([t]) => t);
  sel.innerHTML = `<option value="">All techniques</option>` +
    techs.map(t => `<option value="${t}">${t}</option>`).join("");
}

// ---- item card renderers ----
function actions(viewPath, target, slug) {
  const item = `contribute.html?collection=${encodeURIComponent(state.collection.slug + "/v" + state.collection.version)}` +
               `&target=${target}&item=${encodeURIComponent(slug)}`;
  return `<div class="item-actions">
      <a href="${BLOB}/${viewPath}" target="_blank" rel="noopener">View</a>
      <a href="${EDIT}/${viewPath}" target="_blank" rel="noopener">Edit on GitHub</a>
      <a href="${item}">Suggest improvement</a>
    </div>`;
}

function skillCard(r) {
  const path = `${collDir(state.collection)}/skills/${r.slug}/SKILL.md`;
  const tools = (r.tools || []).slice(0, 6).map(t => `<span class="badge badge-tool">${esc(t)}</span>`).join("");
  const techs = (r.techniques || []).map(t => `<span class="badge badge-skill">${esc(t)}</span>`).join("");
  return `<div class="card item">
      <div class="item-head"><span class="item-name">${esc(r.name || r.slug)}</span></div>
      <p class="item-desc">${esc((r.description || "").trim())}</p>
      <div class="badges">${techs}${tools}</div>
      ${actions(path, "skills", r.slug)}
    </div>`;
}

function workflowCard(r) {
  const path = `${collDir(state.collection)}/workflows/${r.slug}/SKILL.md`;
  const techs = (r.techniques || []).map(t => `<span class="badge badge-skill">${esc(t)}</span>`).join("");
  const stages = (r.stages || []).map(s => `<span class="badge">${esc(s)}</span>`).join(" → ");
  const tools = (r.member_tools || []).slice(0, 8).map(t => `<span class="badge badge-tool">${esc(t)}</span>`).join("");
  return `<div class="card item">
      <div class="item-head"><span class="item-name">${esc(r.name || r.slug)}</span>
        <span class="muted">${r.stage_count || (r.stages || []).length} stages</span></div>
      <p class="item-desc">${esc((r.description || "").trim())}</p>
      <div class="stages">${stages}</div>
      <div class="badges">${techs}${tools}</div>
      ${actions(path, "workflows", r.slug)}
    </div>`;
}

function toolCard(r) {
  const path = `${collDir(state.collection)}/tools/${r.slug}.yaml`;
  const url = r.canonical_url
    ? `<a href="${encodeURI(r.canonical_url)}" target="_blank" rel="noopener">${esc(r.canonical_url)}</a>` : "";
  return `<div class="card item">
      <div class="item-head"><span class="item-name">${esc(r.name || r.slug)}</span></div>
      <p class="item-desc">${url}</p>
      <div class="badges">${(r.edam_topics || []).slice(0, 4).map(t => `<span class="badge">${esc(t.split("/").pop())}</span>`).join("")}</div>
      ${actions(path, "tools", r.slug)}
    </div>`;
}

function matches(r, q) {
  if (!q) return true;
  const hay = `${r.name || ""} ${r.slug || ""} ${r.description || ""} ${(r.tools || r.member_tools || []).join(" ")}`.toLowerCase();
  return q.toLowerCase().split(/\s+/).every(t => hay.includes(t));
}

function renderResults() {
  const results = document.getElementById("results");
  const meta = document.getElementById("result-meta");
  const c = state.collection, tab = state.tab;
  if (!c) return;
  const rows = state.data[tab];
  if (state.loading[tab]) { results.innerHTML = `<p class="loading">Loading ${tab}…</p>`; meta.textContent = ""; return; }
  if (!rows) { results.innerHTML = `<p class="error">Could not load ${tab}.</p>`; return; }
  const q = document.getElementById("filter-q").value.trim();
  const tech = document.getElementById("filter-technique").value;
  const filtered = rows.filter(r => matches(r, q) && (!tech || (r.techniques || []).includes(tech)));
  const render = filtered.slice(0, MAX_RENDER);
  const card = tab === "workflows" ? workflowCard : tab === "tools" ? toolCard : skillCard;
  meta.textContent = `${filtered.length} ${tab}${filtered.length !== rows.length ? ` (of ${rows.length})` : ""}` +
    (filtered.length > render.length ? ` — showing first ${render.length}, refine to narrow` : "");
  results.innerHTML = render.length ? render.map(card).join("") : `<p class="loading">No ${tab} match.</p>`;
}

async function loadTab(tab) {
  const c = state.collection;
  if (!c || state.data[tab] || state.loading[tab]) return;
  state.loading[tab] = true;
  renderResults();
  try {
    state.data[tab] = await fetchJSON(indexPath(c, tab));
    if (tab === "skills") {
      populateTechniqueFilter(state.data[tab]);
      const counts = techniqueCounts(state.data[tab]).slice(0, 8);
      const chart = document.getElementById("summary-chart");
      if (chart && counts.length) chart.innerHTML = `<p class="muted chart-title">Skills by technique</p>` + barChart(counts);
    }
  } catch (e) {
    state.data[tab] = null;
  } finally {
    state.loading[tab] = false;
    renderResults();
  }
}

function selectCollection(c) {
  state.collection = c;
  state.data = {}; state.loading = {};
  document.getElementById("filter-q").value = "";
  document.getElementById("filter-technique").innerHTML = `<option value="">All techniques</option>`;
  renderSummary();
  loadTab(state.tab);
}

async function init() {
  const sel = document.getElementById("collection-select");
  let cols = [];
  try {
    const cat = await fetchJSON("catalogue.jsonld");
    cols = cat.collections || [];
  } catch (e) {
    document.getElementById("results").innerHTML = `<p class="error">Failed to load catalogue: ${e.message}</p>`;
    return;
  }
  if (!cols.length) { sel.innerHTML = "<option>No collections released</option>"; return; }
  sel.innerHTML = cols.map((c, i) => `<option value="${i}">${c.title || c.slug} (v${c.version})</option>`).join("");
  sel.addEventListener("change", () => selectCollection(cols[sel.value]));

  document.querySelectorAll(".tab").forEach(btn => btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    state.tab = btn.dataset.tab;
    loadTab(state.tab);
    renderResults();
  }));
  document.getElementById("filter-q").addEventListener("input", renderResults);
  document.getElementById("filter-technique").addEventListener("change", renderResults);

  // deep-link ?c=<slug>
  const want = new URLSearchParams(location.search).get("c");
  const startIdx = want ? Math.max(0, cols.findIndex(c => c.slug === want)) : 0;
  sel.value = startIdx;
  selectCollection(cols[startIdx]);
}

document.addEventListener("DOMContentLoaded", init);
