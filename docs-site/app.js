// app.js — fetch catalogue.jsonld + career.jsonld from GitHub raw and render tables.
// Paths are relative to the repo root on the main branch.
const REPO = "HolobiomicsLab/asb-skill-collections";
const BRANCH = "main";
const RAW = `https://raw.githubusercontent.com/${REPO}/${BRANCH}`;

async function fetchJSON(path) {
  const url = `${RAW}/${path}`;
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`HTTP ${resp.status} for ${url}`);
  return resp.json();
}

function el(tag, attrs = {}, ...children) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
  for (const c of children) {
    if (typeof c === "string") e.appendChild(document.createTextNode(c));
    else if (c) e.appendChild(c);
  }
  return e;
}

function makeTable(headers, rows) {
  const thead = el("thead", {}, el("tr", {}, ...headers.map(h => el("th", {}, h))));
  const tbody = el("tbody", {}, ...rows.map(r =>
    el("tr", {}, ...r.map(c => el("td", {}, ...(Array.isArray(c) ? c : [c]))))
  ));
  return el("table", {}, thead, tbody);
}

async function renderCatalogue() {
  const section = document.getElementById("catalogue");
  try {
    const data = await fetchJSON("catalogue.jsonld");
    const cols = data.collections || [];
    if (cols.length === 0) {
      section.innerHTML += "<p class='loading'>No collections released yet.</p>";
      return;
    }
    const rows = cols.map(c => {
      const doiLink = c.doi
        ? [el("a", { href: `https://doi.org/${c.doi}`, target: "_blank" }, c.doi)]
        : ["—"];
      const topics = (c.domain_topics || []).map(t => {
        const label = t.split("/").pop();
        return el("span", { class: "badge" }, label);
      });
      return [
        [el("a", { href: c["@id"] || "#", target: "_blank" }, c.title || c.slug)],
        c.version || "—",
        String(c.skills_count || 0),
        String(c.tools_count || 0),
        topics.length ? topics : ["—"],
        doiLink,
        c.released_at ? [c.released_at.substring(0, 10)] : ["pending"],
      ];
    });
    section.appendChild(makeTable(
      ["Collection", "Version", "Skills", "Tools", "EDAM Topics", "DOI", "Released"],
      rows
    ));
    section.querySelector(".loading")?.remove();
  } catch (err) {
    section.querySelector(".loading").className = "error";
    section.querySelector(".error").textContent = `Failed to load catalogue: ${err.message}`;
  }
}

async function renderLeaderboard() {
  const section = document.getElementById("leaderboard");
  try {
    const data = await fetchJSON("leaderboard/career.jsonld");
    const contribs = data.contributors || [];
    if (contribs.length === 0) {
      section.innerHTML += "<p class='loading'>No contributors yet.</p>";
      return;
    }
    const rows = contribs.map(c => {
      const tierBadge = el("span", { class: "badge" }, c.tier || "reviewer");
      const collections = [
        ...(c.lead_curator_of || []),
        ...(c.curator_of || []),
        ...(c.domain_contributor_of || []),
        ...(c.reviewer_of || []),
      ];
      const colBadges = collections.length
        ? collections.map(col => el("span", { class: "badge" }, col))
        : ["—"];
      const pct = typeof c.self_authored_percentage === "number"
        ? `${c.self_authored_percentage.toFixed(1)}%`
        : "—";
      const orcidLink = c.orcid
        ? [el("a", { href: `https://orcid.org/${c.orcid}`, target: "_blank" }, c.orcid)]
        : ["—"];
      return [
        c.rank != null ? String(c.rank) : "—",
        c.name || c.github || "—",
        orcidLink,
        [tierBadge],
        String(c.total_reviews || 0),
        pct,
        colBadges,
      ];
    });
    section.appendChild(makeTable(
      ["#", "Name", "ORCID", "Tier", "Reviews", "Self-authored %", "Collections"],
      rows
    ));
    section.querySelector(".loading")?.remove();
  } catch (err) {
    section.querySelector(".loading").className = "error";
    section.querySelector(".error").textContent = `Failed to load leaderboard: ${err.message}`;
  }
}

async function renderBanner() {
  const box = document.getElementById("release-banner");
  if (!box) return;
  try {
    const data = await fetchJSON("catalogue.jsonld");
    const cols = (data.collections || []).filter(c => c.released_at);
    if (!cols.length) return;
    const newest = cols.reduce((a, b) => (a.released_at > b.released_at ? a : b));
    const id = `${newest.slug}-v${newest.version}-${(newest.released_at || "").substring(0, 10)}`;
    if (localStorage.getItem(`asb-banner-${id}`)) return;
    const date = (newest.released_at || "").substring(0, 10);
    box.className = "banner";
    box.appendChild(el("span", {},
      `🆕 Newest release: ${newest.title || newest.slug} (v${newest.version}) — `,
      el("strong", {}, `${newest.skills_count || 0} skills`), ", ",
      `${newest.tools_count || 0} tools, released ${date}. `,
      el("a", { href: `./collections.html?c=${newest.slug}` }, "Browse →")
    ));
    const close = el("button", { class: "banner-x", title: "Dismiss" }, "✕");
    close.addEventListener("click", () => { localStorage.setItem(`asb-banner-${id}`, "1"); box.remove(); });
    box.appendChild(close);
  } catch (e) { /* banner is best-effort */ }
}

document.addEventListener("DOMContentLoaded", () => {
  renderBanner();
  renderCatalogue();
  renderLeaderboard();
});
