// collections.js: per-collection browser for skills, workflows (super-skills) and tools.
// Reads the release registry (catalogue.jsonld) and the public search index of the
// collection's domain (search_index/<domain>.json) through site-data.js. The skill
// and tool files themselves are in the private domain repository and in the Zenodo
// record of the release; this page shows what the public index holds.
const MAX_RENDER = 60; // cap rendered cards; refine the filter to narrow
const TABS = ["skills", "workflows", "tools"];

const state = { manifest: null, labels: {}, entries: [], collection: null, tab: "skills", rows: null, loading: false, error: null };

// Topic as shown: its EDAM label (topicId and topicLabel are in site-data.js).
function topicName(iri) {
  return topicLabel(state.labels, iri);
}

function shorten(text, n) {
  return text.length > n ? text.slice(0, n - 1) + "…" : text;
}

// ---- summary card with a simple inline-SVG bar chart (basic graphics) ----
// pairs: [label, count, tooltip]
function barChart(pairs) {
  const max = Math.max(1, ...pairs.map(([, n]) => n));
  const rowH = 22, w = 520, labelW = 210, barW = w - labelW - 50;
  const svg = [`<svg viewBox="0 0 ${w} ${pairs.length * rowH + 8}" class="chart" role="img">`];
  pairs.forEach(([label, n], i) => {
    const y = i * rowH + 4;
    const len = Math.max(2, Math.round((n / max) * barW));
    svg.push(
      `<text x="0" y="${y + 13}" class="chart-label"><title>${siteEsc(pairs[i][2] || label)}</title>${siteEsc(shorten(label, 32))}</text>`,
      `<rect x="${labelW}" y="${y + 3}" width="${len}" height="14" rx="3" class="chart-bar"></rect>`,
      `<text x="${labelW + len + 6}" y="${y + 13}" class="chart-num">${n}</text>`
    );
  });
  svg.push("</svg>");
  return svg.join("");
}

function topicCounts(rows) {
  const counts = {};
  for (const r of rows) for (const t of (r.edam_topics || [])) counts[t] = (counts[t] || 0) + 1;
  return Object.entries(counts).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
}

function collectionRows(payload, label) {
  const pick = key => (payload[key] || []).filter(r => r.collection === label);
  return { skills: pick("skills"), workflows: pick("workflows"), tools: pick("tools"), papers: pick("papers") };
}

function renderSummary() {
  const c = state.collection;
  const box = document.getElementById("summary");
  if (!c) { box.innerHTML = ""; return; }
  const rows = state.rows;
  const n = (indexCount, registryCount) => {
    if (!rows) return registryCount != null ? registryCount : "—";
    return indexCount;
  };
  const stats = [
    ["Skills", n(rows && rows.skills.length, c.skills_count)],
    ["Workflows", n(rows && rows.workflows.length, null)],
    ["Tools", n(rows && rows.tools.length, c.tools_count)],
    ["Papers", n(rows && rows.papers.length, null)],
  ];
  const mismatch = rows && (rows.skills.length !== c.skills_count || rows.tools.length !== c.tools_count)
    ? `<p class="error">The public index holds ${rows.skills.length} skills and ${rows.tools.length} tools; ` +
      `the registry records ${c.skills_count} and ${c.tools_count}.</p>` : "";
  const doi = c.doi
    ? `<a href="${doiURL(c.doi)}" target="_blank" rel="noopener">${siteEsc(c.doi)}</a>` : "none";
  const released = (c.released_at || "").slice(0, 10);
  // The registry carries a capsules DOI only once that record is published.
  const capsules = c.capsules_doi
    ? ` · build capsules DOI <a href="${doiURL(c.capsules_doi)}" target="_blank" rel="noopener">${siteEsc(c.capsules_doi)}</a>` : "";
  box.innerHTML =
    `<div class="card summary-card">
       <div class="stat-row">
         ${stats.map(([k, v]) => `<div class="stat"><div class="stat-n">${siteEsc(v)}</div><div class="stat-k">${k}</div></div>`).join("")}
       </div>
       <p class="muted">${siteEsc(c.title || c.label)} · version ${siteEsc(c.version)} · released ${siteEsc(released || "")} · version DOI ${doi}${capsules}</p>
       ${mismatch}
       <p class="muted">This page shows what the public index holds for each item. The full text of every
         skill, workflow and tool record is in the Zenodo record of the release (${doi}) and in the private
         domain repository <code>${siteEsc(domainRepoName(c.slug))}</code> for people with access.</p>
       <div id="summary-chart"></div>
     </div>`;
  if (rows) {
    const counts = topicCounts(rows.skills).slice(0, 8)
      .map(([t, k]) => [topicName(t), k, `${topicName(t)} (${topicId(t)})`]);
    if (counts.length) {
      document.getElementById("summary-chart").innerHTML =
        `<p class="muted chart-title">Skills by EDAM topic</p>` + barChart(counts);
    }
  }
}

function populateTopicFilter() {
  const sel = document.getElementById("filter-topic");
  const want = sel.dataset.want || "";
  const counts = state.rows ? topicCounts(state.rows.skills) : [];
  sel.innerHTML = `<option value="">All EDAM topics</option>` +
    counts.map(([t, k]) => {
      const name = topicName(t), id = topicId(t);
      return `<option value="${siteEsc(t)}">${siteEsc(name === id ? id : `${name} (${id})`)}: ${k}</option>`;
    }).join("");
  if (want && counts.some(([t]) => t === want)) sel.value = want;
  if (state.rows) delete sel.dataset.want;
}

// ---- item card renderers ----
function suggestLink(target, item) {
  const href = `contribute.html?collection=${encodeURIComponent(state.collection.label)}` +
    `&target=${target}&item=${encodeURIComponent(item)}`;
  return `<a href="${href}">Suggest improvement</a>`;
}

function doiLinks(dois) {
  return (dois || []).map(d =>
    `<a href="paper.html?doi=${encodeURIComponent(d)}&amp;collection=${encodeURIComponent(state.collection.label)}">${siteEsc(d)}</a>`
  ).join(", ");
}

function skillCard(r) {
  const topics = (r.edam_topics || []).map(t =>
    `<a class="badge" href="${siteEsc(t)}" title="${siteEsc(topicId(t))}" target="_blank" rel="noopener">${siteEsc(topicName(t))}</a>`).join("");
  const sources = (r.source_dois || []).length
    ? `<p class="muted">Source paper: ${doiLinks(r.source_dois)}</p>` : "";
  const negative = (r.when_to_use_negative || "").trim()
    ? `<details><summary class="muted">When not to use</summary><p class="item-desc">${siteEsc(r.when_to_use_negative.trim())}</p></details>` : "";
  return `<div class="card item">
      <div class="item-head"><span class="item-name">${siteEsc(r.name)}</span></div>
      <p class="item-desc">${siteEsc((r.description || "").trim())}</p>
      ${r.summary ? `<p class="item-desc muted">${siteEsc(r.summary.trim())}</p>` : ""}
      ${negative}
      <div class="badges">${topics}</div>
      ${sources}
      <div class="item-actions">${suggestLink("skills", r.name)}</div>
    </div>`;
}

function workflowCard(r) {
  const techs = (r.techniques || []).map(t => `<span class="badge badge-skill">${siteEsc(t)}</span>`).join("");
  return `<div class="card item">
      <div class="item-head"><span class="item-name">${siteEsc(r.name || r.slug)}</span>
        ${r.stage_count ? `<span class="muted">${r.stage_count} stages</span>` : ""}</div>
      <p class="item-desc">${siteEsc((r.description || "").trim())}</p>
      ${r.summary ? `<p class="item-desc muted">${siteEsc(r.summary.trim())}</p>` : ""}
      ${techs ? `<div class="badges">${techs}</div>` : ""}
      <div class="item-actions">${suggestLink("workflows", r.slug || r.name)}</div>
    </div>`;
}

function toolCard(r) {
  const allRepos = r.source_paper_repos || [];
  const repos = allRepos.slice(0, 4).map(u => /^https?:\/\//.test(u)
    ? `<a href="${siteEsc(u)}" target="_blank" rel="noopener">${siteEsc(u)}</a>` : siteEsc(u)).join(", ") +
    (allRepos.length > 4 ? ` and ${allRepos.length - 4} more` : "");
  const evidence = (r.evidence_text || "").trim();
  const meta = [
    `<code>${siteEsc(r.slug)}</code>`,
    r.license_spdx ? `licence ${siteEsc(r.license_spdx)}` : "",
    r.source_doi ? `source <a href="${doiURL(r.source_doi)}" target="_blank" rel="noopener">${siteEsc(r.source_doi)}</a>` : "",
  ].filter(Boolean).join(" · ");
  return `<div class="card item">
      <div class="item-head"><span class="item-name">${siteEsc(r.name || r.slug)}</span></div>
      <p class="muted">${meta}</p>
      ${repos ? `<p class="item-desc">Code cited by the source paper: ${repos}</p>` : ""}
      ${evidence ? `<p class="item-desc muted">${siteEsc(evidence.length > 400 ? evidence.slice(0, 399) + "…" : evidence)}</p>` : ""}
      <div class="item-actions">${suggestLink("tools", r.slug || r.name)}</div>
    </div>`;
}

function matches(r, q) {
  if (!q) return true;
  const hay = `${r.name || ""} ${r.slug || ""} ${r.description || ""} ${r.summary || ""} ` +
    `${(r.source_dois || []).join(" ")} ${r.source_doi || ""} ${r.license_spdx || ""} ` +
    `${(r.edam_topics || []).map(topicName).join(" ")}`.toLowerCase();
  return q.toLowerCase().split(/\s+/).every(t => hay.includes(t));
}

function writeURL() {
  const c = state.collection;
  if (!c) return;
  const url = new URL(window.location.href);
  url.searchParams.set("c", c.slug);
  url.searchParams.set("v", c.version);
  url.searchParams.set("tab", state.tab);
  const q = document.getElementById("filter-q").value.trim();
  if (q) url.searchParams.set("q", q); else url.searchParams.delete("q");
  const topic = document.getElementById("filter-topic").value;
  if (topic && state.tab === "skills") url.searchParams.set("topic", topicId(topic)); else url.searchParams.delete("topic");
  window.history.replaceState(null, "", url.toString());
}

function renderResults() {
  const results = document.getElementById("results");
  const meta = document.getElementById("result-meta");
  const tab = state.tab;
  const topicSel = document.getElementById("filter-topic");
  topicSel.hidden = tab !== "skills";
  if (!state.collection) return;
  if (state.loading) {
    const size = siteBytes(((state.manifest.domains || {})[state.collection.slug] || {}).bytes);
    results.innerHTML = `<p class="loading">Loading the ${siteEsc(state.collection.slug)} index (${size})…</p>`;
    meta.textContent = "";
    return;
  }
  if (state.error || !state.rows) {
    results.innerHTML = `<p class="error">Could not load the ${siteEsc(state.collection.slug)} index: ${siteEsc(state.error || "unknown error")}.</p>`;
    meta.textContent = "";
    return;
  }
  const rows = state.rows[tab];
  const q = document.getElementById("filter-q").value.trim();
  const topic = tab === "skills" ? topicSel.value : "";
  const filtered = rows.filter(r => matches(r, q) && (!topic || (r.edam_topics || []).includes(topic)));
  const render = filtered.slice(0, MAX_RENDER);
  const card = tab === "workflows" ? workflowCard : tab === "tools" ? toolCard : skillCard;
  meta.textContent = `${filtered.length} ${tab}${filtered.length !== rows.length ? ` (of ${rows.length})` : ""}` +
    (filtered.length > render.length ? `, showing the first ${render.length}; refine the filter to narrow` : "");
  results.innerHTML = render.length ? render.map(card).join("") : `<p class="loading">No ${tab} match.</p>`;
  writeURL();
}

async function selectCollection(c) {
  state.collection = c;
  state.rows = null; state.error = null; state.loading = true;
  renderSummary();
  populateTopicFilter();
  renderResults();
  keepOnlyDomain(c.slug);
  try {
    const payload = await loadDomain(state.manifest, c.slug);
    if (state.collection !== c) return; // another selection superseded this one
    state.rows = collectionRows(payload, c.label);
  } catch (e) {
    if (state.collection !== c) return;
    state.error = e.message;
  }
  state.loading = false;
  renderSummary();
  populateTopicFilter();
  renderResults();
}

function renderNotBrowsable(entries) {
  const box = document.getElementById("not-browsable");
  const others = entries.filter(c => !(c.released && c.indexed));
  if (!others.length) { box.innerHTML = ""; return; }
  const items = others.map(c => {
    const why = c.released
      ? "an earlier release, not in the public index"
      : "staged, not part of a release";
    const doi = c.doi ? ` · <a href="${doiURL(c.doi)}" target="_blank" rel="noopener">${siteEsc(c.doi)}</a>` : "";
    return `<li><code>${siteEsc(c.label)}</code>: ${why}${doi}</li>`;
  }).join("");
  box.innerHTML = `<details><summary class="muted">Not browsable here (${others.length})</summary>` +
    `<ul class="muted">${items}</ul>` +
    `<p class="muted">Rows of staged trees that the public index holds appear in <a href="./search.html">Search</a> with a staged label.</p></details>`;
}

async function init() {
  const sel = document.getElementById("collection-select");
  let catalogue;
  try {
    // loadTopicLabels never rejects: without the file, topics show their ids.
    [catalogue, state.manifest, state.labels] = await Promise.all([loadCatalogue(), loadManifest(), loadTopicLabels()]);
  } catch (e) {
    document.getElementById("results").innerHTML = `<p class="error">Could not load the registry or the index: ${siteEsc(e.message)}.</p>`;
    return;
  }
  const all = joinRegistry(catalogue, state.manifest);
  const entries = all.filter(c => c.released && c.indexed)
    .sort((a, b) => a.slug.localeCompare(b.slug) || Number(a.version) - Number(b.version));
  state.entries = entries;
  renderNotBrowsable(all);
  if (!entries.length) { sel.innerHTML = "<option>No released collection in the public index</option>"; return; }
  sel.innerHTML = entries.map((c, i) => {
    const size = siteBytes(((state.manifest.domains || {})[c.slug] || {}).bytes);
    return `<option value="${i}">${siteEsc(c.title || c.label)} (${size} to download)</option>`;
  }).join("");
  sel.addEventListener("change", () => {
    document.getElementById("filter-q").value = "";
    selectCollection(entries[sel.value]);
  });

  const params = new URLSearchParams(location.search);
  const wantTab = params.get("tab");
  if (TABS.includes(wantTab)) state.tab = wantTab;
  document.querySelectorAll(".tab").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.tab === state.tab);
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.tab = btn.dataset.tab;
      renderResults();
    });
  });
  document.getElementById("filter-q").addEventListener("input", renderResults);
  document.getElementById("filter-topic").addEventListener("change", renderResults);
  if (params.get("q")) document.getElementById("filter-q").value = params.get("q");
  if (params.get("topic")) document.getElementById("filter-topic").dataset.want = `http://edamontology.org/${params.get("topic")}`;

  // Deep link ?c=<slug>[&v=<version>]; without one, the manifest's default domain.
  const want = params.get("c") || ((state.manifest.default_domains || [])[0]);
  const wantV = params.get("v");
  const note = document.getElementById("collection-note");
  let idx = entries.findIndex(c => c.slug === want && (!wantV || String(c.version) === wantV));
  if (idx < 0 && params.get("c")) {
    const asked = all.find(c => c.slug === want && (!wantV || String(c.version) === wantV));
    note.textContent = asked
      ? `${asked.label} is not browsable here (see the list below the selector).`
      : `No collection ${want}${wantV ? "/v" + wantV : ""} in the registry.`;
    idx = entries.findIndex(c => c.slug === want);
  }
  if (idx < 0) idx = Math.max(0, entries.findIndex(c => c.slug === (state.manifest.default_domains || [])[0]));
  sel.value = idx;
  selectCollection(entries[idx]);
}

document.addEventListener("DOMContentLoaded", init);
