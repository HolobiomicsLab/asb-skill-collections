---
name: retention-time-peak-flagging
description: Use when after applying peak detection algorithms to identify local maxima in feature signals across retention time or m/z dimensions, but before exporting or filtering the peak list for further analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
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

# Retention-time peak flagging

## Summary

Peak flagging assigns confidence scores or binary flags to detected peaks in breath spectrometry feature data based on signal intensity and prominence thresholds. This utility validates and ranks peaks for downstream compound identification and filtering.

## When to use

After applying peak detection algorithms to identify local maxima in feature signals across retention time or m/z dimensions, but before exporting or filtering the peak list for further analysis. Use this skill when you need to distinguish high-confidence peaks from noise or borderline signals, particularly in breath VOC analysis workflows where signal-to-noise ratios vary across features.

## When NOT to use

- Input has not yet undergone peak detection—apply peak detection first.
- Feature data are already aligned and aggregated at the sample level rather than at the individual scan level.
- Downstream analysis requires unsupervised clustering or ranking of all peaks without pre-filtering.

## Inputs

- Detected peak list (indices, m/z values, intensity values, and scan times from peak detection)
- Numerical array or dataframe of feature signals with scan-time or m/z dimensions

## Outputs

- Labelled peak output with peak indices, intensity values, and confidence flags (CSV or JSON)
- Peak confidence scores or binary flag annotations for quality control filtering

## How to apply

Load the detected peaks (indices, m/z values, and intensity values) from the peak detection output as a numerical array or dataframe. Apply configurable thresholds based on signal intensity (absolute magnitude) and prominence (local maximum height relative to neighboring baseline) to assign confidence scores or binary flags to each peak. Peaks exceeding both thresholds receive high-confidence flags; those below are marked as low-confidence or excluded. Generate and export the flagged peak output in a structured format (CSV or JSON) that includes peak indices, intensity values, flags, and optionally prominence scores for downstream filtering or validation.

## Related tools

- **BreathXplorer** (Python package that integrates peak recognition as a utility step in the breath spectrometry analysis workflow; applies intensity and prominence thresholds to flag peaks after feature extraction and alignment) — https://github.com/wykswr/breathXplorer

## Evaluation signals

- Flagged peak output contains all detected peaks with non-null confidence scores or binary flags in expected range (e.g., 0–1 for scores, True/False for binary flags).
- Peaks above intensity and prominence thresholds are marked as high-confidence; those below are marked as low-confidence or excluded, consistent with the applied thresholds.
- Output schema matches the declared format (CSV or JSON) with columns/fields for peak index, m/z, intensity, and flag.
- No duplicate peak indices in the output; peak counts match or are a subset of input peak detections (depending on filter strictness).
- Flagged peaks correlate with manual inspection or known positive controls in breath samples (e.g., known VOCs).

## Limitations

- Threshold values (intensity and prominence) must be calibrated per instrument, sample type, and experimental design; no universal defaults are stated in the README.
- Peak flagging does not account for adduct or isotope patterns—those are separate post-processing steps in BreathXplorer.
- High-confidence flags do not guarantee compound identity; they only reflect signal quality. Further MS/MS or spectral library matching is required.
- Prominent peaks in regions of high baseline noise may be incorrectly flagged if prominence thresholds are not adjusted per m/z or retention-time region.

## Evidence

- [other] Apply peak detection algorithm to identify local maxima in the feature signal across the retention time or m/z dimension.: "Apply peak detection algorithm to identify local maxima in the feature signal across the retention time or m/z dimension."
- [other] Assign confidence scores or peak flags to each detected peak based on signal intensity and prominence thresholds.: "Assign confidence scores or peak flags to each detected peak based on signal intensity and prominence thresholds."
- [other] Generate and save labelled peak output with peak indices, intensity values, and flags in a structured format (CSV or JSON).: "Generate and save labelled peak output with peak indices, intensity values, and flags in a structured format (CSV or JSON)."
- [readme] BreathXplorer is a bioinformatic solution to process breath data generated from HRMS analysis. It contains a suite of functions, including feature extraction, feature alignment, and breath recognition.: "BreathXplorer is a bioinformatic solution to process breath data generated from HRMS analysis."
