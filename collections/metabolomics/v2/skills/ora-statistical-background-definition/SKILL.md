---
name: ora-statistical-background-definition
description: Use when you are implementing ORA for metabolomics pathway analysis and must decide which metabolites constitute the statistical background against which to test your experimental detection list.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - Jupyter
  - cwieder/metabolomics-ORA
derived_from:
- doi: 10.1371/journal.pcbi.1009105
  title: ORA
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ora
    doi: 10.1371/journal.pcbi.1009105
    title: ORA
  dedup_kept_from: coll_ora
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009105
  all_source_dois:
  - 10.1371/journal.pcbi.1009105
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ora-statistical-background-definition

## Summary

Define and construct the statistical background set for Over-representation Analysis (ORA) in metabolomics by identifying which metabolites from a pathway database serve as the denominator for significance testing. Correct background definition is critical because misspecification invalidates p-value calculations and leads to false pathway discoveries.

## When to use

You are implementing ORA for metabolomics pathway analysis and must decide which metabolites constitute the statistical background against which to test your experimental detection list. This skill applies when you have (1) a full metabolomics pathway database with known metabolite–pathway associations, (2) an experimental detection list (metabolites detected in your study), and (3) uncertainty about which database metabolites should be included in the background (e.g., should you exclude undetected metabolites, apply detection-method filters, or require minimum pathway size thresholds?).

## When NOT to use

- Your input is already a pre-computed p-value table or enrichment result; you need evaluation or interpretation of ORA results, not background definition.
- You are performing a different pathway analysis method (e.g., GSEA, topology-based analysis) that does not require explicit background-set definition.
- Your metabolomics data lacks a curated pathway database or database coverage is so sparse that most pathways have zero background metabolites.

## Inputs

- Metabolomics pathway database (metabolite–pathway associations, typically tabular or structured format)
- Experimental detection list (set of metabolites detected in the study)
- Method specification for background construction (filtering rules, pathway size thresholds, detection criteria)

## Outputs

- Background set (list of non-detected metabolites eligible for statistical testing)
- Background-set statistics (total count, per-pathway counts, overlap metrics with detection list)
- Validation report (checks for pathway coverage, non-zero sizes, absence of experimental metabolites)

## How to apply

Load the metabolomics pathway database and experimental detection list into Python (using Jupyter for reproducibility). Apply background-set construction logic by (1) identifying all metabolites in the database that were NOT detected in your experiment, (2) applying method-specific filtering criteria (e.g., excluding metabolites below a detection threshold or from pathways with fewer than N members), and (3) computing background statistics: total metabolite count, per-pathway coverage, and overlap metrics with the detection list. Validate that the resulting background set has non-zero representation across all pathways of interest, excludes experimental metabolites, and aligns with the ORA method's assumptions (e.g., hypergeometric test requires correct population size).

## Related tools

- **Python** (Primary language for loading database and detection list, implementing background-set construction logic, and computing validation statistics)
- **Jupyter** (Notebook environment for reproducible execution and documentation of background-set workflow and simulations)
- **cwieder/metabolomics-ORA** (Reference implementation providing complete code examples for background-set construction and validation in ORA simulations) — https://github.com/cwieder/metabolomics-ORA

## Evaluation signals

- Background set contains zero metabolites that appear in the experimental detection list (no overlap).
- Every pathway in the analysis has at least one metabolite represented in the background set (non-zero per-pathway coverage).
- Total background count and per-pathway counts match the expected values given the filtering criteria and database composition.
- Overlap metrics (e.g., percentage of detected metabolites that map to the database, percentage of database metabolites undetected) fall within expected ranges for your study design and detection method.
- Hypergeometric test denominator (population size) derived from background set produces p-values that are stable and appropriately calibrated under null-hypothesis simulations.

## Limitations

- Background-set definition depends critically on the completeness and accuracy of the metabolomics pathway database; sparse or biased databases will produce biased background sets.
- Filtering criteria (e.g., minimum pathway size, detection thresholds) must be pre-specified and justified; arbitrary choices can inflate false positives.
- Undetected metabolites may represent true biological absences, technical limitations, or detection method bias; the statistical background does not distinguish these cases.
- Different ORA implementations may use different background-definition conventions (e.g., some include all database metabolites, others restrict to those in detected pathways), leading to non-comparable results across tools.

## Evidence

- [other] How is the background set of metabolites constructed for Over-representation Analysis (ORA) in metabolomics, given an experimental detection list and a metabolomics pathway database?: "How is the background set of metabolites constructed for Over-representation Analysis (ORA) in metabolomics, given an experimental detection list and a metabolomics pathway database?"
- [other] Apply the background-set construction logic to identify which metabolites from the full database constitute the statistical background, excluding those in the experimental detection list and applying any filtering criteria specified in the ORA method.: "Apply the background-set construction logic to identify which metabolites from the full database constitute the statistical background, excluding those in the experimental detection list and applying"
- [other] Compute background-set statistics: total count, per-pathway coverage, and overlap metrics with the detection list.: "Compute background-set statistics: total count, per-pathway coverage, and overlap metrics with the detection list."
- [other] Validate that background-set size and composition align with expected properties (pathway coverage, non-zero pathway sizes, absence of experimental metabolites).: "Validate that background-set size and composition align with expected properties (pathway coverage, non-zero pathway sizes, absence of experimental metabolites)."
- [intro] The Python code to generate the results is contained within the Jupyter notebook: "The Python code to generate the results is contained within the Jupyter notebook"
- [intro] This repository contains the code to run the simulations presented in the study: "This repository contains the code to run the simulations presented in the study"
