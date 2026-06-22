---
name: tandem-mass-spectrometry-fragmentation-simulation
description: Use when you have a new fragmentation acquisition strategy (e.g., a weighted exclusion variant, alternative TopN ranking, or dynamic isolation window rule) that you wish to evaluate without access to real mass spectrometry hardware.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - Poetry
  - VIMMS
  - OpenMS
  techniques:
  - LC-MS
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

# tandem-mass-spectrometry-fragmentation-simulation

## Summary

Simulate and compare data-dependent acquisition (DDA) fragmentation strategies in LC-MS/MS using a virtual mass spectrometer framework (ViMMS) before testing on real equipment. This skill enables rapid prototyping, evaluation, and optimization of MS/MS scan-level control policies by generating synthetic LC-MS/MS data and computing coverage and intensity metrics against baseline strategies.

## When to use

You have a new fragmentation acquisition strategy (e.g., a weighted exclusion variant, alternative TopN ranking, or dynamic isolation window rule) that you wish to evaluate without access to real mass spectrometry hardware. ViMMS simulation is particularly valuable when you want to compare acquisition metrics (e.g., times_fragmented_summary, cumulative intensity, fragmentation coverage) across multiple controllers using identical virtual chemical populations and controlled acquisition parameters.

## When NOT to use

- You are analyzing real acquired LC-MS/MS data and need to extract metabolites or assign chemical identities; use peak-picking and compound database matching instead.
- You need to simulate instrument hardware behavior (detector noise, calibration drift, ion suppression) beyond scan-level acquisition logic; ViMMS focuses on fragmentation strategy simulation, not hardware physics.
- Your fragmentation strategy depends on external real-time feedback (e.g., live mass calibration, dynamic threshold updates from instrument response); ViMMS operates in batch simulation mode.

## Inputs

- Virtual chemical population (list of Chemical objects with m/z, retention time, and intensity properties)
- Formula sampler specification (min_mz, max_mz range and sampling strategy)
- MS polarity setting (POSITIVE or NEGATIVE)
- Fragmentation controller configuration (isolation_width, N, mz_tol, rt_tol, min_ms1_intensity)
- Simulation time bounds (min_time, max_time in seconds)

## Outputs

- mzML file (serialized scan list with MS1 and MS/MS spectra)
- EvaluationData pickle object (scan metadata, fragmentation coverage, intensity summaries)
- Comparative metrics: times_fragmented_summary, cumulative intensity distributions

## How to apply

First, generate a population of virtual chemicals using a formula sampler (e.g., UniformMZFormulaSampler for uniform m/z range 100–500) and instantiate them via ChemicalMixtureCreator with multiple MS levels. Second, create an IndependentMassSpectrometer with the desired polarity (POSITIVE or NEGATIVE) and chemical list. Third, instantiate your fragmentation controller (e.g., WeightedDEWController with use_weighteddew_exclusion=True, setting isolation_width, N (top-N parameter), mz_tol, rt_tol, and min_ms1_intensity thresholds). Fourth, create an Environment with save_eval=True to enable EvaluationData collection, specify output file and directory paths, then execute env.run() to drive the simulation loop and capture all scans with controller-weighted acquisition decisions. Fifth, call env.write_mzML() to serialize the acquired scans to mzML format. Finally, load the pickled EvaluationData object and compute coverage and intensity metrics using evaluate_simulated_env(), comparing times_fragmented_summary and cumulative intensity distributions against your baseline controller (e.g., TopNController) to quantify performance differences.

## Related tools

- **VIMMS** (Core simulation framework: instantiates virtual mass spectrometer, executes Environment loop, applies controller logic to generate MS/MS scans, exports mzML and EvaluationData) — https://github.com/glasgowcompbio/vimms
- **Python** (Language for scripting chemical generation, controller instantiation, Environment execution, and metric computation)
- **Poetry** (Dependency management for ViMMS development environment) — https://python-poetry.org/
- **OpenMS** (Post-simulation processing of mzML output to compute fragmentation coverage metrics)

## Examples

```
from vimms.Common import POSITIVE
from vimms.ChemicalSampler import UniformMZFormulaSampler, ChemicalMixtureCreator
from vimms.MassSpectrometer import IndependentMassSpectrometer
from vimms.Controller import WeightedDEWController
from vimms.Environment import Environment

formula_sampler = UniformMZFormulaSampler(min_mz=100, max_mz=500)
cmc = ChemicalMixtureCreator(formula_sampler)
chemicals = cmc.sample(100, ms_levels=2)
ms = IndependentMassSpectrometer(polarity=POSITIVE, chemicals=chemicals)
controller = WeightedDEWController(polarity=POSITIVE, use_weighteddew_exclusion=True, isolation_width=1, N=3, mz_tol=10, rt_tol=15, min_ms1_intensity=1.75E5)
env = Environment(ms, controller, min_time=0, max_time=1440, save_eval=True, out_file='output.pkl', out_dir='.')
env.run()
env.write_mzML('output.mzML')
```

## Evaluation signals

- EvaluationData pickle is successfully generated and contains non-empty times_fragmented_summary and cumulative intensity arrays with expected numeric ranges (non-negative, comparable across controllers).
- mzML output file is well-formed XML, parseable by external tools (e.g., OpenMS, mzmine), and contains expected MS1 and MS/MS scan counts matching the controller's acquisition decisions.
- Comparative metrics (e.g., fragmentation coverage, times_fragmented_summary distributions) differ measurably between the test controller (e.g., WeightedDEWController with exclusion=True) and baseline (TopNController), demonstrating that the strategy variant produced distinct acquisition behavior.
- All virtual chemicals in the input population are represented in the output scan list (no silent drops or filtering artifacts); check that the number of unique precursor m/z values in mzML matches the input chemical population size.
- Fragmentation coverage computed via OpenMS peak-picking on mzML output is consistent with ViMMS-reported fragmentation metrics, validating that simulation acquisition decisions were correctly serialized.

## Limitations

- ViMMS simulates fragmentation decisions at scan level but does not model hardware physics (detector saturation, charge state multiplicity, ion suppression, or calibration drift); simulated intensity distributions may not fully replicate real instrument behavior.
- Peak-picking and evaluation rely on MZMine parameters defined in PeakPicking.py; results are sensitive to these hyperparameters and may not match real peak-picking software if parameters differ.
- Virtual chemical populations are generated synthetically (e.g., from uniform m/z sampling or HMDB database sampling); they may not capture coelution patterns, isotope distributions, or adduct complexity observed in real biological samples.
- No changelog was found in the repository, limiting visibility into breaking API changes between ViMMS versions.

## Evidence

- [intro] devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment: "devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment"
- [intro] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
- [other] The ViMMS framework supports toggling WeightedDEW exclusion as an alternative to TopN fragmentation strategies, enabling comparative evaluation through captured EvaluationData pickles and mzML output.: "The ViMMS framework supports toggling WeightedDEW exclusion as an alternative to TopN fragmentation strategies, enabling comparative evaluation through captured EvaluationData pickles and mzML output"
- [other] Instantiate an IndependentMassSpectrometer with polarity=POSITIVE and the generated chemicals list.: "Instantiate an IndependentMassSpectrometer with polarity=POSITIVE and the generated chemicals list"
- [other] Execute env.run() to drive the simulation loop and capture all scans with exclusion-weighted acquisition decisions.: "Execute env.run() to drive the simulation loop and capture all scans with exclusion-weighted acquisition decisions"
- [other] Call env.write_mzML() to serialize the scan list to mzML format.: "Call env.write_mzML() to serialize the scan list to mzML format"
- [readme] ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment. You can generate new LC-MS/MS data based on empirical data or virtually replay a previous LC-MS/MS analysis using existing data, which allows for testing different fragmentation strategies.: "ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment. You can generate new LC-MS/MS data based on empirical data or virtually replay a previous"
