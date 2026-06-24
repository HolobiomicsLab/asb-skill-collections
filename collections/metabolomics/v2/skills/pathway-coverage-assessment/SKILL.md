---
name: pathway-coverage-assessment
description: Use when when preparing to run Over-representation Analysis (ORA) on
  a metabolomics study, after constructing the background set but before running the
  enrichment test.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  tools:
  - Python
  - Jupyter
  - cwieder/metabolomics-ORA
  license_tier: restricted
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

# pathway-coverage-assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Assess and validate the statistical completeness of metabolic pathway databases by computing per-pathway metabolite coverage and overlap metrics between the experimental detection list and the ORA background set. This ensures that the background set used in Over-representation Analysis contains sufficient pathway representation to enable valid statistical inference.

## When to use

When preparing to run Over-representation Analysis (ORA) on a metabolomics study, after constructing the background set but before running the enrichment test. Use this skill to verify that the background set and experimental detection list have appropriate pathway coverage so that downstream statistical tests will not be biased by pathways with zero or near-zero representation.

## When NOT to use

- Background set has not yet been constructed or filtered; pathway-coverage-assessment is a validation step that assumes the background set already exists.
- No pathway database is available or metabolite-to-pathway membership is undefined.
- The analysis goal is exploratory metabolite co-expression clustering rather than pathway enrichment; pathway coverage metrics are specific to statistical hypothesis testing frameworks like ORA.

## Inputs

- metabolomics pathway database (e.g., KEGG, Reactome, or custom pathway list with metabolite memberships)
- experimental detection list (set of metabolites identified in the study)
- background set (set of metabolites from the full database available for statistical testing)

## Outputs

- per-pathway metabolite counts (background set, detection list, overlap)
- pathway coverage summary statistics (total pathway count, zero-coverage pathway count, median/min/max pathway sizes)
- quality report indicating whether background set meets ORA assumptions (non-zero pathway representation, sufficient overlap with detection list)

## How to apply

Load the metabolomics pathway database and compute, for each pathway in the database: (1) the count of metabolites in the background set belonging to that pathway; (2) the count of metabolites in the experimental detection list belonging to that pathway; (3) the overlap between detection list and background set within that pathway. Flag pathways with zero metabolites in the background set, as these cannot be tested in ORA. Compute aggregate statistics (total pathway count, median pathway size, range of per-pathway coverage) and validate that pathway coverage aligns with expected properties of the database—for example, that no pathways are empty and that the detection list represents a reasonable sample of the full pathway landscape. Document any filtering criteria applied during background-set construction that may have reduced pathway coverage.

## Related tools

- **Python** (Language for implementing background-set construction logic and computing per-pathway coverage metrics) — https://www.python.org
- **Jupyter** (Interactive notebook environment for running simulations and validating background-set statistics with reproducibility) — https://jupyter.org
- **cwieder/metabolomics-ORA** (Reference repository containing Python code and Jupyter notebooks demonstrating background-set construction and pathway coverage validation for ORA in metabolomics) — https://github.com/cwieder/metabolomics-ORA

## Evaluation signals

- All pathways in the database have at least one metabolite in the background set (no pathways with zero coverage).
- Per-pathway metabolite counts are consistent with the database definition: sum of per-pathway background-set counts equals total background-set size (accounting for multi-pathway metabolite membership).
- Overlap between detection list and background set is non-empty and proportional to expected detection rate; pathways represented in the detection list are also represented in the background set.
- Pathway coverage summary statistics (median pathway size, range) are documented and reasonable for the chosen database and filtering criteria.
- Any pathways eliminated or filtered during background-set construction are explicitly reported; their removal does not introduce bias toward small or large pathways.

## Limitations

- Pathway coverage assessment does not verify biological relevance or accuracy of pathway annotations; it only validates statistical completeness for ORA.
- Per-pathway metrics depend critically on the quality and completeness of the metabolomics pathway database; sparse or redundant annotations will propagate into coverage statistics.
- Zero-coverage pathways may indicate that filtering criteria (e.g., by metabolite class, detection threshold, or platform limitation) have excluded important biological pathways; the assessment flags these but does not resolve them.
- Overlap metrics alone do not guarantee that the background set is representative of the true biological universe of metabolites; they only confirm internal consistency with the provided database.

## Evidence

- [other] Compute background-set statistics: total count, per-pathway coverage, and overlap metrics with the detection list.: "Compute background-set statistics: total count, per-pathway coverage, and overlap metrics with the detection list."
- [other] Validate that background-set size and composition align with expected properties (pathway coverage, non-zero pathway sizes, absence of experimental metabolites).: "Validate that background-set size and composition align with expected properties (pathway coverage, non-zero pathway sizes, absence of experimental metabolites)."
- [intro] The Python code to generate the results is contained within the Jupyter notebook: "The Python code to generate the results is contained within the Jupyter notebook"
- [intro] This repository contains the code to run the simulations presented in the study: "This repository contains the code to run the simulations presented in the study"
