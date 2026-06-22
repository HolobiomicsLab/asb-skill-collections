---
name: reference-prediction-comparison-evaluation
description: Use when you have executed a structure annotation pipeline (like BAM) on a validation dataset for which ground-truth molecular structure annotations exist, and you need to assess whether the pipeline's predictions match the reference annotations at the required sensitivity and specificity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - HassounLab/BAM
  - PROXIMAL2
  - GNN-SOM
derived_from:
- doi: 10.1021/acs.analchem.4c01565
  title: bam
evidence_spans:
- HassounLab/BAM
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bam
    doi: 10.1021/acs.analchem.4c01565
    title: bam
  dedup_kept_from: coll_bam
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c01565
  all_source_dois:
  - 10.1021/acs.analchem.4c01565
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# reference-prediction-comparison-evaluation

## Summary

Compare pipeline predictions against reference annotations to compute validation metrics (accuracy, coverage) for molecular structure discovery. This skill quantifies how well a method reproduces known molecular structures in a benchmark dataset.

## When to use

You have executed a structure annotation pipeline (like BAM) on a validation dataset for which ground-truth molecular structure annotations exist, and you need to assess whether the pipeline's predictions match the reference annotations at the required sensitivity and specificity.

## When NOT to use

- No reference annotations are available for the dataset being tested.
- The input consists only of raw metabolomics spectra without deposited ground-truth structures.
- The pipeline has not yet been executed; you only have input data and code.

## Inputs

- BAM pipeline predictions (ranked candidate structures with scores per query metabolite)
- Reference annotations (CSV or structured dataset mapping query metabolites to ground-truth structures as SMILES/InChI)
- Validation dataset (anchor-suspect metabolite pairs with known molecular identities)

## Outputs

- Annotation accuracy metric (fraction of queries with reference structure in top predictions)
- Coverage metric (fraction of queries receiving predictions)
- Metrics report (tabulated results, performance benchmarks by reaction dataset and biotransformation rule set)
- Performance analysis by reaction source (KEGG vs. RetroRules accuracy/coverage comparison)

## How to apply

Execute the annotation pipeline end-to-end on the validation dataset to generate candidate structure predictions. Retrieve the reference annotation set (ground truth structures with identifiers). For each query metabolite, compare the pipeline's ranked predictions against the reference structure using structural matching (SMILES/InChI equivalence or exact molecular formula matching). Compute annotation accuracy as the fraction of queries where the reference structure appears in the top-ranked predictions, and coverage as the fraction of queries receiving any prediction. Document achieved metrics in a report, and identify which biotransformation rules and reaction datasets (KEGG, RetroRules) contribute to prediction performance.

## Related tools

- **HassounLab/BAM** (Structure annotation pipeline executed end-to-end to generate ranked molecular structure predictions) — https://github.com/HassounLab/BAM
- **PROXIMAL2** (Dependency for biotransformation operator generation and metabolite pair enumeration) — https://github.com/HassounLab/PROXIMAL2
- **GNN-SOM** (Dependency for graph neural network-based ranking of site-of-metabolism predictions) — https://github.com/HassounLab/GNN-SOM

## Examples

```
sh runBAM.sh  # Execute BAM pipeline on validation data; then compare predictions against molecules_of_interest.csv to compute accuracy and coverage metrics.
```

## Evaluation signals

- Annotation accuracy and coverage metrics are non-negative, bounded by [0, 1], and sum to a valid fraction of total queries processed.
- Reference structures appear in pipeline outputs for all test queries (no missing predictions or null comparisons).
- Metrics report documents performance separately for KEGG and RetroRules reaction datasets, enabling identification of which biotransformation rule set contributes to prediction success.
- All queries in the validation dataset are traced to a matching comparison outcome (match, no match, or unranked); no queries are dropped without documentation.
- Accuracy and coverage metrics remain consistent when the same pipeline and reference set are re-evaluated (reproducibility check).

## Limitations

- BAM relies on prior tools (PROXIMAL2, GNN-SOM) which must be downloaded and conda environments created separately; validation cannot proceed if these dependencies are misconfigured.
- Prediction accuracy depends on the completeness and quality of the reaction dataset (KEGG or RetroRules); rare or non-canonical biotransformations absent from the database will reduce coverage.
- Accuracy metrics are sensitive to the definition of structural equivalence (exact SMILES/InChI match vs. molecular formula match); different matching criteria may yield different accuracy estimates.
- The validation dataset was derived from a single global molecular network source; generalization to other untargeted metabolomics cohorts is not directly assessed.

## Evidence

- [other] Compute validation metrics (annotation accuracy, coverage) by comparing pipeline predictions against reference annotations.: "Compute validation metrics (annotation accuracy, coverage) by comparing pipeline predictions against reference annotations."
- [other] Execute the BAM pipeline end-to-end on the validation data to generate structure annotations.: "Execute the BAM pipeline end-to-end on the validation data to generate structure annotations."
- [readme] All data necessary to run the evaluation of BAM described in our paper is included in the data folder.: "All data necessary to run the evaluation of BAM described in our paper is included in the data folder."
- [readme] BAM checks if the suspect molecule is known by checking whether the SMILES or InChI is specified in the molecules_of_interest csv file.: "BAM checks if the suspect molecule is known by checking whether the SMILES or InChI is specified in the molecules_of_interest csv file."
- [readme] To change to using RetroRules reaction data, simply comment the 'KEGG biotransformations' block and uncomment the 'RetroRules biotransformations' box.: "To change to using RetroRules reaction data, simply comment the 'KEGG biotransformations' block and uncomment the 'RetroRules biotransformations' box."
