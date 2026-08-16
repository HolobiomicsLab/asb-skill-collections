---
name: metabolomics-feature-preprocessing
description: Use when when you have raw profile LC-MS data in .mzML format and need
  to prepare regions of interest (ROI) as input for a CNN-Transformer peak detection
  network.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - QuanFormer
  - Python (v3.8.1+)
  - PyTorch (v1.13.1)
  - R xcms (v4.4.0+)
  techniques:
  - LC-MS
  - direct-infusion-MS
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

# metabolomics-feature-preprocessing

## Summary

Preparation of raw profile LC-MS data in .mzML format into image-like ROI tensors suitable for CNN-Transformer peak detection networks. This skill bridges raw mass spectrometry acquisition and deep learning-based feature quantification by parsing chromatograms, segmenting candidate peaks, and formatting data into standardized tensor representations.

## When to use

When you have raw profile LC-MS data in .mzML format and need to prepare regions of interest (ROI) as input for a CNN-Transformer peak detection network. Specifically: (1) your raw data contains profile (not centroided) ion chromatograms and mass spectra, (2) you have either a feature table (targeted mode with known m/z and RT) or wish to detect features de novo (untargeted mode), and (3) you need to convert candidate peak regions into fixed-size image tensors for neural network inference.

## When NOT to use

- Input data is already centroided (not profile); use centroided-specific preprocessing instead.
- Input is in a non-mzML format (e.g., raw vendor format, NetCDF) without prior conversion to .mzML.
- You have a pre-computed feature table with quantified peak areas; this skill is for raw data ingestion and ROI preparation, not for post-detection analysis.

## Inputs

- Raw profile LC-MS data in .mzML format
- Feature table (CSV with columns: Compound Name, m/z, RT) for targeted mode, or empty/omitted for untargeted mode
- Trained CNN-Transformer detection model checkpoint (.pth file)

## Outputs

- ROI image tensors formatted for CNN-Transformer input
- Verified ROI metadata (m/z, RT, pixel coordinates)
- ROI visualization plots (optional, for QC)

## How to apply

First, parse the raw .mzML file using a dedicated mzML reader to extract ion chromatogram and mass spectrometry profile data. Second, segment the profile LC-MS data into candidate regions of interest (ROIs) containing potential peaks: in targeted mode, use m/z tolerance (default 10 ppm) and retention time windows around known features; in untargeted mode, apply the centWave algorithm with parameters such as minWidth (default 5), maxWidth (default 50), signal-to-noise threshold (default 5), and noise level (default 100). Third, format each ROI as an image-like tensor by normalizing intensity values and padding to match the detection network's input dimensions. Finally, verify that ROI tensor dimensions, data types (typically float32), and value ranges conform to the CNN-Transformer input specifications before inference. PPM tolerance and peak width parameters should be tuned based on your instrument resolution and expected metabolite peak characteristics.

## Related tools

- **QuanFormer** (End-to-end framework orchestrating .mzML parsing, ROI segmentation, tensor formatting, and CNN-Transformer peak detection inference) — https://github.com/LinShuhaiLAB/QuanFormer
- **Python (v3.8.1+)** (Runtime environment for .mzML I/O, array operations (NumPy), and tensor construction)
- **PyTorch (v1.13.1)** (Deep learning framework for loading pre-trained model checkpoint and tensor operations)
- **R xcms (v4.4.0+)** (centWave algorithm implementation for untargeted ROI detection in profile LC-MS data)

## Examples

```
python main.py --ppm 10 --source resources/example/profile --feature resources/example/profile_feature.csv --images_path resources/example/profile_output --output resources/example/profile_output/area.csv --model resources/checkpoint0029.pth
```

## Evaluation signals

- ROI tensor shape matches model input specification (e.g., [batch, channels, height, width]) and data type is float32.
- All ROI intensity values fall within expected normalized range (typically [0, 1] or [-1, 1]) with no NaN or Inf values.
- Targeted mode: every feature in the input CSV is represented by exactly one ROI tensor centered at the specified m/z ± ppm and RT.
- Untargeted mode: generated ROI list contains no duplicate peaks (verified by m/z and RT clustering with default tolerance).
- ROI visualization plots show expected chromatographic peak shapes (Gaussian-like in m/z and RT dimensions) with no artifacts or empty tensor regions.

## Limitations

- Requires R environment (v4.4.2+) and xcms (v4.4.0+) installed for untargeted mode centWave feature detection; targeted mode does not have this dependency.
- Performance is sensitive to PPM tolerance and peak width parameters; suboptimal settings may generate overlapping ROIs or miss narrow peaks.
- The method has been validated on high-resolution LC-MS data for metabolomics; applicability to other mass spectrometry modalities (e.g., MALDI, direct infusion) is stated as potential but not demonstrated.
- Large .mzML files (>1 GB) may require substantial memory for full chromatogram parsing; multi-processing (via --processes_number parameter) can mitigate this but is not always available on all platforms.
- Checkpoint file (checkpoint0029.pth) must be >300 MB; corrupted or undersized weights will cause inference failures.

## Evidence

- [other] Parse raw .mzML file using mzML reader to extract ion chromatogram and mass spectrometry profile data. Segment profile LC-MS data into candidate regions of interest (ROIs) containing potential peaks. Format ROI data as image-like tensors compatible with CNN-Transformer input requirements.: "1. Parse raw .mzML file using mzML reader to extract ion chromatogram and mass spectrometry profile data. 2. Segment profile LC-MS data into candidate regions of interest (ROIs) containing potential"
- [readme] train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries: "train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries"
- [readme] Type of raw data files, currently only supports the mzML format.: "Type of raw data files, currently only supports the mzML format."
- [readme] PPM value for ROI extraction. [...] Polarity. [...] Min peak width [...] Max peak width. [...] Signal-to-noise ratio.: "PPM value for ROI extraction. [...] Polarity. [...] Min peak width [...] Max peak width. [...] Signal-to-noise ratio."
- [readme] Keep only predictions with 0.99 confidence.: "Keep only predictions with 0.99 confidence."
- [readme] if running the targeted quantification, you should prepare the feature.csv file in the following format, else ignore this step: "if running the targeted quantification, you should prepare the feature.csv file in the following format, else ignore this step"
