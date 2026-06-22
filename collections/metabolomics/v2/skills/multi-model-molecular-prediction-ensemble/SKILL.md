---
name: multi-model-molecular-prediction-ensemble
description: Use when you have a set of molecular structures (as .sdf or .csv with SMILES) and need to predict metabolic susceptibility across multiple CYP isoforms (e.g., 1A2, 2A6, 2B6) to prioritize drug candidates or screen for potential metabolic liabilities across the major human CYP enzyme portfolio.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_2258
  tools:
  - CypReact
derived_from:
- doi: 10.1021/acs.jcim.8b00035
  title: CypReact
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cypreact_cq
    doi: 10.1021/acs.jcim.8b00035
    title: CypReact
  dedup_kept_from: coll_cypreact_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.8b00035
  all_source_dois:
  - 10.1021/acs.jcim.8b00035
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multi-model-molecular-prediction-ensemble

## Summary

This skill enables parallel prediction of molecular metabolism across multiple cytochrome P450 (CYP) isoforms in a single CypReact invocation, consolidating per-isoform predictions into a unified result set. Use it when you need to assess how a compound is metabolized by multiple CYP isoforms simultaneously rather than running separate analyses.

## When to use

You have a set of molecular structures (as .sdf or .csv with SMILES) and need to predict metabolic susceptibility across multiple CYP isoforms (e.g., 1A2, 2A6, 2B6) to prioritize drug candidates or screen for potential metabolic liabilities across the major human CYP enzyme portfolio.

## When NOT to use

- You need predictions for only a single CYP isoform; use the single-isoform invocation instead.
- Your input molecules are already pre-processed predictions rather than raw structures.
- You need real-time or interactive refinement of predictions; this workflow is batch-oriented.

## Inputs

- Molecular structure file (.sdf format)
- CSV file with SMILES strings (comma-delimited)
- CYP isoform code list (comma-separated: e.g., '1A2,2A6,2B6')

## Outputs

- Combined prediction file (.sdf or .csv) with per-isoform metabolism results
- Merged metabolic predictions across all specified CYP isoforms

## How to apply

Prepare input molecular structures as an .sdf file or .csv file containing SMILES strings (comma-separated fields). Invoke CypReact via command line by replacing the single isoform parameter with a comma-separated list of isoform codes (no spaces between codes, e.g., '1A2,2A6,2B6'). The tool processes each molecule against all specified isoforms in parallel, generating per-isoform predictions. Collect and merge the output predictions (.sdf or .csv format) into a single combined result file for downstream comparative analysis. The comma-separated isoform format is the key parameter that triggers multi-model prediction without requiring multiple sequential invocations.

## Related tools

- **CypReact** (Command-line tool that accepts comma-separated CYP isoform codes and predicts molecular metabolism across multiple isoforms in parallel) — https://bitbucket.org/Leon_Ti/cypreact

## Examples

```
java -jar cypreact.jar /path/to/input_molecules.sdf /path/to/combined_output.sdf 1A2,2A6,2B6
```

## Evaluation signals

- Output file contains predictions for all requested isoforms (verify row/record count matches input × number of isoforms)
- No malformed SMILES or missing structures in output; all input molecules are represented
- Output .sdf or .csv file is well-formed and parses without schema errors
- Per-isoform metabolite predictions are internally consistent (e.g., same molecule does not report contradictory metabolic sites for the same isoform across multiple records)
- Command execution completes without errors; log or console output confirms all isoforms were processed

## Limitations

- Isoform list must use comma-separated format with no spaces; malformed input will not trigger an informative error.
- Prediction accuracy depends on the training data and chemical space covered by CypReact; out-of-distribution molecules may have poor generalization.
- No changelog is available for the tool, making it difficult to track which CYP isoform models or prediction algorithms have been updated.
- Output merging into a single file must be done manually; the tool does not provide built-in consolidation logic.

## Evidence

- [intro] multiple isoforms specified comma-separated: "if the user wants to test his/her molecules on CYP1A2,2A6 and 2B6, he/she can simply replace "1A2" with "1A2,2A6,2B6""
- [intro] input format SMILES CSV or SDF: "The user can either input a .sdf file or a .csv. If the user input a .csv file, it should contains the SMILEs of all molecules and split them with ","."
- [intro] command-line invocation syntax: "java -jar cypreact.jar C:\Users\Desktop\CypReactBundle\ C:\Users\Desktop\BioData\1A2_Test.sdf C:\Users\Desktop\BioData\1A2_Result.sdf 1A2"
- [other] output merge workflow: "Collect and merge the per-isoform predictions into a single combined result file (.sdf or .csv) for downstream analysis."
- [other] no spaces in isoform codes: "Multiple CYP isoforms are specified as a comma-separated list without spaces by replacing the single isoform parameter"
