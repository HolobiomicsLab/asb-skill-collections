---
name: version-specific-deployment-configuration
description: Use when you have edited core R scripts (Modular.r, genEIC.r, MS1Spectragen.r,
  Stats.R) in the InnovativeOmics/Core-Match repository on GitHub and need to integrate
  those changes into a local LipidMatch-4.2 or FluoroMatch distribution.
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_3172
  tools:
  - R
  - LipidMatch
  - FluoroMatch
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1007/s00216-021-03392-7
  title: FluoroMatch 2.0
evidence_spans:
- put Modular.r into two directories
- 'put Modular.r into two directories (replace existing code): `LipidMatch-4.2\Flow\LipidMatch_Distribution`'
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

# version-specific-deployment-configuration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Configure and deploy edited R scripts into version-specific directories within the LipidMatch-4.2 distribution framework, ensuring correct parameter settings and file placement for either Flow or Modular analysis modes. This skill bridges developer-side algorithm edits on GitHub with end-user installations.

## When to use

You have edited core R scripts (Modular.r, genEIC.r, MS1Spectragen.r, Stats.R) in the InnovativeOmics/Core-Match repository on GitHub and need to integrate those changes into a local LipidMatch-4.2 or FluoroMatch distribution. Use this skill when you must decide whether to target the Flow version (FLOW <- TRUE) or Modular version (FLOW <- FALSE), and route files to the correct subdirectories to avoid conflicts between pipeline modes.

## When NOT to use

- You are an end user downloading LipidMatch from innovativeomics.com for the first time — use the pre-packaged distribution directly without editing or redeploying scripts.
- Your edits are isolated to a single analysis and you do not need to integrate them into the main distribution framework for repeated use.
- You are uncertain whether Modular.r should replace existing code in both directories or only one — clarify with the development team before deploying.

## Inputs

- Edited R script files (Modular.r, genEIC.r, MS1Spectragen.r, Stats.R) from InnovativeOmics/Core-Match GitHub repository
- LipidMatch-4.2 distribution directory tree downloaded from innovativeomics.com
- README or methods specification documenting target paths
- Information about intended analysis mode (Flow vs. Modular) and application type (Lipid, PFAS, or TWeen_pos)

## Outputs

- Configured Modular.r with FLOW parameter set to TRUE or FALSE
- Deployed script files in correct version-specific directories (Flow and/or Modular paths)
- Manifest or layout document mapping source files to target paths
- Validated directory structure with all edited scripts in place and ready for execution

## How to apply

After downloading the LipidMatch-4.2 distribution from innovativeomics.com, identify which pipeline mode (Flow or Modular) your edits target. For Modular.r, place the edited file into both `LipidMatch-4.2\Flow\LipidMatch_Distribution` and `LipidMatch-4.2\FluoroMatch_Modular`, replacing existing code in each. For all other edited script files (genEIC.r, MS1Spectragen.r, Stats.R), route them into the shared library path `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`. Open the main Modular.r file and set `FLOW <- FALSE` for Modular version or `FLOW <- TRUE` for Flow version. Additionally, toggle application-specific parameters: set `Lipid <- TRUE` and `TWeen_pos <- FALSE` for lipid analysis, or leave both FALSE to default to PFAS analysis. Verify all target directories exist; if they do not, refer to the distribution template or contact the developers.

## Related tools

- **LipidMatch** (Target software framework into which edited scripts are deployed; supports both Flow and Modular pipeline modes) — https://github.com/InnovativeOmics/Core-Match
- **FluoroMatch** (Alternative LipidMatch-based distribution that shares the Modular.r script in FluoroMatch_Modular directory) — https://github.com/InnovativeOmics/Core-Match
- **R** (Execution environment for all deployed script files and configuration parameters)

## Evaluation signals

- Modular.r file exists and contains the correct FLOW parameter value (TRUE or FALSE) matching the target pipeline mode
- All edited script files (genEIC.r, MS1Spectragen.r, Stats.R) are present in `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`
- Modular.r is deployed in both `LipidMatch-4.2\Flow\LipidMatch_Distribution` and `LipidMatch-4.2\FluoroMatch_Modular` directories if targeting Modular mode
- Application-specific parameters (Lipid, TWeen_pos) are set correctly in Modular.r and match the intended analysis type
- Directory manifest or layout document reconciles all source files to their target paths with no missing or conflicting mappings

## Limitations

- Modular.r must be placed into two separate directories to support both Flow and Modular versions; failure to do so will break one of the pipeline modes.
- No changelog is provided in the repository, so developers must manually track which scripts were edited and communicate changes to the team.
- Configuration is file-path and parameter-based; no automated deployment or validation tool is mentioned, so manual verification is required.
- Edits made on GitHub are not automatically integrated into user distributions; developers must follow the manual deployment process and contact the team with major changes.

## Evidence

- [readme] Install FluoroMatch or LipidMatch from InnovativeOmics.com: "Install FluoroMatch or LipidMatch from InnovativeOmics.com"
- [readme] Modular.r must be placed in two directories (Flow and Modular): "put Modular.r into two directories (replace existing code): `LipidMatch-4.2\Flow\LipidMatch_Distribution` `LipidMatch-4.2\FluoroMatch_Modular`"
- [readme] Other edited scripts are placed in the LipidMatch_Libraries/Scripts subdirectory: "Place any edited script files (genEIC.r, MS1Spectragen.r, Stats.R) into: `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`"
- [readme] FLOW parameter distinguishes Modular from Flow version: "For the Modular version set `FLOW <- FALSE` ... For the Flow version set `FLOW <- TRUE`"
- [readme] Application-specific parameters control analysis mode: "Make sure to toggle the following parameters depending on your application, if both are FALSE it defaults to PFAS analysis: `Lipid <- TRUE` `TWeen_pos <- FALSE`"
- [readme] Developers edit on GitHub and integrate into local installations: "**Developers can edit the main algorithms here on github** as a team. Then the code needs to be integrated by placing the edited code in the correct directory from the downloaded distribution"
