---
name: documentation-driven-reproducibility
description: Use when you have inherited a multi-language analysis codebase (R and/or
  MATLAB scripts) with accompanying documentation (Read-Me.txt, link-to-codes-and-data-objects
  files) and need to verify that the entire simulation workflow runs correctly on
  a reference dataset (typically a sub-sample scenario).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MATLAB
  - DisCoPad
  license_tier: restricted
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

# documentation-driven-reproducibility

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A workflow for reconstructing and validating a complete simulation or analysis pipeline by executing example scripts in a documented sequence, cross-referencing code documentation (Read-Me files) with intermediate outputs to verify correctness at each stage. This skill ensures that complex multi-language workflows (R, MATLAB) produce expected outputs and remain reproducible across environments.

## When to use

You have inherited a multi-language analysis codebase (R and/or MATLAB scripts) with accompanying documentation (Read-Me.txt, link-to-codes-and-data-objects files) and need to verify that the entire simulation workflow runs correctly on a reference dataset (typically a sub-sample scenario). Use this skill when you cannot assume the code runs as-is, when intermediate file writes and console outputs must be inspected for correctness, or when you need to establish a ground-truth execution baseline before scaling to larger datasets.

## When NOT to use

- Code is already validated and published (skip reconstruction and move directly to production dataset application).
- Reference sub-sample data and documentation files are not available in the repository (cannot establish ground truth).
- Scripts contain undocumented external dependencies or require a specific hardware/OS/library version not mentioned in the Read-Me (reproducibility may fail unpredictably).

## Inputs

- R and MATLAB scripts (source code files)
- Reference data sub-sample object(s) (referenced via link-to-codes-and-data-objects file)
- Read-Me.txt file (script documentation and expected output specifications)
- link-to-codes-and-data-objects file (index to codes and data objects)

## Outputs

- Executed R and MATLAB scripts with console output logs
- Intermediate simulation files (tables, figures, model objects)
- Final simulation outputs (tables, figures, model objects)
- Verification report matching output schema and structure to Read-Me.txt documentation

## How to apply

Begin by consulting the link-to-codes-and-data-objects file to identify all required code scripts and their corresponding reference data objects. Read the Read-Me.txt file to understand the documented purpose, input parameters, and expected outputs of each script. Load the reference data object(s) into the appropriate language environment (R or MATLAB) using the documented file paths and load functions. Execute the R script(s) in the documented sequence, monitoring console output and checking for intermediate file writes (tables, figures, model objects) that match the documented structure. Repeat for MATLAB script(s) in sequence. After each script executes, verify that all generated outputs (intermediate and final) conform to the format, schema, and dimensions documented in the Read-Me.txt file. Cross-reference intermediate outputs with subsequent script inputs to detect pipeline breaks. Document any deviations from expected behavior.

## Related tools

- **R** (Execute R scripts in sequence, loading and processing reference sub-sample data, writing intermediate simulation outputs for verification)
- **MATLAB** (Execute MATLAB scripts in sequence, loading and processing reference sub-sample data, writing intermediate simulation outputs for verification)
- **DisCoPad** (Repository containing all example R and MATLAB codes, reference data objects, code-to-data links, and Read-Me documentation for the reference simulation workflow) — https://github.com/KechrisLab/DisCoPad

## Evaluation signals

- Console output from each script executes without errors or warnings related to missing data, undefined variables, or type mismatches.
- All intermediate file writes (tables, figures, model objects) are produced and can be read back into the same environment without corruption or schema violations.
- Dimensions, data types, and column/field names of all outputs match those documented in the Read-Me.txt file exactly.
- Output values (e.g., model coefficients, summary statistics, figure axis ranges) fall within documented expected ranges or match reference checksums/digests provided in the documentation.
- Downstream scripts execute successfully using intermediate outputs from upstream scripts, indicating no pipeline breaks in data format or dimensionality.

## Limitations

- Verification is limited to a single sub-sample scenario; scaling to full dataset may expose memory, numerical stability, or performance issues not present in the reference run.
- Documentation accuracy depends on the completeness and currency of the Read-Me.txt and link-to-codes-and-data-objects files; if documentation is stale or incomplete, verification may pass despite incorrect implementation.
- Cross-language execution (R and MATLAB together) introduces environment-specific pitfalls (library versions, floating-point precision, file path separators) that a single-language reference run would not reveal.
- Console output inspection and intermediate file verification are manual and labor-intensive; small deviations in numeric output (e.g., due to randomization, optimization convergence) may be missed if not explicitly flagged in documentation.

## Evidence

- [readme] Check out "Codes-Explained" folder to find all the example R and MATLAB codes (for one data sub-sample scenario) used for the simulation.: "Check out "Codes-Explained" folder to find all the example R and MATLAB codes (for one data sub-sample scenario)"
- [readme] Refer to the "Read-Me.txt" file to understand what each script accomplishes.: "Refer to the "Read-Me.txt" file to understand what each script accomplishes"
- [readme] Click on the "link-to-codes-and-data-objects" file to access all codes and related items.: "Click on the "link-to-codes-and-data-objects" file to access all codes and related items"
- [intro] Load the sub-sample data object(s) referenced in the link-to-codes-and-data-objects file using the appropriate language (R or MATLAB). Execute the R script(s) in sequence, monitoring console output and intermediate file writes for correctness.: "Load the sub-sample data object(s) referenced in the link-to-codes-and-data-objects file using the appropriate language (R or MATLAB). Execute the R script(s) in sequence, monitoring console output"
- [intro] Verify that all simulation outputs (tables, figures, model objects) match the expected format and structure described in Read-Me.txt.: "Verify that all simulation outputs (tables, figures, model objects) match the expected format and structure described in Read-Me.txt"
