---
name: spectral-scan-generation-and-export
description: Use when you have real LC-MS/MS data (mzML) from a complex sample (e.g., beer, metabolomics extract) and need to prototype or validate a new data-dependent acquisition (DDA) strategy—such as Top-N fragmentation—before deploying it on physical instrumentation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - ViMMS
  - ChemicalMixtureFromMZML
  - TopNController
  - IndependentMassSpectrometer
  - Environment
  techniques:
  - LC-MS
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

# spectral-scan-generation-and-export

## Summary

Simulate tandem mass spectrometry acquisition by extracting regions of interest (ROIs) from real LC-MS/MS data, instantiating a virtual mass spectrometer, configuring a fragmentation controller, and exporting the generated scans to mzML format for downstream comparison and validation.

## When to use

You have real LC-MS/MS data (mzML) from a complex sample (e.g., beer, metabolomics extract) and need to prototype or validate a new data-dependent acquisition (DDA) strategy—such as Top-N fragmentation—before deploying it on physical instrumentation. Use this skill when you want to replay acquisition patterns from empirical data through a virtual environment to evaluate whether simulated MS/MS scans faithfully recapitulate the original instrument behavior.

## When NOT to use

- Input mzML file contains only MS1 data or lacks MS2 fragmentation spectra; ROI extraction requires at least MS level 2 data.
- Acquisition strategy is already validated on physical hardware and you only need archival or format conversion; simulation is unnecessary.
- You need real-time instrument control or feedback from a live Thermo Orbitrap or equivalent; ViMMS is a virtual environment, not compatible with live acquisition without the vimms_fusion extension and IAPI license.

## Inputs

- reference mzML file (e.g., Beer1pos.mzML)
- retention time range (start_rt, stop_rt in seconds)
- m/z range (min_mz, max_mz)
- minimum MS1 intensity threshold (e.g., 1.75E5)
- fragmentation controller parameters (N, isolation window, m/z tolerance, RT tolerance)

## Outputs

- simulated mzML file with MS1 and MS2 scans
- evaluation metrics (saved when save_eval=True)
- list of extracted UnknownChemical objects

## How to apply

Load the reference mzML file and extract regions of interest (ROIs) as UnknownChemical objects using ChemicalMixtureFromMZML with MS levels set to 2 and intensity thresholds (e.g., at_least_one_point_above=1.75E5). Instantiate an IndependentMassSpectrometer in the appropriate ionization mode (positive or negative) with the extracted chemicals. Configure a controller (e.g., TopNController) with fragmentation parameters: N for the number of top ions to fragment, isolation window width (m/z), m/z tolerance, retention time tolerance, and minimum MS1 intensity threshold. Create an Environment linking the mass spectrometer and controller, set the retention time range to span the total acquisition window, and enable save_eval=True to capture evaluation metrics. Execute env.run() to simulate the acquisition loop, then write the simulated scans to mzML format using Environment.write_mzML() for comparison against the original empirical data.

## Related tools

- **ChemicalMixtureFromMZML** (Extracts regions of interest (ROIs) as UnknownChemical objects from real mzML files for virtual mass spectrometer input) — https://github.com/glasgowcompbio/vimms
- **IndependentMassSpectrometer** (Instantiates a virtual mass spectrometer in the specified ionization mode (positive/negative) with the extracted chemicals) — https://github.com/glasgowcompbio/vimms
- **TopNController** (Configures the data-dependent fragmentation strategy, selecting the top N most intense ions for MS2 acquisition with specified isolation and tolerance windows) — https://github.com/glasgowcompbio/vimms
- **Environment** (Orchestrates the simulation loop, linking the mass spectrometer and controller, managing retention time range and evaluation metric capture) — https://github.com/glasgowcompbio/vimms
- **ViMMS** (Core framework providing the virtual mass spectrometry simulation environment, modular fragmentation strategy controllers, and mzML I/O) — https://github.com/glasgowcompbio/vimms

## Examples

```
from vimms.ChemicalMixtureFromMZML import ChemicalMixtureFromMZML; from vimms.MassSpectrometer import IndependentMassSpectrometer; from vimms.Controller import TopNController; from vimms.Environment import Environment; chem_mixture = ChemicalMixtureFromMZML('Beer1pos.mzML', ms_levels=[2], at_least_one_point_above=1.75E5); ms = IndependentMassSpectrometer(chem_mixture, ionisation_mode='POS'); controller = TopNController(N=10, isolation_window=1.0, mz_tol=0.1, rt_tol=15.0); env = Environment(ms, controller, start_rt=0, stop_rt=1E5, save_eval=True); env.run(); env.write_mzML('simulated_scans.mzML')
```

## Evaluation signals

- Exported mzML file validates against mzML schema and contains both MS1 and MS2 scans with correct metadata (ionization mode, precursor m/z, isolation window).
- Number and intensity of simulated MS1 peaks match the original mzML ROIs within the extraction threshold (1.75E5 or specified minimum).
- MS2 fragmentation pattern (precursor selection, number of fragments, intensity distribution) for simulated scans correlates with the corresponding empirical scans when compared via spectral similarity metrics or manual inspection.
- Evaluation metrics (captured when save_eval=True) can be compared across different controller configurations to validate that the simulation faithfully reproduces relative acquisition patterns.
- Retention time distribution of simulated scans spans the configured retention time range (start_rt to stop_rt) without gaps or duplicates outside the expected window.

## Limitations

- Simulated fragmentation patterns depend on the fidelity of in silico fragmentation models used by the IndependentMassSpectrometer; complex polycyclic or unusual structures may not fragment accurately compared to real instruments.
- ChemicalMixtureFromMZML ROI extraction is sensitive to the minimum intensity threshold; too high a threshold misses low-abundance metabolites, too low risks noise and computational overhead.
- The virtual environment does not account for hardware-specific effects such as ion source instability, detector saturation, or dynamic exclusion drift that occur in real Thermo Orbitrap or equivalent instruments.
- Export to mzML relies on accurate MS1 and MS2 scan parameters (precursor m/z, isolation window, collision energy); downstream tools (e.g., spectral matching, MS1 feature detection) may fail if these parameters are misconfigured.
- Real-time integration with physical instruments (e.g., Thermo Orbitrap Fusion Tribrid) requires the optional vimms_fusion extension and an IAPI license; this skill in isolation is for offline simulation only.

## Evidence

- [other] Load the Beer1pos.mzML file and extract regions of interest (ROIs) as UnknownChemical objects using ChemicalMixtureFromMZML with MS levels set to 2: "Load the Beer1pos.mzML file and extract regions of interest (ROIs) as UnknownChemical objects using ChemicalMixtureFromMZML with MS levels set to 2"
- [other] Instantiate an IndependentMassSpectrometer in positive ionization mode with the extracted chemicals: "Instantiate an IndependentMassSpectrometer in positive ionization mode with the extracted chemicals"
- [other] Configure a TopNController with fragmentation strategy parameters (N for top N most intense ions, isolation window width in m/z, m/z tolerance, retention time tolerance, and minimum MS1 intensity threshold of 1.75E5): "Configure a TopNController with fragmentation strategy parameters (N for top N most intense ions, isolation window width in m/z, m/z tolerance, retention time tolerance, and minimum MS1 intensity"
- [other] Create an Environment with the mass spectrometer and controller, set the retention time range to the total acquisition window, and enable save_eval=True to capture evaluation metrics: "Create an Environment with the mass spectrometer and controller, set the retention time range to the total acquisition window, and enable save_eval=True to capture evaluation metrics"
- [other] Execute env.run() to simulate the DDA acquisition loop. Write the simulated scans to mzML format using Environment.write_mzML() for downstream comparison: "Execute env.run() to simulate the DDA acquisition loop. Write the simulated scans to mzML format using Environment.write_mzML() for downstream comparison"
- [readme] ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment. You can generate new LC-MS/MS data based on empirical data or virtually replay a previous LC-MS/MS analysis using existing data, which allows for testing different fragmentation strategies: "ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment. You can generate new LC-MS/MS data based on empirical data or virtually replay a previous"
- [readme] extract the scan results as mzML files: "extract the scan results as mzML files"
