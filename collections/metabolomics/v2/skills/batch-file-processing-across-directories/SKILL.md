---
name: batch-file-processing-across-directories
description: Use when when you need to systematically extract a specific field or set of fields from multiple files scattered across nested directories—for example, to reconstruct an index of entry statuses from thousands of JSON annotation records, or to audit a repository's content without manually visiting.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3473
  tools:
  - pandas or equivalent tabular data library
  - Python json module
  - pandas
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
---

# batch-file-processing-across-directories

## Summary

Recursively scan a directory tree to locate and parse all files of a target format (e.g., JSON), extract structured fields from each file, and aggregate results into a uniform table. This skill is essential for inventory and metadata extraction tasks across large distributed datasets.

## When to use

When you need to systematically extract a specific field or set of fields from multiple files scattered across nested directories—for example, to reconstruct an index of entry statuses from thousands of JSON annotation records, or to audit a repository's content without manually visiting each file.

## When NOT to use

- Input files are already aggregated in a single database or pre-indexed table; use direct database queries instead.
- The target directory structure is too large (millions of files) and memory-resident aggregation is infeasible; consider streaming or database-backed approaches.
- File parsing requires custom domain logic beyond standard JSON/CSV parsing; implement a custom parser first before applying this skill.

## Inputs

- Directory tree containing multiple files in target format (e.g., JSON files in nested subdirectories)
- File format specification (JSON schema or field name to extract)

## Outputs

- Tabular summary file (CSV) with aggregated extracted fields
- Entry identifier and status mapping (e.g., entry_id, cluster.status columns)

## How to apply

Begin by recursively scanning the target directory (e.g., `data/`) for all files matching your format (e.g., `.json`). Parse each file using the appropriate parser (e.g., Python's `json` module) and extract the desired field(s) (e.g., `cluster.status`). Group or aggregate extracted values by a stable identifier (e.g., entry ID), applying any filtering or mapping rules as needed. Finally, export the aggregated results to a tabular format (CSV or similar) with consistently named columns. The rationale is that distributed file storage requires systematic traversal to avoid missing records, and aggregation enables downstream analysis and validation.

## Related tools

- **Python json module** (Parse JSON files and extract cluster.status field values from each annotation record)
- **pandas** (Aggregate extracted entries into a tabular data structure and export to CSV)

## Examples

```
import json, pandas as pd; from pathlib import Path; records = []; [records.append({'entry_id': f.stem, 'cluster.status': json.load(open(f)).get('cluster', {}).get('status')}) for f in Path('data').rglob('*.json')]; pd.DataFrame(records).to_csv('entry_status_index.csv', index=False)
```

## Evaluation signals

- All JSON files in the target directory tree are successfully located and parsed without errors.
- The output CSV contains one row per entry with non-null values for entry_id and cluster.status columns.
- Row count in the output CSV equals the total number of JSON files scanned (or documents within them, depending on granularity).
- Spot-check: manually verify that cluster.status values extracted from a random sample of JSON files match the values in the output CSV.
- No missing or duplicate entries in the aggregated table; validate against expected entry count from repository documentation or prior inventory.

## Limitations

- Performance scales linearly with the number and size of files; very large repositories (millions of files) may require distributed or streaming approaches.
- Assumes all files in the scanned directory tree follow the expected schema; files with missing or malformed target fields will produce incomplete rows or errors.
- No built-in support for incremental updates; re-scanning the entire tree is required to detect newly added or modified files.

## Evidence

- [other] Recursively scan the `data` directory for all JSON files: "Recursively scan the `data` directory for all JSON files."
- [other] Extract cluster.status field from each entry and aggregate into a table: "Parse each JSON file and extract the `cluster.status` field value for each entry. 4. Aggregate entries into a table grouped by status"
- [readme] MIBiG curation data in JSON format with entry status tracked via cluster.status: "MIBiG curation data in JSON format. The current datasets for [MIBiG] live in the `data` directory, entry status is now tracked via the `cluster.status` field."
- [other] Export aggregated results as CSV with entry_id and cluster.status columns: "Export the summary table as a CSV file with columns: entry_id, cluster.status."
- [other] Tools: Python json module and pandas for tabular data export: "tools: Python (json module for parsing JSON files), pandas or equivalent tabular data library"
