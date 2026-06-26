---
name: mzml-file-format-writing
description: Use when you have peak properties (mass, intensity, retention time) for
  biomolecules, selected noise and fragmentation models, and instrument parameters
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SMITER
  - pyQms
  - Python
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3390/genes12030396
  title: SMITER
evidence_spans:
- SMITER (Synthetic mzML writer) is a python-based command-line tool designed to simulate
  LC-MS/MS runs.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smiter_cq
    doi: 10.3390/genes12030396
    title: SMITER
  dedup_kept_from: coll_smiter_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/genes12030396
  all_source_dois:
  - 10.3390/genes12030396
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mzml-file-format-writing

## Summary

Write synthetic LC-MS/MS data to mzML format by integrating peak-property definitions, noise models, and fragmentation models through SMITER's modular design. This skill enables reproducible gold-standard MS dataset generation where ground truth is known.

## When to use

You have peak properties (mass, intensity, retention time) for biomolecules, selected noise and fragmentation models, and instrument parameters (e.g., gradient_length), and you need to generate a synthetic LC-MS/MS dataset in mzML format for algorithm validation, parameter optimization, or co-elution/co-fragmentation prediction studies.

## When NOT to use

- Input peak properties lack chemical formula information — SMITER's isotopic patterns and fragmentation rely on accurate chemical formulas via pyQms.
- You are processing real experimental MS data rather than generating synthetic data — this skill is for simulation, not import/conversion of existing acquisitions.
- Fragmentation rules for your biomolecule type are not available (SMITER provides peptide and nucleoside models; other classes require custom fragmentor implementation).

## Inputs

- peak properties dictionary (mass, intensity, retention-time per analyte)
- CSV file containing analyte properties (optional; convert via csv_to_peak_properties)
- fragmentor object (PeptideFragmentor, nucleoside fragmentation model, or custom)
- noise injector object (UniformNoiseInjector or custom intensity-specific noise model)
- general simulation parameters (gradient_length, instrument configuration)

## Outputs

- synthetic mzML file (LC-MS/MS dataset in mzML format)
- gold-standard MS dataset with known ground truth

## How to apply

First, load or construct peak properties (mass, intensity, retention time) for analytes, optionally converting from CSV via smiter.lib.csv_to_peak_properties. Second, instantiate a fragmentor object (e.g., fragmentation_functions.PeptideFragmentor for peptides or nucleoside fragmentation model) to define fragmentation rules. Third, instantiate a noise generator (e.g., smiter.noise_functions.UniformNoiseInjector or intensity-specific noise model) to model instrument noise. Fourth, define general simulation parameters including gradient_length and other instrument-configuration settings. Finally, call smiter.synthetic_mzml.write_mzml with the peak properties, noise injector, fragmentor, and general parameters to execute the modular simulation pipeline and write the output mzML file. The modular design allows substitution of default noise/fragmentation models with custom implementations.

## Related tools

- **SMITER** (Primary tool; orchestrates peak properties, noise, and fragmentation models to write synthetic mzML files) — https://github.com/LeidelLab/SMITER
- **pyQms** (Dependency for highly-accurate isotopic pattern calculation used by SMITER) — https://github.com/pyQms/pyqms
- **Python** (Runtime environment and scripting language for SMITER)

## Examples

```
from smiter.lib import csv_to_peak_properties; from smiter.fragmentation_functions import PeptideFragmentor; from smiter.noise_functions import UniformNoiseInjector; from smiter.synthetic_mzml import write_mzml; peaks = csv_to_peak_properties('example_data.csv'); write_mzml(peaks, UniformNoiseInjector(), PeptideFragmentor(), 'output.mzML', gradient_length=30)
```

## Evaluation signals

- Output mzML file is valid XML and compliant with mzML schema (parseable by standard MS software).
- Synthetic peak m/z values match input chemical formulas with expected isotopic fine structure via pyQms.
- Noise injection produces expected intensity ranges or distributions (uniform or intensity-specific noise model as selected).
- Fragmentation spectra (MS2) contain expected peptide b/y ions or nucleoside fragments consistent with selected fragmentor rules.
- Retention time values in output file match input peak properties; gradient_length parameter correctly scales RT distribution.

## Limitations

- SMITER supports peptide and modified nucleoside fragmentation by default; other biomolecule classes require custom fragmentor implementation.
- Retention time prediction is not built-in; external modules (e.g., deep learning models) must be integrated for realistic RT simulation.
- Noise models are simplified (uniform or intensity-specific); real instrument noise complexity may not be fully captured.
- No changelog documented; version history and breaking changes not formally tracked across releases.

## Evidence

- [other] Peak-property definitions, noise models, and fragmentation models integration: "SMITER's write_mzml function executes the final simulation step by accepting peak-property definitions along with selectable noise and fragmentation models, which are integrated through a modular"
- [readme] Modular design for custom noise and fragmentation: "As SMITER features a modular design, noise and fragmentation models can easily be implemented or adapted."
- [readme] Gold-standard dataset purpose: "This allows for the facile creation of defined gold-standard-LC-MS/MS datasets for any type of experiment. Such gold standards, where the ground truth is known, are required in computational mass"
- [readme] Chemical formula basis and isotopic accuracy: "It enables the simulation of any biomolecule since all calculations are based on the chemical formulas. ...usage of highly-accurate isotopic patterns enabled by pyQms"
- [other] Five-step workflow for write_mzml: "1. create the peak properties dict...2. Choose a fragmentor...3. Choose a Noise generator...4. Define general params...5. Run the simulation and write the resulting mzML using"
- [readme] Co-elution and co-fragmentation prediction use case: "Similarly, gold-standard datasets can be used to evaluate analytical hurdles e.g. by predicting co-elution and co-fragmentation of molecules."
