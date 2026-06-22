---
name: matlab-script-execution
description: Use when you have located MATLAB scripts in a Codes-Explained folder with accompanying Read-Me.
license: CC-BY-4.0
metadata:
  edam_topics: []
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
---

# matlab-script-execution

## Summary

Execute MATLAB scripts in sequence as part of a documented simulation workflow, monitoring console output and intermediate file writes to verify correct computation. This skill is applied when reconstructing or validating a multi-language (R + MATLAB) simulation procedure on a reference data sub-sample.

## When to use

You have located MATLAB scripts in a Codes-Explained folder with accompanying Read-Me.txt documentation, have loaded the corresponding sub-sample data objects, and need to run the MATLAB component of a multi-language simulation workflow to generate tables, figures, and model objects for validation or reproduction.

## When NOT to use

- The MATLAB scripts are not documented in a Read-Me.txt file or equivalent specification—execution without clear purpose and expected outputs increases risk of silent failure or misinterpretation.
- Input data objects have not been loaded or validated prior to script execution—running scripts on unverified or missing data will produce unreliable outputs.
- You are executing a full production pipeline rather than a single documented sub-sample scenario—use this skill for reconstruction and validation on reference data; scale to full datasets only after correctness is established.

## Inputs

- MATLAB script files (.m) from Codes-Explained folder
- Sub-sample data objects (referenced in link-to-codes-and-data-objects file)
- Read-Me.txt documentation file describing script purpose and parameters
- Any intermediate .mat or data files produced by prior scripts in the sequence

## Outputs

- Console output and error logs
- Intermediate .mat files or exported data (e.g., .csv tables)
- Generated figures (e.g., .fig, .png files)
- Model objects (parameter estimates, residuals, diagnostic statistics)
- Log files documenting execution metadata

## How to apply

First, consult the Read-Me.txt file to identify which MATLAB script(s) correspond to your simulation scenario and their execution order, parameters, and expected outputs. Load the documented sub-sample data object(s) into the MATLAB workspace using the appropriate load() or readtable() command as referenced in the link-to-codes-and-data-objects file. Execute each MATLAB script in the documented sequence, monitoring the console for errors and tracking intermediate file writes (e.g., .mat files, .csv exports, or figure saves) to verify each step completes successfully. After execution, verify that all simulation outputs (tables, figures, model objects) match the expected format, structure, and content described in the Read-Me.txt file—this validation step ensures correctness before proceeding to downstream analysis or cross-validation with R outputs.

## Related tools

- **MATLAB** (Execution engine for simulation scripts; runs sequential computations on sub-sample data and produces tables, figures, and model objects)
- **DisCoPad repository** (Source repository containing Codes-Explained folder with example MATLAB scripts, Read-Me.txt documentation, and link-to-codes-and-data-objects file) — https://github.com/KechrisLab/DisCoPad

## Evaluation signals

- Console output completes without runtime errors or warnings for each script execution.
- Intermediate files (e.g., .mat, .csv) are created at expected file paths and contain non-empty, valid data.
- Generated figures display expected plots, axes labels, and legend entries consistent with Read-Me.txt descriptions.
- Final model objects (parameter tables, statistics structures) match the schema and value ranges documented in Read-Me.txt.
- Outputs can be successfully loaded and compared against reference outputs from the R implementation (cross-language validation).

## Limitations

- This skill targets a single, documented sub-sample scenario; scaling to full datasets or undocumented data requires adaptation and additional validation.
- Success depends entirely on accuracy and completeness of the Read-Me.txt documentation; gaps or outdated documentation will cause execution or validation to fail.
- Cross-validation between R and MATLAB outputs is recommended but not performed by this skill alone; separate comparison workflow may be required.

## Evidence

- [other] Execute the MATLAB script(s) in sequence, monitoring console output and intermediate file writes for correctness.: "Execute the MATLAB script(s) in sequence, monitoring console output and intermediate file writes for correctness."
- [readme] Check out "Codes-Explained" folder to find all the example R and MATLAB codes (for one data sub-sample scenario) used for the simulation. Refer to the "Read-Me.txt" file to understand what each script accomplishes.: "Check out "Codes-Explained" folder to find all the example R and MATLAB codes (for one data sub-sample scenario) used for the simulation. Refer to the "Read-Me.txt" file to understand what each"
- [other] Verify that all simulation outputs (tables, figures, model objects) match the expected format and structure described in Read-Me.txt.: "Verify that all simulation outputs (tables, figures, model objects) match the expected format and structure described in Read-Me.txt."
- [other] Load the sub-sample data object(s) referenced in the link-to-codes-and-data-objects file using the appropriate language (R or MATLAB).: "Load the sub-sample data object(s) referenced in the link-to-codes-and-data-objects file using the appropriate language (R or MATLAB)."
