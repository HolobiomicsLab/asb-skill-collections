---
name: fragment-ion-mass-calibration
description: Use when when comparing experimental spectra to reference library spectra and fragment ion m/z values show systematic drift or measurement noise that could distort neutral loss peaks or cosine similarity scores.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - spectrum_utils.spectrum
  - cosine_neutral_loss repository
  techniques:
  - tandem-MS
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

# fragment-ion-mass-calibration

## Summary

Calibrate fragment ion m/z values in tandem mass spectra to correct systematic measurement errors before similarity matching. Accurate fragment masses are essential for reliable neutral loss calculation and spectrum alignment in library search workflows.

## When to use

When comparing experimental spectra to reference library spectra and fragment ion m/z values show systematic drift or measurement noise that could distort neutral loss peaks or cosine similarity scores. Particularly important before applying neutral loss similarity measures, which depend on accurate m/z differences between precursor and fragment ions.

## When NOT to use

- Spectra are already certified by the instrument vendor or laboratory as calibrated within acceptable tolerance (typically < 5 ppm).
- Input spectra are from a standardized, pre-calibrated library (e.g., GNPS, MassBank) where m/z accuracy is guaranteed.
- Analysis goal is only qualitative (e.g., presence/absence detection) rather than quantitative mass matching.

## Inputs

- Tandem mass spectra with precursor m/z and fragment ion peaks (m/z, intensity pairs)
- Reference calibration data or known fragment ion assignments
- Mass measurement error estimates or tolerance parameters

## Outputs

- Calibrated fragment ion m/z values
- Recalibrated spectrum objects ready for similarity scoring
- Calibration correction coefficients (slope, intercept, or polynomial)

## How to apply

Extract fragment ion peaks (m/z and intensity pairs) from both query and reference spectra. Identify known calibrant peaks or use internal reference fragments to estimate systematic m/z shifts across the mass range. Apply a linear or polynomial correction function to all fragment m/z values to align them to expected theoretical values. Re-normalize peak intensities if needed. Validate calibration by checking that neutral loss peaks align correctly with reference data before proceeding to similarity calculation (cosine, modified cosine, or neutral loss). The calibration should minimize mass measurement error within the tolerance window used by the spectrum comparison algorithm.

## Related tools

- **spectrum_utils.spectrum** (Spectrum object representation and manipulation; provides m/z range filtering and peak access for calibration workflows) — github.com/bittremieux/cosine_neutral_loss
- **cosine_neutral_loss repository** (Reference implementation of neutral loss similarity; depends on accurate fragment m/z values for neutral loss peak transformation) — github.com/bittremieux/cosine_neutral_loss

## Examples

```
spectrum1 = sus.MsmsSpectrum.from_usi(usi1); spectrum1 = spectrum1.set_mz_range(0, spectrum1.precursor_mz); spectrum1 = spectrum1.remove_precursor_peak(0.1, 'Da'); # Fragments now calibrated for neutral loss similarity
```

## Evaluation signals

- Fragment m/z values align within the specified tolerance (e.g., < 5 ppm or < 0.1 Da) to theoretical or reference library values after calibration.
- Neutral loss peaks computed from calibrated spectra (precursor m/z minus fragment m/z) cluster tightly with reference spectra, indicating correct m/z differences.
- Cosine and neutral loss similarity scores increase or stabilize after calibration compared to pre-calibration scores, reflecting improved mass alignment.
- Calibration correction coefficients remain stable across repeated measurements and do not show systematic drift with m/z value.
- No outlier fragments remain after calibration; residual m/z error distribution is centered near zero with narrow standard deviation.

## Limitations

- Calibration accuracy depends on availability of reliable calibrant peaks or reference assignments; spectra with poor signal-to-noise or sparse fragment ion counts may not calibrate robustly.
- Polynomial or non-linear calibration models risk overfitting to local mass ranges and may not generalize to low- or high-mass regions if calibrant coverage is sparse.
- Fragment m/z calibration does not account for precursor m/z measurement error; precursor mass should be independently validated or recalibrated.
- Post-calibration performance gains are most pronounced when input spectra have significant systematic mass drift (> 50 ppm); well-maintained instruments may show minimal improvement.

## Evidence

- [other] Neutral loss similarity is implemented as a spectrum similarity measure in the repository alongside cosine and modified cosine approaches for comparing mass spectral data.: "Neutral loss similarity is implemented as a spectrum similarity measure in the repository alongside cosine and modified cosine approaches"
- [other] Transform fragment peaks to neutral losses by subtracting each peak m/z from the precursor m/z for both spectra.: "Transform fragment peaks to neutral losses by subtracting each peak m/z from the precursor m/z for both spectra"
- [readme] The README lists neutral loss similarity with a reference to how neutral loss data enhances molecular similarity analysis.: "Neutral loss similarity ... Aisporna, A. _et al_. Neutral loss mass spectral data enhances molecular similarity analysis in METLIN"
- [intro] Code repository implements cosine similarity, modified cosine similarity, and neutral loss similarity measures for spectrum comparison.: "Code repository implements cosine similarity, modified cosine similarity, and neutral loss similarity measures for spectrum comparison"
