---
name: cosine-distance-clustering-of-genomic-clusters
description: Use when you have pre-computed BGC feature vectors (e.g., from HMM domain
  hits extracted via antiSMASH or BiG-SLiCE) and need to group similar BGCs into families
  for comparative genomics, functional prediction, or novelty assessment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_0182
  tools:
  - BiG-SLiCE
  - pyHMMER
  - antiSMASH v7.0.0
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

# cosine-distance-clustering-of-genomic-clusters

## Summary

Groups Biosynthetic Gene Clusters (BGCs) into Gene Cluster Families (GCFs) by applying l2-normalization to feature vectors and performing hierarchical or flat clustering using cosine distance as the metric. This approach enables fast, scalable comparison of BGC domain architectures across large microbial sequence collections.

## When to use

You have pre-computed BGC feature vectors (e.g., from HMM domain hits extracted via antiSMASH or BiG-SLiCE) and need to group similar BGCs into families for comparative genomics, functional prediction, or novelty assessment. Use this skill when you want distance-based clustering that is invariant to feature vector magnitude and suitable for high-dimensional sparse domain composition data.

## When NOT to use

- Input feature vectors are already normalized and you do not need to recompute l2-normalization (re-normalizing may degrade precision).
- You require Euclidean or Manhattan distance for domain-count data; cosine distance is specific to normalized magnitude-invariant comparison.
- Your BGC feature vectors contain missing values or are in sparse formats not amenable to direct l2-normalization without preprocessing.

## Inputs

- Pre-computed BGC feature vectors (matrix: n_bgcs × n_features, as floats or integers)
- BGC identifiers (list of strings, one per row in feature matrix)
- Clustering parameters (e.g., distance threshold, linkage method if hierarchical)

## Outputs

- BGC-to-GCF mapping table (TSV: BGC ID → GCF cluster ID)
- Cluster membership assignments (vector of integers, one label per BGC)
- Optional: GCF summary statistics (e.g., cluster size, centroid, within-cluster distance variance)

## How to apply

Load pre-computed BGC feature vectors (raw or normalized) into memory. Apply l2-normalization to all feature vectors independently to convert them to unit-norm representations, enabling cosine-distance computation. Perform hierarchical or flat clustering on the normalized vectors using cosine distance as the similarity metric (computed as 1 − cosine similarity). Assign each BGC to a GCF based on cluster membership, optionally setting a distance threshold or cut-off height to control GCF granularity. Export the BGC-to-GCF mapping as a TSV file with BGC identifier and GCF cluster ID columns for downstream analysis.

## Related tools

- **BiG-SLiCE** (Reference implementation for l2-normalized cosine-distance clustering of BGC feature vectors; orchestrates full workflow from HMM scanning to GCF export) — https://github.com/medema-group/bigslice
- **pyHMMER** (Extracts HMM-based domain features from BGCs that serve as input to the feature vectors; used by BiG-SLiCE v2 for speed improvements over HMMER CLI) — https://github.com/althonos/pyhmmer
- **antiSMASH v7.0.0** (Defines BGC boundaries and initial domain annotations; outputs GenBank files used to generate feature vectors for clustering)

## Evaluation signals

- All BGC feature vectors are l2-normalized (verify L2 norm ≈ 1.0 for each row; check via `np.linalg.norm(vectors, axis=1, ord=2)` ≈ 1.0).
- Pairwise cosine distances between normalized vectors fall in range [0, 2] and are symmetric (distance(A,B) = distance(B,A)).
- BGC-to-GCF mapping is a valid partition (each BGC assigned to exactly one GCF; no orphaned BGCs).
- GCFs with similar BGCs have low within-cluster cosine distances; GCFs with dissimilar BGCs have high between-cluster distances (visual or statistical separation test).
- TSV export file has exactly n_bgcs rows (excluding header) with two columns (BGC ID and GCF cluster ID); no duplicate BGC IDs; all GCF IDs are integers or strings.

## Limitations

- L2-normalization assumes feature vectors are non-zero or near-zero for all BGCs; zero vectors or vectors with all small values may produce numerical instability.
- Cosine distance treats all domains equally and loses information about domain order or synteny; suitable only for domain composition comparison, not for genomic context.
- The choice of clustering linkage method (single, complete, average, ward) and distance threshold significantly affect GCF granularity; no universally optimal threshold is provided by the method alone.
- Large feature dimensionality (e.g., >10,000 domains in PFAM database) can cause cosine distance to become less discriminative due to the curse of dimensionality in high-dimensional spaces.

## Evidence

- [other] BiG-SLiCE v2 groups BGC feature vectors into GCFs by applying l2-normalization to compute cosine-like distances.: "BiG-SLiCE v2 groups BGC feature vectors into GCFs by applying l2-normalization to compute cosine-like distances between vectors"
- [other] Apply l2-normalization and perform clustering using cosine distance as the metric.: "Apply l2-normalization to all feature vectors to enable cosine-like distance computation. 3. Perform hierarchical or flat clustering on the normalized vectors using cosine distance as the metric."
- [readme] Clustering now uses cosine-like distances via l2-normalization in version 2.0.: "Clustering now uses __cosine-like__ (via l2-normalization) distances"
- [other] Export BGC-to-GCF mapping as TSV with BGC identifier and GCF cluster ID columns.: "Export the BGC-to-GCF mapping as a TSV table with BGC identifier and GCF cluster ID columns."
- [readme] BiG-SLiCE now uses pyHMMER for speed-ups and can be fully installed via pip.: "Switching from HMMER to [pyHMMER](https://github.com/althonos/pyhmmer) (__speed-ups__, can now be fully installed via __pip__)"
- [readme] Ability to export pre-calculated BGCs and GCFs table into TSVs using --export-csv parameter.: "Ability to __export pre-calculated BGCs and GCFs table into TSVs__ (use __--export-csv__ parameter)"
