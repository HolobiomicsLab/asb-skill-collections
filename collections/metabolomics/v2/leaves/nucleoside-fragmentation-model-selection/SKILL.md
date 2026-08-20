---
name: nucleoside-fragmentation-model-selection
description: Use when when your input biomolecule is a nucleoside or modified nucleoside
  (not a peptide) and you are building a synthetic LC-MS/MS run with SMITER.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - SMITER
  - Python
  - pyQms
  techniques:
  - LC-MS
  license_tier: open
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

# nucleoside-fragmentation-model-selection

## Summary

Select and instantiate a nucleoside-specific fragmentation model from SMITER's modular fragmentation interface to replace the default peptide fragmentor in LC-MS/MS simulation workflows. This skill enables accurate synthetic spectrum generation for nucleoside and modified nucleoside compounds by leveraging SMITER's domain-specific fragmentation strategies.

## When to use

When your input biomolecule is a nucleoside or modified nucleoside (not a peptide) and you are building a synthetic LC-MS/MS run with SMITER. Use this skill when you have nucleoside molecular data in CSV format and need to generate realistic MS2 fragmentation patterns specific to nucleoside chemistry rather than peptide cleavage rules.

## When NOT to use

- Input biomolecule is a peptide — use the default PeptideFragmentor instead.
- Input is already a finalized experimental mzML file — this skill is for synthetic spectrum generation, not post-processing.
- Nucleoside modification profile is not covered by either of SMITER's two nucleoside fragmentation models — consider implementing a custom fragmentor via SMITER's modular interface.

## Inputs

- CSV file with nucleoside molecular data (chemical formula, m/z, intensity, retention time)
- Nucleoside fragmentor class instantiation (e.g., NucleosideFragmentor)
- Noise generator (e.g., smiter.noise_functions.UniformNoiseInjector)
- Gradient length parameter (float, minutes)

## Outputs

- mzML file containing synthetic LC-MS/MS run with nucleoside-specific fragmentation patterns
- Peak properties dictionary with fragmentation annotations

## How to apply

After loading nucleoside peak properties via smiter.lib.csv_to_peak_properties from your input CSV, replace the default PeptideFragmentor with SMITER's NucleosideFragmentor class (or alternative nucleoside fragmentation model if available). Pass the selected nucleoside fragmentor to smiter.synthetic_mzml.write_mzml along with your noise injector, peak properties dictionary, and gradient parameters. The modular design allows you to choose between the two nucleoside fragmentation models that SMITER provides; consult the documentation or fragmentation_functions module to determine which model best matches your nucleoside modification profile. Verify model selection by inspecting the resulting mzML file to ensure MS2 spectra contain expected nucleoside-specific fragment ions (e.g., base loss, sugar fragmentation patterns) rather than peptide b/y ions.

## Related tools

- **SMITER** (Modular LC-MS/MS simulation framework providing nucleoside fragmentation models and the synthetic mzML writer interface.) — https://github.com/LeidelLab/SMITER
- **Python** (Programming language for instantiating fragmentor objects and invoking SMITER's library functions.)
- **pyQms** (Underlying library used by SMITER for highly-accurate isotopic pattern calculation.) — https://github.com/pyQms/pyqms

## Examples

```
from smiter.lib import csv_to_peak_properties; from smiter.fragmentation_functions import NucleosideFragmentor; from smiter.noise_functions import UniformNoiseInjector; from smiter import synthetic_mzml; peak_props = csv_to_peak_properties('nucleoside_data.csv'); fragmentor = NucleosideFragmentor(); noise = UniformNoiseInjector(); synthetic_mzml.write_mzml(fragmentor, noise, peak_props, gradient_length=30.0, output_file='synthetic_nucleoside.mzML')
```

## Evaluation signals

- Resulting mzML file contains MS2 spectra with fragment ions consistent with nucleoside fragmentation chemistry (e.g., base or sugar fragments) rather than peptide cleavage products.
- Fragment m/z values match theoretical predictions derived from the nucleoside chemical formula.
- Peak intensity distributions follow the specified noise model and gauss/gamma/exponentially-modified gaussian distributions for feature scaling.
- mzML file schema is valid and parseable by standard proteomics/metabolomics tools.
- Synthetic spectra intensity patterns reflect the input CSV intensity values after noise injection and fragmentation.

## Limitations

- SMITER offers only two nucleoside fragmentation models; if your nucleoside modification type is not covered by either, you must implement a custom fragmentor class via the modular interface.
- Fragmentation models are based on chemical formulas; unusual or non-standard modifications may not be accurately simulated without manual model extension.
- Retention time prediction is not included in the default SMITER workflow; advanced retention time modeling requires implementing external modules (e.g., dedicated retention time prediction libraries).

## Evidence

- [other] SMITER offers two models for nucleoside fragmentation alongside several peptide fragmentation methods, enabling modular selection of fragmentation strategies for different biomolecule types.: "SMITER offers two models for nucleoside fragmentation alongside several peptide fragmentation methods, enabling modular selection of fragmentation strategies for different biomolecule types."
- [other] Select a nucleoside fragmentor from SMITER's provided fragmentation models (e.g., NucleosideFragmentor class) instead of the default PeptideFragmentor.: "Select a nucleoside fragmentor from SMITER's provided fragmentation models (e.g., NucleosideFragmentor class) instead of the default PeptideFragmentor."
- [readme] As SMITER features a modular design, noise and fragmentation models can easily be implemented or adapted.: "As SMITER features a modular design, noise and fragmentation models can easily be implemented or adapted."
- [readme] By default, SMITER uses an established noise model and offers several methods for peptide fragmentation or two models for nucleoside fragmentation.: "By default, SMITER uses an established noise model and offers several methods for peptide fragmentation or two models for nucleoside fragmentation."
- [other] Run the simulation and write the resulting mzML using `smiter.synthetic_mzml.write_mzml`: "Run the simulation and write the resulting mzML using `smiter.synthetic_mzml.write_mzml`"
