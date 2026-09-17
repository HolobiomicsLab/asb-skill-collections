---
name: mass-spectrometry-chromatogram-extraction
description: Use when you have raw profile LC-MS data in .mzML format and need to
  prepare candidate peak regions for classification by a neural network detector (e.g.,
  QuanFormer).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - QuanFormer
  - mzML reader
  - xcms (centWave algorithm)
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# mass-spectrometry-chromatogram-extraction

## Summary

Extract ion chromatograms and mass spectrometry profile data from raw .mzML files as the foundational step for peak detection in LC-MS metabolomics workflows. This skill prepares unprocessed profile LC-MS data into segmented regions of interest (ROI) suitable for downstream machine-learning-based peak classification.

## When to use

You have raw profile LC-MS data in .mzML format and need to prepare candidate peak regions for classification by a neural network detector (e.g., QuanFormer). Use this skill when your goal is to identify true peaks versus false peaks within user-defined m/z and retention time windows, or to discover peaks in an untargeted manner using centWave-derived ROI candidates.

## When NOT to use

- Input is already a centroided (non-profile) feature table or a pre-processed peak list — use this skill only on raw profile LC-MS data.
- You need quantification results directly — this skill produces only ROI candidates; you must apply peak detection and boundary localization downstream.
- Your file format is not .mzML (e.g., raw vendor format, NetCDF, mzXML) — QuanFormer currently supports only .mzML.

## Inputs

- Raw .mzML file (profile LC-MS data)
- Feature table (CSV with compound name, m/z, and retention time for targeted mode, optional)
- PPM tolerance value (integer, default 10)
- Peak width range parameters for untargeted mode (minWidth, maxWidth integers)
- Signal-to-noise and noise threshold parameters (integers, defaults s2n=5, noise=100)

## Outputs

- Segmented ROI tensors (image-like 2D arrays: m/z × retention time intensity matrices)
- ROI metadata (m/z center, retention time center, width, height per ROI)
- Optionally: visualized ROI plots (PNG/image files if roi_plot=True)

## How to apply

Parse the raw .mzML file using an mzML reader to extract the ion chromatogram and mass spectrometry profile data across the full m/z and retention time dimensions. Segment the profile data into candidate ROIs by either (1) targeted mode: extracting windows around known m/z and retention time coordinates with a PPM tolerance (default 10 ppm), or (2) untargeted mode: applying the centWave algorithm with user-specified peak width (minWidth, maxWidth), signal-to-noise ratio (s2n), noise threshold, and m/z difference parameters. Format each ROI as an image-like tensor with dimensions and data types compatible with CNN-Transformer input specifications (typically a 2D intensity matrix indexed by m/z and retention time bins). Verify tensor shape consistency and absence of NaN or out-of-range values before passing to the detection network.

## Related tools

- **QuanFormer** (Main framework that ingests extracted ROI tensors and applies CNN-Transformer detection and boundary localization) — https://github.com/LinShuhaiLAB/QuanFormer
- **mzML reader** (Parses raw .mzML files to extract ion chromatogram and profile MS data)
- **xcms (centWave algorithm)** (Untargeted ROI detection via peak-finding in profile LC-MS data; requires R 4.4.2+ and Bioconductor) — https://www.bioconductor.org/packages/release/bioc/html/xcms.html

## Examples

```
python main.py --ppm 10 --source resources/example/profile --feature resources/example/profile_feature.csv --images_path resources/example/profile_output --output resources/example/profile_output/area.csv --model resources/checkpoint0029.pth
```

## Evaluation signals

- Tensor dimensions match CNN-Transformer input specification (verify shape consistency across all ROIs)
- No NaN, Inf, or out-of-range intensity values in output tensors; data type is float32 or compatible numeric type
- ROI bounding boxes do not exceed m/z and retention time bounds of the input raw file
- In targeted mode: all ROIs are centered within ±PPM tolerance of their respective feature m/z; retention time centers match provided coordinates
- In untargeted mode: ROI count and positions are reproducible across repeated runs; visual ROI plots (if generated) show coherent intensity peaks aligned with expected m/z and retention time

## Limitations

- Currently supports only .mzML format; other vendor formats or NetCDF require prior conversion.
- PPM tolerance and peak width parameters are user-specified; incorrect settings may cause missed peaks or excessive false candidates.
- Untargeted mode requires R 4.4.2+, Bioconductor xcms 4.4.0+, and additional R dependencies; installation can be complex on some systems.
- Profile data with extreme baseline noise or very low signal-to-noise may produce ROIs that fail detection downstream; the skill does not validate SNR a priori.
- Large .mzML files (>2 GB) may consume substantial memory during chromatogram extraction and ROI segmentation.

## Evidence

- [other] Parse raw .mzML file using mzML reader to extract ion chromatogram and mass spectrometry profile data.: "Parse raw .mzML file using mzML reader to extract ion chromatogram and mass spectrometry profile data."
- [other] Segment profile LC-MS data into candidate regions of interest (ROIs) containing potential peaks.: "Segment profile LC-MS data into candidate regions of interest (ROIs) containing potential peaks."
- [other] Format ROI data as image-like tensors compatible with CNN-Transformer input requirements.: "Format ROI data as image-like tensors compatible with CNN-Transformer input requirements."
- [other] Verify ROI tensor dimensions and data types match detection network specifications.: "Verify ROI tensor dimensions and data types match detection network specifications."
- [readme] Type of raw data files, currently only supports the mzML format.: "Type of raw data files, currently only supports the mzML format."
- [readme] PPM value for ROI extraction.: "PPM value for ROI extraction."
- [readme] train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries: "train object detection network combining CNN and Transformer to identify the peaks in ROI (to judge whether it is a true peak or a false peak) and locate the peak boundaries"
