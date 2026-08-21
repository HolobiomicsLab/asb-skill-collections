---
name: w4m-three-table-format-conformance
description: Use when moving a feature table between Workflow4Metabolomics tools and
  the dataMatrix, sampleMetadata and variableMetadata files must agree on identifiers,
  order and R-name validity before a statistics step silently analyses mislabelled
  samples.
license: CC-BY-4.0
status: hold
metadata:
  tools:
  - Workflow4Metabolomics
  - Galaxy
  techniques:
  - LC-MS
  - GC-MS
  - NMR
  repo_url: https://github.com/workflow4metabolomics/tools-metabolomics
  related_skills:
  - galaxy-workflow4metabolomics-reproducible-processing
  license_tier: open
  provenance_tier: repository
  tool_license:
    tier: open
    requires_ack: false
    ref: GPL-3.0
    url: https://github.com/workflow4metabolomics/tools-metabolomics/blob/master/LICENSE.txt
  verified_against:
    repo_ref: master
    observed: '2026-08-21'
schema_version: 0.2.0
---

# w4m-three-table-format-conformance

Keep the three tables that Workflow4Metabolomics passes between its tools
mutually consistent, and catch the mismatch that produces statistics on the
wrong groups.

## When this applies

Workflow4Metabolomics does not pass a single feature table between steps. It
passes three tabular files, and 17 of the platform's 46 tool wrappers — across
LC-MS, NMR and the statistics suite — read or write them. Anything entering the
platform from outside, or leaving it for a local analysis, crosses this contract.

The failure it guards against is quiet. If the data matrix columns and the
sample metadata rows hold the same identifiers in a different order, every tool
still runs. The statistics are computed on samples assigned to the wrong class,
and nothing in the output says so.

## The contract

| file | shape | holds |
| --- | --- | --- |
| `dataMatrix` | variable × sample | the numeric matrix, nothing else |
| `sampleMetadata` | sample × metadata | class, batch, injection order, covariates |
| `variableMetadata` | variable × metadata | m/z, retention time, annotations |

All three are tab-separated, use `.` as the decimal mark and `NA` for missing
values. The binding rules:

- `dataMatrix` column names are exactly the `sampleMetadata` row names.
- `dataMatrix` row names are exactly the `variableMetadata` row names.
- `dataMatrix` carries no metadata columns. A retention-time column left in the
  matrix is read as a sample.

Identifiers must also be syntactically valid R names, because the tools are R.
A name beginning with a digit gains an `X`; a space becomes a `.`. If that
conversion happens in one table and not another, identical identifiers stop
matching.

## Procedure

1. **Run `Check Format` first, on every entry into the platform.** It compares
   the row and column names across the three tables and, where the sets agree
   but the orders differ, permutes the `dataMatrix` to match the metadata. It
   also performs the `make.names` conversion when asked. Running it costs one
   step and converts a silent mismatch into a reported one.

2. **Let the conversion happen in one place.** Enable the syntactic-validity
   option at the point of entry rather than letting individual tools rename as
   they go. Two tools applying `make.names` to differently-spelled originals is
   how the sets diverge.

3. **Build `sampleMetadata` before processing, not after.** One row per file,
   with explicit columns for class, batch and injection order. Batch correction
   and repeated-measures models need these columns and cannot reconstruct them.

4. **Use the platform's own join tools to attach metadata.** `Table Merge`
   merges a metadata table into the `dataMatrix`, and `W4M concatenate` merges
   two metadata tables. Joining in a spreadsheet reorders rows without
   announcing it, which is the mismatch this skill exists to prevent.

5. **Re-check after any step that changes dimensions.** Filtering variables,
   dropping a sample, or splitting by polarity all break the correspondence, and
   the tools that follow assume it holds.

## Verification

- Row and column counts: `dataMatrix` columns equal `sampleMetadata` rows;
  `dataMatrix` rows equal `variableMetadata` rows.
- Set equality *and* order equality of the identifiers, checked in both
  directions. Equal sets in different orders is the failure case, and a
  set-membership test passes it.
- The matrix is numeric throughout. A column that reads as character is usually
  a metadata column that was never removed.
- A known sample's class label, traced by hand from the raw file name through
  `sampleMetadata` to the statistics output, still says what it should.

## Limitations

- The check is structural. It cannot tell that a correctly-formatted
  `sampleMetadata` assigns a sample to the wrong group; only the file-name trace
  in the verification step catches that.
- Permutation only helps when the identifier sets are equal. A genuinely missing
  or extra sample is an error to fix upstream, not a formatting problem.
- The three-table shape is the platform's own interchange format, not a
  community standard. Exporting it for use elsewhere usually means flattening
  the three files back into one, and that conversion is not covered here.
