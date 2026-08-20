# The contribution loop

How a collection built from published literature keeps improving after release.

Peer review makes a skill correct **as written**. Only use makes it correct **as
run**: a flag that changed in the tool's last minor release, a step that assumes
a file layout nobody has, a procedure that works but costs ten times what it
needs to. None of that is visible from the paper the skill was derived from.

The obstacle is not willingness. It is that writing a good issue costs more than
working around the problem once, so the person who found the defect pays, and
everyone after them pays again. The loop below moves that cost onto the agent
that was already in the session when it happened.

## What ships

| Piece | What it does |
|---|---|
| [`asb-contribute`](../collections/metabolomics/v2/skills/asb-contribute/SKILL.md) | Advertised skill. Fires on friction, classifies it, searches for an existing issue, drafts a redacted report, and files it **only** on an explicit yes. |
| [`scripts/skill_feedback.py`](../scripts/skill_feedback.py) | Renders the report, strips outbound secrets, and computes the fingerprint that merges reports of one problem. |
| [`.github/ISSUE_TEMPLATE/skill-feedback.md`](../.github/ISSUE_TEMPLATE/skill-feedback.md) | The manual path, for people not running an agent. |
| Proposal rails | `propose-skill`, `propose-meta-skill`, `claim-skill`, `proposals.yml`, and [`governance/AUTHORSHIP.md`](../governance/AUTHORSHIP.md) — where a report that carries its own fix becomes credit. |

## Three properties that decide whether this helps or hurts

**Aggregation over volume.** A hundred separate "this did not work" issues is
worse for a maintainer than ten issues carrying a hundred corroborations — and
worse for the reporter, whose account disappears into a pile. Every report gets
a fingerprint keyed on kind, target and the content words of the symptom, so a
close restatement of a known problem lands as a comment on the open issue. The
fingerprint catches close restatements, not arbitrary paraphrase, so the skill
searches open issues as well.

**Consent, not automation.** Nothing is posted without an explicit yes in the
session, and the user is shown the exact body rather than a summary of it —
they are deciding whether to publish that text, which they cannot judge from a
paraphrase. Redaction removes home directories, credentials and the clinical
identifiers the release gate already knows about, and names what it stripped;
it cannot recognise a sensitive sample name, and the skill says so rather than
implying a guarantee.

**One offer per problem.** A prompt that returns after being declined stops
being a contribution channel and becomes a reason to disable the plugin.

## Companion skills considered

Only one skill is advertised, because every advertised description is paid for
in the session prompt of every user (`asb-contribute` costs ~96 tokens). The
rest were folded in or deferred:

| Candidate | Decision |
|---|---|
| **Citation / credit** — emit the collection DOI plus the source DOIs actually relied on | **Folded into `asb-contribute`.** Reciprocity is easier to ask for once the user has seen the credit machinery work in their favour, and it needs no separate trigger. |
| **Claim authorship** — link an authored skill to an ORCID | **Deferred.** `claim-skill.md` and `tier_update --credit-author` already cover it; a skill would only wrap them. Revisit if the template goes unused. |
| **Session provenance report** — what was applied, what was grounded, what was assumed | **Deferred, strongest candidate.** Genuinely useful for a methods section, but it wants a session-log surface that does not exist yet. |
| **Pre-flight grounding check** — verify a skill's claim against its source before acting | **Not a new skill.** Already step 4 of `asb-metabolomics`, via the Perspicacité binder. Duplicating it would split the protocol. |

## For maintainers

Reports arrive labelled `usage-feedback` + `needs-triage`, with `propose` added
when the reporter is asking for new work. Triage on the kind:

- `defect` / `drift` → fix the skill; the fingerprint finds every corroborator to notify.
- `gap` / `composition` → invite a proposal, or stage one; see `governance/COMMUNITY_SKILLS.md`.
- `efficiency` → usually a workflow or a better default, rarely a new leaf.
