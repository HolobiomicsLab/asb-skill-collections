---
name: metabolite-feature-normalization
description: Use when you have loaded two or more nontargeted LCMS feature tables
  from the same analytical method that contain m/z, retention time, and intensity
  values, and these datasets exhibit differences in metadata scale, distribution,
  or format that could confound cross-dataset feature matching or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - bmxp
  - Python
  - bmxp.eclipse
  - bmxp.gravity
  - bmxp (Python/C)
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btaf290/8128335
  title: Eclipse
evidence_spans:
- pip install bmxp
- They are written in Python and C
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_eclipse_cq
    doi: 10.1093/bioinformatics/btaf290/8128335
    title: Eclipse
  dedup_kept_from: coll_eclipse_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btaf290/8128335
  all_source_dois:
  - 10.1093/bioinformatics/btaf290/8128335
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-feature-normalization

## Summary

Normalize and standardize feature metadata (m/z, retention time, intensity distributions) across nontargeted LCMS datasets prior to feature alignment. This step ensures that features from different datasets are comparable and prepared for downstream matching and clustering in metabolomics workflows.

## When to use

You have loaded two or more nontargeted LCMS feature tables from the same analytical method that contain m/z, retention time, and intensity values, and these datasets exhibit differences in metadata scale, distribution, or format that could confound cross-dataset feature matching or downstream alignment operations.

## When NOT to use

- Input datasets were generated using different analytical methods or instrument configurations, as normalization assumes comparable instrumental performance and elution behavior.
- Feature tables have already undergone alignment or clustering in a prior run; re-normalization may corrupt existing correspondence annotations.
- Input data are already in a unified vendor format with pre-aligned m/z and RT scales (e.g., aligned mzML or pre-processed feature matrix).

## Inputs

- Two or more nontargeted LCMS feature tables in tabular format (Feature Metadata: Compound_ID, m/z, RT, Intensity; Feature Abundances: Compound_ID × injection_id)
- Analytical method specification (to ensure same-method datasets)

## Outputs

- Normalized feature metadata tables with standardized m/z, retention time, and intensity values across all input datasets
- Normalized feature abundance tables ready for downstream alignment (Eclipse) or clustering (Gravity)

## How to apply

Parse feature metadata (m/z, RT, intensity distributions) from each input dataset and apply normalization transformations to bring them into a common reference frame. The specific normalization strategy depends on the metadata type: m/z values are typically scaled to parts-per-million (ppm) tolerance thresholds to account for instrument mass accuracy; retention time is normalized to align elution windows across datasets; intensity distributions are standardized to account for variation in ionization efficiency or detector response. Apply these normalizations uniformly across all datasets being aligned so that subsequent matching algorithms operate on commensurable feature descriptors. Validation occurs by confirming that metadata ranges and distributions are consistent across all input datasets after normalization.

## Related tools

- **bmxp.eclipse** (Consumes normalized feature metadata and feature abundances to perform m/z-based and retention-time-based matching across datasets) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/eclipse/readme.md
- **bmxp.gravity** (Receives normalized and aligned features for redundancy clustering based on RT and correlation) — https://github.com/broadinstitute/bmxp/blob/main/bmxp/gravity/readme.md
- **bmxp (Python/C)** (Shared schema and data handling framework for metadata normalization and transformation) — https://github.com/broadinstitute/bmxp

## Evaluation signals

- All feature metadata conform to the BMXP shared schema (Compound_ID, m/z, RT, Intensity, Method, etc.); no NaN or out-of-range values remain in normalized fields.
- m/z values across datasets fall within expected instrument mass accuracy range (typically ≤ 5 ppm for high-resolution MS); RT distributions are aligned to comparable elution windows.
- Intensity distributions are comparable in scale and range across datasets (e.g., coefficient of variation or log-intensity spread is consistent).
- Downstream Eclipse feature matching produces expected number of candidate feature pairs and confidence scores; no obvious m/z or RT mismatches in output correspondence table.
- Schema customization (via bmxp.FMDATA, bmxp.IMDATA dictionaries) is correctly applied and consistent across all normalization steps and downstream modules.

## Limitations

- Normalization assumes all input datasets were acquired using the same analytical method and ionization conditions; cross-method or cross-platform datasets will not normalize comparably.
- Retention time normalization is sensitive to instrumental drift or column degradation; large RT shifts between datasets may indicate need for drift correction (Blueshift) before or after normalization.
- Intensity normalization does not account for biological variation or sample preparation differences; abundance-level normalization is separate and handled by downstream modules (e.g., Blueshift for technical replicates).
- The shared schema imposes fixed column headers and data types; datasets with non-standard metadata formats or missing fields (e.g., no m/z, no RT) cannot be normalized without manual reformatting.
- Normalization is a prerequisite for alignment but does not itself produce matched feature correspondences; it prepares input for Eclipse or other matching algorithms.

## Evidence

- [other] Parse and normalize feature metadata (m/z, RT, intensity distributions) across datasets.: "Parse and normalize feature metadata (m/z, RT, intensity distributions) across datasets."
- [readme] All BMXP modules use a shared schema and file formats with our prefered columns headers.: "All BMXP modules use a shared schema and file formats with our prefered columns headers."
- [readme] Some modules (Blueshift, Eclipse) require merging Feature Metadata + Feature Abundances.: "Some modules (Blueshift, Eclipse) require merging Feature Metadata + Feature Abundances."
- [other] Load two or more nontargeted LCMS feature tables (from same analytical method) in a tabular format containing m/z, retention time, and intensity values.: "Load two or more nontargeted LCMS feature tables (from same analytical method) in a tabular format containing m/z, retention time, and intensity values."
- [readme] Feature Metadata describes the LCMS feature. This is a mixture of fundamental nontargeted feature information, annotation info, and anything else.: "Feature Metadata describes the LCMS feature. This is a mixture of fundamental nontargeted feature information, annotation info, and anything else."
