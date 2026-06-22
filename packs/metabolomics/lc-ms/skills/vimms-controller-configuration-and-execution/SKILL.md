---
name: vimms-controller-configuration-and-execution
description: Use when you have a set of chemical compounds (with known retention times and intensities) loaded into a ViMMS IndependentMassSpectrometer and need to simulate a specific MS/MS fragmentation strategy (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - VIMMS
  - Python
  - Poetry
  - OpenMS
  techniques:
  - LC-MS
derived_from:
- doi: 10.21105/joss.03990
  title: vimms
- doi: 10.1021/acs.analchem.0c03895
  title: ''
evidence_spans:
- a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics
- a flexible and modular framework designed to simulate fragmentation strategies
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

# ViMMS Controller Configuration and Execution

## Summary

Configure and execute a ViMMS controller to simulate MS/MS fragmentation acquisition strategies on a virtual mass spectrometer, then export the resulting scan data as mzML files. This skill bridges the gap between strategy design and evaluation by enabling rapid prototyping of data-dependent or data-independent acquisition methods without access to real MS hardware.

## When to use

You have a set of chemical compounds (with known retention times and intensities) loaded into a ViMMS IndependentMassSpectrometer and need to simulate a specific MS/MS fragmentation strategy (e.g., data-dependent acquisition, full-scan MS1, or targeted acquisition) over a defined LC-MS run window. Use this skill when you want to test how a chosen acquisition controller will behave on your chemical mixture and generate reproducible MS/MS scan data for downstream evaluation.

## When NOT to use

- You need to simulate fragmentation on a real instrument—use IAPI integration instead for live hardware control.
- Your chemical list has fewer than 10 compounds or spans less than 30 seconds of LC time—simulation overhead may not justify the execution cost.
- You already have experimental mzML files and want to replay them—use ChemicalMixtureFromMZML to extract chemicals first, then re-simulate with different controllers.

## Inputs

- IndependentMassSpectrometer instance with loaded chemical compounds
- Controller class configured with fragmentation strategy parameters (polarity, isolation width, N, etc.)
- LC-MS run time bounds (min_time and max_time in seconds)

## Outputs

- mzML file containing all acquired MS1 and MS/MS scans
- Environment object with evaluation metrics (if save_eval=True)

## How to apply

First, instantiate a controller class (e.g., FullScanController, TopNController, or a custom subclass) with polarity and strategy-specific parameters such as isolation width and N value. Create an Environment object, passing the mass spectrometer, controller, and LC-MS time bounds (min_time and max_time in seconds); enable save_eval=True to collect evaluation metrics during acquisition. Call env.run() to execute the acquisition loop, which iteratively calls the controller's next_scan() method and updates the mass spectrometer state. After execution completes, invoke Environment.write_mzML() to serialize all acquired scans into mzML format, which can then be processed by external tools (e.g., OpenMS) for fragmentation coverage analysis or spectral matching.

## Related tools

- **VIMMS** (Core framework providing Environment, Controller, and MassSpectrometer classes for LC-MS/MS simulation and mzML export) — https://github.com/glasgowcompbio/vimms
- **OpenMS** (Post-processing tool to compute fragmentation coverage metrics from exported mzML files)
- **Python** (Language runtime for instantiating and executing ViMMS controllers and Environment)
- **Poetry** (Dependency manager for installing ViMMS and its dependencies) — https://python-poetry.org/

## Examples

```
from vimms.Common import POSITIVE
from vimms.MassSpec import IndependentMassSpectrometer
from vimms.Controller import TopNController
from vimms.Environment import Environment

controller = TopNController(POSITIVE, N=5, isolation_width=1)
env = Environment(ms, controller, min_time=0, max_time=1200, save_eval=True)
env.run()
env.write_mzML('output_scans.mzML')
```

## Evaluation signals

- mzML file is valid and readable by external tools (e.g., OpenMS, mzmine); file contains expected number of scans matching run time and dwell time parameters.
- All acquired scans have correct polarity, m/z range, and retention time values consistent with the input chemical mixture and time bounds.
- MS/MS scans include correct precursor m/z, isolation window width, and fragmentation intensity distributions aligned with controller's isolation_width and energy settings.
- save_eval=True produces a metrics dictionary with scan counts, ROI detection rates, and other fragmentation coverage statistics that are > 0 and < total compound count.
- Comparison of two controllers on the same chemical mixture produces different fragmentation patterns (e.g., different precursor selections or scan depths) in their respective mzML outputs, confirming controller logic is being applied.

## Limitations

- Simulation assumes perfect ion transmission and detector response; does not model real instrument artifacts such as space charge effects, thermal noise, or baseline drift.
- Chemical ionization is modeled as a simple mixture-level intensity distribution; adduct formation and in-source fragmentation are not simulated.
- Controller decision logic is executed at each scan, but inter-scan timing and queue buffering are simplified; real instrument constraints (e.g., minimum dwell time, trigger latency) are not enforced.
- mzML export via Environment.write_mzML() may require external tools (e.g., OpenMS) for post-processing to compute standard metrics like fragmentation coverage or MS/MS quality scores.

## Evidence

- [other] 3. Choose a controller for fragmentation strategy  [section=other; evidence='# 3. Choose a controller
controller = TopNController("positive", N=5, isolation_width=1)']: "Choose a controller
controller = TopNController("positive", N=5, isolation_width=1)"
- [other] 4. Create and run the environment  [section=other; evidence='# 4. Create and run the environment
env = Environment(ms, controller, min_time=0, max_time=1200)
env.run()']: "Create and run the environment
env = Environment(ms, controller, min_time=0, max_time=1200)
env.run()"
- [other] 5. Write mzML output  [section=other; evidence='The `Environment` class provides `write_mzML` to export the generated scans']: "The `Environment` class provides `write_mzML` to export the generated scans"
- [other] 6. Enable evaluation data collection  [section=other; evidence='When running an `Environment` you can enable the `save_eval` flag']: "When running an `Environment` you can enable the `save_eval` flag"
- [readme] Key Features from README: 'ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment. You can generate new LC-MS/MS data based on empirical data or virtually replay a previous LC-MS/MS analysis using existing data, which allows for testing different fragmentation strategies.': "ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment. You can generate new LC-MS/MS data based on empirical data or virtually replay a previous"
- [intro] Introduction context: 'devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment': "devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment"
