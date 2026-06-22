---
name: peak-boundary-localization
description: Use when after you have (1) extracted regions of interest (ROIs) around candidate peaks in LC-MS data and (2) run those ROIs through a trained CNN-Transformer peak detection model that outputs both binary peak classifications and bounding box coordinates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python 3.8.1
  - Python
  - QuanFormer
  - PyTorch
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

# peak-boundary-localization

## Summary

Extract peak boundary coordinates (left and right edges) from a trained CNN-Transformer object detection network's predictions on LC-MS regions of interest, then numerically integrate the area under the curve within those boundaries to quantify peak intensity. This skill bridges detected peak locations and quantitative measurements in metabolomics workflows.

## When to use

Apply this skill after you have (1) extracted regions of interest (ROIs) around candidate peaks in LC-MS data and (2) run those ROIs through a trained CNN-Transformer peak detection model that outputs both binary peak classifications and bounding box coordinates. Use it when you need to convert raw detection outputs into quantitative peak areas for downstream metabolite identification or comparative analysis.

## When NOT to use

- Input is already a processed feature table with pre-computed peak areas — skip directly to statistical analysis.
- Detection model has not been trained or checkpoint is not available — train or obtain the model first using the reconstruction workflow.
- ROI extraction has not been performed — run ROI extraction from raw mzML data prior to applying this skill.

## Inputs

- Detection network predictions containing peak confidence scores and boundary coordinates
- ROI-extracted LC-MS chromatogram signal values (intensity array) for each region
- Confidence threshold value (numeric, default 0.99)
- Optional: feature metadata (compound name, m/z, retention time) for targeted quantification

## Outputs

- Quantified peak areas (numeric values)
- Peak boundary coordinates (start and end m/z or retention time positions)
- Associated metadata table (CSV format) with compound identifiers, m/z, retention time, and integrated area

## How to apply

Load the detection network output containing predicted peak locations and confidence scores from the CNN-Transformer model checkpoint. Filter predictions by confidence threshold (default 0.99 in QuanFormer) to retain only high-confidence peaks. For each prediction that passes filtering, extract the peak start and end position coordinates from the boundary localization head outputs. Apply numerical integration (e.g., Simpson's rule or trapezoidal rule) to compute the area under the chromatogram curve between the left and right boundaries. Compile the quantified peak areas and associated metadata (m/z, retention time, compound name if targeted mode) into a structured output table (CSV or similar). The integration should respect the original signal intensity values within the localized window.

## Related tools

- **QuanFormer** (Implements the CNN-Transformer detection network and provides the trained checkpoint (checkpoint0029.pth) for generating boundary predictions; also provides the numerical integration and output compilation routine.) — https://github.com/LinShuhaiLAB/QuanFormer
- **PyTorch** (Underlying deep learning framework for loading the trained detection model and executing forward passes to generate boundary predictions.)

## Examples

```
python main.py --ppm 10 --source resources/example/profile --feature resources/example/profile_feature.csv --images_path resources/example/profile_output --output resources/example/profile_output/area.csv --model resources/checkpoint0029.pth --threshold 0.99
```

## Evaluation signals

- Confidence score check: all retained predictions meet or exceed the threshold (e.g., ≥0.99); filtered predictions are consistently excluded.
- Boundary coordinate validity: left boundary < right boundary for every peak; coordinates fall within the expected ROI window range.
- Area integration sanity: integrated areas are positive and fall within expected intensity ranges for the data; extreme outliers (very small or very large) warrant visual inspection of the ROI.
- Schema conformance: output table contains all required columns (compound name, m/z, RT, peak area) with correct data types; no missing or NaN values in core fields.
- Reproducibility check: re-running with the same model checkpoint and threshold produces identical results; stochasticity should be absent for deterministic operations (unless smoothing is applied).

## Limitations

- Peak boundary predictions depend on the quality of the trained detection model; model performance is limited to the mass range and peak types seen during training (method was developed for high-resolution LC-MS metabolomics data but generalization to other peak targets is possible).
- Numerical integration accuracy depends on signal smoothing and sampling resolution; noisy or under-sampled ROIs may produce unreliable area estimates.
- Confidence threshold (e.g., 0.99) is a hard cutoff; borderline predictions (e.g., confidence 0.98) are discarded without recourse, potentially missing true low-intensity peaks.
- Method assumes that boundary coordinates output by the detection head align properly with the underlying chromatogram intensity axis; misalignment or coordinate system mismatch will produce incorrect areas.
- Currently supports only .mzML input format; other raw data formats (e.g., .raw, .d) must be converted upstream.

## Evidence

- [other] Extract peak boundary coordinates (left and right edges) from the detection network predictions.: "Extract peak boundary coordinates (left and right edges) from the detection network predictions."
- [other] For each identified peak, integrate the area under the curve within the localized boundaries using numerical integration.: "For each identified peak, integrate the area under the curve within the localized boundaries using numerical integration."
- [other] Compile quantified peak areas and associated metadata into a structured output table.: "Compile quantified peak areas and associated metadata into a structured output table."
- [readme] Keep only predictions with 0.99 confidence.: "Keep only predictions with 0.99 confidence."
- [readme] train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries: "train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries"
