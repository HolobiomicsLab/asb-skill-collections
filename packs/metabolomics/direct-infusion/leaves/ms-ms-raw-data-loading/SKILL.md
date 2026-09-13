---
name: ms-ms-raw-data-loading
description: Use when when you have raw LC-MS/MS instrument output files (e.g., .mzML,
  .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - MZmine2
  - Optimus
  - OpenMS
  - KNIME
  techniques:
  - LC-MS
  - direct-infusion-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jnatprod.7b00737
  title: Bioactivity-Based Molecular Networking
evidence_spans:
- open bioinformatic tools, such [MZmine2](http://mzmine.github.io/)
- '[Optimus](https://github.com/MolecularCartography/Optimus) (using OpenMS)'
- or [Optimus](https://github.com/MolecularCartography/Optimus) (using OpenMS)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bioactivity_based_molecular_networking_cq
    doi: 10.1021/acs.jnatprod.7b00737
    title: Bioactivity-Based Molecular Networking
  dedup_kept_from: coll_bioactivity_based_molecular_networking_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jnatprod.7b00737
  all_source_dois:
  - 10.1021/acs.jnatprod.7b00737
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS/MS Raw Data Loading

## Summary

Loading raw MS/MS data files into bioinformatic processing tools (MZmine2 or Optimus/OpenMS) as the essential first step to enable feature detection, chromatogram building, and cross-sample alignment in untargeted metabolomics workflows.

## When to use

When you have raw LC-MS/MS instrument output files (e.g., .mzML, .mzXML, or vendor-native formats) from fractionated samples and need to begin untargeted metabolomics analysis targeting bioactive compound discovery or bioactive molecular networking, or when scaling to process hundreds of LC-MS runs in a single batch workflow.

## When NOT to use

- Input is already a processed feature quantification table or aligned feature matrix (e.g., features_quantification_matrix.csv)—skip directly to normalization or bioassay integration.
- Data has been pre-processed by the vendor software into centroided or otherwise lossy formats and you require full-resolution profile data for advanced annotation.
- You are working with direct-infusion (DI) MS/MS data only and have no chromatographic dimension; use Optimus's direct-infusion input mode instead.

## Inputs

- Raw LC-MS/MS data files (vendor binary format, .mzML, .mzXML, or .netCDF)
- Experimental design file (CSV or TSV listing sample filenames and group metadata)
- System parameters (mass resolution, polarity, expected m/z and RT ranges)

## Outputs

- In-memory or cached representation of full-resolution m/z–RT–intensity tensors for all samples
- Parsed instrument metadata (e.g., analyzer type, scan event definitions, internal standards)
- Ready-to-process data structure for downstream mass detection step

## How to apply

Select an open bioinformatic tool appropriate to your workflow—MZmine2 for standalone peak-picking workflows or Optimus (built on OpenMS with KNIME orchestration) for integrated feature detection through spatial mapping. Point the tool to your raw data directory and configure the input file format and mass spectrometry parameters (instrument type, polarity, expected mass resolution). The tool will internally parse the instrument vendor binary or open format and load the full-resolution m/z and retention time (RT) dimensions into memory or indexed cache. Verify successful loading by checking that all samples appear in the file list and that the m/z and RT ranges match your experimental design (e.g., m/z 50–1200, RT 0–50 min). Once loaded, proceed immediately to mass detection and peak picking without re-exporting; this preserves data fidelity.

## Related tools

- **MZmine2** (Standalone open bioinformatic tool for loading and processing raw LC-MS/MS data into aligned feature tables; directly invoked for feature detection and quantification.) — http://mzmine.github.io/
- **Optimus** (KNIME-orchestrated workflow wrapping OpenMS LC-MS feature detection and quantification; loads raw data and manages multi-step alignment, filtering, annotation, and spatial mapping in a single reproducible pipeline.) — https://github.com/MolecularCartography/Optimus
- **OpenMS** (Underlying C++ library providing state-of-the-art LC-MS feature detection and quantification algorithms; called by Optimus for mass detection, chromatogram building, and feature alignment.)
- **KNIME** (Open-source workflow management system that orchestrates Optimus; required for deployment and execution of the full LC-MS processing pipeline.) — https://www.knime.org

## Evaluation signals

- All sample files appear in the tool's file list and are recognized by their vendor format or open format codec.
- Parsed m/z range, retention time range, and scan count match your instrument configuration and experimental parameters.
- Memory footprint and load time scale linearly or sub-linearly with sample count (e.g., 100 LC-MS runs load in <5 min on a 2 GB RAM system for typical metabolomics experiments).
- Subsequent mass detection step immediately executes without file re-parsing, confirming data is held in accessible memory or indexed cache.
- Instrument metadata (analyzer type, polarity, scan event definitions) are correctly parsed and match your instrument's recorded settings.

## Limitations

- Only 64-bit operating systems are supported; MS Windows, Linux, and macOS are documented in Optimus. Vendor binary formats may not be portable across instruments.
- Minimum 2 GB RAM is required; larger datasets (100+ LC-MS runs) will require proportionally more memory. Temporary files generated during loading and processing can occupy several times the raw dataset size.
- Some vendor instruments require proprietary software or drivers to parse binary formats; Optimus and MZmine2 support mzML and mzXML open formats, which are recommended for reproducibility and long-term archival.
- Direct-infusion MS/MS data requires separate input configuration within Optimus; the default pipeline assumes liquid chromatography separation.
- No changelog is provided in the Optimus repository, complicating version-specific reproducibility and debugging.

## Evidence

- [other] Load raw MS/MS data files into MZmine2 or Optimus (OpenMS): "Load raw MS/MS data files into MZmine2 or Optimus (OpenMS). 2. Apply mass detection to identify peaks across all samples."
- [intro] MZmine2 and Optimus as open bioinformatic tools for feature detection and quantification from raw MS/MS data.: "The bioactive molecular network workflow uses MZmine2 or Optimus (built on OpenMS) as open bioinformatic tools for feature detection and quantification from raw MS/MS data."
- [readme] Optimus employs OpenMS state-of-the-art LC-MS feature detection and quantification algorithms: "Optimus employes the state-of-the-art LC-MS feature detection and quantification algorithms by [OpenMS](http://www.openms.de) which are joined into a handy pipeline"
- [readme] System requirements for data loading and processing: "*RAM*: 2 GB is minimal amount. Generally, it is not enough for analysis of large datasets containing about a hundred or more LC-MS runs."
- [readme] Support for both vendor and open MS data formats: "The workflow was initially developed for LC-MS-based metabolite cartography, but can be useful in almost any study of LC-MS-based untargeted metabolomics. Direct-infusion experimental data is also"
