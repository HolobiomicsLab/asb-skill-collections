---
name: m-z-retention-time-correspondence-mapping
description: Use when you have two peak-picked, conventionally aligned untargeted LC-MS metabolomics datasets (as metabData objects) acquired under different conditions or at different times, and you need to determine which features in dataset X correspond to which features in dataset Y so their sample.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
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

# m-z-retention-time-correspondence-mapping

## Summary

Identify and validate overlapping features between two LC-MS metabolomics datasets by grouping features with similar m/z and retention time coordinates, then constructing a unified combined table with aligned feature pairs. This skill is essential for merging metabolomics measurements acquired under non-identical instrumental or temporal conditions.

## When to use

You have two peak-picked, conventionally aligned untargeted LC-MS metabolomics datasets (as metabData objects) acquired under different conditions or at different times, and you need to determine which features in dataset X correspond to which features in dataset Y so their sample measurements can be concatenated into a single analysis table. This is particularly necessary when datasets were acquired with different instruments, ionization modes, or separation parameters but measure overlapping biological samples.

## When NOT to use

- Input datasets are already merged or de-duplicated; use only when you have two independent, unmapped peak tables.
- Datasets were acquired from completely different sample types or biological matrices with no expectation of feature overlap.
- Raw MS data has not yet been peak-picked and aligned; this skill requires pre-processed metabData objects, not raw .mzML or .raw files.

## Inputs

- metabData object (X dataset — first LC-MS run)
- metabData object (Y dataset — second LC-MS run)
- binGap parameter (numeric; m/z tolerance in Da, default ~0.0075)

## Outputs

- metabCombiner object
- combinedTable (data.frame with 15 initial columns: idx, mzx, rtx, idy, mzy, rty, rtProj, score, rankx, ranky, plus sample and extra columns)

## How to apply

Load both datasets as metabData objects into R. Construct a metabCombiner object using the metabCombiner() function, specifying the first dataset as the X dataset, the second as the Y dataset, and setting the binGap parameter (typically 0.0075 Da) to control the m/z tolerance window for initial feature grouping. The function performs m/z-based binning to group potential feature pairs, then accesses the combinedTable to retrieve the 15-column alignment structure containing feature indices, m/z values, retention times, and placeholder columns (rtProj, score, rankx, ranky) for downstream scoring and validation. Verify that the combined table contains the expected input columns from both datasets and that feature pair counts are reasonable given the input dataset sizes.

## Related tools

- **metabCombiner** (R package that implements m/z grouping, feature pair alignment detection, and combined table construction via the metabCombiner() function and combinedTable accessor) — https://github.com/hhabra/metabCombiner
- **mgcv** (Provides generalized additive model (gam) functions used internally by metabCombiner for retention time mapping spline fitting)

## Examples

```
comb <- metabCombiner(p30, p20, binGap = 0.0075); head(combinedTable(comb)[, 1:15])
```

## Evaluation signals

- The combinedTable contains exactly 15 initial (non-sample, non-extra) columns with correct names: idx, mzx, rtx, idy, mzy, rty, rtProj, score, rankx, ranky, and metadata columns.
- Feature pair count in the combined table is non-zero and reasonable (e.g., typically 50–80% of smaller input dataset size for well-overlapping plasma samples).
- m/z values for paired features (mzx and mzy) fall within the binGap tolerance window; no m/z differences exceed the specified binGap threshold.
- All placeholder scoring columns (rtProj, score, rankx, ranky) are initialized but contain NA or zero values (to be filled in downstream steps).
- Sample and extra column counts match the union of sample columns from both input datasets, confirming no data loss in the grouping step.

## Limitations

- The initial m/z binning is a heuristic grouping step; not all feature pairs in the combined table represent true biological matches—downstream anchor selection and similarity scoring are required to validate alignments.
- Retention time correspondence is unknown at this stage; rtProj and score columns are empty until anchor-based RT mapping and pairwise scoring are performed.
- The skill assumes both datasets have been pre-filtered for quality (e.g., missingness, duplicates, RT range) before metabCombiner object construction; it does not perform data cleaning.
- The binGap parameter is user-configurable and critical; too large a value will cause spurious feature grouping, and too small a value may miss true alignments due to instrumental m/z drift.

## Evidence

- [readme] metabCombiner takes peak-picked and conventionally aligned untargeted LC-MS datasets and determines the overlapping <mass-to-charge (m/z), retention time (rt)> features: "takes peak-picked and conventionally aligned untargeted LC-MS datasets and determines the overlapping <mass-to-charge (m/z), retention time (rt)> features"
- [other] The combined table contains 15 initial columns consisting of input from the x dataset (idx, mzx, rtx, ...), input from the y dataset (idy, mzy, rty, ...), and placeholder columns (rtProj, score, rankx, ranky) for downstream computations: "The combined table contains 15 initial columns consisting of input from the x dataset (idx, mzx, rtx, ...), input from the y dataset (idy, mzy, rty, ...), and placeholder columns (rtProj, score,"
- [intro] Feature alignment between datasets acquired under non-identical conditions presents numerous opportunities in untargeted metabolomics. The key challenge is achieving a correspondence between: "Feature alignment between datasets acquired under non-identical conditions presents numerous opportunities in untargeted metabolomics"
- [other] Construct a metabCombiner object using the metabCombiner() function with p30 as the X dataset, p20 as the Y dataset, and binGap parameter set to 0.0075.: "Construct a metabCombiner object using the metabCombiner() function with p30 as the X dataset, p20 as the Y dataset, and binGap parameter set to 0.0075"
- [intro] metabCombiner determines a list possible feature pair alignments (FPAs) and determines their validity through a pairwise similarity score: "metabCombiner determines a list possible feature pair alignments (FPAs) and determines their validity through a pairwise similarity score"
