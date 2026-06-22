---
name: data-object-loading-and-inspection
description: Use when you have identified example R or MATLAB scripts in a repository's Codes-Explained folder and need to execute them on a documented sub-sample scenario. The link-to-codes-and-data-objects file specifies which data object(s) to load, and the Read-Me.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3571
  tools:
  - R
  - MATLAB
  - DisCoPad repository
derived_from:
- doi: 10.3390/metabo15010028
  title: DisCo P-ad
evidence_spans:
- example R and MATLAB codes (for one data sub-sample scenario) used for the simulation
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_disco_p_ad_cq
    doi: 10.3390/metabo15010028
    title: DisCo P-ad
  dedup_kept_from: coll_disco_p_ad_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo15010028
  all_source_dois:
  - 10.3390/metabo15010028
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# data-object-loading-and-inspection

## Summary

Load sub-sample data objects referenced in a simulation workflow using language-appropriate methods (R or MATLAB), then inspect their structure, dimensions, and content to verify correctness before executing downstream analysis scripts. This skill ensures that input data conform to expected schemas and enables early detection of missing or malformed data.

## When to use

You have identified example R or MATLAB scripts in a repository's Codes-Explained folder and need to execute them on a documented sub-sample scenario. The link-to-codes-and-data-objects file specifies which data object(s) to load, and the Read-Me.txt file documents the expected format and purpose of each object. Use this skill before running simulation or analysis scripts to confirm that data load correctly and match the documented structure.

## When NOT to use

- Data object has already been loaded and verified in a prior session and is still resident in memory.
- You are working with a new sub-sample scenario not documented in the Read-Me.txt file; consult article methods or contact authors first.
- The data object file is corrupted, missing, or the file path in link-to-codes-and-data-objects is broken.

## Inputs

- link-to-codes-and-data-objects file (index of data object references)
- Read-Me.txt file (documentation of expected data structure and purpose)
- Data object file (e.g., .RData, .mat, CSV, or other language-native format)
- Example R or MATLAB script (for reference of object names and expected usage)

## Outputs

- Loaded data object in memory (R data.frame, matrix, or MATLAB struct/array)
- Console output from introspection commands (dimensions, variable names, data types, summary statistics)
- Verification log or notes confirming schema match and absence of missing/malformed entries

## How to apply

First, consult the link-to-codes-and-data-objects file to identify the data object file paths and names. Next, review the Read-Me.txt file to understand the expected data type, dimensionality, variable names, and purpose of each object. Using the appropriate language (R or MATLAB), load each data object via its documented file format (e.g., .RData, .mat, or tabular export). Immediately after loading, inspect the object using language-native introspection (e.g., `str()`, `head()`, `dim()` in R; `whos`, `size()` in MATLAB) to verify dimensions, variable names, and data types match the Read-Me.txt specification. Check for missing values, unexpected NA or NaN entries, and verify that numeric ranges and categorical levels align with the documented sub-sample scenario. Only proceed to execute analysis scripts once all objects pass inspection.

## Related tools

- **R** (Load and inspect data objects using str(), head(), dim(), summary() functions; execute data validation checks)
- **MATLAB** (Load and inspect data objects using load(), whos, size(), and data display functions)
- **DisCoPad repository** (Source repository containing link-to-codes-and-data-objects index, Read-Me.txt documentation, and example data objects) — https://github.com/KechrisLab/DisCoPad

## Examples

```
# R: load and inspect
load('path/to/sub_sample_data.RData')
str(data_object)
dim(data_object)
head(data_object)
```

## Evaluation signals

- Data object loads without error in the target language (R or MATLAB).
- Introspection output (dimensions, variable names, data types) matches the Read-Me.txt specification exactly.
- No missing values (NA, NaN) appear in columns that should be complete according to Read-Me.txt; or missing values are documented and expected.
- Numeric variables fall within the documented range for the sub-sample scenario; categorical variables contain only expected levels.
- Console output or summary statistics are consistent with the documented sample size and feature count in Read-Me.txt.

## Limitations

- The Read-Me.txt file must be comprehensive and accurate; if documentation is incomplete or inconsistent, verification may fail to catch schema mismatches.
- Language-specific introspection tools (R `str()`, MATLAB `whos`) may not catch domain-specific inconsistencies (e.g., physically impossible values, wrong units) that require domain knowledge.
- If the data object file format differs unexpectedly from the documented format (e.g., a CSV stored as .xlsx), standard load functions may fail or produce silent corruption; manual file inspection may be required.
- This skill does not validate that the data are scientifically or statistically appropriate for the downstream analysis; it only checks structure and format.

## Evidence

- [other] Load the sub-sample data object(s) referenced in the link-to-codes-and-data-objects file using the appropriate language (R or MATLAB).: "Load the sub-sample data object(s) referenced in the link-to-codes-and-data-objects file using the appropriate language (R or MATLAB)."
- [other] Consult the Read-Me.txt file to identify which script(s) correspond to the sub-sample simulation and understand the documented purpose and parameters of each.: "Consult the Read-Me.txt file to identify which script(s) correspond to the sub-sample simulation and understand the documented purpose and parameters of each."
- [other] Verify that all simulation outputs (tables, figures, model objects) match the expected format and structure described in Read-Me.txt.: "Verify that all simulation outputs (tables, figures, model objects) match the expected format and structure described in Read-Me.txt."
- [readme] Click on the "link-to-codes-and-data-objects" file to access all codes and related items.: "Click on the "link-to-codes-and-data-objects" file to access all codes and related items."
- [readme] Refer to the "Read-Me.txt" file to understand what each script accomplishes.: "Refer to the "Read-Me.txt" file to understand what each script accomplishes."
