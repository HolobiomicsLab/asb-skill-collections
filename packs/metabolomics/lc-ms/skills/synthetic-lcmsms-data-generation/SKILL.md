---
name: synthetic-lcmsms-data-generation
description: Use when you need to create defined LC-MS/MS datasets with known molecular composition and fragmentation patterns for algorithm validation, method development, or evaluation of analytical challenges (e.g., co-elution prediction).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# synthetic-lcmsms-data-generation

## Summary

Generate gold-standard synthetic LC-MS/MS datasets with known ground truth by simulating mass spectrometry runs for any biomolecule using chemical formula-based calculations, modular fragmentation models, and configurable noise injection. This enables controlled testing of MS algorithms and evaluation of co-elution/co-fragmentation challenges before performing actual experiments.

## When to use

You need to create defined LC-MS/MS datasets with known molecular composition and fragmentation patterns for algorithm validation, method development, or evaluation of analytical challenges (e.g., co-elution prediction). Typical triggers: testing new MS data processing algorithms, benchmarking peak detection or quantification methods, or studying effects of co-fragmenting molecules on detection sensitivity where experimental ground truth is not readily available.

## When NOT to use

- You need to process or analyze real experimental LC-MS/MS data—SMITER generates synthetic data only, not analysis tools.
- Your biomolecules cannot be accurately represented by chemical formulas (e.g., undefined posttranslational modifications not in the model).
- You already have reliable ground-truth LC-MS/MS datasets and do not need synthetic gold standards.

## Inputs

- CSV file with molecular data (formula, retention time, intensity per molecule)
- Fragmentor class (e.g., PeptideFragmentor or NucleosideFragmentor)
- Noise generator object (e.g., UniformNoiseInjector)
- Simulation parameters (gradient_length, etc.)

## Outputs

- mzML file containing simulated LC-MS/MS run with MS1 and MS2 spectra
- Synthetic peak list with isotopic patterns and fragmentation products

## How to apply

Load biomolecule molecular data (chemical formulas, retention times, intensities) from a CSV file and convert to peak properties dictionary using `smiter.lib.csv_to_peak_properties`. Select an appropriate fragmentor module—either PeptideFragmentor for peptides or NucleosideFragmentor for nucleosides—since SMITER offers several peptide fragmentation methods and two nucleoside models. Choose a noise injector (e.g., `UniformNoiseInjector` or the default intensity-specific noise model). Define simulation parameters including LC gradient length. Execute the simulation via `smiter.synthetic_mzml.write_mzml`, passing the fragmentor, noise injector, peak properties, and gradient parameters. The tool generates mzML output with isotopic patterns calculated by pyQms, feature intensity scaling (Gaussian, gamma, or exponentially-modified Gaussian distributions), and m/z or intensity noise, producing a complete synthetic LC-MS/MS run.

## Related tools

- **SMITER** (Command-line and Python library for simulation of LC-MS/MS runs and mzML file generation) — https://github.com/LeidelLab/SMITER
- **pyQms** (Provides highly-accurate isotopic pattern calculations used within SMITER) — https://github.com/pyQms/pyqms
- **Python** (Runtime environment and scripting language for SMITER workflows)

## Examples

```
from smiter.lib import csv_to_peak_properties
from smiter.fragmentation_functions import NucleosideFragmentor
from smiter.noise_functions import UniformNoiseInjector
from smiter.synthetic_mzml import write_mzml
peak_props = csv_to_peak_properties('nucleosides.csv')
write_mzml(peak_properties=peak_props, fragmentor=NucleosideFragmentor(), noise_injector=UniformNoiseInjector(), gradient_length=30, output_path='synthetic_run.mzML')
```

## Evaluation signals

- Output mzML file is valid and can be parsed by standard MS data readers (e.g., mzML validators).
- Generated LC-MS/MS spectra contain expected isotopic patterns consistent with input chemical formulas.
- MS2 fragmentation products match the selected fragmentor model (e.g., peptide backbone cleavages for peptides, nucleoside ring openings for nucleosides).
- Noise level and intensity distribution match configured noise model parameters (e.g., signal-to-noise ratio consistent with UniformNoiseInjector settings).
- Peak retention times and m/z values correspond to input molecular data within numerical precision.

## Limitations

- Simulation accuracy depends on correctness of input chemical formulas and fragmentor model parameterization; errors in these inputs propagate to synthetic data.
- SMITER currently offers limited fragmentation models (several for peptides, two for nucleosides); other biomolecule types or unusual fragmentation patterns require custom fragmentor implementation.
- Synthetic datasets lack real-world complexity such as unexpected adducts, instrument artifacts, or rare fragmentation pathways not captured in the model.
- No changelog is available, limiting traceability of model updates or bug fixes across versions.

## Evidence

- [readme] This allows for the facile creation of defined gold-standard-LC-MS/MS datasets for any type of experiment.: "This allows for the facile creation of defined gold-standard-LC-MS/MS datasets for any type of experiment."
- [other] SMITER offers two models for nucleoside fragmentation alongside several peptide fragmentation methods, enabling modular selection of fragmentation strategies for different biomolecule types.: "SMITER offers several methods for peptide fragmentation or two models for nucleoside fragmentation."
- [other] Workflow steps from the indexed article for nucleoside simulation.: "Create a peak properties dictionary from input CSV containing nucleoside molecular data using smiter.lib.csv_to_peak_properties"
- [readme] It enables the simulation of any biomolecule since all calculations are based on the chemical formulas.: "It enables the simulation of any biomolecule since all calculations are based on the chemical formulas."
- [readme] As SMITER features a modular design, noise and fragmentation models can easily be implemented or adapted.: "As SMITER features a modular design, noise and fragmentation models can easily be implemented or adapted."
- [other] Specification of the final mzML writing step in the workflow.: "Run the simulation and write the resulting mzML using `smiter.synthetic_mzml.write_mzml`"
