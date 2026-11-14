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

## Four routes

Wherever a skill is met (the router and the workflow router of a collection,
the search output, the site, the registry texts, `asbb`), the same four routes
are named in the same words. Each is an issue on the public registry,
<https://github.com/HolobiomicsLab/asb-skill-collections/issues>, with the
collection and the skill filled in.

| Route | Issue template | Labels | Drafted by |
|---|---|---|---|
| 1. this skill is wrong or could be better | `1-skill-feedback.md` | `usage-feedback`, `needs-triage` | router, `asbb report skill`, `scripts/skill_feedback.py`, the site's contribute page and paper page |
| 2. a skill is missing: request it, or propose yours | `2-request-skill.md`; `propose-skill.md` for a skill the reporter wrote | `usage-feedback`, `needs-triage`, `propose` | router, `asbb report missing`, `scripts/skill_feedback.py`, the contribute page (kind `gap` or `composition`) |
| 3. a paper is not referenced: propose it | `3-propose-paper.md` | `propose`, `paper-intake`, `needs-triage` | router, `asbb report paper`, the site's paper form |
| 4. something technical failed: report it | `4-technical-fault.md` | `bug`, `needs-triage` | router, `asbb report fault` |

A report drafted by a script or a form also carries `auto-report`. The kinds of
routes 1 and 2 are one closed list: `defect`, `drift`, `enhancement`,
`efficiency` (route 1), `gap`, `composition` (route 2). The earlier kinds are
read as `correction` and `bug` to `defect`, `tool-update` to `drift`,
`new-skill` to `gap`, `other` to `enhancement`. A technical fault is not a kind:
it is route 4. GitHub applies labels from an address only for people with
triage access; the issue template's own labels and the title prefix carry the
route for the others.

Every route lands on this public registry's issue tracker, through the issue
forms or a draft made with `asbb report` or `bin/report_issue.py`. A maintainer
carries each accepted report into the domain repository.

## What ships

| Piece | What it does |
|---|---|
| The `## Report and contribute` section of the router and the workflow router | Tells the agent when to offer a report, names the four routes, the consent rule and how to file. Rendered by `scripts/router_shape.py`. It is present on the merged content heads prepared for a later release. The published `v1.0.1`, `v2.0.1` and `v3.0.2` collections do not carry it; check the installed or archived version rather than inferring availability from the content head. |
| `bin/report_issue.py` | Standard-library helper a collection can ship beside `bin/search_skills.py`. It redacts, prints the title, labels, body, fingerprint and a prefilled address, and never calls the network. Generated from [`scripts/skill_feedback.py`](../scripts/skill_feedback.py) and `scripts/pii_config.py` into `scripts/templates/report_issue.py`. It is present on the merged content heads prepared for a later release. The published `v1.0.1`, `v2.0.1` and `v3.0.2` collections do not carry it. |
| `asbb report <route>` | The same helper for users of the package. |
| [`scripts/skill_feedback.py`](../scripts/skill_feedback.py) | The source of the routes, kinds, labels, redaction and fingerprint. [`scripts/make_improvement_report.py`](../scripts/make_improvement_report.py) and the site use its vocabulary. |
| The issue templates of [`.github/ISSUE_TEMPLATE/`](../.github/ISSUE_TEMPLATE/) | The manual path, for people not running an agent. The four routes come first in the chooser. |
| `asb-contribute` | The earlier agent-side skill (fires on friction, drafts with `skill_feedback.py`, files on an explicit yes). It ships only with metabolomics v2 (`<domain checkout>/collections/metabolomics/v2/skills/asb-contribute/SKILL.md`); metabolomics v3 and the other nine collections do not carry it. The router section replaces it. |
| Proposal rails | `propose-skill`, `propose-meta-skill`, `claim-skill`, the proposal checks of `domain-gates.yml`, and [`governance/AUTHORSHIP.md`](../governance/AUTHORSHIP.md), where a report that carries its own fix becomes credit. |

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

This section records the design of `asb-contribute` (metabolomics v2).

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

Released collections are listed in `collections.yaml`. Each lives in a
domain repository `asb-skills-<domain>`; for example, metabolomics v3 is in
`asb-skills-metabolomics`. Domain content belongs in the corresponding
`asb-skills-<domain>` checkout, while this repository holds tooling, governance
and the registry.

Triage per route. Every report arrives with `needs-triage`; a maintainer
replaces it with `triaged` once the route and the next step are settled, and
looks for an open issue with the same fingerprint first (close a duplicate with
`duplicate` and a link).

- **Route 1, `usage-feedback`.** `defect` and `drift`: reproduce against the
  skill's source paper and the current tool, then fix the leaf in the domain
  checkout on a branch, and run the domain gates. `enhancement` and
  `efficiency`: decide whether the change belongs in the leaf, in a workflow or
  in a better default. The fix is a skill revision: it lands on the domain
  repository's main branch, ships in the next patch or minor release of the
  collection, and the issue is closed with the release label that carries it.
  Until then the issue stays open, so the next reporter corroborates it. The
  fingerprint finds every corroborator to notify.
- **Route 2, `propose`.** `gap`: look for a method paper that covers the task
  and stage it as route 3, or invite the reporter to propose a skill
  (`propose-skill.md`, `governance/COMMUNITY_SKILLS.md`). `composition`: a
  workflow skeleton, through `propose-superskill.md`.
- **Route 3, `paper-intake`.** Copy the issue to the domain repository, where the
  intake automation reads its fields (`scripts/intake_issue.py`), or stage it
  by hand; see [Adding papers to a collection](adding-papers.md).
- **Route 4, `bug`.** Reproduce against the tooling of this repository and fix
  it here; when the fault is in shipped content (a router command, a vendored
  script), the fix also needs a regenerated collection.

For a new paper, use the proposal rail for a single reviewed suggestion or the
batch build-and-cut rail for a maintained collection. The complete commands and
the boundary between incremental builds and batch consolidation are in
[Adding papers to a collection](adding-papers.md).
