---
name: intensity-normalization-and-scaling
description: Use when when working with raw or filtered MsmsSpectrum objects where peak intensities span a wide dynamic range and need to be normalized for downstream spectrum comparison, database matching, or publication-quality visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - spectrum_utils
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package
- spectrum = sus.MsmsSpectrum.from_usi(usi)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b04884
  all_source_dois:
  - 10.1021/acs.analchem.9b04884
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# intensity-normalization-and-scaling

## Summary

Apply intensity normalization and scaling transformations to mass spectrometry spectra to standardize peak heights and improve comparability across spectra. This skill standardizes the dynamic range of fragment ion intensities, often as a final preprocessing step before spectrum matching or visualization.

## When to use

When working with raw or filtered MsmsSpectrum objects where peak intensities span a wide dynamic range and need to be normalized for downstream spectrum comparison, database matching, or publication-quality visualization. Particularly important when spectra from different instruments, acquisition protocols, or normalization states need to be made directly comparable.

## When NOT to use

- Input spectrum has already been normalized or scaled by an upstream processing step
- Downstream analysis requires raw, unscaled intensities for quantitative abundance comparisons
- Spectrum object contains negative or zero intensity values (data quality issue that must be addressed separately)

## Inputs

- MsmsSpectrum object (after noise filtering and precursor peak removal)
- Peak intensity array (1-D float array with positive values)

## Outputs

- MsmsSpectrum object with scaled intensity values
- Modified intensity array with square-root-scaled values

## How to apply

After filtering noise peaks and removing precursor ions, apply the scale_intensity() method with mode='root' to scale fragment ion intensities by their square root. This transformation compresses the dynamic range of high-intensity peaks while preserving the relative contribution of lower-intensity peaks, improving the signal-to-noise ratio for downstream analysis. The square-root scaling is computationally efficient and suitable for spectrum matching workflows. Verify that intensity arrays contain only positive values post-scaling and that the resulting spectrum's peak ranking and relative intensities remain interpretable.

## Related tools

- **spectrum_utils** (Provides the MsmsSpectrum.scale_intensity() method and intensity array manipulation) — https://github.com/bittremieuxlab/spectrum_utils
- **Python** (Runtime environment for spectrum_utils and array operations)

## Examples

```
spectrum.filter_intensity(min_intensity=0.05, max_num_peaks=50).scale_intensity(mode='root')
```

## Evaluation signals

- Intensity values are in the range [0, 1] or [0, sqrt(original_max)] depending on normalization baseline
- Peak ranking and relative intensity differences are preserved (peak A intensity / peak B intensity remains meaningful)
- Spectrum object's intensity array contains no NaN, infinite, or negative values after scaling
- Scaled spectrum can be successfully passed to downstream matching or visualization functions without errors
- Square-root transformation reduces dynamic range: max(scaled) / min(scaled) < max(raw) / min(raw)

## Limitations

- Square-root scaling may over-emphasize low-intensity noise peaks if noise filtering is insufficient; must be applied after filter_intensity() with appropriate thresholds
- Scale mode 'root' is optimized for computational efficiency but may not be optimal for all downstream applications; alternative scaling modes (e.g., log, max) may be needed for specific analysis goals
- Scaling is a lossy transformation; original raw intensities cannot be recovered after this step

## Evidence

- [intro] Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
- [other] Apply scale_intensity with mode='root' to scale intensities by their square root: "Scale peak intensities by their square root"
- [other] Detailed workflow step showing scale_intensity usage in context: "Apply scale_intensity with mode='root' to scale intensities by their square root."
- [other] The filter_intensity step must precede scaling: "Apply filter_intensity with min_intensity=0.05 (as a fraction of base peak) and max_num_peaks=50 to remove low-intensity noise and cap the peak count."
