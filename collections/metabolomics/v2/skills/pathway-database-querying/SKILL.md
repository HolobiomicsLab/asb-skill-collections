---
name: pathway-database-querying
description: 'Use when when preparing to run ORA on a metabolomics study: you have a list of detected metabolites from your experiment and need to determine which metabolites from the full pathway database should serve as the statistical background, and which pathways contain how many metabolites overall.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
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
---

# pathway-database-querying

## Summary

Retrieve and structure metabolite-to-pathway mappings from a metabolomics pathway database to define the statistical background and pathway membership for Over-representation Analysis (ORA). This skill enables construction of unbiased background sets and accurate pathway coverage estimates required for valid ORA hypothesis testing.

## When to use

When preparing to run ORA on a metabolomics study: you have a list of detected metabolites from your experiment and need to determine which metabolites from the full pathway database should serve as the statistical background, and which pathways contain how many metabolites overall. Apply this skill before computing ORA test statistics to ensure the background set reflects the true composition and pathway coverage of your analytical platform.

## When NOT to use

- Your ORA method has pre-defined, fixed background sets that you must not modify (e.g., curator-approved lists for specific platforms).
- The metabolomics platform detects all or nearly all known metabolites in the pathway database (background set would be empty or trivially small).
- You are using a different pathway analysis method (e.g., GSEA, topGO) that does not require explicit background-set construction.

## Inputs

- Metabolomics pathway database (with metabolite-pathway annotations)
- Experimental detection list (metabolites detected in the study)

## Outputs

- Background-set definition (metabolites from database not in detection list)
- Per-pathway metabolite counts and coverage statistics
- Validated mapping of foreground and background metabolites to pathways

## How to apply

Load the metabolomics pathway database (e.g., KEGG, Reactome, or custom annotation) and cross-reference it with your experimental detection list. Query the database to extract the complete set of metabolites present in each pathway, then partition this universe into two groups: (1) metabolites detected in your experiment (foreground), and (2) metabolites in the database but not detected (background). Apply any filtering criteria specified by your ORA method (e.g., exclusion of pathways below a minimum size threshold, or pathways with zero background metabolites). Compute and validate background-set statistics including total count, per-pathway coverage, and overlap metrics with the detection list to confirm that no experimental metabolites inadvertently appear in the background and that pathway sizes match expected properties.

## Related tools

- **Python** (Implementation language for loading, querying, and validating pathway database and background-set logic) — https://www.python.org
- **Jupyter** (Interactive notebook environment for reproducible pathway database queries and background-set construction simulations) — https://jupyter.org
- **cwieder/metabolomics-ORA** (Reference repository containing concrete Python code and simulations for background-set construction and validation in ORA) — https://github.com/cwieder/metabolomics-ORA.git

## Evaluation signals

- Background set contains zero metabolites from the experimental detection list (mutual exclusivity check).
- All pathways with non-zero background metabolites have size ≥ the method's specified minimum pathway size threshold.
- Total background-set count equals (database total metabolites) − (detected metabolites), with no unaccounted metabolites.
- Per-pathway coverage statistics match expected composition for the analytical platform (e.g., platform-specific detection bias is consistent with known instrumental limitations).
- No pathway appears simultaneously in foreground and background assignments; foreground + background for each pathway accounts for all database metabolites in that pathway.

## Limitations

- Background-set composition is only valid for the specific pathway database version and metabolite detection platform used; results cannot be transferred to different platforms or database versions without re-querying.
- The quality and completeness of background-set construction depends entirely on the accuracy and coverage of the upstream pathway database annotations; missing or incorrectly mapped metabolites will bias the background set.
- If the experimental detection list is biased by sample preparation, chromatography, or mass spectrometry settings (e.g., preferential detection of certain metabolite classes), the background set will not represent a statistically uniform universe, potentially violating ORA's assumptions.

## Evidence

- [other] Load the metabolomics pathway database and experimental detection list (metabolites detected in the study).: "Load the metabolomics pathway database and experimental detection list (metabolites detected in the study)."
- [other] Apply the background-set construction logic to identify which metabolites from the full database constitute the statistical background, excluding those in the experimental detection list.: "Apply the background-set construction logic to identify which metabolites from the full database constitute the statistical background, excluding those in the experimental detection list and applying"
- [other] Compute background-set statistics: total count, per-pathway coverage, and overlap metrics with the detection list.: "Compute background-set statistics: total count, per-pathway coverage, and overlap metrics with the detection list."
- [other] Validate that background-set size and composition align with expected properties (pathway coverage, non-zero pathway sizes, absence of experimental metabolites).: "Validate that background-set size and composition align with expected properties (pathway coverage, non-zero pathway sizes, absence of experimental metabolites)."
- [intro] The Python code to generate the results is contained within the Jupyter notebook: "The Python code to generate the results is contained within the Jupyter notebook"
