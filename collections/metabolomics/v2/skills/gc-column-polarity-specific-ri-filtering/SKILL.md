---
name: gc-column-polarity-specific-ri-filtering
description: Use when you have a combined EI mass spectral library (MSP format) lacking experimental RI values, access to NIST ri.dat and USER.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3371
  tools:
  - mspcompiler
  - R
  - future
  - future.apply
  - Lib2NIST
  - MS Search
  - MS-DIAL
  - NIST MS Search
  - R statistical environment
  techniques:
  - GC-MS
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

# GC column polarity-specific retention index filtering

## Summary

Filter and assign experimental retention indices (RI) from NIST reference data to combined EI spectral libraries based on GC column polarity (semi-polar, non-polar, or polar), retaining only capillary columns and rejecting RI values with standard deviation >30 across replicates. This ensures MS-DIAL-compatible libraries contain only validated, polarity-matched RI annotations.

## When to use

You have a combined EI mass spectral library (MSP format) lacking experimental RI values, access to NIST ri.dat and USER.DBU files, and need to annotate the library with high-confidence retention indices matched to the specific GC column polarity you intend to use (semi-polar, non-polar, or polar). The input library must already contain compound names and structures (SMILES) to enable RI matching.

## When NOT to use

- Input library is MS/MS (tandem MS) rather than EI; use separate RI strategies or omit RI assignment for MS/MS libraries.
- NIST RI database files are unavailable or you have only predicted/theoretical RI values; assign_ri() requires experimentally measured NIST reference data.
- Your intended analysis uses packed-column or packed-capillary GC rather than open-tubular capillary; the filter automatically removes packed-column RI data, making the output unsuitable for non-capillary workflows.

## Inputs

- combined EI mass spectral library (MSP format, with SMILES and compound names)
- NIST ri.dat file (retention index reference database)
- NIST USER.DBU file (user retention index database)
- column polarity specification (string: 'semi-polar', 'non-polar', or 'polar')

## Outputs

- EI mass spectral library with assigned experimental RI values (MSP format, polarity-matched and capillary-filtered)
- internal mapping of compound names to median RI with SD < 30 threshold applied

## How to apply

First, extract experimental RI records from NIST ri.dat and USER.DBU files using extract_ri(). Then, call assign_ri() on your combined EI library, specifying the column polarity ('semi-polar', 'non-polar', or 'polar'). The function automatically filters to capillary columns only (excluding Lee RI), removes entries with standard deviation >30 across multiple measurements for the same compound, and uses the median RI when multiple validated records exist. RI values are then assigned to the library records by compound name matching. This ensures only polarity-congruent, low-variance RI values are retained, improving identification accuracy in MS-DIAL.

## Related tools

- **mspcompiler** (R package that implements extract_ri() and assign_ri() functions for RI extraction and filtering) — https://github.com/QizhiSu/mspcompiler
- **NIST MS Search** (Reference database providing ri.dat and USER.DBU files containing experimental RI records indexed by column polarity and column type)
- **MS-DIAL** (Consumer software that uses the RI-annotated MSP library for GC-MS compound identification)
- **R statistical environment** (Runtime for mspcompiler package and statistical operations (median, SD calculation))

## Examples

```
nist_ri <- extract_ri("D:/MS_libraries/ri.dat", "D:/MS_libraries/USER.DBU"); combine_ei <- assign_ri(combine_ei, nist_ri, polarity = "semi-polar")
```

## Evaluation signals

- Output MSP library records contain SMILES, compound name, and RI (Retention Index) fields for all entries matched to NIST reference RI records.
- RI values assigned are exclusive to the specified column polarity and derived from capillary columns only (packed columns rejected).
- For compounds with multiple RI measurements in NIST database, the median RI is reported and entries with SD > 30 are excluded (not in output).
- Number of output records with assigned RI equals the count of unique compounds in input library that have ≥1 matched NIST capillary RI record passing the SD filter.
- Output is readable by MS-DIAL software without schema errors and produces correct compound peak annotation during GC-MS analysis using the matching column polarity.

## Limitations

- RI assignment requires NIST library installation and accessible ri.dat/USER.DBU files; public or in-house RI databases cannot substitute.
- Compounds in the input library must match NIST compound names for successful RI lookup; name standardization or manual curation may be needed if nomenclature differs.
- RI values are specific to the chosen column polarity; if the actual GC column polarity differs from the specified polarity during assign_ri(), RI annotations will be incorrect and harm identification accuracy.
- The SD > 30 threshold is fixed and not user-adjustable in the function signature; high-variance RI data (e.g., from older or non-standard methods) may be discarded even if valid.
- Lee RI (legacy retention index format) is automatically removed; workflows relying on Lee RI must extract RI before filtering or use an alternative function.

## Evidence

- [methods] Extract experimental RI from NIST ri.dat and USER.DBU files using extract_ri(): "Extract experimental RI from the "ri.dat" and "USER.DBU" files."
- [methods] Assign RI by column polarity with capillary-only and SD filtering: "Assign experimental RI to the combined library depending on the column polarity. The polarity can be "semi-polar", "non-polar", or "polar". Providing that "capillary" GC columns are commonly used."
- [readme] assign_ri() function call with polarity parameter and capillary filtering: "assign_ri(combine_ei, nist_ri, polarity = "semi-polar")"
- [readme] Purpose of RI assignment in library compilation workflow: "compile either EI or tandem mass spectral libraries from various sources, such as NIST (if you have it installed), MoNA, and GPNS, and organize them into a neat and up-to-date msp file that can be"
