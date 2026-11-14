/* site-data.js: public data shared by the Browse, Corpus and Paper pages.
 *
 * Two public sources only:
 *   - the release registry, catalogue.jsonld, read from this repository's raw
 *     files on the main branch (titles, versions, status, counts, version DOIs);
 *   - the search index served next to the pages, search_index/manifest.json and
 *     search_index/<domain>.json (skills, workflows, tools and papers).
 * The collection trees themselves live in the domain repositories
 * (HolobiomicsLab/asb-skills-<domain>); no page requests anything from them.
 * A domain file is fetched with the same URL as search.js, so the browser cache
 * serves it once to every page.
 */

const SITE_REPO = "HolobiomicsLab/asb-skill-collections";
const CATALOGUE_URL = `https://raw.githubusercontent.com/${SITE_REPO}/main/catalogue.jsonld`;
const SITE_INDEX_BASE = "./search_index/";

function siteEl(tag, attrs = {}, ...children) {
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

function siteEsc(s) {
  return String(s == null ? "" : s).replace(/[&<>"']/g, c =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

/** Human-readable size: 34990781 -> "35.0 MB". */
function siteBytes(n) {
  if (!Number.isFinite(n)) return "";
  if (n >= 1e6) return `${(n / 1e6).toFixed(1)} MB`;
  if (n >= 1e3) return `${Math.round(n / 1e3)} kB`;
  return `${n} B`;
}

function doiURL(doi) {
  return `https://doi.org/${encodeURI(doi)}`;
}

/** "proteomics/v1" -> { slug: "proteomics", version: "1" }; "proteomics" -> { slug, version: null }. */
function parseLabel(label) {
  const m = String(label || "").match(/^([^/]+)(?:\/v(\d+))?$/);
  return m ? { slug: m[1], version: m[2] || null } : { slug: "", version: null };
}

/** Domain repository of a domain, named in text only, never linked. */
function domainRepoName(slug) {
  return `${SITE_REPO.split("/")[0]}/asb-skills-${slug}`;
}

let _catalogue = null;
let _manifest = null;
let _topicLabels = null;
const _domains = new Map();

/**
 * EDAM topic labels (edam_topic_labels.json, built by build_edam_topic_labels.py),
 * as { "topic_3520": "Proteomics experiment", ... }. Loaded once per page; the
 * 17 kB file is revalidated (no-cache) rather than keyed by a hash, since no
 * manifest records one. Resolves to {} when the file cannot be read, so every
 * caller falls back to the id.
 */
async function loadTopicLabels() {
  if (!_topicLabels) {
    _topicLabels = fetch("./edam_topic_labels.json", { cache: "no-cache" })
      .then(r => (r.ok ? r.json() : {}))
      .then(d => (d && d.labels) || {})
      .catch(() => ({}));
  }
  return _topicLabels;
}

/** "http://edamontology.org/topic_3520" or "topic_3520" -> "topic_3520". */
function topicId(iri) {
  return String(iri || "").split("/").pop();
}

/** Label of a topic from a loaded label map, or its id when there is none. */
function topicLabel(labels, iri) {
  const id = topicId(iri);
  return (labels && labels[id]) || id;
}

async function loadCatalogue() {
  if (!_catalogue) {
    _catalogue = fetch(CATALOGUE_URL, { cache: "no-cache" }).then(r => {
      if (!r.ok) throw new Error(`${r.status} catalogue.jsonld`);
      return r.json();
    });
  }
  return _catalogue;
}

async function loadManifest() {
  if (!_manifest) {
    _manifest = fetch(SITE_INDEX_BASE + "manifest.json", { cache: "no-store" }).then(r => {
      if (!r.ok) throw new Error(`${r.status} manifest.json`);
      return r.json();
    });
  }
  return _manifest;
}

/** One domain file of the search index; the sha256 in the query keys the browser cache. */
async function loadDomain(manifest, slug) {
  const entry = (manifest.domains || {})[slug];
  if (!entry) throw new Error(`${slug} is not in the public index`);
  if (!_domains.has(slug)) {
    const url = `${SITE_INDEX_BASE}${encodeURIComponent(entry.file)}?v=${encodeURIComponent((entry.sha256 || "").slice(0, 16))}`;
    const p = fetch(url).then(r => {
      if (!r.ok) throw new Error(`${r.status} ${entry.file}`);
      return r.json();
    });
    p.catch(() => _domains.delete(slug));
    _domains.set(slug, p);
  }
  return _domains.get(slug);
}

/** Drop the other domains from memory; one domain file can weigh 35 MB. */
function keepOnlyDomain(slug) {
  for (const d of [..._domains.keys()]) if (d !== slug) _domains.delete(d);
}

/**
 * Registry entries joined with the public index. Each entry carries the
 * catalogue fields plus `label` ("slug/vN"), `released`, and `indexed`
 * (the index holds this collection's rows, so the site can show them).
 */
function joinRegistry(catalogue, manifest) {
  const indexed = new Set();
  for (const entry of Object.values(manifest.domains || {})) {
    for (const c of entry.collections || []) indexed.add(c.label);
  }
  return (catalogue.collections || []).map(c => {
    const label = `${c.slug}/v${c.version}`;
    return { ...c, label, released: c.status === "released", indexed: indexed.has(label) };
  });
}
