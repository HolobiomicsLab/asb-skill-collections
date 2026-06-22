---
name: peptide-level-spectrum-grouping
description: Use when after embedding MS/MS spectra into a 32-dimensional vector space using GLEAMS, when you need to identify and group all spectra originating from the same peptide sequence.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - GLEAMS
  - Python
derived_from:
- doi: 10.1038/s41592-022-01496-1
  title: GLEAMS
evidence_spans:
- GLEAMS encodes mass spectra as vectors of features and feeds them to a neural network
- GLEAMS is a Learned Embedding for Annotating Mass Spectra. GLEAMS encodes mass spectra as vectors of features and feeds them to a neural network
- GLEAMS requires Python 3.8, a Linux operating system, and a CUDA-enabled GPU
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-022-01496-1
  all_source_dois:
  - 10.1038/s41592-022-01496-1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peptide-level-spectrum-grouping

## Summary

Group mass spectra into clusters corresponding to the same peptide by applying hierarchical clustering to 32-dimensional neural network embeddings. This skill enables efficient detection of spectrum redundancy and peptide-centric analysis across large spectral datasets.

## When to use

Apply this skill after embedding MS/MS spectra into a 32-dimensional vector space using GLEAMS, when you need to identify and group all spectra originating from the same peptide sequence. Use it to consolidate redundant spectral observations, prepare data for spectral library construction, or enable peptide-level summary statistics across millions of spectra.

## When NOT to use

- Input spectra have not yet been embedded into the 32-dimensional GLEAMS space; use the embed step first.
- Spectra are from organisms or conditions not well-represented in the GLEAMS training data (30 million PSMs from MassIVE-KB Human HCD library); clustering may be unreliable.
- Goal is to group spectra by charge state, modification, or instrument rather than by peptide identity; this skill is peptide-specific.

## Inputs

- 32-dimensional embedding vectors (NumPy array, n × 32 format)
- Embedding metadata file (parquet format with spectrum identifiers and scan information)

## Outputs

- Cluster assignment labels per embedding (NumPy array, n elements, one label per spectrum)
- Cluster medoid indices (NumPy array identifying representative spectrum per cluster)
- Cluster membership mapping (spectrum identifier to cluster ID)

## How to apply

Execute the `gleams cluster` command on the 32-dimensional embedding vectors (.npy file) produced by the embed step, specifying a distance threshold (typically 0.3) to control cluster granularity. The method performs hierarchical clustering on the embeddings in the space where spectra from the same peptide are known to cluster proximally. The clustering assigns each spectrum to a cluster label (or -1 for noise if it does not meet the minimum cluster size of 2), and outputs both cluster assignments and medoid indices identifying representative spectra for each cluster. Verify clustering quality by inspecting the distribution of cluster sizes and confirming that cluster medoids have high cosine similarity to other members.

## Related tools

- **GLEAMS** (Provides the `gleams cluster` command to perform hierarchical clustering on 32-dimensional embeddings with configurable distance threshold and minimum cluster size.) — https://github.com/bittremieux/GLEAMS
- **Python** (Required runtime environment (Python 3.8+) for executing GLEAMS clustering commands.)

## Examples

```
gleams cluster --embed_name GLEAMS_embed --cluster_name GLEAMS_cluster --distance_threshold 0.3
```

## Evaluation signals

- Cluster size distribution is reasonable (no singleton clusters; median cluster size > 1); clusters with -1 label (noise) represent <5% of spectra unless data is highly sparse.
- Medoids from each cluster have high within-cluster homogeneity: mean cosine similarity of medoid to other cluster members is >0.7.
- Cross-validation: re-embed a subset of spectra and verify they cluster with their original cluster members at the same distance threshold.
- Output files are non-empty: GLEAMS_cluster.npy contains cluster labels matching the number of input embeddings, and GLEAMS_cluster_medoids.npy contains at least one valid spectrum index per cluster.
- Cluster membership is stable across reruns with the same distance threshold (deterministic hierarchical clustering output).

## Limitations

- Clustering quality depends critically on the distance threshold parameter (default 0.3); no principled method for threshold selection is provided in the documentation.
- GLEAMS embedding space is optimized for human HCD spectra from the MassIVE-KB training set; performance on spectra from other organisms, instruments (e.g., Orbitrap, MALDI), or ionization methods is not characterized.
- Minimum cluster size of 2 may exclude genuine low-abundance peptides observed in only one spectrum.
- Clustering is unsupervised; there is no direct validation that clusters correspond to true peptide sequences without independent peptide identification data.

## Evidence

- [readme] After converting the MS/MS spectra to 32-dimensional embeddings, they can be clustered to group spectra with similar embeddings using the `gleams cluster` command.: "After converting the MS/MS spectra to 32-dimensional embeddings, they can be clustered to group spectra with similar embeddings using the `gleams cluster` command."
- [readme] This will perform hierarchical clustering on the embeddings with the given distance threshold. The output will be written to the `GLEAMS_cluster.npy` NumPy file with cluster labels per embedding (`-1` indicates noise, minimum cluster size 2).: "This will perform hierarchical clustering on the embeddings with the given distance threshold. The output will be written to the `GLEAMS_cluster.npy` NumPy file with cluster labels per embedding"
- [intro] GLEAMS embeds mass spectra into a 32-dimensional space where spectra from the same peptide cluster together.: "GLEAMS embeds mass spectra into a 32-dimensional space where spectra from the same peptide cluster together"
- [intro] It then detects spectrum clusters of spectra generated by the same peptide.: "It then detects spectrum clusters of spectra generated by the same peptide."
- [readme] Additionally, a file `GLEAMS_cluster_medoids.npy` will be created containing indexes of the cluster representative spectra (medoids).: "Additionally, a file `GLEAMS_cluster_medoids.npy` will be created containing indexes of the cluster representative spectra (medoids)."
