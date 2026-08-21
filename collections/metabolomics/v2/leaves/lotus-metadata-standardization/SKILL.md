---
name: lotus-metadata-standardization
description: Use when you have raw compound or natural-product metadata in spreadsheet
  or tabular form with inconsistent column names, missing structure information, or
  when you need to query against the LOTUS natural-product database and suspect the
  local copy is stale or absent.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3370
  tools:
  - prepare_wikidata_lotus_prefect.py
  - drugbank_extraction.py
  - jobs.py
  - metadata_cleanup_prefect.py
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41592-025-02813-0
  title: MSnLib
evidence_spans:
- run `prepare_wikidata_lotus_prefect.py` for updating the data
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

# lotus-metadata-standardization

## Summary

Standardize and validate metadata for natural-product and drug-compound queries by aligning column names and content to a template, then optionally regenerate the LOTUS Wikidata database to ensure consistent structure information lookup. This skill ensures downstream query operations receive well-formed input and up-to-date reference data.

## When to use

Use this skill when you have raw compound or natural-product metadata in spreadsheet or tabular form with inconsistent column names, missing structure information, or when you need to query against the LOTUS natural-product database and suspect the local copy is stale or absent.

## When NOT to use

- Your metadata already conforms to the template schema and all structure fields are populated — skip the standardization step.
- You require real-time updates to LOTUS data beyond the Wikidata snapshot; consider querying Wikidata directly instead.
- You lack network access to PubChem or Wikidata; the fallback is to use pre-provided files or manual structure entry.

## Inputs

- Raw metadata spreadsheet or tabular file (CSV, TSC, or Google Sheets) with compound/natural-product records
- Optional: DrugBank XML file (if drug information queries are needed)
- Optional: Pre-existing LOTUS database file or permission to regenerate via Wikidata

## Outputs

- Standardized metadata table with aligned column names and populated structure fields
- Updated LOTUS natural-product database file (if regeneration performed)
- Configuration state in jobs.py reflecting active/inactive database query sources

## How to apply

First, reformat your metadata to match the standardized template (same column names and minimum required fields). If structure information is missing, the system will query PubChem by compound name to fill it in. Next, decide whether to regenerate the LOTUS database: run `prepare_wikidata_lotus_prefect.py` to fetch and process current Wikidata entries for natural products, validate that the regenerated file contains expected columns and record counts, and save it for downstream query operations. If regeneration is not performed or not needed, use the provided pre-existing LOTUS file as a fallback. Configure database query toggles (e.g., Dictionary of Natural Products, DrugBank) in jobs.py according to local file availability and access permissions.

## Related tools

- **prepare_wikidata_lotus_prefect.py** (Fetches and processes Wikidata entries for natural products to regenerate the LOTUS database file; executed to update the local LOTUS data with current records.) — https://github.com/corinnabrungs/msn_tree_library
- **drugbank_extraction.py** (Extracts and processes drug information from a DrugBank XML file for local querying; run on downloaded DrugBank files before metadata cleanup.) — https://github.com/corinnabrungs/msn_tree_library
- **jobs.py** (Configuration file to enable/disable queries against specific databases (Dictionary of Natural Products, LOTUS, DrugBank, DrugCentral, Broad Hub) based on local file availability and access permissions.) — https://github.com/corinnabrungs/msn_tree_library
- **metadata_cleanup_prefect.py** (Orchestrates the metadata cleanup and standardization workflow using Prefect 2; serves the flow locally and processes cleanup jobs submitted via jobs.py.) — https://github.com/corinnabrungs/msn_tree_library

## Examples

```
python prepare_wikidata_lotus_prefect.py && python metadata_cleanup_prefect.py
```

## Evaluation signals

- Metadata table column names match the standardized template exactly; no extraneous or missing columns.
- All compound records contain a unique sample ID, and optional structure fields (SMILES, InChI) are either provided or successfully populated from PubChem name search.
- Regenerated LOTUS file (if applicable) contains the expected schema columns and a non-zero record count that exceeds the previous version or pre-provided baseline.
- jobs.py configuration correctly reflects which databases are queried: set to True only if local files exist and access is available; set to False otherwise, without errors.
- Downstream query operations (e.g., natural-product or drug lookups) execute without schema mismatch errors and return expected metadata fields.

## Limitations

- PubChem name search may return ambiguous or incorrect structures if compound names are not unique or are colloquial; manual verification is recommended.
- LOTUS database regeneration requires network access to Wikidata and may be time-consuming for large datasets; a pre-provided fallback file is available if regeneration fails or is skipped.
- DrugBank, Dictionary of Natural Products, and some other data sources require special access or local files; queries will fail silently if toggled on in jobs.py but files are unavailable.
- No changelog is provided for the LOTUS or other reference data files, so it is unclear which records are new, modified, or removed in each regeneration.

## Evidence

- [readme] Please use the [template] for your metadata for having same column names and minimum needed information for the query: "Please use the [template] for your metadata for having same column names and minimum needed information for the query"
- [readme] If no structure information is provided, it is queried from PubChem by Name search: "If no structure information is provided, it is queried from PubChem by Name search"
- [readme] LOTUS: run `prepare_wikidata_lotus_prefect.py` for updating the data (otherwise use the provided file): "LOTUS: run `prepare_wikidata_lotus_prefect.py` for updating the data (otherwise use the provided file)"
- [intro] The prepare_wikidata_lotus_prefect.py script is executed to update the LOTUS natural-product database file; if this update is not performed, a pre-existing provided file can be used as an alternative.: "The prepare_wikidata_lotus_prefect.py script is executed to update the LOTUS natural-product database file; if this update is not performed, a pre-existing provided file can be used as an alternative."
- [intro] Execute prepare_wikidata_lotus_prefect.py to fetch and process Wikidata entries for natural products. 2. Validate that the regenerated LOTUS database file contains the expected columns and records.: "Execute prepare_wikidata_lotus_prefect.py to fetch and process Wikidata entries for natural products. 2. Validate that the regenerated LOTUS database file contains the expected columns and records."
- [readme] For querying other databases, some need a local file and/or special access otherwise set it to False in the jobs.py: "For querying other databases, some need a local file and/or special access otherwise set it to False in the jobs.py"
