---
name: r-syntax-validation-and-linting
description: Use when after editing R configuration scripts (e.g., Modular.r) that control execution modes (Modular vs Flow) or toggling analysis parameters (Lipid, TWeen_pos, PFAS). Apply this skill before integrating edited scripts into the LipidMatch-4.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0230
  edam_topics:
  - http://edamontology.org/topic_3674
  tools:
  - R
  - Modular.r
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

# r-syntax-validation-and-linting

## Summary

Validate R script syntax and detect errors before execution by running a parse check in R. This skill ensures edited configuration scripts (such as Modular.r) are free of syntax errors and ready for deployment across multiple software distribution directories.

## When to use

After editing R configuration scripts (e.g., Modular.r) that control execution modes (Modular vs Flow) or toggling analysis parameters (Lipid, TWeen_pos, PFAS). Apply this skill before integrating edited scripts into the LipidMatch-4.2 directory structure or before running the software in production.

## When NOT to use

- Input script has not been edited or has not yet been saved to disk
- Only static code review or style checking is needed (use a separate linter like lintr)
- Runtime errors are expected and intentional (e.g., testing error handling)

## Inputs

- Edited R script file (e.g., Modular.r)
- R interpreter or RStudio session

## Outputs

- Parse validation report (success or error list)
- Confirmed syntax-error-free R script ready for deployment

## How to apply

After saving edits to an R script file, open an R session and run a parse check to confirm no syntax errors are present. The parse check validates the script's structure without executing it, catching issues such as mismatched parentheses, unclosed quotes, or invalid flag assignments (e.g., malformed FLOW, csvInput, or ManuallyInputVariables declarations). If the parse succeeds, the script is ready for integration into the target directories (LipidMatch_Distribution or FluoroMatch_Modular). If errors are reported, correct them in the text editor and repeat the parse check until validation passes.

## Related tools

- **R** (Runtime environment for executing parse checks and validating script syntax before deployment)
- **Modular.r** (Configuration script containing FLOW, csvInput, and ManuallyInputVariables flags that must pass syntax validation before integration) — https://github.com/InnovativeOmics/Core-Match

## Examples

```
parse(file='Modular.r'); if(!inherits(try(parse(file='Modular.r')), 'try-error')) { print('Syntax validation passed') }
```

## Evaluation signals

- Parse check completes without error messages or warnings in the R console
- Script file can be sourced into R without syntax errors (e.g., source('Modular.r') succeeds or parse(file='Modular.r') returns no errors)
- Configuration flags (FLOW, csvInput, ManuallyInputVariables, Lipid, TWeen_pos) are syntactically valid assignments (e.g., 'FLOW <- FALSE' not 'FLOW = FALSE' or 'FLOW< -FALSE')
- No unmatched delimiters or unclosed strings are reported by the parser

## Limitations

- Parse checks validate syntax only; they do not detect logical errors (e.g., conflicting parameter combinations or incorrect flag values)
- Parse checks do not verify that dependent packages or data files exist or are accessible at runtime
- This skill does not test the correctness of the script's output or its behavior under different configuration modes

## Evidence

- [other] Validate script syntax by running a parse check in R to confirm no syntax errors are present.: "Validate script syntax by running a parse check in R to confirm no syntax errors are present."
- [other] For Modular mode execution, set FLOW <- FALSE; for Flow mode execution, set FLOW <- TRUE.: "For Modular mode execution, set FLOW <- FALSE; for Flow mode execution, set FLOW <- TRUE."
- [readme] put Modular.r into two directories (replace existing code): `LipidMatch-4.2\Flow\LipidMatch_Distribution` `LipidMatch-4.2\FluoroMatch_Modular`: "put Modular.r into two directories (replace existing code): `LipidMatch-4.2\Flow\LipidMatch_Distribution` `LipidMatch-4.2\FluoroMatch_Modular`"
- [readme] For the Modular version set `FLOW <- FALSE` ... `csvInput <- FALSE #Alternatively you can keep this true and use csv inputs` `ManuallyInputVariables <- FALSE`: "For the Modular version set `FLOW <- FALSE` ... `csvInput <- FALSE #Alternatively you can keep this true and use csv inputs` `ManuallyInputVariables <- FALSE`"
