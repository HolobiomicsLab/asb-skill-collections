---
name: unmatched-peak-detection-and-penalization
description: Use when when annotating MS/MS spectra against spectral libraries and chimeric spectra (spectra containing fragments from multiple precursor ions) are suspected or known to be present in your dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - cosine.py
  - entropy.py
  - bhattacharya1.py
  - reverse_search
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c02047
  title: Reverse Spectral Search
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_reverse_spectral_search_cq
    doi: 10.1021/acs.analchem.5c02047
    title: Reverse Spectral Search
  dedup_kept_from: coll_reverse_spectral_search_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c02047
  all_source_dois:
  - 10.1021/acs.analchem.5c02047
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# unmatched-peak-detection-and-penalization

## Summary

Identify peaks in a query MS/MS spectrum that lack corresponding matches in a library spectrum within a specified m/z tolerance, then apply a penalty factor to the base match score to suppress low-quality chimeric spectral matches while retaining true positive annotations.

## When to use

When annotating MS/MS spectra against spectral libraries and chimeric spectra (spectra containing fragments from multiple precursor ions) are suspected or known to be present in your dataset. Apply this skill when you observe that standard forward spectral matching produces false-positive identifications due to partial peak overlap, or when you need to increase the stringency of spectral matching while maintaining sensitivity.

## When NOT to use

- Input spectra are already known to be high-purity (non-chimeric), as the penalty factor may unnecessarily suppress true matches.
- Matching is intended for low-resolution or noisy spectra where unmatched peaks are expected as instrumental artifacts rather than genuine chimeric components.
- The application requires maximum sensitivity (e.g., biomarker discovery with no tolerance for false negatives) without corresponding specificity requirements.

## Inputs

- query MS/MS spectrum (m/z and intensity pairs)
- library MS/MS spectrum (m/z and intensity pairs)
- m/z tolerance threshold (ppm or Da)
- base match score (cosine similarity, entropy similarity, or Bhattacharyya angle)

## Outputs

- penalized match score (scalar value)
- list of unmatched peak indices and m/z values from query spectrum

## How to apply

After identifying matched peaks between query and library spectra using a specified m/z tolerance threshold (e.g., typical mass spectrometry tolerances), enumerate all peaks in the query spectrum that have no corresponding library peak within the tolerance window. For each unmatched peak, apply a penalty factor (a multiplicative or additive reduction) to the base match score (e.g., cosine similarity, entropy similarity, or Bhattacharyya angle). The penalty accumulates with the number of unmatched peaks, systematically reducing the final score for spectra with poor peak correspondence. This design balances increased spectral matches by reverse search against rigorous quality control: spectra with few unmatched peaks retain high scores, while chimeric spectra with many orphan peaks are downranked. The penalty factor should be tuned empirically on a validation set of known true/false annotations.

## Related tools

- **cosine.py** (calculates cosine similarity as base match score for symmetric and reverse spectral search) — https://github.com/Philipbear/reverse_search/blob/main/reverse_spectral_search/cosine.py
- **entropy.py** (calculates entropy similarity as base match score for symmetric and reverse spectral search) — https://github.com/Philipbear/reverse_search/blob/main/reverse_spectral_search/entropy.py
- **bhattacharya1.py** (calculates Bhattacharyya angle as base match score for symmetric and reverse spectral search) — https://github.com/Philipbear/reverse_search/blob/main/reverse_spectral_search/bhattacharya1.py
- **reverse_search** (implements reverse spectral search with penalty-factor enhancement for chimeric spectra detection and quality control) — https://github.com/Philipbear/reverse_search

## Evaluation signals

- Penalized scores for spectra with many unmatched peaks are lower than for spectra with few unmatched peaks, confirming penalty accumulation.
- The number and m/z values of unmatched peaks match the set difference between query peaks (within tolerance) and library peaks across the full m/z range.
- True-positive annotations (verified metabolite identifications) retain penalized scores above a chosen threshold, while false positives (especially chimeric spectra) are pushed below threshold in validation experiments.
- The distribution of penalized scores shifts toward lower values compared to unpenalized scores, with a larger shift for high-chimera datasets.
- Comparison of annotation recall and precision between penalized and unpenalized reverse search shows improved precision (fewer false positives) at minimal cost to recall (true positive rate).

## Limitations

- The choice of penalty factor magnitude and functional form (linear, exponential, etc.) requires empirical tuning and may not generalize across different MS platforms, ionization methods, or spectral libraries.
- The method assumes that unmatched peaks in the query are indicative of chimeric contamination; however, legitimate low-abundance fragments or instrument noise may also appear as unmatched peaks.
- Performance depends critically on the m/z tolerance threshold; if tolerance is too loose, genuine unmatched peaks are masked; if too tight, true matches are missed, leading to spurious penalties.
- The method does not distinguish between different types of unmatched peaks (e.g., chemically plausible fragments from co-eluting compounds vs. random noise); all are penalized equally.

## Evidence

- [other] Identify unmatched peaks in the query spectrum that have no corresponding library peak within tolerance. Apply a penalty factor to the base match score for each unmatched peak to reduce the final score.: "Identify unmatched peaks in the query spectrum that have no corresponding library peak within tolerance. Apply a penalty factor to the base match score for each unmatched peak to reduce the final"
- [readme] enhanced the reverse search by introducing a penalty factor to unmatched peaks, which increases the number of spectral matches while maintaining rigorous quality control: "enhanced the reverse search by introducing a penalty factor to unmatched peaks, which increases the number of spectral matches while maintaining rigorous quality control"
- [readme] Chimeric spectra are ubiquitous in MS/MS data, which compromises the quality and reliability of MS/MS matching-based metabolite annotation.: "Chimeric spectra are ubiquitous in MS/MS data, which compromises the quality and reliability of MS/MS matching-based metabolite annotation."
