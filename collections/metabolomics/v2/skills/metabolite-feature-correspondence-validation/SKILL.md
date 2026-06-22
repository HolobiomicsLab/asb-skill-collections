---
name: metabolite-feature-correspondence-validation
description: Use when after m/z grouping and pairwise alignment detection when you have a metabCombiner object containing candidate feature pair alignments and need to select a subset of mutually abundant, high-confidence anchors to anchor a nonlinear retention time mapping spline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-feature-correspondence-validation

## Summary

This skill identifies high-confidence anchor feature pairs across two disparately-acquired LC-MS metabolomics datasets by applying retention time windows, m/z tolerance, and abundance thresholds to establish a validated correspondence basis for subsequent RT mapping and alignment scoring. It is essential for bridging non-identical instrumental and acquisition conditions in untargeted metabolomics.

## When to use

Apply this skill after m/z grouping and pairwise alignment detection when you have a metabCombiner object containing candidate feature pair alignments and need to select a subset of mutually abundant, high-confidence anchors to anchor a nonlinear retention time mapping spline. Specifically, use it when your input datasets exhibit systematic RT drift or offset and you require validated reference points (anchor pairs) with both strong m/z–RT proximity and relative abundance concordance.

## When NOT to use

- Input datasets have already been aligned by a prior orthogonal method and require no further anchor validation.
- You lack abundance measurements or relative quantification data across both datasets; anchor selection requires tolQ (relative abundance tolerance) evaluation.
- Datasets were acquired under identical instrumental and LC conditions with negligible RT drift; anchor selection is unnecessary if all feature pairs are already well-aligned in RT space.

## Inputs

- metabCombiner object (post-m/z grouping and pairwise alignment detection)
- Candidate feature pair alignments with m/z, retention time, and abundance annotations

## Outputs

- Selected anchor feature pair set (table with rtx and rty retention time columns)
- CSV export of anchor pairs (optional)

## How to apply

Load the metabCombiner object from the prior m/z grouping and pairwise alignment step. Call selectAnchors() with window parameters (windx and windy defining retention time windows around anchor points in the X and Y datasets), m/z tolerance (tolmz), relative abundance tolerance (tolQ), and linear retention time quantile difference tolerance (tolrtq). Smaller window values increase anchor count but include more outliers; balance specificity against RT mapping robustness. Set useID=FALSE to rely on similarity scores rather than compound IDs. Extract the validated anchor set using getAnchors(), which returns a table with rtx and rty retention time columns. The anchor set serves as the ground truth for the subsequent RT mapping spline that will align all remaining feature pairs.

## Related tools

- **metabCombiner** (R package providing selectAnchors() and getAnchors() methods for anchor-based LC-MS metabolomics dataset alignment) — https://github.com/hhabra/metabCombiner
- **mgcv** (R package providing the generalized additive model (gam) function used by metabCombiner for fitting nonlinear RT mapping splines anchored to validated feature pairs)

## Examples

```
# Load metabCombiner object 'mc' from prior m/z grouping step
mc <- selectAnchors(mc, windx=0.03, windy=0.02, tolQ=0.3, tolmz=0.003, tolrtq=0.3, useID=FALSE)
anchors_df <- getAnchors(mc)
write.csv(anchors_df, file='selected_anchors.csv', row.names=FALSE)
```

## Evaluation signals

- Anchor set size and composition: number of selected anchors should be substantial enough (~20–50+) to support robust spline fitting, without excessive outliers; validate by visual inspection of rtx vs. rty scatter plot.
- m/z and RT concordance: all anchors must satisfy tolmz (m/z tolerance, typically ~0.003 Da) and rtq (linear RT quantile difference, typically ≤0.3); verify no anchors fall outside these thresholds.
- Relative abundance agreement: anchors must satisfy tolQ (relative abundance tolerance, typically ~0.3); check that paired feature abundances are reasonably similar, indicating genuine metabolite correspondence.
- Spline fit quality: after RT mapping, plot observed rtx against predicted rty; residuals should be small and randomly distributed, confirming anchors faithfully represent the underlying RT transformation.
- Downstream alignment precision: verify that the RT-mapped feature pairs exhibit improved cosine similarity scores and lower false-positive alignment rates in the subsequent Feature Pair Alignment Scoring step.

## Limitations

- Smaller retention time window values (windx, windy) increase anchor count but introduce outliers that can degrade spline fit quality; requires manual parameter tuning and validation.
- Anchor selection depends on abundance data quality; datasets with high missingness or poor peak-picking reproducibility may yield spurious anchors with inflated relative abundance concordance by chance.
- Linear RT quantile difference tolerance (tolrtq) assumes approximately linear drift; datasets with strongly nonlinear RT shifts may not be well-served by anchor pairs selected under this metric, requiring alternative RT mapping strategies.
- The selectAnchors() function does not validate that selected anchors span the full RT range of both datasets; anchors clustered in a single RT region may provide poor extrapolation for features at extremes.

## Evidence

- [other] The selectAnchors function identifies anchor feature pairs by applying retention time windows (windx and windy around anchor points), m/z tolerance (tolmz), relative abundance tolerance (tolQ), and linear retention time quantile difference tolerance (tolrtq): "The selectAnchors function identifies anchor feature pairs by applying retention time windows (windx and windy around anchor points), m/z tolerance (tolmz), relative abundance tolerance (tolQ), and"
- [other] smaller window values increase the number of anchors including outliers, and results are retrieved via getAnchors method returning a table with rtx and rty columns: "smaller window values increase the number of anchors including outliers, and results are retrieved via getAnchors method returning a table with rtx and rty columns"
- [other] Apply selectAnchors with window parameters (windx=0.03, windy=0.02), tolerance thresholds (tolQ=0.3, tolmz=0.003, tolrtq=0.3), and useID=FALSE to identify high-confidence anchor feature pairs based on similarity scores and m/z–RT proximity: "Apply selectAnchors with window parameters (windx=0.03, windy=0.02), tolerance thresholds (tolQ=0.3, tolmz=0.003, tolrtq=0.3), and useID=FALSE to identify high-confidence anchor feature pairs"
- [intro] metabCombiner determines possible feature pair alignments (FPAs) and determines their validity through a pairwise similarity score: "metabCombiner determines a list possible feature pair alignments (FPAs) and determines their validity through a pairwise similarity score"
- [intro] Feature alignment between datasets acquired under non-identical conditions presents numerous opportunities in untargeted metabolomics. The key challenge is achieving a correspondence between: "Feature alignment between datasets acquired under non-identical conditions presents numerous opportunities in untargeted metabolomics"
