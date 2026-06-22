---
name: mass-range-window-restriction
description: Use when you have loaded an MsmsSpectrum object and need to focus analysis on a biologically or chemically relevant mass window.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - NumPy
  - Numba
  - spectrum_utils
derived_from:
- doi: 10.1021/acs.analchem.9b04884
  title: spectrumutils
evidence_spans:
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization.
- spectrum_utils is a Python package for efficient mass spectrometry data processing and visualization
- Spectrum processing in spectrum_utils has been optimized for computational efficiency using [NumPy](https://www.numpy.org/)
- import numpy as np
- optimized for computational efficiency using [NumPy](https://www.numpy.org/) and [Numba](http://numba.pydata.org/)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-range-window-restriction

## Summary

Restrict mass spectrometry data to a predefined m/z range to remove spectral regions outside the analyte search space and reduce computational burden. This operation filters out low and high mass-to-charge peaks before downstream analysis.

## When to use

Apply this skill when you have loaded an MsmsSpectrum object and need to focus analysis on a biologically or chemically relevant mass window. Use it as a preprocessing step before precursor peak removal and noise filtering, particularly when working with peptide fragmentation spectra where the expected fragment m/z range is known (e.g., 100–1400 m/z for typical proteomics).

## When NOT to use

- When the expected m/z range of your analyte is unknown or spans the full detector range (e.g., untargeted metabolomics with wide precursor mass windows).
- If you have already applied intensity-based filtering that discarded most low-intensity peaks; mass-range restriction may then remove few additional peaks.
- When your analysis requires preservation of all acquired spectral data for subsequent external calibration or systematic error assessment.

## Inputs

- MsmsSpectrum object (loaded from USI or existing data structure)
- min_mz: float (lower mass-to-charge bound, e.g., 100)
- max_mz: float (upper mass-to-charge bound, e.g., 1400)

## Outputs

- MsmsSpectrum object with peaks outside the specified m/z range removed

## How to apply

Call the set_mz_range() method on your MsmsSpectrum object with min_mz and max_mz parameters that match your analyte's expected fragment mass range. For peptide mass spectrometry, restrict to 100–1400 m/z to exclude background noise outside the biologically relevant region. This operation is applied early in the preprocessing workflow, before removing precursor and noise peaks, because it reduces the dataset size and removes irrelevant spectral information that would otherwise complicate downstream filtering. The choice of bounds depends on your instrument, ionization mode, and the chemical composition of expected fragments.

## Related tools

- **spectrum_utils** (Provides the set_mz_range() method to restrict MsmsSpectrum objects to a user-defined mass window; optimized for computational efficiency using NumPy and Numba.) — https://github.com/bittremieux/spectrum_utils
- **NumPy** (Underlying numerical library used by spectrum_utils for efficient array-based filtering of peaks by m/z value.) — https://www.numpy.org/
- **Numba** (Just-in-time compilation library used by spectrum_utils to optimize computational performance of mass-range filtering operations.) — http://numba.pydata.org/

## Examples

```
spectrum.set_mz_range(min_mz=100, max_mz=1400)
```

## Evaluation signals

- All peaks in the output MsmsSpectrum fall within the specified [min_mz, max_mz] window; no peaks outside the bounds remain.
- The number of peaks in the output spectrum is less than or equal to the input spectrum (monotonic decrease or equality).
- Precursor m/z (if within the mass window) and expected fragment ion m/z values are preserved in the output.
- The m/z values of remaining peaks match the original data; only peaks are removed, no values are modified.
- When applied to a reference dataset (e.g., mzspec:MSV000082283:f07074:scan:5475 restricted to 100–1400 m/z), the output spectrum structure is valid and peak list is contiguous.

## Limitations

- Hard m/z boundaries may exclude legitimate low- or high-mass fragments if the window is chosen too narrowly; verification of the mass window against known fragment ion distributions is recommended.
- This operation is destructive — discarded peaks cannot be recovered without reloading the raw spectrum.
- The choice of min_mz and max_mz is domain-specific and must be justified for your experimental context (e.g., 100–1400 m/z is standard for tryptic peptides but may not suit other analytes).
- No changelog or versioning information is available in the repository, limiting traceability of parameter defaults or breaking changes across spectrum_utils versions.

## Evidence

- [other] Restrict the mass range to 100–1400 m/z to filter out irrelevant peaks: "Restrict the mass range to 100–1400 _m_/_z_ to filter out irrelevant peaks"
- [other] set_mz_range method signature and usage in preprocessing: "Call set_mz_range(min_mz=100, max_mz=1400) to restrict the mass range."
- [other] Position in preprocessing workflow before noise removal: "1. Load an MsmsSpectrum object (from a USI or existing data structure). 2. Call set_mz_range(min_mz=100, max_mz=1400) to restrict the mass range."
- [other] Computational efficiency rationale using NumPy and Numba: "Spectrum processing in spectrum_utils has been optimized for computational efficiency using [NumPy](https://www.numpy.org/) and [Numba](http://numba.pydata.org/)"
- [intro] Core spectrum preprocessing operations include intensity filtering and scaling: "Common spectrum processing operations (precursor & noise peak removal, intensity filtering, intensity scaling) optimized for computational efficiency."
