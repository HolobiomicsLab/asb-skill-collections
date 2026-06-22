---
name: metabolite-spectral-data-merging
description: Use when you have two or more mass spectral libraries in different formats (NIST binary exports converted to MSP, MoNA downloads, RIKEN public databases, GNPS MGF, or batches of in-house standards in separate MSP files) and need to combine them with consistent metadata (SMILES, InChIKey, molecular.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0630
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0154
  tools:
  - mspcompiler
  - R
  - future
  - future.apply
  - parallel
  - Lib2NIST
  - MS-DIAL
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- library(future)
- library(future.apply)
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

# metabolite-spectral-data-merging

## Summary

Merge multiple mass spectral libraries (EI or MS/MS) from heterogeneous public sources (NIST, MoNA, RIKEN, GNPS) and in-house standards into a single unified MSP file with harmonized structure, SMILES, and retention index (RI) annotations for downstream use in MS-DIAL or other metabolite identification pipelines.

## When to use

You have two or more mass spectral libraries in different formats (NIST binary exports converted to MSP, MoNA downloads, RIKEN public databases, GNPS MGF, or batches of in-house standards in separate MSP files) and need to combine them with consistent metadata (SMILES, InChIKey, molecular formula, polarity mode, RI values) into a single reference library for metabolite annotation.

## When NOT to use

- Input libraries are already merged and contain no duplicates or format inconsistencies (redundant processing).
- You require real-time or streaming library updates; this workflow is designed for batch compilation of static reference sources.
- Only single-library annotation is needed without harmonization across multiple sources.

## Inputs

- NIST EI library (MSP file + MOL folder exported via Lib2NIST)
- NIST MS/MS library (MSP file + MOL folder from nist_msms directory)
- MoNA EI or MS/MS library (MSP file downloaded from MoNA)
- RIKEN EI or MS/MS library (MSP file with Kovats RI pre-computed)
- GNPS MS/MS library (MGF file)
- SWGDRUG EI library (MSP + MOL folder)
- In-house standard libraries (directory of MSP files)
- NIST RI reference files (ri.dat and USER.DBU)
- SDF file containing structure records from combined MOL files

## Outputs

- Unified merged MSP file for EI library (write_EI_msp output)
- Unified merged MSP file for MS/MS positive mode (write_MS2_msp output)
- Unified merged MSP file for MS/MS negative mode (write_MS2_msp output)
- Merged library object in R with harmonized SMILES, InChIKey, molecular formula, polarity, and RI annotations

## How to apply

Load and parse each library separately using read_lib() (specifying type='EI' or 'MS2' and format='mgf' for GNPS) and apply library-specific reorganization steps: extract SMILES from MOL files via combine_mol2sdf() and extract_structure() with inchikey or name-based matching, reorganize SMILES from MoNA comment fields using reorganize_mona(), compute molecular formula from SMILES using complete_mgf() for GNPS, and separate mixed-polarity libraries (NIST MS2, GNPS) into positive/negative modes using separate_polarity(). Extract experimental RI values from NIST reference files (ri.dat and USER.DBU) using extract_ri(), then assign these to the combined library using assign_ri() with specified column polarity (semi-polar, non-polar, or polar) and filters (capillary columns only, median RI with std dev < 30). Before processing, enable parallel computing via plan(multisession(workers = detectCores() - 1)) to accelerate structure extraction and RI matching; disable with plan(sequential) before writing output. Finally, concatenate all processed libraries using c() and write to unified MSP format using write_EI_msp() or write_MS2_msp().

## Related tools

- **mspcompiler** (Primary package providing read_lib(), read_multilibs(), combine_mol2sdf(), extract_structure(), reorganize_mona(), assign_smiles(), separate_polarity(), extract_ri(), assign_ri(), complete_mgf(), write_EI_msp(), and write_MS2_msp() functions for library parsing, harmonization, and output) — https://github.com/QizhiSu/mspcompiler
- **future** (Enables parallel execution via plan(multisession()) for accelerating structure extraction and RI assignment steps across worker sessions)
- **future.apply** (Provides parallel versions of apply family functions used internally by mspcompiler for vectorized operations on library entries)
- **parallel** (Supplies detectCores() to determine optimal worker count and enables multi-session parallelization infrastructure)
- **Lib2NIST** (External utility (distributed with NIST library) to convert NIST binary library format into MSP + MOL folder suitable for mspcompiler ingestion) — https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:nist17
- **MS-DIAL** (Downstream metabolite identification software that consumes the final merged MSP library for compound annotation)

## Examples

```
library(mspcompiler); library(future); plan(multisession(workers = detectCores() - 1)); nist_ei <- read_lib('D:/MS_libraries/NIST.MSP', type = 'EI'); combine_mol2sdf('D:/MS_libraries/NIST.MOL', 'D:/MS_libraries/nist.sdf'); nist_ei_structure <- extract_structure('D:/MS_libraries/nist.sdf', 'D:/MS_libraries/nist_structure.txt'); nist_ei <- assign_smiles(nist_ei, nist_ei_structure, match = 'name'); mona_ei <- read_lib('D:/MS_libraries/MoNA-export-GC-MS_Spectra.msp', type = 'EI'); mona_ei <- reorganize_mona(mona_ei); combine_ei <- c(nist_ei, mona_ei); nist_ri <- extract_ri('D:/MS_libraries/ri.dat', 'D:/MS_libraries/USER.DBU'); combine_ei <- assign_ri(combine_ei, nist_ri, polarity = 'semi-polar'); plan(sequential); write_EI_msp(combine_ei, 'D:/MS_libraries/combined_ei.msp')
```

## Evaluation signals

- Merged library object structure matches expected format (named list of compound records with SMILES, InChIKey, molecular formula, polarity, RI fields populated where applicable).
- No duplicate compound entries (by name or InChIKey) exist in the merged output, or duplicates are intentionally retained with source attribution.
- SMILES assignment success rate: verify assign_smiles() matched ≥95% of compounds using the specified matching strategy (inchikey or name); check for NA values in SMILES field post-assignment.
- RI values assigned to compounds in target polarity column show plausible ranges (typical alkane RI 700–4000), exclude records from non-capillary columns, and median RI used when multiple records present with std dev filtering (threshold: std dev > 30 discarded).
- Write operations complete without error and output MSP file parses cleanly by re-reading with read_lib() to verify schema consistency across libraries.

## Limitations

- Structure extraction via extract_structure() is time-consuming (several hours for large NIST exports); parallel computing strongly recommended but requires sufficient RAM and CPU cores.
- SMILES matching via assign_smiles() uses name or InChIKey matching; match='inchikey' unreliable on Linux/Mac systems; match='name' requires compound names to be consistent across MOL and MSP files.
- RI assignment assumes NIST ri.dat and USER.DBU files are available; only capillary column RIs are retained, filtering may discard many records for compounds lacking RI on capillary columns.
- MOL folder movement/copying/deletion is extremely slow due to hundreds of thousands of individual files; plan directory locations carefully before exporting from Lib2NIST.
- GNPS MGF format lacks molecular formula field; complete_mgf() computes formula from SMILES, which fails silently for compounds lacking SMILES.
- Mixed-polarity libraries (NIST MS2, GNPS) require explicit separate_polarity() calls; failure to separate results in contaminated reference spectra for each ionization mode.
- No built-in changelog or version tracking; changelog missing from mspcompiler repository.

## Evidence

- [readme] The goal of mspcompiler is to compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be used in MS-DIAL.: "The goal of mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a"
- [readme] The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing.: "The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing."
- [readme] Combine them into a single file, assign experimental RI retrieved from the ri.dat and USER.DBU files, and filter by column polarity with median RI and standard deviation thresholds.: "Assign experimental RI to the combined library depending on the column polarity. The polarity can be "semi-polar", "non-polar", or "polar". Providing that "capillary" GC columns are commonly used."
- [readme] For mixed-polarity libraries like NIST MS2 and GNPS, separate positive and negative modes using separate_polarity() function.: "The exported msp file has both positive and negative modes mixed in a singled file, so we have to separated them by the separate_polarity function."
- [readme] When you have multiple libraries to be read in, the read_multilibs function gives you an easy way to read all of them at once by specifying a folder containing all MSP files.: "When you have multiple libraries to be read in, for instance if you are building your in-house library and you have one msp file for each batch of standards, then you will have many msp files to"
