---
name: mass-spectrometry-adduct-annotation
description: Use when you have mass spectrometry data from derivatized metabolite samples and need to automatically predict and validate the ion forms (e.g., [M+matrix_adduct]+) produced by a specific derivatizing matrix.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - RDKit
  - Met-ID
derived_from:
- doi: 10.1021/acs.analchem.5c00633
  title: metid
evidence_spans:
- Powered by RDKit
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metid
    doi: 10.1021/acs.analchem.5c00633
    title: metid
  dedup_kept_from: coll_metid
schema_version: 0.2.0
---

# mass-spectrometry-adduct-annotation

## Summary

Automated prediction and annotation of ion adducts produced by derivatizing matrices in mass spectrometry imaging, extending beyond common [M+H]+ and [M-H]− forms to support novel chemical matrices like FMP-10 and TAHS. This skill enables high-throughput metabolite identification by correctly mapping observed m/z peaks to their corresponding adduct forms.

## When to use

Use this skill when you have mass spectrometry data from derivatized metabolite samples and need to automatically predict and validate the ion forms (e.g., [M+matrix_adduct]+) produced by a specific derivatizing matrix. This is especially critical when working with non-standard matrices beyond [M+H]+ in positive mode or [M-H]− in negative mode, or when manual expert annotation is infeasible in high-throughput studies.

## When NOT to use

- Input data is limited to common [M+H]+ or [M-H]− ions without need for matrix-specific adduct prediction
- Derivatizing matrix composition and ionization behavior are not documented or cannot be parameterized in a configuration file
- Manual expert annotation is already complete and no high-throughput automation is required

## Inputs

- Mass spectrometry imaging data (m/z values and intensities)
- Metabolite structure database or known chemical standards
- Derivatizing matrix configuration (composition, ionization parameters, expected adduct forms)
- MS2 spectra from chemical standards (optional, for validation)

## Outputs

- Adduct annotations mapping observed m/z peaks to molecular ions and their characteristic adduct forms
- Confidence scores or validation metrics comparing predictions against ground-truth adducts
- Annotated metabolite identifications with ion type assignments (e.g., [M+matrix_adduct]+)

## How to apply

First, register your derivatizing matrix in Met-ID's configuration system by creating a configuration file or plugin module specifying the matrix composition, ionization behavior, and expected adduct forms (e.g., TAHS or other documented reagents). Next, run Met-ID on a test set of metabolites with known derivatization behavior using the newly registered matrix. Parse Met-ID's output to extract predicted adduct annotations and verify that they match the expected ion forms produced by your matrix. Finally, compare the predicted adducts against ground-truth or literature-reported adducts for your test metabolites using RDKit-powered structure analysis to confirm that the matrix configuration correctly recognizes and applies the derivatizing chemistry.

## Related tools

- **Met-ID** (Core software platform that automates metabolite identification in mass spectrometry imaging with extensible support for multiple derivatizing matrices and adduct form prediction via RDKit-powered structure analysis) — https://github.com/pbjarterot/Met-ID
- **RDKit** (Cheminformatics engine used by Met-ID to parse molecular structures, predict ionization behavior, and compute expected adduct forms for registered derivatizing matrices)

## Evaluation signals

- Predicted adduct annotations match ground-truth or literature-reported adducts for test metabolites with ≥90% accuracy
- Output adduct forms conform to the registered matrix configuration (e.g., [M+matrix_adduct]+ for the specified matrix)
- MS2 spectra from unknown compounds show characteristic fragmentation patterns consistent with the assigned adduct type when compared to standards
- No spurious adduct assignments occur; all predicted ions have documented ionization pathways for the registered derivatizing matrix
- Validation metrics (e.g., cosine similarity between predicted and observed MS2 spectra) fall within expected ranges for your matrix chemistry

## Limitations

- Met-ID is under active development and database files may require manual removal and reinstallation when updating versions (on Windows: 'com.farmbio.metid' folder in AppData/Roaming; on macOS: Library/Application Support; similar paths on Linux)
- Some macOS functionality issues with adding functional groups are noted and under active development
- Adduct prediction accuracy depends critically on accurate parameterization of matrix composition and ionization behavior; undocumented or poorly characterized matrices may not be reliably extended
- The base version includes MS2 spectra only for FMP-10-derivatized standards collected on FT-ICR instruments; other matrix-specific spectral libraries must be user-generated

## Evidence

- [readme] Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]− in negative mode: "Met-ID has a particular focus on derivatizing matrices leading to other ions than the common [M+H]+ in positive mode and [M-H]− in negative mode"
- [other] Met-ID has been designed with extensibility in mind to support any derivatizing matrix, not limited to FMP-10: "Met-ID is extendable to use any derivatizing matrix with the tools to do local version changes right from inside the software"
- [other] Create a configuration for a second derivatizing matrix, specifying composition, ionization, and expected adducts: "Create a configuration file or plugin module for the second derivatizing matrix (TAHS or similar publicly documented reagent), specifying the matrix composition, ionization behavior, and expected"
- [other] Verify adduct annotations match expected ions and compare against ground truth: "Compare predicted adducts against ground truth or literature-reported adducts for the test metabolites to confirm correct recognition and application"
- [readme] Manual metabolite identification in high-throughput studies is not feasible: "most of this is done manually by experts which in the world of high throughput studies is not feasable"
