---
name: targeted-transition-list-generation
description: Use when you have a set of lipid targets defined by species name, acyl chain composition, and expected adducts, and you need to configure a targeted mass spectrometry workflow (PRM or MRM) in Skyline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - Skyline
  - LipidCreator
  - Thermo QExactive HF
  - Agilent QTOF
derived_from:
- doi: 10.1038/s41467-020-15960-z
  title: LipidCreator
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidcreator_cq
    doi: 10.1038/s41467-020-15960-z
    title: LipidCreator
  dedup_kept_from: coll_lipidcreator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-020-15960-z
  all_source_dois:
  - 10.1038/s41467-020-15960-z
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# targeted-transition-list-generation

## Summary

Generate user-defined precursor-to-fragment transition lists and spectral libraries from lipid definitions for targeted proteomics experiments (PRM/MRM). This skill automates the conversion of lipid species, chain compositions, and adduct specifications into Skyline-compatible transition metadata (m/z values, collision energies, retention time windows).

## When to use

Use this skill when you have a set of lipid targets defined by species name, acyl chain composition, and expected adducts, and you need to configure a targeted mass spectrometry workflow (PRM or MRM) in Skyline. Typical triggers: designing a lipidomics assay, transitioning from discovery to targeted analysis, or scaling a lipid panel to new instrument platforms (Thermo QExactive HF, Agilent QTOF).

## When NOT to use

- Your lipid targets are already in a Skyline project file (.sky) or a pre-formatted transition list — use direct import instead of re-generating.
- You have only nominal mass data or insufficient chain-level annotation — the tool requires explicit acyl chain composition to calculate fragment m/z accurately.
- Your workflow is untargeted (discovery mode) and does not require predefined transition lists — use data-dependent acquisition workflows instead.

## Inputs

- lipid definitions (species name, chain composition, adduct type)
- input specification file (text or structured format listing target lipids)
- instrument configuration (ionization polarity, m/z range, collision energy normalization)

## Outputs

- tab-delimited or CSV transition list (precursor m/z, fragment m/z, collision energy, polarity, retention time window per row)
- Skyline-compatible target list file
- spectral library file (.blib or .msp format) for fragment matching

## How to apply

Parse the lipid definitions (species, chain composition, adducts) from an input specification file. For each lipid target, calculate precursor m/z values and apply retention time prediction models. Using lipid-class-specific fragmentation rules and chain cleavage patterns, compute expected fragment m/z values for each transition. Assemble a target list table containing precursor m/z, fragment m/z, collision energy, polarity, and retention time windows. Export as tab-delimited or CSV format compatible with Skyline import, or generate a standalone fragment library file (.blib or .msp) for spectral matching. Validate that all transitions fall within the instrument's m/z range and that collision energies match the instrument's normalization scheme.

## Related tools

- **Skyline** (Primary interface for importing and managing transition lists; host environment for LipidCreator plugin; visualization and curation of precursor-fragment pairs and collision energies) — https://skyline.ms/project/home/software/Skyline/begin.view
- **LipidCreator** (Standalone and command-line tool that generates target lists and fragment libraries from lipid definitions; can run as Skyline plugin or as independent executable) — https://github.com/lifs-tools/lipidcreator
- **Thermo QExactive HF** (Tested target instrument platform; collision energy and m/z calibration reference for transition validation)
- **Agilent QTOF** (Tested target instrument platform; collision energy and m/z calibration reference for transition validation)

## Evaluation signals

- All precursor m/z values fall within the instrument's specified m/z range and match theoretical values for the lipid species and adduct type (±5 ppm for high-resolution instruments).
- Fragment m/z values match predicted cleavage patterns for the acyl chain composition (fatty acid chain losses, headgroup fragments) with no impossible or duplicate transitions.
- Collision energy values are assigned appropriately for the instrument's normalization scheme and match expected ranges for the lipid class and precursor charge.
- Retention time windows are assigned and are consistent with the lipid class or user-provided predictions (e.g., 2–3 min windows for reversed-phase separation).
- Output file format is correctly parsed by Skyline with no import errors; precursor and fragment m/z columns are numeric and polarity is correctly encoded.

## Limitations

- Retention time prediction accuracy depends on the availability and quality of calibration standards; predictions may diverge significantly across different LC methods or lipid standards not represented in the training set.
- Fragmentation rule coverage is limited to common lipid classes and chain compositions; unusual or oxidized lipids may not generate accurate fragment m/z predictions.
- Collision energy recommendations are approximate and may require manual tuning for new instrument platforms or LC–MS configurations not in the tested set (Thermo QExactive HF, Agilent QTOF).
- The tool does not account for isotopic variants or in-source rearrangements; practitioners must manually filter or annotate such variants.
- Linux/Ubuntu and macOS builds rely on Mono framework, which has partial UI compatibility issues affecting window repainting in scrollable areas; command-line mode is recommended for non-Windows platforms.

## Evidence

- [readme] LipidCreator is a plugin for Skyline supporting targeted workflow development in lipidomics.: "LipidCreator is a plugin for [Skyline](https://skyline.ms/project/home/software/Skyline/begin.view) supporting targeted workflow development in lipidomics."
- [readme] It can be used to create user-defined target lists and fragment libraries for PRM and MRM experiments in Skyline.: "It can be used to create user-defined target lists and fragment libraries for PRM and MRM experiments in Skyline."
- [other] Parse lipid definitions, generate precursor m/z and retention time predictions, calculate fragment m/z from fragmentation rules, and assemble a Skyline-compatible output.: "Parse lipid definitions (species, chain composition, adducts) from input specification. 2. Generate precursor m/z values and retention time predictions for each lipid target. 3. Calculate expected"
- [other] Output formatted as tab-delimited or CSV compatible with Skyline import or as standalone spectral library.: "Format output as tab-delimited or CSV target list file compatible with Skyline import (precursor m/z, fragment m/z, collision energy, polarity, retention time window). 6. Optionally generate"
- [readme] Tested with Thermo QExactive HF and Agilent QTOF instruments.: "It has been tested with Thermo QExactive HF and Agilent QTOF instruments."
- [readme] Supports standalone and command-line operation in addition to Skyline plugin mode.: "It also supports standalone and command-line operation."
- [readme] On Linux, locate the directory containing LipidCreator.exe, open a terminal and run with Mono framework.: "To run LipidCreator, locate the directory containing LipidCreator.exe, open a terminal and type mono LipidCreator.exe"
