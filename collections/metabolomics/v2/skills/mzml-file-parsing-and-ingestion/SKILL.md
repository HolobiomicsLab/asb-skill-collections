---
name: mzml-file-parsing-and-ingestion
description: Use when you have raw profile LC-MS data in .mzML format and need to
  prepare it for targeted or untargeted peak detection.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0580
  - http://edamontology.org/topic_3370
  tools:
  - Python
  - QuanFormer
  - xcms (via R/Bioconductor)
  - PyArrow / pandas
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

# mzML File Parsing and Ingestion

## Summary

Parse raw profile LC-MS data in mzML format and extract ion chromatogram and mass spectrometry profile data as structured input for peak detection workflows. This skill is essential for preparing unprocessed LC-MS files into analyzable ROI tensors compatible with CNN-Transformer detection networks.

## When to use

You have raw profile LC-MS data in .mzML format and need to prepare it for targeted or untargeted peak detection. Use this skill when starting a QuanFormer workflow or any peak detection pipeline that requires extraction of ion chromatogram and profile mass spectrometry data before ROI segmentation and model inference.

## When NOT to use

- Input data is already in centroided (not profile) format and centroided-specific processing is not required by your workflow
- Raw data is in a non-mzML format (e.g., NetCDF, Bruker .d) without prior conversion
- Peak boundaries and areas have already been computed; ingestion is only needed at the raw data stage

## Inputs

- .mzML file (raw profile LC-MS data)
- feature.csv file (for targeted mode: compound name, m/z, RT columns)
- centWave algorithm parameters (for untargeted mode: polarity, minWidth, maxWidth, s2n, noise, mzDiff, prefilter)
- PPM tolerance value (default 10)

## Outputs

- Parsed ion chromatogram data
- Parsed mass spectrometry profile data
- Segmented regions of interest (ROI) as 3D tensors
- ROI metadata (m/z, RT, intensity bounds)
- Formatted tensor stack compatible with CNN-Transformer input

## How to apply

Use a dedicated mzML reader (e.g., integrated within QuanFormer's Python pipeline) to parse the .mzML file and extract both ion chromatogram and mass spectrometry profile data. Set the PPM tolerance parameter (default 10 ppm) to control m/z-based ROI extraction precision. If performing targeted quantification, provide a feature.csv file with compound name, m/z, and retention time (RT); otherwise, run untargeted mode using centWave algorithm parameters (polarity, minWidth, maxWidth, s2n, noise, mzDiff, prefilter). Segment the extracted profile data into candidate regions of interest (ROIs) using the specified ppm window. Format ROI data as image-like tensors with verified dimensions and data types matching the detection network input specification (typically expecting 3D tensors compatible with CNN input layers). Verify tensor dimensions and dtype consistency before passing to the detection model.

## Related tools

- **QuanFormer** (Integrated Python package providing mzML parsing, ROI segmentation, and tensor formatting for LC-MS peak detection) — https://github.com/LinShuhaiLAB/QuanFormer
- **xcms (via R/Bioconductor)** (Provides centWave algorithm for untargeted ROI feature detection when feature.csv is not supplied)
- **PyArrow / pandas** (Utility for reading and validating feature.csv input tables in targeted mode)

## Examples

```
python main.py --ppm 10 --source resources/example/profile --feature resources/example/profile_feature.csv --images_path resources/example/profile_output --output resources/example/profile_output/area.csv --model resources/checkpoint0029.pth
```

## Evaluation signals

- Extracted ion chromatogram and profile data dimensions match expected mzML structure (e.g., m/z array length, retention time points, intensity values are numeric and non-null)
- ROI tensor shape matches detection network input spec (typically [batch, channels, height, width] for 2D ROI images or [batch, channels, mz_bins, rt_bins] for LC-MS)
- All ROI tensors have consistent dtype (float32 or specified precision) and no NaN or infinite values outside expected regions
- PPM-based m/z window boundaries are correctly computed (±ppm/1e6 × m/z_value) for each feature in targeted mode
- Feature.csv parsing succeeds with no missing required columns (Compound Name, mz, RT) when in targeted mode, or centWave parameters are all numeric and within valid ranges for untargeted mode

## Limitations

- Currently supports only .mzML format; other LC-MS formats (NetCDF, mzXML, proprietary .d) require prior conversion
- Profile data parsing assumes standard mzML encoding; non-standard or corrupted mzML files may cause parsing failures
- ROI tensor formatting assumes rectangular 2D image representation; highly irregular or fragmented peak shapes may require manual preprocessing
- Untargeted mode requires R ≥4.4.2 and Bioconductor xcms ≥4.4.0 to be installed and properly configured; missing dependencies will trigger 'FileNotFoundError' for xcms_peak_list.csv
- PPM tolerance and centWave algorithm parameters are data-dependent; values that work for one instrument/sample type may require tuning for others

## Evidence

- [other] Parse raw .mzML file using mzML reader to extract ion chromatogram and mass spectrometry profile data.: "Parse raw .mzML file using mzML reader to extract ion chromatogram and mass spectrometry profile data"
- [other] Segment profile LC-MS data into candidate regions of interest (ROIs) containing potential peaks.: "Segment profile LC-MS data into candidate regions of interest (ROIs) containing potential peaks"
- [other] Format ROI data as image-like tensors compatible with CNN-Transformer input requirements.: "Format ROI data as image-like tensors compatible with CNN-Transformer input requirements"
- [other] Verify ROI tensor dimensions and data types match detection network specifications.: "Verify ROI tensor dimensions and data types match detection network specifications"
- [readme] Type of raw data files, currently only supports the mzML format.: "Type of raw data files, currently only supports the mzML format"
- [readme] feature.csv contains the following columns: 1. Compound Name(numbers, unique) 2. mz 3. RT: "feature.csv contains the following columns: 1. Compound Name(numbers, unique) 2. mz 3. RT"
- [readme] PPM value for ROI extraction.: "PPM value for ROI extraction"
- [readme] If it is not empty, the targeted mode will be used. If it is empty, it is the untargeted mode, and the parameters required for the untargeted mode need to be set.: "If it is not empty, the targeted mode will be used. If it is empty, it is the untargeted mode, and the parameters required for the untargeted mode need to be set"
