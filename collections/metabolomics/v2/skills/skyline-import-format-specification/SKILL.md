---
name: skyline-import-format-specification
description: Use when you have computationally generated precursor m/z values, fragment m/z values, collision energies, and retention time predictions for a set of lipid targets (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0153
  tools:
  - Skyline
  - LipidCreator
derived_from:
- doi: 10.1038/s41467-020-15960-z
  title: LipidCreator
evidence_spans:
- LipidCreator is a plugin for Skyline supporting targeted workflow development in lipidomics
- LipidCreator is a plugin for [Skyline](https://skyline.ms/project/home/software/Skyline/begin.view) supporting targeted workflow development in lipidomics.
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
---

# Skyline Import Format Specification

## Summary

Specification and generation of tab-delimited or CSV target list files formatted for import into Skyline, including precursor m/z, fragment m/z, collision energy, polarity, and retention time window metadata. This skill ensures that computationally generated transition lists conform to Skyline's expected schema so that PRM and MRM experiments can be configured without manual reformatting.

## When to use

You have computationally generated precursor m/z values, fragment m/z values, collision energies, and retention time predictions for a set of lipid targets (e.g., from LipidCreator or similar in silico fragmentation tool) and need to import them into Skyline for method development or experiment configuration. The trigger is the availability of structured transition metadata that must be serialized into a format Skyline can parse.

## When NOT to use

- You are importing manually curated or vendor-supplied transition lists that are already in a Skyline-compatible format — reformatting is redundant.
- You need to perform retention time alignment or collision energy optimization; these are post-import refinement steps, not specification.
- Your input is raw MS/MS spectra or fragmentation data that has not yet been converted to structured transition metadata; you must first generate precursor/fragment m/z and collision energy values.

## Inputs

- Precursor m/z values (numeric, one per target lipid)
- Fragment m/z values (numeric, one or more per precursor)
- Collision energy values (numeric, non-negative, in eV or instrument-specific units)
- Polarity indicator (+1 or −1)
- Retention time predictions or windows (numeric, in minutes)
- Lipid identifiers or names (string, optional but recommended)

## Outputs

- Tab-delimited or CSV target list file compatible with Skyline import
- Skyline transition list object (after import into Skyline document)
- Optional: standalone fragment library file (.blib or .msp format)

## How to apply

Assemble transition metadata (precursor m/z, fragment m/z, collision energy, polarity, retention time window) into columns matching Skyline's import schema. Export as tab-delimited or CSV text file with headers. Verify that all required fields are populated, m/z values are numeric and within the instrument's range, collision energies are non-negative, polarity matches the acquisition mode (+1 or −1), and retention time windows are realistic (typically ±2–5 min). Import the file into Skyline via the native import dialog or programmatic interface. Skyline will validate the file structure and parse each row as a transition; incorrect formatting will raise parse errors before import completes. Confirm successful import by verifying that the number of transitions in Skyline matches the input file and that m/z values appear in the expected mass range.

## Related tools

- **Skyline** (Target platform for import; parses and validates tab-delimited or CSV transition lists and manages PRM/MRM experiment design) — https://skyline.ms/project/home/software/Skyline/begin.view
- **LipidCreator** (Generates precursor m/z, fragment m/z, collision energy, and retention time predictions for lipid targets; outputs formatted target lists compatible with Skyline import) — https://github.com/lifs-tools/lipidcreator

## Evaluation signals

- File parses without errors in Skyline import dialog; all rows are successfully parsed as valid transitions
- Number of transitions imported equals the number of rows in the input file
- Precursor and fragment m/z values fall within the expected instrument mass range (e.g., 50–2000 m/z for QExactive HF)
- Collision energy values are non-negative and within instrument-reported limits (typically 0–100 eV or normalized units 0–1)
- Retention time windows are realistic (e.g., 2–5 min, not spanning entire run); retention time predictions are congruent with expected elution order for lipid class and chain length

## Limitations

- Skyline's import format is proprietary and version-specific; files generated for Skyline 21.1 may not import correctly into older versions; check release notes for breaking changes.
- Collision energy values and retention time predictions are instrument and chromatographic method-dependent; values from one platform (e.g., Thermo QExactive HF) may not transfer directly to another (e.g., Agilent QTOF) without recalibration.
- Adduct ions (e.g., [M+H]+, [M+Na]+, [M−H]−) and lipid class-specific fragmentation rules are assumed to be correctly modeled in the upstream tool; systematic errors in precursor m/z or fragment assignment are not caught by Skyline's import validator.
- The README notes repainting and scrolling issues when running LipidCreator under Mono on Linux, which may affect usability but not import format compliance.

## Evidence

- [other] Generate precursor m/z values and retention time predictions for each lipid target. 3. Calculate expected fragment m/z values based on lipid fragmentation rules and chain cleavage patterns. 4. Assemble target list with precursor, fragment, and transition metadata. 5. Format output as tab-delimited or CSV target list file compatible with Skyline import (precursor m/z, fragment m/z, collision energy, polarity, retention time window).: "Format output as tab-delimited or CSV target list file compatible with Skyline import (precursor m/z, fragment m/z, collision energy, polarity, retention time window)."
- [readme] LipidCreator is a plugin for Skyline supporting targeted workflow development in lipidomics. It can be used to create user-defined target lists and fragment libraries for PRM and MRM experiments in Skyline.: "It can be used to create user-defined target lists and fragment libraries for PRM and MRM experiments in Skyline."
- [other] LipidCreator accepts lipid definitions as input and produces target lists and fragment libraries that are formatted for import into Skyline, enabling users to configure PRM and MRM targeted experiments.: "target lists and fragment libraries that are formatted for import into Skyline"
- [readme] It has been tested with Thermo QExactive HF and Agilent QTOF instruments.: "It has been tested with Thermo QExactive HF and Agilent QTOF instruments."
- [readme] Please note that there may be issues with the repainting of certain windows and controls (scrollable areas) due to the not 100% compatible Mono implementation.: "there may be issues with the repainting of certain windows and controls due to the not 100% compatible Mono implementation"
