---
name: mass-spectrum-noise-threshold-parameter-selection
description: Use when when processing raw or centroid mass spectra (e.g., ESI-MS or FT-ICR data from Bruker .d or Thermo .raw formats) and you need to remove instrument noise and low-abundance peaks before peak picking or molecular formula assignment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.encapsulation.factory.parameters import MSParameters
- CoreMS [section=results; evidence='from corems.encapsulation.factory.parameters import MSParameters']
- import pandas as pd
- pandas [section=results; evidence='import pandas as pd']
- import numpy as np
- numpy [section=results; evidence='import numpy as np']
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems
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

# mass-spectrum-noise-threshold-parameter-selection

## Summary

Selection and application of one of three mutually exclusive noise-threshold filtering methods in CoreMS (relative_abundance, signal_noise, or log mode) to remove low-intensity peaks and retain spectrum peaks above a user-defined threshold. Each method filters peaks using different criteria and produces different peak retention counts from the same input spectrum.

## When to use

When processing raw or centroid mass spectra (e.g., ESI-MS or FT-ICR data from Bruker .d or Thermo .raw formats) and you need to remove instrument noise and low-abundance peaks before peak picking or molecular formula assignment. Apply this skill when the spectrum contains hundreds or thousands of peaks and you must choose between filtering by relative abundance percentile, signal-to-noise ratio threshold, or standard deviation-based log filtering to reduce false positives in downstream annotation.

## When NOT to use

- Input spectrum is already noise-filtered or has been processed by a third-party tool—double filtering may remove genuine low-abundance features.
- When working with pseudo-molecular ions ([M+H]+, [M-H]−) where the signal-to-noise ratio is known to be unreliable (e.g., very low concentration samples with high chemical background).
- For untargeted discovery analyses where you explicitly need to retain weak features for later statistical filtering or machine-learning annotation.

## Inputs

- mass spectrum object (CoreMS Spectrum or MassSpectrum)
- raw instrument data file (.d, .raw, .mzML, .cdf, or generic mass list)
- MSParameters configuration object with noise_threshold_method and threshold parameters

## Outputs

- filtered mass spectrum object with noise peaks removed
- peak count per ionization mode and method name
- structured JSON or CSV record with method identifier and retention statistics

## How to apply

Load the mass spectrum data using CoreMS MSParameters factory to instantiate a noise-threshold configuration. Implement conditional dispatch logic to select one of three mutually exclusive noise-threshold methods: (1) 'relative_abundance' filters peaks by a minimum relative abundance parameter (percentage of base peak), (2) 'signal_noise' filters by a signal-to-noise ratio threshold (e.g., S/N > 3), or (3) 'log' filters by a standard deviation parameter applied in log-intensity space. Apply the selected method to the loaded spectrum using CoreMS peak-filtering routines. Capture the resulting peak count per ionization mode and method name. The choice of method depends on the analytical goal: relative_abundance is useful for removing very weak features while preserving abundant ions; signal_noise is appropriate when S/N estimates are reliable; log filtering is useful when peak intensity spans multiple orders of magnitude. Serialize results (method identifier, peak count, mode) as structured JSON or CSV for reproducibility.

## Related tools

- **CoreMS** (Python framework providing MSParameters factory, noise-threshold dispatch logic, and peak-filtering routines for mass spectrum processing) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Data serialization and tabulation of peak counts and method results)
- **numpy** (Numerical computation for standard deviation and log-intensity calculations in log-mode filtering)
- **Docker** (Containerization for reproducible CoreMS execution across environments)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; params = MSParameters(); params.ms_peak.noise_threshold_method = 'signal_noise'; params.ms_peak.s2n_threshold = 3.0; spectrum = load_spectrum('ESI_NEG_SRFA.d'); spectrum.apply_noise_filter(); print(f'Peaks after filter: {len(spectrum.peaks)}')
```

## Evaluation signals

- Peak count per method is deterministic and reproducible for the same input spectrum and parameters (noise_threshold_method, threshold value).
- Selected method produces fewer peaks than unfiltered spectrum; relative_abundance and signal_noise methods typically retain 5–50% of original peaks depending on threshold.
- Peak retention is monotonic: lowering the threshold (relaxing filter) retains equal or more peaks; raising the threshold (tightening filter) retains equal or fewer peaks.
- Serialized output JSON/CSV contains expected fields: method_name (string), threshold_value (numeric), peak_count_original (int), peak_count_filtered (int), ionization_mode (string).
- Visual inspection of filtered spectrum via matplotlib shows removal of low-intensity noise while preserving high-intensity molecular ions and expected isotope patterns.

## Limitations

- The three methods are mutually exclusive; only one can be applied per spectrum pass—combining methods requires manual post-filtering.
- Signal-to-noise filtering requires reliable S/N estimates from the instrument or pre-computed baseline; unreliable S/N estimates (common in very noisy or overloaded spectra) will produce incorrect filter decisions.
- Relative-abundance filtering is scale-dependent: a peak that is 5% of base peak in one ionization mode may be 1% in another, requiring mode-specific tuning.
- Log-mode filtering (standard deviation threshold) may fail or produce unexpected results on spectra with very broad dynamic ranges (>4 orders of magnitude) or multiple unrelated peak populations.
- No changelog is available in the CoreMS repository documentation, making it difficult to track changes to noise-threshold behavior across versions.

## Evidence

- [other] CoreMS provides three mutually exclusive noise threshold methods: 'relative_abundance' (filtered by minimum relative abundance parameter), 'signal_noise' (filtered by signal-to-noise ratio threshold), and 'log' (filtered by standard deviation parameter), each producing different peak retention counts for the same input spectrum.: "CoreMS provides three mutually exclusive noise threshold methods: 'relative_abundance' (filtered by minimum relative abundance parameter), 'signal_noise' (filtered by signal-to-noise ratio"
- [other] 1. Load mass spectrum data from ESI_NEG_SRFA.d using CoreMS MSParameters factory to instantiate noise-threshold configuration. 2. Implement conditional dispatch logic that selects one of three mutually exclusive noise-threshold methods (COND-001, COND-002, COND-003) based on spectrum properties or user input. 3. Apply the selected noise-threshold method to the loaded spectrum using CoreMS peak-filtering routines. 4. Capture the resulting peak count per ionization mode and method name. 5. Serialize the results (method identifier, peak count per mode) as a structured JSON or CSV record.: "Load mass spectrum data from ESI_NEG_SRFA.d using CoreMS MSParameters factory to instantiate noise-threshold configuration. Implement conditional dispatch logic that selects one of three mutually"
- [readme] Manual and automatic noise threshold calculation: "Manual and automatic noise threshold calculation"
- [readme] from corems.encapsulation.factory.parameters import MSParameters: "from corems.encapsulation.factory.parameters import MSParameters"
- [readme] Generic mass list in profile and centroid mde (include all delimiters types and Excel formats): "Generic mass list in profile and centroid mode (include all delimiters types and Excel formats)"
- [readme] Data handling and software development for modern mass spectrometry (MS) is an interdisciplinary endeavor requiring skills in computational science and a deep understanding of MS.: "Data handling and software development for modern mass spectrometry (MS) is an interdisciplinary endeavor requiring skills in computational science and a deep understanding of MS."
