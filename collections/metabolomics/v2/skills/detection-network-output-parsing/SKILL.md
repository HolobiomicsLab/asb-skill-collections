---
name: detection-network-output-parsing
description: Use when you have raw LC-MS data in mzML format with regions of interest (ROI) already identified, and a trained detection model (e.g., checkpoint0029.pth) has produced bounding box predictions with confidence scores.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - Python 3.8.1
  - QuanFormer
  - PyTorch
  - xcms (R package)
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c04531
  all_source_dois:
  - 10.1021/acs.analchem.4c04531
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# detection-network-output-parsing

## Summary

Extract peak boundary coordinates and confidence scores from a trained CNN-Transformer object detection network's output, then integrate the area under the curve within those boundaries for LC-MS peak quantification. This skill bridges neural network predictions to quantitative metabolomics measurements.

## When to use

You have raw LC-MS data in mzML format with regions of interest (ROI) already identified, and a trained detection model (e.g., checkpoint0029.pth) has produced bounding box predictions with confidence scores. Use this skill when you need to convert those detection predictions into quantified peak areas for targeted or untargeted metabolomics analysis.

## When NOT to use

- Input LC-MS data is not in mzML format; currently QuanFormer supports only .mzML.
- Peak detection and boundary localization have not yet been performed; you are starting from raw spectra without a pre-trained model.
- Detection confidence scores are systematically below your chosen threshold (default 0.99), indicating poor model performance on your data.

## Inputs

- Trained object detection model checkpoint (PyTorch .pth format, e.g., checkpoint0029.pth)
- Detection network predictions (bounding box coordinates and confidence scores)
- Raw LC-MS data in mzML format
- Regions of interest (ROI) as 2D images (m/z vs. retention time)
- Feature table or ROI metadata (m/z, retention time, compound name)

## Outputs

- Quantified peak area table (CSV) with columns: compound name, m/z, retention time, integrated area
- Optional: annotated ROI plots showing detected peak boundaries

## How to apply

Load the detection network checkpoint and run inference on ROI images extracted from LC-MS data. Extract predicted peak boundary coordinates (left and right edges) and filter predictions by a confidence threshold (default 0.99). For each peak passing the threshold, retrieve the corresponding m/z–retention time window from the raw data and perform numerical integration of intensity values within the localized boundaries. Compile the integrated areas into a structured CSV output table with compound names, m/z, retention time, and quantified peak area. The method supports both centroided and profile mzML data; for profile data, apply optional smoothing (smooth_sigma parameter) before integration to reduce noise.

## Related tools

- **QuanFormer** (Implements the CNN-Transformer object detection network and performs peak boundary localization and area integration from detection output) — https://github.com/LinShuhaiLAB/QuanFormer
- **PyTorch** (Deep learning framework used to load and run the trained detection model checkpoint)
- **xcms (R package)** (Optional: used in untargeted mode to perform centWave-based ROI extraction before detection-network-output-parsing)

## Examples

```
python main.py --ppm 10 --source resources/example/profile --feature resources/example/profile_feature.csv --images_path resources/example/profile_output --output resources/example/profile_output/area.csv --model resources/checkpoint0029.pth --threshold 0.99
```

## Evaluation signals

- All output peak areas are non-negative numeric values with no NaNs or infinities.
- Peak boundary coordinates are within the m/z and retention time ranges of the input ROI.
- Confidence scores of included peaks meet or exceed the specified threshold (default ≥ 0.99).
- Output CSV contains exactly one row per detected peak with all required columns (compound name, m/z, RT, area) populated.
- Quantified areas for known standards or spike-in compounds fall within expected ranges (e.g., linearity across concentration levels in validation experiments).

## Limitations

- Currently supports only mzML format; other LC-MS formats (NetCDF, .raw) are not compatible.
- Detection accuracy and boundary localization depend critically on the pre-trained model (checkpoint0029.pth); performance on data substantially different from training distribution (different instrument, ionization mode, or mass range) has not been characterized.
- Numerical integration assumes that ROI intensity values are already extracted and aligned; extreme noise or baseline distortion in profile data may require manual tuning of smooth_sigma parameter.
- Untargeted mode requires pre-installation of R (version 4.4.2 or later) and xcms (version 4.4.0) with its dependencies, adding complexity to deployment.
- No changelog is available, making it difficult to track improvements or bug fixes across versions.

## Evidence

- [intro] train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries to integrate the area: "train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries to integrate the area"
- [other] Extract peak boundary coordinates (left and right edges) from the detection network predictions. 3. For each identified peak, integrate the area under the curve within the localized boundaries using numerical integration. 4. Compile quantified peak areas and associated metadata into a structured output table.: "Extract peak boundary coordinates (left and right edges) from the detection network predictions. 3. For each identified peak, integrate the area under the curve within the localized boundaries using"
- [readme] Keep only predictions with 0.99 confidence.: "Keep only predictions with 0.99 confidence."
- [intro] The method is developed for high-resolution LC-MS data for metabolomics purposes, but it can also be applied to other detections that take peaks as the targets.: "The method is developed for high-resolution LC-MS data for metabolomics purposes, but it can also be applied to other detections that take peaks as the targets."
- [readme] quanformer can run in both  centroided and profile data: "quanformer can run in both  centroided and profile data"
- [readme] Sigma value for smoothing.: "Sigma value for smoothing."
