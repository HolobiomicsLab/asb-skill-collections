---
name: noise-smoothing-chromatographic-signals
description: Use when when you have raw LC-HRMS profile-mode data (rt × mz intensity matrices) and need to detect chromatographic peaks using gradient-descent or local-maxima algorithms.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - PeakBot
  - TensorFlow
derived_from:
- doi: 10.1093/bioinformatics/btac344
  title: PeakBot
evidence_spans:
- PeakBot is a python package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_peakbot_cq
    doi: 10.1093/bioinformatics/btac344
    title: PeakBot
  dedup_kept_from: coll_peakbot_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac344
  all_source_dois:
  - 10.1093/bioinformatics/btac344
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# noise-smoothing-chromatographic-signals

## Summary

Apply smoothing filters to LC-HRMS chromatographic signals (retention time × m/z matrices) to reduce noise prior to peak detection. This preprocessing step is essential for accurate gradient-descent peak localization and feature extraction in untargeted metabolomics workflows.

## When to use

When you have raw LC-HRMS profile-mode data (rt × mz intensity matrices) and need to detect chromatographic peaks using gradient-descent or local-maxima algorithms. The smoothing step is mandatory before peak border and center estimation to reduce false positives from background noise and instrument artifacts.

## When NOT to use

- If you already have centroided or deconvoluted peak lists (not profile-mode raw data)
- If your LC-HRMS signal-to-noise ratio is already very high (e.g., SIM or MRM mode with minimal baseline noise); smoothing may become unnecessary and risk peak distortion
- If you are working with already-feature-extracted data or vendor-processed peak tables

## Inputs

- raw LC-HRMS chromatogram data (retention time × m/z intensity matrix, typically NetCDF or mzML format)
- training chromatogram dataset

## Outputs

- smoothed chromatographic signal (rt × mz matrix with attenuated noise)
- intermediate representation ready for gradient-descent peak detection

## How to apply

Load your training chromatogram data in retention time × m/z matrix format. Apply a smoothing filter (specific kernel and window size are implementation-dependent; PeakBot's approach is designed for two-dimensional LC-HRMS data) to attenuate high-frequency noise while preserving peak shape integrity. The smoothed signal is then fed directly into a gradient-descent algorithm to locate chromatographic peak maxima and estimate peak borders and centers. The choice of smoothing strength should balance noise reduction against peak shape distortion; too aggressive smoothing will broaden or merge nearby peaks, while insufficient smoothing will leave noise-driven false maxima. Verify post-smoothing by visual inspection of a subset of chromatograms to confirm peaks remain well-resolved.

## Related tools

- **PeakBot** (Python package that implements smoothing as a preprocessing step before gradient-descent peak detection in LC-HRMS chromatograms) — https://github.com/christophuv/PeakBot
- **TensorFlow** (Machine-learning framework used by PeakBot for CNN-based peak classification after smoothing and peak detection) — https://www.tensorflow.org/

## Examples

```
python quickExample_GPU.py  # PeakBot example that includes smoothing as part of the training pipeline; or manually: from peakbot import preprocessing; smoothed_chromatogram = preprocessing.smooth_chromatogram(raw_rt_mz_matrix, kernel_size=5)
```

## Evaluation signals

- Visual inspection: smoothed chromatogram shows reduced high-frequency noise while preserving peak maxima and shoulders
- Peak detection consistency: gradient-descent algorithm successfully locates expected number of local maxima without spurious noise-driven peaks
- Peak shape integrity: FWHM and peak asymmetry metrics of known reference peaks remain within ±10% of theoretical values post-smoothing
- Matching success rate: when matched against user-defined reference list, smoothed peaks exhibit rt and m/z alignment error < ±1 scan / ±5 ppm
- Signal recovery: intensity of smoothed peaks should not deviate >5% from raw peak area when integrated across the smoothed window

## Limitations

- Smoothing strength is not quantitatively parameterized in the README; users must empirically validate for their instrument and sample type
- Two-dimensional smoothing (across both rt and m/z dimensions) may blur isomeric peak doublets or co-eluting features if applied too aggressively
- Performance depends on LC-HRMS data quality; severely noisy or poorly-calibrated instruments may require manual parameter tuning or preprocessing steps before smoothing
- Smoothing alone does not resolve true co-elution; downstream peak matching and CNN classification are required to distinguish overlapping peaks

## Evidence

- [readme] searching for chromatographic peaks using a smoothing and gradient-descend algorithm: "searching for chromatographic peaks using a smoothing and gradient-descend algorithm"
- [readme] uses local-maxima in the LC-HRMS dataset each of which is then exported as a standarized two-dimensional area (rt x mz): "uses local-maxima in the LC-HRMS dataset each of which is then exported as a standarized two-dimensional area (rt x mz)"
- [readme] The peaks' borders and centers are also estimated in this step: "The peaks' borders and centers are also estimated in this step"
- [other] Load training chromatogram data (retention time × m/z matrix format). Apply smoothing filter to the chromatographic signal to reduce noise.: "Load training chromatogram data (retention time × m/z matrix format). Apply smoothing filter to the chromatographic signal to reduce noise."
- [readme] matched with a user-defined reference list (the ground-truth; isolated single chromatographic peaks) with the aim of using the same chromatographic peak but from different samples: "matched with a user-defined reference list (the ground-truth; isolated single chromatographic peaks)"
