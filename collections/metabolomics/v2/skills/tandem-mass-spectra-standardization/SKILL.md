---
name: tandem-mass-spectra-standardization
description: Use when you have acquired raw tandem MS data from ProteomeXchange or vendor instruments in proprietary formats (e.g., Thermo .raw files) and need to perform comparative clustering benchmarks or quality assessments across multiple clustering tools.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3649
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - msconvert
  - ThermoRawFileParser
  - GNPS 2.0 Classical Networking Workflow
  - GNPS 2.0 PerScanSummarizer
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jproteome.4c00881
  title: MS-RT
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_rt_cq
    doi: 10.1021/acs.jproteome.4c00881
    title: MS-RT
  dedup_kept_from: coll_ms_rt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.4c00881
  all_source_dois:
  - 10.1021/acs.jproteome.4c00881
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tandem-mass-spectra-standardization

## Summary

Standardize raw vendor-specific tandem mass spectrometry data into canonical open formats (mzML or MGF) suitable for downstream clustering and benchmarking workflows. This skill bridges proprietary instrument outputs and reproducible metabolomics analysis pipelines.

## When to use

You have acquired raw tandem MS data from ProteomeXchange or vendor instruments in proprietary formats (e.g., Thermo .raw files) and need to perform comparative clustering benchmarks or quality assessments across multiple clustering tools. Standardization is required before cluster output formats can be canonicalized and metrics computed.

## When NOT to use

- Input data is already in mzML, MGF, or other open standardized mass spectrometry formats.
- Downstream analysis pipeline accepts vendor-specific formats natively and does not require cross-tool benchmarking.
- Raw instrument data is unavailable and only processed spectra libraries are provided.

## Inputs

- vendor-specific raw mass spectrometry files (e.g., Thermo .raw, vendor formats from ProteomeXchange)
- dataset identifiers or download locations from ProteomeXchange

## Outputs

- standardized mzML or MGF format files
- normalized cluster information tables with canonical column names (filename, scan, mass, rt_time, cluster)

## How to apply

Convert vendor-specific mass spectrometry data files into standardized open formats using tools like msconvert (ProteoWizard) or ThermoRawFileParser. For Thermo RAW files on Windows, use ThermoRawFileParser with format flag -f=1 for mzML or -f=0 for MGF output. On macOS/Linux, invoke via Mono. After conversion, verify that the resulting files contain required metadata fields (precursor m/z, retention time, scan identifiers) needed for cluster annotation. Post-processing scripts then normalize tool-specific output columns (e.g., '#Scan', '#ParentMass', '#RetTime', '#ClusterIdx' for msCluster) into a canonical schema ('filename', 'scan', 'mass', 'rt_time', 'cluster') before evaluation metrics are computed.

## Related tools

- **msconvert** (converts vendor-specific mass spectrometry formats to mzML or MGF using ProteoWizard toolkit) — http://proteowizard.sourceforge.net/download.html
- **ThermoRawFileParser** (cross-platform converter for Thermo RAW files to mzML or MGF without vendor software dependency) — https://github.com/compomics/ThermoRawFileParser
- **GNPS 2.0 Classical Networking Workflow** (processes mzML files and outputs standardized cluster information with required columns (filename, scan, mass, retention time, cluster index)) — https://gnps2.org/workflowinput?workflowname=classical_networking_workflow
- **GNPS 2.0 PerScanSummarizer** (extracts retention time information and scan metadata from mzML files for post-hoc merging with clustering results) — https://gnps2.org/workflowinput?workflowname=PerScanSummarizer

## Examples

```
ThermoRawFileParser.exe -i "C:\path\to\your_file.raw" -o "C:\path\to\output\folder" -f=1
```

## Evaluation signals

- Output file is readable and parses without errors in target analysis pipeline.
- Canonical output columns (filename, scan, mass, rt_time, cluster) are present and non-null for all rows.
- Converted mzML/MGF files retain precursor m/z, retention time, and scan identifiers without loss of precision.
- Post-processing scripts complete without data corruption and row counts match input expectations.
- Downstream clustering benchmarking script (Clustering_benchmark_MS_RT.py) executes successfully on standardized outputs without schema mismatch errors.

## Limitations

- Conversion quality depends on data integrity of source .raw files; corrupted vendor files may produce incomplete or invalid open-format outputs.
- ThermoRawFileParser on macOS/Linux requires Mono runtime, adding platform dependency and potential performance overhead.
- Retention time information must be separately extracted via GNPS 2.0 PerScanSummarizer for tools like MaRaCluster and merged manually; automated integration is not provided.
- Column name normalization across msCluster, Falcon, and MaRaCluster outputs requires tool-specific post-processing scripts; no unified converter is included in the repository.

## Evidence

- [readme] All datasets used in this project are publicly available and can be downloaded from ProteomeXchange, a globally coordinated initiative to facilitate the exchange and dissemination of proteomics data.: "All datasets used in this project are publicly available and can be downloaded from ProteomeXchange"
- [readme] To process the raw data files, they need to be converted into standard formats like mzML or MGF. We recommend using either msconvert or ThermoRawFileParser for this purpose.: "To process the raw data files, they need to be converted into standard formats like mzML or MGF"
- [readme] msconvert is a tool from the ProteoWizard toolkit that converts vendor-specific mass spectrometry data formats into open formats.: "msconvert is a tool from the ProteoWizard toolkit that converts vendor-specific mass spectrometry data formats into open formats"
- [readme] ThermoRawFileParser is a cross-platform tool for converting Thermo RAW files to mzML or MGF formats without the need for vendor software.: "ThermoRawFileParser is a cross-platform tool for converting Thermo RAW files to mzML or MGF formats without the need for vendor software"
- [other] Standardize cluster output formats to a canonical representation (e.g., cluster ID per spectrum).: "Standardize cluster output formats to a canonical representation (e.g., cluster ID per spectrum)"
- [readme] For msCluster, you can use any processing protocol as long as the output file has the following column names: 'filename': '#Filename', 'scan': '#Scan', 'mass': '#ParentMass', 'rt_time': '#RetTime', 'cluster': '#ClusterIdx': "output file has the following column names: 'filename': '#Filename', 'scan': '#Scan', 'mass': '#ParentMass', 'rt_time': '#RetTime', 'cluster': '#ClusterIdx'"
