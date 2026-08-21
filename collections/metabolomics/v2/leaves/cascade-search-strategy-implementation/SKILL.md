---
name: cascade-search-strategy-implementation
description: Use when when performing open modification spectral library searches
  on high-resolution mass spectra where computational cost is prohibitive if every
  query is scored against every library spectrum.
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

# cascade-search-strategy-implementation

## Summary

A multi-stage filtering strategy that combines approximate nearest neighbor indexing with progressive refinement to maximize identification of unmodified and modified peptide spectra while strictly controlling false discovery rate. This approach accelerates open modification spectral library searching by retrieving only top-k candidate spectra first, then applying computationally expensive precision scoring only to promising candidates.

## When to use

When performing open modification spectral library searches on high-resolution mass spectra where computational cost is prohibitive if every query is scored against every library spectrum. Use this when you need to balance sensitivity (identify both modified and unmodified spectra) against strict false discovery rate control, and when you have both a spectral library and query spectra in a standard format (mzML, mzXML, or similar).

## When NOT to use

- When closed-modification search is sufficient (i.e., only known modifications are of interest)—cascade strategy's strength is handling unexpected modifications, so simpler methods may suffice for closed searches.
- When the spectral library is very small (<10,000 spectra)—approximate nearest neighbor indexing and cascade filtering add overhead that is not justified for libraries small enough to score exhaustively.
- When query spectra are very low resolution or noisy—the feature hashing and ANN indexing rely on reproducible peak patterns; extremely noisy spectra may not hash consistently enough to benefit from cascade refinement.

## Inputs

- Query mass spectra (mzML or equivalent format)
- Spectral library (reference spectra in indexed format)
- Mass accuracy tolerance (ppm)
- Modification mass offsets (list of allowed post-translational modifications)
- False discovery rate threshold (e.g., 0.01)

## Outputs

- Ranked list of library spectrum matches per query spectrum
- Match scores (shifted dot product values)
- Identified peptide sequences with modification assignments
- False discovery rate-filtered results
- Query latency metrics (milliseconds per spectrum)

## How to apply

Implement a three-stage cascade: (1) Stage 1—retrieve top-k candidate spectra from an approximate nearest neighbor index (using feature hashing or locality-sensitive hashing) without full precision scoring; (2) Stage 2—compute shifted dot product scores with full precision only for these top-k candidates to detect modified peptides by accounting for mass offsets; (3) Stage 3—apply false discovery rate thresholding (e.g., target-decoy or statistical calibration) to the scored subset to report final identifications. The cascade balances speed (via Stage 1 filtering) against sensitivity (via Stage 2 precision scoring on candidates) and specificity (via Stage 3 FDR control). Key decision point: the choice of k (number of candidates) tunes the speed-sensitivity tradeoff—smaller k is faster but risks missing true identifications; larger k is slower but more sensitive. Measure success by sensitivity/specificity on known standard peptides and query latency (ms/spectrum) compared to exhaustive search baseline.

## Related tools

- **ANN-SoLo** (Spectral library search engine implementing cascade search with approximate nearest neighbor indexing and false discovery rate control for open modification searching) — https://github.com/bittremieux/ANN-SoLo
- **Faiss** (Underlying library providing approximate nearest neighbor indexing and GPU acceleration for Stage 1 candidate retrieval) — https://github.com/facebookresearch/faiss

## Examples

```
pip install ann_solo; # Then in Python: from ann_solo import search; results = search.open_modification_search(query_spectra='unknowns.mzML', library='library.mgf', modifications=['15.9949', '42.0106'], fdr_threshold=0.01, top_k=20)
```

## Evaluation signals

- Sensitivity and specificity on benchmark peptides (both unmodified and with known post-translational modifications) match or exceed exhaustive search baseline.
- False discovery rate of final identifications remains at or below the specified threshold (e.g., ≤ 0.01).
- Query latency (milliseconds per spectrum) shows measurable speedup relative to exhaustive dot product scoring of all library spectra.
- Shifted dot product scores for true-positive matches are significantly higher than false positives, indicating cascade refinement correctly prioritizes candidates.
- Top-k candidate recall (percentage of true library matches appearing in Stage 1 ANN results) remains ≥ 95% at chosen k value, ensuring true identifications are not filtered out prematurely.

## Limitations

- Cascade strategy effectiveness depends critically on the quality of the approximate nearest neighbor index; poor feature hashing or index parameters can cause true candidates to be filtered out in Stage 1.
- Open modification search requires enumerating possible mass offsets; if the true modification is not in the offset list, it cannot be identified even if it reaches Stage 2 scoring.
- GPU-accelerated version requires NVIDIA CUDA-enabled hardware and is currently limited to Linux systems (as of the 2019 publication); CPU-only version supports Linux and macOS but is significantly slower.
- Python version support is restricted (3.6 to 3.9 as of the README); newer Python versions require updating dependencies.
- Cascade approach trades some recall for speed; if Stage 1 ANN index retrieves fewer than k true candidates, overall sensitivity will be reduced compared to exhaustive scoring.

## Evidence

- [intro] cascade-search-strategy-definition: "This is combined with a cascade search strategy to maximize the number of identified unmodified and modified spectra while strictly controlling the false discovery rate and the shifted dot product"
- [other] cascade-ann-mechanism: "ANN-SoLo uses approximate nearest neighbor indexing to speed up open modification searching by selecting only a limited number of the most relevant library spectra to compare to an unknown query"
- [other] workflow-cascade-stages: "retrieve top-k candidate spectra from ANN index, compute shifted dot product scores with full precision, and filter by false discovery rate threshold"
- [other] feature-hashing-gpu-acceleration: "Compute feature hash representations of all spectra using a deterministic hashing function to map peaks into fixed-size feature vectors"
- [other] performance-metrics-evaluation: "Measure query latency (milliseconds per spectrum), throughput (spectra per second), and identification accuracy (sensitivity/specificity) for GPU implementation"
