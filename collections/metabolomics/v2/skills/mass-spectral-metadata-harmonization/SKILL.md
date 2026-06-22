---
name: mass-spectral-metadata-harmonization
description: Use when you have multiple mass spectral libraries in different formats (NIST MSP + MOL folder, MoNA MSP, RIKEN MSP, SWGDRUG MSP) and need to merge them into a single, MS-DIAL-compatible MSP file with consistent SMILES assignments, Kovats retention indices (RI), and polarity annotations across all.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0153
  tools:
  - mspcompiler
  - R
  - future
  - future.apply
  - Lib2NIST
  - MS-DIAL
  - MoNA
  - RIKEN
  - ChemmineR
  - ChemmineOB
  - future / future.apply
  techniques:
  - GC-MS
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- library(future)
- library(future.apply)
- you can transformed it into a msp file by *Lib2NIST*
- MS-DIAL friendly msp file
- both positive and negative modes are in a single file as well. Therefore, we need to separated the polarity
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectral-metadata-harmonization

## Summary

Harmonize and standardize metadata fields (SMILES, retention indices, polarity, molecular formula) across heterogeneous EI and MS/MS mass spectral libraries from NIST, MoNA, RIKEN, and SWGDRUG into a unified MSP format for MS-DIAL. This skill reconciles structural and retention data from multiple sources with different formats and completeness levels.

## When to use

You have multiple mass spectral libraries in different formats (NIST MSP + MOL folder, MoNA MSP, RIKEN MSP, SWGDRUG MSP) and need to merge them into a single, MS-DIAL-compatible MSP file with consistent SMILES assignments, Kovats retention indices (RI), and polarity annotations across all compounds.

## When NOT to use

- Your source libraries are already harmonized in a single, unified format with all SMILES and RI fields pre-populated.
- You are building a de novo spectral library from new instrument runs rather than aggregating public reference libraries.
- You need non-GC-based retention data (e.g., LC RT) or polarity types not covered by NIST (e.g., highly polar columns); assign_ri() explicitly filters for capillary GC columns and discards Lee RI.

## Inputs

- NIST EI library MSP file (from Lib2NIST export)
- NIST MOL folder (linked MOL files)
- NIST ri.dat and USER.DBU files (for retention index data)
- RIKEN EI library MSP file (with Kovats RI)
- MoNA EI library MSP file (GC-MS Spectra)
- SWGDRUG EI library MSP file (from Lib2NIST export)
- SWGDRUG MOL folder (linked MOL files)
- MS2 library MSP files (NIST, RIKEN, MoNA positive and negative modes)
- GNPS library MGF file (optional)

## Outputs

- Harmonized combined EI MSP file with SMILES and RI fields populated
- Harmonized combined MS2 MSP files (separate positive and negative modes)
- Structure feature table (SMILES-to-compound index)

## How to apply

Load each library using read_lib() with the appropriate type (EI or MS2) and source-specific parameters (e.g., remove_ri=FALSE for RIKEN to preserve Kovats RI). For NIST and SWGDRUG, convert their MOL folders to SDF format using combine_mol2sdf(), extract chemical structures via extract_structure(), and assign SMILES using assign_smiles() with match='name'. For MoNA, use reorganize_mona() to extract and relocate SMILES from the Comment field into the SMILES field. Combine all processed libraries using the c() operator. Extract experimental RI data from NIST ri.dat and USER.DBU files using extract_ri(), then assign RI to the combined library via assign_ri() with polarity='semi-polar' (or appropriate polarity), filtering to capillary GC columns only and retaining median RI when standard deviation < 30. For MS2 libraries, use separate_polarity() to split positive and negative modes before combining. Finally, write the harmonized library to MSP format using write_EI_msp() or write_MS2_msp().

## Related tools

- **mspcompiler** (Core R package that provides read_lib(), combine_mol2sdf(), extract_structure(), assign_smiles(), reorganize_mona(), assign_ri(), separate_polarity(), write_EI_msp(), and write_MS2_msp() functions for orchestrating metadata harmonization.) — https://github.com/QizhiSu/mspcompiler
- **Lib2NIST** (Converts NIST and SWGDRUG binary library formats to MSP + MOL folder for ingestion into mspcompiler.) — https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:nist17
- **MS-DIAL** (Target analysis software that consumes the harmonized MSP file for compound identification and spectral matching.)
- **ChemmineR** (BioConductor dependency for SDF parsing and chemical structure manipulation in extract_structure().)
- **ChemmineOB** (BioConductor dependency for Open Babel-based structure format conversion and SMILES generation.)
- **future / future.apply** (R packages enabling parallel execution of structure extraction and SMILES assignment across large MOL/SDF files.)

## Examples

```
library(mspcompiler); library(future); plan(multisession(workers = detectCores() - 1)); nist_ei <- read_lib('D:/MS_libraries/NIST.MSP', type='EI'); combine_mol2sdf('D:/MS_libraries/NIST.MOL', 'D:/MS_libraries/nist.sdf'); nist_ei_structure <- extract_structure('D:/MS_libraries/nist.sdf', 'D:/MS_libraries/nist_structure.txt'); nist_ei <- assign_smiles(nist_ei, nist_ei_structure, match='name'); riken_ei <- read_lib('D:/MS_libraries/GCMS_DB-Public-KovatsRI-VS3.msp', type='EI', remove_ri=FALSE); mona_ei <- read_lib('D:/MS_libraries/MoNA-export-GC-MS_Spectra.msp', type='EI'); mona_ei <- reorganize_mona(mona_ei); combine_ei <- c(nist_ei, riken_ei, mona_ei); nist_ri <- extract_ri('D:/MS_libraries/ri.dat', 'D:/MS_libraries/USER.DBU'); combine_ei <- assign_ri(combine_ei, nist_ri, polarity='semi-polar'); write_EI_msp(combine_ei, 'D:/MS_libraries/combined_ei.msp'); plan(sequential)
```

## Evaluation signals

- Output MSP file is valid and readable by MS-DIAL without parsing errors.
- All four source libraries (NIST, RIKEN, MoNA, SWGDRUG) are present in the combined file with no records lost during merge.
- SMILES field is populated for all eligible compounds; compounds without valid structures are logged.
- Retention Index (RI) field is populated only for compounds with median RI (when SD < 30) from capillary GC columns; Lee RI and non-capillary entries are discarded as expected.
- Polarity field (for MS2 libraries) correctly reflects separation into positive and negative mode files; no mixed-polarity records remain in a single output file.
- No structural duplicates exist across source libraries (validated via InChIKey or SMILES deduplication).

## Limitations

- NIST library requires commercial installation and manual export via Lib2NIST; cannot be automated from binary source.
- SMILES assignment via assign_smiles(match='name') is name-based and may fail or yield incorrect structures if compound names are inconsistent or ambiguous across sources.
- Retention Index assignment is restricted to NIST-sourced RI data; user must have NIST library installed to extract ri.dat and USER.DBU files. RI values with SD ≥ 30 are discarded, reducing coverage.
- MOL folder manipulation (combine_mol2sdf) is time-consuming for large NIST libraries (hundreds of thousands of MOL files); moving or deleting the folder is impractical once created.
- On non-Linux/Mac systems, assign_smiles() with match='inchikey' may fail if ChemmineOB is not correctly installed; Windows users should use match='name'.
- MoNA SMILES extraction (reorganize_mona) assumes SMILES is in the Comment field; format changes in MoNA export may break parsing.

## Evidence

- [readme] The goal of mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be used in MS-DIAL.: "compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be"
- [other] The mspcompiler EI pipeline loads libraries via read_lib or read_multilibs, assigns SMILES structures via assign_smiles, assigns Kovats retention indices via assign_ri, combines the processed libraries, and writes the consolidated result to a single MSP file via write_EI_msp for use in MS-DIAL.: "loads libraries via read_lib or read_multilibs, assigns SMILES structures via assign_smiles, assigns Kovats retention indices via assign_ri, combines the processed libraries, and writes the"
- [readme] Combine all mol files into a single sdf file for subsequent structure retrieval. Extract structure based on the sdf file exported before. Assign SMILES to the library. If you are working with Linux-based or Mac OS, please use "match = "inchikey".: "Combine all mol files into a single sdf file for subsequent structure retrieval. Extract structure based on the sdf file exported before. Assign SMILES to the library."
- [readme] The SMILES has to be extracted from the *Comment* and put into the *SMILES* field by the *reorganize_mona* function.: "The SMILES has to be extracted from the *Comment* and put into the *SMILES* field by the *reorganize_mona* function"
- [readme] Assign experimental RI to the combined library depending on the column polarity. The polarity can be "semi-polar", "non-polar", or "polar". Providing that "capillary" GC columns are commonly used. This function will only keep RI records from "capillary" columns and "Lee RI" will be removed. When there are multiple records for a single compound, the median RI will be used and if the standard deviation is higher than 30, this value will be discarded.: "Assign experimental RI to the combined library depending on the column polarity. This function will only keep RI records from "capillary" columns and "Lee RI" will be removed. When there are multiple"
- [readme] The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing.: "The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing"
