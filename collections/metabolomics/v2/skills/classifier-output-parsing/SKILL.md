---
name: classifier-output-parsing
description: Use when after a classifier (such as BitterPredict.m) has computed binary predictions (e.g., bitter vs. non-bitter) on a batch of molecular descriptors and you need to organize those predictions into a structured, labeled output file for downstream analysis, validation, or reporting.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3474
  tools:
  - BitterPredict.m
derived_from:
- doi: 10.1021/acs.jafc.3c09767
  title: bittermass
evidence_spans:
- BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bittermass_cq
    doi: 10.1021/acs.jafc.3c09767
    title: bittermass
  dedup_kept_from: coll_bittermass_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jafc.3c09767
  all_source_dois:
  - 10.1021/acs.jafc.3c09767
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# classifier-output-parsing

## Summary

Parse and structure binary classification predictions from a machine-learning classifier into a formatted output file with molecule identifiers and predicted class labels. This skill is essential when compiling per-sample predictions from a classifier into a reusable, traceable result artifact.

## When to use

Apply this skill after a classifier (such as BitterPredict.m) has computed binary predictions (e.g., bitter vs. non-bitter) on a batch of molecular descriptors and you need to organize those predictions into a structured, labeled output file for downstream analysis, validation, or reporting.

## When NOT to use

- Input is already a pre-compiled prediction table with validated identifiers and labels — skip to validation or downstream filtering instead.
- Predictions are for continuous outcomes (regression) rather than binary classification — this skill assumes discrete class labels.
- Molecule identifiers are missing or cannot be reliably linked to predictions — resolve data integrity issues first.

## Inputs

- Binary predictions array (bitter/non-bitter label per molecule)
- Molecule identifier list or index from the input descriptor file
- Input descriptor table or metadata linking molecules to predictions

## Outputs

- Structured output file (CSV or EXCEL) with molecule identifiers and predicted class labels
- Per-molecule bitterness predictions (bitter or not bitter)

## How to apply

After the BitterPredict.m classifier generates binary predictions for each molecule in the input descriptor table, compile the predictions into a structured output file that preserves the molecule identifiers alongside their predicted class labels (bitter or not bitter). Ensure each row in the output corresponds to exactly one molecule from the input, maintaining referential integrity between input molecules and their predictions. The output format should be human-readable and machine-parseable (e.g., CSV or tabular format) to facilitate downstream filtering, validation, or integration into publication or supplementary materials.

## Related tools

- **BitterPredict.m** (Upstream classifier that computes binary bitterness predictions from molecular descriptors; output predictions are parsed and structured by this skill) — https://github.com/Niv-Lab/BitterPredict1

## Evaluation signals

- Each molecule from the input descriptor file has exactly one row in the output file with a non-null prediction label.
- Molecule identifiers in the output match those in the input descriptor file; no identifiers are dropped or duplicated.
- All predicted class labels are one of the two expected binary classes (bitter or not bitter); no null, invalid, or out-of-scope values are present.
- The output file is readable in a spreadsheet or data-frame tool (e.g., pandas.read_csv()) without parsing errors or encoding issues.
- Row-by-row spot checks confirm that predictions align with the classifier's internal output and are not corrupted or reordered during compilation.

## Limitations

- No changelog or version tracking is provided in the current BitterPredict.m release; output format stability and backwards compatibility are not explicitly documented.
- The README states that full code will be available upon publication; pre-publication versions may have incomplete or undocumented output schemas.
- No validation of prediction plausibility or confidence scores is performed at the parsing stage; all predictions are treated as equally reliable.

## Evidence

- [readme] BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not.: "BitterPredict.m gets as input CSV or EXCEL files with required descriptors of molecules, and calucautes a predictions if each molecule is bitter or not."
- [other] Generate binary predictions (bitter/not bitter) for each molecule. 4. Compile predictions into a structured output file with molecule identifiers and predicted class labels.: "Compile predictions into a structured output file with molecule identifiers and predicted class labels."
- [readme] BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure.: "BitterPredict is a classifier which predicts whether a compound is bitter or not, based on its chemical structure."
- [readme] Details and examples of how to use the code is avalibale inside bitterPredict.m file.: "Details and examples of how to use the code is avalibale inside bitterPredict.m file."
