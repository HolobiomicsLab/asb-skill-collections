---
name: cross-language-workflow-orchestration
description: Use when you have multi-language code implementations (R and MATLAB scripts) for a single scientific workflow, documented example scripts for a reference sub-sample scenario, and need to verify that outputs from one language can serve as inputs to the next, or that both implementations produce.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3552
  edam_topics: []
  tools:
  - R
  - MATLAB
  - DisCoPad repository (KechrisLab)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-language-workflow-orchestration

## Summary

Execute a coordinated simulation workflow across R and MATLAB environments using documented example scripts and shared data objects. This skill is essential when a single analysis requires language-specific implementations (e.g., statistical modeling in R, visualization or specialized toolboxes in MATLAB) and reproducibility depends on sequencing and validation across both platforms.

## When to use

You have multi-language code implementations (R and MATLAB scripts) for a single scientific workflow, documented example scripts for a reference sub-sample scenario, and need to verify that outputs from one language can serve as inputs to the next, or that both implementations produce consistent results on the same data.

## When NOT to use

- Only one language implementation exists (use single-language execution instead)
- Scripts lack documented dependencies or sequencing (resolve documentation gaps first)
- Data objects do not have explicit format mappings between R and MATLAB (establish those mappings before orchestration)

## Inputs

- R scripts from Codes-Explained folder
- MATLAB scripts from Codes-Explained folder
- Data sub-sample objects referenced in link-to-codes-and-data-objects file
- Read-Me.txt workflow documentation

## Outputs

- Intermediate R outputs (console logs, saved objects, intermediate tables)
- Intermediate MATLAB outputs (console logs, saved .mat files, intermediate matrices)
- Final simulation tables and figures matching documented schema
- Model objects from both R and MATLAB environments
- Validation report comparing outputs across languages

## How to apply

Begin by consulting the Read-Me.txt file to understand the dependency order and purpose of each script. Load the reference data sub-sample using the link-to-codes-and-data-objects file, which maps data objects to their language-specific variable formats. Execute R scripts in their documented sequence, capturing console output and intermediate file writes to verify correctness before proceeding to dependent steps. Then execute the corresponding MATLAB scripts in sequence, using the same or transformed intermediate outputs as inputs. After each language-specific phase, verify that output objects (tables, model structures, figures) match the expected schema documented in Read-Me.txt. Compare final outputs across languages to detect format mismatches or numerical divergence that would indicate a workflow orchestration error.

## Related tools

- **R** (Execute statistical and data transformation scripts in sequence; produce intermediate objects and outputs passed to MATLAB phase)
- **MATLAB** (Execute specialized computation and visualization scripts that consume R outputs or operate on shared data objects; produce final simulation figures and model structures)
- **DisCoPad repository (KechrisLab)** (Central archive storing example scripts, data sub-samples, workflow documentation (Read-Me.txt), and link-to-codes-and-data-objects reference file) — https://github.com/KechrisLab/DisCoPad

## Evaluation signals

- All R scripts execute without errors and produce documented intermediate objects matching the Read-Me.txt schema
- All MATLAB scripts execute without errors, successfully load R-generated intermediate outputs, and produce documented final outputs
- Intermediate file writes (from both R and MATLAB) are present, readable, and contain expected data types and dimensions
- Final output tables, figures, and model objects match the format, structure, and value ranges specified in Read-Me.txt
- Cross-language comparison of shared numerical outputs (e.g., statistics, parameters) shows agreement within documented tolerance (if specified)

## Limitations

- Workflow is documented and validated only for a single data sub-sample scenario; extension to other sub-samples or full datasets may reveal undocumented dependencies or format incompatibilities
- Script execution order is critical and must be followed exactly as documented; deviations or parallel execution may cause data availability or format errors
- Data object serialization formats (R .RData vs MATLAB .mat) may require explicit conversion steps not covered in the basic Read-Me.txt documentation

## Evidence

- [readme] Check out "Codes-Explained" folder to find all the example R and MATLAB codes (for one data sub-sample scenario) used for the simulation.: "Check out "Codes-Explained" folder to find all the example R and MATLAB codes (for one data sub-sample scenario) used for the simulation."
- [readme] Refer to the "Read-Me.txt" file to understand what each script accomplishes.: "Refer to the "Read-Me.txt" file to understand what each script accomplishes."
- [intro] Consult the Read-Me.txt file to identify which script(s) correspond to the sub-sample simulation and understand the documented purpose and parameters of each.: "Consult the Read-Me.txt file to identify which script(s) correspond to the sub-sample simulation and understand the documented purpose and parameters of each."
- [intro] Execute the R script(s) in sequence, monitoring console output and intermediate file writes for correctness.: "Execute the R script(s) in sequence, monitoring console output and intermediate file writes for correctness."
- [intro] Execute the MATLAB script(s) in sequence, monitoring console output and intermediate file writes for correctness.: "Execute the MATLAB script(s) in sequence, monitoring console output and intermediate file writes for correctness."
- [intro] Verify that all simulation outputs (tables, figures, model objects) match the expected format and structure described in Read-Me.txt.: "Verify that all simulation outputs (tables, figures, model objects) match the expected format and structure described in Read-Me.txt."
