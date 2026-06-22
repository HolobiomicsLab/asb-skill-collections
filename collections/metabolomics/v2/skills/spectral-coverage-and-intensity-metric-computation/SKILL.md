---
name: spectral-coverage-and-intensity-metric-computation
description: Use when you have completed a ViMMS simulation run or processed real LC-MS/MS data and need to quantitatively assess whether one DDA controller (e.g., WeightedDEWController with exclusion) outperforms another (e.g., TopNController) in terms of spectral coverage and signal recovery.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - Poetry
  - VIMMS
  - OpenMS
  - MZMine
  techniques:
  - LC-MS
  - CE-MS
  - tandem-MS
derived_from:
- doi: 10.21105/joss.03990
  title: vimms
- doi: 10.1021/acs.analchem.0c03895
  title: ''
evidence_spans:
- ViMMS is compatible with Python 3+
- ViMMS dependencies are managed with [Poetry](https://python-poetry.org/)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_vimms
    doi: 10.21105/joss.03990
    title: vimms
  dedup_kept_from: coll_vimms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21105/joss.03990
  all_source_dois:
  - 10.21105/joss.03990
  - 10.1021/acs.analchem.0c03895
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-coverage-and-intensity-metric-computation

## Summary

Compute fragmentation coverage and cumulative intensity metrics from simulated or real LC-MS/MS acquisitions to evaluate and compare the efficacy of different data-dependent acquisition (DDA) strategies. This skill quantifies how completely a fragmentation strategy captures MS/MS spectra across detected analytes and measures total signal intensity recovered.

## When to use

Apply this skill when you have completed a ViMMS simulation run or processed real LC-MS/MS data and need to quantitatively assess whether one DDA controller (e.g., WeightedDEWController with exclusion) outperforms another (e.g., TopNController) in terms of spectral coverage and signal recovery. Specifically, use it after env.run() has captured scans and you have pickled EvaluationData or peak-picked mzML output ready for analysis.

## When NOT to use

- Input is raw, unprocessed mzML without peak picking applied—apply PeakPicking.py first.
- Only MS1 spectra are available (no MS/MS fragmentation data collected)—this metric requires MS2 scans.
- Evaluation data was not saved during the simulation run (save_eval=False in Environment instantiation).

## Inputs

- pickled EvaluationData object from ViMMS Environment run
- mzML file(s) output from env.write_mzML() or real LC-MS/MS acquisition
- peak-picking parameters (MZMine configuration) specifying MS1 intensity thresholds and ROI bounds
- comparison baseline (e.g., TopNController result for reference)

## Outputs

- coverage metrics (times_fragmented_summary, fragmentation rate)
- cumulative intensity scalar (total MS2 signal intensity recovered)
- comparative summary table (baseline vs. test controller metrics)
- evaluation report with ranked controller performance

## How to apply

Load the pickled EvaluationData object from the simulation environment output (or perform peak picking on real mzML using MZMine parameters in PeakPicking.py). Call evaluate_simulated_env() to compute coverage metrics (e.g., times_fragmented_summary) and cumulative intensity sums. The function internally leverages peak picking with user-specified MS1 intensity thresholds (e.g., min_ms1_intensity=1.75E5 for high-sensitivity evaluations or 5000 for exploratory runs) and ROI filtering parameters (min_roi_intensity, min_roi_length). Compare the returned coverage and intensity summaries across controllers using consistent filter settings—identical m/z ranges (e.g., 100–1000), RT tolerance (e.g., 15 s), and MS/MS match tolerances (MS1: 1 ppm, MS2: 0.05 ppm, minimum 3 matching peaks)—to ensure fair comparative evaluation. The output is a set of scalar metrics (total spectra acquired, coverage fraction, total intensity) that directly indicate which strategy is superior.

## Related tools

- **VIMMS** (Framework that generates simulated scans with EvaluationData capture; provides Environment.run() and evaluate_simulated_env() functions for metric computation) — https://github.com/glasgowcompbio/vimms
- **OpenMS** (Processes mzML output from simulation (or real acquisition) to compute fragmentation coverage using external MS analysis)
- **MZMine** (Peak picking engine integrated into ViMMS PeakPicking.py; applies MS1 intensity thresholds and ROI detection for downstream metric calculation)
- **Python** (Language environment for executing evaluate_simulated_env() and loading EvaluationData pickles)

## Examples

```
from vimms.Common import POSITIVE; env = Environment(ms, controller, min_time=0, max_time=1440, save_eval=True, out_file='sim.mzML', out_dir='./results'); env.run(); env.write_mzML(); eval_data = load_eval_data('results/sim_eval.p'); coverage = evaluate_simulated_env(eval_data, min_ms1_intensity=1.75E5)
```

## Evaluation signals

- Coverage metric (times_fragmented_summary) is a non-negative scalar between 0 and 1 (or 0–100%) representing fraction of detected analytes fragmented.
- Cumulative intensity metric is a strictly positive number (sum of MS2 peak intensities) and should be consistent across repeated runs with identical input and parameters.
- Comparative result shows the test controller's coverage and intensity both within a reasonable range relative to baseline (e.g., within 2× or 0.5× of TopNController)—extreme outliers suggest parameter misconfiguration or simulation error.
- Metrics are reproducible: re-running evaluate_simulated_env() with the same EvaluationData pickle and filter parameters yields identical numeric outputs.
- MS1/MS2 match counts and filtering statistics (rows retained after ROI and intensity filtering) are logged and should reflect the specified thresholds (e.g., min_ms1_intensity=1.75E5 filters out low-intensity features).

## Limitations

- Coverage metric is sensitive to peak-picking parameters (min_ms1_intensity, min_roi_length); different thresholds on the same raw data may yield different conclusions about which strategy is superior.
- Cumulative intensity comparison is meaningful only when the same chemical population (same m/z range, same RT window, same polarity) is used in both simulations; cross-run intensity comparisons require intensity normalization.
- The evaluation pipeline relies on MZMine peak picking, which may introduce errors in noisy regions or poorly separated peaks; validation against reference MS/MS libraries (e.g., GNPS-NIST14) is recommended for high-stakes decisions.
- Metric computation assumes that simulated intensity distributions match real mass spectrometer behavior; significant discrepancies between simulation and instrument output will degrade predictive value.

## Evidence

- [other] compute coverage and intensity metrics using evaluate_simulated_env(), comparing times_fragmented_summary and cumulative intensity against the baseline TopN result: "compute coverage and intensity metrics using evaluate_simulated_env(), comparing times_fragmented_summary and cumulative intensity against the baseline TopN result"
- [other] When running an `Environment` you can enable the `save_eval` flag: "When running an `Environment` you can enable the `save_eval` flag"
- [other] The evaluation helpers rely on peak picking using MZMine parameters defined in `PeakPicking.py`: "The evaluation helpers rely on peak picking using MZMine parameters defined in `PeakPicking.py`"
- [results] Filter by ROI intensity and length with minimum parameters: "RoiBuilderParams(min_roi_intensity=0, min_roi_length=3)"
- [results] Filter spectra matching with MS1 tolerance 1 ppm, MS2 tolerance 0.05 ppm, minimum 3 matching peaks: "matching_ms1_tol = 1, matching_ms2_tol = 0.05, matching_min_match_peaks = 3"
- [other] Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS: "Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS"
