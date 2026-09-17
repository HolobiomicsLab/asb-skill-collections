---
name: peak-detection-parameter-optimization
description: Use when when loading and processing raw or recalibrated FT-ICR mass
  spectrum data (Bruker .d format) on a defined field-strength instrument (e.g., 12
  T or 15 T), before executing molecular formula search.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - CoreMS
  - pandas
  - numpy
  - Bruker Solarix (via ReadBrukerSolarix)
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development
  and data analysis of small molecules analysis.'
- import pandas as pd
- import numpy as np
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems_cq
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5281/zenodo.14009575
  all_source_dois:
  - 10.5281/zenodo.14009575
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-detection-parameter-optimization

## Summary

Optimize noise thresholding and peak prominence parameters in FT-ICR mass spectrometry to correctly identify molecular ion peaks while minimizing false positives. This skill is essential for accurate molecular formula assignment downstream, as suboptimal parameter choice leads to either missed peaks or spurious assignments.

## When to use

When loading and processing raw or recalibrated FT-ICR mass spectrum data (Bruker .d format) on a defined field-strength instrument (e.g., 12 T or 15 T), before executing molecular formula search. Peak detection parameters must be tuned when the spectrum contains a wide dynamic range of peak heights, variable signal-to-noise ratios across m/z ranges, or when prior peak-picking results show inconsistent sensitivity across abundance ranges.

## When NOT to use

- Input is already a curated peak list or feature table from an external tool (e.g., mzML centroid data); re-processing would introduce inconsistency.
- Spectrum was acquired in magnitude-only mode or time-domain data is unavailable; CoreMS requires FT processing for proper calibration.
- Peak detection is not the bottleneck: if molecular formula assignment accuracy is already limited by mass calibration error or database coverage, tuning peak detection parameters will not improve results.

## Inputs

- Bruker FT-ICR raw transient data (.d format directory with ser/fid files)
- Recalibrated mass spectrum object with frequency-domain data
- Field-strength instrument configuration (B in Tesla)
- Reference calibration peaks or mass error constraints

## Outputs

- Filtered mass spectrum object with detected peaks (m/z, intensity, prominence)
- Peak list (m/z values with assigned abundance and signal-to-noise metrics)
- Noise threshold metadata (method, min_relative_abundance, peak_min_prominence_percent)

## How to apply

Initialize CoreMS mass spectrum parameters by selecting a noise thresholding method—either 'relative_abundance', 'log', or 'signal_noise'—based on the abundance distribution of your peaks. Set noise_threshold_min_relative_abundance (e.g., 1%) to filter out electronic noise below a baseline abundance level. Configure peak_min_prominence_percent (e.g., 1%) to define the minimum height difference a peak must exceed relative to its surrounding baseline. Run peak picking using apex quadratic fitting on the thresholded peaks. Validate the result by visual inspection (e.g., overlay detected peaks on the raw m/z profile) and by checking that the number of detected peaks and their m/z positions are consistent across replicate runs or prior calibration references. Adjust thresholds iteratively if peaks are missed (increase relative_abundance and prominence thresholds downward) or if noise spikes are falsely detected (increase thresholds upward).

## Related tools

- **CoreMS** (Framework providing mass spectrum object model, noise thresholding methods, and apex quadratic peak fitting for FT-ICR peak detection) — https://github.com/EMSL-Computing/CoreMS
- **Bruker Solarix (via ReadBrukerSolarix)** (Loader for raw Bruker .d format transient data and frequency-domain calibration) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Data structure for storing and exporting peak detection results as structured tables)
- **numpy** (Numerical array operations for threshold calculations and prominence computations)

## Examples

```
MSParameters.mass_spectrum.noise_threshold_method = 'relative_abundance'; MSParameters.mass_spectrum.noise_threshold_min_relative_abundance = 1; MSParameters.ms_peak.peak_min_prominence_percent = 1; mass_spectrum = ReadBrukerSolarix('data.d').get_mass_spectrum(0); mass_spectrum.find_peaks()
```

## Evaluation signals

- Detected peak count is within expected range for instrument resolution and sample complexity (e.g., 500–5000 peaks for complex organic mixtures on 12–15 T instruments).
- Apex m/z positions are stable and reproducible across repeated peak detection runs on the same spectrum with identical parameters.
- Mass calibration error (ppm) after molecular formula assignment is consistent with instrument specifications (<1 ppm for 12 T Solarix); if errors spike or widen after changing peak detection parameters, thresholds may be too permissive.
- Visual overlay of detected peaks on raw spectrum profile shows no obvious missed peaks in high-abundance regions and no spurious peaks in noise-dominated regions (m/z edges, low-intensity tails).
- Downstream molecular formula assignment yields a reasonable match rate (e.g., >70% of peaks receive at least one candidate assignment) without excessive ambiguity (>3 isomeric candidates per m/z).

## Limitations

- Noise thresholding methods ('relative_abundance', 'log', 'signal_noise') are empirical; optimal parameters vary with sample composition, ionization mode (ESI+/−), and instrumental conditions, requiring instrument-specific tuning.
- Apex quadratic fitting assumes peak shape is approximately Gaussian or Lorentzian; highly skewed or unresolved multiplets may be mislocalized.
- No automatic parameter selection is provided in the README; users must manually iterate or validate against reference datasets, which is time-consuming for large batches.
- Peak prominence is defined relative to local baseline within the peak's width; in regions of dense, closely-spaced peaks (e.g., high m/z in complex mixtures), small prominence thresholds may cause fragmentation or merging of true signals.

## Evidence

- [other] Initialize mass spectrum parameters for a 12 T field-strength instrument, setting noise thresholding method (e.g., relative_abundance or log) and peak prominence thresholds.: "Initialize mass spectrum parameters for a 12 T field-strength instrument, setting noise thresholding method (e.g., relative_abundance or log) and peak prominence thresholds."
- [results] noise_threshold_method can be set to 'relative_abundance', 'log', or 'signal_noise', with corresponding abundance and prominence parameters.: "MSParameters.mass_spectrum.noise_threshold_method = 'relative_abundance' / 'log' / 'signal_noise'; MSParameters.mass_spectrum.noise_threshold_min_relative_abundance = 1;"
- [readme] Peak picking uses apex quadratic fitting after noise thresholding.: "Peak picking using apex quadratic fitting"
- [results] ReadBrukerSolarix is used to load Bruker .d format data into CoreMS for processing.: "from corems.transient.input.brukerSolarix import ReadBrukerSolarix"
- [results] The workflow applies noise thresholding and peak picking after processing transient data and before molecular formula assignment.: "Apply noise thresholding and peak picking to detected peaks. Run CoreMS SearchMolecularFormulas with the 12 T calibration parameters"
