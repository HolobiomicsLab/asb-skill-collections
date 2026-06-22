---
name: lc-ms-profile-data-segmentation
description: Use when you have raw profile (not centroided) LC-MS data in .mzML format and need to prepare it for automated peak detection using a trained object detection network.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - QuanFormer
  - xcms (R package) with centWave algorithm
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

# lc-ms-profile-data-segmentation

## Summary

Segment raw profile LC-MS data in .mzML format into candidate regions of interest (ROIs) containing potential peaks, and format them as image-like tensors for CNN-Transformer detection networks. This skill bridges raw chromatographic data and peak detection by isolating localized m/z and retention time windows that serve as input for machine learning–based peak classification.

## When to use

Apply this skill when you have raw profile (not centroided) LC-MS data in .mzML format and need to prepare it for automated peak detection using a trained object detection network. Use it in targeted mode when you have known compound m/z and retention time values, or in untargeted mode when discovering peaks de novo using centWave-derived ROI candidates.

## When NOT to use

- Input is already centroided (binned) LC-MS data — use this skill only on raw profile data.
- Input is already a preprocessed feature table or peak list — segmentation operates on raw ion intensities, not summarized features.
- Peaks have been manually validated or are downstream of a proven peak detection method — redundant application of segmentation.

## Inputs

- .mzML file (raw profile LC-MS data)
- m/z values and retention times (targeted mode) or centWave peak list (untargeted mode)
- PPM tolerance parameter (default: 10)
- Retention time window width in scans (default minWidth=5, maxWidth=50)

## Outputs

- ROI tensors formatted for CNN-Transformer input (image-like arrays)
- ROI metadata file (m/z, retention time, scan range per ROI)
- Visualized ROI images (optional, for QC)

## How to apply

First, parse the raw .mzML file using an mzML reader to extract ion chromatogram and mass spectrometry profile data. Next, segment the profile data into candidate ROIs by applying m/z tolerance (default PPM=10) and retention time windows around known or detected peak positions. For each ROI, extract the 2D ion intensity array (m/z × retention time) and convert it to an image-like tensor with dimensions matching the CNN-Transformer model input specification (e.g., channels, height, width). Verify that tensor data types (typically float32) and dimensions conform to the detection network's requirements before passing to the model. The segmentation should preserve peak morphology while suppressing baseline noise; tune the PPM window width and retention time margin based on expected peak width (default: 5–50 scans) to balance signal inclusion with computational efficiency.

## Related tools

- **QuanFormer** (Implements .mzML parsing and ROI segmentation pipeline; provides trained CNN-Transformer detection network for peak classification) — https://github.com/LinShuhaiLAB/QuanFormer
- **xcms (R package) with centWave algorithm** (Generates untargeted ROI candidates and peak list in untargeted mode before QuanFormer segmentation) — https://www.bioconductor.org/packages/release/bioc/html/xcms.html
- **PyTorch** (Deep learning framework for CNN-Transformer model inference on segmented ROI tensors)

## Examples

```
python main.py --ppm 10 --source resources/example/profile --feature resources/example/profile_feature.csv --images_path resources/example/profile_output --output resources/example/profile_output/area.csv --model resources/checkpoint0029.pth
```

## Evaluation signals

- Verify ROI tensor dimensions match model input specification (e.g., batch size × channels × height × width)
- Confirm ROI tensor data type is float32 and values are in expected intensity range (no NaN, Inf, or extreme outliers)
- Check that m/z tolerance window captures the full isotopic envelope and baseline (PPM window should span ±PPM/2 around target m/z)
- Visually inspect plotted ROI images (via --roi_plot True) to confirm peaks are centered and not clipped by window boundaries
- Verify that ROI metadata CSV contains non-overlapping or appropriately flagged overlapping ROI ranges for the same feature

## Limitations

- Segmentation assumes known or pre-detected ROI positions; performance degrades for unexpected or shifted retention times (not handled by fixed window approach).
- PPM window is static and may exclude low-intensity isotopic peaks or include interfering ions at crowded m/z regions.
- ROI tensor resolution and cropping strategy may lose fine peak boundary information if retention time or m/z granularity is too coarse.
- Untargeted mode requires R, xcms, and MSnbase packages; centWave parameter tuning (minWidth, maxWidth, s2n, noise, mzDiff) is data-dependent and user-configurable.
- Currently supports only .mzML format; other formats (NetCDF, .raw, .d) require conversion before use.

## Evidence

- [other] Parse raw .mzML file using mzML reader to extract ion chromatogram and mass spectrometry profile data.: "Parse raw .mzML file using mzML reader to extract ion chromatogram and mass spectrometry profile data"
- [other] Segment profile LC-MS data into candidate regions of interest (ROIs) containing potential peaks.: "Segment profile LC-MS data into candidate regions of interest (ROIs) containing potential peaks"
- [other] Format ROI data as image-like tensors compatible with CNN-Transformer input requirements.: "Format ROI data as image-like tensors compatible with CNN-Transformer input requirements"
- [readme] train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries: "train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries"
- [readme] PPM value for ROI extraction. Default Value: 10: "PPM value for ROI extraction. Default Value: 10"
- [readme] Min peak width. Default Value: 5 ... Max peak width. Default Value: 50: "Min peak width. Default Value: 5 ... Max peak width. Default Value: 50"
