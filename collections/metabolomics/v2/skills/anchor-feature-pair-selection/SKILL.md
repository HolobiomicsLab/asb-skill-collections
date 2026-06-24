---
name: anchor-feature-pair-selection
description: Use when after completing feature m/z grouping and pairwise alignment
  detection on two LC-MS datasets acquired under non-identical conditions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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

# Anchor Feature Pair Selection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identify high-confidence mutually abundant feature pairs across two LC-MS metabolomics datasets by applying retention time windows, m/z tolerance, and abundance similarity thresholds to enable robust retention time mapping. This step bridges initial feature grouping and spline-based RT correction by establishing a trusted set of aligned landmarks.

## When to use

After completing feature m/z grouping and pairwise alignment detection on two LC-MS datasets acquired under non-identical conditions. Apply this skill when you have a metabCombiner object with grouped feature pairs and need to select a subset of high-quality anchors—typically those with small m/z differences, strong abundance correlation, and clustered retention times—before fitting a retention time mapping spline.

## When NOT to use

- Input datasets have not yet undergone m/z grouping and pairwise alignment detection.
- Feature pairs lack sufficient abundance or retention time variation to define meaningful anchors.
- Retention time drift is non-linear or dataset acquisition conditions are very similar (use direct feature matching instead).

## Inputs

- metabCombiner object (post-grouping and pairwise alignment detection)
- Feature pair table with m/z, retention time, and abundance columns

## Outputs

- Anchor feature pair table (CSV or data.frame) with rtx and rty columns
- metabCombiner object with selected anchors stored in internal state

## How to apply

Load the metabCombiner object containing grouped feature pairs from prior alignment detection. Call selectAnchors with carefully tuned window parameters (windx and windy restrict retention time search around candidate anchor points), m/z tolerance (tolmz, typically 0.003 Da), relative abundance tolerance (tolQ, typically 0.3 quantile units), and linear retention time quantile difference tolerance (tolrtq, typically 0.3). Smaller window values increase anchor count but may include outliers; larger windows reduce noise but risk missing true alignments. Set useID=FALSE to prioritize similarity-based scoring over feature identifiers. Retrieve the selected anchor set using getAnchors, which returns a table with rtx and rty columns representing retention times in each dataset. Verify anchor quality by inspecting the rtx–rty scatter plot for linearity and the count of anchors relative to total features (typically 5–15% for metabolomics data).

## Related tools

- **metabCombiner** (R package providing selectAnchors and getAnchors methods for anchor selection and retrieval) — https://github.com/hhabra/metabCombiner
- **mgcv** (Provides GAM (generalized additive model) implementation used by metabCombiner for retention time spline fitting after anchor selection)

## Examples

```
selectAnchors(metabCombiner_obj, windx=0.03, windy=0.02, tolmz=0.003, tolQ=0.3, tolrtq=0.3, useID=FALSE); anchors <- getAnchors(metabCombiner_obj); write.csv(anchors, 'anchor_pairs.csv')
```

## Evaluation signals

- Anchor count is 5–15% of total feature pairs (indicate balanced coverage without over-selection).
- rtx vs. rty scatter plot shows linear or monotonic trend with minimal scatter (anchors correctly reflect underlying RT alignment).
- All anchors pass m/z tolerance (rtx – rty < tolmz), abundance correlation (|Q_x – Q_y| < tolQ), and RT quantile difference (< tolrtq) thresholds.
- Spline fit quality improves (lower residual variance or AIC) after using selected anchors vs. random subsets.
- Manual spot-checking of 5–10 anchor pairs confirms high m/z and RT proximity across datasets.

## Limitations

- Window parameters (windx, windy) are dataset-dependent and require manual tuning; no automated selection is provided in the article.
- Anchor selection is sensitive to initial pairwise alignment quality; poor grouping upstream will propagate to poor anchor selection.
- Small window values may exclude legitimate anchors in regions of sparse features, leading to sparse spline fit.
- No explicit handling of bimodal or multi-modal RT distributions; assumes unimodal RT alignment structure.

## Evidence

- [intro] anchor_selection_definition: "The selectAnchors function identifies anchor feature pairs by applying retention time windows (windx and windy around anchor points), m/z tolerance (tolmz), relative abundance tolerance (tolQ), and"
- [intro] window_parameter_effect: "smaller window values increase the number of anchors including outliers, and results are retrieved via getAnchors method returning a table with rtx and rty columns"
- [intro] workflow_context: "Apply selectAnchors with window parameters (windx=0.03, windy=0.02), tolerance thresholds (tolQ=0.3, tolmz=0.003, tolrtq=0.3), and useID=FALSE to identify high-confidence anchor feature pairs"
- [intro] workflow_step_name: "Anchor Selection and RT Mapping Spline"
- [intro] problem_statement: "Feature alignment between datasets acquired under non-identical conditions presents numerous opportunities in untargeted metabolomics"
