---
name: ms-ms-spectral-preprocessing-noise-removal
description: Use when when you have raw MS/MS spectra (from NIST, MassBank, or local acquisition) and plan to compute spectral similarity for compound identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MSEntropy
  - SpectralEntropy
  - spectral_similarity
  - ms_distance
  - Entropy Search GUI
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s41592-021-01331-z
  title: Spectral entropy
evidence_spans:
- These are all integrated into the [MSEntropy package
- These are all integrated into the MSEntropy package (https://github.com/YuanyueLi/MSEntropy)
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

# MS/MS Spectral Preprocessing: Noise Removal

## Summary

Remove low-intensity noise peaks from MS/MS spectra prior to similarity computation by filtering peaks below a relative intensity threshold. This preprocessing step improves compound identification performance by reducing spurious peak contributions to entropy similarity and other spectral distance metrics.

## When to use

When you have raw MS/MS spectra (from NIST, MassBank, or local acquisition) and plan to compute spectral similarity for compound identification. Apply this step before calculating entropy similarity, dot product similarity, or any other spectral distance metric, especially when spectra contain weak background noise or instrument artifacts that could inflate spurious matches.

## When NOT to use

- When analyzing untargeted metabolomics data where weak peaks may represent real low-abundance metabolites or adducts critical for annotation.
- If your use case requires retention of all peaks for isotope pattern analysis or high-mass-accuracy fragment tracking.
- When spectra have already been preprocessed by your acquisition software or data provider with undocumented filtering parameters.

## Inputs

- MS/MS spectral peak lists (m/z and intensity pairs)
- Raw spectra in formats: .mgf, .msp, .mzML, or .lbm2

## Outputs

- Preprocessed spectral peak lists with noise peaks removed
- Filtered spectra ready for similarity computation

## How to apply

For each spectrum in your dataset, identify the maximum peak intensity, then remove all peaks with intensity less than 1% of that maximum value. This relative thresholding approach is recommended over absolute cutoffs because it adapts to the dynamic range of individual spectra. Perform this filtering as a preprocessing step before loading spectra into similarity computation functions. The rationale is that low-intensity peaks contribute noise to entropy-based similarity calculations without adding discriminative signal for compound matching; removing them improves identification performance as demonstrated in the original spectral entropy validation study.

## Related tools

- **MSEntropy** (Provides integrated spectral entropy and entropy similarity computation functions after noise removal preprocessing) — https://github.com/YuanyueLi/MSEntropy
- **SpectralEntropy** (Original reference implementation for spectral similarity algorithms; recommends noise removal before similarity calculation) — https://github.com/YuanyueLi/SpectralEntropy
- **ms_distance** (Module within MSEntropy/SpectralEntropy that computes MS spectral distances on preprocessed peaks)
- **Entropy Search GUI** (User-facing tool for spectral comparison and library searching with built-in preprocessing support for .mgf, .msp, .mzML, .lbm2 formats) — https://github.com/YuanyueLi/EntropySearch

## Examples

```
```python
import numpy as np
import ms_entropy as me

# Load raw spectrum
peaks = np.array([[69.071, 7.917962], [86.066, 1.021589], [100.050, 0.5]])  # m/z, intensity

# Remove peaks below 1% of max intensity
max_intensity = np.max(peaks[:, 1])
threshold = 0.01 * max_intensity
filtered_peaks = peaks[peaks[:, 1] >= threshold]

# Now compute entropy similarity on cleaned spectra
similarity = me.entropy_similarity(filtered_peaks, reference_peaks)
```
```

## Evaluation signals

- Verify that all retained peaks have intensity ≥ 1% of the spectrum's maximum intensity; all removed peaks have intensity < 1%.
- Compare similarity score distributions before and after preprocessing: entropy similarity and other distance metrics should show improved discrimination (higher scores for true matches, lower for decoys).
- Confirm that compound identification accuracy (e.g., top-1 match rate or Area Under the ROC Curve against reference datasets like NIST) improves after filtering compared to unfiltered spectra.
- Check that the number of peaks retained per spectrum is reasonable (typically 5–20 for small-molecule MS/MS); extreme reductions suggest over-aggressive filtering or incorrect normalization.
- Validate numerical reproducibility: filtering the same spectrum twice produces identical output peak lists and identical downstream similarity scores.

## Limitations

- The 1% intensity threshold is a heuristic; it may remove weak but genuine low-abundance fragment ions in some spectra or retain noise in others depending on instrument and acquisition settings.
- Relative thresholding assumes spectra are normalized to the maximum peak intensity before filtering; if spectra have been pre-normalized differently (e.g., base-peak normalization, total ion normalization), the threshold must be adjusted accordingly.
- Filtering is applied per-spectrum independently; it does not account for across-spectrum quality or abundance trends that might benefit from global normalization approaches.
- The skill does not address systematic noise sources (e.g., solvent background, contamination) that may persist even above the 1% threshold; alternative denoising methods (wavelet, statistical background modeling) may be needed for heavily contaminated spectra.

## Evidence

- [other] Before calculating spectral similarity, it's highly recommended to remove spectral noise. For example, peaks have intensity less than 1% maximum intensity can be removed to improve identificaiton performance: "Before calculating spectral similarity, it's highly recommended to remove spectral noise. For example, peaks have intensity less than 1% maximum intensity can be removed to improve identificaiton"
- [other] Preprocess spectra by removing peaks with intensity less than 1% of maximum intensity using the noise-removal filter.: "Preprocess spectra by removing peaks with intensity less than 1% of maximum intensity using the noise-removal filter."
- [readme] With the `MSEntropy` package, the method for calculating entropy similarity has been rewritten using the Flash entropy search algorithm. This has resulted in speed improvements without compromising accuracy.: "With the `MSEntropy` package, the method for calculating entropy similarity has been rewritten using the Flash entropy search algorithm."
- [readme] The GUI supports `.mgf`, `.msp`, `.mzML`, and `.lbm2` file formats.: "The GUI supports `.mgf`, `.msp`, `.mzML`, and `.lbm2` file formats."
- [readme] Entropy similarity, which measured spectral similarity based on spectral entropy, has been shown to outperform dot product similarity in compound identification.: "Entropy similarity, which measured spectral similarity based on spectral entropy, has been shown to outperform dot product similarity in compound identification."
