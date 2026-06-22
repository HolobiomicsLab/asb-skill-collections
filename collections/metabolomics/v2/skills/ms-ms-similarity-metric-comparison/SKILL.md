---
name: ms-ms-similarity-metric-comparison
description: Use when when you have MS/MS spectra from both query compounds and a reference library and need to decide which similarity metric will maximize identification accuracy (true positive rank, precision@k) or when benchmarking a new compound identification workflow against a known-good reference.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3945
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SpectralEntropy
  - spectral_similarity
  - MSEntropy
  - spectral_similarity module
  - math_distance module
  - ms_distance module
  - Entropy Search GUI
  - MS Viewer web app
derived_from:
- doi: 10.1038/s41592-021-01331-z
  title: Spectral entropy
evidence_spans:
- This repository contains the original source code for the paper
- '.. automodule:: spectral_similarity :members:'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectral_entropy_cq
    doi: 10.1038/s41592-021-01331-z
    title: Spectral entropy
  dedup_kept_from: coll_spectral_entropy_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-021-01331-z
  all_source_dois:
  - 10.1038/s41592-021-01331-z
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms-ms-similarity-metric-comparison

## Summary

Compare MS/MS spectral similarity scores computed via multiple distance metrics (entropy-based and classical) to identify which metric best ranks reference compounds for a given identification task. This skill enables evidence-based selection of the appropriate similarity algorithm—e.g., entropy similarity vs. dot product—for your spectral library search or compound validation workflow.

## When to use

When you have MS/MS spectra from both query compounds and a reference library and need to decide which similarity metric will maximize identification accuracy (true positive rank, precision@k) or when benchmarking a new compound identification workflow against a known-good reference dataset.

## When NOT to use

- When spectral data is already heavily pre-filtered or normalized by external tools (similarity matrix or feature tables are pre-computed and not reproducible from raw peak lists).
- When only a single similarity metric is required and the metric choice is already validated for your specific sample type or mass spectrometer.
- When computational cost is prohibitive: computing 43+ similarity metrics on very large libraries (>1 million spectra) may require sampling or approximation strategies not covered by this skill.

## Inputs

- MS/MS spectral peaks (m/z and intensity pairs) for query spectra
- MS/MS spectral peaks for reference library spectra
- Reference annotations linking query spectra to ground-truth library compounds

## Outputs

- Similarity score matrix (query × reference, per metric)
- Ranked candidate lists per query spectrum (sorted by similarity, per metric)
- Comparison metrics table (accuracy, precision, recall, rank position statistics per metric)
- Performance summary quantifying the advantage of entropy similarity over dot product similarity

## How to apply

First, prepare input MS/MS spectral data by removing spectral noise—specifically, filter peaks with intensity less than 1% of maximum intensity to improve identification performance. Next, compute spectral similarity scores between query and reference spectra using at least two contrasting metrics: (1) entropy similarity (the primary metric) and (2) MS/MS dot product similarity (or another classical metric such as cosine, Euclidean, or Manhattan distance). Apply these calculations via the math_distance, ms_distance, or spectral_similarity modules. Then, for each query spectrum, rank the reference library by descending similarity score and measure the ranking performance: record the rank position of the true reference compound, compute recall (fraction of true matches ranked in top-k), and tabulate accuracy metrics. Finally, compare the metrics side-by-side using the same test set; entropy similarity should show higher ranking accuracy and lower false discovery rate than dot product similarity for small-molecule compound identification.

## Related tools

- **SpectralEntropy** (Primary package for computing spectral entropy, entropy similarity, and 43+ alternative distance metrics for MS/MS spectral comparison) — https://github.com/YuanyueLi/SpectralEntropy
- **MSEntropy** (Current recommended package integrating spectral entropy functions and the Flash entropy search algorithm; supports Python, R, C/C++, JavaScript) — https://github.com/YuanyueLi/MSEntropy
- **spectral_similarity module** (Module within SpectralEntropy/MSEntropy for computing pairwise spectral similarities across multiple metrics) — https://github.com/YuanyueLi/SpectralEntropy
- **math_distance module** (Module providing distance metric implementations (Euclidean, Manhattan, Chebyshev, etc.) used in spectral comparison) — https://github.com/YuanyueLi/SpectralEntropy
- **ms_distance module** (Module containing MS/MS-specific distance calculations including entropy similarity and dot product similarity) — https://github.com/YuanyueLi/SpectralEntropy
- **Entropy Search GUI** (Standalone graphical tool for querying spectral files against spectral libraries using entropy similarity; supports .mgf, .msp, .mzML, .lbm2 formats) — https://github.com/YuanyueLi/EntropySearch
- **MS Viewer web app** (Web-based real-time visualization and entropy similarity calculation for two MS/MS spectra) — https://yuanyueli.github.io/MSViewer

## Examples

```
import numpy as np; import ms_entropy as me; peaks_query = np.array([[69.071, 7.918], [86.066, 1.022]]); peaks_ref = np.array([[69.071, 5.0], [86.066, 3.0]]); entropy_sim = me.entropy_similarity(peaks_query, peaks_ref); dot_product_sim = me.dot_product_similarity(peaks_query, peaks_ref); print(f'Entropy: {entropy_sim}, Dot product: {dot_product_sim}')
```

## Evaluation signals

- True reference compound is ranked at a higher position (lower rank index) by entropy similarity than by dot product similarity, across ≥80% of query spectra in the test set.
- Entropy similarity achieves higher recall@k (e.g., recall@10, recall@100) than dot product similarity when evaluating prediction accuracy against the reference compound identification dataset.
- Entropy similarity scores lie in the valid range [0, 1] with no anomalous values >1, indicating correct peak merging and normalization within MS2-tolerance windows.
- Spectral noise removal (filtering peaks <1% max intensity) produces a measurable improvement in ranking metrics for at least one metric, confirming correct preprocessing.
- Similarity score distributions (entropy vs. dot product) are visibly distinct and entropy shows lower overlap between true-match and false-match score distributions, indicating better separability.

## Limitations

- Entropy similarity computation requires correct implementation of peak merging within MS2-tolerance; self-implemented code risks producing scores >1 due to merging errors—use the provided SpectralEntropy/MSEntropy repository code to avoid this.
- Comparison results are specific to small-molecule compounds and MS/MS spectra; applicability to other analyte classes (peptides, glycans) or ionization methods not directly established by this benchmark.
- The Flash entropy search algorithm (in MSEntropy) significantly accelerates entropy similarity computation but is currently available only in Python; R, C/C++, and JavaScript users must use the classical (slower) entropy similarity implementation.
- Benchmark conclusions assume a representative reference spectral library; biased or incomplete library coverage may alter the relative ranking performance of similarity metrics.

## Evidence

- [intro] Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification: "Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification"
- [other] Noise removal via intensity threshold improves identification: "peaks have intensity less than 1% maximum intensity can be removed to improve identificaiton performance"
- [other] Multiple tools/modules used for similarity calculation: "These are all integrated into the MSEntropy package (https://github.com/YuanyueLi/MSEntropy)"
- [other] 43 spectral similarity algorithms available for comparison: "The code in this repository provides 43 different spectral similarity algorithms for MS/MS spectral comparison."
- [readme] Risk of entropy similarity >1 from implementation errors: "If you encounter an entropy similarity score higher than 1 in your self-implemented code, it could be due to errors in merging peaks within MS2-tolerance. Use the code provided in our repository to"
- [readme] Flash entropy search improves speed without losing accuracy: "With the `MSEntropy` package, the method for calculating entropy similarity has been rewritten using the Flash entropy search algorithm. This has resulted in speed improvements without compromising"
