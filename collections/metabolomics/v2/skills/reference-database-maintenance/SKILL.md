---
name: reference-database-maintenance
description: Use when when preparing to run compound metadata enrichment or structure queries, check whether your reference databases (LOTUS, DrugBank, DrugCentral) are stale or missing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3373
  tools:
  - prepare_wikidata_lotus_prefect.py
  - drugbank_extraction.py
  - jobs.py
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

# reference-database-maintenance

## Summary

Systematically update and regenerate curated reference databases (LOTUS natural products, DrugBank, DrugCentral) to ensure downstream metadata queries and compound matching are performed against current, validated data. This skill ensures that locally maintained reference files reflect the latest external data sources and remain compatible with query workflows.

## When to use

When preparing to run compound metadata enrichment or structure queries, check whether your reference databases (LOTUS, DrugBank, DrugCentral) are stale or missing. Trigger this skill if: (1) you are setting up a new metadata cleanup pipeline and need current natural-product or drug reference files; (2) you have configured a reference database as active in jobs.py but the local file is outdated or absent; (3) upstream Wikidata or DrugBank sources have been updated and you need to propagate those changes into your query system.

## When NOT to use

- If your reference databases are already current and have been validated against your metadata template schema within the last update cycle—re-running extraction without a trigger wastes resources.
- If a reference database is not configured as active in jobs.py (set to False) and your analysis does not require it—skip maintenance for that database.
- If you are performing a one-time query and a pre-existing, validated reference file is already provided and compatible with your metadata template—maintenance is unnecessary unless you need the very latest external data.

## Inputs

- Wikidata natural-product entries (fetched via API by prepare_wikidata_lotus_prefect.py)
- DrugBank XML/database file (downloaded from drugbank.com/releases/latest)
- DrugCentral SQL dump file
- jobs.py configuration file specifying which databases to use locally vs. skip

## Outputs

- Updated LOTUS natural-product database file (standardized columns, current Wikidata snapshot)
- Extracted and standardized DrugBank records file
- Validated reference database ready for metadata query operations

## How to apply

For each reference database configured as active in jobs.py, execute the corresponding extraction or update script. For LOTUS, run prepare_wikidata_lotus_prefect.py to fetch and process Wikidata entries for natural products and regenerate the LOTUS data file. For DrugBank, download the latest release file and run drugbank_extraction.py to extract and standardize drug records. After execution, validate that the regenerated database file contains the expected columns and record counts, and verify compatibility with the metadata template schema (same column names, minimum required fields for downstream queries). Store the updated file in the location referenced by jobs.py so that query operations access the current data.

## Related tools

- **prepare_wikidata_lotus_prefect.py** (Fetches and processes Wikidata entries for natural products and regenerates the LOTUS database file for use in downstream metadata queries) — github.com/corinnabrungs/msn_tree_library
- **drugbank_extraction.py** (Extracts and standardizes drug records from downloaded DrugBank files for integration into reference queries) — github.com/corinnabrungs/msn_tree_library
- **jobs.py** (Configuration file that specifies which reference databases (LOTUS, DrugBank, DrugCentral, Dictionary of Natural Products) are active (True) or inactive (False) for the cleanup pipeline) — github.com/corinnabrungs/msn_tree_library

## Examples

```
python prepare_wikidata_lotus_prefect.py && python drugbank_extraction.py drugbank_latest.xml
```

## Evaluation signals

- The regenerated database file contains all expected columns matching the metadata template schema (same column names, minimum required fields).
- Record count in the updated database is non-zero and consistent with the source system (e.g., Wikidata LOTUS snapshot contains expected number of natural-product entries).
- Column data types and formats are consistent with the template and downstream query requirements (e.g., structure identifiers are parseable, compound names are non-null).
- If comparing to a previous version, verify that new or updated records reflect the latest external source (e.g., Wikidata or DrugBank release date).
- A sample query using the updated reference file returns expected results (e.g., compound lookup by name or structure succeeds).

## Limitations

- LOTUS data maintenance depends on Wikidata availability and update frequency; if Wikidata is unavailable, prepare_wikidata_lotus_prefect.py will fail, but a pre-existing LOTUS file can be used as a fallback.
- DrugBank extraction requires valid credentials and a download link; access restrictions may prevent automated updates.
- DrugCentral is provided as a SQL dump and requires manual download; no automated extraction script was mentioned.
- No changelog or versioning mechanism is documented, making it difficult to track when reference files were last updated or which external versions they represent.

## Evidence

- [intro] The prepare_wikidata_lotus_prefect.py script is executed to update the LOTUS natural-product database file; if this update is not performed, a pre-existing provided file can be used as an alternative.: "LOTUS: run `prepare_wikidata_lotus_prefect.py` for updating the data (otherwise use the provided file)"
- [intro] Metadata must follow a template with the same column names and minimum required information for queries to succeed.: "Please use the [template] for your metadata for having same column names and minimum needed information for the query"
- [intro] DrugBank extraction is performed on the downloaded file using a dedicated script.: "DrugBank (access needed): [Download] and run `drugbank_extraction.py` on that file"
- [intro] Configuration of which databases to use locally is controlled in jobs.py.: "set it to False in the jobs.py"
- [intro] The workflow validates that regenerated database files contain expected columns and records before downstream use.: "Validate that the regenerated LOTUS database file contains the expected columns and records"
