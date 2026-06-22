---
name: modular-fragmentor-interface-configuration
description: Use when you need to simulate LC-MS/MS spectra for a specific biomolecule type (peptides, modified nucleosides, or other metabolites) and must choose which fragmentation model governs how parent ions break into fragment ions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - SMITER
  - Python
  - pyQms
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# modular-fragmentor-interface-configuration

## Summary

Configure SMITER's pluggable fragmentation interface to select and instantiate biomolecule-specific fragmentation models (peptide or nucleoside) for LC-MS/MS synthetic spectrum generation. This skill enables switching between fragmentation strategies without altering the core simulation pipeline.

## When to use

You need to simulate LC-MS/MS spectra for a specific biomolecule type (peptides, modified nucleosides, or other metabolites) and must choose which fragmentation model governs how parent ions break into fragment ions. Use this skill when the default PeptideFragmentor is inappropriate for your target molecule class, or when you want to compare outputs across multiple fragmentation strategies.

## When NOT to use

- You have experimental LC-MS/MS data already and need to interpret it; use this skill only for generating synthetic ground-truth datasets, not for analyzing real spectra.
- Your biomolecule type is not peptides or nucleosides and no custom fragmentor has been implemented; SMITER's current built-in models do not cover all metabolite classes.
- You require retention time prediction or advanced adduct modeling beyond fragmentation; those require separate SMITER extensions or external modules.

## Inputs

- peak properties dictionary (dict with molecular formula, m/z, retention time, abundance per compound)
- fragmentor class or instance (e.g., NucleosideFragmentor or PeptideFragmentor)
- noise injector instance (e.g., UniformNoiseInjector)
- gradient parameters (dict with gradient_length and other LC method details)

## Outputs

- synthetic mzML file with MS1 and MS2 scans reflecting the selected fragmentation model
- fragment ion lists (m/z and intensity) specific to chosen fragmentor strategy

## How to apply

After loading peak properties from your input CSV via smiter.lib.csv_to_peak_properties, inspect the molecular composition to determine the correct fragmentor class. SMITER provides NucleosideFragmentor and several PeptideFragmentor variants; select the one matching your biomolecule type. Instantiate the chosen fragmentor and pass it to smiter.synthetic_mzml.write_mzml alongside your noise injector, peak properties dictionary, and gradient parameters. The modular design allows fragmentation logic to be swapped at configuration time without modifying simulation or file I/O code. Verify correctness by inspecting the resulting mzML file's MS/MS scan fragmentation patterns — peptide fragmentors should show characteristic b- and y-ion ladders, while nucleoside fragmentors should exhibit base-loss and glycosidic cleavage patterns specific to nucleoside chemistry.

## Related tools

- **SMITER** (Synthetic LC-MS/MS simulator; provides modular fragmentation interface, peak property handling, noise injection, and mzML output) — https://github.com/LeidelLab/SMITER
- **Python** (Runtime environment for instantiating fragmentor classes and calling SMITER library functions) — https://www.python.org
- **pyQms** (Upstream dependency used by SMITER for accurate isotopic pattern calculation during spectrum simulation) — https://github.com/pyQms/pyqms

## Examples

```
from smiter.fragmentation_functions import NucleosideFragmentor; from smiter.noise_functions import UniformNoiseInjector; from smiter.lib import csv_to_peak_properties; fragmentor = NucleosideFragmentor(); noise = UniformNoiseInjector(); peak_props = csv_to_peak_properties('nucleosides.csv'); smiter.synthetic_mzml.write_mzml(fragmentor, noise, peak_props, gradient_length=30, output_file='synthetic_nucleosides.mzML')
```

## Evaluation signals

- The resulting mzML file contains MS/MS scans with fragment peaks; absence of MS/MS data or empty scans indicates fragmentor was not invoked.
- Fragment m/z values match expected cleavage products for the chosen fragmentor type (e.g., b/y ions for peptides, loss of ribose/base for nucleosides).
- Fragmentation intensity distribution reflects the fragmentor's model (e.g., exponential decay vs. uniform); visual inspection of TIC and extracted ion chromatograms should show realistic feature shapes defined by the noise and fragmentor parameters.
- Switching fragmentor class (e.g., PeptideFragmentor → NucleosideFragmentor) produces visibly different MS/MS fragmentation patterns in the same mzML file structure, confirming modularity.
- mzML schema validation passes and the file can be parsed by standard tools (e.g., pymzML, msconvert); invalid fragmentor configuration or missing parameters should fail at write_mzml invocation.

## Limitations

- Only peptide and nucleoside fragmentors are built-in; other biomolecule classes (lipids, carbohydrates, metabolites) require custom fragmentor implementation.
- Fragmentation models are rule-based approximations; simulated spectra may not capture rare fragmentation pathways or instrument-specific quirks present in real LC-MS/MS runs.
- No built-in retention time prediction; gradient_length and other LC parameters are user-specified and do not account for actual column chemistry or sample properties.
- Noise models (uniform and intensity-specific) are simplified; real instrument noise, especially in ion traps or high-resolution orbitrap systems, may be more complex.

## Evidence

- [other] SMITER offers two models for nucleoside fragmentation alongside several peptide fragmentation methods, enabling modular selection of fragmentation strategies for different biomolecule types.: "SMITER offers two models for nucleoside fragmentation alongside several peptide fragmentation methods, enabling modular selection of fragmentation strategies for different biomolecule types."
- [readme] As SMITER features a modular design, noise and fragmentation models can easily be implemented or adapted.: "As SMITER features a modular design, noise and fragmentation models can easily be implemented or adapted."
- [other] Select a nucleoside fragmentor from SMITER's provided fragmentation models (e.g., NucleosideFragmentor class) instead of the default PeptideFragmentor.: "Select a nucleoside fragmentor from SMITER's provided fragmentation models (e.g., NucleosideFragmentor class) instead of the default PeptideFragmentor."
- [other] Execute the simulation and write the resulting synthetic LC-MS/MS run to mzML format using smiter.synthetic_mzml.write_mzml, passing the nucleoside fragmentor, noise injector, peak properties, and gradient parameters.: "Execute the simulation and write the resulting synthetic LC-MS/MS run to mzML format using smiter.synthetic_mzml.write_mzml, passing the nucleoside fragmentor, noise injector, peak properties, and"
- [readme] By default, SMITER uses an established noise model and offers several methods for peptide fragmentation or two models for nucleoside fragmentation.: "By default, SMITER uses an established noise model and offers several methods for peptide fragmentation or two models for nucleoside fragmentation."
