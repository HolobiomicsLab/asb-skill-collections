---
name: breath-volatile-peak-classification
description: Use when after feature extraction and alignment when you have a numerical feature table (CSV or dataframe) with intensity values across retention time or m/z dimensions, and you need to identify and rank peaks by signal quality and prominence rather than relying on all extracted features equally.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - BreathXplorer
derived_from:
- doi: 10.1021/jasms.4c00152
  title: BreathXplorer
evidence_spans:
- '[![PyPI](https://img.shields.io/pypi/pyversions/breathXplorer)]'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_breathxplorer_cq
    doi: 10.1021/jasms.4c00152
    title: BreathXplorer
  dedup_kept_from: coll_breathxplorer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00152
  all_source_dois:
  - 10.1021/jasms.4c00152
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Reconstruct the peak recognition utility identifying peaks from feature data

## Summary

Peak recognition detects and flags local maxima in breath spectrometry feature data (retention time or m/z dimension) to classify volatile organic compounds. This utility assigns confidence scores based on signal intensity and prominence thresholds, enabling prioritization of high-quality features for downstream analysis.

## When to use

Apply this skill after feature extraction and alignment when you have a numerical feature table (CSV or dataframe) with intensity values across retention time or m/z dimensions, and you need to identify and rank peaks by signal quality and prominence rather than relying on all extracted features equally.

## When NOT to use

- Input is already a list of validated, manually curated peaks—peak detection would be redundant.
- No consistent signal intensity variation exists across retention time or m/z (e.g., flat or noise-only spectra).
- Peak confidence scoring is not required; all extracted features are equally trusted.

## Inputs

- Feature table (CSV or dataframe) with m/z values and intensity columns
- Aligned feature table with sample-wise intensity values
- Numerical intensity signal array (retention time or m/z indexed)

## Outputs

- Labelled peak output file (CSV or JSON) with peak indices, m/z values, intensity values, and confidence flags
- Peak detection report with signal intensity, prominence scores, and threshold decisions

## How to apply

Load the aligned or single-sample feature table as a numerical array or dataframe. Apply a peak detection algorithm (e.g., topological or Gaussian-based) to identify local maxima in the intensity signal across the retention time or m/z dimension. Assign confidence scores or binary peak flags to each detected peak by comparing signal intensity and prominence against configurable thresholds (e.g., signal-to-noise ratio, peak width). Export the labelled peak output—including peak indices, intensity values, and confidence flags—in a structured format (CSV or JSON). This approach reduces false positives by filtering noise that lacks consistent breath-like peak morphology.

## Related tools

- **BreathXplorer** (Python package providing peak recognition utility as part of breath spectrometry workflow) — https://github.com/wykswr/breathXplorer

## Evaluation signals

- Peak indices and m/z values are correctly mapped to feature table rows; no out-of-bounds indices.
- Confidence scores or flags are assigned only to local maxima (intensity > neighbouring values); no spurious detections on flat or monotonic regions.
- Intensity and prominence values in the output match the source feature table; exported CSV/JSON parses without schema errors.
- Peaks flagged as high-confidence show higher signal-to-noise ratios and consistency (e.g., lower relative standard deviation) than low-confidence or unflagged peaks.
- Output includes all peaks above the specified threshold; no features are silently omitted.

## Limitations

- Peak detection algorithm performance depends on configurable thresholds (intensity, prominence); suboptimal thresholds may produce false positives or false negatives.
- Noisy or low-resolution spectra may yield ambiguous peak boundaries; requires upstream quality filtering (e.g., RSD-based control) to be effective.
- Overlapping or poorly resolved peaks in high-density m/z or retention-time regions may be misclassified or merged into single detections.
- Peak recognition does not perform compound identification; confidence scores reflect signal morphology only, not chemical annotation.

## Evidence

- [other] Apply peak detection algorithm to identify local maxima in the feature signal across the retention time or m/z dimension.: "Apply peak detection algorithm to identify local maxima in the feature signal across the retention time or m/z dimension."
- [other] Assign confidence scores or peak flags to each detected peak based on signal intensity and prominence thresholds.: "Assign confidence scores or peak flags to each detected peak based on signal intensity and prominence thresholds."
- [other] Generate and save labelled peak output with peak indices, intensity values, and flags in a structured format (CSV or JSON).: "Generate and save labelled peak output with peak indices, intensity values, and flags in a structured format (CSV or JSON)."
- [readme] * [Peak recognition](#peak-recognition): "* [Peak recognition](#peak-recognition)"
- [readme] BreathXplorer is a bioinformatic solution to process breath data generated from HRMS analysis. It contains a suite of functions, including feature extraction, feature alignment, and breath recognition.: "BreathXplorer is a bioinformatic solution to process breath data generated from HRMS analysis. It contains a suite of functions, including feature extraction, feature alignment, and breath"
