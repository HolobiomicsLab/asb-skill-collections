---
name: spectral-peak-binning-and-vectorization
description: Use when you have raw MS/MS spectra with variable numbers of peaks at
  continuous m/z values and need to feed them to a neural network (e.g., Siamese network
  for similarity prediction) that requires fixed-size vector input.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - matchms
  - Python
  - ms2deepscore
  - Python (NumPy, TensorFlow/PyTorch)
  techniques:
  - LC-MS
  - ion-mobility-MS
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included
  cleaning compound names
- Our MS2DeepScore Python library offers two types of data generators
- Our MS2DeepScore Python library
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-021-00558-4
  all_source_dois:
  - 10.1186/s13321-021-00558-4
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-peak-binning-and-vectorization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert a raw tandem mass spectrum (peaks at arbitrary m/z locations with varying intensities) into a fixed-dimensional numerical vector by binning peaks into equally-spaced m/z windows and applying intensity transformation. This preprocessing step prepares MS/MS spectra for neural network input and enables downstream similarity scoring.

## When to use

You have raw MS/MS spectra with variable numbers of peaks at continuous m/z values and need to feed them to a neural network (e.g., Siamese network for similarity prediction) that requires fixed-size vector input. Use this when spectra originate from GNPS, MassBank, or other repositories and must be standardized to a 10,000-dimensional representation covering the 10–1000 m/z range.

## When NOT to use

- Input spectrum has already been converted to a fixed-size vector or feature representation.
- You are working with ion mobility, drift time, or retention time data rather than m/z-based fragmentation spectra.
- The m/z range of your spectra extends substantially below 10 or above 1000; binning will lose or truncate out-of-range peaks.
- You require lossless reconstruction of original peak positions and intensities; binning to 10,000 discrete bins introduces quantization error.

## Inputs

- raw MS/MS spectrum object with peaks (m/z values and intensity pairs)
- spectrum metadata including maximum peak intensity for normalization

## Outputs

- binned spectrum vector (10,000 or 9,948 dimensions, float32/float64)
- square-root-transformed intensity values in [0, ~1] range

## How to apply

First, filter the spectrum by removing peaks with intensities < 0.1% of the maximum peak intensity and retaining only the 1,000 highest-intensity peaks to reduce noise and computational burden. Square-root-transform all remaining peak intensities to avoid over-weighting the highest peaks. Bin the transformed peaks into 10,000 equally-spaced bins spanning m/z 10–1000 (each bin ~0.099 m/z wide). Assign each peak to the nearest bin and record its square-root-transformed intensity in that bin (setting zero-intensity bins to 0). The output is a 9,948-dimensional vector (after filtering to active m/z range) that can be passed directly to a dense neural network layer for embedding computation.

## Related tools

- **matchms** (Metadata cleaning, peak filtering, and spectrum I/O for preparing raw MS/MS data before binning) — https://github.com/matchms/matchms
- **ms2deepscore** (Applies binning as part of the data preparation pipeline before passing vectors to the Siamese network base network) — https://github.com/matchms/ms2deepscore
- **Python (NumPy, TensorFlow/PyTorch)** (Implementation of binning logic, intensity transformation, and vector construction)

## Examples

```
```python
import numpy as np
from matchms.filtering import normalize_intensities, remove_peaks_below_threshold, select_top_n_peaks

# Load and clean spectrum using matchms
spectrum = normalize_intensities(spectrum)
spectrum = remove_peaks_below_threshold(spectrum, threshold=0.001)  # 0.1% of max
spectrum = select_top_n_peaks(spectrum, n=1000)

# Bin into 10,000 bins (10–1000 m/z)
mz_array = np.sqrt(spectrum.peaks.mz)
intensity_array = np.sqrt(spectrum.peaks.intensity)
binned_spectrum = np.zeros(10000)
bins = np.digitize(mz_array, bins=np.linspace(10, 1000, 10001)) - 1
for i, b in enumerate(bins):
    if 0 <= b < 10000:
        binned_spectrum[b] = max(binned_spectrum[b], intensity_array[i])
```
```

## Evaluation signals

- Output vector has exactly 10,000 dimensions (or 9,948 after m/z filtering) with no NaN or Inf values.
- All non-zero bin values are in range [0, ~1] after square-root transformation (verify by checking max/min of non-zero entries).
- Peaks outside m/z 10–1000 are either truncated or handled consistently; no peaks appear in bins outside the designated range.
- Spectral energy is conserved: sum of binned intensities correlates strongly with sum of original (transformed) peak intensities (r > 0.99).
- When applied to a reference spectrum multiple times, output vector remains identical (deterministic binning), and t-SNE/UMAP visualization of embeddings derived from binned vectors shows meaningful chemical clusters (validated against molecular fingerprint Tanimoto scores).

## Limitations

- Binning to 10,000 fixed bins across m/z 10–1000 assumes all spectra fall within this range; spectra with m/z < 10 or > 1000 will have peaks truncated or lost.
- The square-root transformation reduces but does not eliminate the dominance of high-intensity peaks; low-abundance diagnostic peaks may be further suppressed.
- Binning introduces quantization error; two peaks within the same bin are indistinguishable in the vector representation.
- The method is not suitable for very sparse spectra (few peaks) or spectra with unusual isotope patterns, as binning may obscure fine structural detail.
- No explicit handling of peptide cross-linking, neutral loss pathways, or multi-stage MS/MS cascades; the method treats all m/z regions uniformly.

## Evidence

- [methods] Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z: "Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z"
- [methods] The spectra underwent basic filtering to remove excessive amounts of peaks, by removing peaks with intensities < 0.1% of the maximum peak intensity and limiting the maximum number of peaks to the 1000 highest intensity peaks: "The spectra underwent basic filtering to remove excessive amounts of peaks, by removing peaks with intensities < 0.1% of the maximum peak intensity and limiting the maximum number of peaks to the"
- [methods] Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only: "Peak intensities were square root transformed to avoid a too strong focus on the highest intensity peaks only"
- [other] Load a binned MS/MS spectrum vector (9948-dimensional, with peaks binned into 10–1000 m/z range at 10,000 equally-spaced bins, square-root-transformed intensities): "Load a binned MS/MS spectrum vector (9948-dimensional, with peaks binned into 10–1000 m/z range at 10,000 equally-spaced bins, square-root-transformed intensities)"
- [readme] To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum.: "To calculate chemical similarity scores, MS2DeepScore first calculates an embedding (vector) representing each spectrum."
