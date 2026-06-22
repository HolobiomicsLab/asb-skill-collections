---
name: mass-spectrometry-column-polarity-filtering
description: Use when you have a combined EI library (from multiple sources such as NIST, RIKEN, MoNA) and access to NIST RI database files (ri.dat and USER.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - mspcompiler
  - R
  - NIST
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
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

# mass-spectrometry-column-polarity-filtering

## Summary

Filter and assign experimental Kovats retention index (RI) values to a compiled EI mass spectral library based on gas chromatography column polarity. This skill ensures that only RI measurements from appropriate capillary GC columns are retained and that RI records meeting quality thresholds are propagated into the final library.

## When to use

Apply this skill when you have a combined EI library (from multiple sources such as NIST, RIKEN, MoNA) and access to NIST RI database files (ri.dat and USER.DBU), and you need to enrich the library with experimentally validated Kovats RI values while filtering by column type (semi-polar, non-polar, or polar capillary GC columns).

## When NOT to use

- Input library already contains validated RI values from capillary GC columns and does not require re-filtering or enrichment.
- NIST RI database files (ri.dat, USER.DBU) are not available or accessible.
- The analysis goal is to preserve all RI records regardless of column type or measurement variability rather than applying quality-based filtering.

## Inputs

- compiled EI library object (e.g., from read_lib or combined from multiple sources)
- NIST ri.dat file (Kovats RI database)
- NIST USER.DBU file (user-defined RI records)

## Outputs

- EI library object with populated RI fields
- MSP format file with RI values assigned and polarity-filtered

## How to apply

First, extract experimental Kovats RI data from NIST ri.dat and USER.DBU files using extract_ri(), which parses the NIST RI database. Then apply assign_ri() to the combined library object, specifying the column polarity (e.g., 'semi-polar') to filter and retain only RI records from capillary GC columns. During assignment, the function automatically discards RI values where the standard deviation exceeds 30; when multiple RI records exist for a single compound, the median RI is computed and used. Verify population of RI fields by inspecting the RI column in the output library object or writing the output to MSP format and confirming RI presence in the resulting file.

## Related tools

- **mspcompiler** (Main R package providing extract_ri and assign_ri functions for RI extraction and assignment) — https://github.com/QizhiSu/mspcompiler
- **R** (Computing environment in which extract_ri and assign_ri are executed)
- **NIST** (Source of experimental Kovats RI data via ri.dat and USER.DBU database files) — https://chemdata.nist.gov/dokuwiki/doku.php?id=chemdata:nist17

## Examples

```
nist_ri <- extract_ri("D:/MS_libraries/ri.dat", "D:/MS_libraries/USER.DBU"); combine_ei <- assign_ri(combine_ei, nist_ri, polarity = "semi-polar")
```

## Evaluation signals

- RI field is populated in output library object for compounds with valid records matching the specified polarity.
- RI values show absence of records with standard deviation > 30; median RI is used when multiple records per compound exist.
- Only RI records from capillary GC columns are retained; 'Lee RI' and non-capillary entries are removed.
- Written MSP output file contains RI values in the RI field for enriched compounds.
- Cross-check: inspect a sample of library entries before/after assign_ri to confirm RI population and absence of invalid outliers.

## Limitations

- assign_ri filtering only applies to capillary GC columns; RI records from packed or other column types are discarded regardless of quality.
- RI values with standard deviation exceeding 30 are unconditionally removed, which may exclude valid measurements in systems with inherent variability.
- If no NIST RI database is available or installed locally, extract_ri cannot retrieve experimental RI data.
- Median RI calculation assumes that multiple records for the same compound represent equivalent or comparable measurements; this may not hold across different laboratories or instrument configurations.

## Evidence

- [methods] Extract experimental RI from NIST files: "Extract experimental Kovats RI data from NIST ri.dat and USER.DBU files using extract_ri"
- [readme] Assign RI based on polarity and quality thresholds: "The polarity can be "semi-polar", "non-polar", or "polar". Providing that "capillary" GC columns are commonly used. This function will only keep RI records from "capillary" columns and "Lee RI" will"
- [other] Verify RI population in output: "Verify that RI fields are populated in the resulting library object by inspecting the RI column in the output or writing the output to MSP format using write_EI_msp and confirming RI presence in the"
- [readme] Sequential workflow with RI assignment: "After read in and organize all these libraries, we can now combine them into a single file, assign experimental RI retrieved from the "ri.dat" and "USER.DBU" files (if you have NIST library"
