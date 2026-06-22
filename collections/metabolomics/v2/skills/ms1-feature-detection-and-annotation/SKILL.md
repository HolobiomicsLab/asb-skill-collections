---
name: ms1-feature-detection-and-annotation
description: Use when you have FIA-MS, LC-MS, or GC-MS full-scan data in mzML format and need to identify unknown molecular features by accurate mass.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3637
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3172
  tools:
  - OpenMS
  - SmartPeak
  - SmartPeakCLI
  - pyOpenMS
  - BFAIR
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

# ms1-feature-detection-and-annotation

## Summary

Automated detection of molecular features from full-scan MS1 spectra and annotation of detected peaks against metabolite databases using accurate mass matching. This skill integrates peak picking, mass calibration, and database search to produce annotated feature lists with compound identifiers and structural metadata.

## When to use

Apply this skill when you have FIA-MS, LC-MS, or GC-MS full-scan data in mzML format and need to identify unknown molecular features by accurate mass. Specifically, use it when you want to move beyond raw spectra to a validated feature table with HMDB or similar database annotations, and your mass measurement error tolerance allows reliable matching (e.g., <5 ppm after calibration).

## When NOT to use

- Input is already a processed feature table or peak list — skip to downstream quantification or statistical analysis
- Data are from targeted/selected ion monitoring (SIM/MRM) workflows — use targeted peak picking instead
- Mass calibration has not been performed and measured m/z errors exceed database tolerance — recalibrate first or use wider tolerance at the cost of specificity

## Inputs

- Raw MS data (mzML format) from FIA-MS, LC-MS, or GC-MS runs
- Instrument parameters (resolution, mass range, bin step)
- HMDB or similar metabolite database mapping files (e.g., HMDBMappingFile.tsv, HMDB2StructMapping.tsv)
- Ion adduct list (e.g., positive_adducts.tsv, negative_adducts.tsv)
- Mass error tolerance threshold (ppm)

## Outputs

- Annotated feature table (mzTab format) with detected peaks
- Feature list containing m/z, retention time, intensity, and ion mode
- Peak annotations with HMDB compound identifiers, molecular formulas, and structural metadata
- Quality control metrics and calibration statistics

## How to apply

Load the raw MS data (e.g., mzML format) and extract spectra windows over the target acquisition time range using instrument parameters (e.g., resolution 12000, max_mz 1500 for FIA-MS). Merge spectra along the time axis to increase signal-to-noise ratio. Apply MS1 peak picking to detect molecular features from the merged spectrum. Execute accurate mass search against a reference database (HMDB, LIPIDMAPS) using the configured mass error tolerance and ion adducts (e.g., [M+H]+, [M+Na]+ for positive mode). Annotate detected peaks with database compound identifiers, molecular formulas, and structural metadata. Assemble and validate results into mzTab format, ensuring feature intensity, m/z accuracy, and annotation confidence meet quality thresholds.

## Related tools

- **SmartPeak** (Orchestrates the full workflow from raw data load, spectra extraction, peak picking, accurate mass search, and result assembly into mzTab format) — https://github.com/AutoFlowResearch/SmartPeak
- **SmartPeakCLI** (Command-line interface for non-interactive execution of the MS1 feature detection and annotation workflow) — https://github.com/AutoFlowResearch/SmartPeak
- **OpenMS** (Underlying toolkit providing peak picking algorithms, mass calibration, and accurate mass search functionality)
- **pyOpenMS** (Python bindings for parsing and post-processing of mzTab output and feature annotations)
- **BFAIR** (Post-processing and analysis of untargeted FIA-MS feature tables and annotations produced by SmartPeak) — https://github.com/AutoFlowResearch/BFAIR

## Examples

```
docker run --rm -ti -v C:/data:/sample-data autoflowresearch/smartpeak-cli:latest bash; SmartPeakCLI --input /sample-data/FIAMS_FullScan_Unknowns --workflow ms1_annotation --output /sample-data/results
```

## Evaluation signals

- mzTab output file is valid and conforms to mzTab schema (PSI standard); all required columns present
- Feature m/z values fall within expected biological range; no features with m/z < 50 or > configured max_mz without justification
- Annotated features have mass error ≤ configured tolerance (e.g., <5 ppm) after calibration
- Peak intensity and signal-to-noise ratio exceed configured thresholds; no spurious peaks from chemical noise
- Database annotations are non-empty for majority of detected features; compound identifiers, molecular formulas, and adduct assignments are present and consistent

## Limitations

- Accuracy depends on quality of mass calibration; systematic m/z error larger than tolerance will reduce annotation specificity
- Database coverage is limited to compounds in the reference mapping file (HMDB, LIPIDMAPS, etc.); novel or unannotated metabolites will not be identified
- Ion adduct predictions rely on configured adduct list; unexpected or unconventional adducts (e.g., [M+K]+, [M+Cl]-) may be missed
- Spectral resolution and instrument dynamic range affect peak picking sensitivity and specificity; low-resolution data may miss low-abundance features or split high-mass peaks
- No changelog or discussion of known failure modes provided in source documentation

## Evidence

- [methods] Load raw FIA-MS data and extract spectra windows over the specified acquisition time range (0–30 s) using the FIAMS parameters (resolution 12000, max_mz 1500, bin_step 20).: "Load raw FIA-MS data and extract spectra windows over the specified acquisition time range (0–30 s) using the FIAMS parameters (resolution 12000, max_mz 1500, bin_step 20)."
- [methods] Merge spectra along the time axis and perform MS1 peak picking to detect molecular features.: "Merge spectra along the time axis and perform MS1 peak picking to detect molecular features."
- [methods] Execute accurate mass search against the HMDB database using the mapping files (HMDBMappingFile.tsv, HMDB2StructMapping.tsv) and specified ion adducts (positive_adducts.tsv, negative_adducts.tsv) with the configured mass error tolerance.: "Execute accurate mass search against the HMDB database using the mapping files (HMDBMappingFile.tsv, HMDB2StructMapping.tsv) and specified ion adducts (positive_adducts.tsv, negative_adducts.tsv)"
- [methods] Annotate detected peaks with HMDB compound identifiers, molecular formulas, and structural metadata.: "Annotate detected peaks with HMDB compound identifiers, molecular formulas, and structural metadata."
- [intro] The workflow automates all steps from peak detection and integration over calibration curve optimization, to quality control reporting.: "The workflow automates all steps from peak detection and integration over calibration curve optimization, to quality control reporting."
- [readme] SmartPeak is an application that encapsulates advanced algorithms to enable fast, accurate, and automated processing of CE-, GC- and LC-MS(/MS) data, and HPLC data for targeted and semi-targeted metabolomics, lipidomics, and fluxomics experiments.: "SmartPeak is an application that encapsulates advanced algorithms to enable fast, accurate, and automated processing of CE-, GC- and LC-MS(/MS) data, and HPLC data for targeted and semi-targeted"
