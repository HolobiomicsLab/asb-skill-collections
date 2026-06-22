---
name: spectral-library-indexing
description: Use when you have large spectral libraries (thousands to millions of spectra) and need to search query spectra against them for peptide identification with tolerance for post-translational modifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  - Faiss
  - NumPy
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

# spectral-library-indexing

## Summary

Spectral library indexing accelerates open modification peptide identification by using approximate nearest neighbor (ANN) indexing to preselect only the most relevant library spectra for comparison to each query spectrum, reducing computational cost while maintaining sensitivity through cascade search and false discovery rate control.

## When to use

Apply this skill when you have large spectral libraries (thousands to millions of spectra) and need to search query spectra against them for peptide identification with tolerance for post-translational modifications. Use it specifically when search speed is a bottleneck and you cannot afford to compare every query against every library spectrum using exhaustive dot product scoring.

## When NOT to use

- Your spectral library is very small (< 1,000 spectra) — exhaustive search is faster and simpler.
- You require exhaustive comparison of every query to every library spectrum for absolute sensitivity — ANN indexing is approximate and may miss some true matches.
- Your spectra are already represented as pre-computed embeddings or feature vectors incompatible with mzML/mzXML formats.

## Inputs

- spectral library in mzML or mzXML format
- query spectra in mzML or mzXML format

## Outputs

- indexed spectral library (Faiss index)
- peptide-spectrum matches with false discovery rate filtered identifications
- scored candidate matches per query spectrum

## How to apply

Prepare query spectra and a spectral library in mzML or mzXML format. Use ANN-SoLo to index the library using approximate nearest neighbor indexing with Faiss, which embeds spectra into a high-dimensional vector space and partitions them for fast retrieval. For each query spectrum, the index retrieves only a limited number of candidate library spectra (the nearest neighbors) rather than all spectra. Score these candidates using shifted dot product to detect both unmodified and modified peptide matches. Apply a cascade search strategy—first searching unmodified matches, then modified matches—and enforce strict false discovery rate control (typically at 1% peptide or spectrum level) on the final results to filter identifications.

## Related tools

- **ANN-SoLo** (Core spectral library search engine that performs approximate nearest neighbor indexing, cascade search strategy, and false discovery rate-controlled peptide-spectrum matching for open modification searching) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Underlying similarity search library used by ANN-SoLo for approximate nearest neighbor indexing and retrieval) — https://github.com/facebookresearch/faiss
- **NumPy** (Required numerical computing dependency for ANN-SoLo installation)

## Examples

```
pip install ann_solo && ann_solo search --library spectral_library.mzML --spectra query_spectra.mzML --output results.txt
```

## Evaluation signals

- Verify that the number of library spectra retrieved per query is significantly smaller than the total library size (confirming dimensionality reduction through ANN).
- Check that the false discovery rate of peptide-spectrum identifications is at or below the target threshold (typically 1%) as reported in output statistics.
- Confirm that identified peptides include both unmodified and modified matches with appropriate shifted dot product scores.
- Validate reproducibility: re-indexing the same library and re-searching the same query set should yield identical or near-identical results.
- Compare runtime against exhaustive library search to confirm practical speedup (ANN-SoLo should reduce search time by orders of magnitude on large libraries).

## Limitations

- ANN indexing is approximate; some true matches may be missed if they fall outside the top-k nearest neighbors retrieved for a query.
- Python 3.6 to 3.9 only; Python 3.10 and newer are not yet supported according to the README.
- GPU-accelerated version requires Linux with NVIDIA CUDA-enabled GPU; CPU-only version supports Linux and OSX.
- Faiss installation is GPU-version-specific; incorrect GPU/CPU library mismatch will prevent operation.
- Cascade search strategy and FDR control parameters are fixed in the software; limited user configurability of sensitivity-specificity trade-off.

## Evidence

- [intro] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [intro] This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product"
- [other] Prepare spectral library and query spectra in mzML or mzXML format. Index the spectral library using ANN-SoLo's approximate nearest neighbor indexing with cascade search strategy. Execute ANN-SoLo search of query spectra against the indexed library, comparing each query to the selected candidate library spectra using shifted dot product scoring. Apply false discovery rate control to filter identifications and produce the final peptide-spectrum match output.: "Prepare spectral library and query spectra in mzML or mzXML format. Index the spectral library using ANN-SoLo's approximate nearest neighbor indexing with cascade search strategy. Execute ANN-SoLo"
- [readme] ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet). The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device, while the CPU-only version supports both the Linux and OSX platforms.: "ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet). The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device,"
- [readme] The recommended way to install ANN-SoLo is using pip: pip install ann_solo: "The recommended way to install ANN-SoLo is using pip: pip install ann_solo"
