---
name: synthetic-spectrum-generation
description: Use when when you need to create benchmark LC-MS/MS datasets with controlled, known composition for testing MS analysis algorithms, validating retention-time or fragmentation predictions, or predicting co-elution and co-fragmentation challenges before conducting real experiments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SMITER
  - pyQms
  - Python
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.3390/genes12030396
  title: SMITER
evidence_spans:
- SMITER (Synthetic mzML writer) is a python-based command-line tool designed to simulate LC-MS/MS runs.
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# synthetic-spectrum-generation

## Summary

Generation of synthetic LC-MS/MS data in mzML format from chemical formulas by integrating peak-property definitions, fragmentation models, and noise models. This skill enables creation of gold-standard datasets with known ground truth for algorithm validation and analytical challenge prediction.

## When to use

When you need to create benchmark LC-MS/MS datasets with controlled, known composition for testing MS analysis algorithms, validating retention-time or fragmentation predictions, or predicting co-elution and co-fragmentation challenges before conducting real experiments. Applicable when you have chemical formulas or peak properties (mass, intensity, retention time) for analytes and want to simulate realistic instrument noise and MS/MS fragmentation patterns.

## When NOT to use

- Input is already a measured mzML file or real LC-MS/MS run—use this skill to generate synthetic data, not to process existing experimental data.
- You lack chemical formula information or peak-property definitions for your analytes—this skill requires quantitative input on mass, intensity, and retention time.
- You need to simulate small-molecule metabolites without fragmentation rules defined in SMITER's fragmentation models—currently supports peptides and modified nucleosides.

## Inputs

- peak-properties dictionary (mass, intensity, retention-time per analyte)
- CSV file with analyte properties (optional; converted via csv_to_peak_properties)
- fragmentation model object (e.g., PeptideFragmentor, nucleoside fragmentor)
- noise injector object (e.g., UniformNoiseInjector)
- general simulation parameters (gradient_length, instrument configuration)

## Outputs

- synthetic mzML file (LC-MS/MS run data)
- ground-truth dataset with known analyte composition and retention times

## How to apply

First, prepare peak-property definitions containing mass, intensity, and retention-time information for analytes—optionally converting from CSV using smiter.lib.csv_to_peak_properties. Second, instantiate a fragmentor object (e.g., fragmentation_functions.PeptideFragmentor for peptides or nucleoside fragmentation models) that defines how molecules fragment. Third, instantiate a noise generator (e.g., smiter.noise_functions.UniformNoiseInjector) to model instrument-specific or general m/z and intensity noise. Fourth, define general simulation parameters such as gradient_length and other instrument-configuration settings. Finally, call smiter.synthetic_mzml.write_mzml with the peak properties, noise injector, fragmentor, and general parameters to execute the simulation and write the output mzML file. The modular design allows both default models and custom implementations.

## Related tools

- **SMITER** (Python-based command-line tool that executes synthetic mzML generation via modular fragmentor, noise, and peak-property interfaces) — https://github.com/LeidelLab/SMITER
- **pyQms** (Provides highly-accurate isotopic patterns used in SMITER's mass calculation and synthetic spectrum generation) — https://github.com/pyQms/pyqms
- **Python** (Runtime and ecosystem for implementing custom fragmentation models, noise generators, and retention-time prediction modules)

## Examples

```
from smiter.synthetic_mzml import write_mzml; from smiter import fragmentation_functions, noise_functions; write_mzml(peak_properties=peaks_dict, noise_injector=noise_functions.UniformNoiseInjector(), fragmentor=fragmentation_functions.PeptideFragmentor(), gradient_length=30, output_file='synthetic.mzML')
```

## Evaluation signals

- Output mzML file is valid XML and conforms to mzML schema with expected scan structure, MS1/MS2 levels, and peaks sorted by m/z.
- Generated peak m/z values match input peak-properties mass values within expected isotopic-pattern and calibration tolerance.
- Intensity values in synthetic spectra reflect input intensities scaled by chosen feature distribution (Gaussian, gamma, or exponentially-modified Gaussian) and noise injector behavior.
- Fragmentation peaks in MS2 scans are consistent with selected fragmentor model (e.g., expected peptide fragment ion types present, nucleoside backbone cleavage patterns match model).
- Retention times in generated scans match input retention-time values for each analyte across the gradient_length interval without deviation.

## Limitations

- Fragmentation simulation currently limited to peptides (with several methods available) and two nucleoside fragmentation models; other biomolecule classes require custom fragmentor implementation.
- Accuracy of synthetic data depends on quality of input peak-property definitions (mass, intensity, retention time); errors or biased estimates propagate into output mzML.
- Noise models are approximations of real instrument behavior; UniformNoiseInjector and intensity-specific noise models may not capture all instrument-specific or matrix-dependent noise characteristics.
- No built-in retention-time prediction; retention times must be provided as input or predicted externally before peak-property preparation.

## Evidence

- [readme] SMITER enables the simulation of any biomolecule since all calculations are based on chemical formulas.: "SMITER (Synthetic mzML writer) is a python-based command-line tool designed to simulate LC-MS/MS runs. It enables the simulation of any biomolecule since all calculations are based on the chemical"
- [other] SMITER's write_mzml integrates peak properties, noise, and fragmentation models in a modular design.: "Call smiter.synthetic_mzml.write_mzml with the peak properties, noise injector, fragmentor, and general parameters to execute the simulation and write the output mzML file."
- [readme] Modular design allows custom implementations of fragmentation and noise models.: "As SMITER features a modular design, noise and fragmentation models can easily be implemented or adapted."
- [readme] Gold-standard datasets enable algorithm testing and analytical hurdle prediction.: "This allows for the facile creation of defined gold-standard-LC-MS/MS datasets for any type of experiment. Such gold standards, where the ground truth is known, are required in computational mass"
- [readme] Default noise and fragmentation models included; peptide and nucleoside fragmentation supported.: "By default, SMITER uses an established noise model and offers several methods for peptide fragmentation or two models for nucleoside fragmentation."
