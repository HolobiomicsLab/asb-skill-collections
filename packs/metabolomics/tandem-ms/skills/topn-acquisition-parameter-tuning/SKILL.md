---
name: topn-acquisition-parameter-tuning
description: Use when when you have real LC-MS/MS data (mzML format) from an untargeted metabolomics experiment and want to test how variations in TopN DDA parameters affect which precursor ions are selected and fragmented, before deploying the optimized strategy on physical instruments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ViMMS
  - ChemicalMixtureFromMZML
  - TopNController
  - IndependentMassSpectrometer
  - Environment
  - ViMMS (Virtual Metabolomics Mass Spectrometer)
  - PeakPicking (MZMine parameters)
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.21105/joss.03990
  title: vimms
- doi: 10.1021/acs.analchem.0c03895
  title: ''
evidence_spans:
- '**V**irtual **M**etabolomics **M**ass **S**pectrometer (**VIMMS**), a flexible and modular framework designed to simulate fragmentation strategies'
- '**V**irtual **M**etabolomics **M**ass **S**pectrometer (**VIMMS**), a comprehensive and modular framework for the simulation of fragmentation strategies'
- Existing mzML files can be converted into chemical lists using `ChemicalMixtureFromMZML`.
- '`TopNController` – standard Top‑N data dependent acquisition.'
- Mass Spectrometer – either an in silico model (`IndependentMassSpectrometer`) or a real instrument.
- Environment – orchestrates interaction between the mass spectrometer and the controller.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_vimms_cq
    doi: 10.21105/joss.03990
    title: vimms
  dedup_kept_from: coll_vimms_cq
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

# TopN Acquisition Parameter Tuning

## Summary

Optimize data-dependent acquisition (DDA) fragmentation strategies by systematically configuring TopN controller parameters (N value, isolation window width, m/z tolerance, retention time tolerance, and MS1 intensity threshold) and evaluating their effects on simulated acquisition patterns using real metabolomics data.

## When to use

When you have real LC-MS/MS data (mzML format) from an untargeted metabolomics experiment and want to test how variations in TopN DDA parameters affect which precursor ions are selected and fragmented, before deploying the optimized strategy on physical instruments. Use this skill when you need to compare acquisition patterns between different parameter configurations or validate whether a TopN strategy can reproduce patterns observed in empirical data.

## When NOT to use

- Input mzML data is from a single targeted precursor or SRM experiment (not untargeted DDA).
- You are optimizing non-TopN strategies such as targeted inclusion lists or data-independent acquisition (DIA); use controller-specific parameter tuning instead.
- The mzML file has MS level 1 only (no MS/MS fragmentation data); ChemicalMixtureFromMZML requires MS level ≥ 2.

## Inputs

- mzML file (LC-MS/MS dataset from untargeted metabolomics, e.g., Beer1pos.mzML)
- TopN controller parameter set (N value, isolation window width in m/z, m/z tolerance, retention time tolerance, MS1 intensity threshold)
- Retention time range (start_rt, stop_rt in seconds)
- UnknownChemical mixture extracted from mzML via ChemicalMixtureFromMZML

## Outputs

- Simulated mzML file with DDA scans under tested TopN parameters
- Evaluation metrics (peak picking results, spectral matching scores across thresholds 0.0–1.0 with 0.1 step)
- Comparison metrics: precursor ion selection patterns, fragment scan counts, retention time coverage

## How to apply

Load the mzML file and extract regions of interest (ROIs) as UnknownChemical objects using ChemicalMixtureFromMZML with MS levels set to 2. Instantiate an IndependentMassSpectrometer in the appropriate ionization mode with the extracted chemicals. Configure a TopNController by setting fragmentation parameters: N (number of top-intensity ions to fragment, e.g., 10–20), isolation window width in m/z (typically 0.7–1.2 m/z units), m/z tolerance for precursor selection, retention time tolerance for dynamic exclusion, and minimum MS1 intensity threshold (default 1.75E5). Create an Environment linking the mass spectrometer and controller, set the retention time range to the total acquisition window, and enable save_eval=True to capture evaluation metrics. Execute env.run() to simulate the DDA loop, then write simulated scans to mzML format using Environment.write_mzML() and compare acquisition patterns (precursor selection frequency, fragment count distributions, coverage) against the reference empirical data using peak-picking and spectral matching thresholds.

## Related tools

- **ViMMS (Virtual Metabolomics Mass Spectrometer)** (Framework for simulating fragmentation strategies and scan-level DDA control in a virtual MS environment; hosts TopNController and Environment classes) — https://github.com/glasgowcompbio/vimms
- **ChemicalMixtureFromMZML** (Extracts regions of interest (ROIs) from empirical mzML files as UnknownChemical objects for simulation input) — https://github.com/glasgowcompbio/vimms
- **TopNController** (ViMMS controller class that implements TopN DDA logic; accepts and applies fragmentation parameters (N, isolation window, tolerance, intensity threshold)) — https://github.com/glasgowcompbio/vimms
- **IndependentMassSpectrometer** (ViMMS mass spectrometer model configured with extracted chemicals and ionization mode (positive/negative); generates simulated scans) — https://github.com/glasgowcompbio/vimms
- **Environment** (ViMMS orchestrator that runs the DDA simulation loop with a mass spectrometer and controller; enables save_eval=True for metric capture and write_mzML() for output export) — https://github.com/glasgowcompbio/vimms
- **PeakPicking (MZMine parameters)** (Evaluation helper for peak detection in simulated scans; used in downstream comparison with reference data) — https://github.com/glasgowcompbio/vimms

## Examples

```
from vimms.ChemicalMixtureFromMZML import ChemicalMixtureFromMZML; from vimms.MassSpectrometer import IndependentMassSpectrometer; from vimms.Controller import TopNController; from vimms.Environment import Environment; mixture = ChemicalMixtureFromMZML('Beer1pos.mzML', ms_levels=[2]); ms = IndependentMassSpectrometer(ionisation_mode='positive', chemicals=mixture); controller = TopNController(N=10, isolation_window=0.7, mz_tol=10, rt_tol=15, min_ms1_intensity=1.75e5); env = Environment(mass_spectrometer=ms, controller=controller, rt_range=[0, 1e5], save_eval=True); env.run(); env.write_mzML('simulated_topn.mzML')
```

## Evaluation signals

- Simulated mzML file is valid (readable by mzML parsers and contains expected MS1 and MS/MS scan counts consistent with TopN parameter N).
- Precursor ion selection patterns in simulated scans match or correlate strongly with patterns in the reference empirical data (comparison of m/z values and retention times of fragmented ions).
- Peak-picking results from simulated scans yield spectral matching scores ≥ 0.7 (by default cosine similarity threshold) when compared against a reference spectral library (e.g., GNPS-NIST14-MATCHES.mgf).
- Retention time coverage and fragment scan frequency distributions are within expected ranges relative to the reference data (e.g., no artificial clustering of fragments or gaps).
- Evaluation metrics are exported (save_eval=True) and show consistency across multiple TopN parameter trials, demonstrating stable simulation behavior.

## Limitations

- Simulation accuracy depends on accurate extraction of ROIs from the reference mzML; poorly detected or fragmented ions in the original data will propagate into simulation.
- TopN parameter tuning is specific to the chemical composition of the input sample; optimized parameters may not generalize to different matrices or sample types without re-tuning.
- The virtual mass spectrometer model (IndependentMassSpectrometer) may not capture all instrumental artifacts (e.g., space-charge effects, detector saturation, instrumental drift) present in empirical acquisition; simulated scans may differ systematically from real data.
- Computational cost scales with the number of extracted chemicals and the retention time range; very large mzML files or long acquisition windows may require downsampling or ROI pre-filtering.
- Real-time constraints and missed scans due to instrument duty cycle are not modeled; TopN parameters optimized in simulation may not perform identically on hardware.

## Evidence

- [methods] Configuration workflow from task_003 specification: "Configure a TopNController with fragmentation strategy parameters (N for top N most intense ions, isolation window width in m/z, m/z tolerance, retention time tolerance, and minimum MS1 intensity"
- [methods] Extraction and simulation loop: "Extract chemicals via ChemicalMixtureFromMZML and running them through the mass spectrometer Environment loop with TopNController"
- [readme] Framework motivation and capability: "ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment. You can generate new LC-MS/MS data based on empirical data or virtually replay a previous"
- [methods] Evaluation metric capture and export: "set the retention time range to the total acquisition window, and enable save_eval=True to capture evaluation metrics. Execute env.run() to simulate the DDA acquisition loop. Write the simulated"
- [results] Intensity threshold specification: "at_least_one_point_above=min_ms1_intensity with default value 1.75E5"
- [results] Spectral matching evaluation range: "matching_thresholds array from 0.0 to 1.0 with step 0.1"
