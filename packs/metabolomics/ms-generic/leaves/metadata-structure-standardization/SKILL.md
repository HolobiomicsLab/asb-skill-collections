---
name: metadata-structure-standardization
description: Use when when you have experimental metadata (e.g., sample annotations, plate layouts, compound lists) with inconsistent or missing column names, non-standard field formats, or incomplete information required for downstream database queries (PubChem, DrugBank, LOTUS) or sequence generation for mass.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3071
  - http://edamontology.org/topic_0091
  tools:
  - metadata_cleanup_prefect.py
  - jobs.py
  - drugbank_extraction.py
  - prepare_wikidata_lotus_prefect.py
  - sequence_creation.py
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1038/s41592-025-02813-0
  title: MSnLib
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msnlib_cq
    doi: 10.1038/s41592-025-02813-0
    title: MSnLib
  dedup_kept_from: coll_msnlib_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-025-02813-0
  all_source_dois:
  - 10.1038/s41592-025-02813-0
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metadata-structure-standardization

## Summary

Standardize and clean experimental metadata to conform to a required template schema with consistent column names and minimum required fields before querying external databases or running downstream analysis pipelines. This ensures interoperability with automated metadata cleanup workflows and structure lookups.

## When to use

When you have experimental metadata (e.g., sample annotations, plate layouts, compound lists) with inconsistent or missing column names, non-standard field formats, or incomplete information required for downstream database queries (PubChem, DrugBank, LOTUS) or sequence generation for mass spectrometry instruments (Orbitrap ID-X).

## When NOT to use

- Metadata already in the required template schema with all fields populated and validated
- When structure information is critical and PubChem does not contain the compound of interest (DrugBank, LOTUS, or Dictionary of Natural Products must be queried instead — ensure those sources are enabled and accessible in jobs.py)
- Metadata for non-chemical or non-pharmacological samples not intended for drug or natural product database cross-referencing

## Inputs

- Raw metadata spreadsheet or CSV (arbitrary schema)
- Compound names or identifiers (string)
- Sample identifiers (string)
- Plate/batch identifiers and well locations (for Orbitrap workflows)

## Outputs

- Standardized metadata spreadsheet conforming to template schema
- Cleaned compound records with matched structure information (from PubChem or other sources)
- Validated metadata ready for prefect workflow submission

## How to apply

Map your metadata columns to the required template schema, ensuring you include at minimum a unique sample identifier, compound name or identifier, and any instrument-specific fields (e.g., plate_id, well_location for Orbitrap sequence creation). For missing structure information, the pipeline will automatically query PubChem by compound name, so ensure compound names are spelled consistently and match PubChem nomenclature. Validate that all rows conform to the template's data types and required fields before submission to the metadata_cleanup_prefect.py workflow. If querying specialized databases (DrugBank, Dictionary of Natural Products, LOTUS), pre-populate access credentials or set the corresponding flag to False in jobs.py.

## Related tools

- **metadata_cleanup_prefect.py** (Orchestrates the standardized metadata cleanup workflow via Prefect 2; executes the template validation and database query pipeline) — https://github.com/corinnabrungs/msn_tree_library
- **jobs.py** (Defines which external databases (DrugBank, LOTUS, Dictionary of Natural Products) are enabled and accessible; controls feature flags for local file access and credentials) — https://github.com/corinnabrungs/msn_tree_library
- **drugbank_extraction.py** (Parses downloaded DrugBank release file to extract drug records for enrichment during metadata cleanup) — https://github.com/corinnabrungs/msn_tree_library
- **prepare_wikidata_lotus_prefect.py** (Updates local LOTUS (natural product) database for metadata enrichment queries) — https://github.com/corinnabrungs/msn_tree_library
- **sequence_creation.py** (Converts standardized metadata with sample_id, plate_id, and well_location into Orbitrap ID-X Xcalibur sequence files) — https://github.com/corinnabrungs/msn_tree_library

## Examples

```
# Prepare metadata using the template, then submit to Prefect workflow:
python metadata_cleanup_prefect.py  # starts the cleanup flow; define jobs in jobs.py with your standardized metadata file path
```

## Evaluation signals

- All rows in the standardized output match the required template column names and data types with no missing required fields
- Structure information is successfully retrieved from PubChem (or alternative source) for all compounds with unambiguous matches logged
- Metadata can be directly ingested by downstream workflows (metadata_cleanup_prefect.py, sequence_creation.py) without schema validation errors
- Sample and plate identifiers are unique within their respective scopes (no duplicate sample_ids or conflicting plate/well combinations)
- Database lookups (if enabled) return non-null enrichment fields (e.g., drug class from DrugBank, natural product family from LOTUS) with no critical lookup failures

## Limitations

- PubChem name search may fail or return ambiguous matches if compound names are misspelled, use trade names, or refer to non-indexed compounds; manual curation or alternative database lookup is required in these cases
- DrugBank, Dictionary of Natural Products, and LOTUS require pre-downloaded files or active credentials; if not provided, queries will be skipped or set to False in jobs.py, limiting enrichment
- Structure information retrieval from PubChem is asynchronous and may introduce latency for large metadata files; no changelog is provided for tracking which compounds were auto-enriched versus user-supplied
- Sequence creation (Orbitrap ID-X) requires strict plate_id, well_location, and sample_id formatting; non-conformant entries will cause downstream instrument sequence generation to fail

## Evidence

- [readme] Please use the [template] for your metadata for having same column names and minimum needed information for the query: "Please use the [template] for your metadata for having same column names and minimum needed information for the query"
- [readme] If no structure information is provided, it is queried from PubChem by Name search: "If no structure information is provided, it is queried from PubChem by Name search"
- [readme] The metadatasheet needs to hava a unique sample id, a plate name (batch identifier) as plate_id and the vial or well location as well_location to run: "The metadatasheet needs to hava a unique sample id, a plate name (batch identifier) as plate_id and the vial or well location as well_location to run"
- [readme] For querying other databases, some need a local file and/or special access otherwise set it to False in the jobs.py: "For querying other databases, some need a local file and/or special access otherwise set it to False in the jobs.py"
- [intro] The drugbank_extraction.py script is executed on a downloaded DrugBank release file to extract and parse drug information for use in the metadata cleanup pipeline: "The drugbank_extraction.py script is executed on a downloaded DrugBank release file to extract and parse drug information for use in the metadata cleanup pipeline"
