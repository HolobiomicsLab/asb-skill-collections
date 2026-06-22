---
name: spectral-similarity-scoring-with-mass-shifts
description: Use when you have an unknown query spectrum suspected to carry a post-translational modification and need to match it against a library of unmodified reference spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
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

# spectral-similarity-scoring-with-mass-shifts

## Summary

The shifted dot product score compares a query mass spectrum to library spectra by computing dot products across a range of mass offset values to detect post-translational modifications. This scoring mechanism sensitively matches modified spectra to their unmodified counterparts within a cascade search strategy combined with false discovery rate control.

## When to use

Use this skill when you have an unknown query spectrum suspected to carry a post-translational modification and need to match it against a library of unmodified reference spectra. Apply it as the sensitive scoring stage in an open modification search pipeline where the exact mass shift is unknown and must be discovered empirically across a range of offset values.

## When NOT to use

- Query spectrum is already annotated with a known modification mass — use exact-mass matching instead.
- Library spectra are heavily modified or contain a broad distribution of modification types; shifted dot product assumes comparison against predominantly unmodified counterparts.
- Computational budget is extremely constrained and approximate nearest neighbor pre-filtering is not available — the full shifted dot product search over all mass offsets and library spectra becomes prohibitively slow.

## Inputs

- Query mass spectrum (as intensity vector with m/z values)
- Spectral library (collection of unmodified reference spectra with normalized intensity vectors)
- Mass offset range (e.g., −500 to +500 Da, in discrete intervals)

## Outputs

- Shifted dot product scores (one score per query–library spectrum pair per mass offset)
- Ranked matches (library spectra ranked by highest shifted dot product score at optimal mass offset)
- Mass shift assignments (inferred post-translational modification mass for top-scoring matches)

## How to apply

Define a shifted dot product scoring algorithm that systematically varies the mass offset applied to the query spectrum, computing normalized dot products between the shifted query and each library spectrum across the full range of plausible modification masses. For each query–library pair, vectorize the pairwise similarity computation by normalizing both intensity vectors and computing dot products at discrete mass offset intervals. Score true matches higher than random decoys by verifying the algorithm ranks correct modified–unmodified pairs above decoy matches when evaluated against a validation set of known modified spectra. Integrate the shifted dot product scores into a cascade search strategy that first identifies candidates using approximate nearest neighbor indexing, then applies the shifted dot product to maximize sensitivity while maintaining strict false discovery rate control.

## Related tools

- **ANN-SoLo** (Spectral library search engine that integrates shifted dot product scoring within a cascade search strategy using approximate nearest neighbor indexing to speed up open modification searching) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Approximate nearest neighbor indexing library used by ANN-SoLo for fast candidate selection prior to shifted dot product scoring) — https://github.com/facebookresearch/faiss

## Evaluation signals

- True modified–unmodified spectrum pairs receive higher shifted dot product scores than random decoy matches at their correct mass offset.
- The inferred mass shift from the highest-scoring offset aligns with the known post-translational modification mass (within instrumental mass accuracy).
- False discovery rate of identifications remains below a specified threshold (e.g., 1%) when shifted dot product scores are integrated into the cascade search strategy.
- Vectorized computation of shifted dot products across all query–library–offset combinations completes within expected time constraints for the library size and offset range.
- Comparison of normalized intensity vectors yields numerical stability (no numerical overflow or underflow in dot product computation).

## Limitations

- Shifted dot product scoring assumes the query spectrum is a modified version of a spectrum in the unmodified library; performance degrades if true counterparts are absent or heavily modified.
- Mass offset range and interval granularity must be specified a priori; insufficient range or coarse intervals may miss small or unusual modifications, while excessive ranges increase computational cost.
- The method is sensitive to spectrum preprocessing (normalization, noise filtering); inconsistent preprocessing between query and library spectra can reduce match sensitivity.
- False discovery rate control via cascade search depends on the quality of approximate nearest neighbor candidate selection; poor indexing can lead to true positives being excluded before shifted dot product scoring occurs.

## Evidence

- [other] The shifted dot product score is used as a mechanism within a cascade search strategy to sensitively match modified spectra to their unmodified counterparts, operating in conjunction with false discovery rate control.: "shifted dot product score is used as a mechanism within a cascade search strategy to sensitively match modified spectra to their unmodified counterparts"
- [readme] ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query spectrum.: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [readme] Cascade search strategy combined with approximate nearest neighbor indexing to maximize identified unmodified and modified spectra while strictly controlling false discovery rate and the shifted dot product score to sensitively match modified spectra to their unmodified counterpart.: "cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product score to sensitively match"
- [other] Define the shifted dot product scoring algorithm that compares a query spectrum to library spectra by computing dot products across a range of mass offset values to detect post-translational modifications.: "Define the shifted dot product scoring algorithm that compares a query spectrum to library spectra by computing dot products across a range of mass offset values to detect post-translational"
- [other] Implement vectorized computation of pairwise similarities using the shifted dot product metric, incorporating normalization for spectrum intensity vectors.: "Implement vectorized computation of pairwise similarities using the shifted dot product metric, incorporating normalization for spectrum intensity vectors"
