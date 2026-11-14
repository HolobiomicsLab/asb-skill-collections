# EDAM vocabulary and remap

The collection tooling uses a pinned EDAM snapshot. It does not query an
ontology service while resolving, remapping, or running a gate. The vocabulary
contains the four EDAM branches and records the source CSV digest and the
CC-BY-SA-4.0 ontology licence. Release `1.25` is inferred from the maximum
numeric value in the CSV `Created in` column, not read from release metadata.

## Resolution statuses

`scripts/edam_vocabulary.py` resolves an IRI to one of five statuses:

| Status | Meaning |
|---|---|
| `valid` | The exact class exists and is not obsolete. |
| `obsolete` | The exact class is obsolete. A live same-branch `replacedBy` is returned when available. |
| `wrong_branch` | The numeric identifier exists only in another branch, such as `topic_3272` versus `data_3272`. |
| `ghost` | The numeric identifier exists in no branch in this snapshot. |
| `malformed` | The value is not an `http://edamontology.org/<branch>_<digits>` IRI. |

A number above the snapshot maximum is a ghost. It may be a newer EDAM term,
not necessarily a fabrication. In particular, `topic_3993` and `operation_4096`
may belong to a release newer than this snapshot. Do not treat a pinned
vocabulary as proof about later releases.

Refresh the table offline and supply the generation date explicitly:

```bash
python scripts/edam_vocabulary.py refresh \
  --csv <local EDAM.csv> \
  --out scripts/data/edam_vocabulary.json \
  --date YYYY-MM-DD
```

## Remap tiers

### Per-domain rules

T1 and T2 are generic and need no domain rules. T3, T3b and T4 load
`scripts/rules/<domain>/edam_remap_rules.yaml`, with `<domain>` resolved from
`collection.yaml`; `--rules` selects another file. These tiers refuse to run
without the file. The receipt records its path, version and SHA-256 digest.

`scripts/remap_edam.py` defaults to T2 and to a dry run. T1 removes unresolved
identifiers. T2 also replaces obsolete identifiers with a live same-branch
`replacedBy`, or removes them when no such replacement exists. T3 additionally
removes `topic_0121` when the leaf has no proteomics signal in its tools, name,
description, or body. T3b additionally removes `operation_3646` and
`operation_0282`. T4 instead removes all seven foreign operations measured by
the audit: those two plus `operation_3218`, `operation_3216`, `operation_3219`,
`operation_3222`, and `operation_3891`.

`topic_3520` is never touched. It is a live class whose preferred label is
"Proteomics experiment" and whose EDAM synonym is "Mass spectrometry". Removing
it would discard valid mass spectrometry annotations.

Dry runs on metabolomics v3 gave:

| Tier | Leaves | Papers | Empty topics | Empty operations |
|---|---:|---:|---:|---:|
| T1 | 693 | 316 | 1,040 | 2,948 |
| T2 | 921 | 360 | 1,042 | 3,057 |
| T3 | 1,854 | 426 | 1,126 | 3,057 |
| T3b | 2,302 | 441 | 1,126 | 3,610 |
| T4 | 2,709 | 450 | 1,126 | 4,107 |

The empty-field counts start at 903 topics and 2,646 operations. T1 and T2
match the audit exactly. T3 and later tiers differ because this implementation
uses the requested body vocabulary as well as the audit's name, description,
and tool vocabulary. That broader signal removes 968 `topic_0121` assignments;
the audit's narrower implementation removed 1,042.

## Metabolomics v3.0.1 procedure

Work on a branch of the domain repository `asb-skills-metabolomics`.
The tooling command never commits or publishes content.

1. Run the T2 dry run against the domain collection and retain its receipt.
2. Review the totals, per-rule counters, field changes, and top-five counts.
3. Add `--write` on the domain branch. The command updates the mirrored leaf
   fields, index rows, the sorted unique `collection.yaml` aggregate, and any
   populated EDAM fields in `tools_index.json`. Other file bytes are preserved.
4. Update the prose counts in `USAGE.md` by hand from `top_five` in the receipt.
5. Regenerate the release receipt through the release procedure. Switch the
   domain EDAM gate to `--edam-strict` after v3.0.1 has landed.

```bash
python scripts/remap_edam.py \
  --collection <domain checkout>/collections/metabolomics/v3 \
  --vocabulary scripts/data/edam_vocabulary.json \
  --tier T2 --receipt <evidence>/edam-remap.json \
  --date YYYY-MM-DD

python scripts/remap_edam.py \
  --collection <domain checkout>/collections/metabolomics/v3 \
  --vocabulary scripts/data/edam_vocabulary.json \
  --tier T2 --write --receipt <evidence>/edam-remap-write.json \
  --date YYYY-MM-DD
```

The `asb-edam-remap/1` receipt records the tier, vocabulary release and digest,
input digests, per-rule counters, totals, each `(slug, field, before, after,
rules)` change, top-five topic and operation counts, generation date, and write
mode. A write receipt additionally retains the original aggregate block,
metadata values, and index text needed for exact reversion.

Revert only from a receipt produced with `--write`:

```bash
python scripts/remap_edam.py revert \
  --collection <domain checkout>/collections/metabolomics/v3 \
  --receipt <evidence>/edam-remap-write.json
```

## Gate mode

`scripts/domain_content_gates.py` always keeps its canonical-prefix failures.
It also prints valid, obsolete, wrong-branch, ghost, and malformed counts plus
the ten most frequent unresolved identifiers. Resolution is advisory by default
while released v3 still carries its known defects. Add `--edam-strict` to the
focused command or the full orchestrating command to fail on every non-valid
resolution. `--edam-vocabulary` selects another pinned table.

The reusable domain workflow `.github/workflows/domain-gates.yml` exposes the
switch as the `edam_strict` input, false by default. The caller template sets it
to true for new domains; a released domain enables it once its collection
resolves cleanly, as metabolomics does from v3.0.1.

`scripts/normalize_skill.py` keeps `valid_edam` as the prefix-only predicate
used by `frontmatter_violations`. Its new `resolve_edam` delegates to the pinned
resolver. Existing callers retain their behavior; contribution normalization
can move to resolution later once callers supply a vocabulary and the project
decides whether obsolete terms are acceptable in proposed content.
