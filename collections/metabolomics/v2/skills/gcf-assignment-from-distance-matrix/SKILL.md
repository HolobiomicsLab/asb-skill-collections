---
name: gcf-assignment-from-distance-matrix
description: Use when when you have pre-computed BGC feature vectors (from domain architecture or other representations) and need to group them into functionally coherent GCFs for comparative analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0160
  - http://edamontology.org/topic_3391
  tools:
  - BiG-SLiCE
  - pyHMMER
  - antiSMASH v7.0.0
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
---

# GCF assignment from distance matrix

## Summary

Assigns biosynthetic gene clusters (BGCs) to Gene Cluster Families (GCFs) by performing hierarchical or flat clustering on l2-normalized BGC feature vectors using cosine distance as the metric. This skill implements the distance-based grouping step that is central to the BiG-SLiCE v2 clustering pipeline.

## When to use

When you have pre-computed BGC feature vectors (from domain architecture or other representations) and need to group them into functionally coherent GCFs for comparative analysis. Use this skill after feature extraction but before downstream comparative genomics or biosynthetic diversity profiling. Cosine-distance clustering is particularly suitable when BGC representations are sparse or high-dimensional.

## When NOT to use

- Input is already a pre-computed GCF assignment table or clustering result; use this skill only when starting from raw or normalized feature vectors.
- BGC feature vectors have not been extracted yet; use domain annotation tools (e.g., antiSMASH, pyHMMER) first.
- You require Euclidean distance clustering rather than cosine distance; this skill is optimized for normalized representations.

## Inputs

- BGC feature vectors (raw or pre-normalized)
- BGC identifiers (e.g., antiSMASH output IDs)

## Outputs

- BGC-to-GCF mapping table (TSV format with BGC ID and GCF cluster ID columns)
- GCF cluster assignments

## How to apply

Load pre-computed BGC feature vectors into memory and apply l2-normalization to all vectors to convert Euclidean distances into cosine-like distances. Perform hierarchical or flat clustering on the normalized vectors using cosine distance as the metric, which measures the angle between normalized vectors rather than their magnitude. Assign each BGC to a GCF cluster based on the clustering result using a distance threshold appropriate to your biological context (typically guided by the dendrogram or silhouette analysis). Export the BGC-to-GCF mapping as a two-column TSV table with BGC identifier and GCF cluster ID. The rationale for l2-normalization is that it eliminates the magnitude component of feature vectors, allowing the distance metric to reflect only compositional similarity—important for BGCs with varying numbers of domains.

## Related tools

- **BiG-SLiCE** (Primary clustering engine that implements l2-normalization and cosine-distance-based hierarchical/flat clustering for GCF assignment) — https://github.com/medema-group/bigslice
- **pyHMMER** (Fast HMMER3 bindings used by BiG-SLiCE v2 for profile-HMM domain annotation to generate input feature vectors) — https://github.com/althonos/pyhmmer
- **antiSMASH v7.0.0** (BGC detection and gene cluster definition tool; output is used as input for feature extraction and clustering)

## Examples

```
bigslice -i <input_folder> <output_folder> && python -c "import sqlite3; conn = sqlite3.connect('<output_folder>/result.db'); cursor = conn.execute('SELECT bgc_id, gcf_id FROM bgc_to_gcf'); [print(f'{row[0]}	{row[1]}') for row in cursor.fetchall()]"
```

## Evaluation signals

- All BGCs receive exactly one GCF assignment; no missing or duplicate assignments.
- l2-norm of each normalized feature vector equals 1.0 (or very close due to floating-point precision).
- Cosine distances between vectors in the same GCF are consistently smaller than distances between vectors assigned to different GCFs (verify via silhouette coefficient or Davies–Bouldin index).
- Output TSV is valid and parseable, with non-empty BGC ID and GCF ID columns for all rows.
- GCF cluster IDs are contiguous integers or strings with no gaps or collisions.

## Limitations

- Clustering quality depends heavily on the quality and coverage of the input feature vectors; poor domain annotation upstream will degrade GCF assignments.
- The choice of distance threshold or clustering algorithm (hierarchical vs. flat) is not explicitly specified in the source material; users must calibrate this based on their biological context.
- No changelog or detailed algorithmic justification is available in the source documentation; the rationale for cosine distance is cited from an external publication (https://www.nature.com/articles/s41564-022-01110-2).
- Scalability on very large BGC collections (>10^6 clusters) is not quantified; memory requirements for the normalized feature matrix may become prohibitive.

## Evidence

- [readme] Clustering now uses cosine-like (l2-normalized) distances: "Clustering now uses __cosine-like__ (via l2-normalization) distances"
- [other] Apply l2-normalization to enable cosine-like distance computation: "Apply l2-normalization to all feature vectors to enable cosine-like distance computation"
- [other] Perform hierarchical or flat clustering on normalized vectors: "Perform hierarchical or flat clustering on the normalized vectors using cosine distance as the metric"
- [other] Export BGC-to-GCF mapping as TSV table: "Export the BGC-to-GCF mapping as a TSV table with BGC identifier and GCF cluster ID columns"
- [readme] Ability to export pre-calculated BGCs and GCFs into TSVs: "Ability to __export pre-calculated BGCs and GCFs table into TSVs__ (use __--export-csv__ parameter)"
