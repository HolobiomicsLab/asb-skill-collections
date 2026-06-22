---
name: lc-ms-roi-annotation-interpretation
description: Use when when you have extracted LC-MS ROI windows (m/z × retention time snippets) from raw mzML data and need to distinguish genuine metabolite peaks from noise or artifacts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - QuanFormer
  - PyTorch
  - xcms (R package)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# LC-MS ROI Annotation and Interpretation

## Summary

Train and deploy a hybrid CNN-Transformer object detection network to classify candidate peaks in LC-MS regions of interest (ROIs) as true or false peaks and localize their boundaries. This skill enables quantitative peak detection and area integration in high-resolution LC-MS data for metabolomics.

## When to use

When you have extracted LC-MS ROI windows (m/z × retention time snippets) from raw mzML data and need to distinguish genuine metabolite peaks from noise or artifacts. Apply this skill in targeted quantification workflows where you have a feature list (compound name, m/z, RT), or in untargeted discovery after centWave peak picking has generated candidate ROI regions. Use when ROI-level binary classification and precise peak boundary coordinates are required for area integration.

## When NOT to use

- Input is already a centroided feature table or quantification matrix — use this skill only on raw profile data or extracted ROI windows, not pre-processed peak lists.
- ROI windows have not been extracted or candidates have not been identified — centWave or equivalent ROI extraction must precede model inference.
- The LC-MS data is in a format other than mzML — QuanFormer supports only mzML at present.

## Inputs

- mzML file (raw or centroided LC-MS profile data)
- feature.csv (targeted mode): columns [Compound Name, mz, RT]
- Extracted ROI windows (m/z × RT regions of interest as tensor or image data)

## Outputs

- Peak classification predictions (binary: true/false peak per ROI)
- Peak boundary coordinates (start/end m/z and RT positions)
- Integrated peak areas (area.csv output file)
- Annotated ROI plots (optional visualization)

## How to apply

Load the pre-trained CNN-Transformer model checkpoint (default: checkpoint0029.pth, >300 MB) and process ROI windows through the hybrid encoder: convolutional layers extract local spectral features from the mass chromatogram window while transformer layers capture long-range m/z and RT dependencies. The model outputs two heads: (1) binary classification logits (true vs. false peak) and (2) boundary box coordinates (peak start/end positions). Apply a confidence threshold (default 0.99) to filter predictions, keeping only high-confidence detections. For targeted mode, provide a feature.csv with columns [Compound Name, mz, RT] to focus analysis on known targets with PPM tolerance (default 10 ppm). For untargeted mode, run centWave peak picking first to generate candidate ROIs, then pass them through the model. Visualize ROIs and predictions by setting --roi_plot and --plot to True on first use to validate preprocessing.

## Related tools

- **QuanFormer** (Pre-trained CNN-Transformer model for peak detection and boundary localization; implements the object detection network and provides checkpoint0029.pth model weights.) — https://github.com/LinShuhaiLAB/QuanFormer
- **PyTorch** (Deep learning framework for loading and executing the CNN-Transformer model; required version 1.13.1+cu117 or compatible.)
- **xcms (R package)** (Implements centWave algorithm for untargeted ROI candidate generation; optional for untargeted mode workflows.) — https://www.bioconductor.org/packages/release/bioc/html/xcms.html

## Examples

```
python main.py --ppm 10 --source resources/example/profile --feature resources/example/profile_feature.csv --images_path resources/example/profile_output --output resources/example/profile_output/area.csv --model resources/checkpoint0029.pth
```

## Evaluation signals

- Output confidence scores exceed the specified threshold (default 0.99); predictions below threshold are filtered and logged.
- Peak boundary coordinates are physically plausible: start < end in both m/z and RT dimensions; boundaries align with visible signal in the ROI image.
- Integrated peak areas (from area.csv) are non-negative and match the spatial extent of predicted boundaries; areas scale proportionally with ROI signal intensity.
- Visualized predictions (when --plot=True) show peak boundaries overlaid on ROI images; false positives should be rare and true peaks should be centered within predicted boxes.
- Targeted mode predictions match expected m/z (within ±PPM tolerance, default ±10 ppm) and RT windows of queried compounds in feature.csv.

## Limitations

- Model is trained on high-resolution LC-MS data for metabolomics; applicability to other mass spectrometry instruments or different m/z ranges is not validated.
- Requires pre-trained checkpoint (checkpoint0029.pth, >300 MB); re-training workflow for new datasets is not provided in the README.
- Untargeted mode depends on R environment and xcms package installation; dependency installation can be error-prone, particularly on Windows or macOS.
- Performance on centroided data is supported but is primarily optimized for profile (raw) LC-MS data; centroided spectra may have reduced localization accuracy.
- No changelog or version history provided; model stability and reproducibility across updates cannot be assessed.

## Evidence

- [readme] QuanFormer is a novel approach written in Python (v3.8.1) for peaks (aka features) detection and quantification in raw profile LC-MS data.: "QuanFormer is a novel approach written in Python (v3.8.1) for peaks (aka features) detection and quantification in raw profile LC-MS data."
- [readme] train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries: "train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries"
- [intro] convolutional layers extract local spectral features from ROI windows and transformer layers capture long-range dependencies in the mass chromatogram signal: "convolutional layers extract local spectral features from ROI windows and transformer layers capture long-range dependencies in the mass chromatogram signal"
- [intro] Implement or adapt a standard object detection loss function (e.g., cross-entropy for classification, smooth L1 or focal loss for boundary regression) combining both tasks.: "cross-entropy for classification, smooth L1 or focal loss for boundary regression"
- [readme] Keep only predictions with 0.99 confidence.: "Keep only predictions with 0.99 confidence."
- [readme] if running the targeted quantification, you should prepare the feature.csv file in the following format: Compound Name (numbers, unique), mz, RT: "feature.csv contains the following columns: 1. Compound Name(numbers, unique) 2. mz 3. RT"
- [readme] PPM value for ROI extraction. Default Value: 10: "PPM value for ROI extraction. Default Value: 10"
- [readme] Note: Make sure checkpoint0029.pth in /resources/ is normal (>300MB): "Make sure *checkpoint0029.pth* in /resources/ is normal (>300MB)"
