---
name: entropy-similarity-scoring
description: Use when you need to quantify the degree of match between two MS/MS spectra—either to validate that a denoised spectrum remains faithful to a reference ground-truth spectrum, or to rank candidate library matches for a query spectrum.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - RDkit
  - ms_entropy
  - molmass
  - chemparse
  - pandas
  - scipy
  - spectral_denoising
  - numpy
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41592-025-02646-x
  title: Spectral Denoising
- doi: 10.1038/s41592-023-02012-9
  title: ''
evidence_spans:
- Spectral denoising requires ``Python >= 3.8`` installed on your system
- import spectral_denoising as sd
- rdkit==2024.3.5
- smiles = 'O=c1nc[nH]c2nc[nH]c12'
- ms_entropy==1.3.3
- '- ``ms_entropy==1.3.3``'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_flash_entropy_search_cq
    doi: 10.1038/s41592-023-02012-9
    title: Flash entropy search
  - build: coll_spectral_denoising_cq
    doi: 10.1038/s41592-025-02646-x
    title: Spectral Denoising
  dedup_kept_from: coll_spectral_denoising_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-025-02646-x
  all_source_dois:
  - 10.1038/s41592-025-02646-x
  - 10.1038/s41592-023-02012-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# entropy-similarity-scoring

## Summary

Compute entropy similarity between a query MS/MS spectrum and a reference spectrum to quantify spectral match quality and validate the effectiveness of denoising operations. This metric integrates both peak presence and intensity distribution, providing a normalized similarity score suitable for library searching and denoising validation.

## When to use

Apply this skill when you need to quantify the degree of match between two MS/MS spectra—either to validate that a denoised spectrum remains faithful to a reference ground-truth spectrum, or to rank candidate library matches for a query spectrum. Use entropy similarity in particular when you want a metric that accounts for both the presence of peaks and their relative intensities, rather than a simple presence/absence comparison.

## When NOT to use

- Input spectra contain only a single peak or very few peaks (entropy metric becomes unreliable with low spectral complexity).
- You need deterministic, threshold-based binary classification of a match (entropy similarity provides a continuous score; use with a cutoff threshold if binary output is required).
- Precursor m/z is unknown or unreliable, since entropy similarity calculation depends on correct mass calibration and ion detection.

## Inputs

- query_spectrum (numpy array: [m/z, intensity] columns, dtype float32)
- reference_spectrum (numpy array: [m/z, intensity] columns, dtype float32)
- precursor_mz (float: measured or theoretical m/z of the precursor ion)

## Outputs

- entropy_similarity_score (float: normalized similarity metric, typically 0.0–1.0 range)

## How to apply

Entropy similarity compares the spectral entropy profiles of a query spectrum against a reference spectrum using the formula and implementation provided by the ms_entropy package. Call the entropy_similairty function (note: function name has a typo in the source) with the query spectrum array (m/z and intensity columns), the reference spectrum array, and the precursor m/z value. The function computes normalized entropy for both spectra and returns a similarity score. To validate denoising, compute entropy_similarity for both the raw noisy spectrum against a reference and the denoised spectrum against the same reference; improvement in the latter score indicates successful noise removal while preserving chemically valid peaks. Typical application in library search loops through all candidate reference spectra and ranks by entropy similarity score.

## Related tools

- **ms_entropy** (Provides entropy_similairty function to compute normalized spectral similarity using entropy-based distance metrics) — https://pypi.org/project/ms-entropy/
- **spectral_denoising** (Python package that wraps entropy_similairty and uses it to validate denoising results and rank denoising_search candidates) — https://github.com/FanzhouKong/spectral_denoising
- **numpy** (Data structure and array operations for storing and manipulating spectrum arrays)

## Examples

```
entropy_similarity_score = entropy_similairty(peak_denoised, peak, pmz=pmz); print(f'denoised entropy similarity: {entropy_similarity_score:.2f}')
```

## Evaluation signals

- Entropy similarity score for denoised spectrum vs. reference should be ≥ score for noisy spectrum vs. reference (denoising validation).
- Entropy similarity scores should be in a bounded, normalized range (e.g., 0.0 to 1.0 or similar), consistent across library searches.
- Top-ranked candidate from denoising_search should have entropy similarity of denoised query spectrum that correlates with manual MS/MS interpretation (e.g., correct molecular structure identified).
- Entropy similarity metric should be symmetric or quasi-symmetric: score(query, ref) should be reasonably close to score(ref, query) after normalization.
- Repeated calls with identical input spectra and precursor m/z should yield identical scores (deterministic and reproducible).

## Limitations

- Entropy similarity is sensitive to precursor m/z accuracy; miscalibration or incorrect mass assignment can artificially inflate or deflate scores.
- The metric may not distinguish between spectra with similar overall entropy but very different fragmentation patterns (e.g., isomers with similar mass and intensity distributions).
- Low-intensity or noise-dominated spectra may yield uninformative entropy values; pre-filtering or normalization may be needed for robust comparisons.
- The function name in the codebase contains a typo (entropy_similairty instead of entropy_similarity), which may cause confusion or errors if not corrected.

## Evidence

- [other] Compute entropy_similarity between the input noisy spectrum and reference/ground-truth spectrum, and between the denoised spectrum and reference spectrum, and report both scores for comparison.: "Compute entropy_similarity between the input noisy spectrum and reference/ground-truth spectrum, and between the denoised spectrum and reference spectrum, and report both scores for comparison."
- [readme] The entropy similarity of contaminated spectrum and the raw spectrum is {entropy_similairty(peak_with_noise,peak, pmz = pmz):.2f}: "the entropy similarity of contaminated spectrum and the raw spectrum is {entropy_similairty(peak_with_noise,peak, pmz = pmz):.2f}"
- [readme] result will return all precursor candidates of the query spectrum, each with entropy similarities of both raw and denoised spectra: "result will return all precursor candidates of the query spectrum, each with entropy similarities of both raw and denoised spectra"
- [other] Validate the denoised spectrum by calculating entropy similarity against a reference spectrum using entropy_similairty, confirming the similarity improvement.: "Validate the denoised spectrum by calculating entropy similarity against a reference spectrum using entropy_similairty, confirming the similarity improvement."
