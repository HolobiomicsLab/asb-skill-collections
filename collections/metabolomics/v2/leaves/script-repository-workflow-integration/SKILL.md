---
name: script-repository-workflow-integration
description: Use when you have cloned or downloaded scripts from a development repository
  (e.g., github.com/InnovativeOmics/Core-Match) and need to incorporate edits into
  an installed distribution copy of LipidMatch-4.2 or FluoroMatch.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - R
  - LipidMatch
  - FluoroMatch
  - Core-Match repository
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# script-repository-workflow-integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Integrate edited R scripts from a developer repository into a distributed software installation by placing files into version-specific directories and configuring execution mode flags. This skill ensures that locally modified algorithms (e.g., Modular.r, genEIC.r) are correctly staged for both Flow and Modular execution modes in LipidMatch or FluoroMatch.

## When to use

You have cloned or downloaded scripts from a development repository (e.g., github.com/InnovativeOmics/Core-Match) and need to incorporate edits into an installed distribution copy of LipidMatch-4.2 or FluoroMatch. Use this skill when you have modified core algorithms and need to replace the bundled versions while preserving the correct directory structure and mode-specific parameter settings.

## When NOT to use

- You are using end-user downloads from innovativeomics.com/software and do not intend to modify the core algorithms — use the default installation as-is.
- Your edited scripts are designed for a different software version or tool (LipidMatch-4.1, PolyMatch) — verify compatibility before integration.
- You lack the installed reference distribution on your system — install from innovativeomics.com/software first to establish the required directory structure.

## Inputs

- Edited R scripts from development repository (Modular.r, genEIC.r, MS1Spectragen.r, Stats.R)
- Installed LipidMatch-4.2 or FluoroMatch distribution directory
- Configuration parameters (FLOW, csvInput, ManuallyInputVariables, Lipid, TWeen_pos)

## Outputs

- Integrated Modular.r file in both Flow and Modular version directories
- Updated script files in LipidMatch_Libraries/Scripts subdirectory
- Configured Modular.r with mode-specific parameter settings (FLOW=TRUE or FALSE)
- Validated R scripts free of syntax errors

## How to apply

First, install the target software (LipidMatch or FluoroMatch) from innovativeomics.com/software to establish the reference directory structure. Then, copy your edited Modular.r file into both `LipidMatch-4.2\Flow\LipidMatch_Distribution` and `LipidMatch-4.2\FluoroMatch_Modular`, replacing the existing code. Place any other edited scripts (genEIC.r, MS1Spectragen.r, Stats.R) into `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`. Next, configure the execution mode by setting `FLOW <- FALSE` for Modular mode or `FLOW <- TRUE` for Flow mode in the appropriate installed copy. Optionally configure csvInput and ManuallyInputVariables flags according to your input strategy. Finally, validate the edited script by running a syntax check in R (e.g., `parse(file='path/to/Modular.r')`) to confirm no parsing errors before testing.

## Related tools

- **LipidMatch** (Target distribution software into which edited Modular.r and supporting scripts are integrated) — https://innovativeomics.com/software
- **FluoroMatch** (Alternative target distribution software supporting Modular mode for script integration) — https://innovativeomics.com/software
- **R** (Environment for editing, validating, and executing the integrated scripts; used for syntax checking and parse validation)
- **Core-Match repository** (Source repository from which edited scripts are retrieved and modified by developers before integration into distributions) — https://github.com/InnovativeOmics/Core-Match

## Examples

```
# In R: validate edited Modular.r before integration
parse(file='LipidMatch-4.2/Flow/LipidMatch_Distribution/Modular.r')
# Then set mode via text editor: FLOW <- FALSE
```

## Evaluation signals

- Modular.r file exists in both `LipidMatch-4.2\Flow\LipidMatch_Distribution` and `LipidMatch-4.2\FluoroMatch_Modular` directories with identical edited content.
- Script support files (genEIC.r, MS1Spectragen.r, Stats.R) are present in `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts` directory.
- R syntax validation command `parse(file='path/to/Modular.r')` executes without errors, confirming no parsing errors.
- Configuration flags in the integrated Modular.r match the intended mode: `FLOW <- FALSE` for Modular version, `FLOW <- TRUE` for Flow version.
- Application mode parameters (Lipid, TWeen_pos) are set according to intended analysis type (PFAS, Lipid, or TWeen_pos analysis).

## Limitations

- No changelog is available to track what changes have been made to scripts in the development repository, making it difficult to audit modifications.
- The integration workflow requires manual placement into multiple directories; there is no automated build or deployment system documented, increasing risk of placement errors.
- Configuration flags (FLOW, csvInput, ManuallyInputVariables) must be manually set for each version; no validation script is provided to verify correct flag combinations before execution.
- The workflow assumes Windows-style directory paths (`\` separators); adaptation may be needed for Linux/macOS installations.

## Evidence

- [readme] Developers can retrieve edited scripts from the Core-Match repository: "**Developers can edit the main algorithms here on github** as a team."
- [readme] Edited Modular.r must replace existing code in two specific directories: "If edited, put Modular.r into two directories (replace existing code): `LipidMatch-4.2\Flow\LipidMatch_Distribution` `LipidMatch-4.2\FluoroMatch_Modular`"
- [readme] Supporting script files must be placed in a specific library subdirectory: "Place any edited script files (genEIC.r, MS1Spectragen.r, Stats.R) into: `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`"
- [readme] Execution mode is controlled by the FLOW configuration flag: "For the Modular version set `FLOW <- FALSE` ... For the Flow version set `FLOW <- TRUE`"
- [readme] Optional CSV input handling is configured via csvInput flag: "`csvInput <- FALSE #Alternatively you can keep this true and use csv inputs`"
- [readme] Analysis mode is toggled via Lipid and TWeen_pos parameters: "Make sure to toggle the following parameters depending on your application, if both are FALSE it defaults to PFAS analysis: `Lipid <- TRUE` `TWeen_pos <- FALSE`"
- [readme] Users should download the distribution from the official website: "For LipidMatch, FluoroMatch, and PolyMatch **users should directly download from innovativeomics.com/software** for the latest stable release."
