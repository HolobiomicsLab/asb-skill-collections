---
name: ei-spectral-library-parsing-and-merging
description: Use when you need to build a comprehensive EI spectral reference library
  for GC-MS compound identification in MS-DIAL, starting from raw downloads of NIST,
  RIKEN, MoNA, or SWGDRUG libraries that have inconsistent metadata organization (SMILES
  in different fields or absent, RI values missing or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - mspcompiler
  - R
  - future
  - future.apply
  - Lib2NIST
  - MS Search
  - MS-DIAL
  - ChemineR
  techniques:
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- Read the msp file into R.
- library(future)
- library(future.apply)
- you can transformed it into a msp file by *Lib2NIST*
- The total number of spectra that your NIST library have can be checked in the *MS
  Search* program
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# EI spectral library parsing and merging

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Parse electron ionization (EI) mass spectral libraries from multiple heterogeneous sources (NIST, RIKEN, MoNA, SWGDRUG), standardize their metadata fields (SMILES, retention indices, molecular formulas), and merge them into a unified MS-DIAL-compatible MSP file. This skill addresses the challenge that public EI libraries use inconsistent field organization, missing structure annotations, and vary in retention index coverage.

## When to use

Apply this skill when you need to build a comprehensive EI spectral reference library for GC-MS compound identification in MS-DIAL, starting from raw downloads of NIST, RIKEN, MoNA, or SWGDRUG libraries that have inconsistent metadata organization (SMILES in different fields or absent, RI values missing or non-standardized across column polarities) and you want to merge them without duplication while assigning experimental retention indices.

## When NOT to use

- Input is tandem MS/MS library data (use MS2 mode and separate by polarity instead)
- Libraries are already merged and validated in a single MSP file with consistent SMILES and RI fields
- You only need a single source library without cross-source merging (overhead not justified)

## Inputs

- NIST EI library MSP file (exported via Lib2NIST as Text File .MSP format)
- NIST.MOL folder (MOL files linked by Lib2NIST export)
- RIKEN EI library MSP file (All records with Kovats RI…EI-MS…)
- MoNA GC-MS Spectra MSP file
- SWGDRUG EI library MSP file and MOL folder
- NIST ri.dat file (retention index database)
- NIST USER.DBU file (retention index database)
- R environment with mspcompiler, future, future.apply, parallel packages loaded

## Outputs

- Unified combined_ei.msp file (MS-DIAL-compatible)
- Merged library object in R with standardized SMILES field across all records
- Assigned experimental retention indices by semi-polar column polarity
- Deduplicated spectral entries from all four source libraries

## How to apply

Read each library's MSP file into R using type='EI' or 'MS2'. For libraries distributed with MOL files (NIST, SWGDRUG), convert the MOL folder to a unified SDF using combine_mol2sdf(), then extract molecular structures and assign SMILES by name-based matching using assign_smiles(); for libraries with SMILES in non-standard fields (MoNA Comment field), use reorganize_mona() to move SMILES into the canonical SMILES field. Combine all parsed libraries with c(). Extract experimental retention indices from NIST ri.dat and USER.DBU files using extract_ri(), then assign RI to the combined library with assign_ri() using semi-polar column polarity, filtering to capillary columns only and discarding median RI values with standard deviation >30. Enable parallel computing via the future package (workers = detectCores() - 1) for the computationally intensive structure extraction and SMILES assignment steps, then disable it with plan(sequential) before writing the final merged library to MSP format using write_EI_msp().

## Related tools

- **mspcompiler** (Main R package for parsing MSP files, combining MOL to SDF, extracting and assigning SMILES, reorganizing metadata fields, and merging libraries) — https://github.com/QizhiSu/mspcompiler
- **Lib2NIST** (Converts NIST proprietary library format to MSP text file + MOL folder export) — https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:nist17
- **MS Search** (NIST utility to verify total number of spectra in installed NIST library before export)
- **MS-DIAL** (Target software that consumes the final merged combined_ei.msp file for GC-MS spectral matching) — http://prime.psc.riken.jp/compms/msdial/main.html
- **ChemineR** (Bioconductor dependency for chemical structure manipulation in mspcompiler)
- **future** (R package enabling parallel processing of computationally intensive steps (structure extraction, SMILES assignment))

## Examples

```
library(mspcompiler); library(future); plan(multisession(workers = detectCores() - 1)); nist_ei <- read_lib("D:/MS_libraries/NIST.MSP", type="EI"); combine_mol2sdf("D:/MS_libraries/NIST.MOL", "D:/MS_libraries/nist.sdf"); nist_ei_structure <- extract_structure("D:/MS_libraries/nist.sdf", "D:/MS_libraries/nist_structure.txt"); nist_ei <- assign_smiles(nist_ei, nist_ei_structure, match="name"); riken_ei <- read_lib("D:/MS_libraries/GCMS_DB-Public-KovatsRI-VS3.msp", type="EI", remove_ri=FALSE); mona_ei <- read_lib("D:/MS_libraries/MoNA-export-GC-MS_Spectra.msp", type="EI"); mona_ei <- reorganize_mona(mona_ei); combine_ei <- c(nist_ei, riken_ei, mona_ei); nist_ri <- extract_ri("D:/MS_libraries/ri.dat", "D:/MS_libraries/USER.DBU"); combine_ei <- assign_ri(combine_ei, nist_ri, polarity="semi-polar"); plan(sequential); write_EI_msp(combine_ei, "D:/MS_libraries/combine_ei.msp")
```

## Evaluation signals

- Output MSP file is readable by MS-DIAL software without parsing errors
- All four source libraries are present in the merged file with no duplication of entries (verify by record count: sum of input library sizes)
- Every compound record in the merged library has a SMILES field populated (no missing/NA values in canonical SMILES column)
- Retention indices are assigned only to capillary column entries; records with standard deviation >30 are excluded; median RI is used when multiple values exist per compound
- No records from non-capillary columns remain (verify by filtering on column type metadata field)

## Limitations

- SMILES assignment by name matching is OS-dependent; Linux/Mac users should use match='inchikey' where available, but SWGDRUG library lacks InChIKey data entirely, limiting its name-based matching success rate
- Process is time-consuming (several hours depending on hardware) due to conversion of hundreds of thousands of MOL files to SDF and structure property extraction; large MOL folders should not be moved/copied/deleted after export to avoid I/O overhead
- Experimental retention indices are sourced only from NIST ri.dat and USER.DBU; RIKEN and MoNA libraries have their own pre-assigned RI values (Kovats RI) which are retained as-is and not re-validated or filtered by polarity/column type
- When multiple RI records exist for a single compound, median is computed; if standard deviation exceeds 30, the value is discarded entirely, which may remove legitimate RI data for compounds with variable chromatographic behavior across labs

## Evidence

- [readme] The goal of mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be used in MS-DIAL.: "The goal of mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a"
- [readme] Combine all mol files into a single sdf file for subsequent structure retrieval. Extract structure based on the sdf file exported before. Assign SMILES to the library.: "Combine all mol files into a single sdf file for subsequent structure retrieval. Extract structure based on the sdf file exported before. Assign SMILES to the library."
- [readme] This file has SMILES information though, it is in the Comment field. Therefore, the SMILES has to be extracted from the Comment and put into the SMILES field by the reorganize_mona function.: "This file has SMILES information though, it is in the Comment field. Therefore, the SMILES has to be extracted from the Comment and put into the SMILES field"
- [readme] Assign experimental RI to the combined library depending on the column polarity. The polarity can be 'semi-polar', 'non-polar', or 'polar'. Providing that 'capillary' GC columns are commonly used. This function will only keep RI records from 'capillary' columns and 'Lee RI' will be removed. When there are multiple records for a single compound, the median RI will be used and if the standard deviation is higher than 30, this value will be discarded.: "Assign experimental RI to the combined library depending on the column polarity. The polarity can be 'semi-polar', 'non-polar', or 'polar'. This function will only keep RI records from 'capillary'"
- [readme] Set up parallel computing. Just remember to set it back once you have the library compiled by 'plan(sequential)'. We will include it later. The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing.: "The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing."
- [readme] As the SWGDRUG file does not contain InChIKey information, even though you are working with Linux-based or Mac OS, you should not use 'match = inchikey'. 'match = 'name' is more than enough in this case.: "As the SWGDRUG file does not contain InChIKey information, you should not use 'match = inchikey'. 'match = 'name' is more than enough in this case."
