# License tiers

`license_tier` answers a consumer question — *what may I do with the tool this skill
grounds on?* — and is **separate** from the paper open-access axis (`access.type`),
which answers *may we redistribute the source?*

## What the tier does and does not govern

Three different questions get confused with one another. Only the third is what
`license_tier` answers.

| Question | Governed by | Bearing on this collection |
|---|---|---|
| May we **describe** a tool in a skill? | Not the tool's licence. A tool's name, purpose, input/output types, and the fact that a paper used it are facts, and facts are not copyrightable. | None. Every tool is describable, proprietary ones included — otherwise no review article could exist. |
| May we **redistribute** the tool's code, wrapper or config? | The tool's licence, fully. | Only if we vendor those bytes. This collection ships prose and references, so it does not. |
| May a consumer **run** the tool for their purpose? | The tool's licence, fully. | This is what `license_tier` advises on. |

The consequence worth stating plainly: **an unlicensed tool is not thereby freely
usable, and it is not thereby un-describable either.** Absent a licence, default
copyright reserves all rights, and GitHub's terms grant other users only viewing and
forking within GitHub — no redistribution, no derivative works. That makes "no
licence" the *most* restrictive state for redistribution, not a permissive one. It
places no restriction at all on naming the tool and saying what it does.

So the tier is **downstream-use advice attached to a record**, never an admission
gate. A skill is never excluded because the tool it describes is proprietary or
unlicensed. Vendoring is what the tier gates.

## The tiers

| Tier | Meaning | Examples |
|---|---|---|
| `open` | Commercial use OK | MIT, Apache-2.0, BSD, MPL-2.0, CC-BY/CC0, **GPL/AGPL/LGPL** |
| `noncommercial` | Academic / noncommercial only | CC-BY-NC-*, PolyForm-Noncommercial, "academic use free, commercial by permission" |
| `restricted` | Established, and it constrains | CC-BY-ND, proprietary vendor EULA, declared all-rights-reserved |
| `unknown` | **No tool-level evidence found** | not looked up; lookup failed; a LICENSE file that no classifier could identify |

Copyleft maps to `open`: it governs derivative *distribution*, not whether a consumer
may use the tool commercially. Canonical SPDX→tier map: `governance/license_tiers.yaml`.
A licence string that is present but unrecognised falls back to `restricted`, unless
its text contains a noncommercial keyword → `noncommercial`.

### `unknown` is not `restricted`

`restricted` is a **verdict**: a licence was established and it constrains reuse.
`unknown` is an **open question**: nothing about the tool's own licence was
established. They have different remedies — a `restricted` tool needs a lawyer or a
vendor conversation, an `unknown` tool needs a lookup — so a consumer that cannot
tell them apart cannot act on either.

This is the same distinction `source_reuse` already draws between `None` (unknown,
blocks and reports loudly) and `none` (a known refusal). The tool axis previously
collapsed it, defaulting every unresolved tool to `restricted`; that made 257 of 909
tools indistinguishable from a genuine proprietary verdict, and made the catalogue
look far more resolved than it was.

**Why a tier value rather than a `--strict`-style flag.** The state belongs to the
record, not to the run. A flag would make the same catalogue mean different things
depending on how it was invoked, and every consumer would have to be told which mode
produced the file it is reading. A value is visible to everyone, is diffable, and
lets each consumer choose its own strictness. `--strict` also already means
"promotion mode" in `release_gate.py`; a second meaning there would be its own bug.

### Non-profit and commercial use

| Tier | Non-profit / academic | Commercial | Redistribution by us |
|---|---|---|---|
| `open` | permitted | permitted | permitted (respect copyleft on derivatives) |
| `noncommercial` | permitted | **not permitted** without a separate licence | link-only |
| `restricted` | per the licence | per the licence — usually a vendor EULA | link-only |
| `unknown` | describing and using are unaffected | verify before relying on it | **never vendor** — treat as all-rights-reserved |

Both `noncommercial` and `restricted` tiers are **link-only** in shipped grounding
bundles (referenced, never embedded). Beyond that, they differ:

- **`noncommercial`** additionally triggers a **blocking runtime acknowledgment**
  (commercial use is forbidden without a separate license; the consumer must
  explicitly confirm a permitted purpose before the skill is applied).
- **`restricted`** instead carries a **non-blocking soft note**: "licence established
  and it constrains reuse — check it before commercial use or redistribution."
- **`unknown`** carries a different non-blocking note: "no tool-level licence
  evidence — verify before redistributing." It does not block, because the absence of
  evidence is not a prohibition on use; it does forbid vendoring, because absence of a
  grant is not a grant.

## A tool's licence may only come from the tool

A licence claim on a tool record must rest on evidence about **that tool**: its own
repository, its own `DESCRIPTION`/`pyproject`, its own LICENSE file, its own
distribution page.

It may **never** be inherited from a paper that uses the tool. That inheritance was
the mechanism behind issue #42: every tool tier in the metabolomics catalogue was the
licence of a citing paper, aggregated most-restrictively across citations, which
recorded CAMERA (GPL) as Apache-2.0 because a paper using CAMERA is Apache-2.0, and
scikit-learn (BSD) as `noncommercial` because one preprint mentioning it is
CC-BY-NC-ND. Both directions are wrong and neither was visible, because the record
did not say whose licence it was.

`scripts/license_tier.py::licence_subject` exists to make the subject explicit, and
`tools_index.json` records `license_subject` on every entry. A `-paper` detection is
evidence about a paper and yields `unknown` on the tool axis. Enforced by
`scripts/check_tools_index.py`.

### Not every catalogue entry is software

The catalogue is assembled by extraction from papers, so an entry may be a software
package, a vendor instrument, a proprietary application, or a fragment a paper
happened to name. `entry_kind` says which, from the vocabulary in
`governance/tool_entry_kinds.yaml`:

| `entry_kind` | What it is | Tier |
|---|---|---|
| `software` | A tool with a licence to find | resolved, or `unknown` while it is not |
| `vendor_product` | An instrument or a proprietary application | `restricted` |
| `artefact` | An extraction defect: a module path, a bare URL, a function call, a sentence fragment | `unknown` |

**Instruments and vendor software are legitimate entries and legitimate to use.** A
lab uses the instrument it owns and the software it licensed; nothing here
discourages that. What they are not is redistributable, and there is no repository
to resolve an SPDX id from — so they take `restricted`, whose meaning is exactly
"use is governed by an agreement rather than an open licence", and not `unknown`,
which would claim a lookup is outstanding when none is possible.

Artefacts stay in the catalogue because skills reference their slugs and removing a
row would break that. Labelling them stops them counting as unresolved licence work.

The distinction is what makes the `unknown` count mean something. Of 909 entries: 195
`open`, 20 `restricted`, 1 `noncommercial`, and 693 `unknown` — of which 39 are
artefacts, leaving **654 pieces of software genuinely awaiting a licence lookup**.

Vendor terms are matched as whole words, never inside a token: `Thermo Xcalibur` is a
vendor product and `ThermoRawFileParser` is Apache-2.0 open source. Proprietary
applications that carry no vendor word are a curated list, because a name alone
cannot say whether software is proprietary and guessing either way is worse than a
reviewed entry — Skyline, ProteoWizard and msconvert are deliberately absent from it.
The vocabulary is measured against the 196 tools whose licences were resolved from
their own repositories: none of them may classify as anything but `software`, and
`tests/test_classify_tool_entries.py` fails if a carelessly added term makes one.

### Where a tool licence is allowed to come from

`scripts/resolve_tool_licenses.py` writes `tool_licenses.json`, and that file is the
only thing `enrich_tools_index.py` will tier a tool from. Two routes, both evidence
about the tool itself:

| Route | Evidence | Network |
|---|---|---|
| `self_published` | The tool is the subject of a paper already in the corpus — matched on exact name equality, never substring — so that paper's repository is the tool's, and the licence already resolved from it is the tool's licence. | no |
| `registry` | The tool's name matches a package in a curated life-science registry declared in `governance/tool_registries.yaml`. | yes, cached |

Only *curated life-science* registries are consulted, and that restriction is the
design. An exact name match is not by itself evidence: CRAN carries `AER` (Applied
Econometrics with R) and `arrow` (Apache Arrow), and PyPI carries a deprecated
`sklearn` shim. Matching a metabolomics tool name against a general-purpose index
reproduces the wrong-entity attribution of issue #42 one registry further down. A
registry that indexes only life-science software carries the domain constraint
structurally.

That is necessary but still not sufficient, and the measurement says so: of 94
registry matches reviewed on 2026-08-21, four were different projects sharing a short
name — `bart`, `grid`, `meteor`, `mist` — plus `ggplot`, where the corpus means the R
package and the registry has a Python re-implementation. They are recorded as
reviewed exclusions with reasons in `governance/tool_registries.yaml` rather than
guessed at by a detector, because no automatic signal separates them yet: requiring
the tool's own evidence to attest the package rejects 52 of the 94, CAMERA, mzmine,
rdkit, MSnbase and nextflow among them. Finding one is issue #43, and it is the
precondition for consulting a general-purpose registry at all.

**Where the routes disagree, the registry wins on the licence string.** A package
declares its own licence; a repository read infers one from whatever LICENSE file
sits at the root. `sneumann/xcms` is the case: DESCRIPTION says `GPL (>= 2)`, GitHub
reports NOASSERTION, and the LICENSE file classifies as LGPL-3.0 because it carries
terms for a bundled component. The superseded reading is kept on the record. A
disagreement in *tier*, though, is a contradiction rather than an override — the two
sources would give a consumer materially different advice — so the tool resolves to
`unknown` and the conflict is reported.

Every resolved entry records the `repo_url` it came from, so the claim can be
disputed. `check_tools_index.py` fails if `tools_index.json` drifts from the
resolution it was derived from, or if a tool carries a tier with no entry behind it.

## The source-reuse axis

`license_tier` answers *"what may I do with the tool?"*. It does **not** answer
*"what may we do with the source text?"* — and the two disagree. CC-BY-ND permits
commercial use of a tool (so it is not `noncommercial`) while forbidding derivative
text (so it is not `open`). Reading a paper's licence through the tool tier would
call such a source open, which is the mistake the blanket "pre-prints are always
CC-BY" rule made.

The second canonical table, `source_reuse` in `license_tiers.yaml`, answers the
source question. Reach it via `scripts/license_tier.py::source_reuse_for_license`.

| Value | Meaning | Examples |
|---|---|---|
| `full` | Redistribute, quote at length, derive — the open-access bar | CC-BY, CC-BY-SA, CC0 |
| `limited` | Some grant, but not full reuse; link-only | CC-BY-NC-*, CC-BY-ND-* |
| `none` | No reuse rights granted | arXiv `nonexclusive-distrib` |
| *(absent)* | **Unknown** — blocks admission, reported loudly | any unlisted licence |

An unlisted licence returns `None`, never a default. `None` (unknown) and `none`
(a known refusal) are different answers and must not be collapsed: one means we
failed to establish the rights, the other means the rights were withheld. Only
`full` admits a source at an open `access.type`. See
`scripts/preprint_license.py` and `governance/OPEN_ACCESS_POLICY.md` § Pre-prints.
