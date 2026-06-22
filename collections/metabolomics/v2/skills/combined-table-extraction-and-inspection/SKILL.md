---
name: combined-table-extraction-and-inspection
description: Use when after constructing a metabCombiner object by grouping features from two metabData objects by m/z, and before proceeding to anchor selection, RT mapping, or alignment scoring.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - metabCombiner
derived_from:
- doi: 10.1021/acs.analchem.0c03693
  title: metabCombiner
evidence_spans:
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS metabolomics.
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS metabolomics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabcombiner_cq
    doi: 10.1021/acs.analchem.0c03693
    title: metabCombiner
  dedup_kept_from: coll_metabcombiner_cq
schema_version: 0.2.0
---

# combined-table-extraction-and-inspection

## Summary

Extract and inspect the combined feature pair alignment table from a metabCombiner object to verify its structure and column composition before downstream processing. This skill validates that m/z-grouped feature pairs from two LC-MS datasets have been correctly aligned and formatted.

## When to use

After constructing a metabCombiner object by grouping features from two metabData objects by m/z, and before proceeding to anchor selection, RT mapping, or alignment scoring. Use this skill to verify that the combined table contains the expected 15 initial columns (idx, mzx, rtx, idy, mzy, rty, rtProj, score, rankx, ranky, plus sample and extra columns) and to inspect the alignment candidates produced by the binGap parameter.

## When NOT to use

- The input is not a metabCombiner object, or has not yet been constructed via the metabCombiner() function.
- You need to modify or filter the combined table — use dedicated metabCombiner filter functions (retention time range filter, missingness filter, duplicate filter) instead.
- The combined table has already been reduced or scored; use this skill early in the workflow, before anchor selection and RT mapping.

## Inputs

- metabCombiner object (constructed from two metabData objects with specified binGap parameter)

## Outputs

- combined feature pair alignment table (data.frame or matrix with 15+ initial columns: idx, mzx, rtx, idy, mzy, rty, rtProj, score, rankx, ranky, plus sample and extra columns)

## How to apply

Use the combinedTable() accessor function on the metabCombiner object to extract the combined feature pair alignment table. Inspect the first 15 named columns to confirm they contain input from both the X dataset (idx, mzx, rtx, and other X-derived columns), input from the Y dataset (idy, mzy, rty, and other Y-derived columns), and placeholder columns (rtProj, score, rankx, ranky) reserved for downstream computations. Verify row count and column names match the binGap parameter setting used during construction; a smaller binGap produces stricter m/z grouping and fewer candidate pairs. Use head() and str() to inspect data types and sample values, confirming that mz and rt columns are numeric and indices are integers.

## Related tools

- **metabCombiner** (R package that constructs the metabCombiner object and provides the combinedTable() accessor; handles m/z grouping and feature pair candidate generation) — https://github.com/hhabra/metabCombiner
- **R** (programming language and environment for loading metabData objects, constructing metabCombiner, and extracting/inspecting combined tables)

## Examples

```
library(metabCombiner); data(p30, p20); combined <- metabCombiner(p30, p20, binGap = 0.0075); head(combinedTable(combined)[, 1:15])
```

## Evaluation signals

- The combined table has exactly 15 or more initial named columns; the first 15 are idx, mzx, rtx (from X), idy, mzy, rty (from Y), rtProj, score, rankx, ranky (placeholders).
- All mz columns (mzx, mzy) and rt columns (rtx, rty, rtProj) contain numeric values; all index columns (idx, idy, rankx, ranky) contain integer values.
- The number of rows (candidate feature pairs) is consistent with the binGap parameter: smaller binGap values produce fewer rows, larger values produce more rows.
- Placeholder columns (rtProj, score, rankx, ranky) contain NA or 0 values initially, indicating they have not yet been populated by downstream processing steps.
- Sample columns (following the first 15 columns) match the union of sample names from both the X and Y metabData objects.

## Limitations

- The combined table contains only candidate feature pairs meeting the m/z grouping criterion (binGap); it does not yet contain alignment validity scores or retention time projections.
- Placeholder columns (rtProj, score, rankx, ranky) are empty at this stage and require downstream anchor selection, RT mapping spline, and feature pair alignment scoring steps to populate them.
- The combined table may contain erroneous alignments; visual or statistical inspection alone does not validate biochemical correctness — downstream scoring and filtering steps are needed.
- No changelog or version history is available in the repository to track changes to the combined table structure across metabCombiner versions.

## Evidence

- [results] Extract and verify combined table structure and columns: "The combined table contains 15 initial columns consisting of input from the x dataset (idx, mzx, rtx, ...), input from the y dataset (idy, mzy, rty, ...), and placeholder columns (rtProj, score,"
- [results] Use metabCombiner() constructor and combinedTable accessor: "Construct a metabCombiner object using the metabCombiner() function with p30 as the X dataset, p20 as the Y dataset, and binGap parameter set to 0.0075. Extract the combined feature pair alignment"
- [intro] metabCombiner determines possible feature pair alignments: "`metabCombiner` determines a list possible feature pair alignments (FPAs) and determines their validity through a pairwise similarity score."
- [intro] Feature alignment between datasets under non-identical conditions: "Feature alignment between datasets acquired under non-identical conditions presents numerous opportunities in untargeted metabolomics. The key challenge is achieving a correspondence between"
- [readme] metabCombiner takes peak-picked datasets and determines overlapping features: "*metabCombiner* takes peak-picked and conventionally aligned untargeted LC-MS datasets and determines the overlapping <mass-to-charge (m/z), retention time (rt)>  features, concatenating their"
