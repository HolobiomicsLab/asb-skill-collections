---
name: peak-center-coordinate-localization
description: Use when you have LC-HRMS profile mode data with candidate peak regions (local maxima) exported as standardized rt×mz two-dimensional areas, and you need to automatically predict the precise peak-center location (both rt and mz coordinates) rather than relying on manual inspection or simple.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - PeakBot
  - TensorFlow
  - OpenMS / TOPPView
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
---

# peak-center-coordinate-localization

## Summary

Train and apply a CNN model to predict the precise rt×mz center coordinates of chromatographic peaks detected in LC-HRMS profile mode data. This skill enables automated, coordinate-level localization of peak maxima from standardized two-dimensional rt×mz areas extracted around local maxima.

## When to use

You have LC-HRMS profile mode data with candidate peak regions (local maxima) exported as standardized rt×mz two-dimensional areas, and you need to automatically predict the precise peak-center location (both rt and mz coordinates) rather than relying on manual inspection or simple gradient-descent algorithms. Use this when peak-center accuracy is critical for downstream quantification, alignment across samples, or feature table construction.

## When NOT to use

- Input data are already centroided (not profile mode); centroided peaks have fundamentally different structure and do not benefit from pixel-level coordinate regression.
- You only need binary peak-vs.-background classification and do not need precise center location; simpler classifiers would be more efficient.
- Reference chromatograms or ground-truth peak lists are unavailable or too small to generate sufficient training instances; the CNN requires large augmented training datasets to achieve accurate coordinate prediction.

## Inputs

- LC-HRMS profile mode chromatogram data (raw or NetCDF format)
- Standardized two-dimensional rt×mz area images around local maxima
- User-defined reference list of ground-truth isolated chromatographic peaks
- Training chromatograms for reference feature extraction

## Outputs

- Predicted peak-center rt coordinate (retention time)
- Predicted peak-center mz coordinate (mass-to-charge ratio)
- Peak-center coordinate prediction error metrics
- Trained CNN model weights (TensorFlow format)

## How to apply

First, prepare a training dataset by extracting reference chromatographic peaks from ground-truth chromatograms using smoothing and gradient-descent peak-finding, then match these peaks to a user-defined reference list and iteratively combine matched references to generate a large number of augmented training instances (including distraction peaks and different background types). Train a CNN model with an auxiliary regression head using TensorFlow on these instances, with GPU acceleration (CUDA) to reduce training time. The model learns to output peak-center coordinates (rt and mz) alongside peak-type classification. On new LC-HRMS data, apply the trained model to standardized rt×mz areas around detected local maxima to predict their center coordinates; validate predictions by checking coordinate prediction error on held-out test sets and visually inspecting exported detection examples.

## Related tools

- **PeakBot** (Python package that implements the complete CNN-based peak-center localization workflow, including reference feature extraction, training instance generation with GPU acceleration, CNN model training in TensorFlow, and inference on new LC-HRMS data) — https://github.com/christophuv/PeakBot
- **TensorFlow** (Deep learning framework used to implement and train the CNN model with regression head for peak-center coordinate prediction) — https://www.tensorflow.org/
- **OpenMS / TOPPView** (Optional visualization and export tool; detected peaks with predicted center coordinates can be exported as featureML files for inspection in TOPPView) — https://pubmed.ncbi.nlm.nih.gov/19425593/

## Examples

```
python quickExample_GPU.py
```

## Evaluation signals

- Peak-center coordinate prediction error (difference between predicted rt, mz and ground-truth center) on held-out test set is below acceptable threshold (article does not specify threshold; use domain expectations, e.g., <0.5% rt error, <5 ppm mz error).
- Predicted center coordinates lie within the bounding-box output by the model; coordinate should not fall outside suggested peak boundaries.
- Visual inspection of exported detection examples confirms that predicted centers align with the visual center of chromatographic peak regions in rt×mz space.
- Coordinate predictions are consistent across replicate samples of the same compound; peak-center rt and mz should be stable within known instrumental/biological variation.
- Downstream quantification or feature alignment using predicted center coordinates shows improved accuracy or reduced error compared to gradient-descent-only center estimates.

## Limitations

- GPU with CUDA support and sufficient memory (≥4 GB for default export batch size of 2048) is required for efficient training; CPU-only execution is possible but significantly slower. Block dimension (blockdim) and grid dimension (griddim) parameters must be tuned per GPU architecture.
- Coordinate prediction accuracy depends heavily on the size and representativeness of the training dataset; small or biased reference peak sets will lead to poor generalization on new samples.
- The model trains on augmented instances (synthetic combinations of reference peaks with distraction peaks and background); if the training distribution does not match the real data distribution (e.g., novel background types, unusual peak shapes), prediction error may increase.
- No changelog is provided in the repository, making it difficult to assess version differences or known bugs in coordinate prediction across releases.

## Evidence

- [readme] uses local-maxima in the LC-HRMS dataset each of which is then exported as a standarized two-dimensional area (rt x mz), which is used as the input for a machine-learning CNN model: "uses local-maxima in the LC-HRMS dataset each of which is then exported as a standarized two-dimensional area (rt x mz), which is used as the input for a machine-learning CNN model"
- [readme] reports whether the local-maxima is a chromatographic peak with left/right isomeric compounds or a signal of the background. Moreover, for chromatographic peaks it suggests a bounding-box and a peak-center: "for chromatographic peaks it suggests a bounding-box and a peak-center"
- [readme] generate a large number of training instances by iteratively combining them. Each such training instance can consist of a chromatographic peak or background signal and several other distraction peaks to generalize: "generate a large number of training instances by iteratively combining them. Each such training instance can consist of a chromatographic peak or background signal and several other distraction peaks"
- [readme] A GPU (CUDA) based approach is implemented that decreases the time required for their generation. The CNN model is implemented in the TensorFlow package: "A GPU (CUDA) based approach is implemented that decreases the time required for their generation. The CNN model is implemented in the TensorFlow package"
- [readme] It consists of several convolutional and pooling-layers and outputs a peak-type, -center, and -bounding-box.: "It consists of several convolutional and pooling-layers and outputs a peak-type, -center, and -bounding-box"
- [readme] If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512.: "If an exportBatchSize of 2048 requires some 4GB of GPU-memory. If you have less, try reducing this value to 1024 of 512"
- [readme] the properties of the reference features are also updated to best fit the chromatographic peaks from the reference chromatograms: "the properties of the reference features are also updated to best fit the chromatographic peaks from the reference chromatograms"
