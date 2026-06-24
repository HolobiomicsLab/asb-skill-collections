---
name: lc-ms-feature-quality-scoring
description: Use when immediately after peak detection and feature table generation
  from LC-MS data, when you need to rank or filter features by confidence before annotation
  or statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - masscube
  - Python
  techniques:
  - LC-MS
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-4.0
    url: huaxuyu/masscube
derived_from:
- doi: 10.1038/s41467-025-60640-5
  title: MassCube
evidence_spans:
- masscube is an integrated Python package for liquid chromatography-mass spectrometry
  (LC-MS) data processing.
- masscube is an integrated Python package for liquid chromatography-mass spectrometry
  (LC-MS) data processing
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lc-ms-feature-quality-scoring

## Summary

Compute per-feature quality scores for LC-MS detected features by evaluating peak shape, chromatographic metrics, signal-to-noise ratio, and coherence of isotopes/adducts. This skill produces a quality-annotated feature table with diagnostic flags (pass/fail/warning) suitable for downstream filtering and confidence assessment.

## When to use

Apply this skill immediately after peak detection and feature table generation from LC-MS data, when you need to rank or filter features by confidence before annotation or statistical analysis. Use it when raw detected features lack quality assessment, or when you require per-feature diagnostic information to justify inclusion/exclusion thresholds.

## When NOT to use

- Input is already a manually validated or literature-curated feature table where quality assessment is complete.
- Analysis requires only simple intensity filtering or m/z-based selection; use this skill only if multi-dimensional quality assessment is needed.
- Peak detection has not yet been performed; apply peak detection before quality scoring.

## Inputs

- Feature table (pandas DataFrame or CSV format) from peak detection
- Per-feature attributes: retention time, m/z, peak shape metrics, signal-to-noise ratio, chromatographic metrics

## Outputs

- Quality-annotated feature table with per-feature quality scores
- Quality flags per feature (pass/fail/warning)
- Diagnostic metrics per feature (peak definition, resolution, intensity consistency, isotope/adduct coherence)

## How to apply

Load the feature table (e.g., peak detection output) into Python using pandas, extracting feature attributes including retention time, m/z, peak shape, signal-to-noise ratio, and chromatographic metrics. Invoke MassCube's quality evaluation module to compute individual quality dimensions: peak definition (peak shape regularity and baseline separation), chromatographic resolution, intensity consistency across scans, and isotope/adduct coherence. Aggregate these dimensions into a single comprehensive quality score per feature, then assign quality flags (pass/fail/warning) based on empirically derived or user-defined thresholds. Output the quality-annotated feature table alongside per-feature diagnostics for transparency and traceability.

## Related tools

- **masscube** (Integrated LC-MS data processing package providing the quality evaluation module that computes per-feature quality scores, peak shape analysis, and isotope/adduct coherence assessment.) — https://github.com/huaxuyu/masscube/
- **Python** (Programming environment for loading feature tables via pandas, invoking MassCube quality functions, and outputting annotated results.)

## Examples

```
from masscube import FeatureQualityEvaluator; import pandas as pd; features = pd.read_csv('peak_detection_output.csv'); evaluator = FeatureQualityEvaluator(); quality_table = evaluator.compute_quality_scores(features); quality_table.to_csv('quality_annotated_features.csv', index=False)
```

## Evaluation signals

- Output feature table has the same number of rows as input feature table; no features are dropped during scoring.
- All features have non-null quality scores and assigned flags (pass/fail/warning); no missing values in quality columns.
- Per-feature diagnostics (peak definition, resolution, intensity consistency, isotope/adduct coherence) are numeric and within expected ranges (e.g., 0–1 for normalized metrics).
- Quality flags correlate with known artifact patterns (e.g., low SNR features flagged as 'fail', poor peak shape metrics correlate with 'warning').
- Summary statistics of quality scores show expected distribution (e.g., majority of features pass, small tail of warning/fail features).

## Limitations

- Quality thresholds are heuristic; users must validate that empirical pass/fail cutoffs are appropriate for their specific LC-MS instrument, ionization mode, and metabolite classes.
- Feature quality evaluation assumes features have already been detected and peak-picked; garbage input (e.g., noise spikes or misaligned peaks from poor LC conditions) may yield misleading quality scores.
- Isotope and adduct coherence assessment requires that the feature table include annotations linking related m/z features; if such relationships are unavailable, this dimension cannot be evaluated.
- No changelog found; version-specific changes to quality metrics are not publicly documented, which may affect reproducibility across software versions.

## Evidence

- [intro] Comprehensive feature quality evaluation as part of its LC-MS data processing pipeline: "MassCube provides comprehensive feature quality evaluation as part of its LC-MS data processing pipeline, which operates on detected features to generate per-feature quality scores."
- [other] Extract feature attributes and compute individual quality dimensions: "Extract feature attributes including retention time, m/z, peak shape, signal-to-noise ratio, and chromatographic metrics. 3. Compute individual quality dimensions (peak definition, chromatographic"
- [other] Aggregate per-feature quality scores and assign quality flags: "Aggregate per-feature quality scores into a single comprehensive metric and assign quality flags (pass/fail/warning). 5. Output a quality-annotated feature table with per-feature quality scores and"
- [readme] MassCube is an integrated Python package for LC-MS data processing: "masscube is an integrated Python package for liquid chromatography-mass spectrometry (LC-MS) data processing."
- [readme] Comprehensive feature quality evaluation as a core capability: "Comprehensive feature quality evaluation."
