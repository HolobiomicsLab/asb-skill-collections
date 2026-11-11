// propose.js: the paper proposal form (route 3) as a pre-filled issue on the
// public registry. The body carries the bold fields that scripts/intake_issue.py
// reads ("What is it?", "Link:", "Type:", "Target collection:", "Why it
// matters"), in the same lines as paper_body() of scripts/skill_feedback.py;
// tests/test_contribution_routes.py runs this file under node and feeds its
// body through the parser.
const PROPOSE_REPO = "HolobiomicsLab/asb-skill-collections";
const PROPOSE_TEMPLATE = "3-propose-paper.md";
const PROPOSE_LABELS = ["propose", "paper-intake", "needs-triage", "auto-report"];

function oneLine(value) {
  return String(value || "").split(/\s+/).filter(Boolean).join(" ");
}

/** The issue body, in the order and words of paper_body() in skill_feedback.py. */
function buildProposalBody(f) {
  const lines = [
    `**What is it?** ${oneLine(f.what)}`, "",
    `**Link:** ${oneLine(f.link)}`, "",
    `**Type:** ${oneLine(f.type)}`, "",
    `**Target collection:** ${oneLine(f.collection)}`, "",
    "**Why it matters (one or two sentences):**",
    String(f.why || "").trim(),
  ];
  for (const [label, key] of [["Target version:", "version"], ["Open access?", "open_access"],
    ["You:", "you"], ["Conflict of interest?", "coi"]]) {
    const value = oneLine(f[key]);
    if (value) lines.push("", `**${label}** ${value}`);
  }
  return lines.join("\n").replace(/\s+$/, "") + "\n";
}

const ACCESS_WORDS = {
  "dont-know": "not sure",
  "open-access": "yes",
  "hybrid": "hybrid (paywalled with quotation rights)",
  "closed": "no",
};

/** Read the form's FormData into the fields of buildProposalBody. */
function proposalFields(form) {
  const get = name => (form.get(name) || "").toString();
  const cois = [];
  if (form.get("coi_author")) cois.push("author of this paper");
  if (form.get("coi_inst")) cois.push("same institution as the lead author");
  if (form.get("coi_fund")) cois.push("direct funding ties");
  const you = [get("gh") ? "@" + get("gh").replace(/^@/, "") : "", get("orcid") ? `ORCID ${get("orcid")}` : ""]
    .filter(Boolean).join(", ");
  return {
    what: get("title"),
    link: get("doi"),
    type: get("type") || "paper",
    collection: get("collection"),
    why: get("rationale"),
    version: get("version"),
    open_access: ACCESS_WORDS[get("access")] || "",
    you,
    coi: cois.length ? cois.join("; ") : "none disclosed",
  };
}

function proposalIssueURL(fields) {
  const params = new URLSearchParams({
    template: PROPOSE_TEMPLATE,
    title: `Propose: ${oneLine(fields.what || fields.link)}`,
    labels: PROPOSE_LABELS.join(","),
    body: buildProposalBody(fields),
  });
  return `https://github.com/${PROPOSE_REPO}/issues/new?${params.toString()}`;
}

if (typeof module !== "undefined") {
  module.exports = { buildProposalBody, proposalFields, proposalIssueURL, PROPOSE_LABELS, PROPOSE_TEMPLATE };
}
