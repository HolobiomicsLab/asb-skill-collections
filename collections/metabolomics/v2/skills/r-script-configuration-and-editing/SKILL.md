---
name: r-script-configuration-and-editing
description: Use when you need to switch between Modular and Flow execution modes in LipidMatch/FluoroMatch, or when you need to change the analysis application type (PFAS analysis, Lipid analysis, or TWeen_pos analysis).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_3577
  tools:
  - R
  - LipidMatch
  - FluoroMatch
  - PolyMatch
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

# R Script Configuration and Editing

## Summary

Configure and edit R scripts (particularly Modular.r) to toggle between execution modes (Modular vs. Flow) and analysis application types (PFAS, Lipid, or TWeen_pos) by setting boolean flags and integrating modified code into the correct software distribution directories. This skill is essential when adapting LipidMatch, FluoroMatch, or PolyMatch workflows to specific analytical goals and execution paradigms.

## When to use

Apply this skill when you need to switch between Modular and Flow execution modes in LipidMatch/FluoroMatch, or when you need to change the analysis application type (PFAS analysis, Lipid analysis, or TWeen_pos analysis). Use it after cloning or downloading the Core-Match repository and before integrating edited scripts into the installed software distribution.

## When NOT to use

- You are working with the distributed binary release from innovativeomics.com/software and do not need to modify algorithm code — use the pre-configured parameters instead.
- You are not integrating developer-level changes into the software framework — if you only need to run pre-installed LipidMatch/FluoroMatch with default settings, this skill is unnecessary.
- Input files are already in the expected format and no mode or application toggling is required.

## Inputs

- Modular.r source file (from github.com/InnovativeOmics/Core-Match)
- Text editor or R IDE
- Installed LipidMatch/FluoroMatch distribution directory structure

## Outputs

- Edited Modular.r with configured FLOW, csvInput, ManuallyInputVariables, Lipid, and TWeen_pos boolean flags
- Script files copied to LipidMatch-4.2\Flow\LipidMatch_Distribution and LipidMatch-4.2\FluoroMatch_Modular directories
- R syntax validation report (parse check results)

## How to apply

Retrieve Modular.r from the github.com/InnovativeOmics/Core-Match repository and open it in a text editor. Locate the configuration flag declarations (FLOW, csvInput, ManuallyInputVariables, Lipid, TWeen_pos). For Modular mode execution, set FLOW <- FALSE, csvInput <- FALSE (or TRUE for CSV inputs), and ManuallyInputVariables <- FALSE; for Flow mode, set FLOW <- TRUE. To select analysis application, set Lipid <- TRUE and TWeen_pos <- FALSE for lipid analysis, or leave both FALSE to default to PFAS analysis. After editing, validate script syntax by running a parse check in R (e.g., source() with error handling). Finally, place the edited Modular.r file into both required directories: LipidMatch-4.2\Flow\LipidMatch_Distribution and LipidMatch-4.2\FluoroMatch_Modular, replacing existing code. Place any other edited script files (genEIC.r, MS1Spectragen.r, Stats.R) into LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts.

## Related tools

- **R** (Script execution environment and syntax validation for Modular.r and related analysis scripts)
- **LipidMatch** (Target software distribution into which edited Modular.r is integrated for lipid/metabolite identification workflows) — https://github.com/InnovativeOmics/Core-Match
- **FluoroMatch** (Target software distribution into which edited Modular.r is integrated for fluorine-containing compound analysis) — https://github.com/InnovativeOmics/Core-Match
- **PolyMatch** (Related target software distribution supporting similar configuration and editing workflows) — https://github.com/InnovativeOmics/Core-Match

## Examples

```
# In R: parse and validate Modular.r syntax
parse(file='Modular.r')
# Then manually edit Modular.r to set: FLOW <- FALSE; csvInput <- FALSE; ManuallyInputVariables <- FALSE; Lipid <- TRUE; TWeen_pos <- FALSE
# Finally copy edited file: file.copy('Modular.r', 'LipidMatch-4.2/Flow/LipidMatch_Distribution/Modular.r', overwrite=TRUE)
```

## Evaluation signals

- R script syntax validation completes without errors when running parse check (e.g., parse(file='Modular.r') succeeds).
- Configuration flags are explicitly set to the target values (FLOW = TRUE or FALSE, csvInput = TRUE or FALSE, ManuallyInputVariables = FALSE for Modular mode; FLOW = TRUE for Flow mode).
- Edited Modular.r file is present in both required directories: LipidMatch-4.2\Flow\LipidMatch_Distribution and LipidMatch-4.2\FluoroMatch_Modular, confirmed by file existence and timestamp checks.
- Application-specific parameters (Lipid, TWeen_pos) match the intended analysis type: both FALSE defaults to PFAS analysis; Lipid=TRUE and TWeen_pos=FALSE selects lipid analysis.
- Software launches with the edited Modular.r and executes in the selected mode without configuration-related errors (verified by running a test analysis and checking for mode-specific behavior).

## Limitations

- Manual file placement into two separate directory locations increases risk of synchronization errors if both copies are not updated together.
- No automated changelog or version tracking is provided, making it difficult to audit which configuration changes were applied across distributed copies.
- Syntax validation does not guarantee functional correctness — parse check only confirms R syntax, not algorithm logic or compatibility with downstream dependencies.
- Configuration flags must be manually edited in plaintext; no configuration file or GUI is mentioned, making bulk or template-based deployments more error-prone.

## Evidence

- [readme] For the Modular version set `FLOW <- FALSE` `csvInput <- FALSE #Alternatively you can keep this true and use csv inputs` `ManuallyInputVariables <- FALSE`: "For the Modular version set `FLOW <- FALSE` `csvInput <- FALSE #Alternatively you can keep this true and use csv inputs` `ManuallyInputVariables <- FALSE`"
- [readme] For the Flow version set `FLOW <- TRUE`: "For the Flow version set `FLOW <- TRUE`"
- [readme] Make sure to toggle the following parameters depending on your application, if both are FALSE it defaults to PFAS analysis: `Lipid <- TRUE` `TWeen_pos <- FALSE`: "Make sure to toggle the following parameters depending on your application, if both are FALSE it defaults to PFAS analysis: `Lipid <- TRUE` `TWeen_pos <- FALSE`"
- [readme] put Modular.r into two directories (replace existing code): `LipidMatch-4.2\Flow\LipidMatch_Distribution` `LipidMatch-4.2\FluoroMatch_Modular`: "put Modular.r into two directories (replace existing code): `LipidMatch-4.2\Flow\LipidMatch_Distribution` `LipidMatch-4.2\FluoroMatch_Modular`"
- [readme] Place any edited script files (genEIC.r, MS1Spectragen.r, Stats.R) into: `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`: "Place any edited script files (genEIC.r, MS1Spectragen.r, Stats.R) into: `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`"
- [other] Modular mode requires setting FLOW to FALSE, csvInput to FALSE (or optionally TRUE for CSV inputs), and ManuallyInputVariables to FALSE, while Flow mode requires setting FLOW to TRUE.: "Modular mode requires setting FLOW to FALSE, csvInput to FALSE (or optionally TRUE for CSV inputs), and ManuallyInputVariables to FALSE, while Flow mode requires setting FLOW to TRUE."
- [other] Validate script syntax by running a parse check in R to confirm no syntax errors are present.: "Validate script syntax by running a parse check in R to confirm no syntax errors are present."
