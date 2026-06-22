---
name: smiles-structure-annotation-from-molfiles
description: Use when you have a mass spectral library in MSP format (e.g., from NIST, SWGDRUG, or other sources) exported alongside a folder of MOL files, and you need to populate the SMILES field in each library record to enable structure-based filtering, annotation, or downstream MS-DIAL analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0362
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0199
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
  techniques:
  - mass-spectrometry
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

# SMILES structure annotation from MOL files

## Summary

Convert a folder of MOL files into a single SDF file, extract chemical structures, and assign SMILES strings to a mass spectral library record by matching on compound name or InChIKey. This skill bridges structural data (MOL format) with spectral records (MSP format) for integrated cheminformatics workflows.

## When to use

You have a mass spectral library in MSP format (e.g., from NIST, SWGDRUG, or other sources) exported alongside a folder of MOL files, and you need to populate the SMILES field in each library record to enable structure-based filtering, annotation, or downstream MS-DIAL analysis. Typical triggers: processing commercial spectral databases with separate structural data, or integrating in-house spectral and structural datasets.

## When NOT to use

- The spectral library already has SMILES or InChIKey fields fully populated with high-quality structures; re-annotation risks overwriting reliable data.
- MOL files are missing or corrupt, or the MOL folder contains <10 structures—extraction and matching will fail or produce sparse coverage.
- The compound naming scheme in MSP does not match the identifiers embedded in MOL file headers; name-based matching will fail; InChIKey matching is not available in your context.

## Inputs

- folder of MOL files (e.g., NIST.MOL, SWGDRUG.MOL)
- mass spectral library in MSP format (pre-loaded via read_lib())
- compound name or InChIKey metadata for matching

## Outputs

- single consolidated SDF file (chemical structures in standard format)
- text file mapping compound identifiers to SMILES strings
- MSP-format library object with SMILES field populated for all matched compounds

## How to apply

First, combine all MOL files into a single SDF file using combine_mol2sdf(), pointing to the MOL folder and specifying an output SDF path. Next, extract chemical structures and their metadata from the SDF using extract_structure(), which outputs a text file mapping compound identifiers to SMILES. Finally, assign SMILES to the library using assign_smiles() with the match parameter set to 'name' (for compound name matching on most platforms) or 'inchikey' (for Linux/Mac OS users where name matching is less reliable). The function matches records by the chosen identifier and populates the SMILES field. If standard deviation of matched identifiers exceeds acceptable thresholds or duplicates arise, the function filters or resolves them based on median or preference rules.

## Related tools

- **mspcompiler** (R package providing combine_mol2sdf(), extract_structure(), and assign_smiles() functions for orchestrating MOL-to-SMILES assignment) — https://github.com/QizhiSu/mspcompiler
- **ChemmineR** (underlying R package for reading and parsing SDF files and extracting chemical structure objects)
- **ChemmineOB** (R wrapper for Open Babel providing structure matching and SMILES generation from MOL/SDF)
- **Lib2NIST** (NIST utility for exporting spectral libraries to MSP format with linked MOL files) — https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:nist17

## Examples

```
combine_mol2sdf("D:/MS_libraries/NIST.MOL", "D:/MS_libraries/nist.sdf"); nist_ei_structure <- extract_structure("D:/MS_libraries/nist.sdf", "D:/MS_libraries/nist_structure.txt"); nist_ei <- assign_smiles(nist_ei, nist_ei_structure, match = "name")
```

## Evaluation signals

- Output SDF file exists, is well-formed, and contains a structure record for each unique compound name in the MOL folder.
- Text mapping file contains non-null SMILES strings for ≥90% of compounds in the input library (or as specified by your source library completeness).
- MSP library object has SMILES field populated for all matched records; unmatched records retain empty SMILES (no insertion of invalid or NULL values).
- No structural duplicates or conflicting SMILES assignments for the same compound name across the four libraries (NIST, RIKEN, MoNA, SWGDRUG) when combined.
- Spot-check: manually verify 5–10 SMILES strings against the original chemical names for chemical validity (e.g., formula and structure match expected molecular weight).

## Limitations

- MOL-to-SMILES conversion depends on Open Babel via ChemmineOB; if Open Babel or ChemmineOB is not installed or fails, the skill will halt.
- Matching quality depends on the consistency and uniqueness of compound names in both MSP and MOL file headers; name variations, special characters, or missing names in MOL files will cause silent failures (unmatched records).
- Large MOL folders (hundreds of thousands of files) are time-consuming to process and move on disk; the README recommends using a stable location to avoid repeated copying.
- InChIKey-based matching (preferred on Linux/Mac) requires InChIKey information in MOL file headers; if absent, fallback to name-based matching may be less reliable.
- The skill does not validate chemical plausibility of the resulting SMILES or detect impossible structures; manual spot-checking is recommended.

## Evidence

- [readme] Combine all mol files into a single sdf file for subsequent structure retrieval.: "Combine all mol files into a single sdf file for subsequent structure retrieval."
- [readme] Extract structure based on the sdf file exported before.: "Extract structure based on the sdf file exported before."
- [readme] Assign SMILES to the library. If you are working with Linux-based or Mac OS, please use "match = "inchikey".: "Assign SMILES to the library. If you are working with Linux-based or Mac OS, please use "match = "inchikey"."
- [readme] Since the *.MOL folder contains a large number of mol files, it will be time-consuming to move, copy, or delete this folder.: "Since the *.MOL folder contains a large number of mol files, it will be time-consuming to move, copy, or delete this folder."
- [readme] If ChemineR and ChemineOB fail, please try installing via BiocManager.: "If ChemineR and ChemineOB fail, please try: if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager"); BiocManager::install("ChemmineR");"
