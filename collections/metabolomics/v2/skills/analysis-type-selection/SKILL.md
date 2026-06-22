---
name: analysis-type-selection
description: 'Use when preparing to run LipidMatch-4.2 and you need to determine which analysis mode should execute. Specifically: when your input data consists of lipid standards or lipid-rich samples (set Lipid analysis mode); when you are analyzing Tween surfactant-containing samples (set Tween-positive mode);'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0188
  tools:
  - LipidMatch
  - R
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# analysis-type-selection

## Summary

Select the correct analysis mode (Lipid, Tween-positive, or PFAS) in LipidMatch by configuring two boolean parameters that implement order-agnostic conditional dispatch. This skill ensures the integration scripts route metabolomics data toward the intended detection pipeline based on application requirements.

## When to use

Use this skill when preparing to run LipidMatch-4.2 and you need to determine which analysis mode should execute. Specifically: when your input data consists of lipid standards or lipid-rich samples (set Lipid analysis mode); when you are analyzing Tween surfactant-containing samples (set Tween-positive mode); or when your sample is a per- and polyfluoroalkyl substance (PFAS) mixture or environmental water extract (set PFAS mode as default).

## When NOT to use

- Input data has already been assigned to a specific analysis pipeline—skip this skill and proceed directly to execution.
- The application type is ambiguous or unknown and cannot be determined from sample metadata or user specification—resolve metadata clarity first before applying parameter dispatch.
- You are modifying algorithm logic or filter thresholds rather than selecting between pre-built analysis modes.

## Inputs

- Sample metadata or user specification (text or structured format indicating application type)
- LipidMatch-4.2 parameter template or configuration file stub
- Core-Match integration script template

## Outputs

- Configured parameter block with Lipid and TWeen_pos boolean values set correctly
- Integration script with conditional dispatch logic encoded and ready for execution

## How to apply

Inspect the input sample metadata or user specification to determine the intended application type. Then configure the Lipid and TWeen_pos boolean parameters in the parameter block according to the conditional dispatch logic: set `Lipid <- TRUE` and `TWeen_pos <- FALSE` for lipid-focused analysis; set `Lipid <- FALSE` and `TWeen_pos <- TRUE` for Tween-positive analysis; set both `Lipid <- FALSE` and `TWeen_pos <- FALSE` to default to PFAS analysis. Write the configured parameter block to the output configuration file. The order of parameter assignment does not affect the dispatch outcome—only the final boolean state of each parameter determines which analysis pipeline executes.

## Related tools

- **LipidMatch** (Primary metabolomics matching and analysis framework in which boolean parameters control dispatch to Lipid, Tween-positive, or PFAS analysis modes) — github.com/InnovativeOmics/Core-Match
- **R** (Language used to edit and execute Modular.r and supporting scripts containing the parameter block and conditional dispatch logic)

## Examples

```
# In R, after opening Modular.r or equivalent parameter block:
Lipid <- TRUE
TWeen_pos <- FALSE
# Then save and execute the integration script to route to Lipid analysis mode.
```

## Evaluation signals

- Verify the parameter block was written to the output configuration file with boolean values matching the intended analysis type (inspect file directly or query configuration object).
- Confirm that when the integration script executes, the correct analysis module (lipid, Tween, or PFAS) initializes—check runtime logs or module initialization messages.
- Validate that input data is routed through the expected pipeline by checking intermediate output file names, directory structure, or console output that should reflect the selected analysis mode.
- Test boundary case: set both Lipid and TWeen_pos to FALSE and confirm the pipeline defaults to PFAS analysis without error.
- Re-run with swapped parameter values and confirm the analysis mode switches as expected, confirming order-agnostic dispatch.

## Limitations

- The skill assumes the user has access to the parameter block location within the LipidMatch-4.2 installation (Modular.r or configuration template); if the parameter block is missing or corrupted, dispatch will fail.
- No explicit error message or warning is documented if both parameters are misconfigured (e.g., both TRUE simultaneously); behavior in this state is undefined and may lead to silent failure or unexpected analysis output.
- The skill requires correct integration of edited scripts into the correct directory structure (`LipidMatch-4.2\Flow\LipidMatch_Distribution` and `LipidMatch-4.2\FluoroMatch_Modular`) before dispatch logic is active; incomplete integration will prevent the parameter block from being recognized.

## Evidence

- [intro] Finding: dispatch mechanism and boolean semantics: "LipidMatch implements order-agnostic conditional dispatch via two boolean parameters: setting Lipid to TRUE routes to lipid analysis; setting TWeen_pos to TRUE routes to Tween-positive analysis;"
- [readme] README: explicit parameter configuration instructions: "Make sure to toggle the following parameters depending on your application, if both are FALSE it defaults to PFAS analysis: `Lipid <- TRUE` `TWeen_pos <- FALSE`"
- [intro] Finding: workflow logic for determining application type: "Determine the application type from input metadata or user specification (PFAS, Lipid, or Tween-positive)."
- [intro] Finding: integration of parameter block into output: "Write the parameter block to the output configuration file, ensuring the conditional dispatch logic is correctly encoded."
- [readme] README: multiple analysis modes via parameter toggling: "Software supports multiple analysis modes including PFAS analysis, Lipid analysis, and TWeen_pos analysis via parameter toggling"
