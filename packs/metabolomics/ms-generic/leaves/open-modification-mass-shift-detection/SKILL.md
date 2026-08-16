---
name: open-modification-mass-shift-detection
description: Use when query mass spectra do not confidently match unmodified peptides in the spectral library, or when you suspect the sample contains unknown or unexpected post-translational modifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  - Faiss
  techniques:
  - mass-spectrometry
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# open-modification-mass-shift-detection

## Summary

Identifies peptide spectral matches with unexpected post-translational modifications by allowing variable mass shifts during library search, rather than enforcing exact mass matching. This skill enables discovery of both known and novel modifications while maintaining strict false discovery rate control.

## When to use

Apply this skill when query mass spectra do not confidently match unmodified peptides in the spectral library, or when you suspect the sample contains unknown or unexpected post-translational modifications. Use it as a secondary search stage after exhausting exact-match strategies, particularly when analyzing complex proteomes where modification diversity is high or modification types are not pre-specified.

## When NOT to use

- Input spectra are already confidently matched to unmodified peptides with high cosine similarity—use exact library search instead.
- Modifications are known and pre-defined with exact mass values—use targeted modification search with fixed mass lists.
- Sample contains only unmodified peptides and modification discovery is not relevant to the analysis goal.

## Inputs

- Query mass spectra (in mzML or similar format)
- Spectral library (reference peptide spectra)
- Approximate nearest neighbor index built on library spectra

## Outputs

- List of identified matches (unmodified and modified peptides)
- Matched spectra with assigned mass shifts
- FDR-controlled confidence scores (spectrum-level or peptide-level)
- Final identifications with FDR values

## How to apply

After retrieving candidate library spectra via approximate nearest neighbor indexing, perform a cascade search that first attempts exact unmodified peptide matching using cosine similarity scoring. For spectra without confident unmodified matches, apply open modification search on the same candidates, allowing variable mass shifts (no pre-defined modification list required). Score all matches using the shifted dot product, which sensitively accounts for mass shifts between query and library spectra. Rank identified matches (unmodified and modified) by score and apply false discovery rate control via spectrum-level or peptide-level FDR filtering to assign confidence thresholds and output final identifications with FDR values.

## Related tools

- **ANN-SoLo** (Spectral library search engine that combines approximate nearest neighbor indexing with cascade search strategy and shifted dot product scoring to perform open modification identification) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Dependency for building and querying approximate nearest neighbor indices on spectral library vectors) — https://github.com/facebookresearch/faiss

## Evaluation signals

- FDR values for output identifications are ≤ the specified threshold (e.g., 1% spectrum-level or peptide-level FDR) and are correctly computed from the ranked match list.
- Modified peptide identifications have mass shifts within a physically plausible range (typically ±500 Da for common PTMs) and are supported by shifted dot product scores above the confidence cutoff.
- Spectrum-level or peptide-level FDR filtering produces a non-empty set of high-confidence matches and correctly removes low-scoring spurious matches.
- Unmodified matches are preferred over modified matches when both have similar scores (cascade strategy prioritization), verified by inspecting the ranking of identified matches.
- Identified mass shifts correspond to known or chemically reasonable modifications (e.g., phosphorylation ~79.97 Da, acetylation ~42.01 Da, oxidation ~15.99 Da).

## Limitations

- Requires pre-built spectral library and approximate nearest neighbor index; not suitable for de novo sequencing without reference spectra.
- Computational cost scales with library size and query spectrum count; ANN indexing trades exact nearest neighbor retrieval for speed, potentially missing rare but correct matches.
- Python 3.6–3.9 support only; Python 3.10+ not currently supported (as of README documentation).
- GPU-powered version requires Linux with NVIDIA CUDA-enabled GPU; CPU-only version supports Linux and OSX.
- Open modification search allows arbitrary mass shifts, risking false positives if FDR filtering is misconfigured or if query spectra are very noisy; careful tuning of FDR cutoffs and spectral quality thresholds is essential.

## Evidence

- [intro] Cascade search strategy combined to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate"
- [intro] Shifted dot product score sensitively matches modified spectra to unmodified counterparts: "shifted dot product score to sensitively match modified spectra to their unmodified counterpart"
- [intro] ANN indexing selects limited relevant candidates for comparison, enabling fast open modification searching: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [readme] Python 3.6–3.9 required; GPU version Linux-only; CPU version supports Linux and OSX: "ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet). The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device,"
- [other] Cascade search applies open modification search to candidates without confident unmodified matches: "For spectra without confident unmodified matches, perform open modification search on the same candidates, allowing variable mass shifts"
