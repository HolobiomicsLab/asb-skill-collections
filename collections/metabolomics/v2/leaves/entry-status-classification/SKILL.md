---
name: entry-status-classification
description: Use when you need to assess the overall curation coverage and quality
  of a MIBiG repository snapshot, identify which entries require further review, or
  track how entry validation status changes over time. Specifically use it when the
  `data` directory contains JSON files with `cluster.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0091
  tools:
  - mibig-json repository
  - MIBiG web interface
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/nar/gkz882
  title: MIBiG 2.0
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mibig_2_0_cq
    doi: 10.1093/nar/gkz882
    title: MIBiG 2.0
  dedup_kept_from: coll_mibig_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/nar/gkz882
  all_source_dois:
  - 10.1093/nar/gkz882
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# entry-status-classification

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and aggregate entry status values from MIBiG JSON curation records to build a searchable index of data quality and curation state across the repository. This skill is essential for understanding the completeness and validation stage of secondary metabolite biosynthetic gene cluster annotations.

## When to use

Apply this skill when you need to assess the overall curation coverage and quality of a MIBiG repository snapshot, identify which entries require further review, or track how entry validation status changes over time. Specifically use it when the `data` directory contains JSON files with `cluster.status` fields that must be indexed and reported.

## When NOT to use

- Input data is not from the MIBiG `data` directory or lacks `cluster.status` fields
- The goal is to retrieve sequence data rather than assess curation metadata — use the `genbanks` directory instead
- Entry status has already been indexed or is available from a pre-built status table

## Inputs

- MIBiG JSON files from the `data` directory
- Entry identifier fields (filename or internal ID)
- cluster.status field values from parsed JSON objects

## Outputs

- Structured index (CSV or JSON format) with entry ID and cluster status columns
- Aggregated entry-status mapping suitable for filtering or reporting

## How to apply

Clone or download the mibig-json repository, then systematically traverse all JSON files in the `data` directory. For each file, parse the JSON structure and extract two key fields: the entry identifier (from the filename or an internal ID field) and the `cluster.status` value, which indicates the curation or validation state of that entry. Aggregate these pairs into a structured format (CSV or JSON with columns for entry ID and cluster status). Validate completeness by confirming that all files in the `data` directory have been parsed and that no entries lack a status value. The rationale is that `cluster.status` is the authoritative field tracking entry state in MIBiG's curation workflow.

## Related tools

- **mibig-json repository** (Source repository containing JSON-formatted curation data with cluster.status fields) — https://github.com/mibig-secmet/mibig-json
- **MIBiG web interface** (Reference for understanding entry status terminology and curation guidelines) — https://mibig.secondarymetabolites.org/

## Examples

```
cd mibig-json && find data -name '*.json' -exec jq -r '[.cluster_number // .filename, .cluster.status] | @csv' {} + > entry_status_index.csv
```

## Evaluation signals

- All JSON files in the `data` directory are successfully parsed without errors
- Every entry in the index has a non-null, non-empty `cluster.status` value
- The count of indexed entries matches the total number of JSON files in `data`
- The generated index can be loaded and queried to filter entries by status
- Manual spot-check of 5–10 entries confirms that status values and IDs are correctly extracted

## Limitations

- No changelog is available in the repository, so version history and documentation of status value changes cannot be tracked
- The skill assumes `cluster.status` field is present in all JSON files; files with missing or malformed status fields may cause parsing failures or incomplete indexing
- Status terminology and valid values are not formally documented in the provided README, so interpretation of status strings requires external knowledge of MIBiG curation workflow

## Evidence

- [intro] MIBiG annotations are maintained in JSON format with entry status tracked via cluster.status field: "MIBiG curation data in JSON format. The current datasets for [MIBiG] live in the `data` directory, entry status is now tracked via the `cluster.status` field."
- [other] Workflow includes extraction of entry identifier and status field, aggregation into structured format, and validation of completeness: "For each JSON file, extract the entry identifier (filename or internal ID field) and the `cluster.status` field value. Aggregate results into a structured index (CSV or JSON format) with columns for"
- [discussion] No changelog available limits ability to track status changes over time: "No changelog found — version history and documentation of changes not available"
