---
name: data-dependent-acquisition-controller-implementation
description: Use when you have a conceptual MS/MS fragmentation strategy (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
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

# data-dependent-acquisition-controller-implementation

## Summary

Implement and configure a data-dependent acquisition (DDA) controller within the ViMMS simulation framework to prototype and evaluate MS/MS fragmentation strategies before testing on real mass spectrometry hardware. This skill enables rapid iteration of acquisition logic (e.g., TopN, WeightedDEW) with controlled parameters and comparative evaluation via mzML output and EvaluationData metrics.

## When to use

You have a conceptual MS/MS fragmentation strategy (e.g., select top N ions by intensity, apply weighted exclusion to balance coverage and dynamic exclusion) and want to prototype it in silico, measure its coverage and intensity performance against a baseline, and generate reproducible simulation results without requiring access to real mass spectrometry instrumentation.

## When NOT to use

- You already have real LC-MS/MS data from hardware and do not need to prototype new strategies before acquisition.
- Your fragmentation strategy is not implementable as a deterministic controller (e.g., requires real-time external sensor feedback or hardware-specific API calls like IAPI).
- You need to simulate ion suppression, space-charge effects, or other instrument physics not modeled by IndependentMassSpectrometer.

## Inputs

- chemical list (list of Chemical objects with m/z, RT, intensity, formula)
- controller configuration (class name, parameters: N, isolation_width, mz_tol, rt_tol, min_ms1_intensity)
- simulation parameters (polarity, min_time, max_time in seconds)
- baseline controller results (optional, for comparative evaluation)

## Outputs

- mzML file (serialized MS1 and MS/MS scans from simulation)
- EvaluationData pickle object (scan-level metadata, fragmentation decisions, coverage metrics)
- coverage and intensity summary metrics (times_fragmented_summary, cumulative intensity, scan counts)

## How to apply

First, instantiate a virtual mass spectrometer (IndependentMassSpectrometer) with a defined list of chemical analytes (generated via formula samplers or extracted from real mzML files) and polarity setting. Second, create a controller instance (e.g., WeightedDEWController or TopNController) with your chosen fragmentation logic and tunable parameters: isolation width, N (number of precursors), m/z tolerance, RT tolerance, and MS1 intensity threshold (e.g., min_ms1_intensity=1.75E5). Third, instantiate an Environment with the mass spectrometer, controller, and simulation time bounds (min_time, max_time in seconds; e.g., 0–1440 s), enable save_eval=True to capture evaluation metadata. Fourth, execute env.run() to simulate the full acquisition loop, which iterates through retention time, calls the controller to make fragmentation decisions, and accumulates scans. Fifth, export the result to mzML via env.write_mzML() and load the pickled EvaluationData object to compute coverage metrics (times_fragmented_summary, cumulative intensity) and compare against baseline results using evaluate_simulated_env(). The rationale is that tunable parameters like isolation_width, N, and intensity threshold directly shape which precursors are fragmented; simulating multiple configurations allows you to optimize before hardware deployment.

## Related tools

- **ViMMS** (Provides the Environment, IndependentMassSpectrometer, and controller base classes (TopNController, WeightedDEWController) to instantiate and run the DDA simulation loop, plus mzML export and EvaluationData capture.) — https://github.com/glasgowcompbio/vimms
- **Poetry** (Dependency and environment management for ViMMS project setup.) — https://python-poetry.org/
- **Python** (Programming language for instantiating controller objects, configuring parameters, and executing the simulation.)
- **OpenMS** (Post-simulation peak picking and fragmentation coverage calculation from mzML output to evaluate controller performance.)

## Examples

```
from vimms.Common import POSITIVE
from vimms.ChemicalSamplers import UniformMZFormulaSampler
from vimms.MixtureCreator import ChemicalMixtureCreator
from vimms.MassSpectrometer import IndependentMassSpectrometer
from vimms.Controller import WeightedDEWController
from vimms.Environment import Environment

formula_sampler = UniformMZFormulaSampler(min_mz=100, max_mz=500)
cmc = ChemicalMixtureCreator(formula_sampler)
chemicals = cmc.sample(100, ms_levels=2)
ms = IndependentMassSpectrometer(polarity=POSITIVE, chemicals=chemicals)
controller = WeightedDEWController(polarity=POSITIVE, N=3, isolation_width=1, mz_tol=10, rt_tol=15, min_ms1_intensity=1.75E5, use_weighteddew_exclusion=True)
env = Environment(ms, controller, min_time=0, max_time=1440, save_eval=True, out_file='sim_output.mzML', out_dir='./results')
env.run()
env.write_mzML()
```

## Evaluation signals

- mzML file is valid and contains expected MS1 and MS/MS scan count consistent with controller decisions and retention time range.
- EvaluationData pickle loads without error and contains non-empty times_fragmented_summary (fragmentation count per retention time bin) and cumulative intensity tracks.
- Comparison metrics (coverage %, cumulative intensity) between implemented controller and baseline TopN show expected directional differences (e.g., WeightedDEW with exclusion should show broader coverage but lower peak intensity than TopN with N=5).
- All fragmented precursor m/z values fall within expected isolation window range around selected parent ion (isolation_width ± tolerance).
- Fragmentation decisions respect defined thresholds: no MS/MS triggered on precursor intensity < min_ms1_intensity, and retention time or m/z exclusion duration matches configured rt_tol and mz_tol.

## Limitations

- IndependentMassSpectrometer models idealized instrument behavior and does not simulate ion suppression, space-charge effects, or detector saturation; real hardware may show degraded coverage at high sample complexity.
- Controller logic must be implemented as Python code within the ViMMS framework; integration with external real-time feedback (e.g., IAPI Thermo Tribrid control) requires custom bridging not provided by the framework.
- EvaluationData metrics depend on accurate peak picking and ROI detection parameters (MZMine-style thresholds); suboptimal min_roi_intensity or min_roi_length may underestimate or overestimate coverage.
- Simulation assumes uniform or sampled chemical background; real LC-MS/MS runs contain co-eluting contaminants and matrix effects that affect precursor intensity and ionization efficiency.
- Time complexity scales with chemical count and simulation duration; very large chemical lists (>10,000) or long runs (>3600 s) may require parallelization or sampling to complete in reasonable wall-clock time.

## Evidence

- [readme] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
- [other] Instantiate a WeightedDEWController instance with use_weighteddew_exclusion=True, setting isolation_width=1, N=3, mz_tol=10, rt_tol=15, and min_ms1_intensity=1.75E5: "Create a WeightedDEWController instance with use_weighteddew_exclusion=True, setting isolation_width=1, N=3, mz_tol=10, rt_tol=15, and min_ms1_intensity=1.75E5"
- [other] Instantiate an Environment with the mass spectrometer, controller, min_time=0, max_time=1440, save_eval=True, and specify out_file and out_dir parameters. Execute env.run() to drive the simulation loop: "Instantiate an Environment with the mass spectrometer, controller, min_time=0, max_time=1440, save_eval=True, and specify out_file and out_dir parameters. Execute env.run() to drive the simulation"
- [other] Call env.write_mzML() to serialize the scan list to mzML format. Load the pickled EvaluationData object and compute coverage and intensity metrics using evaluate_simulated_env(): "Call env.write_mzML() to serialize the scan list to mzML format. Load the pickled EvaluationData object and compute coverage and intensity metrics using evaluate_simulated_env()"
- [intro] devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment: "devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment"
- [readme] ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment. You can generate new LC-MS/MS data based on empirical data or virtually replay a previous LC-MS/MS analysis using existing data, which allows for testing different fragmentation strategies.: "ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment. You can generate new LC-MS/MS data based on empirical data or virtually replay a previous"
