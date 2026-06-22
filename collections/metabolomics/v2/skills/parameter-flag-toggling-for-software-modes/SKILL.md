---
name: parameter-flag-toggling-for-software-modes
description: Use when when integrating edited Modular.r scripts into the LipidMatch-4.2 distribution and you need to switch between Modular mode (standalone R execution with manual or CSV inputs) and Flow mode (integrated pipeline execution).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0331
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - R
  - LipidMatch
  - FluoroMatch
  - Core-Match repository
derived_from:
- doi: 10.1007/s00216-021-03392-7
  title: FluoroMatch 2.0
evidence_spans:
- put Modular.r into two directories
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fluoromatch_2_0_cq
    doi: 10.1007/s00216-021-03392-7
    title: FluoroMatch 2.0
  dedup_kept_from: coll_fluoromatch_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s00216-021-03392-7
  all_source_dois:
  - 10.1007/s00216-021-03392-7
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Parameter Flag Toggling for Software Modes

## Summary

Configure execution mode (Modular vs. Flow) in LipidMatch/FluoroMatch by toggling boolean flags in Modular.r to control data input handling, processing pipeline, and analysis type. This skill ensures the correct algorithmic pathway and dependency chain is activated for the intended workflow.

## When to use

When integrating edited Modular.r scripts into the LipidMatch-4.2 distribution and you need to switch between Modular mode (standalone R execution with manual or CSV inputs) and Flow mode (integrated pipeline execution). Use this skill after downloading the official software from InnovativeOmics.com and before running metabolomics or lipidomics analysis.

## When NOT to use

- Input scripts are already pre-compiled binaries or do not expose configuration flags
- Analysis goal does not require switching between Modular and Flow execution modes
- Software is being run from the official downloaded distribution without local algorithmic edits

## Inputs

- Modular.r script (from github.com/InnovativeOmics/Core-Match repository)
- Target installation directories (LipidMatch-4.2 distribution)

## Outputs

- Edited Modular.r with configured FLOW, csvInput, ManuallyInputVariables, Lipid, and TWeen_pos flags
- Updated script files in LipidMatch_Distribution and FluoroMatch_Modular directories
- Validated R syntax confirmation

## How to apply

Open the Modular.r script in a text editor and locate the configuration flag declarations (FLOW, csvInput, ManuallyInputVariables, Lipid, TWeen_pos). For Modular mode execution, set FLOW <- FALSE, csvInput <- FALSE (or TRUE if using CSV inputs), and ManuallyInputVariables <- FALSE; for Flow mode, set FLOW <- TRUE. Additionally, toggle Lipid and TWeen_pos parameters based on analysis type: set Lipid <- TRUE for lipid analysis, or leave both FALSE to default to PFAS analysis. Save the edited file, then validate syntax by running a parse check in R (e.g., parse(file='Modular.r')) to confirm no syntax errors are present before placing the script into the target directories (LipidMatch_Distribution and FluoroMatch_Modular).

## Related tools

- **LipidMatch** (Primary metabolomics/lipidomics software distribution containing Modular.r configuration) — innovativeomics.com/software
- **FluoroMatch** (Fluorinated compound analysis software using same Modular.r configuration scheme) — innovativeomics.com/software
- **R** (Execution environment for Modular.r script and syntax validation via parse())
- **Core-Match repository** (Source repository where developers edit main algorithms before integration into distributions) — github.com/InnovativeOmics/Core-Match

## Examples

```
# In R: edit Modular.r, then validate
parse(file='Modular.r'); # Returns NULL on success
# Linux/macOS: Copy validated script to both directories
cp Modular.r LipidMatch-4.2/Flow/LipidMatch_Distribution/
cp Modular.r LipidMatch-4.2/FluoroMatch_Modular/
```

## Evaluation signals

- R parse() check returns TRUE with no syntax errors
- Edited Modular.r files successfully copied into both LipidMatch_Distribution and FluoroMatch_Modular directories without file conflicts
- Script execution in chosen mode (Modular or Flow) proceeds without flag-related runtime errors
- Output analysis type matches toggled parameter state (PFAS when Lipid=FALSE and TWeen_pos=FALSE; Lipid analysis when Lipid=TRUE)
- csvInput parameter state matches actual data input method (FALSE for manual input, TRUE for CSV file input)

## Limitations

- Flag configuration is mode-specific; incorrect combinations (e.g., FLOW=TRUE with ManuallyInputVariables=TRUE) may cause runtime errors or undefined behavior
- Changes to Modular.r must be replicated into both target directories to maintain consistency across Flow and Modular versions
- No changelog is provided for tracking which flag changes were applied or their rationale across versions
- Manual validation of syntax is required; automated testing infrastructure for flag combinations is not documented

## Evidence

- [readme] For Modular mode configuration: "For the Modular version set `FLOW <- FALSE` `csvInput <- FALSE #Alternatively you can keep this true and use csv inputs` `ManuallyInputVariables <- FALSE`"
- [readme] For Flow mode configuration: "For the Flow version set `FLOW <- TRUE`"
- [readme] Analysis type toggling: "Make sure to toggle the following parameters depending on your application, if both are FALSE it defaults to PFAS analysis: `Lipid <- TRUE` `TWeen_pos <- FALSE`"
- [readme] Integration workflow requirement: "If edited, put Modular.r into two directories (replace existing code): `LipidMatch-4.2\Flow\LipidMatch_Distribution` `LipidMatch-4.2\FluoroMatch_Modular`"
- [other] Validation step in workflow: "Validate script syntax by running a parse check in R to confirm no syntax errors are present."
