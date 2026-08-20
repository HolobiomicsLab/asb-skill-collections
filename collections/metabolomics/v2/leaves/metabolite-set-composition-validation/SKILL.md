---
name: metabolite-set-composition-validation
description: 'Use when after constructing a background set for ORA in metabolomics:
  you have loaded an experimental detection list and a metabolomics pathway database,
  applied background-set construction logic, and need to confirm that the resulting
  background set has the correct size, composition, pathway.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - Jupyter
  license_tier: open
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

# metabolite-set-composition-validation

## Summary

Verify that a background-set or experimental metabolite collection is correctly constructed by validating its composition against the metabolomics pathway database, ensuring absence of contamination, appropriate pathway coverage, and statistical soundness for Over-representation Analysis.

## When to use

After constructing a background set for ORA in metabolomics: you have loaded an experimental detection list and a metabolomics pathway database, applied background-set construction logic, and need to confirm that the resulting background set has the correct size, composition, pathway coverage, and does not contain metabolites that should have been excluded (e.g., those in the experimental detection list).

## When NOT to use

- The experimental detection list has not yet been acquired or is empty; validation requires both a reference database and a non-empty detection list to be meaningful.
- You are performing pathway analysis without ORA; this skill is specific to validating background-set construction in Over-representation Analysis workflows.
- The pathway database has not been loaded or parsed; validation requires a complete, structured pathway annotation resource.

## Inputs

- metabolomics pathway database (full reference set of metabolites and pathway annotations)
- experimental detection list (metabolites detected in the study)
- ORA method specification (filtering criteria, exclusion rules)

## Outputs

- validated background-set composition report
- background-set statistics (total count, per-pathway coverage, overlap metrics)
- validation pass/fail status for each invariant

## How to apply

Load the full metabolomics pathway database and the experimental detection list (metabolites detected in the study). Construct the background set by identifying all metabolites from the database that should serve as the statistical reference, applying any filtering criteria specified by the ORA method (e.g., exclusion of experimentally detected metabolites). Compute background-set statistics: total metabolite count, per-pathway coverage, and overlap metrics with the experimental detection list. Validate four key invariants: (1) the background set contains no metabolites present in the experimental detection list; (2) all pathways in the background set have non-zero metabolite counts; (3) per-pathway coverage is consistent with database entries; (4) background-set size and composition align with expected properties for the chosen ORA configuration.

## Related tools

- **Python** (Implement background-set construction logic, compute statistics, and execute validation checks on pathway coverage and metabolite overlap)
- **Jupyter** (Interactive notebook environment for reproducible background-set validation, exploratory statistics, and visualization of validation results) — https://github.com/cwieder/metabolomics-ORA

## Evaluation signals

- Background set contains zero overlap with experimental detection list (no experimentally detected metabolites are present).
- All pathways in the background set have non-zero metabolite counts; no pathway is empty or misconfigured.
- Per-pathway coverage statistics match the counts recorded in the source metabolomics pathway database.
- Total background-set size and composition are consistent with the specified ORA filtering criteria and database schema.
- Validation report explicitly confirms absence of experimental metabolites and alignment of background-set properties with expected invariants.

## Limitations

- Background-set validation depends critically on correct parsing and loading of the pathway database; errors in database ingestion will propagate to validation results.
- The skill assumes that the experimental detection list is accurate and complete; contamination or missing metabolites in the input detection list will affect the validity of background-set exclusion.
- Validation checks are syntax and schema-level; they do not assess whether the background set is statistically appropriate for the biological question or whether pathway annotations are current and curated.
- The article does not specify how to handle metabolites present in the database but absent from any pathway annotation; validation logic must explicitly define behavior in such cases.

## Evidence

- [other] Compute background-set statistics: total count, per-pathway coverage, and overlap metrics with the detection list.: "Compute background-set statistics: total count, per-pathway coverage, and overlap metrics with the detection list."
- [other] Validate that background-set size and composition align with expected properties (pathway coverage, non-zero pathway sizes, absence of experimental metabolites).: "Validate that background-set size and composition align with expected properties (pathway coverage, non-zero pathway sizes, absence of experimental metabolites)."
- [intro] The Python code to generate the results is contained within the Jupyter notebook: "The Python code to generate the results is contained within the Jupyter notebook"
- [intro] This repository contains the code to run the simulations presented in the study: "This repository contains the code to run the simulations presented in the study"
