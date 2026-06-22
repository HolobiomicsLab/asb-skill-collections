---
name: lipid-fragmentation-pattern-application
description: Use when you have an enumerated list of lipid species (identified by class, fatty acid composition, and chain length) and need to generate theoretical precursor m/z values, fragment ion masses, and relative intensities for targeted or untargeted lipidomics experiments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - LSG (Lipid Spectrum Generator)
  - Excalibur
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.2c04518
  title: Lipid Spectrum Generator
evidence_spans:
- https://github.com/98104781/LSG/releases/tag/v1.3.0
- Excalibur compatible precursor list (for DDA analysis via orbitrap)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipid_spectrum_generator_cq
    doi: 10.1021/acs.analchem.2c04518
    title: Lipid Spectrum Generator
  dedup_kept_from: coll_lipid_spectrum_generator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04518
  all_source_dois:
  - 10.1021/acs.analchem.2c04518
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-fragmentation-pattern-application

## Summary

This skill applies peer-reviewed lipid class- and adduct-specific fragmentation patterns to generate theoretical mass spectra for enumerated lipid species. It is used to create in silico spectral libraries for lipid identification via data-dependent acquisition (DDA) on high-resolution instruments.

## When to use

Apply this skill when you have an enumerated list of lipid species (identified by class, fatty acid composition, and chain length) and need to generate theoretical precursor m/z values, fragment ion masses, and relative intensities for targeted or untargeted lipidomics experiments. This is essential when preparing a spectral library for DDA analysis on Orbitrap instruments or when you need to predict fragmentation patterns for lipid–adduct combinations not yet measured empirically.

## When NOT to use

- Input lipid species lack defined class or fatty acid composition metadata; fragmentation cannot be assigned without this structural information.
- Empirical spectra from authentic standards are already available; in silico generation is unnecessary when ground truth data exists.
- Target instrument does not support the export format (MSP, CSV precursor lists, or Skyline transition lists); LSG output formats may not align with non-Orbitrap or non-DDA workflows.

## Inputs

- lipid species list (with lipid class, fatty acid chain composition, and chain length)
- adduct type specification ([M+H]+, [M+Na]+, [M−H]−, etc.)
- peer-reviewed fragmentation pattern rules for target lipid classes

## Outputs

- theoretical mass spectra (precursor m/z, fragment m/z values, relative intensities)
- spectral library in MSP format
- Excalibur-compatible precursor list (CSV) for DDA analysis

## How to apply

Begin by loading a validated lipid species list that specifies lipid class (e.g., PC, PE, TAG) and fatty acid composition (chain lengths and saturation). For each lipid species, enumerate all relevant adduct forms (e.g., [M+H]+, [M+Na]+, [M−H]−) based on your ionization mode. Apply the corresponding peer-reviewed fragmentation pattern for that lipid class and adduct type to calculate theoretical fragment m/z values and assign relative intensities based on known fragmentation rules (e.g., neutral losses, characteristic fragment ions). Construct complete mass spectra as m/z–intensity pairs for each lipid–adduct combination. Finally, export the spectral library in MSP format for spectral matching or as an Excalibur-compatible precursor list (CSV) for DDA scheduling on Orbitrap instruments.

## Related tools

- **LSG (Lipid Spectrum Generator)** (Primary tool for enumerating lipid species and applying peer-reviewed fragmentation patterns to generate theoretical spectra; handles adduct enumeration and exports in MSP or Excalibur-compatible CSV format.) — https://github.com/98104781/LSG/releases/tag/v1.3.0
- **Excalibur** (Target mass spectrometry control and data acquisition software on Orbitrap instruments; receives DDA precursor lists and transition lists exported by LSG for scheduling targeted lipid analysis.)

## Evaluation signals

- Verify that all enumerated lipid species have corresponding entries in the output spectral library with no missing m/z values or intensities.
- Confirm that precursor m/z values match theoretical calculations for each lipid–adduct combination (e.g., verify [M+H]+ = monoisotopic mass + 1.00783 Da within <5 ppm error on Orbitrap).
- Check that fragment m/z values conform to expected neutral losses and characteristic fragments for the lipid class (e.g., PC loss of 59 for trimethylamine, PE loss of 141 for phosphatidylethanolamine head group).
- Validate that relative intensities are ranked logically (precursor typically 10–100%, base peak = 100%, minor fragments <10%).
- Confirm export format validity: MSP files parse without error in spectral matching software; CSV precursor lists load successfully into Excalibur with correct column structure and m/z precision.

## Limitations

- Fragmentation patterns are derived from peer-reviewed studies, which may not cover all lipid classes, rare saturation patterns, or uncommon adducts; coverage depends on literature availability.
- In silico spectra assume idealized fragmentation and may not capture instrument-specific variation in relative intensities or unexpected fragment ions observed in real mass spectra.
- Precursor intensity predictions are approximate and do not account for chromatographic or ionization efficiency differences across lipid species.
- Export to Skyline-compatible transition lists is mentioned but not detailed in this context; validation of Skyline compatibility is beyond the scope of this documentation.

## Evidence

- [readme] Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts.: "Lipids are generated with respect to class and fatty acid composition, spectra are then generated with respect to their adducts."
- [readme] The fragmentation patterns used to generate the spectra are based on peer-reviewed studies.: "The fragmentation patterns used to generate the spectra are based on peer-reviewed studies."
- [other] Spectra are generated with respect to lipid adducts using fragmentation patterns based on peer-reviewed studies.: "Spectra are generated with respect to lipid adducts using fragmentation patterns based on peer-reviewed studies."
- [other] For each lipid species, enumerate all relevant adduct forms (e.g., [M+H]+, [M+Na]+, [M−H]−).: "For each lipid species, enumerate all relevant adduct forms (e.g., [M+H]+, [M+Na]+, [M−H]−)."
- [readme] Spectral libraries can be exported with the file extension '.MSP' selected. Otherwise, an Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may be exported: "Spectral libraries can be exported with the file extension '.MSP' selected. Otherwise, an Excalibur compatible precursor list (for DDA analysis via orbitrap) or Skylike compatible transition list may"
