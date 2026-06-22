---
name: aggregate-statistics-computation
description: 'Use when you have a validated or curated dataset (e.g., a TSV or gzip-compressed tabular file) and need to produce summary counts: unique curated structures (separately for 3D and 2D representations), unique organisms, and unique structure-organism pair combinations.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3050
  tools:
  - R
  - Python 3
  - lotus-processor
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- db/../standardizing.R, common.R
- 1_integrating.R
- Python scripts for data parsing and transformation
- 221[[smiles.py]]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus_cq
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.7554/eLife.70780
  all_source_dois:
  - 10.7554/eLife.70780
  - 10.1007/s00044-016-1764-y
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# aggregate-statistics-computation

## Summary

Compute summary statistics (counts of unique entities and their combinations) over a deduplicated dataset to produce structured aggregate metrics. This skill is essential for validating data completeness and generating high-level summaries of large curated collections.

## When to use

Apply this skill when you have a validated or curated dataset (e.g., a TSV or gzip-compressed tabular file) and need to produce summary counts: unique curated structures (separately for 3D and 2D representations), unique organisms, and unique structure-organism pair combinations. Use it to validate dataset size, document data availability statements, or populate metadata tables for publication or archival.

## When NOT to use

- Input dataset is not yet deduplicated or validated; apply deduplication/cleaning steps before aggregation.
- You need granular per-structure or per-organism statistics (e.g., frequency distributions, occurrence counts); use a different skill for those.
- The dataset is still in raw or semi-curated form; ensure it has passed validation gates (e.g., organism/structure/reference subgraph curation steps) first.

## Inputs

- Validated/curated dataset file (TSV, TSV.GZ, or tabular format)
- Structure identifier column(s) (SMILES, InChI, or nominal ID)
- Organism taxonomy identifier column
- Structure-organism pair composite keys
- Structure format annotation (3D, 2D, or both)

## Outputs

- Structured summary table (CSV or TSV) with rows: unique_structures_3d, unique_structures_2d, unique_organisms, unique_pairs_3d_2d, unique_pairs_total
- Deduplicated structure identifier list (optional)
- Deduplicated organism identifier list (optional)
- Validation report (count agreement vs. expected thresholds)

## How to apply

Load the validated dataset (e.g., interim/tables/4_analysed/platinum.tsv.gz) into R or Python. Extract and deduplicate structure identifiers (SMILES, InChI, or nominal identifiers) to count unique curated structures, recording counts separately for 3D and 2D format variants. Similarly, extract and deduplicate organism taxonomy identifiers to count unique organisms. Then extract and deduplicate all structure-organism pair combinations, again stratified by 3D/2D format. Validate that counts match expected aggregates (e.g., 231330 unique 3D structures, 153956 unique 2D structures, 42166 organisms, 588694 total structure-organism pairs with 484174 in 3D|2D format). Export all counts to a structured summary table (CSV or TSF) with rows for each metric and columns for count value and data format classification.

## Related tools

- **R** (Load TSV data, perform deduplication (unique(), table()), aggregate counts, export summary table) — https://www.r-project.org
- **Python 3** (Load gzipped TSV, deduplicate using pandas (drop_duplicates()), compute value_counts(), export CSV) — https://www.python.org
- **lotus-processor** (Provides validated interim dataset (platinum.tsv.gz) and pipeline context for aggregation) — https://github.com/lotusnprod/lotus-processor

## Examples

```
# Load, deduplicate, and count using Python:
python3 -c "import pandas as pd; df=pd.read_csv('platinum.tsv.gz', sep='\t'); print(f'Unique structures 3D: {len(df[df.format==\"3D\"][\"structure_id\"].unique())}'); print(f'Unique organisms: {len(df[\"organism_id\"].unique())}'); print(f'Unique pairs: {len(df[[\"structure_id\",\"organism_id\"]].drop_duplicates())}'); df_summary=pd.DataFrame([{\"metric\":\"structures_3d\",\"count\":len(df[df.format==\"3D\"][\"structure_id\"].unique())}]); df_summary.to_csv('summary.tsv', sep='\t', index=False)"
```

## Evaluation signals

- Count of unique 3D structures equals 231330 (or documented expected value) and is strictly ≤ total unique structures.
- Count of unique 2D structures equals 153956 (or documented expected value) and is strictly ≤ total unique structures.
- Count of unique organisms equals 42166 (or documented expected value).
- Count of unique structure-organism pairs (total) equals 588694 (or documented expected value); 3D|2D subset equals 484174.
- All deduplication operations preserve row cardinality: sum of pair counts across all organisms equals total pairs; no negative counts or NaN values in output table.

## Limitations

- Deduplication depends critically on identifier consistency: if structure IDs are heterogeneous (e.g., SMILES vs. InChI variants for the same compound), counts may be artificially inflated.
- Format stratification (3D vs. 2D) requires reliable annotation in the input; missing or inconsistent format labels will distort stratified counts.
- Memory usage scales with dataset size; for very large collections (>1M rows), streaming or chunked processing may be necessary.

## Evidence

- [methods] Exact counts definition: "231330 | 153956 (3D|2D) unique curated structures and 42166 unique organisms"
- [methods] Pair count definition: "588694 | 484174 (3D|2D) unique referenced structure-organism pairs"
- [methods] Input dataset location: "Load the validated platinum dataset (interim/tables/4_analysed/platinum.tsv.gz)"
- [methods] Deduplication method: "Extract and deduplicate structure identifiers (SMILES, InChI, or nominal identifiers) to count unique curated structures, separately for 3D and 2D structure representations."
- [methods] Output format and validation: "Export counts to a structured summary table (CSV or TSV) with rows for each metric and columns for count value and data format."
- [readme] Tool requirements: "R, Python 3, Java >= 17"
