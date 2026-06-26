---
name: virtual-mass-spectrometer-configuration
description: Use when when you have generated or extracted a chemical mixture (via
  DatabaseFormulaSampler, ChemicalMixtureCreator, or ChemicalMixtureFromMZML) and
  need to establish a virtual instrument to simulate scan acquisition.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ViMMS
  - ChemicalMixtureFromMZML
  - TopNController
  - IndependentMassSpectrometer
  - Environment
  - ChemicalMixtureCreator
  - DatabaseFormulaSampler
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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

# Virtual Mass Spectrometer Configuration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Configure an IndependentMassSpectrometer instance with ionization polarity and chemical mixture composition to enable realistic full-scan or tandem MS acquisition simulation. This is the foundational step for prototyping fragmentation strategies in ViMMS before testing on real LC-MS/MS hardware.

## When to use

When you have generated or extracted a chemical mixture (via DatabaseFormulaSampler, ChemicalMixtureCreator, or ChemicalMixtureFromMZML) and need to establish a virtual instrument to simulate scan acquisition. Specifically: use this skill when you are ready to move from chemical definition to instrument simulation, and before you instantiate a controller (e.g., FullScanController, TopNController) and Environment loop.

## When NOT to use

- You have not yet defined or extracted a chemical mixture—define chemicals first using DatabaseFormulaSampler or ChemicalMixtureFromMZML.
- You intend only to analyze or reprocess real experimental mzML data without simulation—use direct mzML parsing tools instead.
- Your chemicals lack defined fragmentation parameters or retention time ranges—the mass spectrometer requires these to generate realistic scans.

## Inputs

- ChemicalMixtureCreator instance (with ms_levels and retention time range defined)
- ChemicalMixtureFromMZML instance (ROIs extracted from real mzML with MS levels ≥ 2)
- Ionization polarity flag (positive or negative mode)

## Outputs

- IndependentMassSpectrometer object (ready for Environment instantiation)
- Virtual instrument configured with supplied chemicals and ionization state

## How to apply

Instantiate an IndependentMassSpectrometer with your prepared chemical mixture and specify the ionization polarity (positive or negative). The mass spectrometer object serves as the scanning engine that will generate realistic MS1 and MS2 spectra based on the fragmentation parameters of the supplied chemicals. Set the polarity according to your experimental design—beer or HMDB metabolite samples are typically analyzed in positive mode. The mass spectrometer is then passed to an Environment instance (along with a chosen controller) to execute the acquisition loop. Validation occurs at runtime: confirm that the mass spectrometer generates scans with expected m/z ranges (e.g., 100–1000 for HMDB sampling) and realistic intensity distributions matching the input chemical composition.

## Related tools

- **ViMMS** (Framework providing IndependentMassSpectrometer class and acquisition environment simulation) — https://github.com/glasgowcompbio/vimms
- **ChemicalMixtureCreator** (Generates chemical mixture input for mass spectrometer configuration) — https://github.com/glasgowcompbio/vimms
- **ChemicalMixtureFromMZML** (Extracts ROI-based UnknownChemical objects from real mzML to supply to mass spectrometer) — https://github.com/glasgowcompbio/vimms
- **DatabaseFormulaSampler** (Samples molecular formulas from HMDB to seed ChemicalMixtureCreator input) — https://github.com/glasgowcompbio/vimms
- **Environment** (Receives configured mass spectrometer and controller; orchestrates acquisition loop) — https://github.com/glasgowcompbio/vimms

## Examples

```
from vimms.MassSpec import IndependentMassSpectrometer; from vimms.Chemicals import ChemicalMixtureCreator; chemicals = ChemicalMixtureCreator(num_chemicals=100, ms_levels=2); ms = IndependentMassSpectrometer(chemicals, polarity='positive'); env = Environment(ms, controller, min_rt=0, max_rt=1440); env.run(); env.write_mzML('simulated_output.mzML')
```

## Evaluation signals

- Mass spectrometer object instantiates without error and retains reference to all supplied chemicals
- Output scans generated by Environment.run() span the expected m/z range (e.g., 100–1000 for HMDB samples)
- MS1 and MS2 spectra intensity distributions and fragmentation patterns match the chemical mixture composition (e.g., correct precursor m/z, expected fragment masses)
- Scans written to mzML via Environment.write_mzML() are structurally valid and parseable by external tools
- Ionization polarity is correctly reflected in written scans (positive or negative m/z values and ion counts)

## Limitations

- Mass spectrometer simulation assumes fragmentation parameters are accurate; incorrect chemical definitions or retention time windows will produce unrealistic scans.
- The simulator does not model detector saturation or mass calibration drift observed in real hardware; it provides idealized baseline performance.
- Performance scales with chemical mixture size; very large mixtures (e.g., >100k chemicals) may incur long Environment.run() times.
- Polarity setting is fixed at configuration time; switching polarities requires instantiating a new IndependentMassSpectrometer.

## Evidence

- [other] Instantiate an IndependentMassSpectrometer in positive ionization mode with the extracted chemicals: "Instantiate an IndependentMassSpectrometer in positive ionization mode with the extracted chemicals."
- [other] Use ChemicalMixtureCreator to generate a chemical mixture with ms_levels=1 (MS1 only): "Use ChemicalMixtureCreator to generate a chemical mixture with ms_levels=1 (MS1 only)."
- [readme] a flexible and modular framework designed to simulate fragmentation strategies: "a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics."
- [other] Create an Environment instance with the mass spectrometer, controller, and retention time range: "Create an Environment instance with the mass spectrometer, controller, and retention time range (e.g., min_rt=0, max_rt=1440)."
- [readme] You can generate new LC-MS/MS data based on empirical data or virtually replay a previous LC-MS/MS analysis using existing data: "You can generate new LC-MS/MS data based on empirical data or virtually replay a previous LC-MS/MS analysis using existing data, which allows for testing different fragmentation strategies."
