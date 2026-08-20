---
name: spectral-library-format-conversion
description: Use when when you have mass spectral libraries from multiple sources (NIST, MoNA, RIKEN, GNPS) in disparate formats (MSP, MGF, MOL folder structures) or with misaligned metadata (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0639
  tools:
  - mspcompiler
  - R
  - MoNA
  - future
  - future.apply
  - RIKEN
  - GNPS
  - MS-DIAL
  - Lib2NIST
  - ChemmineR
  - ChemmineOB
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- The MassBank of North America (MoNA) has an EI library available
- The MoNA MS2 libraries can be downloaded from https://mona.fiehnlab.ucdavis.edu/downloads
- library(future)
- library(future.apply)
- The MS-DIAL developers have compiled an EI library with Kovat RI included
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  - build: coll_metaboannotator_cq
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
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

# spectral-library-format-conversion

## Summary

Convert mass spectral libraries between formats (MSP, MGF, MOL/SDF, text) and reorganize metadata fields to conform to downstream tool requirements such as MS-DIAL. This skill is essential when compiling heterogeneous spectral sources (NIST, MoNA, RIKEN, GNPS) into a unified, polarity-separated library.

## When to use

When you have mass spectral libraries from multiple sources (NIST, MoNA, RIKEN, GNPS) in disparate formats (MSP, MGF, MOL folder structures) or with misaligned metadata (e.g., SMILES in Comment field instead of SMILES field), and need to produce polarity-separated MSP files conforming to MS-DIAL input specification.

## When NOT to use

- Input library is already in MS-DIAL MSP format and has been previously validated for polarity separation and SMILES field consistency.
- Source is a single, non-NIST EI library without MOL structure files and structure assignment is not required for downstream analysis.
- Library data exists only in proprietary database format without export capability to MSP, MGF, or MOL structures.

## Inputs

- MSP file (NIST, MoNA, RIKEN format)
- MGF file (GNPS format)
- MOL folder (structure files from NIST export)
- SDF file (combined structure data)
- Text file (extracted structure information with SMILES/InChIKey)

## Outputs

- R list object (internal library representation)
- MSP file (polarity-separated, MS-DIAL compatible)
- SDF file (combined structure data)
- Text file (structure information lookup table)

## How to apply

Load each source library using read_lib() with the appropriate type (EI, MS2) or format (mgf) parameter. For MOL-based sources, combine all MOL files into a single SDF using combine_mol2sdf(), then extract chemical structures and assign SMILES via assign_smiles(). For MoNA sources, apply reorganize_mona() to relocate SMILES from the Comment field to the SMILES field. For GNPS MGF libraries, use complete_mgf() to calculate missing Molecular Formula from SMILES. For mixed-polarity libraries, apply separate_polarity() with polarity='pos' and polarity='neg' to create separate objects. Combine polarity-specific objects using c() and write to MS-DIAL-compliant MSP format using write_EI_msp() or write_MS2_msp().

## Related tools

- **mspcompiler** (Primary R package providing read_lib, combine_mol2sdf, extract_structure, assign_smiles, reorganize_mona, separate_polarity, complete_mgf, write_EI_msp, write_MS2_msp functions for format conversion and metadata reorganization.) — https://github.com/QizhiSu/mspcompiler
- **Lib2NIST** (Utility for exporting NIST library database into MSP text file and MOL structure folder for downstream processing.) — https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:nist17
- **ChemmineR** (Bioconductor package for chemical structure handling and SMILES/InChIKey extraction.)
- **ChemmineOB** (Open Babel interface for ChemmineR; required for structure property calculations.)
- **MS-DIAL** (Downstream metabolomics software that consumes the MSP libraries produced by this skill.) — http://prime.psc.riken.jp/compms/msdial/main.html

## Examples

```
mona_ms2_pos <- read_lib('D:/MS_libraries/MoNA-export-LC-MS-MS_Positive_Mode.msp'); mona_ms2_pos <- reorganize_mona(mona_ms2_pos); write_MS2_msp(mona_ms2_pos, 'D:/MS_libraries/mona_ms2_pos_converted.msp')
```

## Evaluation signals

- Output MSP files contain no mixed polarities within a single file; positive and negative mode records are in separate files.
- SMILES field is populated for all records; no SMILES remain in Comment field or other non-standard locations.
- Row count of output library matches input library (no records lost during conversion).
- Output MSP conforms to MS-DIAL format specification: required fields (Name, PrecursorMZ, Num Peaks, etc.) are present and properly formatted.
- When comparing polarity-separated libraries via separate_polarity(), the union of pos and neg libraries equals the original combined library by record count.

## Limitations

- MOL folder processing is time-consuming (several hours reported) for large libraries (e.g., NIST with hundreds of thousands of files); parallel computing is strongly recommended but adds complexity.
- NIST library requires commercial license and manual export via Lib2NIST tool; not freely downloadable.
- Structure matching (assign_smiles) uses compound name or InChIKey; if neither is reliable or present, SMILES assignment may fail; Linux/Mac OS systems should use match='inchikey' while Windows systems may need match='name'.
- GNPS MGF format lacks Molecular Formula field in source; complete_mgf() computes it from SMILES, which requires SMILES to be present and valid.
- No automated validation of SMILES chemical validity; invalid SMILES may be retained in output.

## Evidence

- [readme] The goal of mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be used in MS-DIAL.: "compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be"
- [other] The mspcompiler system processes MS2 libraries through a sequence of steps: loading libraries from NIST, MoNA, GNPS, or RIKEN sources via read_lib; completing MGF metadata through complete_mgf; assigning SMILES structures via assign_smiles; separating positive and negative ionization modes via separate_polarity; and writing polarity-separated MSP files via write_MS2_msp for use in MS-DIAL.: "processes MS2 libraries through a sequence of steps: loading libraries from NIST, MoNA, GNPS, or RIKEN sources via read_lib; completing MGF metadata through complete_mgf; assigning SMILES structures"
- [readme] This file has SMILES information though, it is in the Comment field. Therefore, the SMILES has to be extracted from the Comment and put into the SMILES field by the reorganize_mona function.: "SMILES has to be extracted from the Comment and put into the SMILES field by the reorganize_mona function"
- [readme] Unlike others, the GNPS library is organized in mgf format, so it has to be treated differently. Hence, we have to set format = 'mgf' in the read_lib function. Besides, this library does not have the Molecular Formula (MF) field, so we can calculated the MF from the SMILES (if it exists) by the complete_mgf function.: "GNPS library is organized in mgf format, so it has to be treated differently. Hence, we have to set format = 'mgf' in the read_lib function. Besides, this library does not have the Molecular Formula"
- [readme] The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing.: "The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing"
- [readme] Select 'Text File(.MSP) + MOLfiles linked by BOTH' in Output Format; Select the library in Input Libraries or Text Files and Convert.: "Select 'Text File(.MSP) + MOLfiles linked by BOTH' in Output Format"
