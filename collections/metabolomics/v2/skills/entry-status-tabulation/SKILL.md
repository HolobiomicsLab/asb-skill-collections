---
name: entry-status-tabulation
description: Use when you need to assess the curation completeness and status distribution
  of a MIBiG JSON dataset—for instance, to identify how many entries are in 'active',
  'retired', or 'pending' states, or to audit changes in entry status over time.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0160
  tools:
  - pandas or equivalent tabular data library
  - Python json module
  - mibig-json repository
  license_tier: restricted
  provenance_tier: literature
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

# entry-status-tabulation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and aggregate entry status values from a MIBiG JSON annotation dataset by parsing the `cluster.status` field across all records, producing a tabular summary grouped by status. This skill enables systematic inventory and tracking of curation state across secondary metabolite gene cluster annotations.

## When to use

Apply this skill when you need to assess the curation completeness and status distribution of a MIBiG JSON dataset—for instance, to identify how many entries are in 'active', 'retired', or 'pending' states, or to audit changes in entry status over time. Trigger this skill when the analysis goal is to understand or report on the metadata organization of the MIBiG repository itself, rather than the chemical or genomic content of individual clusters.

## When NOT to use

- You are analyzing the genomic or chemical content of clusters rather than their curation metadata—use genome assembly or sequence homology skills instead.
- Your input is already a pre-compiled status index or manifest file—tabulation is unnecessary if the status summary is already available.
- You need to extract sequence data from the genbanks directory—use sequence retrieval skills instead of this curation-status skill.

## Inputs

- MIBiG JSON annotation files (directory path)
- Entry identifier and cluster.status field values (from parsed JSON records)

## Outputs

- CSV table with columns: entry_id, cluster.status
- Entry status summary grouped by status category

## How to apply

Clone or access the mibig-secmet/mibig-json repository and recursively scan the `data` directory for all JSON files. Parse each JSON file using a JSON library (Python's `json` module) and extract the `cluster.status` field value from each annotation record. Aggregate the extracted status values into a table, grouping entries by their status and recording the entry identifier alongside the status. The rationale is that MIBiG curation data is maintained in JSON format with entry status tracked explicitly through the `cluster.status` field; by systematizing this extraction, you create a queryable inventory of curation state. Export the aggregated summary as a CSV file with columns: `entry_id` and `cluster.status`. This tabulation serves as a ground-truth record of entry lifecycle and can feed downstream filtering, reporting, or quality-assurance workflows.

## Related tools

- **Python json module** (Parse JSON files and extract cluster.status field values from each annotation record)
- **pandas or equivalent tabular data library** (Aggregate extracted status values, group by status category, and export summary as CSV)
- **mibig-json repository** (Source repository containing the data directory with all MIBiG JSON annotation files) — https://github.com/mibig-secmet/mibig-json

## Examples

```
import json, pandas as pd, os; data = []; [data.append({'entry_id': f.split('.')[0], 'cluster.status': json.load(open(os.path.join('data', f)))['cluster']['status']}) for f in os.listdir('data') if f.endswith('.json')]; pd.DataFrame(data).to_csv('entry_status.csv', index=False)
```

## Evaluation signals

- CSV output file is created with exactly two columns (entry_id, cluster.status) and contains no null or malformed rows.
- All entry identifiers are unique within the CSV; no duplicate entry_id values appear.
- Every entry_id in the CSV corresponds to a valid JSON file found in the data directory; spot-check against filesystem scan confirms completeness.
- Status value distribution matches expected curation states (e.g., all status values are valid MIBiG curation categories); verify no truncated or partial status strings.
- Row count in output CSV equals the number of JSON files successfully parsed; compare against recursive file count to confirm no records were dropped.

## Limitations

- The skill assumes the `cluster.status` field is present and consistently formatted across all JSON records; malformed or missing status fields will result in gaps or errors in the tabulation.
- No changelog is provided in the repository, so historical status changes cannot be reconstructed from a single snapshot—multiple versions or archived datasets would be needed to track status evolution over time.
- The skill produces a cross-sectional inventory only; it does not infer or validate the correctness of status assignments or detect inconsistencies in status logic across entries.

## Evidence

- [other] MIBiG curation data is maintained in JSON format with entry status tracked through the `cluster.status` field within each annotation record.: "MIBiG curation data is maintained in JSON format with entry status tracked through the `cluster.status` field within each annotation record."
- [other] Clone or access the mibig-json repository; recursively scan the `data` directory for all JSON files; parse each JSON file and extract the `cluster.status` field value; aggregate entries into a table grouped by status.: "1. Clone or access the mibig-json repository from github.com/mibig-secmet/mibig-json. 2. Recursively scan the `data` directory for all JSON files. 3. Parse each JSON file and extract the"
- [readme] The current datasets for MIBiG live in the `data` directory, entry status is now tracked via the `cluster.status` field.: "The current datasets for [MIBiG] live in the `data` directory, entry status is now tracked via the `cluster.status` field."
- [other] Export the summary table as a CSV file with columns: entry_id, cluster.status.: "Export the summary table as a CSV file with columns: entry_id, cluster.status."
