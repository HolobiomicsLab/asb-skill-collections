---
name: mass-spectrum-peak-normalization
description: Use when when comparing two or more MSMS spectra using intensity-weighted similarity measures (cosine similarity, modified cosine, or neutral loss similarity), and the spectra have been acquired under different instrumental conditions, ionization efficiencies, or detector gains that produce.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - spectrum_utils.spectrum.MsmsSpectrum
  - cosine_neutral_loss repository
  techniques:
  - CE-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-peak-normalization

## Summary

Normalize fragment peak intensities in tandem mass spectra to a common scale (typically 0–1 or unit norm) to enable fair intensity-weighted similarity comparisons across spectra with different dynamic ranges or absolute intensity values. This is a prerequisite step for cosine-based and neutral loss similarity scoring.

## When to use

When comparing two or more MSMS spectra using intensity-weighted similarity measures (cosine similarity, modified cosine, or neutral loss similarity), and the spectra have been acquired under different instrumental conditions, ionization efficiencies, or detector gains that produce different absolute intensity ranges. Normalization is required before computing dot products or vector norms.

## When NOT to use

- Input spectra are already in a pre-normalized or standardized format (e.g., intensity values already in 0–1 range from library).
- The analysis goal is to preserve absolute intensity information for quantification or abundance comparison; normalization discards quantitative intensity differences.
- Spectra contain no fragment peaks after precursor removal and m/z filtering; resulting vectors would be empty or all-zero.

## Inputs

- Query MSMS spectrum (precursor m/z, list of fragment peaks with m/z and intensity)
- Reference MSMS spectrum (precursor m/z, list of fragment peaks with m/z and intensity)

## Outputs

- Normalized query spectrum intensity vector (unit norm, real-valued)
- Normalized reference spectrum intensity vector (unit norm, real-valued)

## How to apply

For each input spectrum, extract the fragment peaks (m/z and intensity pairs) after removing the precursor peak and restricting to the desired m/z range (e.g., 0 to precursor m/z). Construct an intensity vector from all peaks in the spectrum. Normalize the intensity vector to unit norm (L2 normalization, Euclidean norm) by dividing each intensity by the square root of the sum of squared intensities across all peaks. This transforms intensities to a 0–1 range where the vector magnitude equals 1.0. Apply the same normalization independently to both query and reference spectra before computing similarity scores. The rationale is that unit-norm normalization makes similarity scores invariant to absolute intensity scaling, allowing structural comparison based on the relative distribution of fragment masses rather than instrument-dependent absolute values.

## Related tools

- **spectrum_utils.spectrum.MsmsSpectrum** (Spectrum object model and methods for loading, filtering (set_mz_range, remove_precursor_peak), and accessing fragment peaks for normalization) — github.com/bittremieux/cosine_neutral_loss
- **cosine_neutral_loss repository** (Reference implementation of cosine, modified cosine, and neutral loss similarity measures that depend on normalized intensity vectors) — github.com/bittremieux/cosine_neutral_loss

## Examples

```
import spectrum_utils.spectrum as sus
spectrum1 = sus.MsmsSpectrum.from_usi('mzspec:GNPS:GNPS-LIBRARY:accession:CCMSLIB00000424840')
spectrum1 = spectrum1.set_mz_range(0, spectrum1.precursor_mz).remove_precursor_peak(0.1, 'Da')
```

## Evaluation signals

- L2 norm of the normalized intensity vector equals 1.0 (or is within numerical tolerance ~1e-6).
- All normalized intensities are in the range [0, 1].
- Cosine similarity or neutral loss similarity score computed on normalized spectra is in the expected range [0, 1] with no NaN or infinity values.
- Similarity scores between two spectra are identical when absolute intensities are uniformly scaled (e.g., multiplying all peaks by 10) before normalization, demonstrating scale invariance.
- Mirror plot visualization shows peaks aligned by m/z without intensity distortion artifacts.

## Limitations

- Spectra with very few fragment peaks (e.g., 1–2 peaks) may yield unstable similarity scores after normalization due to sparse vector representation.
- Normalization is sensitive to noise peaks; intense noise peaks will inflate the norm and suppress signal from true fragment peaks. Pre-filtering or denoising is recommended.
- Normalization discards information about absolute ion abundance; applications requiring quantitative or relative quantification must store original intensities separately.
- If a spectrum contains no peaks after precursor removal and m/z range filtering, the intensity vector becomes zero and normalization is undefined (division by zero).

## Evidence

- [other] Parse input spectra (precursor m/z and fragment peaks with intensities) for both query and reference spectra... Create normalized intensity vectors for neutral loss peaks in each spectrum.: "Create normalized intensity vectors for neutral loss peaks in each spectrum"
- [readme] spectrum1 = spectrum1.set_mz_range(0, spectrum1.precursor_mz)
spectrum1 = spectrum1.remove_precursor_peak(0.1, "Da"): "spectrum1 = spectrum1.set_mz_range(0, spectrum1.precursor_mz)
spectrum1 = spectrum1.remove_precursor_peak(0.1, "Da")"
- [intro] Cosine similarity calculation for spectrum comparison: "Cosine similarity calculation for spectrum comparison"
