---
name: precursor-and-noise-filtering
description: Use when you have loaded raw tandem MS spectra (in MGF, mzML, or similar
  format) and need to prepare them for peptide identification, spectral library matching,
  or intensity-based analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pymzML
  - pyOpenMS
  - Python
  - seaborn
  - NumPy
  - pyteomics
  - spectrum_utils
  - Numba
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- pymzML (version 2.5.2)
- pyOpenMS (version 2.7.0)
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing
  and visualization
- import seaborn as sns
- Spectrum processing in spectrum_utils has been optimized for computational efficiency
  using [NumPy](https://www.numpy.org/)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spectrumutils_cq
    doi: 10.1021/acs.analchem.9b04884
    title: spectrumutils
  dedup_kept_from: coll_spectrumutils_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.9b04884
  all_source_dois:
  - 10.1021/acs.analchem.9b04884
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# precursor-and-noise-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Remove interfering peaks (precursor ion and low-intensity noise) from tandem mass spectra to improve signal quality and reduce computational burden in downstream analysis. This is a foundational spectrum preprocessing step that enhances spectral matching and annotation accuracy.

## When to use

Apply this skill when you have loaded raw tandem MS spectra (in MGF, mzML, or similar format) and need to prepare them for peptide identification, spectral library matching, or intensity-based analysis. Use it before intensity filtering or scaling, especially when spectra contain intense precursor peaks or high baseline noise that would otherwise dominate peak-matching algorithms.

## When NOT to use

- Input spectra are MS1 (precursor-only) scans with no expected fragment ions — there is no precursor peak to remove and noise filtering may over-aggressively remove signal.
- Precursor m/z or charge state metadata is missing or unreliable — removal will fail or remove incorrect peaks.
- Downstream analysis explicitly requires the precursor peak (e.g., precursor mass accuracy validation) — removing it will invalidate those checks.

## Inputs

- Spectrum objects with populated m/z and intensity arrays
- Precursor m/z and charge state metadata
- Fragment mass tolerance (Da or ppm)
- Base peak intensity reference

## Outputs

- Filtered spectrum objects with precursor peak removed
- Spectra with noise peaks below threshold eliminated
- Peak count (before and after filtering)
- Intensity distribution after filtering

## How to apply

First, remove the precursor peak by identifying the m/z corresponding to the selected precursor ion (available in spectrum metadata) and eliminating all peaks within a user-defined mass tolerance window (typically 0.02 Da in high-resolution MS). Then, apply intensity-based noise filtering by computing the base peak (most intense peak) in the spectrum and retaining only peaks at ≥5% of that base peak intensity. Both operations preserve the relative intensities of genuine fragment peaks while eliminating low-signal noise and the dominant precursor signal that would otherwise bias downstream analysis. The order matters: remove precursor first (to avoid artificially lowering the base peak threshold), then filter by intensity threshold. Document the tolerance and threshold values used, as they may need adjustment based on your instrument resolution and spectral quality.

## Related tools

- **spectrum_utils** (Primary library providing optimized remove_precursor_peak() and filter_intensity() methods for precursor and noise filtering) — https://github.com/bittremieux/spectrum_utils
- **pymzML** (Alternative library for spectrum I/O and filtering; included in throughput comparison baseline) — https://github.com/pymzml/pymzML
- **pyOpenMS** (Alternative library for spectrum preprocessing and MS data handling; included in throughput comparison baseline)
- **pyteomics** (Used in the benchmark workflow to parse MGF files and extract valid spectra before filtering)
- **NumPy** (Underlying numerical library optimizing spectrum_utils filtering operations for computational efficiency) — https://www.numpy.org/
- **Numba** (JIT compiler used alongside NumPy to optimize spectrum_utils filtering performance) — http://numba.pydata.org/

## Examples

```
from spectrum_utils.spectrum import Spectrum
import numpy as np

spectrum.remove_precursor_peak(fragment_tol_mass=0.02, fragment_tol_mode='Da')
spectrum.filter_intensity(min_intensity=0.05, max_num_peaks=150)
```

## Evaluation signals

- Precursor peak is completely absent from filtered spectrum (verify by checking m/z range ±tolerance around precursor m/z)
- Peak count after filtering is ≤ original peak count, and no peaks remain below the 5% base peak intensity threshold
- Filtered spectrum retains majority of non-noise signal (compare summed intensity before/after; expect <10–15% total intensity loss for real spectra)
- Filtered spectra pass downstream spectral library matching or peptide identification with improved match scores compared to unfiltered spectra
- Processing completes within expected runtime (spectrum_utils v0.4.0 reported ~0.1–1 ms per spectrum depending on peak count; pymzML/pyOpenMS slower by 2–10×)

## Limitations

- Precursor peak removal accuracy depends on reliable precursor m/z metadata; presence of neutral loss peaks (e.g., H₂O, NH₃ from precursor) near the precursor m/z may be incompletely removed with fixed tolerance windows.
- The 5% base peak intensity threshold is heuristic and may remove genuine low-abundance fragment ions in spectra with highly skewed peak distributions (e.g., one very intense b or y ion); users may need to lower the threshold for low-charge or multiply-charged peptides.
- No explicit handling of chimeric spectra (multiple peptide precursors co-isolated); filtering assumes single-precursor spectra. For data-independent acquisition (DIA) or wide isolation windows, precursor removal may eliminate legitimate co-fragmented ions.
- Peak count restriction (e.g., ≤150 peaks after filtering) is not applied uniformly by all implementations; spectrum_utils documentation mentions 50 or 150 peaks, but exact limits depend on downstream use case.

## Evidence

- [intro] Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency.: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
- [other] Remove low-intensity noise peaks by only retaining peaks at least 5% of base peak intensity.: "Remove low-intensity noise peaks by only retaining peaks that are at at least 5% of the base peak intensity and restrict the total number of peaks to the 50 most intense peaks"
- [other] Precursor peak removal with 0.02 Da tolerance as part of the benchmark workflow.: "remove precursor peak (0.02 Da tolerance), filter by 5% base peak intensity (max 150 peaks)"
- [other] spectrum_utils version 0.4.0 is reported to be faster than alternative libraries pymzML and pyOpenMS.: "spectrum_utils (version 0.4.0) is faster than alternative libraries, such as pymzML (version 2.5.2) and pyOpenMS (version 2.7.0)"
- [other] Spectrum processing in spectrum_utils has been optimized for computational efficiency using NumPy and Numba.: "Spectrum processing in spectrum_utils has been optimized for computational efficiency using NumPy and Numba"
