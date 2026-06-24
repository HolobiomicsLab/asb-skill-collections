---
name: parameter-configuration-conditional-logic
description: Use when setting up a LipidMatch analysis run and you need to select
  among three mutually-exclusive analysis modes (PFAS, Lipid, or Tween-positive detection).
  The trigger is application-level metadata or user specification that indicates which
  detection mode should execute.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - LipidMatch
  - R
  techniques:
  - mass-spectrometry
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

# parameter-configuration-conditional-logic

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Configure boolean parameters (Lipid, TWeen_pos) in LipidMatch to conditionally route analysis toward lipid detection, Tween-positive detection, or PFAS analysis based on application intent. This skill encodes order-agnostic dispatch logic into parameter blocks within configuration files.

## When to use

Use this skill when setting up a LipidMatch analysis run and you need to select among three mutually-exclusive analysis modes (PFAS, Lipid, or Tween-positive detection). The trigger is application-level metadata or user specification that indicates which detection mode should execute.

## When NOT to use

- Analysis mode is already predetermined by the software or pipeline and cannot be overridden via parameters.
- Input data or metadata do not contain sufficient information to determine which of the three analysis modes is appropriate.
- The downstream workflow requires simultaneous execution of multiple analysis modes in a single run.

## Inputs

- Application type specification (PFAS, Lipid, or Tween_pos)
- LipidMatch configuration template or README reference

## Outputs

- Parameter block with Lipid and TWeen_pos boolean values set
- Output configuration file with conditional dispatch logic encoded

## How to apply

First, determine the intended application type from input metadata or explicit user specification (PFAS, Lipid, or Tween_pos). Then, set the two boolean parameters according to the dispatch table: Lipid ← TRUE and TWeen_pos ← FALSE for lipid analysis; Lipid ← FALSE and TWeen_pos ← TRUE for Tween-positive analysis; both FALSE defaults to PFAS analysis. Write the configured parameter block into the output configuration file, ensuring the conditional dispatch logic is correctly encoded. The rationale is that LipidMatch implements this dispatch via two independent boolean toggles, allowing the application to read the parameter state and branch to the appropriate analysis routine.

## Related tools

- **LipidMatch** (Software platform hosting the conditional dispatch logic controlled by Lipid and TWeen_pos parameters) — https://github.com/InnovativeOmics/Core-Match
- **R** (Runtime environment for executing LipidMatch analysis routines selected by parameter dispatch)

## Evaluation signals

- Parameter block in output configuration file contains exactly two boolean parameters (Lipid and TWeen_pos) with no syntax errors.
- Lipid and TWeen_pos values correspond to the intended analysis mode: (TRUE, FALSE) for Lipid, (FALSE, TRUE) for Tween_pos, (FALSE, FALSE) for PFAS.
- LipidMatch reads the parameter block and branches to the correct analysis routine without error or ambiguity.
- No conflicting or redundant parameter configurations exist in the configuration file.
- Analysis output file headers, feature detection logic, or mass spectrometry processing steps match the expected mode (e.g., lipid m/z ranges and adducts for Lipid mode, PFAS-specific ion signatures for PFAS mode).

## Limitations

- The dispatch logic depends on exact boolean state; partial or intermediate settings are not supported.
- No validation is described to confirm that the selected mode is compatible with the input data characteristics or instrument configuration.
- The README does not document behavior if both parameters are set to TRUE (conflict resolution or error handling).
- Parameter configuration must be performed manually; no automated mode selection based on data inspection is mentioned.

## Evidence

- [other] LipidMatch implements order-agnostic conditional dispatch via two boolean parameters: setting Lipid to TRUE routes to lipid analysis; setting TWeen_pos to TRUE routes to Tween-positive analysis; setting both to FALSE defaults to PFAS analysis.: "LipidMatch implements order-agnostic conditional dispatch via two boolean parameters: setting Lipid to TRUE routes to lipid analysis; setting TWeen_pos to TRUE routes to Tween-positive analysis;"
- [readme] Make sure to toggle the following parameters depending on your application, if both are FALSE it defaults to PFAS analysis: `Lipid <- TRUE` `TWeen_pos <- FALSE`: "Make sure to toggle the following parameters depending on your application, if both are FALSE it defaults to PFAS analysis"
- [other] Set Lipid <- TRUE and TWeen_pos <- FALSE for Lipid analysis; set Lipid <- FALSE and TWeen_pos <- TRUE for Tween-positive analysis; set both to FALSE for PFAS analysis.: "Set Lipid <- TRUE and TWeen_pos <- FALSE for Lipid analysis; set Lipid <- FALSE and TWeen_pos <- TRUE for Tween-positive analysis; set both to FALSE for PFAS analysis."
- [other] Write the parameter block to the output configuration file, ensuring the conditional dispatch logic is correctly encoded.: "Write the parameter block to the output configuration file, ensuring the conditional dispatch logic is correctly encoded."
