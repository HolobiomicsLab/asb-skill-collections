---
name: feature-property-refinement-from-training-data
description: Use when you have a set of training LC-HRMS chromatograms (retention time × m/z matrix format) and a manually curated reference list of isolated single chromatographic peaks, and you need to update the reference peak properties (retention time, m/z, peak shape) to match the actual peak signatures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - PeakBot
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bioinformatics/btac344
  title: PeakBot
evidence_spans:
- PeakBot is a python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_peakbot_cq
    doi: 10.1093/bioinformatics/btac344
    title: PeakBot
  dedup_kept_from: coll_peakbot_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac344
  all_source_dois:
  - 10.1093/bioinformatics/btac344
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-property-refinement-from-training-data

## Summary

Refine chromatographic feature properties (retention time, m/z, peak shape parameters) by matching peaks detected via smoothing and gradient-descent algorithms in training chromatograms against a user-defined reference list of isolated single peaks. This skill enables accurate ground-truth feature definition for machine learning model training in LC-HRMS peak detection.

## When to use

You have a set of training LC-HRMS chromatograms (retention time × m/z matrix format) and a manually curated reference list of isolated single chromatographic peaks, and you need to update the reference peak properties (retention time, m/z, peak shape) to match the actual peak signatures observed across different training samples before generating synthetic training instances for a CNN model.

## When NOT to use

- Training chromatograms contain primarily background signal or noise with few detectable peaks; the matching step will fail or produce unreliable updates.
- Reference list is already validated and stable across multiple instrument runs; re-refinement may introduce unnecessary noise or drift.
- Peak properties are expected to vary significantly between samples due to instrumental drift or chemical interference; single-pass refinement may not capture the full distribution.

## Inputs

- Training LC-HRMS chromatograms in retention-time × m/z matrix format (e.g., netCDF, mzML, or equivalent 2D array)
- User-defined reference list of isolated single chromatographic peaks (ground-truth features with initial retention time, m/z, and peak descriptors)

## Outputs

- Updated reference list with refined peak properties (retention time, m/z, peak shape parameters, bounding-box coordinates, peak centers)
- Peak-to-reference match mapping (record of which detected peaks were matched to which reference features)

## How to apply

Load training chromatogram data as standardized two-dimensional retention-time × m/z matrices. Apply a smoothing filter to reduce noise, then execute a gradient-descent peak search algorithm to detect local maxima and estimate peak borders and centers. Match detected peaks to the user-defined reference list using retention-time and m/z alignment criteria as matching keys. For each successfully matched peak, update the corresponding reference feature's retention time, m/z value, and peak shape parameters (e.g., bounding-box coordinates, peak center) to best fit the observed peaks from the training chromatograms. This refinement grounds the reference list in empirical peak observations rather than theoretical expectations, reducing false positives and improving model generalization when the refined references are subsequently used to generate augmented training instances.

## Related tools

- **PeakBot** (Python package that implements the smoothing, gradient-descent peak search, matching, and reference property refinement workflow for LC-HRMS chromatograms) — https://github.com/christophuv/PeakBot

## Examples

```
from peakbot import Chromatogram, Reference; chrom = Chromatogram.load('training_data.mzML'); refs = Reference.load('reference_list.txt'); matches = chrom.match_peaks_to_references(refs, rt_tolerance=10, mz_tolerance=5); refs.update_from_matches(matches); refs.save('refined_reference_list.txt')
```

## Evaluation signals

- Matched peaks exhibit retention-time and m/z offsets consistent with instrumental measurement error (e.g., ±a few seconds in RT, <5 ppm in m/z); large systematic deviations indicate misalignment.
- Updated reference properties show convergence across multiple training chromatograms (e.g., standard deviation of RT and m/z updates decreases with each refinement iteration).
- Refined reference features produce fewer false positives and higher precision when used to generate training instances and subsequently applied to held-out test chromatograms.
- Visual inspection of bounding-box and peak-center updates confirms that they capture the majority of the peak intensity mass in the 2D retention-time × m/z space.
- Reference properties remain stable if the skill is re-run on the same training dataset (idempotency check).

## Limitations

- Smoothing and gradient-descent algorithms may fail to detect peaks with low signal-to-noise ratio or overlapping/co-eluting features; unmatched peaks will not contribute to reference refinement.
- Retention-time and m/z alignment criteria must be tuned to the specific instrument and chemical context; inappropriate thresholds will produce spurious matches or miss valid peaks.
- Reference list must contain at least one isolated, high-quality example of each peak of interest; features absent from the reference list cannot be refined.
- GPU memory constraints (e.g., exportBatchSize parameter) may require parameter tuning for large-scale training datasets; CPU-only execution is slower.
- Peak shape parameters (e.g., bounding-box, peak center) are estimated from local maxima detection; highly irregular or multiply-modaled peaks may not be well-characterized by this approach.

## Evidence

- [intro] PeakBot matches detected peaks with a user-defined reference list to use the same chromatographic peak from different samples: "matched with a user-defined reference list (the ground-truth; isolated single chromatographic peaks) with the aim of using the same chromatographic peak but from different samples"
- [intro] Reference feature properties are updated to best fit the detected peaks from training chromatograms: "the properties of the reference features are also updated to best fit the chromatographic peaks from the reference chromatograms"
- [intro] Smoothing and gradient-descent algorithm detects peak borders and centers: "searching for chromatographic peaks using a smoothing and gradient-descend algorithm. The peaks' borders and centers are also estimated in this step"
- [intro] Training data format is retention-time × m/z matrix: "uses local-maxima in the LC-HRMS dataset each of which is then exported as a standarized two-dimensional area (rt x mz), which is used as the input for a machine-learning CNN model"
- [intro] Refined references enable augmented training instance generation: "generate a large number of training instances by iteratively combining them"
- [readme] Installation and runtime parameters for GPU execution: "Note: If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512."
