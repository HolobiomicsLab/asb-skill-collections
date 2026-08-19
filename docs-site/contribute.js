// contribute.js — client-side anonymized improvement report -> pre-filled GitHub issue.
// Mirrors scripts/make_improvement_report.py so humans (web) and agents (CLI) produce
// the same scrubbed, well-formed contribution. Nothing leaves the browser until you
// click submit (which opens GitHub's new-issue page with the body pre-filled).
const REPO = "HolobiomicsLab/asb-skill-collections";
const DRAFT_KEY = "asb-contribute-draft";

// Redaction rules — kept in lock-step with scripts/make_improvement_report.py.
// Bounded quantifiers (no ReDoS on long pasted blobs); non-alnum lookbehind (not
// \b) so ANTHROPIC_API_KEY / GITHUB_TOKEN etc. still match.
const SCRUBBERS = [
  ["email", /[\w.+-]{1,64}@[\w-]{1,255}(?:\.[\w-]{1,255})+/g, "[email]"],
  ["ip", /\b\d{1,3}(?:\.\d{1,3}){3}\b/g, "[ip]"],
  ["path", /(?:\/Users\/|\/home\/|\/private\/|~\/)[^\s"'`]+/g, "[path]"],
  ["path", /\b[A-Za-z]:\\[^\s"'`]+/g, "[path]"],
  ["path", /(?<![\w.])\/(?:usr|var|tmp|opt|etc|mnt|srv)\/[^\s"'`]+/g, "[path]"],
  ["secret", /\b(?:sk|pk)-[A-Za-z0-9_-]{16,}/g, "[secret]"],
  ["secret", /\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{16,}\b/g, "[secret]"],
  ["secret", /\bglpat-[A-Za-z0-9_-]{16,}/g, "[secret]"],
  ["secret", /\bAKIA[0-9A-Z]{12,}\b/g, "[secret]"],
  ["secret", /\bBearer\s+[A-Za-z0-9._-]{12,}/gi, "Bearer [secret]"],
  ["secret", /(?<![A-Za-z0-9])(api[_-]?key|access[_-]?key|secret[_-]?key|token|secret|password|passwd|pwd|key)\s*[:=]\s*\S+/gi, "$1=[secret]"],
];

function scrub(text) {
  let out = text || "";
  const counts = {};
  for (const [label, pat, repl] of SCRUBBERS) {
    out = out.replace(pat, (...m) => {
      counts[label] = (counts[label] || 0) + 1;
      return typeof repl === "string" ? repl.replace("$1", m[1] ?? "") : repl;
    });
  }
  return { out, counts };
}

const $ = id => document.getElementById(id);

function gather() {
  return {
    collection: $("collection").value.trim(),
    target: $("target").value,
    item: $("item").value.trim(),
    kind: $("kind").value,
    summary: $("summary").value,
    detail: $("detail").value,
    diff: $("diff").value,
    runtime: $("runtime").value.trim(),
    handle: $("handle").value.trim(),
  };
}

function buildBody(f) {
  const redacted = {};
  const clean = (t) => {
    const { out, counts } = scrub(t);
    for (const k in counts) redacted[k] = (redacted[k] || 0) + counts[k];
    return out;
  };
  const label = f.target === "workflows" ? "workflow" : f.target === "tools" ? "tool" : "skill";
  const lines = [
    `## Improvement report — \`${f.item || "?"}\``,
    "",
    `- **collection:** \`${f.collection || "?"}\``,
    `- **${label}:** \`${f.item || "?"}\``,
    `- **kind:** ${f.kind}`,
  ];
  if (f.runtime) lines.push(`- **agent runtime:** ${clean(f.runtime)}`);
  if (f.handle) lines.push(`- **contributor:** @${f.handle.replace(/^@/, "")}`);
  lines.push("", "### Summary", clean(f.summary) || "_(none)_", "", "### Detail", clean(f.detail) || "_(none)_");
  const d = clean(f.diff);
  if (d.trim()) lines.push("", "### Proposed change", "```diff", d, "```");
  const note = Object.keys(redacted).length
    ? "Redacted: " + Object.entries(redacted).sort().map(([k, v]) => `${k}×${v}`).join(", ") + "."
    : "No PII/secrets/paths detected.";
  lines.push("", "---", `_Auto-generated, anonymized improvement report. ${note} Submitted via the ASB contribute form._`);
  return { body: lines.join("\n"), redacted };
}

function refresh() {
  const f = gather();
  const { body, redacted } = buildBody(f);
  $("preview").textContent = body;
  const n = Object.entries(redacted).sort().map(([k, v]) => `${k}×${v}`).join(", ");
  $("redaction").textContent = n
    ? `Scrubbed before submission: ${n}.`
    : "No file paths, emails, IPs, or secrets detected in your text.";
  localStorage.setItem(DRAFT_KEY, JSON.stringify(f));
  return { f, body };
}

function issueURL(f, body) {
  const params = new URLSearchParams({
    title: `[improvement] ${f.item || "?"}: ${f.kind}`,
    body,
    labels: "improvement,needs-triage,auto-report",
  });
  return `https://github.com/${REPO}/issues/new?${params.toString()}`;
}

function init() {
  // restore draft
  try {
    const d = JSON.parse(localStorage.getItem(DRAFT_KEY) || "{}");
    for (const k of Object.keys(d)) if ($(k)) $(k).value = d[k];
  } catch (e) { /* ignore */ }

  // prefill from query params (from a "Suggest improvement" link)
  const p = new URLSearchParams(location.search);
  for (const k of ["collection", "target", "item", "kind"]) {
    if (p.get(k)) $(k).value = p.get(k);
  }

  document.querySelectorAll("#form input, #form textarea, #form select")
    .forEach(elm => elm.addEventListener("input", refresh));

  $("form").addEventListener("submit", (e) => {
    e.preventDefault();
    const { f, body } = refresh();
    const url = issueURL(f, body);
    if (url.length > 8000) {
      alert("This report is long; GitHub may truncate the URL. Trim the detail/diff, or paste it into the issue after it opens.");
    }
    window.open(url, "_blank", "noopener");
  });

  refresh();
}

document.addEventListener("DOMContentLoaded", init);
