---
name: spectral-library-metadata-assignment
description: Use when you have a compiled EI or MS2 library object (read from MSP
  format via read_lib) and access to NIST ri.dat and USER.DBU files; you need to populate
  RI values for capillary GC-MS workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - mspcompiler
  - R
  - NIST ri.dat and USER.DBU
  - MS-DIAL
  techniques:
  - LC-MS
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-library-metadata-assignment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Assign experimental Kovats retention index (RI) values from NIST database files to compiled mass spectral library objects, filtering by capillary column polarity and statistical robustness. This enriches spectral libraries with validated chemical reference data needed for GC-MS compound identification workflows.

## When to use

You have a compiled EI or MS2 library object (read from MSP format via read_lib) and access to NIST ri.dat and USER.DBU files; you need to populate RI values for capillary GC-MS workflows. Apply this when your library lacks experimental RI or you are combining multi-source libraries (NIST, MoNA, RIKEN, SWGDRUG) and want unified, quality-controlled RI metadata before writing the final MSP output.

## When NOT to use

- Your library consists of LC-MS/MS or tandem MS data without gas chromatography; RI is specific to GC-MS.
- You have no access to NIST ri.dat and USER.DBU files; extract_ri will fail.
- Your library already contains validated and curated RI values from another authoritative source; re-assignment may introduce conflicts or overwrite higher-quality metadata.

## Inputs

- compiled EI library object (from read_lib or c() concatenation of multiple library objects)
- NIST ri.dat file (RI database)
- NIST USER.DBU file (RI database supplement)
- polarity specification string ('semi-polar', 'non-polar', or 'polar')

## Outputs

- compiled library object with RI field populated for matched compounds
- optionally, MSP format file with RI values embedded (via write_EI_msp)

## How to apply

First, extract experimental Kovats RI from NIST ri.dat and USER.DBU files using extract_ri(), which parses the raw NIST RI database. Then apply assign_ri() to the compiled library object, specifying polarity='semi-polar' to retain only capillary GC column records (Lee RI values are removed). When multiple RI records exist for a single compound, the function computes the median RI and discards the value if standard deviation exceeds 30. Verify assignment by inspecting the RI column in the resulting object or writing to MSP format (write_EI_msp) and confirming RI presence in the output file.

## Related tools

- **mspcompiler** (R package providing extract_ri and assign_ri functions for NIST RI parsing and assignment) — https://github.com/QizhiSu/mspcompiler
- **R** (runtime environment for executing mspcompiler functions)
- **NIST ri.dat and USER.DBU** (source database files containing experimental Kovats RI values and metadata)
- **MS-DIAL** (downstream mass spectral search tool that accepts compiled MSP libraries with RI metadata)

## Examples

```
nist_ri <- extract_ri("D:/MS_libraries/ri.dat", "D:/MS_libraries/USER.DBU")
combine_ei <- assign_ri(combine_ei, nist_ri, polarity = "semi-polar")
```

## Evaluation signals

- RI column is non-empty for matched compounds in the output library object (check via inspect or summary)
- RI values fall within expected ranges for the target compound class (typically 800–3000 for capillary GC)
- Compounds with RI standard deviation >30 are excluded (no RI assigned); check count of retained vs. discarded records
- Final MSP file written via write_EI_msp contains RI= entries for expected compound rows
- No Lee RI values remain in the output when polarity='semi-polar' is specified (Lee RI is removed per design)

## Limitations

- assign_ri discards RI records with standard deviation >30, which may lose valid but variable experimental data for labile or isomeric compounds.
- Median RI is used when multiple records exist; this may mask important column or method-specific variation.
- RI assignment depends on exact name matching between library entries and NIST database; name normalization differences can cause non-matches.
- Only capillary GC column RI values are retained when polarity='semi-polar'; packed-column RI data is discarded, limiting applicability to legacy packed-column GC methods.
- The process is time-consuming (several hours) for large libraries; parallel computing (via future.apply) is recommended but adds setup complexity.

## Evidence

- [methods] extract_ri() to extract experimental RI from NIST files, and assign_ri() to assign experimental RI to the combined library: "extract_ri() to extract experimental RI from NIST files, and assign_ri() to assign experimental RI to the combined library"
- [readme] Extract experimental RI from the "ri.dat" and "USER.DBU" files. Once you have NIST library installed, these files can be found in, for example, "~/Programs/nist14/mssearch/nist_ri": "Extract experimental RI from the "ri.dat" and "USER.DBU" files. Once you have NIST library installed, these files can be found in, for example, "~/Programs/nist14/mssearch/nist_ri""
- [readme] Assign experimental RI to the combined library depending on the column polarity. The polarity can be "semi-polar", "non-polar", or "polar". Providing that "capillary" GC columns are commonly used. This function will only keep RI records from "capillary" columns and "Lee RI" will be removed.: "Assign experimental RI to the combined library depending on the column polarity. The polarity can be "semi-polar", "non-polar", or "polar". Providing that "capillary" GC columns are commonly used."
- [readme] When there are multiple records for a single compound, the median RI will be used and if the standard deviation is higher than 30, this value will be discarded.: "When there are multiple records for a single compound, the median RI will be used and if the standard deviation is higher than 30, this value will be discarded."
- [other] specifying polarity = "semi-polar" to filter RI records from capillary GC columns only, and discard RI values where standard deviation exceeds 30 or use median RI when multiple records exist for a single compound: "specifying polarity = "semi-polar" to filter RI records from capillary GC columns only, and discard RI values where standard deviation exceeds 30 or use median RI when multiple records exist"
