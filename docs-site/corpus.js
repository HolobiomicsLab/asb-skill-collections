/* corpus.js: source papers of one domain, read from the public index.
 *
 * The papers of every collection of a domain are in search_index/<domain>.json
 * (loaded through site-data.js). One domain is loaded at a time: the manifest's
 * default domain, or the one named in ?domain=, or the one picked in the selector,
 * whose download size the selector shows.
 */

let MANIFEST = null;
let PAPERS = [];
let STATUS = {};   // collection label -> "released" | "staged"
let SKILL_COUNT = new Map();  // "<collection> <doi lower case>" -> skills citing that paper

// The ledger fields derived_skills and derived_tools are 0 in every index file,
// so the skill count is computed from the source_dois of the skills instead.
// The index does not link tools to papers, so no tool count is shown.
function countSkillsByPaper(skills) {
  const counts = new Map();
  for (const s of skills || []) {
    for (const d of s.source_dois || []) {
      const key = `${s.collection} ${String(d).toLowerCase()}`;
      counts.set(key, (counts.get(key) || 0) + 1);
    }
  }
  return counts;
}

function fillSelect(id, values, allLabel) {
  const sel = document.getElementById(id);
  const keep = sel.value;
  sel.innerHTML = "";
  sel.appendChild(siteEl("option", { value: "" }, allLabel));
  for (const v of values) sel.appendChild(siteEl("option", { value: v }, v));
  if (values.includes(keep)) sel.value = keep;
}

function distinct(key) {
  return [...new Set(PAPERS.map(p => p[key] || "unknown"))].sort();
}

function collectionCell(label) {
  return siteEl("td", {}, label || "—",
    STATUS[label] === "staged" ? " " : null,
    STATUS[label] === "staged" ? siteEl("span", { class: "badge badge-staged" }, "staged") : null);
}

function renderPapers() {
  const container = document.getElementById("papers");
  container.innerHTML = "";
  const fColl = document.getElementById("filter-collection").value;
  const fStatus = document.getElementById("filter-status").value;
  const fAccess = document.getElementById("filter-access").value;
  const fSearch = document.getElementById("filter-search").value.toLowerCase().trim();

  let filtered = PAPERS;
  if (fColl) filtered = filtered.filter(p => p.collection === fColl);
  if (fStatus) filtered = filtered.filter(p => (p.status || "unknown") === fStatus);
  if (fAccess) filtered = filtered.filter(p => (p.access_type || "unknown") === fAccess);
  if (fSearch) filtered = filtered.filter(p =>
    (p.doi || "").toLowerCase().includes(fSearch) ||
    (p.title || "").toLowerCase().includes(fSearch));

  container.appendChild(siteEl("p", { class: "hint" }, `Showing ${filtered.length} of ${PAPERS.length} papers`));
  if (!filtered.length) {
    container.appendChild(siteEl("p", { class: "empty" }, "No matches."));
    return;
  }
  const tbody = siteEl("tbody");
  for (const p of filtered) {
    const paperHref = `./paper.html?doi=${encodeURIComponent(p.doi || "")}&collection=${encodeURIComponent(p.collection || "")}`;
    tbody.appendChild(siteEl("tr", {},
      siteEl("td", {}, p.doi ? siteEl("a", { href: doiURL(p.doi), target: "_blank", rel: "noopener" }, p.doi) : "—"),
      siteEl("td", {}, p.title || "—"),
      collectionCell(p.collection),
      siteEl("td", {}, p.status || "—"),
      siteEl("td", {}, p.access_type || "unknown"),
      siteEl("td", {}, String(SKILL_COUNT.get(`${p.collection} ${String(p.doi || "").toLowerCase()}`) || 0)),
      siteEl("td", {}, siteEl("a", { href: paperHref }, "Details")),
    ));
  }
  container.appendChild(siteEl("table", { class: "catalogue" },
    siteEl("thead", {}, siteEl("tr", {},
      ...["DOI", "Title", "Collection", "Status", "Access", "Skills", ""].map(h => siteEl("th", {}, h)))),
    tbody));
}

async function selectDomain(slug) {
  const entry = MANIFEST.domains[slug];
  const container = document.getElementById("papers");
  container.innerHTML = "";
  container.appendChild(siteEl("p", { class: "loading" }, `Loading the ${slug} index (${siteBytes(entry.bytes)})…`));
  const url = new URL(window.location.href);
  url.searchParams.set("domain", slug);
  window.history.replaceState(null, "", url.toString());
  keepOnlyDomain(slug);
  let payload;
  try {
    payload = await loadDomain(MANIFEST, slug);
  } catch (e) {
    container.innerHTML = "";
    container.appendChild(siteEl("p", { class: "error" }, `Could not load the ${slug} index: ${e.message}.`));
    return;
  }
  if (document.getElementById("filter-domain").value !== slug) return;
  PAPERS = payload.papers || [];
  STATUS = payload.collection_status || {};
  SKILL_COUNT = countSkillsByPaper(payload.skills);
  fillSelect("filter-collection", [...new Set(PAPERS.map(p => p.collection))].sort(), "All");
  fillSelect("filter-status", distinct("status"), "All");
  fillSelect("filter-access", distinct("access_type"), "All");
  renderPapers();
}

(async function init() {
  try {
    MANIFEST = await loadManifest();
  } catch (e) {
    document.getElementById("papers").innerHTML =
      `<p class="error">Could not load the index manifest: ${siteEsc(e.message)}.</p>`;
    return;
  }
  const domains = Object.keys(MANIFEST.domains || {}).sort();
  const sel = document.getElementById("filter-domain");
  sel.innerHTML = "";
  for (const slug of domains) {
    const entry = MANIFEST.domains[slug];
    sel.appendChild(siteEl("option", { value: slug },
      `${slug} (${(entry.counts || {}).papers || 0} papers, ${siteBytes(entry.bytes)})`));
  }
  const asked = new URLSearchParams(window.location.search).get("domain");
  const start = domains.includes(asked) ? asked
    : ((MANIFEST.default_domains || []).find(d => domains.includes(d)) || domains[0]);
  if (asked && asked !== start) {
    document.getElementById("domain-note").textContent = `Not in the index: ${asked}.`;
  }
  sel.value = start;
  sel.addEventListener("change", () => selectDomain(sel.value));
  for (const id of ["filter-collection", "filter-status", "filter-access", "filter-search"]) {
    document.getElementById(id).addEventListener("input", renderPapers);
  }
  await selectDomain(start);
})();
