---
name: metabolite-detection-and-acquisition-performance-benchmarking
description: Use when you have simulated or experimental mzML data from two or more
  fragmentation controllers (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3699
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Poetry
  - VIMMS
  - OpenMS
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-detection-and-acquisition-performance-benchmarking

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A comparative evaluation skill for quantifying how well different tandem MS fragmentation strategies (e.g., WeightedDEW with exclusion vs. TopN) detect and acquire metabolite spectra in virtual LC-MS/MS experiments. This skill measures coverage metrics, intensity profiles, and MS/MS acquisition efficiency using simulated or real mzML data against reference chemical libraries.

## When to use

Use this skill when you have simulated or experimental mzML data from two or more fragmentation controllers (e.g., WeightedDEWController vs. TopNController) and need to determine which strategy achieves better metabolite detection rates, cumulative MS1 intensity coverage, fragmentation times, and MS/MS spectrum quality. This is essential when validating a new controller design before deploying it to real instruments, or when re-acquiring existing LC-MS/MS data with alternative fragmentation rules to compare outcomes.

## When NOT to use

- Input is a single mzML file or a single controller run — benchmarking requires ≥2 strategies to compare.
- Chemical mixture is not well-characterized or lacks retention time and m/z ground truth — evaluation metrics depend on knowing what should have been fragmented.
- The fragmentation library (GNPS, HMDB) is incomplete or misaligned with your chemical space — spectral matching will be unreliable.

## Inputs

- Simulated or empirical mzML files from ViMMS Environment (two or more controller variants)
- EvaluationData pickled objects from each simulation run
- Chemical mixture list (e.g., UniformMZFormulaSampler or DatabaseFormulaSampler output)
- Reference fragmentation library (GNPS-NIST14-MATCHES.mgf or HMDB metabolites)
- Controller configuration (isolation_width, N, mz_tol, rt_tol, min_ms1_intensity)

## Outputs

- Comparative metrics table (times_fragmented_summary per controller)
- Coverage report (number and % of chemicals fragmented)
- Cumulative MS1 intensity profile per controller
- Mass spectral matching results (cosine similarity, matching peaks, coverage per chemical)
- Peak-picked spectral data (MZMine format) for downstream analysis

## How to apply

First, run two or more fragmentation strategies through the ViMMS simulation environment using the same chemical mixture (e.g., 100 chemicals sampled uniformly from m/z 100–500 using UniformMZFormulaSampler) and identical mass spectrometer configuration (polarity, isolation width, MS levels). For each controller, instantiate an Environment with save_eval=True to capture EvaluationData pickles and write_mzML() to serialize scans. Extract the pickled EvaluationData object from each run and invoke evaluate_simulated_env() to compute times_fragmented_summary (tracking acquisition decisions per chemical) and cumulative intensity metrics. Load reference fragmentation spectra (e.g., GNPS-NIST14-MATCHES.mgf) and apply peak picking with MZMine parameters, then use OpenMS to measure coverage (number of chemicals fragmented) and matching rates (ms1_tol=1 ppm, ms2_tol=0.05 ppm, min_match_peaks=3). Compare the two strategies side-by-side: a strategy is superior if it fragments more chemicals with comparable or higher intensity without sacrificing MS1 specificity.

## Related tools

- **VIMMS** (Core simulation framework for running fragmentation controllers (TopNController, WeightedDEWController) against virtual chemical mixtures and capturing EvaluationData and mzML output) — https://github.com/glasgowcompbio/vimms
- **OpenMS** (Processes mzML output from simulation to compute fragmentation coverage and peak-picking metrics using MZMine parameters)
- **Python** (Script environment for loading EvaluationData pickles, invoking evaluate_simulated_env(), and computing side-by-side metric comparison tables)
- **Poetry** (Dependency manager for VIMMS installation and version control) — https://python-poetry.org/

## Examples

```
from vimms.Common import POSITIVE, ROI_EXCLUSION_WEIGHTED_DEW; from vimms.Env import Environment; env = Environment(ms, controller, min_time=0, max_time=1440, save_eval=True, out_file='eval_data.p', out_dir='./results'); env.run(); env.write_mzML(); eval_data = pickle.load(open('eval_data.p', 'rb')); coverage, intensity = evaluate_simulated_env(eval_data)
```

## Evaluation signals

- EvaluationData objects successfully load from both controller runs and contain non-empty times_fragmented_summary and cumulative_intensity fields.
- mzML files are valid (parseable by OpenMS or pyteomics) and contain matching MS1 and MS2 scan counts for both controllers.
- Peak-picked spectral library matches reference GNPS/HMDB entries with ≥3 matching peaks and cosine similarity traceable in output report.
- Coverage metric (% of chemicals fragmented) differs between the two controllers by ≥5% or shows measurable rank change in top-N fragmented compounds.
- Cumulative intensity profile shows monotonic increase over time with no negative jumps, and sums match expected total ion current range for the chemical mixture.

## Limitations

- Evaluation depends heavily on accurate reference library (GNPS, HMDB); missing or low-quality entries reduce coverage sensitivity.
- Peak-picking parameters (MZMine thresholds) are empirically tuned and may not transfer across different m/z ranges or ionization modes.
- Simulated evaluation does not account for instrument tuning, column fouling, or matrix suppression effects seen in real LC-MS/MS runs.
- Comparison is valid only when both controllers operate under identical chemical mixtures, MS configuration, and time windows; mismatched parameters invalidate ranking.

## Evidence

- [other] The ViMMS framework supports toggling WeightedDEW exclusion as an alternative to TopN fragmentation strategies, enabling comparative evaluation through captured EvaluationData pickles and mzML output.: "The ViMMS framework supports toggling WeightedDEW exclusion as an alternative to TopN fragmentation strategies, enabling comparative evaluation through captured EvaluationData pickles and mzML output."
- [other] Load the pickled EvaluationData object and compute coverage and intensity metrics using evaluate_simulated_env(), comparing times_fragmented_summary and cumulative intensity against the baseline TopN result.: "Load the pickled EvaluationData object and compute coverage and intensity metrics using evaluate_simulated_env(), comparing times_fragmented_summary and cumulative intensity against the baseline TopN"
- [other] Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS: "Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS"
- [other] The evaluation helpers rely on peak picking using MZMine parameters defined in `PeakPicking.py`: "The evaluation helpers rely on peak picking using MZMine parameters defined in `PeakPicking.py`"
- [results] Filter spectra matching with MS1 tolerance 1 ppm, MS2 tolerance 0.05 ppm, minimum 3 matching peaks: "matching_ms1_tol = 1, matching_ms2_tol = 0.05, matching_min_match_peaks = 3"
- [readme] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
