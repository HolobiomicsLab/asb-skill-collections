---
name: peptide-spectrum-representation-learning
description: Use when you have a collection of MS/MS spectra (in mzML or MGF format) and need to group or compare spectra from the same peptide without prior sequence annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - GLEAMS
  - Python
  - Conda
  - CUDA-enabled GPU
derived_from:
- doi: 10.1038/s41592-022-01496-1
  title: GLEAMS
evidence_spans:
- GLEAMS encodes mass spectra as vectors of features and feeds them to a neural network
- GLEAMS is a Learned Embedding for Annotating Mass Spectra. GLEAMS encodes mass spectra as vectors of features and feeds them to a neural network
- GLEAMS requires Python 3.8, a Linux operating system, and a CUDA-enabled GPU
- Create a Conda environment and install the necessary compiler tools and GPU runtime
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gleams_cq
    doi: 10.1038/s41592-022-01496-1
    title: GLEAMS
  dedup_kept_from: coll_gleams_cq
schema_version: 0.2.0
---

# peptide-spectrum-representation-learning

## Summary

Learn a low-dimensional neural network embedding of mass spectra such that spectra from the same peptide cluster together in a 32-dimensional space. This enables efficient joint analysis of millions of MS/MS spectra by converting high-dimensional peak data into a compact, semantically meaningful representation suitable for downstream clustering and annotation.

## When to use

You have a collection of MS/MS spectra (in mzML or MGF format) and need to group or compare spectra from the same peptide without prior sequence annotation. This skill is especially valuable when processing large-scale spectral datasets (millions of spectra) where pairwise similarity computation becomes computationally prohibitive, or when you want to detect spectrum clusters corresponding to the same peptide independent of database search results.

## When NOT to use

- Your spectra are already annotated with high-confidence peptide identifications and you only need to validate or refine those assignments — use a spectrum library search or peptide scoring method instead.
- You need real-time, single-spectrum queries against a reference library — GLEAMS is designed for batch processing and offline clustering, not online retrieval.
- Your input spectra are from non-standard instruments or fragmentation methods (e.g., ETD, ECD) that are significantly different from the HCD/CID spectra used in the MassIVE-KB training set — generalization may be poor.

## Inputs

- MS/MS spectra in mzML format
- MS/MS spectra in MGF format
- Peak list files compatible with GLEAMS input format

## Outputs

- 32-dimensional embedding vectors (NumPy array, n × 32)
- Spectrum metadata table (Parquet format)
- Cluster assignments (optional, via gleams cluster)

## How to apply

Prepare your MS/MS spectra in mzML or MGF format, then invoke the `gleams embed` command to encode each spectrum as a feature vector and pass it through a pre-trained neural network encoder. The encoder projects each spectrum into a 32-dimensional space in which spectra derived from the same peptide are positioned close together. The output is a NumPy array (n × 32) where n is the number of spectra, plus a Parquet metadata file. You can then apply hierarchical clustering (e.g., via `gleams cluster` with a distance threshold of 0.3) on these embeddings to detect spectrum clusters; the rationale is that Euclidean distance in the learned embedding space reflects spectral and peptide similarity more reliably than raw peak-space metrics.

## Related tools

- **GLEAMS** (Pre-trained neural network encoder that transforms mass spectra into 32-dimensional embeddings via the `gleams embed` command) — https://github.com/bittremieux/GLEAMS
- **Python** (Required runtime environment; GLEAMS requires Python 3.8+)
- **Conda** (Dependency and environment management for installing GLEAMS and GPU runtime)
- **CUDA-enabled GPU** (Hardware accelerator required for efficient neural network inference during embedding computation)

## Examples

```
gleams embed *.mzML --embed_name GLEAMS_embed
```

## Evaluation signals

- Output embedding array has shape (n, 32) where n equals the number of input spectra, with no NaN or Inf values.
- Spectra known to originate from the same peptide (via database search or manual curation) have Euclidean distances < 0.3 in embedding space; cross-peptide distances are > 0.3.
- Downstream hierarchical clustering with distance threshold 0.3 produces clusters in which >90% of spectra share the same peptide annotation (precision) and >85% of spectra from the same peptide are grouped together (recall).
- Metadata Parquet file contains one row per spectrum with consistent indexing and no missing values for scan numbers or precursor m/z.
- Runtime scales approximately linearly with spectral count; embedding computation for 1 million spectra completes within expected GPU-accelerated time (typically hours, not days).

## Limitations

- GLEAMS requires a Linux operating system and a CUDA-enabled GPU; CPU-only systems are not supported.
- The pre-trained model was optimized on 30 million PSMs from HCD/CID fragmentation of human proteomes in the MassIVE-KB dataset; performance on spectra from non-standard fragmentation methods (ETD, UVPD) or organism-specific proteomes may be degraded.
- The 32-dimensional space is optimized for grouping spectra by peptide identity but does not explicitly capture post-translational modification states; PTM-bearing spectra from the same sequence may not cluster tightly.
- Very low-abundance or noisy spectra with few detected peaks may produce poor embeddings or be assigned to noise clusters (label -1) during clustering.
- Installation can encounter Git LFS bandwidth quota errors; manual download of pre-trained model weights may be required as a workaround.

## Evidence

- [intro] GLEAMS encodes mass spectra as vectors of features and feeds them to a neural network to embed them into a 32-dimensional space in which spectra generated by the same peptide are close together.: "GLEAMS encodes mass spectra as vectors of features and feeds them to a neural network to embed them into a 32-dimensional space in which spectra generated by the same peptide are close together"
- [readme] GLEAMS provides the `gleams embed` command to convert MS/MS spectra in peak files to 32-dimensional embeddings.: "GLEAMS provides the `gleams embed` command to convert MS/MS spectra in peak files to 32-dimensional embeddings"
- [readme] This will read the MS/MS spectra from all matched mzML files and export the results to a two-dimensional NumPy array of dimension n x 32.: "export the results to a two-dimensional NumPy array of dimension n x 32 in file `GLEAMS_embed.npy`, with n the number of MS/MS spectra"
- [readme] GLEAMS requires Python 3.8, a Linux operating system, and a CUDA-enabled GPU.: "GLEAMS requires Python 3.8, a Linux operating system, and a CUDA-enabled GPU"
- [readme] GLEAMS was trained on 30 million PSMs from the MassIVE-KB (v1) dataset.: "GLEAMS was trained on 30 million PSMs from the MassIVE-KB (v1) dataset"
- [intro] It then detects spectrum clusters of spectra generated by the same peptide.: "It then detects spectrum clusters of spectra generated by the same peptide"
- [readme] This will perform hierarchical clustering on the embeddings with the given distance threshold.: "This will perform hierarchical clustering on the embeddings with the given distance threshold"
