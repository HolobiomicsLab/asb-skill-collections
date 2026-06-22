---
name: metabolite-tandem-ms-library-curation
description: Use when you have multiple tandem MS/MS libraries in different formats (msp, mgf) from different providers (NIST, RIKEN, MoNA, GNPS) with incomplete or inconsistent structural annotations (missing SMILES or molecular formula fields) and need to combine them into unified, polarity-specific msp files.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - mspcompiler
  - R
  - MS-DIAL
  - future / future.apply / parallel
  - ChemmineR / ChemineOB
  techniques:
  - LC-MS
  - GC-MS
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- Read the msp file into R.
- MS-DIAL friendly msp file
- organize them into a neat and up-to-date msp file that can be used in MS-DIAL.
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

# Metabolite Tandem MS/MS Library Curation

## Summary

Compile and organize tandem mass spectral libraries from multiple sources (NIST, RIKEN, MoNA, GNPS) into polarity-separated msp files compatible with MS-DIAL by reading, enriching with structural metadata (SMILES, molecular formula), and separating positive and negative ionization modes.

## When to use

You have multiple tandem MS/MS libraries in different formats (msp, mgf) from different providers (NIST, RIKEN, MoNA, GNPS) with incomplete or inconsistent structural annotations (missing SMILES or molecular formula fields) and need to combine them into unified, polarity-specific msp files for use in MS-DIAL analysis workflows.

## When NOT to use

- Input libraries are already merged and polarity-separated into individual msp files — skip combine and separate_polarity steps.
- Target MS/MS library is EI (electron ionization) rather than tandem MS/MS — use write_EI_msp() and different RI assignment workflow instead.
- MS/MS spectra are already in MS-DIAL proprietary format — no conversion needed.

## Inputs

- NIST MS/MS msp file (mixed polarity)
- RIKEN MS/MS msp files (MSMS-Public-Pos-VS15.msp, MSMS-Public-Neg-VS15.msp)
- MoNA LC-MS/MS msp files (positive and negative mode, separate)
- GNPS mgf library (ALL_GNPS.mgf, mixed polarity)
- Molecular structure files (sdf) or structural annotations (InChIKey, SMILES)

## Outputs

- combine_ms2_pos.msp (polarity-separated positive-mode library)
- combine_ms2_neg.msp (polarity-separated negative-mode library)
- Merged tandem MS/MS library object with enriched SMILES and molecular formula fields

## How to apply

Load each library using read_lib() with appropriate type (MS2) and format parameters (msp or mgf). For GNPS mgf format, compute missing molecular formula fields from SMILES using complete_mgf(). For RIKEN, load pre-separated positive and negative mode files directly. For MoNA, reorganize SMILES from the Comment field using reorganize_mona(). Separate any mixed-polarity libraries (NIST MS2, GNPS) into positive and negative modes using separate_polarity() with polarity="pos" and polarity="neg" parameters. Concatenate all positive-mode libraries into a single object, then all negative-mode libraries into a second object. Write each combined object to msp format using write_MS2_msp(), producing separate combine_ms2_pos.msp and combine_ms2_neg.msp files. This workflow ensures consistent schema, complete metadata, and correct polarity segregation for downstream MS-DIAL use.

## Related tools

- **mspcompiler** (R package providing read_lib(), separate_polarity(), complete_mgf(), reorganize_mona(), and write_MS2_msp() functions for library curation) — https://github.com/QizhiSu/mspcompiler
- **MS-DIAL** (Target metabolomics software for which polarity-separated msp files are output and used)
- **future / future.apply / parallel** (R packages for parallel computing acceleration during library loading and processing)
- **ChemmineR / ChemineOB** (Bioconductor packages for chemical structure extraction and SMILES computation from mol/sdf files)

## Examples

```
plan(multisession(workers = detectCores() - 1)); riken_ms2_pos <- read_lib("D:/MS_libraries/MSMS-Public-Pos-VS15.msp"); gnps <- read_lib("D:/MS_libraries/ALL_GNPS.mgf", format="mgf"); gnps <- complete_mgf(gnps); gnps_pos <- separate_polarity(gnps, polarity="pos"); combine_ms2_pos <- c(riken_ms2_pos, gnps_pos); write_MS2_msp(combine_ms2_pos, "D:/MS_libraries/combine_ms2_pos.msp"); plan(sequential)
```

## Evaluation signals

- Output msp files contain no missing SMILES or molecular formula fields for entries that require them (validation against schema)
- Polarity field is consistently labeled (e.g., 'POS' vs 'NEG') and correctly segregated — no positive-mode spectra appear in combine_ms2_neg.msp and vice versa
- Total spectrum count in combined files matches sum of input libraries minus duplicates (if deduplication applied)
- MS-DIAL can parse and load combine_ms2_pos.msp and combine_ms2_neg.msp without errors or warnings
- Enriched entries (from GNPS or MoNA) contain populated InChIKey, SMILES, and MolecularFormula fields; entries inherit these from parent library where applicable

## Limitations

- Processing large NIST libraries (hundreds of megabytes, hundreds of thousands of mol files) is time-consuming (several hours) even with parallel computing; requires adequate disk space and CPU cores.
- GNPS library must have SMILES present to compute molecular formula via complete_mgf(); spectra without SMILES will have incomplete metadata.
- MoNA reorganize_mona() function assumes SMILES is located in the Comment field; other non-standard formats may not parse correctly.
- Linux and Mac OS users must use match="inchikey" for extract_structure() and assign_smiles() rather than match="name" to ensure reliable compound matching across mol files.
- When multiple RI records exist for a single compound, the median RI is used and values with standard deviation > 30 are discarded — may lose valid RI information for compounds with high variability.

## Evidence

- [readme] The goal of mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be used in MS-DIAL.: "organize mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a"
- [other] mspcompiler separates tandem MS/MS libraries by ionization polarity using the separate_polarity function, which can partition libraries into positive and negative modes, enabling the subsequent generation of polarity-specific msp files for MS-DIAL.: "mspcompiler separates tandem MS/MS libraries by ionization polarity using the separate_polarity function, which can partition libraries into positive and negative modes"
- [other] Separate GNPS library into positive and negative modes using separate_polarity() function with polarity="pos" and polarity="neg" parameters.: "Separate GNPS library into positive and negative modes using separate_polarity() function with polarity="pos" and polarity="neg" parameters"
- [other] For GNPS library, compute molecular formula from SMILES using complete_mgf() before polarity separation.: "Compute Molecular Formula from SMILES: so we can calculated the MF from the SMILES (if it exists) by the *complete_mgf* function"
- [readme] The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing.: "The whole process is time-consuming (several hours, depending on the capability of your PC), so we suggests to use parallel computing"
- [readme] This library does not have the *Molecular Formula* (MF) field, so we can calculated the MF from the SMILES (if it exists) by the *complete_mgf* function.: "This library does not have the *Molecular Formula* (MF) field, so we can calculated the MF from the SMILES (if it exists) by the *complete_mgf* function"
- [readme] After read in and organize all these libraries, we can now combine them into a single file.: "After read in and organize all these libraries, we can now combine them into a single file"
