---
name: open-modification-peptide-identification
description: Use when when you have high-resolution tandem mass spectra (query spectra) and need to identify peptides with unanticipated or open modifications (any mass shift on any amino acid position).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0601
  tools:
  - ANN-SoLo
  - Faiss
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
---

# open-modification-peptide-identification

## Summary

Identify peptides with unknown post-translational modifications in high-resolution mass spectra by combining approximate nearest neighbor indexing with cascade search strategy and false discovery rate control. This approach enables fast and accurate matching of query spectra to unmodified and modified peptides in spectral libraries without prior knowledge of modification type or location.

## When to use

When you have high-resolution tandem mass spectra (query spectra) and need to identify peptides with unanticipated or open modifications (any mass shift on any amino acid position). Specifically, use this skill when: (1) modifications are unknown a priori, (2) you must search against a large spectral library, (3) computational speed is critical (avoiding exhaustive comparison of all library spectra), and (4) strict false discovery rate control is required for publication or downstream analysis.

## When NOT to use

- When modifications are known a priori and limited to a predefined set — use targeted modification search instead
- When computational resources are abundant and exhaustive spectral library comparison is feasible — gains are marginal if all spectra can be scored in acceptable time
- When query spectra are low-resolution (ion trap or Orbitrap at low resolving power) — feature hashing and approximate nearest neighbor indexing are optimized for high-resolution data

## Inputs

- high-resolution tandem mass spectra (query spectra) in standard formats (mzML, mzXML, or mgf)
- peptide spectral library in high-resolution format

## Outputs

- ranked list of candidate peptide matches per query spectrum
- identification scores (dot product or shifted dot product values) for each match
- peptide sequence assignments with modification annotations
- false discovery rate estimates for unmodified and modified identifications

## How to apply

Load query mass spectra and a spectral library in high-resolution format, then execute a cascade search strategy: first match unmodified peptides using approximate nearest neighbor indexing to rapidly select only the most relevant library spectra (rather than exhaustively comparing all spectra), then perform open modification searches on the candidates using shifted dot product scoring to sensitively match spectra with mass shifts. Apply strict false discovery rate control across both unmodified and modified identification stages. The approximate nearest neighbor indexing dramatically reduces computational burden by pre-filtering the library to a limited subset of candidates before expensive similarity calculations. Shifted dot product scoring enables detection of modified peptides by tolerating systematic mass offsets between query and library spectra.

## Related tools

- **ANN-SoLo** (Spectral library search engine implementing approximate nearest neighbor indexing, cascade search strategy, and shifted dot product scoring for open modification peptide identification) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Approximate nearest neighbor indexing library underlying ANN-SoLo's rapid candidate retrieval, supports GPU acceleration) — https://github.com/facebookresearch/faiss

## Examples

```
pip install ann_solo
```

## Evaluation signals

- Verify false discovery rate control: check that reported q-values for unmodified identifications are ≤ specified threshold (typically 0.01 or 0.05) and modified identifications meet the same strict threshold
- Confirm cascade search ordering: validate that unmodified peptide matches are computed before open modification searches, and that modification assignments only occur when unmodified candidates fall below confidence threshold
- Validate approximate nearest neighbor candidate set quality: spot-check that the correct peptide (or a high-similarity correct peptide) appears in the ANN-retrieved candidate subset for true positive matches
- Compare shifted dot product scores: confirm that matches with systematic mass offsets (modified peptides) show lower standard dot product but higher shifted dot product scores than unmodified matches
- Benchmark speed gains: verify that search time scales sublinearly with library size (ANN-SoLo should enable searching large libraries in minutes vs. hours for exhaustive approaches)

## Limitations

- Requires Python 3.6–3.9; Python 3.10+ not yet supported as of the README
- GPU-powered version limited to Linux systems with NVIDIA CUDA-enabled devices; CPU-only version supports Linux and OSX but is substantially slower
- Approximate nearest neighbor indexing inherently introduces a small risk of missing the true best match if it falls outside the ANN candidate set; parameters controlling candidate set size must be tuned per application
- Shifted dot product scoring assumes modifications produce a single consistent mass shift; does not model complex, multi-site modifications or mass-labile modifications that may fragment differently than predicted

## Evidence

- [readme] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [readme] Cascade search strategy combined with shifted dot product scoring for modified peptides: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product"
- [other] Workflow steps: feature hashing, GPU acceleration, and cascade search: "Convert spectra to feature hash vectors using a fixed-size hash table representation to reduce dimensionality while preserving similarity structure. Index the hashed library spectra using approximate"
- [readme] GPU-powered version platform requirements: "The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device, while the CPU-only version supports both the Linux and OSX platforms."
- [readme] Python version constraints: "ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet)."
