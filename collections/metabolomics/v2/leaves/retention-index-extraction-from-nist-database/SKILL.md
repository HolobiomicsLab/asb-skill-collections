---
name: retention-index-extraction-from-nist-database
description: Use when you have a compiled EI or MS2 library object (from read_lib
  or c() combination of multiple sources) and a local NIST library installation with
  accessible ri.dat and USER.DBU files in the mssearch/nist_ri directory.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - mspcompiler
  - R
  - NIST
  - NIST library (mssearch)
  - MS-DIAL
  techniques:
  - LC-MS
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.2c05389
  title: mspcompiler
evidence_spans:
- library(mspcompiler)
- NIST is the most commonly used **commercial** EI library
- The NIST MS2 library can be treated as the same as the NIST EI library
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

# retention-index-extraction-from-nist-database

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract Kovats retention index (RI) values from NIST ri.dat and USER.DBU database files, then assign experimental RI records to a compiled EI or MS2 mass spectral library object. This skill enables enrichment of spectral libraries with GC retention data for improved compound identification.

## When to use

You have a compiled EI or MS2 library object (from read_lib or c() combination of multiple sources) and a local NIST library installation with accessible ri.dat and USER.DBU files in the mssearch/nist_ri directory. Use this skill to populate RI fields in your library when retention index data is absent or incomplete, particularly if you intend to use the library in MS-DIAL or require semi-polar or non-polar capillary GC retention data.

## When NOT to use

- NIST library is not installed locally or ri.dat/USER.DBU files are unavailable
- Your compiled library is intended for LC-MS/MS analysis (RI applies to capillary GC only)
- Library already contains experimentally validated RI values and you do not wish to overwrite or supplement them

## Inputs

- compiled EI or MS2 library object (from read_lib or c() concatenation)
- NIST ri.dat file (path, e.g. ~/Programs/nist14/mssearch/nist_ri/ri.dat)
- NIST USER.DBU file (path, e.g. ~/Programs/nist14/mssearch/nist_ri/USER.DBU)

## Outputs

- RI-enriched compiled library object with RI field populated for matching compounds
- MSP file with RI values embedded (when write_EI_msp is called)

## How to apply

Execute extract_ri() on the NIST ri.dat and USER.DBU files to parse and extract experimental Kovats RI records into a data structure. Then apply assign_ri() to your compiled library, specifying the column polarity (semi-polar, non-polar, or polar) to filter records from capillary GC columns only; the function automatically excludes Lee RI values, discards RI records with standard deviation exceeding 30, and uses median RI when multiple records exist for a single compound. Finally, verify RI field population by inspecting the output library object or writing it to MSP format with write_EI_msp() and confirming RI values are present in the resulting file.

## Related tools

- **mspcompiler** (R package that provides extract_ri() and assign_ri() functions for RI extraction and assignment in mass spectral library compilation workflows) — https://github.com/QizhiSu/mspcompiler
- **NIST library (mssearch)** (Source of ri.dat and USER.DBU database files containing experimental Kovats retention index records)
- **R** (Execution environment for mspcompiler functions)
- **MS-DIAL** (Downstream tool that consumes the MSP library file produced by write_EI_msp() after RI assignment)

## Examples

```
nist_ri <- extract_ri("D:/MS_libraries/ri.dat", "D:/MS_libraries/USER.DBU")
combine_ei <- assign_ri(combine_ei, nist_ri, polarity = "semi-polar")
```

## Evaluation signals

- RI column is present and populated in the output library object (inspect via summary or head)
- Numeric RI values fall within expected Kovats index range (typically 500–3000+ depending on column phase)
- Number of compounds with assigned RI is consistent with input library size and NIST database coverage for the specified polarity
- When write_EI_msp() is called, the resulting MSP file contains 'RI:' field entries for matching compounds
- Standard deviation filtering has been applied: no RI records with SD > 30 are present in output; median RI is used when multiple records exist per compound

## Limitations

- RI assignment only succeeds for compounds present in both the NIST ri.dat/USER.DBU database and the compiled library; many compounds may lack RI records
- Requires local NIST library installation; the ri.dat and USER.DBU files cannot be distributed separately and are only available via NIST purchase
- RI values are filtered to capillary GC columns only; non-capillary or packed-column RI records are excluded regardless of polarity parameter
- Lee RI values are automatically discarded; only Kovats RI are retained
- Processing is time-consuming with large libraries; parallel computing (via future/future.apply) is recommended for multi-hour workflows

## Evidence

- [readme] Extract experimental RI from the "ri.dat" and "USER.DBU" files. Once you have NIST library installed, these files can be found in, for example, "~/Programs/nist14/mssearch/nist_ri": "Extract experimental RI from the "ri.dat" and "USER.DBU" files. Once you have NIST library installed, these files can be found in, for example, "~/Programs/nist14/mssearch/nist_ri""
- [readme] This function will only keep RI records from "capillary" columns and "Lee RI" will be removed. When there are multiple records for a single compound, the median RI will be used and if the standard deviation is higher than 30, this value will be discarded.: "This function will only keep RI records from "capillary" columns and "Lee RI" will be removed. When there are multiple records for a single compound, the median RI will be used and if the standard"
- [other] Extract experimental RI to the combined library, specifying polarity = "semi-polar" to filter RI records from capillary GC columns only, and discard RI values where standard deviation exceeds 30 or use median RI when multiple records exist for a single compound: "specifying polarity = "semi-polar" to filter RI records from capillary GC columns only, and discard RI values where standard deviation exceeds 30 or use median RI when multiple records exist"
- [other] Verify that RI fields are populated in the resulting library object by inspecting the RI column in the output or writing the output to MSP format using write_EI_msp and confirming RI presence in the file: "Verify that RI fields are populated in the resulting library object by inspecting the RI column in the output or writing the output to MSP format using write_EI_msp and confirming RI presence in the"
- [other] extract_ri() to extract experimental RI from NIST files, and assign_ri() to assign experimental RI to the combined library: "extract_ri() to extract experimental RI from NIST files, and assign_ri() to assign experimental RI to the combined library"
