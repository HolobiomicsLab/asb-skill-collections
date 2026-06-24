---
name: metadata-field-extraction
description: Use when you have a directory of JSON-formatted annotation files and
  need to systematically extract a specific metadata field (such as curation status,
  entry identifier, or validation state) across all records.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0219
  tools:
  - pandas or equivalent tabular data library
  - Python json module
  - pandas
  license_tier: restricted
derived_from:
- doi: 10.1093/nar/gkac1049
  title: MIBiG 3.0
evidence_spans:
- entry status is now tracked via the `cluster.status` field
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mibig_3_0_cq
    doi: 10.1093/nar/gkac1049
    title: MIBiG 3.0
  dedup_kept_from: coll_mibig_3_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/nar/gkac1049
  all_source_dois:
  - 10.1093/nar/gkac1049
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metadata-field-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and aggregate structured metadata fields from a collection of JSON annotation records, organizing them into a searchable index or summary table. This skill is essential when you need to track curation status, inventory dataset properties, or build faceted views of large annotation repositories.

## When to use

Apply this skill when you have a directory of JSON-formatted annotation files and need to systematically extract a specific metadata field (such as curation status, entry identifier, or validation state) across all records. This is particularly relevant when the metadata field is nested within the JSON structure and you need to produce a consolidated inventory or quality-control summary.

## When NOT to use

- Input data is already in tabular format (CSV, TSV, Excel) — use direct import instead
- Metadata field is unstructured or not consistently present across records — use data validation/cleaning skill first
- You need real-time or streaming updates to a live annotation database — use API-based extraction instead

## Inputs

- Directory containing JSON annotation files (e.g., mibig-json/data)
- Schema path to target metadata field (e.g., 'cluster.status')

## Outputs

- CSV table with columns: entry_id, extracted_metadata_field
- Summary statistics grouped by field value

## How to apply

Recursively scan the target directory for all JSON files in the collection. Parse each JSON file using a JSON parser (e.g. Python's json module) and navigate to the target metadata field using the documented schema path (e.g., `cluster.status` for MIBiG entries). For each file, extract the field value and the entry identifier, recording both in a structured intermediate format. Aggregate all extracted records into a tabular format (e.g., a pandas DataFrame) grouped by the extracted field value. Export the final summary table as a delimited text file (CSV) with explicit column headers. Validate that all records have been processed and that no field values are missing unexpectedly.

## Related tools

- **Python json module** (Parse and navigate nested JSON structures to locate and extract target metadata fields)
- **pandas** (Aggregate extracted field values into a tabular DataFrame and export as CSV)

## Examples

```
import json; import pandas as pd; import os; records = []; [records.append({'entry_id': f.split('.')[0], 'status': json.load(open(os.path.join('data', f)))['cluster']['status']}) for f in os.listdir('data') if f.endswith('.json')]; pd.DataFrame(records).to_csv('entry_status_index.csv', index=False)
```

## Evaluation signals

- All JSON files in the target directory have been processed (file count matches expected total)
- CSV output contains no duplicate entry_id values and no null values in the extracted metadata field column
- Field value distribution matches known curation workflow (e.g., expected status categories are present)
- CSV row count equals the number of JSON input files processed
- Schema path successfully navigates the documented JSON structure without KeyError or AttributeError exceptions

## Limitations

- Skill assumes the target metadata field exists and is consistently located at the documented schema path; missing or variably-structured fields may be silently skipped or cause parsing failures
- No changelog or version history is tracked in the mibig-json repository, so schema changes between snapshots may not be documented
- Nested JSON structures with variable depth or naming conventions require manual schema inspection before automation

## Evidence

- [intro] Entry status is tracked through the `cluster.status` field: "entry status is now tracked via the `cluster.status` field"
- [other] Recursively scan data directory and parse JSON to extract status values: "Recursively scan the `data` directory for all JSON files. 3. Parse each JSON file and extract the `cluster.status` field value for each entry."
- [other] Aggregate entries into a table grouped by status: "Aggregate entries into a table grouped by status, recording entry identifier and status."
- [other] Export summary as CSV with entry_id and cluster.status columns: "Export the summary table as a CSV file with columns: entry_id, cluster.status."
- [other] Use Python json module and pandas for tabular data handling: "Python (json module for parsing JSON files), pandas or equivalent tabular data library"
- [readme] MIBiG JSON data lives in data directory: "The current datasets for [MIBiG] live in the `data` directory, entry status is now tracked via the `cluster.status` field."
