---
name: chemical-structure-smiles-assignment
description: Use when you have a mass spectral library (EI or MS2 format) loaded into R via read_lib() and possess either MOL files (from Lib2NIST export) or an SDF file containing the corresponding chemical structures, but the library entries lack SMILES fields or have incomplete structure information.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - mspcompiler
  - R
  - future
  - future.apply
  - RIKEN
  - MoNA
  - GNPS
  - MS-DIAL
  - Lib2NIST
  - ChemmineR / ChemmineOB
  - future / future.apply
  techniques:
  - tandem-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-structure-smiles-assignment

## Summary

Assign SMILES (Simplified Molecular Input Line Entry System) chemical structure strings to mass spectral library entries using structure files derived from MOL or SDF files. This skill enables enrichment of MS libraries with standardized chemical structure notation needed for downstream metabolomics workflows like MS-DIAL.

## When to use

Apply this skill when you have a mass spectral library (EI or MS2 format) loaded into R via read_lib() and possess either MOL files (from Lib2NIST export) or an SDF file containing the corresponding chemical structures, but the library entries lack SMILES fields or have incomplete structure information.

## When NOT to use

- Library already contains complete and valid SMILES fields from the source (e.g., RIKEN EI library)—skip directly to combination or write steps.
- Structure files (MOL/SDF) are unavailable or unaligned with library entries by name or InChIKey—structure assignment will fail silently on non-matching records.
- Working with MoNA libraries—use reorganize_mona() instead, which extracts SMILES from the Comment field without requiring external structure files.

## Inputs

- mass spectral library object (loaded via read_lib with type='EI' or type='MS2')
- MOL file directory (from Lib2NIST export) or pre-existing SDF file
- structure reference file (tab-delimited text with name/InChIKey and SMILES columns, from extract_structure())

## Outputs

- mass spectral library object with SMILES field populated
- ready for downstream polarity separation or RI assignment

## How to apply

First, prepare a structure reference file by either combining MOL files into a single SDF using combine_mol2sdf(), or use an existing SDF. Extract structure information (name and SMILES pairs) from the SDF file using extract_structure(), which produces a tab-delimited text file with compound names and SMILES strings. Then call assign_smiles() with the loaded library object and the extracted structure file, specifying match='name' for Windows/Agilent workflows or match='inchikey' for Linux/Mac systems (when InChIKey is available). The function performs name-based or InChIKey-based lookup and cross-references entries, appending SMILES to library records where matches are found. For large NIST libraries, enable parallel computing via future/future.apply before calling assign_smiles() to reduce processing time from hours to minutes.

## Related tools

- **mspcompiler** (R package providing assign_smiles(), extract_structure(), and combine_mol2sdf() functions for structure assignment to spectral libraries) — https://github.com/QizhiSu/mspcompiler
- **Lib2NIST** (Windows tool for exporting NIST libraries to MSP + MOL files in the required format for mspcompiler structure extraction) — https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:nist17
- **ChemmineR / ChemmineOB** (Bioconductor packages used by mspcompiler for SDF parsing and structure format conversions)
- **future / future.apply** (R packages enabling parallel backend for assign_smiles() on multi-core systems to accelerate SMILES matching)

## Examples

```
library(mspcompiler); library(future); plan(multisession(workers = detectCores() - 1)); nist_ei <- read_lib("D:/MS_libraries/NIST.MSP", type = "EI"); combine_mol2sdf("D:/MS_libraries/NIST.MOL", "D:/MS_libraries/nist.sdf"); nist_ei_structure <- extract_structure("D:/MS_libraries/nist.sdf", "D:/MS_libraries/nist_structure.txt"); nist_ei <- assign_smiles(nist_ei, nist_ei_structure, match = "name"); plan(sequential)
```

## Evaluation signals

- All or nearly all library entries now contain non-empty SMILES fields (inspect head() of library object and compare pre/post assignment counts).
- SMILES strings conform to standard SMILES grammar (correct valence, no dangling bonds, parseable by cheminformatics tools).
- Match rate (number of records with assigned SMILES / total records) is ≥ 95% for high-quality sources like NIST, or ≥ 80% for public libraries with nomenclature variation.
- No false positive SMILES assignments—spot-check 10–20 entries by comparing assigned SMILES to the original compound name or InChIKey to ensure lookup correctness.
- Library can be successfully written to MSP format via write_EI_msp() or write_MS2_msp() without schema errors.

## Limitations

- MOL/SDF structure files must be aligned with library entries by compound name or InChIKey; mismatches or typos in nomenclature cause silent failures (no error raised, no SMILES assigned).
- InChIKey-based matching (match='inchikey') is recommended for Linux/Mac but requires InChIKey fields in both the structure file and library metadata—unavailable in some older NIST releases.
- Processing time scales with library size (NIST EI: several hours on single core; parallel computing highly recommended). Intermediate SDF files (from combine_mol2sdf) can occupy hundreds of gigabytes.
- MOL folder manipulation (copy/move/delete) is extremely slow due to the large number of small files; choose storage location carefully before exporting from Lib2NIST.
- Some compounds lack MOL representations or valid SMILES, resulting in partial coverage—no imputation or fallback mechanism is provided.

## Evidence

- [other] Assign SMILES structures via assign_smiles with match='name'.: "Assign SMILES structures via assign_smiles; if you are working with Linux-based or Mac OS, please use "match = "inchikey"."
- [readme] Extract structure based on the sdf file exported before.: "Extract structure based on the sdf file exported before. nist_ei_structure <- extract_structure("D:/MS_libraries/nist.sdf", "D:/MS_libraries/nist_structure.txt")"
- [readme] Combine all mol files into a single sdf file for subsequent structure retrieval.: "Combine all mol files into a single sdf file for subsequent structure retrieval. combine_mol2sdf("D:/MS_libraries/NIST.MOL", "D:/MS_libraries/nist.sdf")"
- [readme] The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing.: "The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing."
- [other] For MoNA MS2 libraries, apply reorganize_mona() to relocate SMILES from Comment field to SMILES field.: "For MoNA MS2 libraries (positive and negative), apply reorganize_mona() to relocate SMILES from Comment field to SMILES field."
