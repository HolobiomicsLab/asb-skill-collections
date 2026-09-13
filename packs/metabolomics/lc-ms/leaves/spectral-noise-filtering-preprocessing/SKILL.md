---
name: spectral-noise-filtering-preprocessing
description: Use when you have raw MS/MS spectral data and plan to calculate spectral
  similarity scores (whether using entropy distance, dot product, or other algorithms)
  for compound identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SpectralEntropy
  - spectral_similarity
  - MSEntropy
  - ms_distance module
  - spectral_similarity module
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# spectral-noise-filtering-preprocessing

## Summary

Remove low-intensity peaks from MS/MS spectra prior to similarity calculations to improve compound identification accuracy. This preprocessing step filters noise while preserving signal-bearing peaks by eliminating peaks below a relative intensity threshold.

## When to use

Apply this skill when you have raw MS/MS spectral data and plan to calculate spectral similarity scores (whether using entropy distance, dot product, or other algorithms) for compound identification. The presence of low-intensity noise peaks—particularly those arising from instrument artifacts or chemical background—degrades similarity metrics and ranking performance, making this preprocessing step essential before benchmarking or production identification workflows.

## When NOT to use

- Spectra that have already been noise-filtered by the instrument or vendor software; re-filtering may degrade signal.
- Analysis pipelines where peak intensity variance is itself the object of study (e.g., studying noise patterns or low-abundance metabolite detection); removing low peaks destroys that information.
- High-resolution or targeted analysis requiring detection of very low-abundance precursor or product ions; the 1% threshold may be too aggressive.

## Inputs

- raw MS/MS spectral data (m/z and intensity pairs)
- list or array of spectra with peak intensity values

## Outputs

- preprocessed MS/MS spectral data with noise peaks removed
- filtered peak lists (m/z and intensity pairs above 1% threshold)

## How to apply

Remove peaks with intensity less than 1% of the maximum intensity in each spectrum before calculating spectral similarity. This threshold balances noise suppression with signal retention: peaks below 1% maximum intensity contribute noise that degrades compound ranking without providing discriminative information, while peaks above this threshold carry identification signal. Apply this filter uniformly to all spectra in your dataset (both query and library spectra) to ensure consistent preprocessing. The README recommends this step explicitly: 'it's highly recommended to remove spectral noise. For example, peaks have intensity less than 1% maximum intensity can be removed to improve identification performance.' Verify the filtered spectrum retains the majority of peak count and total intensity to confirm the threshold is appropriate.

## Related tools

- **SpectralEntropy** (Source repository containing spectral preprocessing and similarity calculation modules; provides the spectral_similarity and ms_distance modules that operate on filtered spectra) — https://github.com/YuanyueLi/SpectralEntropy
- **MSEntropy** (Maintained Python package (ms_entropy on PyPI) integrating spectral entropy and preprocessing functionality; recommended for current use over the original SpectralEntropy repository) — https://github.com/YuanyueLi/MSEntropy
- **ms_distance module** (Submodule within SpectralEntropy/MSEntropy that calculates distance metrics on filtered spectral data) — https://github.com/YuanyueLi/SpectralEntropy
- **spectral_similarity module** (Submodule that computes similarity scores; operates on preprocessed spectra after noise filtering) — https://github.com/YuanyueLi/SpectralEntropy

## Evaluation signals

- Peak count reduction: Verify that the number of peaks decreases after filtering (typically 20–50% reduction depending on noise level in raw data).
- Intensity threshold validation: Confirm that all retained peaks have intensity ≥ 1% of the maximum intensity in each spectrum; all removed peaks have intensity < 1%.
- Similarity metric improvement: Compare spectral similarity scores or compound ranking accuracy before and after filtering; preprocessed spectra should yield higher dot product or entropy similarity scores and better rank-ordering of true matches.
- Spectrum integrity: Confirm that base peak (maximum intensity) and major product ion peaks are retained; no critical ions should fall below the 1% threshold.
- Reproducibility: Apply the same 1% threshold uniformly across all query and reference spectra to ensure fair comparison.

## Limitations

- The 1% intensity threshold is empirical and may require adjustment for different instrument types, ionization methods, or compound classes; spectra from very clean ion sources or highly abundant low-mass products may lose signal with this threshold.
- The paper does not report threshold sensitivity analysis or recommend adaptive thresholds; practitioners must validate the 1% cutoff against their specific data.
- This preprocessing step assumes peaks are independent; it does not account for isotope patterns or multiply-charged ion clusters that might span a wide intensity range.
- The filter is applied post-acquisition; instrumental or vendor-level noise filtering settings should be optimized first; this skill is a secondary confirmation step, not a replacement for instrument configuration.

## Evidence

- [other] Before calculating spectral similarity, it's highly recommended to remove spectral noise: "Before calculating spectral similarity, it's highly recommended to remove spectral noise"
- [other] peaks have intensity less than 1% maximum intensity can be removed to improve identificaiton performance: "peaks have intensity less than 1% maximum intensity can be removed to improve identificaiton performance"
- [readme] it's highly recommended to remove spectral noise. For example, peaks have intensity less than 1% maximum intensity can be removed: "it's highly recommended to remove spectral noise. For example, peaks have intensity less than 1% maximum intensity can be removed"
