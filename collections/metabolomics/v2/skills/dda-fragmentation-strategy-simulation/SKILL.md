---
name: dda-fragmentation-strategy-simulation
description: Use when you have real mzML LC-MS/MS data (e.g., from a Beer sample or
  HMDB reference set) and want to test whether a proposed TopN DDA strategy (or variant)
  can accurately reproduce the observed acquisition patterns, or you want to compare
  multiple acquisition controllers on the same chemical.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - ViMMS
  - ChemicalMixtureFromMZML
  - TopNController
  - IndependentMassSpectrometer
  - Environment
  - ViMMS (Virtual Metabolomics Mass Spectrometer)
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.21105/joss.03990
  title: vimms
- doi: 10.1021/acs.analchem.0c03895
  title: ''
evidence_spans:
- '**V**irtual **M**etabolomics **M**ass **S**pectrometer (**VIMMS**), a flexible
  and modular framework designed to simulate fragmentation strategies'
- '**V**irtual **M**etabolomics **M**ass **S**pectrometer (**VIMMS**), a comprehensive
  and modular framework for the simulation of fragmentation strategies'
- Existing mzML files can be converted into chemical lists using `ChemicalMixtureFromMZML`.
- '`TopNController` – standard Top‑N data dependent acquisition.'
- Mass Spectrometer – either an in silico model (`IndependentMassSpectrometer`) or
  a real instrument.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# DDA Fragmentation Strategy Simulation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Simulate Data-Dependent Acquisition (DDA) fragmentation strategies on real or synthetic LC-MS/MS data by extracting chemical constituents and running them through a virtual mass spectrometer with a configurable acquisition controller. This skill enables rapid prototyping and benchmarking of TopN and other MS/MS acquisition strategies before deployment on real instruments.

## When to use

You have real mzML LC-MS/MS data (e.g., from a Beer sample or HMDB reference set) and want to test whether a proposed TopN DDA strategy (or variant) can accurately reproduce the observed acquisition patterns, or you want to compare multiple acquisition controllers on the same chemical mixture without repeated instrument time.

## When NOT to use

- Input is already a processed feature table or spectral library (not raw mzML) — use mzML import/export conversions first.
- You seek to optimize MS1-only acquisition or data-independent acquisition (DIA) strategies — this skill is specific to DDA fragmentation control.
- The chemical mixture is too large (>10,000 unique compounds) to simulate efficiently within available compute time or memory.

## Inputs

- mzML file (real LC-MS/MS data, e.g., Beer1pos.mzML)
- MS ionization mode (positive or negative)
- TopN acquisition parameters (N, isolation window, m/z tolerance, RT tolerance, intensity threshold)

## Outputs

- UnknownChemical objects (extracted ROIs from mzML)
- Simulated mzML file with DDA scans
- Evaluation metrics (capture via save_eval=True in Environment)

## How to apply

Load the reference mzML file and extract regions of interest (ROIs) as UnknownChemical objects using ChemicalMixtureFromMZML, specifying MS level 2 and filtering by retention time range (e.g., start_rt=0, stop_rt=1E5) and intensity threshold (e.g., min_ms1_intensity=1.75E5). Instantiate an IndependentMassSpectrometer in the appropriate ionization mode (positive or negative) with the extracted chemicals. Configure a TopNController with fragmentation parameters: N (number of most intense parent ions to fragment), isolation window width in m/z, m/z tolerance, retention time tolerance, and minimum MS1 intensity threshold. Create an Environment with the mass spectrometer and controller, set the retention time range to cover the total acquisition window, and enable save_eval=True to capture evaluation metrics. Execute env.run() to simulate the DDA acquisition loop, then write the simulated scans to mzML format using Environment.write_mzML() for downstream comparison with the original data.

## Related tools

- **ViMMS (Virtual Metabolomics Mass Spectrometer)** (Core framework providing mass spectrometer simulation engine, chemical extraction, controller interface, and environment loop for DDA acquisition replay and strategy prototyping) — https://github.com/glasgowcompbio/vimms
- **ChemicalMixtureFromMZML** (Extracts UnknownChemical objects (ROIs) from real mzML files with configurable MS level, retention time, and intensity filtering) — https://github.com/glasgowcompbio/vimms
- **TopNController** (Implements TopN DDA acquisition logic — selects N most intense MS1 parent ions and fragments them with specified isolation window and tolerance parameters) — https://github.com/glasgowcompbio/vimms
- **IndependentMassSpectrometer** (Virtual mass spectrometer instance configured with ionization mode and chemical mixture; simulates fragmentation and ion detection) — https://github.com/glasgowcompbio/vimms
- **Environment** (Orchestrates the DDA acquisition loop, manages retention time scheduling, captures evaluation metrics (save_eval=True), and exports simulated scans to mzML) — https://github.com/glasgowcompbio/vimms

## Examples

```
from vimms.ChemicalMixtureFromMZML import ChemicalMixtureFromMZML
from vimms.TopNController import TopNController
from vimms.IndependentMassSpectrometer import IndependentMassSpectrometer
from vimms.Environment import Environment

chem = ChemicalMixtureFromMZML('Beer1pos.mzML', ms_level=2, start_rt=0, stop_rt=1E5, min_ms1_intensity=1.75E5)
ms = IndependentMassSpectrometer(ionization_mode='positive', chemical_mixture=chem)
control = TopNController(N=10, isolation_width=1.0, mz_tol=5.0, rt_tol=15.0, min_intensity=1.75E5)
env = Environment(mass_spectrometer=ms, controller=control, rt_range=[0, 1E5], save_eval=True)
env.run()
env.write_mzML('simulated_dda.mzML')
```

## Evaluation signals

- Simulated mzML file is valid and readable by standard mzML parsers; schema conforms to mzML specification.
- Acquisition pattern (number of MS1 scans, number and timing of MS2 scans) matches observed pattern in original mzML within ±10% of scan count or ±5 s retention time drift.
- MS1 peak intensity and m/z values extracted from simulated scans fall within 5–20% relative error of original data (checking chemical recovery fidelity).
- Evaluation metrics (save_eval=True output) include coverage metrics (% of extracted ROIs fragmented) and are non-NaN and in valid ranges (0–100%).
- TopN controller successfully selected top N intense ions and isolated them at specified m/z window width without controller-level errors or crashes.

## Limitations

- Extraction and simulation accuracy depend on the quality of the input mzML file and ChemicalMixtureFromMZML filtering parameters; noisy or low-intensity data may yield incomplete ROI extraction.
- Simulation is slower than real-time acquisition; large chemical mixtures (thousands of ROIs) may require several minutes to hours depending on retention time range and hardware.
- ViMMS simulates fragmentation using idealized mass spectrometry models and does not account for instrument-specific effects (e.g., space charge, dead time, detector saturation) present on real Orbitrap or Tribrid systems.
- TopNController is a simplified DDA implementation; real instruments may employ more complex heuristics (dynamic exclusion, adaptive m/z windows, real-time recalibration) not modeled here.
- Comparison with real data is qualitative unless accompanied by quantitative metrics (e.g., spectral matching or library scoring); the simulated scans must be independently validated against reference spectra.

## Evidence

- [other] TopN simulations from real beer mzML data produce comparable acquisition patterns by extracting chemicals via ChemicalMixtureFromMZML and running them through the mass spectrometer Environment loop with TopNController.: "TopN simulations from real beer mzML data produce comparable acquisition patterns by extracting chemicals via ChemicalMixtureFromMZML and running them through the mass spectrometer Environment loop"
- [other] Load the Beer1pos.mzML file and extract regions of interest (ROIs) as UnknownChemical objects using ChemicalMixtureFromMZML with MS levels set to 2.: "Load the Beer1pos.mzML file and extract regions of interest (ROIs) as UnknownChemical objects using ChemicalMixtureFromMZML with MS levels set to 2."
- [other] Configure a TopNController with fragmentation strategy parameters (N for top N most intense ions, isolation window width in m/z, m/z tolerance, retention time tolerance, and minimum MS1 intensity threshold of 1.75E5).: "Configure a TopNController with fragmentation strategy parameters (N for top N most intense ions, isolation window width in m/z, m/z tolerance, retention time tolerance, and minimum MS1 intensity"
- [other] Create an Environment with the mass spectrometer and controller, set the retention time range to the total acquisition window, and enable save_eval=True to capture evaluation metrics.: "Create an Environment with the mass spectrometer and controller, set the retention time range to the total acquisition window, and enable save_eval=True to capture evaluation metrics."
- [other] Execute env.run() to simulate the DDA acquisition loop. Write the simulated scans to mzML format using Environment.write_mzML() for downstream comparison.: "Execute env.run() to simulate the DDA acquisition loop. Write the simulated scans to mzML format using Environment.write_mzML() for downstream comparison."
- [readme] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
- [readme] You can generate new LC-MS/MS data based on empirical data or virtually replay a previous LC-MS/MS analysis using existing data, which allows for testing different fragmentation strategies.: "You can generate new LC-MS/MS data based on empirical data or virtually replay a previous LC-MS/MS analysis using existing data, which allows for testing different fragmentation strategies."
