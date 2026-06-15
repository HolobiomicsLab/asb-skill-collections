---
name: dynamic-exclusion-weighting-strategy-evaluation
description: Use when you have prototyped a novel data-dependent acquisition strategy that uses dynamic exclusion with intensity or ROI weighting, and you need to quantitatively compare its MS/MS coverage and intensity performance against a simpler baseline (TopN) before testing on real instrumentation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3699
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3047
  tools:
  - Python
  - Poetry
  - ViMMS
  - OpenMS
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_vimms
    doi: 10.21105/joss.03990
    title: vimms
  dedup_kept_from: coll_vimms
schema_version: 0.2.0
---

# dynamic-exclusion-weighting-strategy-evaluation

## Summary

Evaluate how weighted dynamic exclusion fragmentation strategies (e.g., WeightedDEWController) compare to baseline TopN acquisition in LC-MS/MS by running parallel simulations through the ViMMS framework and measuring coverage and intensity metrics on the resulting mzML and EvaluationData outputs.

## When to use

You have prototyped a novel data-dependent acquisition strategy that uses dynamic exclusion with intensity or ROI weighting, and you need to quantitatively compare its MS/MS coverage and intensity performance against a simpler baseline (TopN) before testing on real instrumentation. Use this when you have a virtual chemical mixture, a candidate controller implementation, and access to ViMMS Environment simulation.

## When NOT to use

- You do not have a working implementation of your candidate controller ready to run in ViMMS — use this skill only after validation that your controller class instantiates and runs without errors.
- Your goal is to evaluate a single acquisition strategy in isolation, not to compare strategies — the skill is specifically designed for comparative evaluation.
- Input chemicals are not representative of your target analyte set (e.g., generated from a different m/z range or database than intended) — results will not transfer to real data.

## Inputs

- chemical_mixture (list of Chemical objects with m/z, RT, intensity, MS levels)
- IndependentMassSpectrometer instance (polarity, chemicals)
- WeightedDEWController instance (strategy parameters: use_weighteddew_exclusion, isolation_width, N, mz_tol, rt_tol, min_ms1_intensity)
- TopNController instance (baseline parameters: N, isolation_width, polarity)
- Environment simulation parameters (min_time, max_time)

## Outputs

- mzML files (one per controller, containing all scans with acquisition metadata)
- EvaluationData pickle objects (one per controller, with times_fragmented_summary, cumulative intensity, scan-level statistics)
- comparative metrics (e.g., fragmentation coverage %, total intensity acquired, ROI completeness)

## How to apply

Instantiate two parallel simulation runs in ViMMS: one using your experimental WeightedDEWController with parameters like use_weighteddew_exclusion=True, isolation_width, N (number of precursors), mz_tol, rt_tol, and min_ms1_intensity (e.g., 1.75E5), and a second using a TopNController baseline with identical chemical input and acquisition window. Run both through an Environment with save_eval=True to capture EvaluationData pickles and mzML output. Load both pickled EvaluationData objects and compare times_fragmented_summary (fragmentation coverage) and cumulative intensity metrics using evaluate_simulated_env(). Differences in coverage and intensity distributions directly indicate whether the weighting scheme improves or degrades acquisition performance relative to the baseline.

## Related tools

- **ViMMS** (Core simulation framework: instantiate Environment, WeightedDEWController, IndependentMassSpectrometer; execute env.run() to drive the acquisition loop; export mzML and evaluate_simulated_env() to compare metrics.) — https://github.com/glasgowcompbio/vimms
- **Python** (Host language for instantiating controllers, running Environment loops, loading EvaluationData pickles, and computing comparative metrics.)
- **Poetry** (Dependency and environment manager for ViMMS installation and development setup.) — https://python-poetry.org/
- **OpenMS** (Post-processing of mzML output to compute fragmentation coverage metrics using external peak-picking and spectral matching.)

## Examples

```
from vimms.Common import POSITIVE; from vimms.ChemicalSamplers import UniformMZFormulaSampler; from vimms.MassSpectrometer import IndependentMassSpectrometer; from vimms.Controllers import WeightedDEWController, TopNController; from vimms.Environment import Environment; sampler = UniformMZFormulaSampler(100, 500); chemicals = sampler.sample(100); ms = IndependentMassSpectrometer(POSITIVE, chemicals); dew_ctrl = WeightedDEWController(POSITIVE, N=3, mz_tol=10, rt_tol=15, min_ms1_intensity=1.75E5, use_weighteddew_exclusion=True); env_dew = Environment(ms, dew_ctrl, min_time=0, max_time=1440, save_eval=True); env_dew.run(); env_dew.write_mzML('dew_output.mzML')
```

## Evaluation signals

- Both controller runs complete without runtime errors and produce valid mzML files with identical scan count structure.
- EvaluationData pickle files load successfully and contain non-empty times_fragmented_summary and cumulative intensity arrays for both controllers.
- Fragmentation coverage (times_fragmented_summary) and intensity metrics are numerically comparable (same units, overlapping range) between the two controller results.
- The weighted controller shows measurably different (higher or lower) coverage or intensity than the baseline TopN controller, confirming that the weighting scheme is being applied during acquisition decisions.
- Peak-picking and spectral matching (if using OpenMS) yield consistent ROI completeness and matching confidence scores across both controller outputs.

## Limitations

- Virtual simulation does not capture instrument-specific artifacts (e.g., quadrupole transmission efficiency, thermal noise, detector saturation) that may alter ranking in real MS/MS acquisition.
- Comparison depends critically on identical chemical mixture input and identical acquisition window (min_time, max_time); mismatched parameters will confound results.
- EvaluationData metrics rely on accurate peak-picking parameters (MZMine settings); different MZMine configurations may yield different coverage conclusions from the same mzML.
- WeightedDEWController performance is sensitive to parameter choices (isolation_width, mz_tol, rt_tol, min_ms1_intensity); results may not generalize to different thresholds or biological contexts.

## Evidence

- [other] The ViMMS framework supports toggling WeightedDEW exclusion as an alternative to TopN fragmentation strategies, enabling comparative evaluation through captured EvaluationData pickles and mzML output.: "The ViMMS framework supports toggling WeightedDEW exclusion as an alternative to TopN fragmentation strategies, enabling comparative evaluation through captured EvaluationData pickles and mzML output."
- [other] Create a WeightedDEWController instance with use_weighteddew_exclusion=True, setting isolation_width=1, N=3, mz_tol=10, rt_tol=15, and min_ms1_intensity=1.75E5.: "Create a WeightedDEWController instance with use_weighteddew_exclusion=True, setting isolation_width=1, N=3, mz_tol=10, rt_tol=15, and min_ms1_intensity=1.75E5."
- [other] Execute env.run() to drive the simulation loop and capture all scans with exclusion-weighted acquisition decisions.: "Execute env.run() to drive the simulation loop and capture all scans with exclusion-weighted acquisition decisions."
- [other] Load the pickled EvaluationData object and compute coverage and intensity metrics using evaluate_simulated_env(), comparing times_fragmented_summary and cumulative intensity against the baseline TopN result.: "Load the pickled EvaluationData object and compute coverage and intensity metrics using evaluate_simulated_env(), comparing times_fragmented_summary and cumulative intensity against the baseline TopN"
- [readme] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
- [other] When running an Environment you can enable the save_eval flag: "When running an Environment you can enable the save_eval flag"
