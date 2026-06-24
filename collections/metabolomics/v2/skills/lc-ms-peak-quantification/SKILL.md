---
name: lc-ms-peak-quantification
description: Use when after a CNN-Transformer peak detection model has been run on
  LC-MS ROI images and has output predicted peak locations with confidence scores.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python 3.8.1
  - QuanFormer
  - xcms / centWave
  techniques:
  - LC-MS
  license_tier: open
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

# LC-MS Peak Boundary Localization and Area Integration

## Summary

Localize peak boundaries from a trained CNN-Transformer object detection network's predictions on LC-MS regions of interest (ROI), then numerically integrate the area under the curve within those boundaries to quantify peak abundance. This skill bridges detection confidence scores to quantitative metabolite measurements in raw or centroided mzML data.

## When to use

After a CNN-Transformer peak detection model has been run on LC-MS ROI images and has output predicted peak locations with confidence scores. Apply this skill when you need to convert bounding-box predictions into quantitative peak areas for targeted or untargeted metabolomics workflows on high-resolution LC-MS data.

## When NOT to use

- Input is already a feature table with pre-computed peak areas — skip directly to statistical analysis or normalization.
- Detection network predictions have not been generated or confidence scores are unavailable — run the detection step first.
- Low-resolution or heavily noisy LC-MS data where peak boundaries cannot be reliably localized by the CNN-Transformer model — consider pre-processing or model retraining.

## Inputs

- CNN-Transformer detection network predictions (peak locations, confidence scores, bounding-box coordinates)
- mzML file or centroided LC-MS data
- ROI images or extracted chromatographic regions with intensity values

## Outputs

- Quantified peak areas (numerical values per peak)
- Structured output CSV table with columns: Compound Name, m/z, Retention Time, Peak Area, File Name

## How to apply

Load the detection network's output containing predicted peak locations and confidence scores. Filter predictions by a confidence threshold (default 0.99 in QuanFormer) to retain only high-confidence detections. Extract the left and right boundary coordinates for each peak from the bounding-box predictions. For each localized peak, numerically integrate the intensity values (m/z signal) within those boundaries to obtain the integrated peak area. Compile the quantified areas and associated metadata (compound name, m/z, retention time, file name) into a structured CSV output table. The integration step treats the localized peak region as a 1D or 2D numerical integration problem over the intensity signal within the predicted boundaries.

## Related tools

- **QuanFormer** (CNN-Transformer-based object detection network that generates peak boundary predictions and confidence scores for mzML LC-MS data; implements the peak localization and area integration workflow) — https://github.com/LinShuhaiLAB/QuanFormer
- **xcms / centWave** (Alternative peak detection algorithm (used in untargeted mode) that can precede or complement the CNN-Transformer predictions for ROI identification)

## Examples

```
python main.py --ppm 10 --source resources/example/profile --feature resources/example/profile_feature.csv --images_path resources/example/profile_output --output resources/example/profile_output/area.csv --model resources/checkpoint0029.pth --threshold 0.99
```

## Evaluation signals

- Output CSV contains no null or negative peak area values; all areas are positive real numbers.
- Number of quantified peaks matches the number of high-confidence (≥ threshold) predictions after filtering.
- Peak boundaries (left and right coordinates) are within the spatial extent of the original ROI image or chromatographic region.
- Integrated areas are proportional to visual peak height and width in plotted ROI images (when --plot=True).
- Quantified areas for replicate analysis of the same compound are reproducible (low coefficient of variation across replicates).

## Limitations

- Accuracy depends critically on the pre-trained CNN-Transformer detection model checkpoint; poor model quality or domain shift (different instrument, ionization mode, or matrix) will degrade boundary localization.
- Confidence threshold (default 0.99) is a hyperparameter that must be tuned per dataset; overly stringent thresholds may miss true peaks, while lenient thresholds may retain false positives.
- Numerical integration method and smoothing (sigma parameter, default 0) are not fully detailed in the README; results may vary with different interpolation or smoothing strategies.
- Currently supports only mzML format; other formats (NetCDF, .raw) must be converted before use.
- Computational performance scales with the number of processes (default 1); untargeted mode with centWave ROI search requires additional R environment configuration and can be time-consuming.

## Evidence

- [intro] train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries: "train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries"
- [other] Load the detection network output containing predicted peak locations and confidence scores from the CNN-Transformer model. Extract peak boundary coordinates (left and right edges) from the detection network predictions. For each identified peak, integrate the area under the curve within the localized boundaries using numerical integration.: "Load the detection network output containing predicted peak locations and confidence scores from the CNN-Transformer model. Extract peak boundary coordinates (left and right edges) from the detection"
- [readme] Keep only predictions with 0.99 confidence.: "Keep only predictions with 0.99 confidence."
- [other] Compile quantified peak areas and associated metadata into a structured output table.: "Compile quantified peak areas and associated metadata into a structured output table."
- [readme] QuanFormer is a novel approach written in Python (v3.8.1) for peaks (aka features) detection and quantification in raw profile LC-MS data.: "QuanFormer is a novel approach written in Python (v3.8.1) for peaks (aka features) detection and quantification in raw profile LC-MS data."
