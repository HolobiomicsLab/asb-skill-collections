---
name: mzml-file-parsing-and-roi-extraction
description: Use when when you have a real mzML file from an untargeted metabolomics LC-MS/MS experiment and need to extract the chemical features it contains—either to simulate a data-dependent acquisition (DDA) strategy on those same compounds, to benchmark different fragmentation controllers, or to reproduce.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0091
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

# mzML file parsing and ROI extraction

## Summary

Parse a real LC-MS/MS mzML data file and extract regions of interest (ROIs) as chemical objects for simulation or analysis. This skill bridges raw mass spectrometry data and virtual fragmentation simulation by converting observed m/z and retention time features into UnknownChemical objects suitable for downstream mass spectrometer modeling.

## When to use

When you have a real mzML file from an untargeted metabolomics LC-MS/MS experiment and need to extract the chemical features it contains—either to simulate a data-dependent acquisition (DDA) strategy on those same compounds, to benchmark different fragmentation controllers, or to reproduce acquisition patterns observed in an empirical dataset. Specifically use this when you want to replay observed MS1 ion populations through a virtual mass spectrometer with alternative acquisition logic.

## When NOT to use

- When you only have extracted feature tables (e.g., peak lists or CSV files); use mzML parsing only for raw binary mzML/mzXML files.
- When you need to extract MS/MS fragmentation spectra; this skill focuses on MS1 precursor ROI extraction, not fragment ion data.
- When your data is already represented as UnknownChemical or ChemicalMixture objects; parsing is unnecessary if chemicals are pre-instantiated.

## Inputs

- mzML file (e.g., Beer1pos.mzML)
- MS level specification (integer, typically 2 for MS1 precursors)
- m/z range bounds (min_mz, max_mz in Daltons)
- retention time window (start_rt, stop_rt in seconds)
- minimum MS1 intensity threshold (floating-point intensity value)

## Outputs

- ChemicalMixture object (collection of UnknownChemical objects)
- List of UnknownChemical objects with m/z, retention time, and intensity attributes
- ROI-derived chemical features ready for environment simulation

## How to apply

Load the mzML file using ViMMS's ChemicalMixtureFromMZML class, specifying MS level 2 to extract MS1 precursor ion observations as ROIs. Set the m/z range (typically min_mz=100, max_mz=1000) and retention time window (start_rt, stop_rt in seconds) to define the feature extraction boundaries. Apply a minimum MS1 intensity threshold (e.g., at_least_one_point_above=1.75E5) to filter noise and retain only chemically significant ions. The tool automatically constructs UnknownChemical objects from each ROI, capturing observed m/z, retention time, and intensity profiles. These chemicals are then passed to an IndependentMassSpectrometer configured in the same ionization mode (positive/negative) as the source data, enabling faithful simulation of the original acquisition conditions.

## Related tools

- **ViMMS** (Framework providing ChemicalMixtureFromMZML class for mzML parsing and ROI extraction into UnknownChemical objects) — https://github.com/glasgowcompbio/vimms
- **ChemicalMixtureFromMZML** (Core ViMMS utility class that parses mzML files, applies intensity and m/z filtering, and constructs ROI-derived chemical features) — https://github.com/glasgowcompbio/vimms
- **IndependentMassSpectrometer** (Downstream consumer of parsed chemicals; simulates fragmentation on extracted ROI features in specified ionization mode) — https://github.com/glasgowcompbio/vimms
- **Environment** (Orchestrates simulation of parsed chemicals through mass spectrometer and controller; enables mzML output of simulated scans) — https://github.com/glasgowcompbio/vimms

## Examples

```
from vimms.MassSpec import IndependentMassSpectrometer
from vimms.ChemicalMixture import ChemicalMixtureFromMZML
from vimms.Controller import TopNController
from vimms.Environment import Environment

chemicals = ChemicalMixtureFromMZML('Beer1pos.mzML', ms_level=2, min_mz=100, max_mz=1000, start_rt=0, stop_rt=1E5, at_least_one_point_above=1.75E5)
ms = IndependentMassSpectrometer(chemicals=chemicals, ionisation_mode='positive')
env = Environment(ms, TopNController(N=10, isolation_window_width=1.0), start_rt=0, stop_rt=1E5, save_eval=True)
env.run()
env.write_mzML('simulated_output.mzML')
```

## Evaluation signals

- Parsed ChemicalMixture contains non-empty list of UnknownChemical objects with valid m/z values within specified range (min_mz to max_mz).
- All extracted chemicals have retention times within the specified window (start_rt to stop_rt); verify no outliers or boundary violations.
- Each ROI-derived chemical has at least one intensity data point ≥ the minimum intensity threshold (at_least_one_point_above); check none fall below cutoff.
- Simulated mzML output (from Environment.write_mzML()) exhibits comparable MS1 scan patterns to the input mzML—verify peak presence, m/z positions, and retention time spacing by visual inspection or spectral library matching.
- Number of extracted chemicals is reasonable given input file size and filtering parameters; an unusually low count may indicate overly strict thresholds or parsing failure.

## Limitations

- Extraction fidelity depends on mzML file quality; corrupted or incompletely centroided mzML files may yield spurious or incomplete ROIs.
- Minimum intensity threshold (e.g., 1.75E5) is user-tunable but arbitrary; threshold choice affects number and coverage of extracted chemicals and must be validated empirically for each instrument/matrix combination.
- Only MS1 precursor ROIs are extracted by default (MS level 2 specification); MS/MS fragment spectra are not automatically recovered, limiting scope to precursor ion-based simulation.
- Retention time and m/z filtering windows must be specified a priori; if windows are too narrow, real features may be excluded; if too broad, extraction becomes computationally expensive.
- The tool does not perform peak deconvolution; overlapping or unresolved features in the source mzML are treated as single ROIs, potentially confounding simulation of coeluting compounds.

## Evidence

- [other] extracting chemicals via ChemicalMixtureFromMZML and running them through the mass spectrometer Environment loop with TopNController: "Load the Beer1pos.mzML file and extract regions of interest (ROIs) as UnknownChemical objects using ChemicalMixtureFromMZML with MS levels set to 2."
- [other] Instantiate an IndependentMassSpectrometer in positive ionization mode with the extracted chemicals: "Instantiate an IndependentMassSpectrometer in positive ionization mode with the extracted chemicals."
- [results] minimum MS1 intensity threshold of 1.75E5: "at_least_one_point_above=min_ms1_intensity with default value 1.75E5"
- [results] min_mz=100, max_mz=1000 for chemical sampling: "min_mz=100, max_mz=1000 for chemical sampling"
- [readme] flexible and modular framework designed to simulate fragmentation strategies: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
