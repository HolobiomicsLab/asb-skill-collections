---
name: high-resolution-mass-spectrum-processing
description: Use when when you have high-resolution tandem mass spectra from proteomics experiments and need to search against a spectral library for both unmodified peptides and those with unknown or variable post-translational modifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  - Faiss
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.jproteome.8b00359
  title: ANN-SoLo
evidence_spans:
- '**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ann_solo_gpu_feature_hashing_cq
    doi: 10.1021/acs.jproteome.8b00359
    title: ANN-SoLo
  dedup_kept_from: coll_ann_solo_gpu_feature_hashing_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.8b00359
  all_source_dois:
  - 10.1021/acs.jproteome.8b00359
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# high-resolution-mass-spectrum-processing

## Summary

Accelerate open modification spectral library searching of high-resolution mass spectra by combining approximate nearest neighbor (ANN) indexing with cascade search and false discovery rate control. This skill enables rapid identification of both unmodified and post-translationally modified peptides by reducing the spectral library search space while maintaining sensitivity.

## When to use

When you have high-resolution tandem mass spectra from proteomics experiments and need to search against a spectral library for both unmodified peptides and those with unknown or variable post-translational modifications. Use this approach when the spectral library is large enough that exhaustive comparison to all library entries becomes computationally expensive, or when you require both speed and strict false discovery rate control to maximize identifications.

## When NOT to use

- Input spectra are low-resolution or from unit-mass instruments; ANN indexing and feature hashing assume sufficient spectral detail to preserve similarity in hash space.
- Spectral library is very small (< 1000 spectra) or exhaustive searching is already fast; the overhead of ANN indexing may not be justified.
- Your goal is to identify only known, unmodified peptides with no interest in open modification searching; a simpler direct library search would suffice.

## Inputs

- high-resolution mass spectra (query set, e.g., mzML or mzXML format)
- high-resolution spectral library (annotated reference spectra)
- spectral preprocessing parameters (normalization, intensity thresholding)

## Outputs

- ranked peptide identifications with unmodified and open modification matches
- identification scores (shifted dot product scores) per query spectrum
- false discovery rate estimates per cascade stage

## How to apply

Load query high-resolution mass spectra and the spectral library in their native format. Convert spectra to fixed-size feature hash vectors to reduce dimensionality while preserving similarity structure. Index the hashed library spectra using approximate nearest neighbor indexing (Faiss) to enable rapid candidate retrieval of only the most relevant library entries. Apply a cascade search strategy: begin with unmodified peptide matching, then perform open modification searches on candidates that fall below the unmodified match threshold. Apply strict false discovery rate control at each cascade stage using the shifted dot product score to sensitively match modified spectra. Return ranked candidate matches with identification scores for each query spectrum.

## Related tools

- **ANN-SoLo** (spectral library search engine implementing approximate nearest neighbor indexing, cascade search, and FDR control for open modification searching) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (approximate nearest neighbor indexing library used to rapidly retrieve candidate library spectra; supports GPU acceleration) — https://github.com/facebookresearch/faiss

## Examples

```
pip install ann_solo; ann_solo --library spectral_library.mgf --spectrum query_spectra.mzML --output results.tsv
```

## Evaluation signals

- Ranked candidates returned for each query spectrum with non-negative shifted dot product scores; top-ranked match indicates most similar library entry.
- False discovery rate estimates reported per cascade stage and cumulatively remain below specified threshold (typically 1% or 5%).
- Number of identifications (both unmodified and open modification) exceeds those from exhaustive search with equivalent FDR threshold, indicating improved sensitivity.
- Query spectra with known ground-truth modifications are correctly matched to modified library entries in the open modification stage (not rejected as FDR-filtered).
- Search runtime for a fixed query set is substantially lower than exhaustive spectral library search, confirming ANN indexing speedup.

## Limitations

- Feature hashing reduces spectral information to a fixed-size vector; collisions in the hash table may lose fine details necessary to distinguish very similar spectra.
- ANN indexing is approximate; there is a small probability that the true nearest neighbor is not retrieved if it falls outside the candidate set selected by the index.
- GPU-accelerated version requires NVIDIA CUDA-enabled GPUs and is limited to Linux; CPU-only version supports Linux and OSX but is substantially slower.
- Python 3.6–3.9 required; Python 3.10 and newer are not yet supported, which may limit compatibility with newer environments.

## Evidence

- [intro] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [intro] Cascade search strategy combined with false discovery rate control: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate"
- [other] Feature hashing and GPU acceleration enable extremely fast searching: "The second publication describes a method that combines feature hashing and graphics processing units (GPU acceleration) to enable extremely fast and accurate open modification spectral library"
- [readme] Shifted dot product score used for modification matching: "the shifted dot product score to sensitively match modified spectra to their unmodified counterpart"
- [readme] GPU-powered version available on Linux with NVIDIA CUDA: "The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device, while the CPU-only version supports both the Linux and OSX platforms"
