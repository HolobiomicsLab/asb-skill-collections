---
name: roi-tensor-formatting-for-deep-learning
description: Use when after segmenting raw profile LC-MS data into candidate ROIs containing potential peaks, and before feeding ROI data to a CNN-Transformer peak detection network.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - mzML reader
  - QuanFormer CNN-Transformer detection network
  - PyTorch
derived_from:
- doi: 10.1021/acs.analchem.4c04531
  title: QuanFormer
evidence_spans:
- written in Python (v3.8.1)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_quanformer_cq
    doi: 10.1021/acs.analchem.4c04531
    title: QuanFormer
  dedup_kept_from: coll_quanformer_cq
schema_version: 0.2.0
---

# ROI tensor formatting for deep learning

## Summary

Convert segmented regions of interest (ROI) from LC-MS profile data into image-like tensors compatible with CNN-Transformer detection networks. This preprocessing step bridges raw mass spectrometry data and deep learning inference by reshaping peak ROI data into fixed tensor dimensions that the peak detection model expects as input.

## When to use

After segmenting raw profile LC-MS data into candidate ROIs containing potential peaks, and before feeding ROI data to a CNN-Transformer peak detection network. Required when preparing mzML-derived ROI candidates for binary classification (true peak vs. false peak) and peak boundary localization.

## When NOT to use

- Input is already centroided (m/z-intensity pairs only) rather than profile data; centroided data requires different segmentation and formatting logic.
- ROI candidates have already been formatted and validated by upstream preprocessing; reformatting wastes computation.
- Detection network input specification is unknown or unavailable; tensor dimensions cannot be matched without model checkpoint inspection.

## Inputs

- Parsed mzML profile LC-MS data (ion chromatogram and mass spectrum intensity values)
- Segmented ROI boundaries (retention time range, m/z range, and intensity values)
- Detection model checkpoint specification (tensor shape, dtype, expected input channels)

## Outputs

- Batch of formatted ROI tensors (image-like 2D or 3D arrays) ready for CNN-Transformer inference
- Tensor metadata (shape, dtype, normalization parameters) for validation

## How to apply

Extract ion chromatogram and mass spectrometry profile intensity values from each candidate ROI using mzML parsing. Normalize or rescale ROI intensity values to a consistent range suitable for image-like tensor input (typically 0–1 or standardized). Reshape ROI data into 2D or 3D tensor arrays matching the detection network's expected input dimensions (e.g., height × width channels for CNN-Transformer). Verify that tensor dtype (e.g., float32) and dimensions match the model checkpoint specifications (checkpoint0029.pth in QuanFormer). Apply optional smoothing (Gaussian sigma parameter, default 0) if configured. Stack formatted tensors in batch format for model inference.

## Related tools

- **mzML reader** (Parse raw .mzML file to extract ion chromatogram and mass spectrometry profile data for ROI extraction)
- **QuanFormer CNN-Transformer detection network** (Consume formatted ROI tensors and perform peak classification and boundary localization) — https://github.com/LinShuhaiLAB/QuanFormer
- **PyTorch** (Tensor creation, normalization, and batch formatting operations)

## Examples

```
python main.py --ppm 10 --source resources/example/profile --feature resources/example/profile_feature.csv --images_path resources/example/profile_output --output resources/example/profile_output/area.csv --model resources/checkpoint0029.pth
```

## Evaluation signals

- Tensor shape matches model checkpoint input specification (e.g., batch_size × height × width × channels)
- Tensor dtype is consistent with model weights (float32 for PyTorch checkpoint0029.pth)
- Intensity values fall within expected normalized range (no NaN, inf, or out-of-range extremes after rescaling)
- All ROI tensors in batch have identical shape (no ragged tensors)
- Model checkpoint loads without shape mismatch or dimension errors during inference

## Limitations

- Tensor formatting assumes profile LC-MS data; centroided data requires alternative preprocessing.
- Smoothing (smooth_sigma parameter) may reduce peak sharpness if sigma > 0; default σ=0 preserves raw intensity profile.
- ROI segmentation quality upstream directly affects tensor informativeness; poorly segmented ROIs will not be recovered by reformatting.
- Tensor dtype must match model weights precision; float32 is required for checkpoint0029.pth; automatic casting may introduce numerical drift.

## Evidence

- [other] Format ROI data as image-like tensors compatible with CNN-Transformer input requirements.: "Format ROI data as image-like tensors compatible with CNN-Transformer input requirements"
- [other] Verify ROI tensor dimensions and data types match detection network specifications.: "Verify ROI tensor dimensions and data types match detection network specifications"
- [intro] train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries: "train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries"
- [other] Segment profile LC-MS data into candidate regions of interest (ROIs) containing potential peaks.: "Segment profile LC-MS data into candidate regions of interest (ROIs) containing potential peaks"
- [readme] --smooth_sigma Default Value: 0 Description: Sigma value for smoothing.: "--smooth_sigma Default Value: 0 Description: Sigma value for smoothing"
