---
name: area-integration-from-detection-output
description: Use when you have region-of-interest (ROI) LC-MS data and a pre-trained object detection model has already predicted peak locations and confidence scores.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python 3.8.1
  - QuanFormer
  - PyTorch
  - Python scipy.integrate
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

# area-integration-from-detection-output

## Summary

Extract peak boundary coordinates predicted by a CNN-Transformer object detection network from LC-MS data and integrate the area under the curve within those boundaries to quantify peak intensity. This skill bridges peak localization and peak quantification in raw profile LC-MS data.

## When to use

You have region-of-interest (ROI) LC-MS data and a pre-trained object detection model has already predicted peak locations and confidence scores. You need to convert those bounding-box predictions into integrated peak areas for downstream quantification or feature extraction in targeted or untargeted metabolomics workflows.

## When NOT to use

- Peak boundaries have already been manually defined or obtained from a non-detection-based method; use this skill only when boundaries come from the CNN-Transformer detector.
- Input is already a feature table with pre-computed areas; this skill is for boundary extraction and integration, not post-processing.
- Data format is not mzML; QuanFormer currently supports only mzML files.

## Inputs

- Detection network output with predicted peak bounding boxes and confidence scores (.pth model predictions)
- ROI LC-MS data (mzML profile or centroided format)
- Feature file (CSV) with columns: Compound Name, m/z, RT (required for targeted mode; optional for untargeted)

## Outputs

- Quantified peak areas table (CSV) with columns: Compound Name, m/z, RT, integrated area, filename
- Optional ROI visualization plots (PNG/PDF)

## How to apply

Load the detection network's output containing predicted peak locations and confidence scores from the CNN-Transformer model checkpoint. Extract peak boundary coordinates (left and right edges along the retention-time or m/z axis) from the model predictions, filtering by a confidence threshold (default 0.99 in QuanFormer). For each identified peak, apply numerical integration to compute the area under the curve within the localized boundaries. Compile quantified peak areas and associated metadata (compound name, m/z, RT, filename) into a structured output table (CSV). Optionally apply smoothing (sigma parameter) before integration to reduce noise artifacts.

## Related tools

- **QuanFormer** (CNN-Transformer object detection network for peak boundary localization and area integration in LC-MS data) — https://github.com/LinShuhaiLAB/QuanFormer
- **PyTorch** (Deep learning framework for loading and executing the pre-trained detection model checkpoint)
- **Python scipy.integrate** (Numerical integration library for computing area under the curve within localized peak boundaries)

## Examples

```
python main.py --ppm 10 --source resources/example/profile --feature resources/example/profile_feature.csv --images_path resources/example/profile_output --output resources/example/profile_output/area.csv --model resources/checkpoint0029.pth --threshold 0.99 --smooth_sigma 0
```

## Evaluation signals

- Output CSV contains exactly one row per detected peak with no missing values in Compound Name, m/z, RT, and area columns.
- All integrated areas are positive and non-zero for true peaks; areas for confidence-filtered predictions (below threshold 0.99) are excluded from output.
- Peak boundary coordinates (left/right edges) are consistent with ROI dimensions and retention-time/m/z ranges in the input mzML file.
- Integrated areas correlate positively with visual peak height/intensity in ROI plots; areas for noise or artifacts are near zero.
- Output file path and format match the `--output` parameter (default 'resources/example/output/area.csv').

## Limitations

- Method currently supports only mzML file format; centroided and profile data are both accepted, but other formats (NetCDF, .raw) are not supported.
- Peak integration accuracy depends critically on the quality and calibration of the pre-trained model checkpoint (checkpoint0029.pth >300 MB); a corrupted or mismatched model will produce invalid boundaries.
- Numerical integration assumes the area under the curve is a valid proxy for peak intensity; highly skewed or multi-modal peaks within a single detected boundary may integrate incorrectly.
- The default confidence threshold (0.99) is strict and may exclude low-confidence but genuine peaks; tuning via the `--threshold` parameter is necessary for non-standard datasets.
- Smoothing (sigma > 0) can reduce noise but may artificially inflate or suppress peak areas; the trade-off must be evaluated per dataset.

## Evidence

- [other] Extract peak boundary coordinates (left and right edges) from the detection network predictions.: "Extract peak boundary coordinates (left and right edges) from the detection network predictions."
- [other] For each identified peak, integrate the area under the curve within the localized boundaries using numerical integration.: "For each identified peak, integrate the area under the curve within the localized boundaries using numerical integration."
- [other] Compile quantified peak areas and associated metadata into a structured output table.: "Compile quantified peak areas and associated metadata into a structured output table."
- [intro] train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries: "train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries"
- [readme] --threshold: Keep only predictions with 0.99 confidence.: "--threshold: Keep only predictions with 0.99 confidence."
- [readme] --smooth_sigma: Sigma value for smoothing.: "--smooth_sigma: Sigma value for smoothing."
- [readme] QuanFormer is a novel approach written in Python (v3.8.1) for peaks (aka features) detection and quantification in raw profile LC-MS data.: "QuanFormer is a novel approach written in Python (v3.8.1) for peaks (aka features) detection and quantification in raw profile LC-MS data."
