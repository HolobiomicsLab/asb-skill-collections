---
name: lc-ms-scan-acquisition-orchestration
description: Use when when you have a curated list of chemical compounds (real or
  virtual), a defined fragmentation strategy (e.g., Top-N, exclusion lists), and need
  to simulate how that strategy will acquire MS1 and MS2 scans over a defined retention-time
  window.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - ViMMS
  - UniformMZFormulaSampler
  - DatabaseFormulaSampler
  - ChemicalMixtureCreator
  - TopNController
  - Environment
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

# LC-MS Scan Acquisition Orchestration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Orchestrate a complete tandem mass spectrometry (MS/MS) simulation control loop by coupling a virtual mass spectrometer, chemical library, and fragmentation strategy controller within an Environment instance. This skill enables rapid prototyping and evaluation of data-dependent acquisition (DDA) strategies before testing on real LC-MS/MS hardware.

## When to use

When you have a curated list of chemical compounds (real or virtual), a defined fragmentation strategy (e.g., Top-N, exclusion lists), and need to simulate how that strategy will acquire MS1 and MS2 scans over a defined retention-time window. Use this skill to generate synthetic mzML scan data and assess whether your controller and isolation parameters will achieve desired fragmentation coverage without access to physical instrumentation.

## When NOT to use

- You are testing acquisition directly on physical LC-MS/MS hardware (use this skill only for simulation prior to instrument time).
- Your chemical library is empty or contains no compounds in the target m/z range (filter and validate chemicals before orchestration).
- You need real-time instrument control or closed-loop feedback (VIMMS is a simulation framework, not a live instrument driver).

## Inputs

- Chemical compound list with m/z, intensity, and fragmentation properties (output of ChemicalMixtureCreator or ChemicalMixtureFromMZML)
- Fragmentation strategy parameters (isolation window, m/z tolerance, retention-time tolerance, MS1 intensity threshold, Top-N fragment count)
- Ionization mode (positive or negative polarity)

## Outputs

- Scans list containing MS1 and MS2 scan records with m/z, intensity, and fragmentation metadata
- mzML-formatted mass spectrometry data file (via write_mzML()) compatible with downstream peak picking and metabolite matching

## How to apply

Instantiate three core components: (1) Generate virtual chemicals by sampling m/z formulae (e.g., UniformMZFormulaSampler or DatabaseFormulaSampler for empirical HMDB data) across your target mass range, requesting both MS1 and MS2 levels via ChemicalMixtureCreator; (2) Create an IndependentMassSpectrometer instance in your desired polarity (positive or negative) with the chemical list; (3) Configure a Controller (e.g., TopNController) specifying fragmentation parameters: number of fragments per survey scan (N), isolation window width (typically 1 Da), m/z tolerance (e.g., 10 ppm), retention-time tolerance (e.g., 15 s), and MS1 intensity threshold (e.g., 1.75E5). (4) Construct an Environment spanning your desired retention-time range (e.g., 0–1440 s), attach both the mass spectrometer and controller, and invoke env.run() to execute the orchestrated acquisition loop. (5) Export the resulting scan list via write_mzML() and verify that both MS1 and MS2 scan records are present and non-empty.

## Related tools

- **ViMMS** (Core framework providing Environment, IndependentMassSpectrometer, and Controller classes for orchestrating the MS/MS acquisition loop and generating synthetic mzML scans) — https://github.com/glasgowcompbio/vimms
- **UniformMZFormulaSampler** (Chemical formula sampler for generating virtual compounds across a specified m/z range (e.g., 100–500 Da) without empirical data) — https://github.com/glasgowcompbio/vimms
- **DatabaseFormulaSampler** (Chemical formula sampler for generating compounds by sampling from metabolite databases (e.g., HMDB) within a specified m/z window) — https://github.com/glasgowcompbio/vimms
- **ChemicalMixtureCreator** (Utility to batch-generate chemical objects from formula samplers with specified MS levels (MS1, MS2)) — https://github.com/glasgowcompbio/vimms
- **TopNController** (Fragmentation strategy controller implementing data-dependent acquisition by selecting top N most abundant precursors for MS2 fragmentation) — https://github.com/glasgowcompbio/vimms
- **Environment** (Master orchestrator class that coordinates the mass spectrometer and controller over a retention-time window, executes the acquisition loop via env.run(), and exports mzML) — https://github.com/glasgowcompbio/vimms
- **OpenMS** (Post-processing tool to compute fragmentation coverage and validate acquisition results from mzML output)

## Examples

```
from vimms.Common import POSITIVE; from vimms.ChemicalSamplers import UniformMZFormulaSampler, ChemicalMixtureCreator; from vimms.MassSpectrometer import IndependentMassSpectrometer; from vimms.Controller import TopNController; from vimms.Environment import Environment; sampler = UniformMZFormulaSampler(min_mz=100, max_mz=500); cmc = ChemicalMixtureCreator(sampler); chemicals = cmc.sample(100, ms_levels=2); ms = IndependentMassSpectrometer(POSITIVE, chemicals); controller = TopNController(POSITIVE, N=3, isolation_width=1, mz_tol=10, rt_tol=15, min_ms1_intensity=1.75e5); env = Environment(ms, controller, min_time=0, max_time=1440); env.run(); env.write_mzML('output.mzML')
```

## Evaluation signals

- Scans list is non-empty and contains both MS1 and MS2 scan records (schema check).
- All MS1 scans have intensity above the configured threshold (e.g., 1.75E5); all MS2 scans are linked to valid MS1 precursors within m/z tolerance and retention-time window.
- MS2 count equals or approximates N × (number of survey scans), confirming the TopNController is fragmenting the expected number of precursors per cycle.
- mzML output file is valid and parseable by downstream tools (e.g., OpenMS peak picking, MZMine).
- Retention-time span of scans matches the configured Environment window (e.g., 0–1440 s with no gaps or out-of-range records).

## Limitations

- Simulation assumes perfect ionization and no ion suppression effects; intensity profiles are idealized and may not reflect real competitive ionization in complex mixtures.
- No chromatographic peak shape or retention-time variation; all chemical features are treated as point objects at fixed retention times.
- Controller logic is deterministic and does not model instrument variability, dead time, or queue-based scan scheduling delays observed in real hardware.
- Requires manual parameterization of isolation window, m/z tolerance, and intensity threshold; no automated optimization provided by the framework itself (optimization is performed via external comparison workflows).

## Evidence

- [other] The Environment class orchestrates three components: Chemicals are generated via samplers (e.g., DatabaseFormulaSampler), passed to an IndependentMassSpectrometer instance, and controlled by a fragmentation strategy Controller; the Environment runs this loop and produces a scan list via write_mzML output.: "The Environment class orchestrates three components: Chemicals are generated via samplers (e.g., DatabaseFormulaSampler), passed to an IndependentMassSpectrometer instance, and controlled by a"
- [readme] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
- [readme] devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment: "devising new methods is often challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment"
- [other] Generate 100 virtual chemicals by sampling m/z uniformly between 100–500 Da using UniformMZFormulaSampler and ChemicalMixtureCreator, requesting both MS1 and MS2 levels.: "Generate 100 virtual chemicals by sampling m/z uniformly between 100–500 Da using UniformMZFormulaSampler and ChemicalMixtureCreator, requesting both MS1 and MS2 levels."
- [other] Instantiate an IndependentMassSpectrometer in positive-ion mode with the generated chemical list.: "Instantiate an IndependentMassSpectrometer in positive-ion mode with the generated chemical list."
- [other] Configure a TopNController with N=3 fragments per survey scan, 1 Da isolation window, 10 ppm m/z tolerance, 15 s retention-time tolerance, and 1.75E5 minimum MS1 intensity threshold.: "Configure a TopNController with N=3 fragments per survey scan, 1 Da isolation window, 10 ppm m/z tolerance, 15 s retention-time tolerance, and 1.75E5 minimum MS1 intensity threshold."
- [other] Construct an Environment orchestrator spanning 0–1440 s, attach both the mass spectrometer and controller, and invoke env.run() to execute the fixed simulation control loop.: "Construct an Environment orchestrator spanning 0–1440 s, attach both the mass spectrometer and controller, and invoke env.run() to execute the fixed simulation control loop."
- [other] Verify the resulting scans list is non-empty and contains both MS1 and MS2 scan records.: "Verify the resulting scans list is non-empty and contains both MS1 and MS2 scan records."
- [other] The `Environment` class provides `write_mzML` to export the generated scans: "The `Environment` class provides `write_mzML` to export the generated scans"
