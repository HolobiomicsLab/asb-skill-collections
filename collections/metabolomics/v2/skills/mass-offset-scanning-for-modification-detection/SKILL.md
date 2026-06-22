---
name: mass-offset-scanning-for-modification-detection
description: Use when you have a query mass spectrum of unknown modification status and need to search a spectral library to identify the peptide and its post-translational modifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  - Faiss
derived_from:
- doi: 10.1021/acs.jproteome.8b00359
  title: ANN-SoLo
evidence_spans:
- ANN-SoLo (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine
- '**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is a spectral library search engine'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ann_solo_cq
    doi: 10.1021/acs.jproteome.8b00359
    title: ANN-SoLo
  dedup_kept_from: coll_ann_solo_cq
schema_version: 0.2.0
---

# mass-offset-scanning-for-modification-detection

## Summary

Mass-offset scanning computes shifted dot product scores across a range of mass offset values to detect and match post-translational modifications in peptide spectra. This technique enables sensitive identification of modified spectra by comparing query spectra to library spectra at multiple mass shifts, operating as part of a cascade search strategy with false discovery rate control.

## When to use

Apply this skill when you have a query mass spectrum of unknown modification status and need to search a spectral library to identify the peptide and its post-translational modifications. Use it specifically when unmodified reference spectra exist in the library but the query spectrum may carry unknown mass shifts due to PTMs (e.g., phosphorylation, acetylation, oxidation). This skill is essential in open modification searching workflows where the modification type is not predefined.

## When NOT to use

- Input spectra are already annotated with known modification types and positions; use targeted searches instead of open modification detection.
- Mass accuracy is poor (>0.1 Da error) or spectrum quality is very low; mass offset scanning assumes adequate spectral resolution to resolve modification-induced shifts.
- Library contains only modified spectra or lacks unmodified reference spectra; the algorithm relies on comparing query spectra to a diverse library to disambiguate true modifications from noise.

## Inputs

- Query mass spectrum (m/z and intensity pairs)
- Spectral library (collection of reference spectra with known peptide and modification annotations)
- Mass offset range (e.g., −200 to +200 Da or domain-specific PTM masses)
- Normalized intensity vectors from query and library spectra

## Outputs

- Shifted dot product score matrix (spectra × mass offsets)
- Best-match score and corresponding mass offset for each query spectrum
- Ranked list of library matches with associated mass shifts
- False discovery rate-controlled identifications with modification assignments

## How to apply

Define a shifted dot product scoring algorithm that compares query spectra to library spectra by computing dot products across a discrete range of mass offset values (e.g., spanning common PTM masses). For each candidate library spectrum, normalize the intensity vectors and compute pairwise similarities at each offset. The algorithm returns a score distribution across offsets; the maximum score and its corresponding mass shift indicate the best match. Integrate this scoring function into a cascade search strategy: first perform an approximate nearest neighbor index lookup to reduce the candidate set to the most relevant spectra, then apply shifted dot product scoring to those candidates, and finally apply false discovery rate control to the scored matches. True modified–unmodified pairs should consistently receive higher scores than random decoy matches.

## Related tools

- **ANN-SoLo** (Spectral library search engine that integrates shifted dot product scoring with approximate nearest neighbor indexing and cascade search strategy for fast open modification searching) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Provides approximate nearest neighbor indexing backend to accelerate candidate spectrum selection before shifted dot product scoring) — https://github.com/facebookresearch/faiss

## Examples

```
pip install ann_solo; ann_solo --spectrum query.mgf --library library.msp --mode open_search --tolerance 0.1
```

## Evaluation signals

- True modified–unmodified spectrum pairs receive higher shifted dot product scores than decoy (random) matches across the tested mass offset range.
- Identified mass offsets match known PTM masses within the specified accuracy tolerance (e.g., ±0.02 Da for high-resolution instruments).
- False discovery rate control (e.g., using target–decoy strategy) achieves the specified FDR threshold (typically <1% or <5%).
- Sensitivity and precision on a validation set of manually curated modified–unmodified pairs meet or exceed baseline methods.
- Score distributions show clear separation between true matches and decoys across the mass offset dimension.

## Limitations

- Computational cost scales with the range of mass offsets scanned; large offset ranges or very large libraries may require approximate nearest neighbor acceleration to remain practical.
- Performance depends on spectral quality and library size; low-resolution spectra or incomplete libraries reduce the sensitivity of modification detection.
- The method assumes modifications manifest as predictable mass shifts; complex modifications or multiple simultaneous PTMs may require larger offset ranges or ensemble scoring.
- False discovery rate control relies on accurate target–decoy modeling; biased decoy generation or library composition can inflate false discovery rates.
- Python 3.6–3.9 required; GPU-accelerated versions require NVIDIA CUDA support on Linux; CPU-only versions available for Linux and macOS.

## Evidence

- [other] computes dot products across a range of mass offset values to detect post-translational modifications: "compute dot products across a range of mass offset values to detect post-translational modifications"
- [readme] cascade search strategy with FDR control and shifted dot product score: "a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score to sensitively"
- [other] normalize intensity vectors for similarity computation: "incorporating normalization for spectrum intensity vectors"
- [other] validate using known modified–unmodified pairs: "Validate the scoring function against known modified–unmodified spectrum pairs by verifying that true matches receive higher scores than random decoy matches"
- [readme] approximate nearest neighbor indexing selects relevant candidate spectra: "approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum"
