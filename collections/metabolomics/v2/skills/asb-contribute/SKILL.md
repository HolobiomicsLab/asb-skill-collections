---
name: asb-contribute
description: "Use when an ASB skill was wrong, stale, missing, or wasteful in practice — a skill's steps did not work, no skill covered the task, the leaves existed but nothing composed them, or the underlying tool has changed. Turns that friction into a redacted, dedupable report the user approves before anything is filed, and closes the credit loop for skills the user relied on."
license: CC-BY-4.0
metadata:
  role: meta
  helper: scripts/skill_feedback.py
  issue_templates:
  - .github/ISSUE_TEMPLATE/skill-feedback.md
  - .github/ISSUE_TEMPLATE/propose-skill.md
  - .github/ISSUE_TEMPLATE/propose-meta-skill.md
derived_from:
- doi: 10.5281/zenodo.20794027
  title: ASB Metabolomics Skill Collection v2 (metabolomics-v0.1.0)
schema_version: 0.2.0
---

# asb-contribute

The collection hardens from use, not from review. This skill is how a session
that hit friction becomes something a maintainer can act on.

## When this fires

Notice it yourself; do not wait to be asked. Any of these is a trigger:

- a skill's procedure failed, or its parameters no longer match the tool;
- the search returned nothing usable and the work was done unaided;
- the right leaves existed but the user had to compose them by hand;
- the skill worked, but at obviously avoidable cost;
- the user says some version of "that's wrong" about a skill's content.

**One offer per session per problem.** If the user declines, drop it — do not
raise it again for the same friction. Persistent asking is how a good idea
becomes an annoyance people disable.

## Protocol

### 1. Classify

Pick exactly one kind: `defect`, `gap`, `composition`, `efficiency`, `drift`.
The kind decides routing and labels, so guessing costs a maintainer real time.
If two apply, pick the one a fix would address.

### 2. Search before drafting

Look for an existing issue — by fingerprint, by skill slug, by symptom:

```bash
gh issue list --repo HolobiomicsLab/asb-skill-collections --state all \
  --search "<slug> OR <symptom keywords>" --limit 20
```

**If one matches, corroborate it. Do not open a second.** Ten corroborations on
one issue tell a maintainer what ten near-identical issues cannot, and the
reporter's account of the problem is read rather than buried.

### 3. Draft

```bash
python scripts/skill_feedback.py --kind defect --target <slug> \
  --symptom "..." --expected "..." --context "tool + version, OS" \
  --collection metabolomics/v2
```

It returns the title, body, labels and fingerprint, with home directories,
credentials and clinical identifiers already removed, and it names the
categories it stripped.

### 4. Show the user the exact body, then ask

Print the rendered body verbatim — not a summary of it. The user is deciding
whether to publish this text, and they can only decide that by reading it.

State plainly what redaction does and does not do: it removes paths, tokens and
clinical identifiers; **it cannot recognise a sensitive sample name**, so they
are the last check. Invite edits before filing.

Then make the case once, briefly and honestly. Something like: *this collection
is grounded in published work and given away under CC-BY; it improves only when
people who run it say what broke. Reporting this takes a minute and saves the
next person the hour you just lost.* Do not moralise, do not repeat it, and do
not imply an obligation.

### 5. File only on an explicit yes

```bash
gh issue create --repo HolobiomicsLab/asb-skill-collections \
  --title "<title>" --body-file <path> --label usage-feedback --label needs-triage
```

Corroborating instead:

```bash
gh issue comment <number> --body-file <path>
```

No `gh`, or no consent to use it: hand the user the rendered body and the
`new/choose` URL for the repository, and stop. Filing on their behalf without a
yes is publishing their words under their name.

### 6. Offer the fix, when there is one

A `gap` or `composition` report the user can answer themselves is worth more as
a proposal than as a request. Point them at `propose-skill` /
`propose-meta-skill`, and say what it earns: `governance/AUTHORSHIP.md` records
an authored skill as credit toward the reviewer tier, and `claim-skill` links it
to their ORCID.

## Closing the credit loop

When a session ends having leaned on this collection, offer the citation for
what was actually used — the collection DOI plus the source DOIs of the skills
applied, from each skill's `derived_from`. Reciprocity is easier to ask for
after the user has seen the machinery work in their favour, and a methods
section that names its sources is the point of grounding skills in literature at
all.

## What never happens here

- No issue, comment, or PR without an explicit yes in this session.
- No session transcript, file path, or dataset pasted in unredacted.
- No second issue when an open one already describes the problem.
- No report filed against a repository the user did not name.
