---
name: retention-time-alignment-scoring
description: Use when after feature m/z grouping and pairwise alignment detection have identified candidate feature pairs, and anchor points have been selected to establish retention time correspondence.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# retention-time-alignment-scoring

## Summary

Scoring and validation of feature pair alignments across LC-MS metabolomics datasets by mapping retention time relationships through anchor-based spline fitting and similarity metrics. This skill transforms raw feature pair candidates into validated alignments by establishing a nonlinear retention time transformation model between datasets.

## When to use

After feature m/z grouping and pairwise alignment detection have identified candidate feature pairs, and anchor points have been selected to establish retention time correspondence. Use this skill when you need to validate which candidate pairs genuinely represent the same metabolite across two disparately-acquired LC-MS datasets by quantifying the consistency of their retention time and m/z relationships.

## When NOT to use

- Input datasets already have been manually or externally aligned to a reference standard — use direct matching instead
- Retention time shifts are highly non-monotonic or show discontinuities across the RT range — the spline assumption of smooth transformation will fail
- Fewer than ~5–10 confident anchor pairs are available — the spline fit will be unreliable and overfitting risk is high

## Inputs

- metabCombiner object with grouped feature pairs from m/z grouping step
- Anchor feature pairs table with rtx and rty columns
- Candidate feature pair list with m/z, retention time, and abundance data

## Outputs

- Feature pair alignment scores (numeric table)
- Validated feature pair assignments (table with rtx, rty, m/z alignment metrics)
- Retention time mapping spline model (GAM object)
- Combined feature table with aligned measurements from both datasets

## How to apply

Load the metabCombiner object containing candidate feature pairs and anchor selection results. The selectAnchors function identifies high-confidence anchor pairs using retention time windows (windx, windy around anchor points), m/z tolerance (tolmz ~0.003 Da), relative abundance tolerance (tolQ ~0.3), and linear retention time quantile difference tolerance (tolrtq ~0.3); smaller window values increase anchors but may include outliers. A generalized additive model (GAM) is fitted using the mgcv R package to create a smooth nonlinear spline mapping retention times from dataset X to dataset Y through the selected anchors. Feature pair alignment scores are then computed by evaluating how well each candidate pair's observed retention time shift aligns with the spline-predicted shift, combined with m/z proximity and abundance similarity. Pairs with scores above a threshold are validated as true alignments; those deviating significantly from the spline model are flagged as likely misalignments or noise.

## Related tools

- **metabCombiner** (Primary R package implementing selectAnchors, getAnchors, spline-based RT mapping via GAM, and feature pair alignment scoring) — https://github.com/hhabra/metabCombiner
- **mgcv** (R package providing the GAM (generalized additive model) function for fitting smooth nonlinear retention time transformation splines between datasets)

## Examples

```
anchors <- selectAnchors(metabCombiner_obj, windx=0.03, windy=0.02, tolmz=0.003, tolQ=0.3, tolrtq=0.3); anchor_table <- getAnchors(metabCombiner_obj); write.csv(anchor_table, 'anchors.csv')
```

## Evaluation signals

- Anchor selection produces a set of mutually abundant feature pairs with rtx and rty columns consistent with both dataset retention time ranges
- GAM spline fit exhibits smooth monotonic or near-monotonic RT transformation with residuals randomly distributed around zero (no systematic curvature)
- Alignment score distribution shows clear separation between high-scoring validated pairs and low-scoring spurious pairs; validated pairs cluster near the spline model prediction
- Export to CSV table shows realistic feature pair matches: m/z differences ≤ tolmz (e.g., ≤0.003 Da), RT shift consistency across the RT range, and non-redundant feature assignments
- Downstream combined table has no duplicate or conflicting feature entries; sample-level measurements from both datasets successfully concatenate without artificial gaps or outliers

## Limitations

- Smaller window values (windx, windy) increase the number of anchors but may include outliers, degrading spline fit quality; requires manual validation and potential re-tuning
- Spline model assumes smooth, monotonic retention time transformation — datasets with severe RT calibration drift, column degradation, or non-linear instrumental effects may violate this assumption
- Anchor-based approach depends critically on having a sufficient number of high-confidence anchor pairs; datasets with few common features or poor initial alignment detection will produce unreliable spline estimates
- Tolerance thresholds (tolmz, tolQ, tolrtq) are user-specified and data-dependent; no automatic threshold optimization is provided in the package

## Evidence

- [other] Anchor selection and tolerance parameters: "Apply selectAnchors with window parameters (windx=0.03, windy=0.02), tolerance thresholds (tolQ=0.3, tolmz=0.003, tolrtq=0.3), and useID=FALSE"
- [intro] Spline-based RT mapping via GAM: "a modified form of the `gam` function implemented in the *mgcv* R package"
- [other] How selectAnchors works mechanistically: "The selectAnchors function identifies anchor feature pairs by applying retention time windows (windx and windy around anchor points), m/z tolerance (tolmz), relative abundance tolerance (tolQ), and"
- [other] Impact of window parameters on anchor count and quality: "smaller window values increase the number of anchors including outliers, and results are retrieved via getAnchors method returning a table with rtx and rty columns"
- [intro] Validation workflow sequence: "Anchor Selection and RT Mapping Spline"
- [readme] Core purpose of metabCombiner: "*metabCombiner* takes peak-picked and conventionally aligned untargeted LC-MS datasets and determines the overlapping <mass-to-charge (m/z), retention time (rt)> features, concatenating their"
