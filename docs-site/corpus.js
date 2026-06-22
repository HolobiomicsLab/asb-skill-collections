/* corpus.js — browse all collections' corpus.yaml ledgers (static, no backend) */

const RAW_BASE = "https://raw.githubusercontent.com/HolobiomicsLab/asb-skill-collections/main";
const CATALOGUE_URL = `${RAW_BASE}/catalogue.jsonld`;

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") node.className = v;
    else if (k.startsWith("on")) node.addEventListener(k.slice(2).toLowerCase(), v);
    else node.setAttribute(k, v);
  }
  for (const c of children) {
    if (c == null) continue;
    node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
  }
  return node;
}

async function fetchYAML(url) {
  const r = await fetch(url, { cache: "no-store" });
  if (!r.ok) throw new Error(`${r.status} ${url}`);
  return r.text();
}

async function fetchJSON(url) {
  const r = await fetch(url, { cache: "no-store" });
  if (!r.ok) throw new Error(`${r.status} ${url}`);
  return r.json();
}

// Tiny YAML parser sufficient for corpus.yaml (lists of dicts with scalar values + nested access dict)
// Falls back to a simple line-based scanner since we don't want to ship js-yaml for this single file.
function parseSimpleYAML(text) {
  // The corpus.yaml shape is: { schema_version, collection, ..., papers: [...] }
  // Each paper is a dict. We just need DOIs + a few scalar fields per paper.
  // For robustness, embed a minimal parser:
  const lines = text.split("\n");
  let papers = [];
  let current = null;
  let inPapers = false;
  let nestedKey = null;
  let collection = "";
  let collectionVersion = "";
  for (const raw of lines) {
    const line = raw.replace(/\r$/, "");
    if (line.startsWith("collection:")) collection = line.split(":").slice(1).join(":").trim().replace(/^['"]|['"]$/g, "");
    if (line.startsWith("collection_version:")) collectionVersion = line.split(":").slice(1).join(":").trim();
    if (line.match(/^papers:\s*$/)) { inPapers = true; continue; }
    if (!inPapers) continue;
    const m = line.match(/^- (\w+):\s*(.*)$/);
    if (m) {
      if (current) papers.push(current);
      current = { collection, collection_version: collectionVersion, [m[1]]: m[2].trim().replace(/^['"]|['"]$/g, "") };
      nestedKey = null;
      continue;
    }
    const flat = line.match(/^  (\w+):\s*(.*)$/);
    if (flat && current) {
      if (flat[2] === "" || flat[2] == null) {
        nestedKey = flat[1];
        current[nestedKey] = {};
      } else {
        current[flat[1]] = flat[2].trim().replace(/^['"]|['"]$/g, "");
        nestedKey = null;
      }
      continue;
    }
    const nested = line.match(/^    (\w+):\s*(.*)$/);
    if (nested && current && nestedKey) {
      current[nestedKey][nested[1]] = nested[2].trim().replace(/^['"]|['"]$/g, "");
      continue;
    }
  }
  if (current) papers.push(current);
  return papers;
}

async function loadAllCorpus() {
  let collections = [];
  try {
    const cat = await fetchJSON(CATALOGUE_URL);
    collections = cat?.collections ?? [];
  } catch {
    // No catalogue yet — fall back to a hard-coded list of one (metabolomics/v1).
    collections = [{ slug: "metabolomics", version: 1 }];
  }
  const all = [];
  for (const c of collections) {
    const slug = c.slug || (c["@id"] ?? "").split("/").slice(-3, -2)[0];
    const ver = c.version ?? 1;
    if (!slug) continue;
    // Try staged-collections first, then collections.
    const paths = [
      `${RAW_BASE}/staged-collections/${slug}/v${ver}/corpus.yaml`,
      `${RAW_BASE}/collections/${slug}/v${ver}/corpus.yaml`,
    ];
    for (const path of paths) {
      try {
        const text = await fetchYAML(path);
        const papers = parseSimpleYAML(text);
        for (const p of papers) {
          all.push({ ...p, _source_path: path });
        }
        break; // first hit wins
      } catch {
        // try next
      }
    }
  }
  return all;
}

function renderPapers(papers) {
  const container = document.getElementById("papers");
  container.innerHTML = "";

  // Filters
  const fColl = document.getElementById("filter-collection").value;
  const fStatus = document.getElementById("filter-status").value;
  const fAccess = document.getElementById("filter-access").value;
  const fSearch = document.getElementById("filter-search").value.toLowerCase().trim();

  let filtered = papers;
  if (fColl) filtered = filtered.filter(p => p.collection === fColl);
  if (fStatus) filtered = filtered.filter(p => p.status === fStatus);
  if (fAccess) filtered = filtered.filter(p => (p.access?.type || "unknown") === fAccess);
  if (fSearch) filtered = filtered.filter(p =>
    (p.doi || "").toLowerCase().includes(fSearch) ||
    (p.title || "").toLowerCase().includes(fSearch)
  );

  container.appendChild(el("p", { class: "hint" },
    `Showing ${filtered.length} of ${papers.length} papers`));

  if (!filtered.length) {
    container.appendChild(el("p", { class: "empty" }, "No matches."));
    return;
  }

  const table = el("table", { class: "catalogue" },
    el("thead", {},
      el("tr", {},
        el("th", {}, "DOI"),
        el("th", {}, "Title"),
        el("th", {}, "Collection"),
        el("th", {}, "Status"),
        el("th", {}, "Access"),
        el("th", {}, "Skills"),
        el("th", {}, "Tools"),
        el("th", {}, "Actions"),
      ),
    ),
    el("tbody"),
  );
  const tbody = table.querySelector("tbody");
  for (const p of filtered) {
    const doiHref = `https://doi.org/${p.doi}`;
    const paperHref = `./paper.html?doi=${encodeURIComponent(p.doi || "")}&collection=${encodeURIComponent(p.collection || "")}`;
    tbody.appendChild(el("tr", {},
      el("td", {}, el("a", { href: doiHref, target: "_blank" }, p.doi || "—")),
      el("td", {}, p.title || "—"),
      el("td", {}, p.collection || "—"),
      el("td", {}, p.status || "—"),
      el("td", {}, (p.access?.type) || "unknown"),
      el("td", {}, String(p.derived_skills ?? "—")),
      el("td", {}, String(p.derived_tools ?? "—")),
      el("td", {}, el("a", { href: paperHref }, "Review →")),
    ));
  }
  container.appendChild(table);
}

function populateCollectionFilter(papers) {
  const sel = document.getElementById("filter-collection");
  const seen = new Set();
  for (const p of papers) {
    if (p.collection && !seen.has(p.collection)) {
      seen.add(p.collection);
      sel.appendChild(el("option", { value: p.collection }, p.collection));
    }
  }
}

(async function init() {
  let papers;
  try {
    papers = await loadAllCorpus();
  } catch (e) {
    document.getElementById("papers").innerHTML =
      `<p class="error">Could not load corpus.yaml files: ${e.message}.<br>` +
      `(If the repository is still private, the static pages can't reach raw URLs yet.)</p>`;
    return;
  }
  populateCollectionFilter(papers);
  renderPapers(papers);
  for (const id of ["filter-collection", "filter-status", "filter-access", "filter-search"]) {
    document.getElementById(id).addEventListener("input", () => renderPapers(papers));
  }
})();
