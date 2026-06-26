---
name: model-validation-on-chromatographic-standards
description: Use when after training a CNN model on labeled rt×mz two-dimensional
  areas extracted from LC-HRMS data, use this skill to quantify model performance
  on a held-out test set of reference chromatograms before deploying the model for
  peak detection on new samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - PeakBot
  - TensorFlow
  - TOPPView (OpenMS)
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-4.0
    url: christophuv/PeakBot
  license_tier: noncommercial
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# model-validation-on-chromatographic-standards

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Validate a trained CNN peak-picker against held-out chromatographic standards by measuring classification accuracy (peak vs. background) and regression error (bounding-box and peak-center coordinates). This ensures the model generalizes correctly to unseen LC-HRMS profile data.

## When to use

After training a CNN model on labeled rt×mz two-dimensional areas extracted from LC-HRMS data, use this skill to quantify model performance on a held-out test set of reference chromatograms before deploying the model for peak detection on new samples. Apply when you have ground-truth peak annotations (bounding-box, peak-center, peak-type labels) and need to confirm the model meets accuracy thresholds for production use.

## When NOT to use

- The model has not yet been trained on a labeled training set of rt×mz areas; first train the CNN using the training-data-generation skill.
- No ground-truth annotations are available for the test set; validation requires known peak labels and coordinates.
- The test set contains only a small number of examples (<50 local-maxima); statistical reliability of accuracy and error metrics is compromised.

## Inputs

- Held-out test set of standardized rt×mz two-dimensional area images (NumPy arrays or image files)
- Ground-truth annotations: peak-type labels (peak with left/right isomers vs. background), bounding-box coordinates, peak-center coordinates

## Outputs

- Classification accuracy (proportion of correct peak vs. background predictions)
- Bounding-box coordinate prediction error (e.g., mean absolute error, RMSE per coordinate)
- Peak-center coordinate prediction error (e.g., mean absolute error, RMSE)
- Verification images showing detected vs. ground-truth annotations
- featureML or tab-separated-values files with detected peak features for visual inspection in TOPPView or similar tools

## How to apply

Prepare a held-out test set of standardized rt×mz two-dimensional area images corresponding to local maxima from LC-HRMS chromatograms with ground-truth annotations (peak/background class, bounding-box coordinates, peak-center location). Run inference on the test set and collect the CNN's predicted peak-type, peak-center, and bounding-box outputs. Compute classification accuracy (proportion of local-maxima correctly labeled as peak vs. background) and regression error (e.g., mean absolute error or RMSE) for bounding-box and peak-center coordinate predictions. Compare error distributions against acceptable tolerances established during model development. Document examples of detection results exported as images for manual inspection of failure modes and edge cases (e.g., co-eluting isomers, wall artifacts).

## Related tools

- **PeakBot** (Provides CNN model architecture, inference pipeline, and utilities for exporting predicted peak features and verification images) — https://github.com/christophuv/PeakBot
- **TensorFlow** (Deep learning framework used to implement the CNN model and perform inference)
- **TOPPView (OpenMS)** (Optional visualization tool for inspecting detected chromatographic peaks in featureML format)

## Evaluation signals

- Classification accuracy on test set is ≥85–95% (threshold depends on acceptable false-positive and false-negative rates for downstream analysis)
- Bounding-box coordinate RMSE is ≤2–5 pixels (or ≤2–5% of image dimensions), indicating precise localization of peak boundaries
- Peak-center coordinate RMSE is ≤1–2 pixels, demonstrating reliable peak-center prediction
- Manual inspection of exported verification images shows visually correct peak annotations overlaid on rt×mz areas; misclassifications align with expected failure modes (e.g., wall artifacts, low-intensity noise)
- Distribution of prediction errors is approximately symmetric and centered near zero, with no systematic bias in over/under-prediction of coordinates

## Limitations

- Validation on a held-out test set does not guarantee performance on new chromatographic conditions (different solvents, pH, instruments, or sample types); external validation against independently acquired chromatograms is recommended.
- Model performance depends heavily on the quality and representativeness of the training dataset; if training data lack certain peak shapes or background types, test accuracy may not reflect real-world performance.
- GPU memory constraints (noted in README: 4 GB for exportBatchSize=2048, or 2 GB at 1024) may limit the size of validation batches, requiring serial processing and longer wall-clock time.
- Classification and coordinate errors are reported as aggregate metrics; rare edge cases (e.g., very narrow peaks, severe peak overlap, extreme mass-error artifacts) may not be adequately sampled in a small test set.

## Evidence

- [other] Validate the model on a held-out test set, evaluating classification accuracy and bounding-box / peak-center coordinate prediction error.: "Validate the model on a held-out test set, evaluating classification accuracy and bounding-box / peak-center coordinate prediction error."
- [readme] The CNN model reports whether the local-maxima is a chromatographic peak with left/right isomeric compounds or a signal of the background. Moreover, for chromatographic peaks it suggests a bounding-box and a peak-center.: "The CNN model reports whether the local-maxima is a chromatographic peak with left/right isomeric compounds or a signal of the background. Moreover, for chromatographic peaks it suggests a"
- [readme] Examples of the detection can be exported to images for user-verification. Furthermore, the detected chromatographic peaks can also be exported as featureML files and tab-separated-values files.: "Examples of the detection can be exported to images for user-verification. Furthermore, the detected chromatographic peaks can also be exported as featureML files and tab-separated-values files."
- [readme] If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512.: "If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512."
- [readme] The CNN model is implemented in the TensorFlow package. It consists of several convolutional and pooling-layers and outputs a peak-type, -center, and -bounding-box.: "The CNN model is implemented in the TensorFlow package. It consists of several convolutional and pooling-layers and outputs a peak-type, -center, and -bounding-box."
