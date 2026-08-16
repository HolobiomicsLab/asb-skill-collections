---
name: tandem-ms-data-reorganization
description: Use when importing MS/MS spectral libraries (particularly from MoNA or
  GNPS) where SMILES or chemical structure identifiers are embedded in free-text or
  non-standard Comment fields rather than in dedicated SMILES/InChIKey fields, or
  when positive and negative ionization mode spectra are commingled.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - mspcompiler
  - R
  - future
  - future.apply
  - RIKEN
  - MoNA
  - GNPS
  - MS-DIAL
  - future / future.apply
  techniques:
  - LC-MS
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- library(future)
- library(future.apply)
- The MS-DIAL developers have compiled an EI library with Kovat RI included
- The RIKEN MS2 libraries can be download from the MS-DIAL homepage
- The MassBank of North America (MoNA) has an EI library available
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mspcompiler
    doi: 10.1021/acs.analchem.2c05389
    title: mspcompiler
  dedup_kept_from: coll_mspcompiler
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c05389
  all_source_dois:
  - 10.1021/acs.analchem.2c05389
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Tandem MS Data Reorganization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Reorganize tandem mass spectrometry (MS/MS) library records by relocating chemical structure metadata (SMILES, InChIKey) from non-standard fields (e.g., Comment) into their proper schema fields, and separate mixed-polarity spectral records into polarity-specific outputs for downstream analysis in MS-DIAL or similar platforms.

## When to use

Use this skill when importing MS/MS spectral libraries (particularly from MoNA or GNPS) where SMILES or chemical structure identifiers are embedded in free-text or non-standard Comment fields rather than in dedicated SMILES/InChIKey fields, or when positive and negative ionization mode spectra are commingled in a single file and must be segregated for ion-mode-specific analysis.

## When NOT to use

- Input library already has SMILES and InChIKey in proper schema fields and polarities are already separated into distinct files.
- MS/MS records lack SMILES or structural identifiers entirely and no external reference (e.g., InChIKey match) is available.
- Input is EI (electron ionization) rather than MS/MS (tandem MS); EI libraries use different reorganization and RI-assignment workflows.

## Inputs

- MS/MS spectral library in MSP format (mixed or single polarity)
- MS/MS spectral library in MGF format (e.g., GNPS)
- Library metadata object (class msp or mgf, with SMILES in Comment or missing fields)

## Outputs

- Reorganized MSP/MGF object with SMILES in standard SMILES field
- Positive-mode MS/MS spectral library (MSP or mgf object)
- Negative-mode MS/MS spectral library (MSP or mgf object)
- Polarity-separated MSP files compliant with MS-DIAL format specification

## How to apply

Load the MS/MS library (MSP or MGF format) using read_lib() with type='MS2' or format='mgf'. For libraries with SMILES in the Comment field (e.g., MoNA), apply reorganize_mona() to extract and relocate SMILES into the standard SMILES field. For MGF-format libraries (e.g., GNPS) lacking Molecular Formula, use complete_mgf() to compute MF from SMILES where available. Separate mixed-polarity libraries into positive and negative modes by calling separate_polarity() twice (once with polarity='pos', once with polarity='neg'). Combine polarity-separated records using c() to produce unified positive and negative mode objects. Validate that output files conform to MS-DIAL schema: no mixed polarities within a single file, all SMILES/InChIKey in proper fields, and Molecular Formula populated or absent consistently.

## Related tools

- **mspcompiler** (Provides reorganize_mona(), separate_polarity(), and complete_mgf() functions to restructure metadata fields, segment polarity, and compute molecular formula in MS/MS libraries.) — https://github.com/QizhiSu/mspcompiler
- **MS-DIAL** (Target platform for output MSP files; defines schema specification for polarity-separated, properly formatted MS/MS spectral records.)
- **R** (Execution environment and data structure container for mspcompiler objects and reorganization functions.)
- **future / future.apply** (Optional parallelization framework for accelerating reorganization of large libraries (millions of spectra).)

## Examples

```
mona_ms2_pos <- read_lib("D:/MS_libraries/MoNA-export-LC-MS-MS_Positive_Mode.msp"); mona_ms2_pos <- reorganize_mona(mona_ms2_pos); gnps <- read_lib("D:/MS_libraries/ALL_GNPS.mgf", format="mgf"); gnps <- complete_mgf(gnps); gnps_pos <- separate_polarity(gnps, polarity="pos"); gnps_neg <- separate_polarity(gnps, polarity="neg")
```

## Evaluation signals

- Output MSP/MGF objects contain SMILES in the standard SMILES field (not Comment or other non-standard fields).
- No mixed polarities remain within a single polarity-specific file (all records tagged or indexed for pos or neg mode only).
- Molecular Formula field is present and populated for all records (after complete_mgf) or explicitly documented as absent and consistent.
- Positive and negative mode objects are distinct and do not overlap in compound records (no duplicates across polarity files).
- Output MSP files conform to MS-DIAL specification: proper header fields, Num Peaks matches actual peak count, no malformed peak intensity pairs.

## Limitations

- reorganize_mona() assumes SMILES are present in the Comment field; if SMILES are absent, no chemical structure is added.
- complete_mgf() relies on existing SMILES in the MGF; if SMILES are missing, Molecular Formula cannot be computed.
- Separation by polarity (separate_polarity) depends on correct polarity assignment in the input file; if polarity metadata is corrupted or missing, separation may fail or produce incorrect assignments.
- Processing large libraries (e.g., NIST with hundreds of thousands of spectra) is time-consuming; the README recommends parallel computing (future/future.apply) to reduce wall-clock time, which may not be available on all compute platforms.
- GNPS library in MGF format requires explicit format='mgf' parameter; MSP format assumes default type='MS2', and mixing formats or omitting format may cause parsing errors.

## Evidence

- [other] For MoNA MS2 libraries (positive and negative), apply reorganize_mona() to relocate SMILES from Comment field to SMILES field.: "For MoNA MS2 libraries (positive and negative), apply reorganize_mona() to relocate SMILES from Comment field to SMILES field."
- [readme] SMILES information though, it is in the *Comment* field. Therefore, the SMILES has to be extracted from the *Comment* and put into the *SMILES* field by the *reorganize_mona* function.: "SMILES information though, it is in the *Comment* field. Therefore, the SMILES has to be extracted from the *Comment* and put into the *SMILES* field by the *reorganize_mona* function."
- [other] For GNPS library in MGF format, use complete_mgf() to calculate Molecular Formula from SMILES where missing.: "For GNPS library in MGF format, use complete_mgf() to calculate Molecular Formula from SMILES where missing."
- [readme] this library does not have the *Molecular Formula* (MF) field, so we can calculated the MF from the SMILES (if it exists) by the *complete_mgf* function.: "this library does not have the *Molecular Formula* (MF) field, so we can calculated the MF from the SMILES (if it exists) by the *complete_mgf* function."
- [other] Separate both NIST and GNPS libraries into positive and negative modes using separate_polarity() with polarity='pos' and polarity='neg'.: "Separate both NIST and GNPS libraries into positive and negative modes using separate_polarity() with polarity='pos' and polarity='neg'."
- [readme] The exported msp file has both positive and negative modes mixed in a singled file, so we have to separated them by the separate_polarity function.: "The exported msp file has both positive and negative modes mixed in a singled file, so we have to separated them by the separate_polarity function."
- [other] Validation: output MSP files conform to MS-DIAL format specification and contain no mixed polarities within a single file.: "Validation: output MSP files conform to MS-DIAL format specification and contain no mixed polarities within a single file."
