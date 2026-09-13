---
name: entropy-based-spectral-distance-computation
description: Use when when comparing two preprocessed MS/MS spectra for compound identification
  and you need higher accuracy than dot product similarity provides.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_1812
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - spectral_similarity
  - MSEntropy
  - spectral_similarity module
  - Entropy Search GUI
  - MS Viewer web app
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41592-021-01331-z
  title: Spectral entropy
evidence_spans:
- '.. automodule:: spectral_similarity :members:'
- These are all integrated into the [MSEntropy package
- These are all integrated into the MSEntropy package (https://github.com/YuanyueLi/MSEntropy)
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

# entropy-based-spectral-distance-computation

## Summary

Compute similarity between two MS/MS spectra using entropy-based distance metrics rather than classical dot product similarity. This approach quantifies spectral complexity and comparison on information-theoretic principles, yielding improved accuracy for small-molecule compound identification.

## When to use

When comparing two preprocessed MS/MS spectra for compound identification and you need higher accuracy than dot product similarity provides. Particularly valuable when spectra have sparse, noisy, or unequal peak distributions, as entropy similarity is more robust to these characteristics than classical distance metrics.

## When NOT to use

- Input spectra have not been noise-filtered or contain very low-intensity artifacts; apply noise removal first.
- You need to compare more than two spectra simultaneously against a large library; use Flash entropy search algorithm instead for scalability.
- Input data is not MS/MS spectral data (e.g., chromatographic, proteomics, or already aggregated feature tables).

## Inputs

- Two preprocessed MS/MS spectra (noise-filtered: peaks <1% of max intensity removed)
- Spectral data as peak lists (m/z–intensity pairs)
- Spectrum identifiers and metadata

## Outputs

- Entropy similarity score (scalar, range [0, 1])
- Structured metadata table (spectrum IDs, peak counts, entropy values, similarity score)

## How to apply

First, preprocess both input spectra by removing noise—specifically, filter peaks with intensity less than 1% of maximum intensity. Load the two cleaned spectra (as peak m/z and intensity pairs) into the entropy_similarity function from the spectral_similarity module or MSEntropy package. The function computes a normalized entropy distance score between the spectra by comparing their entropy profiles. Validate that the returned similarity score lies within the expected range [0, 1], where 1 indicates identical spectra and 0 indicates orthogonal spectra. Record the score alongside spectrum identifiers, peak counts, and entropy values for downstream analysis or library matching.

## Related tools

- **MSEntropy** (Primary package integrating entropy similarity, spectral entropy, and Flash entropy search functions for MS/MS spectral comparison) — https://github.com/YuanyueLi/MSEntropy
- **spectral_similarity module** (Submodule within MSEntropy/SpectralEntropy that exports the entropy_similarity function and 42 other spectral distance algorithms) — https://github.com/YuanyueLi/SpectralEntropy
- **Entropy Search GUI** (Standalone graphical tool for real-time entropy similarity visualization and library searching; supports .mgf, .msp, .mzML, .lbm2 formats) — https://github.com/YuanyueLi/EntropySearch
- **MS Viewer web app** (Web-based interactive viewer for visualizing and computing entropy similarity between two spectra in real time) — https://yuanyueli.github.io/MSViewer

## Examples

```
import numpy as np
import ms_entropy as me

peaks_query = np.array([[69.071, 7.918], [86.066, 1.022]])
peaks_ref = np.array([[69.071, 10.0], [86.066, 2.5]])
similarity_score = me.spectral_entropy_similarity(peaks_query, peaks_ref)
print(f"Entropy similarity: {similarity_score}")
```

## Evaluation signals

- Returned similarity score is a scalar in range [0.0, 1.0]; scores >1.0 indicate a peak-merging error within MS2 tolerance.
- Similarity score matches reference output for known spectrum pairs (e.g., identical spectra should score ≈1.0; unrelated spectra should score ≈0.0).
- Output metadata table is complete and well-formed: contains spectrum IDs, peak counts, entropy values, and similarity score for audit trail.
- Spectral entropy values are positive and finite; extreme entropy values (very low or infinite) may indicate unexpected peak distributions or empty spectra.
- Input spectra confirm noise has been removed: no peaks with intensity <1% max intensity remain after filtering step.

## Limitations

- If entropy similarity scores exceed 1.0, this indicates an error in peak merging during MS2-tolerance alignment; use vetted implementation from MSEntropy repository to avoid this.
- Performance scales with spectrum complexity; for searching a single spectrum against large spectral libraries (>10k entries), use Flash entropy search algorithm instead, available only in Python currently.
- Entropy similarity assumes spectra have been preprocessed consistently (same normalization, fragmentation conditions); inconsistent preprocessing can inflate or deflate scores.
- Method is optimized for small-molecule MS/MS data; applicability to peptide, lipid, or other specialized fragmentation modes has not been extensively validated in the original paper.

## Evidence

- [other] How does the entropy similarity calculation operate to quantify the similarity between two MS/MS spectra: "research_question: How does the entropy similarity calculation operate to quantify the similarity between two MS/MS spectra in the spectral_similarity module?"
- [other] Noise filtering threshold and workflow: "Load two preprocessed MS/MS spectra (with noise removed: peaks <1% of maximum intensity filtered) from input files"
- [intro] Entropy similarity outperforms dot product for identification: "Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification"
- [intro] Entropy similarity is a core integrated function: "Package includes spectral entropy, entropy similarity, and many other functions"
- [other] Expected output range and validation: "Validate that the calculated entropy similarity value is within the expected range [0, 1] and matches reference output for known spectrum pairs"
- [readme] Peak-merging error indicator: "If you encounter an entropy similarity score higher than 1 in your self-implemented code, it could be due to errors in merging peaks within MS2-tolerance"
- [readme] Flash entropy search acceleration: "With the `MSEntropy` package, the method for calculating entropy similarity has been rewritten using the Flash entropy search algorithm. This has resulted in speed improvements without compromising"
- [readme] Multiple language support and tools: "The MSEntropy package supports multiple languages, including `Python`, `R`, `C/C++`, and `JavaScript`."
