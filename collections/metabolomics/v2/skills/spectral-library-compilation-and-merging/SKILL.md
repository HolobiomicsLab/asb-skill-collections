---
name: spectral-library-compilation-and-merging
description: Use when you have multiple mass spectral library files in different formats (MSP, MGF, MOL folders) from sources like NIST, MoNA, RIKEN, or GNPS, and need to produce a single consolidated MSP file with complete SMILES, InChIKey, and experimental retention index (RI) annotations for metabolomics or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - mspcompiler
  - R
  - future
  - future.apply
  - Lib2NIST
  - MS-DIAL
  - MoNA
  - RIKEN
  - GNPS
  - parallel
  - ChemmineR
  - ChemmineOB
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

# spectral-library-compilation-and-merging

## Summary

Compile and merge mass spectral libraries (EI or MS/MS) from heterogeneous public sources (NIST, MoNA, RIKEN, GNPS, SWGDRUG) into unified, annotated MSP files for use in MS-DIAL. The skill orchestrates library loading, structure assignment, retention index curation, and polarity-specific separation.

## When to use

You have multiple mass spectral library files in different formats (MSP, MGF, MOL folders) from sources like NIST, MoNA, RIKEN, or GNPS, and need to produce a single consolidated MSP file with complete SMILES, InChIKey, and experimental retention index (RI) annotations for metabolomics or toxicology screening in MS-DIAL.

## When NOT to use

- Your MS/MS library is already polarity-separated and requires no recombination
- You have a single library source and do not need to merge multiple sources
- Your libraries are already annotated with SMILES, InChIKey, and RI and require no re-processing

## Inputs

- NIST EI library (MSP file + MOL folder)
- NIST MS/MS library (MSP file + MOL folder)
- RIKEN EI library (MSP file with Kovats RI)
- RIKEN MS/MS library (MSP file, polarity-separated)
- MoNA EI library (MSP file with SMILES in Comment field)
- MoNA MS/MS library (MSP file, positive and negative modes)
- SWGDRUG EI library (MSP file + MOL folder)
- GNPS library (MGF format, mixed polarity)
- NIST RI reference files (ri.dat, USER.DBU)

## Outputs

- Merged EI library (MSP file with SMILES, InChIKey, experimental RI)
- Merged MS/MS positive mode library (MSP file with SMILES, InChIKey)
- Merged MS/MS negative mode library (MSP file with SMILES, InChIKey)
- Processed individual libraries (R objects) ready for combination

## How to apply

Load each source library using read_lib() with the appropriate type ('EI' or 'MS2') and format ('mgf' for GNPS). For NIST and SWGDRUG, convert MOL folders to SDF using combine_mol2sdf(), then extract structures via extract_structure() and assign SMILES with assign_smiles(match='name'). For MoNA libraries, use reorganize_mona() to relocate SMILES from Comment to SMILES field. For GNPS (MGF format), use complete_mgf() to compute molecular formula from SMILES. Separate positive and negative ionization modes using separate_polarity() for MS/MS libraries. For EI libraries, extract experimental RI from NIST ri.dat and USER.DBU files using extract_ri(), then assign RI to the combined library via assign_ri(polarity='semi-polar'), filtering for capillary GC columns and discarding RI values with standard deviation > 30. Combine all processed libraries using the c() operator, then write output via write_EI_msp() or write_MS2_msp(). Use parallel computing (future, future.apply, parallel) as processing is time-consuming for large libraries.

## Related tools

- **mspcompiler** (Core R package implementing read_lib, combine_mol2sdf, extract_structure, assign_smiles, reorganize_mona, extract_ri, assign_ri, separate_polarity, complete_mgf, write_EI_msp, write_MS2_msp functions) — https://github.com/QizhiSu/mspcompiler
- **Lib2NIST** (Desktop utility to export NIST library as MSP + MOL folder; installed with NIST library or downloadable separately) — https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:nist17
- **MS-DIAL** (Target metabolomics software that consumes the compiled and merged MSP libraries for spectral matching) — http://prime.psc.riken.jp/compms/msdial/main.html
- **R** (Runtime environment for mspcompiler package)
- **future** (R package enabling parallel execution strategy selection for long-running library processing)
- **future.apply** (R package providing parallel-safe versions of apply() for batch processing library records)
- **parallel** (R package for detecting and managing CPU core count for parallel workers)
- **ChemmineR** (Bioconductor package for chemical structure handling and SMILES manipulation (dependency))
- **ChemmineOB** (Bioconductor package wrapping Open Babel for structure file conversion and property calculation (dependency))

## Examples

```
library(mspcompiler); library(future); plan(multisession(workers=detectCores()-1)); nist_ei <- read_lib('D:/MS_libraries/NIST.MSP', type='EI'); combine_mol2sdf('D:/MS_libraries/NIST.MOL', 'D:/MS_libraries/nist.sdf'); nist_ei_structure <- extract_structure('D:/MS_libraries/nist.sdf', 'D:/MS_libraries/nist_structure.txt'); nist_ei <- assign_smiles(nist_ei, nist_ei_structure, match='name'); riken_ei <- read_lib('D:/MS_libraries/GCMS_DB-Public-KovatsRI-VS3.msp', type='EI', remove_ri=FALSE); combine_ei <- c(nist_ei, riken_ei); nist_ri <- extract_ri('D:/MS_libraries/ri.dat', 'D:/MS_libraries/USER.DBU'); combine_ei <- assign_ri(combine_ei, nist_ri, polarity='semi-polar'); plan(sequential); write_EI_msp(combine_ei, 'D:/MS_libraries/combine_ei.msp')
```

## Evaluation signals

- Output MSP file conforms to MS-DIAL MSP format specification (valid field names, structure, encoding)
- All source libraries are present in the merged output with no duplicates or loss of records across sources
- SMILES and InChIKey fields are populated for all eligible compounds; missing values are documented
- For EI libraries, experimental RI values are assigned only from capillary GC columns with SD < 30; non-qualifying RI records are excluded
- MS/MS output files contain no mixed polarities within a single MSP file (separate positive and negative files validate independently)
- Parallel processing completes without errors; no records are corrupted or lost during concurrent I/O operations

## Limitations

- Processing large libraries (hundreds of thousands of spectra) is time-consuming even with parallel computing; several hours expected on standard hardware
- MOL folder handling is slow for move/copy/delete operations; folder placement should be finalized before processing to avoid relocation
- NIST library is commercial and requires local installation; export via Lib2NIST introduces format-dependence and manual configuration steps
- SMILES assignment via match='name' fails silently for compounds without InChIKey or common name matches; match='inchikey' recommended for Linux/Mac but unavailable for SWGDRUG
- RI assignment requires NIST-specific ri.dat and USER.DBU reference files; these are not available for all column types or polarity settings; median RI is discarded if SD > 30, potentially losing valid annotations
- GNPS MGF format requires compute_mgf() to infer molecular formula from SMILES; this step may fail or produce incorrect formulas for polymeric or unconventional structures

## Evidence

- [readme] The goal of mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be used in MS-DIAL.: "The goal of mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a"
- [other] The mspcompiler EI pipeline loads libraries via read_lib or read_multilibs, assigns SMILES structures via assign_smiles, assigns Kovats retention indices via assign_ri, combines the processed libraries, and writes the consolidated result to a single MSP file via write_EI_msp for use in MS-DIAL.: "The mspcompiler EI pipeline loads libraries via read_lib or read_multilibs, assigns SMILES structures via assign_smiles, assigns Kovats retention indices via assign_ri, combines the processed"
- [other] For NIST EI, the workflow involves loading via read_lib(), converting MOL folder to SDF using combine_mol2sdf(), extracting chemical structures from SDF using extract_structure(), and assigning SMILES with match='name' parameter.: "Load NIST EI library MSP file using read_lib() with type='EI'; convert NIST.MOL folder to SDF format using combine_mol2sdf(); extract chemical structures from SDF using extract_structure(); assign"
- [readme] For EI libraries, the assign_ri() function filters for capillary GC columns only, retains median RI when standard deviation < 30, and removes Lee RI.: "This function will only keep RI records from "capillary" columns and "Lee RI" will be removed. When there are multiple records for a single compound, the median RI will be used and if the standard"
- [other] MS/MS libraries must be separated into positive and negative ionization modes using separate_polarity(), with output to separate MSP files for each mode.: "Separate both NIST and GNPS libraries into positive and negative modes using separate_polarity() with polarity='pos' and polarity='neg'. Write polarity-separated libraries to MSP format using"
- [readme] For GNPS libraries in MGF format, use complete_mgf() to calculate Molecular Formula from SMILES where missing.: "For GNPS library in MGF format, use complete_mgf() to calculate Molecular Formula from SMILES where missing"
- [readme] The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing.: "The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing"
