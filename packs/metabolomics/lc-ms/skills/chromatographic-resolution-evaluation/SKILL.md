---
name: chromatographic-resolution-evaluation
description: Use when when you have a feature table from LC-MS peak detection (e.g., output from MassCube's nontargeted peak segmentation step) and need to assess which features have adequate chromatographic separation from coeluting or nearby peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - masscube
  - Python
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-025-60640-5
  title: MassCube
evidence_spans:
- masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing.
- masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing
- masscube is an integrated Python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_masscube_cq
    doi: 10.1038/s41467-025-60640-5
    title: MassCube
  dedup_kept_from: coll_masscube_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-60640-5
  all_source_dois:
  - 10.1038/s41467-025-60640-5
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-resolution-evaluation

## Summary

Evaluation of chromatographic peak resolution as a component of LC-MS feature quality assessment, determining whether detected peaks are sufficiently resolved from neighboring signals to be reliably characterized. This skill is applied within MassCube's comprehensive feature quality module to flag poorly resolved features that may confound downstream annotation and quantification.

## When to use

When you have a feature table from LC-MS peak detection (e.g., output from MassCube's nontargeted peak segmentation step) and need to assess which features have adequate chromatographic separation from coeluting or nearby peaks. Apply this skill before confident annotation of feature groups (isotopes, adducts, in-source fragments) or when you suspect peak overlap is introducing noise into intensity measurements or mass accuracy.

## When NOT to use

- Input data is already manually curated or has been pre-filtered for coelution; chromatographic resolution evaluation is redundant after manual review.
- Data originates from targeted MS/MS assays where peak identity is known a priori and coelution risk has been orthogonally validated.
- Feature table lacks sufficient metadata (retention time, peak width, intensity profile) needed to compute resolution metrics.

## Inputs

- feature table with per-feature retention time, m/z, peak shape, and signal-to-noise ratio attributes
- LC-MS peak detection output (e.g., from MassCube nontargeted segmentation)
- chromatographic raw data or derived peak metrics (peak width, intensity profile)

## Outputs

- quality-annotated feature table with per-feature chromatographic resolution scores
- per-feature quality flags (pass/fail/warning) incorporating resolution assessment
- diagnostic metrics for peak separation and coelution risk

## How to apply

Extract per-feature chromatographic metrics including retention time, peak width, and signal intensity from the detected feature table. Compute chromatographic resolution as one of several quality dimensions using MassCube's quality evaluation module, comparing each feature's peak shape and separation characteristics against resolution thresholds. The module aggregates this dimension with other quality metrics (peak definition, intensity consistency, isotope/adduct coherence) into per-feature quality scores and assigns flags (pass/fail/warning). Features with poor chromatographic resolution indicate potential coelution or peak tailing and should be handled conservatively in downstream feature grouping and annotation steps.

## Related tools

- **masscube** (Integrated Python package that implements the feature quality evaluation module, including chromatographic resolution assessment as one quality dimension aggregated into per-feature scores) — https://github.com/huaxuyu/masscube/
- **Python** (Environment for loading feature tables (via pandas), extracting chromatographic attributes, and calling MassCube's quality evaluation functions)

## Evaluation signals

- Output feature table contains a new numeric column for chromatographic resolution score and/or resolution quality flag; all input features are annotated
- Per-feature resolution scores correlate with manual visual inspection of peak shape and overlap in the raw chromatogram (coeluted peaks score lower)
- Aggregate quality flags (pass/fail/warning) are consistent across the feature population; no unexpected missing or NaN values
- Features flagged 'warning' or 'fail' for resolution show measurable peak width increase, tailing, or retention time proximity to other detected features
- Quality-annotated feature table maintains row-wise correspondence with input feature table; no features are dropped or duplicated

## Limitations

- Chromatographic resolution assessment relies on accurate peak detection and segmentation upstream; poor peak boundaries or missed small peaks will inflate apparent resolution scores.
- Resolution metric may be less informative in data with very broad or poorly defined peaks (e.g., early elution, dead volume effects) where peak shape itself is ill-defined.
- No changelog is publicly available for MassCube, making it difficult to track whether resolution calculation thresholds or aggregation logic have changed between versions.

## Evidence

- [other] Compute individual quality dimensions (peak definition, chromatographic resolution, intensity consistency, isotope/adduct coherence): "Compute individual quality dimensions (peak definition, chromatographic resolution, intensity consistency, isotope/adduct coherence) using masscube's quality evaluation module."
- [intro] Comprehensive feature quality evaluation as part of LC-MS processing: "Comprehensive feature quality evaluation."
- [other] Extract feature attributes for quality assessment: "Extract feature attributes including retention time, m/z, peak shape, signal-to-noise ratio, and chromatographic metrics."
- [other] Aggregate per-feature quality scores into comprehensive metric: "Aggregate per-feature quality scores into a single comprehensive metric and assign quality flags (pass/fail/warning)."
- [readme] MassCube provides accurate nontargeted peak detection: "Highly accurate nontargeted peak detection and segmentation."
