---
name: metabcombiner-object-construction
description: Use when you have two peak-picked, conventionally aligned untargeted LC-MS metabolomics datasets (metabData objects) acquired under different conditions and need to identify overlapping <m/z, retention time> features across them.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3345
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - metabCombiner
  - mgcv
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.0c03693
  title: metabCombiner
evidence_spans:
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS metabolomics.
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS metabolomics
- Combine LC-MS Metabolomics Datasets with metabCombiner
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c03693
  all_source_dois:
  - 10.1021/acs.analchem.0c03693
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabcombiner-object-construction

## Summary

Construct a metabCombiner object by grouping feature pairs from two LC-MS metabolomics datasets by m/z tolerance and creating an aligned combined table with structured columns for downstream processing. This is the foundational step that establishes the feature pair alignment scaffold before scoring and reduction.

## When to use

You have two peak-picked, conventionally aligned untargeted LC-MS metabolomics datasets (metabData objects) acquired under different conditions and need to identify overlapping <m/z, retention time> features across them. Use this skill when you are ready to construct the initial feature pair grouping and combined alignment table after data formatting and filtering are complete.

## When NOT to use

- Input datasets are already merged or aligned—use this skill only when you have two separate peak-picked metabData objects that need initial grouping.
- Feature pair alignments have already been manually validated or filtered—this skill generates candidate alignments before scoring/reduction steps.
- Data have not yet been formatted and filtered (retention time range, missingness, duplicates)—complete data QC before object construction.

## Inputs

- metabData object (X dataset, typically higher-resolution or reference LC-MS run)
- metabData object (Y dataset, typically lower-resolution or secondary LC-MS run)
- binGap parameter (numeric, m/z tolerance in Da for grouping features)

## Outputs

- metabCombiner object containing the combined feature pair alignment table
- combined table with 15+ initial columns (idx, mzx, rtx, idy, mzy, rty, rtProj, score, rankx, ranky) plus sample and extra columns

## How to apply

Load two metabData objects (e.g., p30 as the X dataset and p20 as the Y dataset) into R. Call the metabCombiner() constructor function, specifying the X and Y datasets and setting the binGap parameter to define the m/z grouping tolerance (e.g., binGap=0.0075 Da). The function groups features from both datasets by m/z within the binGap window and generates candidate feature pairs. Extract the combined table using the combinedTable accessor to verify structure: the first 15 columns should contain idx, mzx, rtx from X; idy, mzy, rty from Y; and placeholder columns (rtProj, score, rankx, ranky) for downstream computations, followed by sample measurement columns and extra metadata columns.

## Related tools

- **metabCombiner** (R package providing the metabCombiner() constructor, combinedTable accessor, and metabData object handling for LC-MS feature alignment) — github.com/hhabra/metabCombiner
- **R** (Programming environment for executing metabCombiner object construction and table manipulation)
- **mgcv** (Provides generalized additive model (gam) functions used internally by metabCombiner for retention time mapping)

## Examples

```
library(metabCombiner); data(p30, p20); comb <- metabCombiner(x = p30, y = p20, binGap = 0.0075); head(combinedTable(comb)[, 1:15])
```

## Evaluation signals

- metabCombiner object is successfully created without errors; inspect class(object) == 'metabCombiner'
- Combined table has exactly 15 named initial columns in the expected order: idx, mzx, rtx, idy, mzy, rty, rtProj, score, rankx, ranky, followed by sample columns and extra columns
- Feature pairs are grouped within the specified binGap m/z tolerance; verify by examining mzx and mzy differences for all rows (should all be ≤ binGap)
- No spurious or duplicate feature pair entries; check that each unique combination of (idx, idy) appears exactly once in the combined table
- Placeholder scoring columns (rtProj, score, rankx, ranky) are initialized as NA or 0; these will be populated by downstream scoring steps

## Limitations

- The m/z tolerance (binGap) is global and uniform across all m/z ranges; users must choose a single binGap value appropriate for their instrument mass accuracy rather than adaptive per-region tolerance.
- Initial grouping is based on m/z alone; feature pairs sharing similar m/z but originating from different chemical compounds are not distinguished until downstream scoring incorporates retention time and similarity metrics.
- No changelog or version history available in the repository, limiting reproducibility tracking of changes to the metabCombiner constructor behavior across releases.

## Evidence

- [other] object structure and column composition: "The combined table contains 15 initial columns consisting of input from the x dataset (idx, mzx, rtx, ...), input from the y dataset (idy, mzy, rty, ...), and placeholder columns (rtProj, score,"
- [other] constructor call and parameters: "Construct a metabCombiner object using the metabCombiner() function with p30 as the X dataset, p20 as the Y dataset, and binGap parameter set to 0.0075."
- [readme] m/z grouping and feature alignment principle: "metabCombiner takes peak-picked and conventionally aligned untargeted LC-MS datasets and determines the overlapping <mass-to-charge (m/z), retention time (rt)> features, concatenating their"
- [intro] workflow context within broader pipeline: "Feature m/z Grouping and Pairwise Alignment Detection"
