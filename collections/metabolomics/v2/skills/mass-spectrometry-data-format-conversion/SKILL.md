---
name: mass-spectrometry-data-format-conversion
description: Use when you have mass spectral libraries from multiple sources (e.g., NIST EI, RIKEN MS2, MoNA GC-MS or LC-MS/MS, GNPS mgf) that need to be consolidated for use in MS-DIAL, or you have a single library with incomplete or malformed metadata (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - mspcompiler
  - R
  - MS-DIAL
  - Lib2NIST
  - MS Search
  - ChemmineR and ChemineOB
  - future and future.apply
  - PNNL PreProcessor
  - Agilent MassHunter
  - IM-MS Browser
  - IMFE
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
- doi: 10.1021/jasms.4c00220
  title: ''
- doi: 10.1021/acs.jproteome.1c00425
  title: ''
evidence_spans:
- library(mspcompiler)
- Read the msp file into R.
- MS-DIAL friendly msp file
- organize them into a neat and up-to-date msp file that can be used in MS-DIAL.
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files
- we have developed this user-friendly tool for Agilent MassHunter (.d) and UIMF mass spectrometry data files (MS-files) from drift tube (DT) and structure for lossless ion manipulations (SLIM) IM-MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mspcompiler_cq
    doi: 10.1021/acs.analchem.2c05389
    title: mspcompiler
  - build: coll_pnnl_preprocessor_cq
    doi: 10.1021/jasms.4c00220
    title: PNNL PreProcessor
  dedup_kept_from: coll_mspcompiler_cq
schema_version: 0.2.0
---

# mass-spectrometry-data-format-conversion

## Summary

Convert and harmonize mass spectral libraries from heterogeneous sources (NIST, MoNA, GNPS, RIKEN) into unified, polarity-separated msp files suitable for MS-DIAL analysis. This skill handles structural annotation, metadata reorganization, and format standardization across EI and tandem MS/MS libraries.

## When to use

You have mass spectral libraries from multiple sources (e.g., NIST EI, RIKEN MS2, MoNA GC-MS or LC-MS/MS, GNPS mgf) that need to be consolidated for use in MS-DIAL, or you have a single library with incomplete or malformed metadata (e.g., SMILES embedded in Comment fields, missing molecular formulas, mixed polarity modes).

## When NOT to use

- Input library is already a single, well-organized msp file with complete SMILES, InChIKey, and polarity annotations — direct import to MS-DIAL is more efficient.
- You need to perform spectral matching or similarity scoring across libraries — use this skill only for format preparation upstream of matching workflows.
- Library contains only MS1 data or precursor m/z values without fragmentation spectra — this skill is designed for EI or tandem MS/MS libraries with fragment annotations.

## Inputs

- msp files (EI or MS2 type)
- mgf files (GNPS format)
- MOL file directories (NIST, SWGDRUG export format)
- sdf files (structure definitions)
- NIST ri.dat and USER.DBU files (optional, for retention index assignment)

## Outputs

- unified msp file (EI library with Kovat RI)
- polarity-separated msp files (combine_ms2_pos.msp, combine_ms2_neg.msp)
- reorganized library object with harmonized SMILES, molecular formula, and metadata fields

## How to apply

Load each source library using read_lib() with the appropriate type parameter (EI, MS2, or mgf format). For libraries lacking structural information, convert associated MOL files to a unified SDF using combine_mol2sdf(), then extract structures and assign SMILES via extract_structure() and assign_smiles(). For libraries with SMILES in non-standard fields (e.g., MoNA Comment field), use reorganize_mona() to relocate SMILES to the dedicated SMILES metadata slot. For MS2 libraries with mixed ionization modes, separate positive and negative records using separate_polarity(polarity='pos' or 'neg'). For mgf-format libraries lacking molecular formulas, compute them from SMILES using complete_mgf(). Finally, concatenate all processed libraries by polarity and write to polarity-specific msp files using write_EI_msp() or write_MS2_msp(). Use parallel computing (via future and future.apply packages) to reduce processing time on large libraries (hundreds of thousands of spectra).

## Related tools

- **mspcompiler** (Core R package providing read_lib, combine_mol2sdf, extract_structure, assign_smiles, reorganize_mona, separate_polarity, complete_mgf, assign_ri, write_EI_msp, and write_MS2_msp functions for library ingestion, metadata harmonization, and export.) — https://github.com/QizhiSu/mspcompiler
- **MS-DIAL** (Target software that accepts the output msp files for spectral annotation and quantification workflows.)
- **Lib2NIST** (Utility for converting NIST library database files to msp format and exporting associated MOL files prior to mspcompiler ingestion.) — https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:nist17
- **MS Search** (Tool for checking total number of spectra in NIST library before selective export via Lib2NIST.)
- **ChemmineR and ChemineOB** (Bioconductor packages required as dependencies for mspcompiler to handle chemical structure parsing and SMILES computation.)
- **future and future.apply** (R packages enabling parallel computing to accelerate MOL-to-SDF conversion and structure extraction on multi-core systems.)

## Examples

```
library(mspcompiler); library(future); plan(multisession(workers = detectCores() - 1)); riken_ms2_pos <- read_lib("D:/MS_libraries/MSMS-Public-Pos-VS15.msp"); gnps <- read_lib("D:/MS_libraries/ALL_GNPS.mgf", format = "mgf"); gnps <- complete_mgf(gnps); gnps_pos <- separate_polarity(gnps, polarity = "pos"); combine_ms2_pos <- c(riken_ms2_pos, gnps_pos); write_MS2_msp(combine_ms2_pos, "D:/MS_libraries/combine_ms2_pos.msp")
```

## Evaluation signals

- All records in output msp file(s) have non-empty SMILES and molecular formula (MF) fields; verify by spot-checking 10+ records with read_lib() and inspecting $SMILES and $MF slots.
- Polarity separation is complete: positive-mode records have [M+H]+ precursor annotations and negative-mode records have [M-H]- annotations; verify distribution of PRECURSORTYPE field across combine_ms2_pos.msp and combine_ms2_neg.msp.
- No duplicate records or conflicting metadata across source libraries: compare InChIKey values and compound names before and after concatenation to identify redundancy.
- Output msp file is parseable by MS-DIAL without format errors: import into MS-DIAL and confirm successful library loading and spectrum visualization.
- Retention index (RI) assignment (EI libraries only): verify that combine_ei records include semi-polar capillary column RI values from NIST data, with standard deviation filtering applied (SD < 30 threshold enforced).

## Limitations

- Processing time is substantial for large libraries (several hours depending on CPU capability); parallel computing is necessary but not guaranteed to scale linearly. MOL file directories with hundreds of thousands of files are slow to move, copy, or delete after generation.
- SMILES extraction from MOL files relies on cheminformatics tooling (ChemmineR/ChemineOB) which may fail on malformed or non-standard chemical structures. InChIKey matching for SMILES assignment may fail on some systems; the package recommends Linux/Mac OS use 'match="inchikey"' but Windows users should fall back to 'match="name"'.
- RI assignment requires NIST library installation and manual export of ri.dat and USER.DBU files; only capillary column RI records are retained, and median RI is used when multiple records exist (discarding those with SD > 30).
- MoNA library reorganization assumes SMILES is consistently embedded in the Comment field; malformed or missing SMILES in Comment will result in empty SMILES fields after reorganize_mona().
- GNPS mgf format requires the complete_mgf() step to compute molecular formulas from SMILES; if SMILES is absent or invalid, molecular formula computation will fail.

## Evidence

- [readme] The goal of mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be used in MS-DIAL.: "The goal of mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a"
- [other] mspcompiler separates tandem MS/MS libraries by ionization polarity using the separate_polarity function, which can partition libraries into positive and negative modes.: "mspcompiler separates tandem MS/MS libraries by ionization polarity using the separate_polarity function, which can partition libraries into positive and negative modes"
- [other] The reorganize_mona operation parses SMILES data that is embedded in the Comment field of MoNA EI library records and relocates it into the dedicated SMILES metadata field.: "The reorganize_mona operation parses SMILES data that is embedded in the Comment field of MoNA EI library records and relocates it into the dedicated SMILES metadata field"
- [readme] This file has SMILES information though, it is in the Comment field. Therefore, the SMILES has to be extracted from the Comment and put into the SMILES field.: "This file has SMILES information though, it is in the Comment field. Therefore, the SMILES has to be extracted from the Comment and put into the SMILES field"
- [readme] The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing.: "The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing."
- [readme] we can calculated the MF from the SMILES (if it exists) by the *complete_mgf* function: "we can calculated the MF from the SMILES (if it exists) by the *complete_mgf* function"
- [readme] Assign experimental RI to the combined library depending on the column polarity. The polarity can be 'semi-polar', 'non-polar', or 'polar'.: "Assign experimental RI to the combined library depending on the column polarity. The polarity can be 'semi-polar', 'non-polar', or 'polar'."
- [readme] when there are multiple records for a single compound, the median RI will be used and if the standard deviation is higher than 30, this value will be discarded.: "when there are multiple records for a single compound, the median RI will be used and if the standard deviation is higher than 30, this value will be discarded."
