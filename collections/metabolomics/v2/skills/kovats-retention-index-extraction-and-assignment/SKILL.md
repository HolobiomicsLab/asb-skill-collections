---
name: kovats-retention-index-extraction-and-assignment
description: Use when you have compiled a multi-source EI library (NIST, RIKEN, MoNA, SWGDRUG) into a single msp object and want to enrich it with experimental retention index metadata. Apply this skill when you have access to NIST library installation files (ri.dat and USER.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - mspcompiler
  - R
  - future
  - future.apply
  - Lib2NIST
  - MS Search
  - MS-DIAL
  - NIST Library Installation
  techniques:
  - GC-MS
  - tandem-MS
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

# Kovats Retention Index Extraction and Assignment

## Summary

Extract experimental Kovats retention indices (RI) from NIST reference files and assign them to combined EI spectral library records based on GC column polarity, using median RI values and filtering by column type and variance thresholds to improve library metadata quality for MS-DIAL.

## When to use

You have compiled a multi-source EI library (NIST, RIKEN, MoNA, SWGDRUG) into a single msp object and want to enrich it with experimental retention index metadata. Apply this skill when you have access to NIST library installation files (ri.dat and USER.DBU) and need to assign RI values stratified by GC column polarity (semi-polar, non-polar, or polar) before writing the final MS-DIAL-ready msp file.

## When NOT to use

- NIST library is not installed or ri.dat/USER.DBU files are not available on your system
- Library records are MS2 (tandem MS) rather than EI spectra; MS2 records do not use Kovats RI
- Column polarity of your target GC method is unknown or does not match the available RI references (semi-polar, non-polar, polar)

## Inputs

- combined EI library object (mspcompiler lib object containing NIST, RIKEN, MoNA, and/or SWGDRUG records)
- ri.dat file (NIST RI database, typically at ~/Programs/nist14/mssearch/nist_ri/ri.dat)
- USER.DBU file (NIST user RI database, typically at ~/Programs/nist14/mssearch/nist_ri/USER.DBU)
- column polarity specification (semi-polar | non-polar | polar)

## Outputs

- combined EI library object with assigned Kovats RI field enriched with experimental values
- RI records stratified by column polarity and filtered for capillary columns only
- median RI values per compound with variance thresholding applied

## How to apply

First, extract experimental RI data from NIST reference files (ri.dat and USER.DBU) using the extract_ri() function, which parses the NIST RI database. Second, call assign_ri() on the combined library object, specifying the target column polarity (typically 'semi-polar' for capillary GC columns). The function filters to retain only capillary column records, removes Lee RI values, computes the median RI when multiple records exist for a single compound, and discards median values with standard deviation > 30 to ensure quality. This multi-step filtering ensures that only robust, polarity-matched RI annotations are assigned to each spectral record.

## Related tools

- **mspcompiler** (R package providing extract_ri() and assign_ri() functions for RI extraction, filtering, and assignment) — https://github.com/QizhiSu/mspcompiler
- **NIST Library Installation** (source of ri.dat and USER.DBU files containing experimental RI data indexed by compound name and GC column polarity)
- **MS-DIAL** (target software that consumes the RI-enriched msp file for spectral library matching and peak annotation) — http://prime.psc.riken.jp/compms/msdial/main.html

## Examples

```
nist_ri <- extract_ri("D:/MS_libraries/ri.dat", "D:/MS_libraries/USER.DBU")
combine_ei <- assign_ri(combine_ei, nist_ri, polarity = "semi-polar")
```

## Evaluation signals

- Output library object contains RI values assigned to all or most compound records without duplication or missing values for the target polarity
- RI assignments are stratified correctly by the specified GC column polarity (semi-polar, non-polar, or polar)
- Records with RI standard deviation > 30 are discarded; remaining RI values are robust median estimates
- Only capillary column RI records are retained; Lee RI and other column types are removed
- Final msp file is readable and accepted by MS-DIAL without parse errors related to RI field format or range

## Limitations

- RI assignment requires NIST library installation and ri.dat/USER.DBU file access; not available for open-source EI libraries lacking these files
- RI values are filtered by column polarity; if your GC method uses a non-standard or hybrid column polarity, RI assignment may fail or yield few matches
- Median RI and standard deviation filtering (SD > 30 threshold) may result in loss of RI annotations for compounds with high variability across NIST records
- RIKEN EI library records already contain Kovats RI; re-assigning RI from NIST may override pre-existing RIKEN annotations if not handled carefully

## Evidence

- [methods] Extract experimental RI from NIST ri.dat and USER.DBU files using extract_ri(): "Extract experimental RI from the "ri.dat" and "USER.DBU" files."
- [methods] Assign experimental RI depending on column polarity with filtering for capillary columns and variance threshold: "Assign experimental RI to the combined library depending on the column polarity. The polarity can be "semi-polar", "non-polar", or "polar". Providing that "capillary" GC columns are commonly used."
- [readme] mspcompiler goal is to compile EI and tandem mass spectral libraries from various sources and organize them into a neat and up-to-date msp file: "The goal of mspcompiler is to offer ways to compile either EI or tandem mass spectral libraries from various sources"
- [methods] RIKEN EI library already contains Kovats RI; read with remove_ri=FALSE to retain existing RI: "As it contains Kovats RI, we can set *remove_ri* to **FALSE** to keep original RI in this file."
- [methods] Workflow step to assign RI after reading and organizing all libraries: "assign_ri(combine_ei, nist_ri, polarity = "semi-polar")"
