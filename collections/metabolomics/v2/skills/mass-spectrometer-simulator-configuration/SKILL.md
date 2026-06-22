---
name: mass-spectrometer-simulator-configuration
description: Use when when you have a list of chemical compounds (with m/z values, retention times, and intensities) and need to simulate their acquisition behavior under a specific ionization polarity and mass spectrometer configuration.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - OpenMS
  - ViMMS
derived_from:
- doi: 10.21105/joss.03990
  title: vimms
- doi: 10.1021/acs.analchem.0c03895
  title: ''
evidence_spans:
- ViMMS is compatible with Python 3+
- Processes mzML output from a simulation (or real acquisition) to compute fragmentation coverage using OpenMS
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
---

# Mass Spectrometer Simulator Configuration

## Summary

Configure a virtual mass spectrometer instance within the ViMMS framework to simulate tandem MS/MS acquisition on a chemical mixture with specified polarity, ionization mode, and detector parameters. This skill enables prototyping of fragmentation strategies before real instrument deployment.

## When to use

When you have a list of chemical compounds (with m/z values, retention times, and intensities) and need to simulate their acquisition behavior under a specific ionization polarity and mass spectrometer configuration. Use this skill as the second step after generating or extracting chemicals, immediately before attaching a controller to orchestrate the fragmentation strategy.

## When NOT to use

- Your chemicals are already represented as raw spectrum objects or mzML files without extracted m/z/RT/intensity metadata; use ChemicalMixtureFromMZML first.
- You need to simulate instrument-specific hardware behavior (e.g., Thermo Orbitrap resolution curves, Agilent Q-TOF drift); ViMMS provides idealized independent mass detection.
- You are replaying real acquired data without modification; use mzML replay features instead of configuring a new virtual spectrometer.

## Inputs

- chemical list (list of Chemical objects with m/z, retention time, intensity, and MS levels)
- polarity setting (string: 'positive' or 'negative')
- optional: ionization mode parameters

## Outputs

- configured IndependentMassSpectrometer instance
- internally tracked scan list (populated after Environment.run())

## How to apply

Instantiate an `IndependentMassSpectrometer` class with the chemical mixture and polarity setting (positive or negative ion mode). Pass the extracted or generated chemical list (e.g., from `ChemicalMixtureFromMZML` or `ChemicalMixtureCreator`) to the constructor. The mass spectrometer will model scan-level MS1 and MS2 acquisition behavior based on the chemical properties (m/z, retention time, intensity) without requiring real instrument hardware. Configure isolation window, m/z tolerance, intensity thresholds, and retention-time tolerance as parameters to the downstream controller, not the mass spectrometer itself. The mass spectrometer acts as a virtual detector that simulates peak intensity evolution over time and fragmentation patterns according to the controller's strategy.

## Related tools

- **ViMMS** (Core framework providing IndependentMassSpectrometer class and virtual acquisition simulation engine) — https://github.com/glasgowcompbio/vimms
- **Python** (Language for instantiating and configuring the mass spectrometer object)
- **OpenMS** (Optional post-simulation tool for peak picking and fragmentation coverage analysis on mzML output)

## Examples

```
ms = IndependentMassSpectrometer(polarity="positive", chemicals=chemicals)
```

## Evaluation signals

- IndependentMassSpectrometer instance is created without errors and accepts the chemical list and polarity argument.
- After Environment.run(), the scans list is non-empty and contains both MS1 and MS2 scan records with matching chemical m/z values.
- MS1 intensity profiles evolve over retention time in a manner consistent with the input chemical retention times and peak widths.
- MS2 spectra are only generated when controller triggers fragmentation based on MS1 intensity, isolation window, and m/z tolerance constraints.
- Exported mzML file contains valid scan metadata (polarity, precursor m/z, isolation window, retention time) conforming to mzML schema.

## Limitations

- IndependentMassSpectrometer does not model instrument-specific mass accuracy, resolution, or detector saturation; it assumes ideal peak shapes and m/z detection.
- Fragmentation intensity distribution is determined by the attached controller strategy, not by real peptide/metabolite fragmentation chemistry.
- Chemical list must include retention times for realistic scan timing; purely m/z-based chemical lists will be assigned default or synthetic retention times.
- The simulator runs in silico and does not interact with actual Thermo Fisher IAPI or other hardware APIs; hardware integration requires separate instrumentation layers.

## Evidence

- [other] Set up a virtual mass spectrometer
ms = IndependentMassSpectrometer(polarity="positive", chemicals=chemicals): "Set up a virtual mass spectrometer
ms = IndependentMassSpectrometer(polarity="positive", chemicals=chemicals)"
- [readme] ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment. You can generate new LC-MS/MS data based on empirical data or virtually replay a previous LC-MS/MS analysis using existing data: "ViMMS provides scan-level control simulation of the MS2 acquisition process in a virtual environment"
- [other] Instantiate an IndependentMassSpectrometer in positive-ion mode with the generated chemical list: "Instantiate an IndependentMassSpectrometer in positive-ion mode with the generated chemical list"
- [intro] a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics"
- [other] Extract chemicals from the Beer1pos mzML using ChemicalMixtureFromMZML class to create a chemical list with known retention times and m/z values. Set up an IndependentMassSpectrometer with the extracted chemicals in positive polarity mode.: "Extract chemicals from the Beer1pos mzML using ChemicalMixtureFromMZML class to create a chemical list with known retention times and m/z values. Set up an IndependentMassSpectrometer with the"
