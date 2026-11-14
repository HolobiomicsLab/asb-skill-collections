---
name: "1. A skill is wrong or could be better"
about: A skill was wrong, stale, wasteful or improvable in practice. Reports from real use are how the collection hardens.
title: "<kind>: <skill slug>: <what happened>"
labels: ["usage-feedback", "needs-triage"]
---

<!--
Route 1 of 4: this skill is wrong or could be better.
A missing skill is route 2 (request-skill), a paper that is not referenced is
route 3 (propose-paper), a technical fault of install, plugin, search, CLI, site
or gates is route 4 (technical-fault).

The router of each collection, `bin/report_issue.py` where a collection ships it,
`asbb report` and `scripts/skill_feedback.py` fill this in for you, redact paths
and credentials, and show you the result before anything is posted. Filling it
in by hand is fine too.

Before opening: search for the fingerprint below, or for the skill slug. If an
issue already describes this, comment there instead. Ten corroborations on one
issue are worth more to a maintainer, and to you, than ten separate issues.
-->

**Route:** this skill is wrong or could be better

**Kind:** <!-- defect | drift | enhancement | efficiency -->

- `defect`: an existing skill is wrong, stale, or does not work as written
- `drift`: the underlying tool changed and the skill no longer matches it
- `enhancement`: the skill works but could be better: a missing step, a better default, a clearer text
- `efficiency`: the skill works but costs far more than it needs to

**Target:** <!-- the skill slug, as the search printed it -->

**Collection:** <!-- e.g. metabolomics/v3 -->  ·  **Release:** <!-- e.g. metabolomics-v3.0.2 -->

**Fingerprint:** <!-- from the helper; lets other reporters find this issue -->

### What happened

<!-- What you ran, what the skill told you to do, and what actually occurred. -->

### What the skill led me to expect

<!-- Optional. Quote the line that misled you, if there was one. -->

### Context

<!-- Tool and version, OS, anything that makes it reproducible. No sample data,
no absolute paths, no credentials. See the note below. -->

---

**Before you post, check this issue contains nothing you would not publish.**
Automated redaction removes home directories, tokens and clinical identifiers,
but it cannot recognise every sensitive sample name. You are the last check.

<!--
Why bother: this collection is grounded in the published literature and given
away under CC-BY. It gets better only when people who use it say what broke.
A maintainer triages the report here and carries the fix into the domain
repository; the revised skill ships in a later release. If you can
write the fix yourself, propose it (propose-skill.md); governance/AUTHORSHIP.md
records authored skills as credit toward the reviewer tier.
-->
