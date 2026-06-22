---
name: peptide-spectrum-matching
description: Use when when you have high-resolution tandem mass spectrometry data (in mzML or mzXML format) and a spectral library, and need to identify peptides including those with post-translational modifications.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
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

# peptide-spectrum-matching

## Summary

Identify peptides from mass spectrometry data by matching query spectra against a spectral library using approximate nearest neighbor indexing and cascade search with shifted dot product scoring. This skill enables fast, accurate open modification searching while controlling false discovery rate.

## When to use

When you have high-resolution tandem mass spectrometry data (in mzML or mzXML format) and a spectral library, and need to identify peptides including those with post-translational modifications. Use this skill when speed and sensitivity for modified peptides are both required and false discovery rate control is essential.

## When NOT to use

- Input spectra are in a non-standard format incompatible with mzML/mzXML conversion
- The spectral library is empty or does not cover the peptides of interest
- You require identification without any false discovery rate filtering or quality control

## Inputs

- Query spectra (mzML or mzXML format)
- Spectral library (mzML or mzXML format)
- Mass tolerance parameters
- False discovery rate threshold

## Outputs

- Peptide-spectrum matches with quality scores
- FDR-filtered identifications
- Shifted dot product scores
- Post-translational modification assignments

## How to apply

Prepare query spectra and a reference spectral library in mzML or mzXML format. Index the library using approximate nearest neighbor indexing to pre-select a limited set of the most relevant candidate spectra for each query. For each query spectrum, apply the cascade search strategy: first attempt unmodified matching, then extend to modified spectra using shifted dot product scoring across a range of mass offset values to detect post-translational modifications. Score each query against selected candidates using the shifted dot product metric with intensity normalization. Apply strict false discovery rate control to filter identifications and produce final peptide-spectrum match output. The cascade strategy maximizes both unmodified and modified peptide identifications while maintaining controlled error rates.

## Related tools

- **ANN-SoLo** (Spectral library search engine that implements approximate nearest neighbor indexing, cascade search strategy, shifted dot product scoring, and FDR control for open modification peptide identification) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Approximate nearest neighbor indexing library used by ANN-SoLo to pre-select relevant candidate spectra) — https://github.com/facebookresearch/faiss
- **NumPy** (Required numerical library for vectorized computation of pairwise similarities using shifted dot product metric)

## Examples

```
pip install ann_solo
```

## Evaluation signals

- Query spectra correctly matched to library spectra with known ground truth peptides; true matches receive higher shifted dot product scores than random decoys
- FDR-filtered output maintains error rate below specified threshold; verify by inspecting rank distribution and target/decoy score separation
- Cascade search identifies both unmodified peptides and peptides with known post-translational modifications at expected mass offsets
- Output includes shifted dot product scores and mass offset assignments; validate against independently verified modified–unmodified spectrum pairs
- Computational runtime scales sub-linearly with library size due to approximate nearest neighbor pre-filtering

## Limitations

- ANN-SoLo requires Python 3.6 to 3.9; Python 3.10 and newer are not yet supported
- GPU-powered version requires Linux with NVIDIA CUDA-enabled GPU; CPU-only version supports Linux and OSX
- Shifted dot product scoring sensitivity depends on appropriate mass tolerance and normalization of spectrum intensity vectors
- False discovery rate control assumes a sufficient pool of unmodified decoys; sparse libraries may inflate actual error rates
- Open modification search space grows with mass offset range; extremely wide tolerance windows may reduce specificity

## Evidence

- [readme] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [readme] This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score to sensitively match modified spectra to their unmodified counterpart: "cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score to sensitively match"
- [other] The shifted dot product score is used as a mechanism within a cascade search strategy to sensitively match modified spectra to their unmodified counterparts, operating in conjunction with false discovery rate control: "shifted dot product score is used as a mechanism within a cascade search strategy to sensitively match modified spectra to their unmodified counterparts"
- [other] Implement vectorized computation of pairwise similarities using the shifted dot product metric, incorporating normalization for spectrum intensity vectors: "Implement vectorized computation of pairwise similarities using the shifted dot product metric, incorporating normalization for spectrum intensity vectors"
- [readme] ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet). The GPU-powered version of ANN-SoLo can be used on Linux systems with an NVIDIA CUDA-enabled GPU device, while the CPU-only version supports both the Linux and OSX platforms: "ANN-SoLo requires Python 3.6 to 3.9 (Python 3.10 and newer are currently not supported yet). The GPU-powered version can be used on Linux systems with an NVIDIA CUDA-enabled GPU device, while the"
