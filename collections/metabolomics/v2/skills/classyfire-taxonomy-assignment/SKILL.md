---
name: classyfire-taxonomy-assignment
description: Use when after molecular structures have been standardized (e.g., via PubChem standardization) and you need to enrich them with chemical taxonomy labels for cohort stratification, chemical space analysis, or retention time prediction model development.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3307
  tools:
  - ClassyFire
  - PubChem standardization
  - rcdk
derived_from:
- doi: 10.1038/s41592-023-02143-z
  title: RepoRT (retention-time repository)
evidence_spans:
- Classification of molecules is performed using ClassyFire
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-023-02143-z
  all_source_dois:
  - 10.1038/s41592-023-02143-z
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# classyfire-taxonomy-assignment

## Summary

Assign standardized chemical taxonomy (kingdom, superclass, class, subclass) to molecular structures using the ClassyFire API or local instance. This skill is essential in cheminformatics pipelines to enable downstream chemical classification-based analysis and filtering of small molecules.

## When to use

After molecular structures have been standardized (e.g., via PubChem standardization) and you need to enrich them with chemical taxonomy labels for cohort stratification, chemical space analysis, or retention time prediction model development. Apply when your input is a collection of standardized molecular structures (SMILES or MOL format) lacking kingdom/superclass/class/subclass annotations.

## When NOT to use

- Input structures have not been standardized (use PubChem standardization first)
- Molecules are already pre-classified with an alternative taxonomy system and no re-annotation is desired
- Internet or API access to ClassyFire is unavailable and no local instance is set up

## Inputs

- Standardized molecular structures (SMILES or MOL format)
- Molecular identifiers or batch file of structures
- Connection parameters to ClassyFire API or local instance

## Outputs

- Aggregated classification table (CSV or JSON) with molecular identifiers and ClassyFire taxonomy (kingdom, superclass, class, subclass)
- Validation report flagging molecules with null or incomplete classification records

## How to apply

Load standardized molecular structures (SMILES or MOL format) from input file. Query the ClassyFire API or local instance with each structure to retrieve the complete chemical classification taxonomy. Aggregate the returned classification results (kingdom, superclass, class, subclass) with corresponding molecular identifiers into a structured output table (CSV or JSON). Validate that each molecule has a non-null ClassyFire classification record and all available taxonomy levels are populated; flag or retry any molecules that fail classification or return incomplete taxonomy branches.

## Related tools

- **ClassyFire** (Queries and retrieves standardized chemical classification taxonomy for each molecular structure)
- **PubChem standardization** (Pre-processes and standardizes input molecular structures before ClassyFire annotation)
- **rcdk** (Calculates molecular fingerprints and chemical descriptors, often used in conjunction with ClassyFire taxonomy for comprehensive molecular characterization)

## Evaluation signals

- All input molecules have a corresponding non-null ClassyFire classification record in the output table
- Taxonomy levels (kingdom, superclass, class, subclass) are populated where available; no incomplete or truncated taxonomy branches
- Aggregated output table structure matches specified format (CSV or JSON) with all expected columns (molecular ID, kingdom, superclass, class, subclass)
- Validation report contains zero 'failed classification' flags; any molecules flagged should be manually inspected or retried
- Spot-check: verify that known reference structures (e.g., a lipid, amino acid, or drug compound) are assigned to chemically plausible taxonomy nodes

## Limitations

- ClassyFire classification relies on external API availability or a maintained local instance; API rate limits or downtime may delay large batch processing
- Non-standard or highly unusual molecular structures may fail to classify or receive incomplete taxonomy annotations; such molecules should be manually reviewed
- Classification accuracy depends on the quality of input structure standardization; errors in structure standardization propagate to taxonomy assignment

## Evidence

- [readme] structures are standardized using the PubChem standardization and molecular fingerprints and chemical descriptors are calculated using rcdk. Classification of molecules is performed using ClassyFire.: "structures are standardized using the PubChem standardization and molecular fingerprints and chemical descriptors are calculated using rcdk. Classification of molecules is performed using ClassyFire."
- [other] Query ClassyFire API or local instance with each structure to retrieve chemical classification taxonomy (kingdom, superclass, class, subclass).: "Query ClassyFire API or local instance with each structure to retrieve chemical classification taxonomy (kingdom, superclass, class, subclass)."
- [other] Aggregate classification results with corresponding molecular identifiers into a structured table (CSV or JSON).: "Aggregate classification results with corresponding molecular identifiers into a structured table (CSV or JSON)."
- [other] Validation: verify each molecule has a non-null ClassyFire classification record and all taxonomy levels are populated where available.: "Validation: verify each molecule has a non-null ClassyFire classification record and all taxonomy levels are populated where available."
