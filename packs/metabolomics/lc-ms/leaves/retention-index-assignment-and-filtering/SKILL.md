---
name: retention-index-assignment-and-filtering
description: Use when after combining multiple EI or MS2 mass spectral libraries and you have access to NIST RI reference files (ri.dat and USER.DBU) and need to assign experimental retention indices to compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0625
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
  - NIST MS Search
  techniques:
  - LC-MS
  - GC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Retention-Index Assignment and Filtering

## Summary

Assigns experimental Kovats retention indices (RI) to combined mass spectral libraries by extracting RI data from NIST reference files, then filters assigned RI values based on column type, polarity, and statistical quality thresholds. This enriches library records with validated RI metadata for improved compound identification in GC-MS workflows.

## When to use

Apply this skill after combining multiple EI or MS2 mass spectral libraries and you have access to NIST RI reference files (ri.dat and USER.DBU) and need to assign experimental retention indices to compounds. Use it when your combined library lacks RI values or when you want to replace provisional RI with validated median values across multiple GC column measurements.

## When NOT to use

- Your library already contains high-confidence, curated RI values from a single, trusted source (e.g., RIKEN library, which retains original RI by setting remove_ri=FALSE during read_lib())
- You do not have access to NIST RI reference files (ri.dat and USER.DBU)
- Your input library is MS2 (tandem MS) only and does not require GC-MS retention indices (which are specific to EI and GC-MS workflows)

## Inputs

- combined mass spectral library object (from c() operator on multiple read_lib() results)
- NIST ri.dat file (experimental RI reference data)
- NIST USER.DBU file (additional RI reference data)

## Outputs

- mass spectral library object with assigned RI field
- filtered RI values (capillary columns only, polarity-matched, median-aggregated, SD < 30)

## How to apply

First, extract experimental RI values from NIST 'ri.dat' and 'USER.DBU' files using extract_ri(). Then apply assign_ri() to the combined library, specifying the target column polarity (semi-polar, non-polar, or polar). The function automatically filters to retain only capillary GC column records (excluding Lee RI), removes Lee RI entries, computes the median RI when multiple records exist for a single compound, and discards the median value if the standard deviation exceeds 30. This two-step process ensures that only experimentally validated, high-confidence RI values are retained in the final library.

## Related tools

- **mspcompiler** (R package containing extract_ri() and assign_ri() functions for RI extraction and assignment) — https://github.com/QizhiSu/mspcompiler
- **NIST MS Search** (Source of RI reference files (ri.dat and USER.DBU) and GC column metadata)
- **MS-DIAL** (Downstream tool that consumes the RI-enriched MSP library for compound identification) — http://prime.psc.riken.jp/compms/msdial/main.html#MSP

## Examples

```
nist_ri <- extract_ri("D:/MS_libraries/ri.dat", "D:/MS_libraries/USER.DBU")
combine_ei <- assign_ri(combine_ei, nist_ri, polarity = "semi-polar")
```

## Evaluation signals

- Output library contains RI values in the RI field for eligible compounds (those matching semi-polar capillary GC columns in NIST reference)
- All retained RI values have standard deviation < 30 across multiple measurements (or are single measurements)
- All RI records originate from capillary GC columns only (non-capillary and Lee RI entries removed)
- RI polarity matches the specified parameter (semi-polar, non-polar, or polar) in assign_ri()
- When multiple RI records exist per compound, the median is retained; when SD ≥ 30, the value is discarded (no RI field entry)

## Limitations

- RI assignment is restricted to compounds present in NIST RI reference files; compounds not found in ri.dat or USER.DBU will not receive RI values
- The polarity filter (semi-polar, non-polar, polar) requires exact matching to the GC column metadata in NIST reference; mismatches result in loss of RI data for those compounds
- Standard deviation threshold of 30 is a fixed parameter; compounds with high measurement variability across GC columns are excluded, potentially losing valid RI data from heterogeneous sources
- RI assignment is specific to GC-MS (EI) workflows; it is not applicable to LC-MS/MS (MS2) libraries, which use retention time instead

## Evidence

- [methods] Extract experimental RI from NIST files (ri.dat and USER.DBU): "Extract experimental RI from the "ri.dat" and "USER.DBU" files"
- [methods] Assign RI with polarity filter and statistical quality checks: "Assign experimental RI to the combined library depending on the column polarity. The polarity can be "semi-polar", "non-polar", or "polar". Providing that "capillary" GC columns are commonly used."
- [methods] Median RI aggregation with SD threshold: "When there are multiple records for a single compound, the median RI will be used and if the standard deviation is higher than 30, this value will be discarded."
- [other] Assign RI step in the full pipeline: "assign RI to combined library using assign_ri() with polarity='semi-polar', filtering for capillary GC columns only and retaining median RI when standard deviation < 30"
