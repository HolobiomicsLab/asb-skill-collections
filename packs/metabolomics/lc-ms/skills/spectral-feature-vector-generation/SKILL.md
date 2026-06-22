---
name: spectral-feature-vector-generation
description: Use when you have a collection of MS/MS spectra in standard formats (mzML, MGF) and need to perform rapid similarity search, clustering, or joint analysis across millions of spectra without repeated peptide database searches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - GLEAMS
  - Python
  - Conda
  - NumPy
  techniques:
  - LC-MS
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

# spectral-feature-vector-generation

## Summary

Encode tandem mass spectrometry (MS/MS) spectra into fixed-dimensional feature vectors using a pre-trained neural network encoder, producing a 32-dimensional embedding space where spectra from the same peptide cluster together. This is a prerequisite step for downstream spectrum similarity analysis and peptide identification.

## When to use

Apply this skill when you have a collection of MS/MS spectra in standard formats (mzML, MGF) and need to perform rapid similarity search, clustering, or joint analysis across millions of spectra without repeated peptide database searches. Use it as the first step in the GLEAMS workflow to convert raw peak data into normalized, comparable vector representations.

## When NOT to use

- Do not use this skill if you require spectrum annotation or peptide sequence assignment; GLEAMS embedding alone does not identify peptides—it only produces comparable vector representations.
- Do not use this skill if your spectra are in formats other than mzML or MGF without prior conversion; unsupported file types will cause execution failure.
- Do not use this skill if you lack a CUDA-enabled GPU or a Linux operating system; GLEAMS encoder requires GPU acceleration and does not run on Windows or macOS.
- Do not use this skill if you need feature interpretability at the peak level; the 32-dimensional embedding is a learned, non-linear transformation and individual dimensions do not correspond to specific m/z values or ion types.

## Inputs

- MS/MS spectra file in mzML format
- MS/MS spectra file in MGF format
- Pre-trained GLEAMS neural network model weights (HDF5 file)

## Outputs

- NumPy array (n × 32) of 32-dimensional spectrum embeddings
- Parquet file containing spectrum metadata (scan numbers, precursor m/z, retention time, etc.)
- GLEAMS_embed.npy embedding vectors
- GLEAMS_embed.parquet metadata table

## How to apply

First, prepare your mass spectra input file in a format recognized by GLEAMS (e.g., mzML or MGF). Execute the `gleams embed` command on the input spectra file; the pre-trained neural network encoder will process each spectrum as feature vectors and project them into 32-dimensional space via the installed GLEAMS model weights (pre-trained on 30 million PSMs from MassIVE-KB). The command outputs a two-dimensional NumPy array (n × 32, where n is the number of spectra) and a corresponding metadata parquet file. Verify correctness by confirming that the embedding array dimensions match your input spectrum count and that spectra known to derive from the same peptide occupy nearby positions in the 32-dimensional space (measurable via cosine distance or Euclidean distance on the embeddings).

## Related tools

- **GLEAMS** (Pre-trained neural network encoder that transforms peak spectra into 32-dimensional embeddings; invoked via the `gleams embed` command) — https://github.com/bittremieux/GLEAMS
- **Python** (Required runtime environment (Python 3.8+) for executing GLEAMS and processing output NumPy arrays and parquet metadata files)
- **Conda** (Package manager used to create isolated environment with GPU runtime (CUDA) and compiler dependencies for GLEAMS installation)
- **NumPy** (Library for reading and manipulating the output embedding array (n × 32 matrix) and computing distances between embeddings)

## Examples

```
gleams embed *.mzML --embed_name GLEAMS_embed
```

## Evaluation signals

- Embedding output array shape is exactly (n_spectra, 32) where n_spectra matches the number of spectra in the input file
- Parquet metadata file contains one row per spectrum with non-null scan numbers and precursor m/z values
- Spectra confirmed to originate from the same peptide (e.g., same sequence, same charge state from replicate runs) have cosine similarity > 0.7 or Euclidean distance < 0.3 in the 32-dimensional space
- Embedding vectors have zero mean and unit variance across all spectra (standard normalization after neural network projection)
- No NaN or infinite values appear in the embedding array; all 32 dimensions contain finite floating-point numbers

## Limitations

- GLEAMS embeddings are peptide-centric; spectra from different post-translational modifications (PTMs) of the same peptide sequence may not cluster together if the PTM substantially alters fragmentation patterns.
- Model is trained exclusively on human high-collision-dissociation (HCD) spectra from MassIVE-KB; performance on non-human organisms, alternative ionization methods (e.g., ESI-CID), or novel instrument types is not characterized.
- Requires a CUDA-enabled GPU and Linux operating system; installation can fail due to Git LFS bandwidth limits when downloading pre-trained model weights (workaround documented in README: manual weight download and local installation).
- The 32-dimensional space is a learned, non-interpretable representation; individual dimensions do not correspond to semantic features (e.g., fragment ion types) and cannot be used for peak-level diagnosis of spectral quality.
- Embedding step alone does not perform peptide identification; downstream clustering or database search is required to assign sequences to spectra.

## Evidence

- [intro] GLEAMS encodes mass spectra as vectors of features and feeds them to a neural network to embed them into a 32-dimensional space in which spectra generated by the same peptide are close together.: "GLEAMS encodes mass spectra as vectors of features and feeds them to a neural network to embed them into a 32-dimensional space in which spectra generated by the same peptide are close together"
- [readme] GLEAMS provides the `gleams embed` command to convert MS/MS spectra in peak files to 32-dimensional embeddings. Example: gleams embed *.mzML --embed_name GLEAMS_embed: "GLEAMS provides the `gleams embed` command to convert MS/MS spectra in peak files to 32-dimensional embeddings. Example: gleams embed *.mzML --embed_name GLEAMS_embed"
- [readme] This will read the MS/MS spectra from all matched mzML files and export the results to a two-dimensional NumPy array of dimension n x 32 in file `GLEAMS_embed.npy`, with n the number of MS/MS spectra read from the mzML files. Additionally, a tabular file `GLEAMS_embed.parquet` will be created containing corresponding metadata for the embedded spectra.: "This will read the MS/MS spectra from all matched mzML files and export the results to a two-dimensional NumPy array of dimension n x 32 in file `GLEAMS_embed.npy`, with n the number of MS/MS spectra"
- [readme] GLEAMS requires Python 3.8, a Linux operating system, and a CUDA-enabled GPU.: "GLEAMS requires Python 3.8, a Linux operating system, and a CUDA-enabled GPU"
- [readme] GLEAMS was trained on 30 million PSMs from the MassIVE-KB (v1) dataset.: "GLEAMS was trained on 30 million PSMs from the MassIVE-KB (v1) dataset"
