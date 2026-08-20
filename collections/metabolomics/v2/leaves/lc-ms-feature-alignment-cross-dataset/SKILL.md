---
name: lc-ms-feature-alignment-cross-dataset
description: Use when you have two peak-picked, conventionally aligned LC-MS metabolomics
  datasets (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0599
  tools:
  - R
  - metabCombiner
  - mgcv
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.0c03693
  title: metabCombiner
evidence_spans:
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS
  metabolomics.
- This is an R package for aligning a pair of disparately-acquired untargeted LC-MS
  metabolomics
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lc-ms-feature-alignment-cross-dataset

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Align and merge feature measurements from two independently acquired untargeted LC-MS metabolomics datasets by matching overlapping <m/z, retention time> pairs and constructing a unified combined table. This skill is essential when integrating disparately-acquired datasets to expand sample coverage while maintaining feature correspondence despite non-identical acquisition conditions.

## When to use

Apply this skill when you have two peak-picked, conventionally aligned LC-MS metabolomics datasets (e.g., two plasma cohorts acquired on different instruments or at different times) and need to identify which features represent the same metabolites across both datasets so their sample measurements can be concatenated. The trigger is the presence of overlapping m/z and retention time ranges across the two datasets and the goal of creating a single combined feature table.

## When NOT to use

- Input datasets are already merged or from the same acquisition batch (feature alignment is only needed for cross-dataset integration of disparately-acquired data).
- One or both input datasets lack reliable retention time calibration; metabCombiner relies on RT correspondence and spline mapping for validation.
- The two datasets have no overlapping m/z or RT ranges (no potential feature matches to detect).

## Inputs

- metabData object (X dataset) — peak-picked, retention-time aligned LC-MS features with m/z, RT, and sample abundances
- metabData object (Y dataset) — peak-picked, retention-time aligned LC-MS features with m/z, RT, and sample abundances

## Outputs

- metabCombiner object — container holding both input datasets, combined feature pair alignment table, and intermediate computational results
- combinedTable (data frame) — unified feature table with 15+ core columns (idx, mzx, rtx, idy, mzy, rty, rtProj, score, rankx, ranky, sample measurements from X and Y, extra columns)

## How to apply

Load both metabData objects (X and Y datasets) into R and construct a metabCombiner object using the metabCombiner() function, specifying the binGap parameter (e.g., 0.0075 Da) to control the m/z grouping tolerance for feature pairing. The tool determines possible feature pair alignments by grouping features with similar m/z values within the binGap threshold, then validates candidate pairs through pairwise similarity scoring based on retention time and spectral properties. Extract the combined table from the resulting metabCombiner object using the combinedTable accessor; this table contains 15 initial columns (idx, mzx, rtx from dataset X; idy, mzy, rty from dataset Y; plus placeholder columns rtProj, score, rankx, ranky for downstream validation and filtering steps) followed by concatenated sample measurements and extra columns from both datasets. The initial alignment is followed by anchor selection, retention time mapping via spline fitting, and iterative scoring and filtering to reduce false positive pairs before finalizing the combined table.

## Related tools

- **metabCombiner** (Core R package that implements feature pair alignment detection, m/z grouping, pairwise similarity scoring, and combined table construction for cross-dataset LC-MS integration) — https://github.com/hhabra/metabCombiner
- **mgcv** (R package providing generalized additive model (GAM) function used for retention time mapping spline fitting during anchor-based RT calibration)

## Examples

```
library(metabCombiner); data(p30, p20); mb <- metabCombiner(p30, p20, binGap=0.0075); ct <- combinedTable(mb); head(ct[, 1:15])
```

## Evaluation signals

- The resulting combinedTable contains exactly 15 named core columns (idx, mzx, rtx, idy, mzy, rty, rtProj, score, rankx, ranky, plus sample and extra columns from both X and Y datasets) with no missing or misaligned column structure.
- Feature pairs in the combined table have score values assigned (numeric, non-null), indicating successful pairwise similarity scoring based on m/z, RT, and spectral alignment.
- The number of feature pairs in the combined table is consistent with the expected overlap given the binGap threshold and the m/z and RT distributions of the two input datasets.
- Sample measurements from dataset X (columns beginning with prefix from Y metadata) and dataset Y are correctly concatenated side-by-side for each feature pair without duplication or loss.
- Anchor feature pairs (high-ranking pairs used for RT mapping) are distributed across the retention time range, indicating successful spline-based RT calibration without isolated clusters.

## Limitations

- Feature alignment accuracy depends critically on the binGap parameter; setting it too large increases false positive pairs, while setting it too small may miss true matches. User must validate or tune binGap based on instrument mass accuracy and expected feature distributions.
- Datasets must be peak-picked and conventionally aligned before input; the tool does not handle raw MS data or unaligned peak lists.
- Retention time ranges of the two datasets must overlap substantially; if one dataset covers an entirely different RT window, few or no feature pairs will be detected.
- The method assumes features from both datasets have been acquired under similar but not identical conditions; if conditions are very different (e.g., different pH, temperature, or chromatographic method), spectral similarity scoring may fail to validate true matches.

## Evidence

- [readme] This is an R package for aligning a pair of disparately-acquired untargeted LC-MS metabolomics.: "This is an R package for aligning a pair of disparately-acquired untargeted LC-MS metabolomics."
- [readme] metabCombiner takes peak-picked and conventionally aligned untargeted LC-MS datasets and determines the overlapping <mass-to-charge (m/z), retention time (rt)> features, concatenating their measurements to form a combined table of sample mass spectral measurements.: "metabCombiner takes peak-picked and conventionally aligned untargeted LC-MS datasets and determines the overlapping <mass-to-charge (m/z), retention time (rt)> features, concatenating their"
- [other] The combined table contains 15 initial columns consisting of input from the x dataset (idx, mzx, rtx, ...), input from the y dataset (idy, mzy, rty, ...), and placeholder columns (rtProj, score, rankx, ranky) for downstream computations, followed by samples and extra columns.: "The combined table contains 15 initial columns consisting of input from the x dataset (idx, mzx, rtx, ...), input from the y dataset (idy, mzy, rty, ...), and placeholder columns (rtProj, score,"
- [intro] metabCombiner determines a list possible feature pair alignments (FPAs) and determines their validity through a pairwise similarity score.: "metabCombiner determines a list possible feature pair alignments (FPAs) and determines their validity through a pairwise similarity score."
- [intro] The workflow we outline here is composed of five major steps: 1) Data Formatting and Filtering 2) Feature m/z Grouping and Pairwise Alignment Detection 3) Anchor Selection and RT Mapping Spline 4) Feature Pair Alignment Scoring 5) Combined Table Reduction: "Feature m/z Grouping and Pairwise Alignment Detection, Anchor Selection and RT Mapping Spline, Feature Pair Alignment Scoring"
