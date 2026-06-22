---
name: peak-detection-signal-processing
description: Use when after feature extraction from mzML/mzXML breath analysis data when you have a numerical array or dataframe of feature intensities across retention time or m/z dimensions and need to identify which features represent genuine volatile organic compound (VOC) signals rather than noise or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
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
---

# peak-detection-signal-processing

## Summary

Identify and flag local maxima (peaks) in breath spectrometry feature data by applying peak detection algorithms to signal intensity or m/z dimensions, assigning confidence scores based on signal prominence thresholds. This utility processes extracted features to produce labelled peak indices and intensity values for downstream metabolite identification.

## When to use

Apply this skill after feature extraction from mzML/mzXML breath analysis data when you have a numerical array or dataframe of feature intensities across retention time or m/z dimensions and need to identify which features represent genuine volatile organic compound (VOC) signals rather than noise or baseline variation.

## When NOT to use

- Input data is already a manually curated or vendor-provided peak list with pre-assigned peak/noise classifications.
- Raw mzML/mzXML spectra have not yet undergone feature extraction; apply feature extraction first.
- Peak detection parameters (intensity threshold, prominence threshold, algorithm type) are unknown and no prior quality control (RSD filtering) has been applied to remove obvious noise.

## Inputs

- FeatureSet object (m/z values, scan time, intensity array, relative standard deviation)
- Sample object (aligned feature table with m/z index and sample intensity columns)
- Numerical array or dataframe with feature intensities indexed by m/z or retention time

## Outputs

- Labelled peak table (CSV or JSON) with peak indices, m/z values, intensity values, and confidence flags
- Peak flags or confidence scores per detected feature
- Structured output suitable for MS/MS spectra matching or metabolite annotation

## How to apply

Load the feature extraction output (FeatureSet or aligned Sample object) as a numerical array indexed by m/z value with intensity columns corresponding to scan time or sample identifiers. Apply a peak detection algorithm to identify local maxima across the retention time or m/z dimension, using signal intensity and prominence thresholds to distinguish true peaks from background. Assign confidence scores or binary peak flags to each detected peak based on the signal-to-noise ratio and prominence relative to adjacent baseline. Export the labelled output as a structured format (CSV or JSON) containing peak indices, m/z values, intensity values, and confidence flags for validation and downstream MS/MS spectra matching or adduct/isotope annotation.

## Related tools

- **BreathXplorer** (Python package providing peak recognition utility component for breath spectrometry feature data; includes peak detection algorithm, confidence scoring, and structured output export) — https://github.com/wykswr/breathXplorer

## Evaluation signals

- Detected peaks have m/z values and intensity values within expected biochemical ranges for volatile organic compounds (typically m/z 40–500 in breath analysis).
- Confidence scores or flags are assigned consistently and reproducibly across replicate runs or similar samples.
- Peak indices and intensity values in the output are valid and map correctly back to the input feature array without off-by-one or alignment errors.
- Flagged peaks correspond to local maxima in the original signal; visual inspection or plotting of a subset of peaks against raw intensity traces confirms correct identification.
- Output CSV/JSON schema is valid and contains all required fields (peak indices, m/z, intensity, flags); no missing or null values for detected peaks.

## Limitations

- Peak detection algorithm performance depends on signal-to-noise ratio and prominence thresholds; poorly chosen thresholds may miss weak peaks or flag noise as peaks.
- Baseline subtraction or smoothing of the input signal is not described in the README; if the feature extraction output contains strong baseline drift or noise, peak detection sensitivity may be reduced.
- The README does not specify the exact algorithm (e.g., derivative-based, wavelet-based, or statistical) used for peak detection; without access to the source code, reproducibility across different implementations may vary.
- Peak recognition is listed as a utility but not fully documented in the provided README excerpt; detailed parameter documentation, algorithm choice (Topological vs. Gaussian analog), and failure modes are not fully described.

## Evidence

- [other] Apply peak detection algorithm to identify local maxima in the feature signal across the retention time or m/z dimension.: "Apply peak detection algorithm to identify local maxima in the feature signal across the retention time or m/z dimension."
- [other] Assign confidence scores or peak flags to each detected peak based on signal intensity and prominence thresholds.: "Assign confidence scores or peak flags to each detected peak based on signal intensity and prominence thresholds."
- [other] Generate and save labelled peak output with peak indices, intensity values, and flags in a structured format (CSV or JSON).: "Generate and save labelled peak output with peak indices, intensity values, and flags in a structured format (CSV or JSON)."
- [other] Load feature data from the feature extraction output as a numerical array or dataframe.: "Load feature data from the feature extraction output as a numerical array or dataframe."
- [readme] Peak recognition is listed under Utilities alongside MS/MS spectra export as part of the BreathXplorer analytical workflow: "* [Peak recognition](#peak-recognition)"
