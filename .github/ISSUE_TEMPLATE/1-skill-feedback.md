---
name: Report friction using a skill
about: A skill was wrong, stale, missing, or wasteful in practice. Reports from real use are how the collection hardens.
title: "<kind>: <skill or capability> — <what happened>"
labels: ["usage-feedback", "needs-triage"]
---

<!--
The `asb-contribute` skill fills this in for you from the session where the
problem happened, redacts paths and credentials, and shows you the result before
anything is posted. Filling it in by hand is fine too.

Before opening: search for the fingerprint below, or for the skill slug. If an
issue already describes this, comment there instead — ten corroborations on one
issue are worth more to a maintainer, and to you, than ten separate issues.
-->

**Kind:** <!-- defect | gap | composition | efficiency | drift -->

- `defect` — an existing skill is wrong, stale, or does not work as written
- `gap` — no skill covers the task; a new one is warranted
- `composition` — the leaves exist but nothing composes them; a workflow is warranted
- `efficiency` — the skill works but costs far more than it needs to
- `drift` — the underlying tool changed and the skill no longer matches it

**Target:** <!-- the skill slug, or a short name for the capability that is missing -->

**Fingerprint:** <!-- from `asb-contribute`; lets other reporters find this issue -->

### What happened

<!-- What you ran, what the skill told you to do, and what actually occurred. -->

### What the skill led you to expect

<!-- Optional. Quote the line that misled you, if there was one. -->

### Context

<!-- Tool and version, OS, anything that makes it reproducible. No sample data,
no absolute paths, no credentials — see the note below. -->

---

**Before you post, check this issue contains nothing you would not publish.**
Automated redaction removes home directories, tokens and clinical identifiers,
but it cannot recognise every sensitive sample name. You are the last check.

<!--
Why bother: this collection is grounded in the published literature and given
away under CC-BY. It gets better only when people who use it say what broke.
If you report a gap you can also propose the fix — see
.github/ISSUE_TEMPLATE/propose-skill.md and governance/AUTHORSHIP.md, which
records authored skills as credit toward the reviewer tier.
-->
