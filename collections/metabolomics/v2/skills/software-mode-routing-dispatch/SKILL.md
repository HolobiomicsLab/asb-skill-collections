---
name: software-mode-routing-dispatch
description: 'Use when you are preparing to run LipidMatch or FluoroMatch and need
  to select the correct analysis mode for your sample type: lipid profiling, Tween-positive
  surfactant analysis, or PFAS (per- and polyfluoroalkyl substances) analysis.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3373
  tools:
  - LipidMatch
  - R
  - FluoroMatch
  license_tier: restricted
derived_from:
- doi: 10.1007/s00216-021-03392-7
  title: FluoroMatch 2.0
evidence_spans:
- 'put Modular.r into two directories (replace existing code): `LipidMatch-4.2\Flow\LipidMatch_Distribution`'
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

# software-mode-routing-dispatch

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Configure boolean parameters in LipidMatch to route analysis execution toward lipid detection, Tween-positive detection, or PFAS analysis based on intended application. This skill encodes conditional dispatch logic that determines which algorithmic pathway executes at runtime.

## When to use

You are preparing to run LipidMatch or FluoroMatch and need to select the correct analysis mode for your sample type: lipid profiling, Tween-positive surfactant analysis, or PFAS (per- and polyfluoroalkyl substances) analysis. The choice depends on your sample composition and experimental objective, not on input file format or preprocessing state.

## When NOT to use

- Input data has already been preprocessed or aligned to a mode-specific database; parameter dispatch occurs at initialization and cannot be changed mid-analysis.
- You have uncertainty about sample type but want to run exploratory analysis across all modes; this skill commits to a single mode and must be repeated separately for each mode comparison.
- The LipidMatch version does not support boolean parameter toggling (e.g., legacy versions prior to LipidMatch-4.2).

## Inputs

- LipidMatch configuration template or parameter block
- User specification of analysis application type (PFAS, Lipid, or Tween-positive)
- Input metadata indicating sample composition

## Outputs

- Configured parameter block with Lipid and TWeen_pos boolean values set
- Output configuration file ready for LipidMatch or FluoroMatch execution
- Analysis mode dispatch pathway correctly encoded

## How to apply

Identify your intended analysis application (PFAS, Lipid, or Tween-positive) from your experimental design or sample metadata. Set the boolean parameters Lipid and TWeen_pos in the LipidMatch configuration block according to a three-state dispatch rule: set Lipid ← TRUE and TWeen_pos ← FALSE for lipid analysis; set Lipid ← FALSE and TWeen_pos ← TRUE for Tween-positive analysis; set both Lipid ← FALSE and TWeen_pos ← FALSE to default to PFAS analysis. Write these parameter assignments into the configuration file before invoking the LipidMatch or FluoroMatch executable. The order of parameter assignment is not significant; the conditional logic reads both flags simultaneously to determine the execution path.

## Related tools

- **LipidMatch** (Primary analysis software whose execution pathway is routed by parameter configuration; implements order-agnostic conditional dispatch logic based on Lipid and TWeen_pos boolean flags) — https://github.com/InnovativeOmics/Core-Match
- **FluoroMatch** (Sister software supporting identical analysis-mode parameter dispatch via same Lipid and TWeen_pos boolean configuration) — https://github.com/InnovativeOmics/Core-Match
- **R** (Execution environment in which parameter configuration block is evaluated and conditional dispatch logic is resolved)

## Examples

```
# In R configuration file for LipidMatch:
Lipid <- FALSE
TWeen_pos <- FALSE
# This routes analysis to PFAS detection mode
```

## Evaluation signals

- Configuration file is parseable and contains both Lipid and TWeen_pos boolean assignments with no syntax errors.
- Lipid and TWeen_pos values follow the three-state rule: exactly one of {(TRUE,FALSE), (FALSE,TRUE), (FALSE,FALSE)} is set; mixed states like (TRUE,TRUE) indicate misconfiguration.
- LipidMatch execution log or output metadata confirms the correct analysis mode was selected (e.g., 'Lipid analysis mode active' or 'PFAS default mode active').
- Output feature tables or match scores are consistent with the intended analysis mode (e.g., lipid class annotations present for Lipid mode, PFAS marker compounds for PFAS mode).
- Parameter block is correctly placed in the location specified by the README: immediately after FLOW configuration and before any analysis-specific parameter overrides.

## Limitations

- Both boolean parameters set to TRUE is undefined behavior; the README does not document fallback or error handling for this state.
- Parameter dispatch is static at initialization; switching analysis modes requires restarting LipidMatch with a reconfigured parameter block.
- The THREE-state design (Lipid / Tween-pos / PFAS) permits no mixed-mode analysis within a single execution; comparative or exploratory workflows require serial runs.
- No changelog is available, so version-specific parameter behavior or changes are not documented.

## Evidence

- [readme] Parameter configuration mechanism and three-state dispatch logic: "Make sure to toggle the following parameters depending on your application, if both are FALSE it defaults to PFAS analysis: `Lipid <- TRUE` `TWeen_pos <- FALSE`"
- [other] Conditional dispatch is order-agnostic and depends on simultaneous flag state: "LipidMatch implements order-agnostic conditional dispatch via two boolean parameters: setting Lipid to TRUE routes to lipid analysis; setting TWeen_pos to TRUE routes to Tween-positive analysis;"
- [readme] Parameter block placement and integration workflow: "Place any edited script files (genEIC.r, MS1Spectragen.r, Stats.R) into: `LipidMatch-4.2\Flow\LipidMatch_Distribution\LipidMatch_Libraries\Scripts`"
- [other] Application determines execution pathway based on parameter configuration: "The application determines which analysis mode executes based on parameter configuration."
