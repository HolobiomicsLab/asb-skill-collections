/* paper.js — per-paper review page: skill + tool + workflow derivations */

const RAW_BASE = "https://raw.githubusercontent.com/HolobiomicsLab/asb-skill-collections/main";
const REPO = "HolobiomicsLab/asb-skill-collections";

function getParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

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

async function fetchText(url) {
  const r = await fetch(url, { cache: "no-store" });
  if (!r.ok) throw new Error(`${r.status}`);
  return r.text();
}

async function fetchJSON(url) {
  const r = await fetch(url, { cache: "no-store" });
  if (!r.ok) throw new Error(`${r.status}`);
  return r.json();
}

async function getCollectionWorkflowIndex(collection, version) {
  const paths = [
    `${RAW_BASE}/staged-collections/${collection}/v${version}/_workflow_index.json`,
    `${RAW_BASE}/collections/${collection}/v${version}/_workflow_index.json`,
  ];
  for (const p of paths) {
    try { return { idx: await fetchJSON(p), base: p.replace(/\/_workflow_index\.json$/, "") }; }
    catch { /* try next */ }
  }
  return null;
}

async function fetchPaperMeta(doi) {
  try {
    const r = await fetch(`https://api.crossref.org/works/${doi}`,
      { headers: { "Accept": "application/json" } });
    if (r.ok) {
      const data = (await r.json()).message || {};
      return {
        title: (data.title || [""])[0],
        authors: (data.author || []).slice(0, 5).map(a =>
          `${a.given || ""} ${a.family || ""}`.trim()).join(", "),
        venue: (data["container-title"] || [""])[0],
        year: data.issued?.["date-parts"]?.[0]?.[0],
      };
    }
  } catch { /* CORS or 404 */ }
  return null;
}

function parsefrontmatter(text) {
  // Read the first --- ... --- block as YAML (simple line-based).
  const m = text.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!m) return { fm: {}, body: text };
  const fmText = m[1];
  // Minimal parse: top-level scalar key: value pairs + first-level lists ("- ...").
  // For metadata.{iri, related_workflows, claims}, deeper indented blocks
  // are aggregated as raw text.
  const fm = {};
  let lines = fmText.split("\n");
  let key = null;
  let buf = [];
  function flushKey() {
    if (key) fm[key] = buf.join("\n").trim();
    key = null; buf = [];
  }
  for (const line of lines) {
    const flat = line.match(/^([a-zA-Z_][\w-]*):\s*(.*)$/);
    if (flat) {
      flushKey();
      if (flat[2] && !flat[2].startsWith("|") && !flat[2].startsWith(">")) {
        fm[flat[1]] = flat[2].trim().replace(/^['"]|['"]$/g, "");
      } else {
        key = flat[1];
        buf = [];
      }
    } else if (key) {
      buf.push(line.replace(/^  /, ""));
    }
  }
  flushKey();
  return { fm, body: m[2] };
}

function makeIssueURL({ title, body, labels = [] }) {
  const params = new URLSearchParams();
  params.set("title", title);
  params.set("body", body);
  if (labels.length) params.set("labels", labels.join(","));
  return `https://github.com/${REPO}/issues/new?${params.toString()}`;
}

function makeAttestationPRBody({ doi, slugs, collection, version }) {
  // Body links the reviewer to copy-paste a candidate attestation YAML.
  // The actual PR is opened via the GH new-file URL below.
  const lines = [];
  lines.push(`# Review attestation for paper ${doi}`);
  lines.push(``);
  lines.push(`Auto-prefilled by the static review UI. Please review carefully before submitting.`);
  lines.push(``);
  lines.push("```yaml");
  lines.push(`# Save as collections/${collection}/v${version}/reviews/${(doi || "").replace(/[/:]/g, "_")}.yaml`);
  lines.push(`paper_doi: ${doi}`);
  lines.push(`collection: ${collection}/v${version}`);
  lines.push(`reviewer:`);
  lines.push(`  orcid: 0000-0000-0000-0000   # <-- replace with your ORCID`);
  lines.push(`  github: ${"<your-github-handle>"}`);
  lines.push(`  is_coauthor: false           # <-- set true if you are an author of this paper`);
  lines.push(`reviewed_at: ${new Date().toISOString().slice(0, 10)}`);
  lines.push(`verdict: accepted              # accepted | corrected | rejected`);
  lines.push(`credit_roles: [Validation, Data-Curation]`);
  lines.push(`verified_skills:`);
  for (const s of slugs) lines.push(`  - ${s}`);
  lines.push(`verified_claim_ids: []         # gold-tier subset, populate if you verified claims against paper text`);
  lines.push(`notes: |`);
  lines.push(`  <free-text — describe what you checked and any corrections made>`);
  lines.push("```");
  return lines.join("\n");
}

function parseJSONL(text) {
  const out = [];
  for (const line of text.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    try { out.push(JSON.parse(trimmed)); } catch { /* skip malformed */ }
  }
  return out;
}

async function fetchClaimsForTier(paperIds, tier) {
  // tier: "silver" -> ground_truth.jsonl
  //       "gold"   -> gold/ground_truth.jsonl
  const suffix = tier === "gold" ? "gold/ground_truth.jsonl" : "ground_truth.jsonl";
  for (const id of paperIds) {
    const url = `${RAW_BASE}/benchmark/claims/per_paper/${id}/${suffix}`;
    try {
      const txt = await fetchText(url);
      return parseJSONL(txt).map(c => ({ ...c, _tier: tier, _paperId: id }));
    } catch { /* try next id */ }
  }
  return [];
}

function truncate(s, n) {
  if (!s) return "";
  s = String(s);
  return s.length > n ? s.slice(0, n - 1) + "…" : s;
}

async function renderClaims({ doi, doiSafe, collection, version, myWorkflow }) {
  const listDiv = document.getElementById("claims-list");
  const filterDiv = document.getElementById("claims-filter");
  const countEl = document.getElementById("claims-count");
  if (!listDiv) return;

  // Build candidate paper-ids the per_paper directory may use.
  const candidates = new Set();
  candidates.add(doiSafe);
  candidates.add(doi);
  candidates.add(doi.toLowerCase());
  candidates.add(doi.replace(/[^a-zA-Z0-9]/g, "_"));
  // If workflow path encodes the paper-id as the first segment, try that.
  if (myWorkflow) {
    const parts = myWorkflow.split("/").filter(Boolean);
    for (const p of parts) {
      if (p && !p.endsWith(".yaml") && !p.endsWith(".json") && p !== "workflows" && p !== "runs") {
        candidates.add(p);
      }
    }
  }
  const ids = [...candidates];

  const [silver, gold] = await Promise.all([
    fetchClaimsForTier(ids, "silver"),
    fetchClaimsForTier(ids, "gold"),
  ]);

  // Merge: gold claims may also appear in silver under same claim_id;
  // prefer the gold record when there is a collision.
  const byId = new Map();
  for (const c of silver) {
    const cid = c.claim_id || c.id || JSON.stringify(c).slice(0, 32);
    byId.set(cid, { ...c, claim_id: cid });
  }
  for (const c of gold) {
    const cid = c.claim_id || c.id || JSON.stringify(c).slice(0, 32);
    byId.set(cid, { ...c, claim_id: cid, _tier: "gold" });
  }
  const allClaims = [...byId.values()];

  if (!allClaims.length) {
    listDiv.innerHTML = "";
    listDiv.appendChild(el("p", { class: "empty" },
      "No claim ledger emitted for this paper yet."));
    return;
  }

  filterDiv.hidden = false;

  let currentTier = "all";

  function renderTable() {
    listDiv.innerHTML = "";
    const filtered = currentTier === "all"
      ? allClaims
      : allClaims.filter(c => c._tier === currentTier);

    countEl.textContent = `${filtered.length} of ${allClaims.length} claim(s)`;

    if (!filtered.length) {
      listDiv.appendChild(el("p", { class: "empty" },
        `No ${currentTier}-tier claims for this paper.`));
      return;
    }

    const table = el("table", { class: "claims-table" });
    const thead = el("thead", {}, el("tr", {},
      el("th", {}, "claim_id"),
      el("th", {}, "tier"),
      el("th", {}, "text"),
      el("th", {}, "section"),
      el("th", {}, ""),
    ));
    table.appendChild(thead);
    const tbody = el("tbody", {});
    for (const c of filtered) {
      const tierBadge = el("span",
        { class: c._tier === "gold" ? "badge badge-gold" : "badge badge-silver" },
        c._tier);
      const verifyBtn = el("button", {
        type: "button",
        class: "btn-verify-claim",
        onclick: () => openClaimAttestation({ doi, collection, version, claim: c }),
      }, "Verify ✓");
      tbody.appendChild(el("tr", {},
        el("td", {}, el("code", {}, truncate(c.claim_id, 40))),
        el("td", {}, tierBadge),
        el("td", {}, truncate(c.text || c.claim || c.statement || "", 200)),
        el("td", {}, truncate(c.section || c.location || "", 40)),
        el("td", {}, verifyBtn),
      ));
    }
    table.appendChild(tbody);
    listDiv.appendChild(table);
  }

  for (const btn of filterDiv.querySelectorAll(".tier-btn")) {
    btn.addEventListener("click", () => {
      currentTier = btn.dataset.tier;
      for (const b of filterDiv.querySelectorAll(".tier-btn")) {
        b.classList.toggle("is-active", b === btn);
      }
      renderTable();
    });
  }

  renderTable();
}

function openClaimAttestation({ doi, collection, version, claim }) {
  const cid = claim.claim_id || claim.id || "<claim-id>";
  const lines = [];
  lines.push(`# Claim verification for paper ${doi}`);
  lines.push(``);
  lines.push(`Reviewing a single claim from the ${claim._tier}-tier ledger.`);
  lines.push(``);
  lines.push("```yaml");
  lines.push(`# Save as collections/${collection}/v${version}/reviews/${(doi || "").replace(/[/:]/g, "_")}.yaml`);
  lines.push(`paper_doi: ${doi}`);
  lines.push(`collection: ${collection}/v${version}`);
  lines.push(`reviewer:`);
  lines.push(`  orcid: 0000-0000-0000-0000   # <-- replace with your ORCID`);
  lines.push(`  github: <your-github-handle>`);
  lines.push(`  is_coauthor: false`);
  lines.push(`reviewed_at: ${new Date().toISOString().slice(0, 10)}`);
  lines.push(`verdict: accepted`);
  lines.push(`verified_claim_ids:`);
  lines.push(`  - ${cid}`);
  lines.push(`tier_reviewed: ${claim._tier}`);
  lines.push(`notes: |`);
  lines.push(`  Claim text (truncated): ${truncate(claim.text || claim.claim || claim.statement || "", 240)}`);
  lines.push("```");
  const url = makeIssueURL({
    title: `[review:claim] ${cid} from ${doi}`,
    body: lines.join("\n"),
    labels: ["review-attestation", "claim-verification", `tier:${claim._tier}`],
  });
  window.open(url, "_blank");
}

(async function init() {
  const doi = getParam("doi");
  const collection = getParam("collection") || "metabolomics";
  const version = getParam("version") || "1";

  if (!doi) {
    document.getElementById("meta-card").innerHTML =
      `<p class="error">No DOI specified. Use ?doi=10.../...&collection=...&version=...</p>`;
    return;
  }

  // 1. Crossref metadata
  document.getElementById("paper-title").textContent = `Paper: ${doi}`;
  const meta = await fetchPaperMeta(doi);
  const metaCard = document.getElementById("meta-card");
  metaCard.innerHTML = "";
  if (meta) {
    document.getElementById("paper-title").textContent = meta.title || doi;
    document.getElementById("paper-meta").textContent =
      `${meta.authors || "?"} — ${meta.venue || "?"} (${meta.year || "?"})`;
    metaCard.appendChild(el("p", {},
      el("a", { href: `https://doi.org/${doi}`, target: "_blank" }, doi),
      " · ",
      el("a", { href: `https://api.crossref.org/works/${doi}`, target: "_blank" }, "Crossref metadata")
    ));
  } else {
    metaCard.appendChild(el("p", { class: "hint" }, `DOI: ${doi} (Crossref metadata fetch blocked or unavailable in this browser)`));
  }

  // 2. Workflow index → which skills + tools came from this paper
  const result = await getCollectionWorkflowIndex(collection, version);
  if (!result) {
    document.getElementById("skills-list").innerHTML =
      `<p class="error">No _workflow_index.json found for ${collection}/v${version}.</p>`;
    return;
  }
  const { idx, base } = result;

  // Match paper-id directories: corpus.yaml DOI may map to a task-dir
  // whose name is the run basename. Try both forms.
  const doiSafe = doi.replace(/[/:]/g, "_");
  const candidateIds = new Set([doi, doiSafe, doi.toLowerCase()]);
  let myWorkflow = null;
  for (const id of Object.keys(idx.by_paper || {})) {
    if (candidateIds.has(id)) {
      myWorkflow = idx.by_paper[id];
      break;
    }
  }

  // Skills: by_skill values list workflow paths; reverse-find.
  const mySkills = [];
  for (const [slug, wfs] of Object.entries(idx.by_skill || {})) {
    if (myWorkflow && wfs.includes(myWorkflow)) mySkills.push(slug);
  }
  if (!mySkills.length) {
    // Fallback: walk all skills' SKILL.md and check provenance.source_papers
    // (slow but accurate). Limit to first 30 to keep page responsive.
    const samples = Object.keys(idx.by_skill || {}).slice(0, 50);
    for (const slug of samples) {
      try {
        const txt = await fetchText(`${base}/skills/${slug}/SKILL.md`);
        if (txt.toLowerCase().includes(doi.toLowerCase())) mySkills.push(slug);
      } catch { /* skip */ }
    }
  }

  // Tools
  const myTools = [];
  for (const [slug, wfs] of Object.entries(idx.by_tool || {})) {
    if (myWorkflow && wfs.includes(myWorkflow)) myTools.push(slug);
  }

  // Render skills
  const skillsDiv = document.getElementById("skills-list");
  skillsDiv.innerHTML = "";
  if (mySkills.length) {
    skillsDiv.appendChild(el("p", { class: "hint" },
      `${mySkills.length} skill(s) reference this paper. (Some may also have other source papers.)`));
    const ul = el("ul", { class: "skill-list" });
    for (const slug of mySkills) {
      ul.appendChild(el("li", {},
        el("code", {}, slug), " ",
        el("a", { href: `${base.replace(RAW_BASE, "https://github.com/" + REPO + "/blob/main")}/skills/${slug}/SKILL.md`, target: "_blank" }, "view SKILL.md"),
      ));
    }
    skillsDiv.appendChild(ul);
  } else {
    skillsDiv.appendChild(el("p", { class: "empty" }, "No derived skills found for this DOI."));
  }

  // Render tools
  const toolsDiv = document.getElementById("tools-list");
  toolsDiv.innerHTML = "";
  if (myTools.length) {
    toolsDiv.appendChild(el("p", { class: "hint" }, `${myTools.length} tool(s) reference this paper.`));
    const ul = el("ul", {});
    for (const slug of myTools.slice(0, 50)) {
      ul.appendChild(el("li", {},
        el("code", {}, slug), " ",
        el("a", { href: `${base.replace(RAW_BASE, "https://github.com/" + REPO + "/blob/main")}/tools/${slug}.yaml`, target: "_blank" }, "view tool record"),
      ));
    }
    toolsDiv.appendChild(ul);
  } else {
    toolsDiv.appendChild(el("p", { class: "empty" }, "No derived tools tagged to this DOI."));
  }

  // Workflow
  const wfDiv = document.getElementById("workflow-detail");
  wfDiv.innerHTML = "";
  if (myWorkflow) {
    const githubURL = myWorkflow.replace(/^/, `https://github.com/${REPO}/blob/main/staged-collections/${collection}/v${version}/`).replace(`staged-collections/${collection}/v${version}/staged-collections/${collection}/v${version}/`, `staged-collections/${collection}/v${version}/`);
    wfDiv.appendChild(el("p", {}, "Reference workflow: ",
      el("a", { href: `${RAW_BASE}/staged-collections/${collection}/v${version}/${myWorkflow}`, target: "_blank" }, myWorkflow)));
  } else {
    wfDiv.appendChild(el("p", { class: "empty" }, "No workflow available for this paper (yet)."));
  }

  // Wire action buttons
  document.getElementById("btn-verify-all").addEventListener("click", () => {
    const body = makeAttestationPRBody({ doi, slugs: mySkills, collection, version });
    const url = makeIssueURL({
      title: `[review] ${doi} (collection: ${collection}/v${version})`,
      body,
      labels: ["review-attestation", "needs-merge"],
    });
    window.open(url, "_blank");
  });
  // -------------------------------------------------------------------
  // Claims ledger (Enhancement 2): silver + gold tier rendering w/ filter
  // -------------------------------------------------------------------
  await renderClaims({ doi, doiSafe, collection, version, myWorkflow });

  document.getElementById("btn-flag").addEventListener("click", () => {
    const body = `## Issue with derived content from paper ${doi}\n\n` +
      `Collection: ${collection}/v${version}\n\n` +
      `**What's wrong:** <fill in>\n\n` +
      `**Affected skills/tools:** <list any specific ones>\n\n` +
      `**Suggested fix:** <if known>\n`;
    const url = makeIssueURL({
      title: `[flag] Issue with content derived from ${doi}`,
      body,
      labels: ["needs-review", "derived-content"],
    });
    window.open(url, "_blank");
  });
})();
