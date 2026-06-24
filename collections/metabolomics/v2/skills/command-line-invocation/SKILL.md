---
name: command-line-invocation
description: Use when after completing a BiG-SLiCE clustering analysis and needing
  to access the pre-calculated BGC and GCF cluster assignments in tabular format for
  spreadsheet analysis, statistical testing, or integration with other bioinformatics
  pipelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0160
  - http://edamontology.org/topic_3293
  tools:
  - BiG-SLiCE
  - pyHMMER
  license_tier: open
derived_from:
- doi: 10.1093/gigascience/giaa154
  title: BiG-SLiCE
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_big_slice_cq
    doi: 10.1093/gigascience/giaa154
    title: BiG-SLiCE
  dedup_kept_from: coll_big_slice_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/gigascience/giaa154
  all_source_dois:
  - 10.1093/gigascience/giaa154
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Export pre-calculated BGC and GCF tables to TSV via --export-csv

## Summary

Export pre-calculated Biosynthetic Gene Cluster (BGC) and Gene Cluster Family (GCF) tables from a completed BiG-SLiCE v2 clustering run into tab-separated values (TSV) format. This skill enables downstream tabular analysis and integration of clustering results into external workflows.

## When to use

After completing a BiG-SLiCE clustering analysis and needing to access the pre-calculated BGC and GCF cluster assignments in tabular format for spreadsheet analysis, statistical testing, or integration with other bioinformatics pipelines. Specifically when you have a completed BiG-SLiCE output directory and want TSV exports rather than programmatic SQL queries.

## When NOT to use

- If you require programmatic access to the full richness of the SQLite database schema and need to perform complex SQL joins or aggregations—use SQL queries directly on the database instead.
- If you have not yet completed a BiG-SLiCE clustering run—you must first execute the primary analysis (bigslice -i <input_folder> <output_folder>) to generate the output directory and database.
- If you need real-time or streaming export of results during an active clustering run—the --export-csv parameter operates only on completed runs.

## Inputs

- Completed BiG-SLiCE v2 output directory (containing SQLite3 database with pre-calculated BGC and GCF clustering results)

## Outputs

- TSV file(s) with pre-calculated BGC cluster table
- TSV file(s) with pre-calculated GCF cluster table

## How to apply

Invoke BiG-SLiCE with the --export-csv parameter on a completed run directory to export the pre-calculated BGC and GCF cluster tables into TSV format. The command takes a directory path containing prior clustering results and outputs TSV files to the same directory. This is performed after the primary clustering analysis (bigslice -i <input_folder> <output_folder>) has already completed and the SQLite database has been populated. The exported TSVs preserve the cluster assignments and similarity relationships computed during the l2-normalized cosine-like distance clustering, making them suitable for downstream tabular analysis without requiring SQL queries.

## Related tools

- **BiG-SLiCE** (Primary clustering tool that computes BGC and GCF tables; --export-csv parameter invoked on completed run output) — https://github.com/medema-group/bigslice
- **pyHMMER** (Underlying HMM profile matching engine used by BiG-SLiCE v2 to compute domain architectures; enables speed improvements in clustering workflow) — https://github.com/althonos/pyhmmer

## Examples

```
bigslice --export-csv <output_folder>
```

## Evaluation signals

- TSV files are successfully created in the output directory with expected filenames (e.g., containing 'BGC' and 'GCF' in their names).
- TSV files are readable as delimited text with tab characters and contain expected columns (e.g., cluster IDs, BGC/GCF identifiers, similarity scores).
- Row counts in exported TSV files match or exceed the number of BGCs and GCFs present in the SQLite database (checked via SQL SELECT COUNT).
- No errors or warnings are emitted during --export-csv invocation; command completes with exit code 0.
- Cluster assignments in TSV files are consistent with the cosine-like distance clustering (l2-normalized) performed during the primary run.

## Limitations

- TSV export is available only in BiG-SLiCE v2.0 or later; earlier versions do not support the --export-csv parameter.
- The exported TSVs represent a flattened snapshot of the clustering results and do not preserve the full hierarchical or graph structure of relationships that may exist in the underlying database.
- Very large clustering runs (>100,000 BGCs) may produce TSV files that are difficult to handle in spreadsheet applications; SQL queries on the database may be more practical for such cases.
- TSV export requires a successfully completed and valid BiG-SLiCE output directory; corrupted or incomplete databases will fail to export.

## Evidence

- [intro] Ability to export pre-calculated BGCs and GCFs table into TSVs: "Ability to __export pre-calculated BGCs and GCFs table into TSVs__ (use __--export-csv__ parameter)"
- [other] Workflow step: invoke BiG-SLiCE with --export-csv on completed run: "Invoke BiG-SLiCE with the --export-csv parameter on a completed run directory to export the pre-calculated BGC and GCF cluster tables"
- [other] Output retrieval via TSV files: "Retrieve the exported TSV files from the output directory"
- [readme] Clustering uses cosine-like distances enabling export consistency: "Clustering now uses __cosine-like__ (via l2-normalization) distances"
