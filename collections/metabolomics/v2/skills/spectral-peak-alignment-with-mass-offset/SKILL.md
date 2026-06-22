---
name: spectral-peak-alignment-with-mass-offset
description: Use when when comparing two MS/MS spectra where the precursor m/z values differ (indicating potential mass modifications, adducts, or related compounds), and you want to detect structurally conserved fragmentation patterns that would be missed by direct m/z matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3646
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - cosine_neutral_loss
  - spectrum_utils
derived_from:
- doi: 10.1021/jasms.2c00153
  title: Neutral-loss similarity
- doi: 10.1016/1044-0305
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_neutral_loss_similarity_cq
    doi: 10.1021/jasms.2c00153
    title: Neutral-loss similarity
  dedup_kept_from: coll_neutral_loss_similarity_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.2c00153
  all_source_dois:
  - 10.1021/jasms.2c00153
  - 10.1016/1044-0305
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Spectral Peak Alignment with Mass Offset

## Summary

Align peaks between two MS/MS spectra by accounting for their precursor mass difference, enabling detection of structurally related molecules that may have undergone mass shifts or modifications. This is the core computational step in modified cosine similarity scoring.

## When to use

When comparing two MS/MS spectra where the precursor m/z values differ (indicating potential mass modifications, adducts, or related compounds), and you want to detect structurally conserved fragmentation patterns that would be missed by direct m/z matching. Use this when the research goal is to discover structurally related molecules rather than exact matches.

## When NOT to use

- When comparing spectra from the same compound or with identical precursor masses—use standard (unmodified) cosine similarity instead.
- When the precursor mass difference is due to instrument calibration error rather than true chemical modification—normalize/recalibrate spectra first.
- When the mass offset exceeds the expected range for your experiment (e.g., >500 Da in small-molecule metabolomics)—this may indicate unrelated compounds.

## Inputs

- MS/MS spectrum 1 (query): m/z values, intensity values, precursor m/z
- MS/MS spectrum 2 (reference): m/z values, intensity values, precursor m/z

## Outputs

- Aligned peak pairs: list of (m/z_query, intensity_query, m/z_reference, intensity_reference) tuples
- Precursor mass difference: float (Da or m/z units)
- Similarity score: float between 0 and 1 (when passed to cosine computation)

## How to apply

Extract the precursor m/z values from both the query and reference spectra and calculate their mass difference. Match peaks between spectra such that a peak at m/z_query aligns with a peak at m/z_reference + mass_difference, rather than requiring identical m/z values. This offset-aware matching preserves alignment even when both spectra have undergone the same mass shift. Compute intensity-weighted similarity (e.g., cosine similarity) on the aligned peak pairs. The key rationale is that structural analogs often retain their fragmentation patterns despite precursor mass shifts, so accounting for the offset reveals these hidden similarities.

## Related tools

- **cosine_neutral_loss** (Reference implementation of modified cosine similarity and peak alignment with mass offset) — https://github.com/bittremieux/cosine_neutral_loss
- **spectrum_utils** (Utility library for loading and manipulating MS/MS spectra objects (MsmsSpectrum), extracting precursor m/z, and removing noise peaks)

## Examples

```
import spectrum_utils.spectrum as sus; spectrum1 = sus.MsmsSpectrum.from_usi('mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00000424840'); spectrum2 = sus.MsmsSpectrum.from_usi('mzspec:MSV000086109:BD5_dil2x_BD5_01_57213:scan:760'); mass_diff = spectrum1.precursor_mz - spectrum2.precursor_mz; aligned_peaks = [(mz1, int1, mz2, int2) for mz1, int1 in zip(spectrum1.mz, spectrum1.intensities) for mz2, int2 in zip(spectrum2.mz, spectrum2.intensities) if abs(mz1 - (mz2 + mass_diff)) < 0.1]
```

## Evaluation signals

- Verify that the precursor mass difference is computed correctly: abs((spectrum1.precursor_mz - spectrum2.precursor_mz) * spectrum1.precursor_charge - mass_difference) ≈ 0.
- Confirm that aligned peak pairs satisfy the offset condition: for each pair, |m/z_query - (m/z_reference + mass_difference)| ≤ tolerance (typically 0.1 Da or 10 ppm).
- Check that similarity scores are symmetric or near-symmetric when comparing the same pair in both directions (modified_cosine(A, B) ≈ modified_cosine(B, A)).
- Validate that related compounds (known analogs with expected mass shifts) produce higher similarity scores than unrelated compounds with the same precursor mass difference.
- Ensure that the aligned peak intensity values are used correctly in downstream similarity computation (cosine or other metric), with no duplicate or missing peaks.

## Limitations

- The method assumes that the mass offset is uniform across all peaks; if different fragment ions have undergone different mass shifts, alignment will be incorrect.
- Sensitivity to precursor m/z measurement error: small calibration errors can compound across many spectrum pairs, leading to systematic misalignment.
- The alignment threshold (tolerance) must be chosen carefully; too loose a threshold admits spurious matches, too strict excludes legitimate ones.
- Performance depends on peak-picking quality upstream; noisy or poorly resolved spectra reduce the reliability of matched peaks.
- Not applicable to comparing spectra with very different fragmentation patterns, even if precursor mass shift is accounted for; alignment alone does not guarantee similarity.

## Evidence

- [other] Calculate the precursor mass difference between the two spectra. 4. Match peaks between spectra allowing for the precursor mass offset (modified cosine: peaks at m/z_query and m/z_reference + mass_difference are considered aligned).: "Calculate the precursor mass difference between the two spectra. 4. Match peaks between spectra allowing for the precursor mass offset (modified cosine: peaks at m/z_query and m/z_reference +"
- [other] Modified cosine similarity is a spectrum similarity measure implemented in the repository alongside cosine similarity and neutral loss similarity for comparing MS/MS spectra in the discovery of structurally related molecules.: "Modified cosine similarity is a spectrum similarity measure implemented in the repository alongside cosine similarity and neutral loss similarity for comparing MS/MS spectra in the discovery of"
- [intro] Comparison of cosine, modified cosine, and neutral loss based spectral alignment for discovery of structurally related molecules: "Comparison of cosine, modified cosine, and neutral loss based spectral alignment for discovery of structurally related molecules"
- [readme] for score, filename in [(None, "spectra.png"), ("cosine", "cosine.png"), ("modified_cosine", "modified_cosine.png"), ("neutral_loss", "neutral_loss.png"),]: plot.plot_mirror(spectrum1, spectrum2, score, filename): "for score, filename in [(None, "spectra.png"), ("cosine", "cosine.png"), ("modified_cosine", "modified_cosine.png"), ("neutral_loss", "neutral_loss.png"),]: plot.plot_mirror(spectrum1, spectrum2,"
