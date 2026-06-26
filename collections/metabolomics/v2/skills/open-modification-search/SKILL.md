---
name: open-modification-search
description: Use when your query spectra contain peptides with unknown modifications
  (e.g., oxidation, phosphorylation, acetylation, or non-enzymatic modifications not
  specified in the search parameters), and you have a reference spectral library in
  mzML or mzXML format.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3646
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ANN-SoLo
  - Faiss
  - NumPy
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.8b00359
  title: ANN-SoLo
evidence_spans:
- ANN-SoLo (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary) is
  a spectral library search engine
- '**ANN-SoLo** (**A**pproximate **N**earest **N**eighbor **S**pectral **L**ibrary)
  is a spectral library search engine'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# open-modification-search

## Summary

Search mass spectrometry spectral libraries for peptide identifications when peptides carry unknown or unexpected post-translational modifications. This skill uses approximate nearest neighbor indexing combined with cascade search to rapidly screen candidate library spectra and sensitively match both unmodified and modified peptides while controlling false discovery rate.

## When to use

Your query spectra contain peptides with unknown modifications (e.g., oxidation, phosphorylation, acetylation, or non-enzymatic modifications not specified in the search parameters), and you have a reference spectral library in mzML or mzXML format. You need both speed and sensitivity: rapid candidate selection without exhaustive comparison to every library spectrum, while preserving the ability to identify modified forms alongside unmodified matches.

## When NOT to use

- Your spectral library is not in mzML or mzXML format; conversion is required first.
- You have a complete, validated list of expected modifications and can use closed-modification search instead; open modification searching trades some speed for the benefit of discovering unanticipated modifications.
- Your query spectra are of very low quality or from non-standard instruments where approximate nearest neighbor indexing may fail to retrieve relevant candidates due to poor spectral similarity structure.

## Inputs

- spectral library in mzML format
- spectral library in mzXML format
- query mass spectra in mzML format
- query mass spectra in mzXML format

## Outputs

- peptide-spectrum match (PSM) identifications with FDR-filtered scores
- matched peptide sequences (unmodified and modified forms)
- shifted dot product scores per match
- false discovery rate estimates per PSM

## How to apply

Index your spectral library using approximate nearest neighbor indexing to pre-select only the most relevant candidate spectra for each query, rather than comparing against all library entries—this step dramatically reduces computational cost. Apply a cascade search strategy that first attempts unmodified peptide matching, then progressively searches for modified forms, at each stage computing shifted dot product scores to sensitively align spectra with mass shifts. Finally, apply false discovery rate (FDR) control via statistical filtering to separate true identifications from false positives, using the cascade scores and peptide-spectrum match statistics. The combination of ANN indexing (speed) + cascade search (sensitivity to modifications) + FDR correction (specificity) ensures you recover both standard and modified peptide assignments while maintaining statistical rigor.

## Related tools

- **ANN-SoLo** (spectral library search engine that implements approximate nearest neighbor indexing with cascade search strategy and shifted dot product scoring for open modification identification) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (provides approximate nearest neighbor indexing backend; required dependency for ANN-SoLo GPU and CPU versions) — https://github.com/facebookresearch/faiss
- **NumPy** (numerical library; must be installed prior to ANN-SoLo installation)

## Examples

```
pip install ann_solo
```

## Evaluation signals

- FDR-filtered peptide-spectrum matches are reported with explicit q-values or adjusted p-values showing that false positives are controlled at the specified threshold (typically ≤ 0.05 or ≤ 0.01).
- Identifications include both unmodified peptides and peptides with mass shifts corresponding to known PTM masses or fragments thereof (evidence of cascade search effectiveness).
- Shifted dot product scores for modified PSMs are lower than for unmodified matches but still meet significance threshold, indicating sensitive detection of mass-shifted peptides.
- The number of identifications increases compared to closed-modification search on the same query set, validating that open search discovers modifications missed by closed approaches.
- Query-library spectrum pairs retrieved by approximate nearest neighbor indexing show high baseline spectral similarity (cosine or dot product) before cascade scoring, confirming that indexing selected genuinely relevant candidates rather than random spectra.

## Limitations

- Approximate nearest neighbor indexing requires sufficient spectral similarity structure; highly noisy or atypical spectra may not retrieve relevant candidates, resulting in missed identifications.
- The cascade search strategy and shifted dot product scoring assume peptides differ by intact mass shifts; complex modifications affecting fragmentation patterns beyond mass alone may reduce sensitivity.
- Python 3.6–3.9 required; Python 3.10 and newer are not currently supported, limiting deployment on newer systems without version management.
- GPU-powered version requires Linux with NVIDIA CUDA-enabled GPU; CPU-only version supports Linux and macOS but may be slower on very large spectral libraries.

## Evidence

- [intro] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [intro] cascade search strategy combined with approximate nearest neighbor indexing maximizes identified unmodified and modified spectra while strictly controlling false discovery rate: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate"
- [readme] shifted dot product score used to sensitively match modified spectra to their unmodified counterpart: "shifted dot product score to sensitively match modified spectra to their unmodified counterpart"
- [readme] ANN-SoLo requires Python 3.6 to 3.9; Python 3.10 and newer are not currently supported: "ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet)"
- [readme] GPU version available on Linux with NVIDIA CUDA-enabled GPU; CPU-only version supports Linux and OSX: "The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device, while the CPU-only version supports both the Linux and OSX platforms"
