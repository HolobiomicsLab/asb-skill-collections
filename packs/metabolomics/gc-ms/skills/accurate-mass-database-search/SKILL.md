---
name: accurate-mass-database-search
description: Use when after peak detection and MS1 feature extraction from FIA-MS, GC-MS, LC-MS(/MS), or CE-MS data, when you need to identify unknown metabolites by matching observed m/z values to a reference database and want to recover HMDB identifiers, molecular formulas, and structural annotations for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - OpenMS
  - SmartPeak
  - SmartPeakCLI
  - pyOpenMS
  techniques:
  - LC-MS
  - GC-MS
  - CE-MS
  - direct-infusion-MS
  - ion-mobility-MS
derived_from:
- doi: 10.1021/acs.analchem.0c03421
  title: SmartPeak
evidence_spans:
- The software is based on the OpenMS toolkit
- The software is based on the OpenMS toolkit.
- SmartPeak automates targeted and quantitative metabolomics data processing
- SmartPeak CLI provides an equivalent of SmartPeak GUI application, however with a possibility to run in headless mode
- SmartPeak CLI provides an equivalent of SmartPeak GUI application
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smartpeak_cq
    doi: 10.1021/acs.analchem.0c03421
    title: SmartPeak
  dedup_kept_from: coll_smartpeak_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c03421
  all_source_dois:
  - 10.1021/acs.analchem.0c03421
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# accurate-mass-database-search

## Summary

Annotate detected molecular features by searching their accurate m/z values against a curated metabolite database (HMDB) using configurable mass error tolerance and ion adduct rules. This skill produces compound identifiers, molecular formulas, and structural metadata linked to each MS1 peak.

## When to use

After peak detection and MS1 feature extraction from FIA-MS, GC-MS, LC-MS(/MS), or CE-MS data, when you need to identify unknown metabolites by matching observed m/z values to a reference database and want to recover HMDB identifiers, molecular formulas, and structural annotations for downstream quantification or pathway analysis.

## When NOT to use

- If the input data contain only MS/MS fragmentation spectra without MS1 m/z values (library matching or spectral similarity methods are more appropriate).
- If ion adduct modes are unknown or highly variable and cannot be specified in advance (ion mode determination must precede this skill).
- If the reference database is incomplete, outdated, or not curated for your biological system of interest (limiting annotation sensitivity and specificity).

## Inputs

- Detected MS1 features (m/z, retention time, peak intensity, feature ID)
- Reference metabolite database (HMDB) with mapping files (HMDBMappingFile.tsv, HMDB2StructMapping.tsv)
- Ion adduct configuration files (positive_adducts.tsv, negative_adducts.tsv)
- Mass error tolerance threshold (ppm)

## Outputs

- Annotated feature list with HMDB identifiers and compound metadata
- mzTab annotation summary file (containing feature list and mass search results)
- Match quality metrics (mass error in ppm, rank, match confidence)

## How to apply

Load detected MS1 features (m/z, retention time, intensity) and configure the accurate mass search with: (1) a reference metabolite database (HMDB with HMDBMappingFile.tsv and HMDB2StructMapping.tsv files), (2) expected ion adducts (positive_adducts.tsv, negative_adducts.tsv specifying [M+H]+, [M-H]−, [M+Na]+, etc.), and (3) mass error tolerance (typically in ppm, e.g., 5 ppm for high-resolution Orbitrap). Execute the search against the database index, matching each feature's observed m/z to theoretical m/z values of known metabolites after applying adduct mass shifts. Rank candidate matches by mass error and, optionally, by database cross-references or structural similarity. Store matched annotations (HMDB ID, compound name, molecular formula, InChI, neutral mass) as feature metadata.

## Related tools

- **SmartPeak** (Orchestrates peak detection, calibration, accurate mass search, and mzTab assembly in a unified workflow) — https://github.com/AutoFlowResearch/SmartPeak
- **SmartPeakCLI** (Command-line interface for executing accurate mass search and annotation workflows without GUI) — https://github.com/AutoFlowResearch/SmartPeak
- **OpenMS** (Underlying toolkit providing accurate mass search algorithms and m/z calibration)
- **pyOpenMS** (Python bindings for parsing and processing annotated feature files and database search results)

## Examples

```
docker run --rm -ti -v C:/data:/sample-data autoflowresearch/smartpeak-cli:latest bash -c "SmartPeakCLI --config workflow.ini --data FIAMS_FullScan_Unknowns.mzML --database HMDB_mapping --adducts positive_adducts.tsv --mz_tolerance 5 --output results.mzTab"
```

## Evaluation signals

- All detected MS1 features have a best-match HMDB entry or are explicitly marked as unannotated (no orphaned features).
- Mass errors for matched features are ≤ the specified tolerance threshold (e.g., ≤ 5 ppm for high-resolution instruments).
- Ion adduct assignments are consistent with the acquisition mode and fragmentation patterns (e.g., [M+H]+ in positive mode, [M-H]− in negative mode).
- mzTab output conforms to the mzTab specification and includes mandatory columns (feature m/z, formula, accession) and optional metadata (InChI, compound name, neutral mass).
- Reproducibility: re-running the search on the same data with the same parameters and database version yields identical annotations.

## Limitations

- Mass error tolerance must be manually configured and is instrument-dependent; misconfigration leads to false positives or missed identifications.
- HMDB is primarily human-centric; coverage of non-mammalian, environmental, or drug metabolites may be incomplete.
- Multiple structural isomers can have identical m/z values; accurate mass search alone cannot distinguish them without orthogonal data (retention time, MS/MS fragmentation, or ion mobility).
- Isotope patterns and adduct ratios are not considered in the annotation step; results may include artefactual matches for low-intensity features or co-eluting unknowns.

## Evidence

- [methods] Execute accurate mass search against the HMDB database using the mapping files (HMDBMappingFile.tsv, HMDB2StructMapping.tsv) and specified ion adducts (positive_adducts.tsv, negative_adducts.tsv) with the configured mass error tolerance.: "Execute accurate mass search against the HMDB database using the mapping files (HMDBMappingFile.tsv, HMDB2StructMapping.tsv) and specified ion adducts (positive_adducts.tsv, negative_adducts.tsv)"
- [methods] Annotate detected peaks with HMDB compound identifiers, molecular formulas, and structural metadata.: "Annotate detected peaks with HMDB compound identifiers, molecular formulas, and structural metadata."
- [methods] Assemble results into mzTab format containing the feature list and mass search annotations, then store the mzTab output file.: "Assemble results into mzTab format containing the feature list and mass search annotations, then store the mzTab output file."
- [readme] SmartPeak is an application that encapsulates advanced algorithms to enable fast, accurate, and automated processing of CE-, GC- and LC-MS(/MS) data, and HPLC data for targeted and semi-targeted metabolomics, lipidomics, and fluxomics experiments.: "SmartPeak is an application that encapsulates advanced algorithms to enable fast, accurate, and automated processing of CE-, GC- and LC-MS(/MS) data, and HPLC data for targeted and semi-targeted"
