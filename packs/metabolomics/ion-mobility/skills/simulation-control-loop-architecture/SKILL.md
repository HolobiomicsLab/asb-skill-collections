---
name: simulation-control-loop-architecture
description: Use when you have a set of metabolites or chemical formulas to analyze and want to evaluate how different MS/MS fragmentation strategies (e.g., TopN, exclusion lists, dynamic window selection) would perform without access to real instrument time.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - ViMMS
  - UniformMZFormulaSampler / DatabaseFormulaSampler
  - ChemicalMixtureCreator
  - TopNController
  - OpenMS
  - Python 3+
  techniques:
  - LC-MS
  - ion-mobility-MS
derived_from:
- doi: 10.21105/joss.03990
  title: vimms
- doi: 10.1021/acs.analchem.0c03895
  title: ''
evidence_spans:
- ViMMS is compatible with Python 3+
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

# Simulation Control Loop Architecture

## Summary

Set up and execute a complete virtual mass spectrometry control loop by orchestrating three core components—chemical sample generators, a simulated mass spectrometer, and a fragmentation strategy controller—within a time-bounded Environment to produce realistic MS/MS scan data. This skill is essential for prototyping and testing data-dependent acquisition (DDA) strategies before instrument deployment.

## When to use

You have a set of metabolites or chemical formulas to analyze and want to evaluate how different MS/MS fragmentation strategies (e.g., TopN, exclusion lists, dynamic window selection) would perform without access to real instrument time. Use this when you need to generate synthetic LC-MS/MS data to compare acquisition strategies, benchmark peak coverage, or optimize controller parameters (isolation width, m/z tolerance, intensity thresholds) in a reproducible virtual environment.

## When NOT to use

- You have real LC-MS/MS data already acquired and want to reprocess it with a different peak-picking or feature detection method (use ChemicalMixtureFromMZML instead, not full simulation).
- Your goal is to simulate ion mobility or other orthogonal separation dimensions not yet implemented in ViMMS.
- You need to model retention-time prediction or chromatographic interactions; ViMMS assumes uniform or simplified RT distributions and does not include explicit LC simulation.

## Inputs

- Chemical formula sampler configuration (e.g., UniformMZFormulaSampler or DatabaseFormulaSampler with min_mz, max_mz, polarity)
- MS levels specification (MS1, MS2, or both)
- Fragmentation strategy controller parameters (N, isolation_width, m/z tolerance, retention-time tolerance, MS1 intensity threshold)
- Time bounds for the Environment (min_time, max_time in seconds)

## Outputs

- Scans list (list of MS1 and MS2 scan records with m/z, intensity, retention time, and fragmentation metadata)
- mzML file (standard mass spectrometry data interchange format suitable for downstream peak picking and spectral matching)
- Coverage metrics (fragmentation events matched to precursor ions; evaluated via OpenMS or equivalent)

## How to apply

First, generate a population of virtual chemicals by sampling from a formula database (e.g., HMDB via DatabaseFormulaSampler) or direct m/z range (e.g., UniformMZFormulaSampler with min_mz=100, max_mz=500 Da) and request both MS1 and MS2 scan levels via ChemicalMixtureCreator. Second, instantiate an IndependentMassSpectrometer with the chemical list and specify ionization polarity (positive or negative). Third, configure a fragmentation strategy controller (e.g., TopNController with N fragments per survey scan, isolation_width in Da, m/z tolerance in ppm, and MS1 intensity threshold such as 1.75E5) to govern which precursor ions are selected and fragmented. Fourth, create an Environment orchestrator spanning your desired retention-time window (e.g., 0–1440 s), attach both the mass spectrometer and controller, and call env.run() to execute the fixed simulation loop. Finally, export the resulting scans list as mzML via write_mzML() for downstream evaluation (e.g., peak picking, spectral matching, coverage analysis).

## Related tools

- **ViMMS** (Core orchestration framework providing Environment, IndependentMassSpectrometer, and fragmentation strategy controllers (TopNController, etc.) for simulating MS/MS acquisition loops) — https://github.com/glasgowcompbio/vimms
- **UniformMZFormulaSampler / DatabaseFormulaSampler** (Chemical formula and m/z sampling engines for populating the virtual chemical space (e.g., from HMDB)) — https://github.com/glasgowcompbio/vimms
- **ChemicalMixtureCreator** (Batch generation of chemical objects with specified MS levels (MS1, MS2) and ionization polarity) — https://github.com/glasgowcompbio/vimms
- **TopNController** (Fragmentation strategy implementation for selecting top-N precursor ions per survey scan with configurable isolation width, m/z tolerance, and intensity thresholds) — https://github.com/glasgowcompbio/vimms
- **OpenMS** (Post-simulation evaluation tool for peak picking and computation of fragmentation coverage from mzML output)
- **Python 3+** (Execution runtime for ViMMS and integration of simulation pipeline)

## Examples

```
from vimms.ChemicalSamplers import UniformMZFormulaSampler, ChemicalMixtureCreator
from vimms.MassSpectrometer import IndependentMassSpectrometer
from vimms.Controller import TopNController
from vimms.Environment import Environment

formula_sampler = UniformMZFormulaSampler(min_mz=100, max_mz=500)
cmc = ChemicalMixtureCreator(formula_sampler)
chemicals = cmc.sample(100, ms_levels=2)
ms = IndependentMassSpectrometer(polarity="positive", chemicals=chemicals)
controller = TopNController("positive", N=3, isolation_width=1)
env = Environment(ms, controller, min_time=0, max_time=1440)
env.run()
env.write_mzML("output.mzML")
```

## Evaluation signals

- Non-empty scans list with both MS1 and MS2 records present after env.run()
- mzML file generated via write_mzML() is valid and parseable by OpenMS or standard mass spectrometry software
- MS1 survey scans contain precursor ions within specified m/z range and above intensity threshold (e.g., 1.75E5)
- MS2 scans correspond to TopN-selected precursors with isolation windows matching controller configuration (e.g., ±0.5 Da for 1 Da width)
- Fragmentation coverage (number of unique precursor ions fragmented divided by total chemical population) is consistent with N and retention-time tolerance settings

## Limitations

- ViMMS does not model chromatographic retention time explicitly; chemicals are sampled uniformly across the time window, which oversimplifies real LC dynamics.
- Fragmentation patterns are simulated via a generative model (not always captured from empirical spectra), so synthetic MS2 spectra may not perfectly match real fragmentation behavior.
- Controller logic is fixed during a run; dynamic recalibration or real-time feedback (as on modern instruments) is not currently supported.
- Requires valid chemical database (e.g., HMDB) or sampler configuration; if sampler yields no chemicals in the m/z range or MS level mismatch occurs, the run will produce empty or partial scans.
- No changelog was found in the repository, limiting clarity on API stability across versions.

## Evidence

- [other] The Environment class orchestrates three components: Chemicals are generated via samplers (e.g., DatabaseFormulaSampler), passed to an IndependentMassSpectrometer instance, and controlled by a fragmentation strategy Controller; the Environment runs this loop and produces a scan list via write_mzML output.: "The Environment class orchestrates three components: Chemicals are generated via samplers (e.g., DatabaseFormulaSampler), passed to an IndependentMassSpectrometer instance, and controlled by a"
- [readme] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
- [readme] devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment: "devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment"
- [other] # 1. Generate chemicals
formula_sampler = UniformMZFormulaSampler(min_mz=100, max_mz=600)
cmc = ChemicalMixtureCreator(formula_sampler)
chemicals = cmc.sample(100, ms_levels=2): "formula_sampler = UniformMZFormulaSampler(min_mz=100, max_mz=600)
cmc = ChemicalMixtureCreator(formula_sampler)
chemicals = cmc.sample(100, ms_levels=2)"
- [other] # 2. Set up a virtual mass spectrometer
ms = IndependentMassSpectrometer(polarity="positive", chemicals=chemicals): "ms = IndependentMassSpectrometer(polarity="positive", chemicals=chemicals)"
- [other] # 3. Choose a controller
controller = TopNController("positive", N=5, isolation_width=1): "controller = TopNController("positive", N=5, isolation_width=1)"
- [other] # 4. Create and run the environment
env = Environment(ms, controller, min_time=0, max_time=1200)
env.run(): "env = Environment(ms, controller, min_time=0, max_time=1200)
env.run()"
- [other] The `Environment` class provides `write_mzML` to export the generated scans: "The `Environment` class provides `write_mzML` to export the generated scans"
