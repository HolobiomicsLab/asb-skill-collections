---
name: simulation-output-validation
description: Use when after executing a multi-stage simulation workflow in R and/or
  MATLAB, when you have generated intermediate and final outputs (tables, figures,
  model objects) and need to confirm that all artifacts conform to the documented
  format, structure, and expected content before downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2945
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - MATLAB
  - Python
  - Jupyter
  license_tier: restricted
derived_from:
- doi: 10.3390/metabo15010028
  title: DisCo P-ad
- doi: 10.1371/journal.pcbi.1009105
  title: ''
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
  - build: coll_ora
    doi: 10.1371/journal.pcbi.1009105
    title: ORA
  dedup_kept_from: coll_disco_p_ad_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo15010028
  all_source_dois:
  - 10.3390/metabo15010028
  - 10.1371/journal.pcbi.1009105
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# simulation-output-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Verify that simulation outputs (tables, figures, model objects) match expected format, structure, and content as documented in reference materials. This skill ensures reproducibility and correctness of computational workflows by systematically comparing generated artifacts against documented specifications.

## When to use

After executing a multi-stage simulation workflow in R and/or MATLAB, when you have generated intermediate and final outputs (tables, figures, model objects) and need to confirm that all artifacts conform to the documented format, structure, and expected content before downstream analysis or publication.

## When NOT to use

- Simulation scripts have not yet been executed; validation requires actual output artifacts to inspect.
- No documentation (Read-Me.txt or equivalent) exists that specifies the expected format and structure of outputs.
- The analysis goal is exploratory model development rather than reproducibility verification of a published workflow.

## Inputs

- Executed R scripts from Codes-Explained folder
- Executed MATLAB scripts from Codes-Explained folder
- Console output logs from script execution
- Intermediate and final output files (tables, figures, model objects)
- Read-Me.txt file with documented output specifications
- link-to-codes-and-data-objects reference file

## Outputs

- Validation report confirming format and structure correctness
- List of matched outputs (tables, figures, model objects) and their specifications
- Documentation of any discrepancies between expected and actual outputs
- Verification checkpoints from console output and intermediate file writes

## How to apply

Execute the simulation scripts (R and MATLAB) in sequence as specified in the workflow documentation, then systematically verify each output by comparing its structure, dimensionality, data types, and summary statistics against the specifications documented in the Read-Me.txt file. Check that all expected tables and figures are present, that numerical outputs fall within plausible ranges, and that model objects contain the required fields and metadata. Use console output and intermediate file writes as checkpoints during execution to catch errors early. Document any discrepancies between actual outputs and documented expectations, and trace them back to script parameters or data object specifications to identify whether the deviation is a genuine error or an expected variation.

## Related tools

- **R** (Execute simulation scripts and generate outputs (tables, figures, model objects) for validation) — https://www.r-project.org
- **MATLAB** (Execute simulation scripts and generate outputs (tables, figures, model objects) for validation) — https://www.mathworks.com/products/matlab.html

## Evaluation signals

- All expected output files (tables, figures, model objects) are present in the designated output directory after script execution.
- Output data structures (matrix dimensions, table column names, field names in model objects) exactly match the specifications documented in Read-Me.txt.
- Numerical outputs fall within the expected range and distribution as documented; spot-check summary statistics (mean, SD, min, max) against reference values.
- Console output and intermediate file writes during execution contain no error or warning messages indicating failed computations or data misalignment.
- Metadata and provenance fields in output objects (e.g., script name, execution timestamp, parameter values) are correctly populated and traceable to input scripts and data sub-sample scenario.

## Limitations

- Validation is confined to format and structure correctness; it does not assess whether the simulation results are statistically or scientifically meaningful.
- Validation requires reference documentation (Read-Me.txt) to be present and accurate; if documentation is incomplete or incorrect, validation may pass spuriously or fail incorrectly.
- Cross-language comparison between R and MATLAB outputs may be complicated by numerical precision differences and data type representations; a tolerance threshold for floating-point comparisons may be needed.
- Validation of a single documented sub-sample scenario may not generalize to other data sub-samples or parameter configurations not covered in the provided example scripts.

## Evidence

- [other] Verify that all simulation outputs (tables, figures, model objects) match the expected format and structure described in Read-Me.txt.: "Verify that all simulation outputs (tables, figures, model objects) match the expected format and structure described in Read-Me.txt."
- [other] Execute the R script(s) in sequence, monitoring console output and intermediate file writes for correctness.: "Execute the R script(s) in sequence, monitoring console output and intermediate file writes for correctness."
- [other] Execute the MATLAB script(s) in sequence, monitoring console output and intermediate file writes for correctness.: "Execute the MATLAB script(s) in sequence, monitoring console output and intermediate file writes for correctness."
- [readme] Refer to the "Read-Me.txt" file to understand what each script accomplishes.: "Refer to the "Read-Me.txt" file to understand what each script accomplishes."
