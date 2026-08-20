---
name: metabolite-background-set-construction
description: Use when when preparing to run Over-representation Analysis (ORA) on
  metabolomics pathway data, after you have loaded both a metabolomics pathway database
  (e.g., KEGG, MetExplore) and an experimental detection list (metabolites measured
  in your study).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
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

# metabolite-background-set-construction

## Summary

Construct a statistical background set of metabolites for Over-representation Analysis (ORA) in metabolomics by filtering a complete metabolomics pathway database to exclude experimental detection lists and apply method-specific criteria. This background set defines the universe against which pathway enrichment significance is computed.

## When to use

When preparing to run Over-representation Analysis (ORA) on metabolomics pathway data, after you have loaded both a metabolomics pathway database (e.g., KEGG, MetExplore) and an experimental detection list (metabolites measured in your study). Background-set construction is required before computing enrichment p-values, as the statistical universe must be clearly defined and reproducible.

## When NOT to use

- When the experimental detection list already includes the complete database (no background/foreground distinction possible).
- When using enrichment methods that do not require an explicit background set (e.g., some topology-based pathway analysis methods).
- When metabolite identities or pathway annotations are too sparse or unreliable to construct a meaningful background.

## Inputs

- Metabolomics pathway database (e.g., KEGG, MetExplore format)
- Experimental metabolite detection list (IDs or names of detected metabolites)
- ORA method specification or configuration (filtering thresholds)

## Outputs

- Background metabolite set (list of metabolites to use as statistical universe)
- Per-pathway background counts (number of background metabolites per pathway)
- Background-set validation report (coverage, overlap metrics, pathway sizes)
- Background set composition statistics

## How to apply

Load the complete metabolomics pathway database and the experimental detection list of metabolites identified in your study. Apply filtering logic to exclude experimental metabolites from the database, then apply any additional filtering criteria specified by your chosen ORA method (e.g., minimum pathway size, metabolite annotation confidence, or inclusion rules based on detectability). Compute and record background-set statistics: total metabolite count, per-pathway coverage (number of background metabolites per pathway), and overlap metrics with the experimental detection list. Validate that the background set has non-zero size for each pathway, contains no experimental metabolites, and aligns with expected database properties before proceeding to enrichment testing.

## Related tools

- **Python** (Implement background-set construction logic, filtering, and validation within scripts or Jupyter notebooks)
- **Jupyter** (Interactive environment for loading database and detection list, running simulations, and documenting background-set construction reproducibly)

## Evaluation signals

- Background-set size is positive and non-zero for each pathway represented in the enrichment analysis.
- No experimental metabolites appear in the background set (validated by set difference check).
- Per-pathway background counts match expected database coverage after filtering.
- Background-set composition aligns with ORA method specifications (e.g., minimum pathway sizes are respected).
- Overlap metrics between background set and detection list are consistent with study design (e.g., no unintended metabolites excluded).

## Limitations

- Background-set construction depends critically on the completeness and accuracy of the metabolomics pathway database; sparse or incomplete annotations will bias the universe definition.
- Filtering criteria must be clearly specified and documented; arbitrary or undisclosed background-set construction undermines reproducibility and statistical validity of ORA.
- Background sets constructed from different databases or with different filtering logic are not directly comparable, making it difficult to reconcile enrichment results across studies.

## Evidence

- [other] The study provides Python code within a Jupyter notebook to implement and run simulations for pathway analysis in metabolomics, enabling reproducible construction and evaluation of background sets for ORA.: "enabling reproducible construction and evaluation of background sets for ORA"
- [other] Load the metabolomics pathway database and experimental detection list (metabolites detected in the study). Apply the background-set construction logic to identify which metabolites from the full database constitute the statistical background, excluding those in the experimental detection list and applying any filtering criteria specified in the ORA method.: "Load the metabolomics pathway database and experimental detection list (metabolites detected in the study). Apply the background-set construction logic to identify which metabolites from the full"
- [other] Compute background-set statistics: total count, per-pathway coverage, and overlap metrics with the detection list. Validate that background-set size and composition align with expected properties (pathway coverage, non-zero pathway sizes, absence of experimental metabolites).: "Compute background-set statistics: total count, per-pathway coverage, and overlap metrics with the detection list. Validate that background-set size and composition align with expected properties"
- [intro] Pathway analysis in metabolomics: Pitfalls and best practice for the use of Over-representation Analysis: "Over-representation Analysis (ORA) is a pathway analysis method used in metabolomics with identifiable pitfalls and best practices"
- [intro] This repository contains the code to run the simulations presented in the study: "This repository contains the code to run the simulations presented in the study"
