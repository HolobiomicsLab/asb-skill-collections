---
name: spectral-entropy-calculation
description: Use when when you have preprocessed MS/MS spectral peak data (m/z and
  intensity pairs) and need to compute a complexity metric for individual spectra
  prior to similarity comparisons, or when benchmarking compound identification performance
  against dot product–based methods.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SpectralEntropy
  - spectral_similarity
  - MSEntropy
  - spectral_similarity module
  - ms_distance module
  - math_distance module
  - MS Viewer web app
  - Entropy Search GUI
  - ms-entropy Python package
  techniques:
  - LC-MS
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-entropy-calculation

## Summary

Calculate spectral entropy from MS/MS spectra to quantify spectral complexity using Shannon entropy principles. This metric outperforms traditional dot product similarity for small-molecule compound identification and serves as the foundation for entropy-based spectral similarity scoring.

## When to use

When you have preprocessed MS/MS spectral peak data (m/z and intensity pairs) and need to compute a complexity metric for individual spectra prior to similarity comparisons, or when benchmarking compound identification performance against dot product–based methods.

## When NOT to use

- Input spectra have not been noise-filtered; entropy calculation will be skewed by low-intensity noise peaks.
- You need real-time search against very large spectral libraries and require only classical entropy similarity; use the Flash entropy search algorithm instead (available in MSEntropy package) for speed improvements.
- Your workflow requires only dot product similarity or cosine correlation; entropy similarity is a complementary method, not a replacement for all use cases.

## Inputs

- MS/MS spectral data (array of m/z and intensity pairs)
- Peak intensity threshold (typically 1% of maximum intensity for noise filtering)

## Outputs

- Spectral entropy value (scalar, typically 0–log(N) where N is number of peaks)
- Entropy distance or entropy similarity score (for pairwise comparisons)
- Benchmark performance metrics (accuracy, ranking scores vs. dot product method)

## How to apply

Load MS/MS spectral data as peak pairs (m/z, intensity). First, remove spectral noise by filtering peaks with intensity less than 1% of maximum intensity to improve identification performance. Normalize peak intensities to a probability distribution (sum to 1.0). Apply the Shannon entropy formula to the normalized intensity distribution to compute spectral entropy, which measures the complexity and information content of the spectrum. Higher entropy values indicate more complex, information-rich spectra; lower values indicate simple spectra dominated by few intense peaks. Use the spectral_similarity module's spectral entropy distance metrics (available in ms_distance and math_distance modules) to compute entropy-based similarity scores between query and reference spectra.

## Related tools

- **SpectralEntropy** (Core repository containing original source code for spectral entropy calculation and 43 spectral similarity algorithms) — https://github.com/YuanyueLi/SpectralEntropy
- **MSEntropy** (Recommended package integrating spectral entropy, entropy similarity, and Flash entropy search algorithm; supports Python, R, C/C++, and JavaScript) — https://github.com/YuanyueLi/MSEntropy
- **spectral_similarity module** (Module for calculating spectral similarity scores using both entropy and traditional distance metrics) — https://github.com/YuanyueLi/SpectralEntropy
- **ms_distance module** (Module containing MS-specific distance metrics including entropy distance for spectral comparison) — https://github.com/YuanyueLi/SpectralEntropy
- **math_distance module** (Module providing mathematical distance functions for entropy similarity computation) — https://github.com/YuanyueLi/SpectralEntropy
- **MS Viewer web app** (GUI for real-time visualization and calculation of entropy similarity for two MS/MS spectra) — https://yuanyueli.github.io/MSViewer
- **Entropy Search GUI** (Standalone GUI for searching one spectral file against a spectral library using entropy similarity; supports .mgf, .msp, .mzML, .lbm2 formats) — https://github.com/YuanyueLi/EntropySearch
- **ms-entropy Python package** (PyPI package for Python users to calculate spectral entropy and entropy similarity; includes Flash entropy search algorithm) — https://pypi.org/project/ms-entropy/

## Examples

```
import numpy as np
import ms_entropy as me
peaks_query = np.array([[69.071, 7.917962], [86.066, 1.021589]])
spectral_entropy = me.cal_spectral_entropy(peaks_query)
print(f'Spectral entropy: {spectral_entropy}')
```

## Evaluation signals

- Spectral entropy values are non-negative, typically in range 0 to log(N) where N is the number of peaks after noise filtering.
- Entropy similarity scores (distance metrics) range from 0 to 1 (or equivalent normalized scale); scores should NOT exceed 1.0, which indicates improper peak merging or normalization.
- Benchmark comparison shows spectral entropy-based identification achieves higher accuracy and better ranking performance than MS/MS dot product similarity on the reference compound identification dataset.
- Noise-filtered spectra (peaks below 1% max intensity removed) produce entropy values that correlate with spectral complexity; simple spectra yield lower entropy, complex spectra yield higher entropy.
- Entropy similarity scores for identical query and reference spectra equal 1.0 (perfect match); scores decrease monotonically as spectral differences increase.

## Limitations

- Spectral entropy calculation requires proper normalization of peak intensities to a probability distribution; errors in peak merging or normalization can produce entropy similarity scores exceeding 1.0.
- The 1% maximum intensity noise filter is recommended but may be tuned; threshold selection affects entropy values and downstream identification performance.
- Classical entropy similarity computation can be slow for searching a query spectrum against very large spectral libraries; use the Flash entropy search algorithm (MSEntropy package) for accelerated computation.
- Entropy-based methods assume peak intensity distributions are informative; spectra with few dominant peaks may not benefit from entropy metrics as much as complex spectra.

## Evidence

- [intro] Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification: "Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification"
- [readme] Spectral entropy is inspired by Shannon entropy and measures spectrum complexity: "Spectral entropy is an useful property to measure the complexity of a spectrum. It is inspried by the concept of Shannon entropy in information theory."
- [other] Noise filtering below 1% of maximum intensity is recommended before entropy calculation: "peaks have intensity less than 1% maximum intensity can be removed to improve identificaiton performance"
- [intro] Package includes spectral entropy and entropy similarity functions: "our package includes spectral entropy, entropy similarity, and many other functions"
- [readme] Entropy similarity has been rewritten using the Flash entropy search algorithm for speed improvements: "With the MSEntropy package, the method for calculating entropy similarity has been rewritten using the Flash entropy search algorithm. This has resulted in speed improvements without compromising"
- [readme] Peak merging errors can cause entropy similarity scores to exceed 1.0: "If you encounter an entropy similarity score higher than 1 in your self-implemented code, it could be due to errors in merging peaks within MS2-tolerance."
