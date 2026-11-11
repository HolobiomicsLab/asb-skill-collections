/* paper.js: one source paper and the skills derived from it, from the public index.
 *
 * ?doi=<doi>&collection=<slug>/v<N> (or ?collection=<slug>, or the older
 * ?collection=<slug>&version=<N>). The paper row and its skills come from
 * search_index/<slug>.json, the release DOI from catalogue.jsonld, both through
 * site-data.js. Nothing is read from the private domain repositories.
 */

function getParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

function makeIssueURL({ title, body, labels = [], template = "" }) {
  const params = new URLSearchParams();
  if (template) params.set("template", template);
  params.set("title", title);
  params.set("body", body);
  if (labels.length) params.set("labels", labels.join(","));
  return `https://github.com/${SITE_REPO}/issues/new?${params.toString()}`;
}

function setBody(id, ...nodes) {
  const box = document.getElementById(id);
  box.innerHTML = "";
  for (const n of nodes) if (n) box.appendChild(n);
}

function fail(message) {
  document.getElementById("paper-meta").textContent = "";
  setBody("meta-card", siteEl("p", { class: "error" }, message));
  for (const id of ["skills-list", "tools-list"]) setBody(id);
}

(async function init() {
  const doi = (getParam("doi") || "").trim();
  const parsed = parseLabel(getParam("collection") || "");
  const version = parsed.version || getParam("version");
  const slug = parsed.slug;
  if (!doi) { fail("No DOI given. Use ?doi=10.xxxx/...&collection=<domain>/v<N>."); return; }
  document.getElementById("paper-title").textContent = `Paper ${doi}`;
  if (!slug) { fail("No collection given. Use ?doi=...&collection=<domain>/v<N>."); return; }

  let manifest;
  try { manifest = await loadManifest(); } catch (e) { fail(`Could not load the index manifest: ${e.message}.`); return; }
  if (!(manifest.domains || {})[slug]) { fail(`The domain ${slug} is not in the public index.`); return; }
  document.getElementById("paper-meta").textContent =
    `Loading the ${slug} index (${siteBytes(manifest.domains[slug].bytes)})…`;
  let payload;
  try { payload = await loadDomain(manifest, slug); } catch (e) { fail(`Could not load the ${slug} index: ${e.message}.`); return; }
  // The registry gives the version DOI; the page still works without it.
  let catalogue = null;
  try { catalogue = await loadCatalogue(); } catch { /* DOI of the release not shown */ }

  const key = doi.toLowerCase();
  const status = payload.collection_status || {};
  const rows = (payload.papers || []).filter(p => String(p.doi || "").toLowerCase() === key);
  if (!rows.length) { fail(`The ${slug} index has no paper with DOI ${doi}.`); return; }
  const wanted = version ? `${slug}/v${version}` : null;
  const paper = rows.find(p => p.collection === wanted)
    || rows.find(p => status[p.collection] === "released") || rows[0];
  const label = paper.collection;
  const entry = catalogue ? joinRegistry(catalogue, manifest).find(c => c.label === label) : null;

  // ---- the paper itself ----
  document.getElementById("paper-title").textContent = paper.title || doi;
  document.getElementById("paper-meta").textContent =
    `${label}${status[label] === "staged" ? " (staged, not part of a release)" : ""} · ${paper.status || "?"} · ${paper.access_type || "unknown access"}`;
  const others = rows.filter(p => p !== paper).map(p => p.collection);
  setBody("meta-card",
    siteEl("p", {}, "DOI ", siteEl("a", { href: doiURL(doi), target: "_blank", rel: "noopener" }, doi)),
    paper.rationale ? siteEl("p", {}, paper.rationale) : null,
    others.length ? siteEl("p", { class: "hint" }, `Also in ${others.join(", ")}.`) : null,
    wanted && wanted !== label ? siteEl("p", { class: "hint" }, `${wanted} does not list this paper; showing ${label}.`) : null);

  // ---- skills that cite this paper ----
  const skills = (payload.skills || []).filter(s => s.collection === label &&
    (s.source_dois || []).some(d => String(d).toLowerCase() === key));
  const { version: v } = parseLabel(label);
  const browse = name => `./collections.html?c=${encodeURIComponent(slug)}&v=${encodeURIComponent(v)}` +
    `&tab=skills&q=${encodeURIComponent(name)}`;
  const fullText = entry && entry.doi
    ? siteEl("p", { class: "hint" }, "The full text of each skill is in the Zenodo record of the release (",
        siteEl("a", { href: doiURL(entry.doi), target: "_blank", rel: "noopener" }, entry.doi),
        `) and in the private domain repository ${domainRepoName(slug)} for people with access.`)
    : siteEl("p", { class: "hint" },
        `The full text of each skill is in the private domain repository ${domainRepoName(slug)} for people with access` +
        (status[label] === "staged" ? "; this staged tree is not part of a release." : "."));
  if (skills.length) {
    const ul = siteEl("ul", { class: "skill-list" });
    for (const s of skills) {
      ul.appendChild(siteEl("li", {},
        // Only released collections are browsable; a staged skill name stays plain text.
        status[label] === "released"
          ? siteEl("a", { href: browse(s.name) }, siteEl("code", {}, s.name))
          : siteEl("code", {}, s.name),
        s.description ? siteEl("div", { class: "hint" }, s.description.trim()) : null));
    }
    setBody("skills-list",
      siteEl("p", { class: "hint" }, `${skills.length} skill(s) of ${label} cite this paper as a source.`),
      ul, fullText);
  } else {
    setBody("skills-list", siteEl("p", { class: "empty" }, `No skill of ${label} cites this paper as a source.`), fullText);
  }

  // ---- tools ----
  const tools = (payload.tools || []).filter(t => t.collection === label && String(t.source_doi || "").toLowerCase() === key);
  if (tools.length) {
    const ul = siteEl("ul", {});
    for (const t of tools) ul.appendChild(siteEl("li", {}, siteEl("code", {}, t.slug), " ", t.name || ""));
    setBody("tools-list", siteEl("p", { class: "hint" }, `${tools.length} tool(s) name this paper as their source.`), ul);
  } else if (status[label] === "released") {
    setBody("tools-list", siteEl("p", { class: "empty" },
      "The public index does not link tools to this paper. Browse the tools of the collection on ",
      siteEl("a", { href: `./collections.html?c=${encodeURIComponent(slug)}&v=${encodeURIComponent(v)}&tab=tools` }, "the Browse page"),
      "."));
  } else {
    setBody("tools-list", siteEl("p", { class: "empty" }, "The public index does not link tools to this paper."));
  }

  // ---- actions: issues on the public repository, with the labels of its templates ----
  const skillList = skills.map(s => `- ${s.name}`).join("\n") || "- none in the public index";
  document.getElementById("btn-review").addEventListener("click", () => {
    const body = [
      "## Paper information", "",
      `**Paper DOI:** ${doi}`, "",
      `**Paper title:** ${paper.title || ""}`, "",
      `**Link to paper (optional):** ${doiURL(doi)}`, "",
      `**Collection:** ${label}`, "",
      "## Skills derived from this paper", "", skillList, "",
      "## What should a reviewer check?", "", "<fill in>",
    ].join("\n");
    window.open(makeIssueURL({
      template: "request-paper-review.md",
      title: `[REVIEW-REQUEST] ${paper.title || doi}`,
      body,
      labels: ["review-requested", "needs-triage"],
    }), "_blank", "noopener");
  });
  document.getElementById("btn-flag").addEventListener("click", () => {
    const body = [
      "**Route:** this skill is wrong or could be better", "",
      "**Kind:** `defect` (an existing skill is wrong, stale, or does not work as written)", "",
      `## Content derived from paper ${doi}`, "",
      `Collection: ${label}`, "",
      "**What is wrong:** <fill in>", "",
      "**Affected skills:** <list the ones concerned>", "", skillList, "",
      "**Suggested fix:** <if known>",
    ].join("\n");
    // Route 1 in the vocabulary of scripts/skill_feedback.py: kind `defect`.
    window.open(makeIssueURL({
      template: "1-skill-feedback.md",
      title: `defect: content derived from ${doi}`,
      body,
      labels: ["usage-feedback", "needs-triage", "auto-report"],
    }), "_blank", "noopener");
  });
  document.getElementById("actions").hidden = false;
})();
