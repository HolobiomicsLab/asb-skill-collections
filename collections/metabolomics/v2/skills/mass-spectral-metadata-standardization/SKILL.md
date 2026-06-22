---
name: mass-spectral-metadata-standardization
description: Use when you have acquired EI or MS/MS spectral libraries from multiple public sources (NIST, RIKEN, MoNA, SWGDRUG, GNPS) with inconsistent metadata field layouts, missing or misplaced SMILES entries, undocumented retention indices, or mixed polarity modes, and you need to merge them into a single.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - mspcompiler
  - R
  - future
  - future.apply
  - Lib2NIST
  - MS Search
  - MS-DIAL
  - R future package
  techniques:
  - LC-MS
  - GC-MS
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- Read the msp file into R.
- library(future)
- library(future.apply)
- you can transformed it into a msp file by *Lib2NIST*
- The total number of spectra that your NIST library have can be checked in the *MS Search* program
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mspcompiler_cq
    doi: 10.1021/acs.analchem.2c05389
    title: mspcompiler
  dedup_kept_from: coll_mspcompiler_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c05389
  all_source_dois:
  - 10.1021/acs.analchem.2c05389
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectral-metadata-standardization

## Summary

Standardize and reorganize mass spectral library metadata (SMILES, retention indices, molecular formulas, polarity) from heterogeneous public sources (NIST, RIKEN, MoNA, SWGDRUG) into a unified, MS-DIAL-compatible MSP format with consistent field organization and validated structure assignments.

## When to use

You have acquired EI or MS/MS spectral libraries from multiple public sources (NIST, RIKEN, MoNA, SWGDRUG, GNPS) with inconsistent metadata field layouts, missing or misplaced SMILES entries, undocumented retention indices, or mixed polarity modes, and you need to merge them into a single MS-DIAL-ready library with standardized, searchable metadata.

## When NOT to use

- Input is already a validated, single-source library with consistent metadata and no missing SMILES or RI fields — standardization adds no value.
- You need to retain all original RI values without filtering by column polarity or quality thresholds; the standardization workflow discards capillary-incompatible and high-variance RI records.
- Your MS/MS data are already separated into distinct positive and negative mode files with no polarity mixing — the separate_polarity() step is unnecessary.

## Inputs

- NIST EI library MSP file and corresponding MOL folder
- RIKEN EI library MSP file (with Kovats RI)
- MoNA GC-MS or LC-MS/MS Spectra MSP file
- SWGDRUG EI library MSP file and MOL folder
- NIST ri.dat and USER.DBU files (for experimental RI)
- GNPS MS2 library in MGF format (optional)

## Outputs

- Unified combined_ei.msp file readable by MS-DIAL
- Separate combined_ms2_pos.msp and combined_ms2_neg.msp files (for MS2 libraries)
- SDF file containing extracted molecular structures
- Text file of extracted structure information

## How to apply

Read each source library into R using mspcompiler::read_lib() with appropriate type ('EI' or 'MS2'). For libraries with MOL file folders (NIST, SWGDRUG), combine them into a single SDF using combine_mol2sdf(), extract molecular structures, and assign SMILES via assign_smiles() using name-based or InChIKey matching. For MoNA, reorganize SMILES from the Comment field into the SMILES field using reorganize_mona(). For MS2 libraries with mixed polarity, separate into positive and negative modes using separate_polarity(). Extract experimental retention indices from NIST ri.dat and USER.DBU files using extract_ri(), then assign RIs to the combined library via assign_ri() filtered by column polarity ('semi-polar', 'non-polar', or 'polar'), retaining only capillary columns and discarding records with standard deviation > 30. Finally, combine all organized libraries into a single object using c() and write the standardized output using write_EI_msp() or write_MS2_msp().

## Related tools

- **mspcompiler** (R package providing read_lib(), combine_mol2sdf(), extract_structure(), assign_smiles(), reorganize_mona(), separate_polarity(), assign_ri(), and write_EI_msp/write_MS2_msp functions for standardizing and combining spectral libraries) — https://github.com/QizhiSu/mspcompiler
- **MS-DIAL** (Target software that consumes the standardized MSP files as input for metabolomics analysis) — http://prime.psc.riken.jp/compms/msdial/main.html
- **Lib2NIST** (Utility to export NIST and SWGDRUG libraries from proprietary formats into MSP and MOL files suitable for mspcompiler ingestion) — https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:nist17
- **MS Search** (NIST utility to check total number of spectra in installed NIST library before exporting with Lib2NIST)
- **R future package** (Enables parallel computing for time-consuming structure extraction and SMILES assignment steps across multiple processor cores)

## Examples

```
library(mspcompiler); library(future); plan(multisession(workers = detectCores() - 1)); nist_ei <- read_lib('D:/MS_libraries/NIST.MSP', type = 'EI'); combine_mol2sdf('D:/MS_libraries/NIST.MOL', 'D:/MS_libraries/nist.sdf'); nist_ei_structure <- extract_structure('D:/MS_libraries/nist.sdf', 'D:/MS_libraries/nist_structure.txt'); nist_ei <- assign_smiles(nist_ei, nist_ei_structure, match = 'name'); riken_ei <- read_lib('D:/MS_libraries/GCMS DB-Public-KovatsRI-VS3.msp', type = 'EI', remove_ri = FALSE); combine_ei <- c(nist_ei, riken_ei); nist_ri <- extract_ri('D:/MS_libraries/ri.dat', 'D:/MS_libraries/USER.DBU'); combine_ei <- assign_ri(combine_ei, nist_ri, polarity = 'semi-polar'); plan(sequential); write_EI_msp(combine_ei, 'D:/MS_libraries/combine_ei.msp')
```

## Evaluation signals

- Output MSP file exists and is readable by MS-DIAL without parse errors
- All four (or selected subset of) source libraries are present in the combined output with no duplicate entries across sources
- SMILES field is present and consistently formatted in all records; no SMILES are missing from libraries that contained them
- Retention index assignments are consistent with the specified column polarity ('semi-polar', etc.) and standard deviation filter (SD ≤ 30); only capillary column RIs are retained
- Molecular Formula field is calculated and populated for all records containing SMILES (via complete_mgf for GNPS or equivalent)

## Limitations

- Parallel computing setup is time-consuming (several hours) for large libraries (hundreds of megabytes of MSP, hundreds of thousands of MOL files); MOL folder movement/deletion is slow and should be avoided after export.
- InChIKey-based SMILES matching (recommend for Linux/macOS) is not available for SWGDRUG library; name-based matching is less specific and may produce false positives.
- NIST library access requires commercial installation; if NIST is unavailable, RI assignment is limited to experimental RI already present in RIKEN and MoNA records.
- Retention index filtering by capillary column and SD threshold (>30 discarded) may result in loss of valid RI data for non-standard GC configurations.
- No changelog or version history provided; reproducibility and backwards compatibility across mspcompiler releases are undocumented.

## Evidence

- [other] how does mspcompiler organize and combine EI spectral libraries from multiple sources (NIST, MoNA, GPNS) into a unified MS-DIAL-ready MSP file: "how does mspcompiler organize and combine EI spectral libraries from multiple sources (NIST, MoNA, GPNS) into a unified MS-DIAL-ready MSP file with assigned SMILES and retention indices?"
- [other] mspcompiler reads EI libraries into R, combines molecular structure files into a unified SDF, extracts and assigns SMILES to library records: "mspcompiler reads EI libraries into R, combines molecular structure files into a unified SDF, extracts and assigns SMILES to library records, reorganizes SMILES fields from source metadata"
- [other] Extract experimental RI from NIST ri.dat and USER.DBU files using extract_ri(). Assign experimental RI to combined library with assign_ri() using semi-polar column polarity, filtering to capillary columns only and discarding values with standard deviation >30.: "Extract experimental RI from NIST ri.dat and USER.DBU files using extract_ri(). Assign experimental RI to combined library with assign_ri() using semi-polar column polarity, filtering to capillary"
- [readme] The goal of mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be used in MS-DIAL.: "The goal of mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a"
- [readme] The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing.: "The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing."
- [readme] This file has SMILES information though, it is in the Comment field. Therefore, the SMILES has to be extracted from the Comment and put into the SMILES field: "This file has SMILES information though, it is in the Comment field. Therefore, the SMILES has to be extracted from the Comment and put into the SMILES field"
- [readme] we have to separated them by the separate_polarity function: "The exported msp file has both positive and negative modes mixed in a singled file, so we have to separated them by the separate_polarity function"
- [readme] Providing that capillary GC columns are commonly used. This function will only keep RI records from capillary columns and Lee RI will be removed. When there are multiple records for a single compound, the median RI will be used and if the standard deviation is higher than 30, this value will be discarded.: "Providing that capillary GC columns are commonly used. This function will only keep RI records from capillary columns and Lee RI will be removed. When there are multiple records for a single"
