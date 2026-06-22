---
name: chemical-classification-aggregation
description: Use when you have a collection of standardized molecular structures (SMILES or MOL format) that have been submitted to ClassyFire and you need to collect and organize their classification results into a single CSV or JSON table for downstream analysis, validation, or retention time modeling.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - ClassyFire
  - PubChem standardization
derived_from:
- doi: 10.1038/s41592-023-02143-z
  title: RepoRT (retention-time repository)
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_report_retention_time_repository_cq
    doi: 10.1038/s41592-023-02143-z
    title: RepoRT (retention-time repository)
  dedup_kept_from: coll_report_retention_time_repository_cq
schema_version: 0.2.0
---

# chemical-classification-aggregation

## Summary

Aggregate chemical taxonomy classifications assigned by ClassyFire into a structured table indexed by molecular identifiers, after standardized molecular structures have been classified. This step consolidates per-molecule kingdom, superclass, class, and subclass taxonomy levels into a single machine-readable artifact.

## When to use

You have a collection of standardized molecular structures (SMILES or MOL format) that have been submitted to ClassyFire and you need to collect and organize their classification results into a single CSV or JSON table for downstream analysis, validation, or retention time modeling.

## When NOT to use

- Input structures have not been standardized using PubChem standardization or an equivalent canonical form — ClassyFire requires consistent chemical notation
- Molecules are already annotated with a curated or expert-assigned classification system that is authoritative for your use case — aggregating ClassyFire results may introduce redundancy or conflict
- The ClassyFire API or local instance is unavailable or has not been deployed in your environment

## Inputs

- Standardized molecular structures (SMILES or MOL format files)
- Molecular identifiers (e.g., InChI, compound names, or sequential IDs)
- Optional: chromatographic metadata (column, gradient, flow rate, eluents)

## Outputs

- Aggregated classification table (CSV or JSON format)
- Per-molecule taxonomy records (kingdom, superclass, class, subclass)
- Validation report (non-null classification coverage, taxonomy completeness)

## How to apply

Query the ClassyFire API or local instance with each standardized molecular structure to retrieve its full chemical classification taxonomy (kingdom, superclass, class, subclass). Aggregate the returned classifications alongside their corresponding molecular identifiers and any other metadata (e.g., retention time, chromatographic conditions) into a structured table format (CSV or JSON). Perform validation by checking that each molecule has a non-null ClassyFire classification record and that all available taxonomy levels are populated where applicable. Sort or index the aggregated table by molecular identifier to enable cross-referencing with input structure files and downstream feature tables.

## Related tools

- **ClassyFire** (Query chemical classification taxonomy for each standardized structure and retrieve kingdom, superclass, class, and subclass levels)
- **PubChem standardization** (Standardize input molecular structures to canonical form prior to ClassyFire submission)

## Evaluation signals

- All molecules in the input structure file have a corresponding non-null record in the aggregated classification table (100% coverage)
- Each taxonomy level (kingdom, superclass, class, subclass) is populated where ClassyFire returns a value; no spurious null entries
- Aggregated table rows are indexed by molecular identifier and can be cross-referenced successfully with input structure files and computed molecular fingerprints/descriptors
- No duplicate molecular identifier rows exist in the aggregated table
- Taxonomy values conform to ClassyFire's controlled vocabulary (e.g., kingdom is one of Organic, Inorganic, Mixed, or Unknown)

## Limitations

- ClassyFire classification relies on the quality and currency of its chemical ontology; molecules outside its coverage (e.g., complex salts, rare isotopologues) may receive incomplete or missing classifications
- Aggregation will fail or produce sparse results if the ClassyFire API is slow, rate-limited, or encounters network errors; no retry logic or fallback is specified in the workflow
- The workflow assumes all input structures can be successfully queried against ClassyFire; malformed or non-standard SMILES/MOL input will cause per-molecule failures

## Evidence

- [other] Query ClassyFire API or local instance with each structure to retrieve chemical classification taxonomy (kingdom, superclass, class, subclass).: "Query ClassyFire API or local instance with each structure to retrieve chemical classification taxonomy (kingdom, superclass, class, subclass)."
- [other] Aggregate classification results with corresponding molecular identifiers into a structured table (CSV or JSON).: "Aggregate classification results with corresponding molecular identifiers into a structured table (CSV or JSON)."
- [other] Validation: verify each molecule has a non-null ClassyFire classification record and all taxonomy levels are populated where available.: "Validation: verify each molecule has a non-null ClassyFire classification record and all taxonomy levels are populated where available."
- [readme] Classification of molecules is performed using ClassyFire.: "Classification of molecules is performed using ClassyFire."
- [readme] structures are standardized using the PubChem standardization and molecular fingerprints and chemical descriptors are calculated using rcdk: "structures are standardized using the PubChem standardization and molecular fingerprints and chemical descriptors are calculated using rcdk"
