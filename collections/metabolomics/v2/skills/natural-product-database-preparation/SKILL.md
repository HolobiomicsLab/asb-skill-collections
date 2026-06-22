---
name: natural-product-database-preparation
description: Use when you need to update your local LOTUS natural-product database file before running metadata enrichment or structure-query workflows, or when a pre-existing provided LOTUS file is unavailable or suspected to be stale. Trigger on project initialization or on a scheduled basis (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3345
  tools:
  - prepare_wikidata_lotus_prefect.py
  - jobs.py
  - Prefect 2
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# natural-product-database-preparation

## Summary

Regenerate and validate the LOTUS natural-product database by executing a Prefect-orchestrated Python script that fetches and processes Wikidata entries for downstream metadata queries and structure lookups. This skill ensures the local LOTUS data file remains current and contains expected schema columns and record counts for reliable compound annotation.

## When to use

Apply this skill when you need to update your local LOTUS natural-product database file before running metadata enrichment or structure-query workflows, or when a pre-existing provided LOTUS file is unavailable or suspected to be stale. Trigger on project initialization or on a scheduled basis (e.g., quarterly) to capture new Wikidata natural-product entries.

## When NOT to use

- You already have a recently validated LOTUS file and do not require updates to Wikidata entries.
- Your workflow does not involve natural-product annotation or structure queries; use alternative drug databases (DrugBank, DrugCentral) if compounds are pharmaceuticals only.
- Network connectivity to Wikidata is unavailable; rely on the pre-existing provided file instead.

## Inputs

- Wikidata SPARQL endpoint (accessed via the script)
- Optional: pre-existing LOTUS data file (fallback)

## Outputs

- Regenerated LOTUS natural-product database file (CSV or tabular format with standardized columns)
- Validation report (record count, schema conformance)

## How to apply

Execute the prepare_wikidata_lotus_prefect.py script within a Prefect 2 workflow environment to fetch current Wikidata entries for natural products and regenerate the local LOTUS database file. The script outputs a standardized CSV or tabular file with consistent column names matching the metadata template (e.g., structure identifiers, compound names, source references). After execution, validate that the regenerated file contains the expected schema columns and a non-zero record count; if validation fails, fall back to the provided pre-existing LOTUS file. Save the validated LOTUS data file to a known location for use in downstream query operations such as PubChem structure lookups or compound matching against sample metadata.

## Related tools

- **prepare_wikidata_lotus_prefect.py** (Orchestrated script that fetches and processes Wikidata natural-product entries and regenerates the local LOTUS database file) — https://github.com/corinnabrungs/msn_tree_library
- **jobs.py** (Configuration file to toggle LOTUS data updates and specify local file paths in the Prefect deployment) — https://github.com/corinnabrungs/msn_tree_library
- **Prefect 2** (Orchestration framework for deploying and executing the LOTUS update workflow)

## Examples

```
python prepare_wikidata_lotus_prefect.py
```

## Evaluation signals

- Regenerated LOTUS file exists at the expected output path and is readable as tabular data.
- Schema validation: the output file contains all required metadata columns (matching the template) with no missing headers.
- Record count: the output file contains a non-zero number of records (natural products) after regeneration.
- Timestamp consistency: records include Wikidata identifiers and timestamps that indicate recent fetch (no stale or duplicated entries from previous runs).
- Downstream query success: downstream tools (e.g., structure queries against PubChem) successfully retrieve compound information using the regenerated LOTUS file without schema errors.

## Limitations

- The script depends on Wikidata availability and SPARQL endpoint stability; network outages or Wikidata maintenance will cause the update to fail.
- Wikidata coverage of natural products is incomplete; some compounds may not be present or may lack structure information, requiring fallback to PubChem name search.
- The regenerated LOTUS file is a snapshot at the time of execution; new Wikidata entries added after the run will not be reflected until the script is executed again.
- No changelog is provided, so it is not possible to track which specific natural products were added, removed, or updated between script runs.

## Evidence

- [other] Execute prepare_wikidata_lotus_prefect.py to fetch and process Wikidata entries for natural products.: "Execute prepare_wikidata_lotus_prefect.py to fetch and process Wikidata entries for natural products."
- [other] Validate that the regenerated LOTUS database file contains the expected columns and records.: "Validate that the regenerated LOTUS database file contains the expected columns and records."
- [readme] LOTUS: run `prepare_wikidata_lotus_prefect.py` for updating the data (otherwise use the provided file): "LOTUS: run `prepare_wikidata_lotus_prefect.py` for updating the data (otherwise use the provided file)"
- [readme] use the [template] for your metadata for having same column names and minimum needed information for the query: "use the [template] for your metadata for having same column names and minimum needed information for the query"
- [readme] If no structure information is provided, it is queried from PubChem by Name search: "If no structure information is provided, it is queried from PubChem by Name search"
