---
name: in-silico-fragment-prediction
description: Use when you have a collection of compound structures in SDF format (e.g.,
  DNA adduct structures) and need to systematically generate predicted fragment spectra
  across a defined ionization level and mass range to populate a reference spectral
  database or validate experimental fragmentation patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - CFM-ID
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.3389/fchem.2022.908572
  title: DNA adduct database
evidence_spans:
- CFM-ID
- the CFM-ID spectra, the Chemdraw files, the mol files and the SDF files of the DNA
  adducts
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dna_adduct_database_cq
    doi: 10.3389/fchem.2022.908572
    title: DNA adduct database
  dedup_kept_from: coll_dna_adduct_database_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fchem.2022.908572
  all_source_dois:
  - 10.3389/fchem.2022.908572
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# in-silico-fragment-prediction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate predicted mass spectrometry fragment spectra computationally from compound chemical structures using CFM-ID, enabling rapid annotation and validation of experimental fragmentations for metabolites and DNA adducts without requiring wet-lab MS/MS experiments.

## When to use

Apply this skill when you have a collection of compound structures in SDF format (e.g., DNA adduct structures) and need to systematically generate predicted fragment spectra across a defined ionization level and mass range to populate a reference spectral database or validate experimental fragmentation patterns.

## When NOT to use

- Input compounds lack well-defined 2D/3D structure information — CFM-ID requires chemically valid structure representations
- Experimental fragment spectra are already available and validated — in-silico prediction is most useful for annotation of unknowns or high-throughput reference generation, not as a replacement for experimental data
- The goal is to identify which compounds are present in a sample — use this skill for spectral reference building, not for sample analysis

## Inputs

- SDF format compound structure file containing molecular structures (e.g., DNA adduct compounds)

## Outputs

- Structured predicted fragment spectra database indexed by compound identifier
- Individual predicted MS/MS spectra for each input compound

## How to apply

Load all compound structures from an SDF format file containing your target compounds. Execute CFM-ID on each structure, specifying the appropriate ionization level and mass range relevant to your compounds. Compile the resulting predicted fragment spectra into a structured database matching the schema of your target resource (e.g., matching the format of online predicted-fragments databases). Validate completeness by confirming that all input compounds from the SDF file have corresponding predicted spectra entries in the output database.

## Related tools

- **CFM-ID** (In-silico fragment spectrum prediction engine that processes compound structures and generates predicted MS/MS spectra at specified ionization levels)

## Evaluation signals

- All compounds in the input SDF file have exactly one corresponding entry in the output predicted fragments database
- Predicted spectra follow expected mass fragmentation patterns consistent with the chemical structure and ionization method (no negative masses, fragments within specified mass range)
- Output database schema matches the format of the target resource (e.g., predicted-fragments online database format) with required fields populated
- Predicted spectra can be successfully cross-matched against experimental spectra using standard metrics (e.g., cosine similarity with experimental MS/MS data when available)

## Limitations

- CFM-ID prediction accuracy depends on compound structure quality and chemical validity; invalid or poorly-drawn structures produce unreliable spectra
- Predicted spectra represent gas-phase fragmentation patterns and may not fully capture solution-phase or matrix-dependent effects observed in experimental data
- The skill requires specification of correct ionization level and mass range parameters; misaligned parameters will generate spectra outside the relevant analytical window

## Evidence

- [other] Load compound structures from the SDF format file containing DNA adduct compounds: "Load compound structures from the SDF format file containing DNA adduct compounds"
- [other] Execute CFM-ID on each compound structure to predict fragment spectra at the appropriate ionization level and mass range: "Execute CFM-ID on each compound structure to predict fragment spectra at the appropriate ionization level and mass range"
- [other] Compile predicted fragment spectra into a structured database matching the format of the deposited predicted-fragments online resource: "Compile predicted fragment spectra into a structured database matching the format of the deposited predicted-fragments online resource"
- [other] Validate output by confirming all input compounds have corresponding predicted spectra entries: "Validate output by confirming all input compounds have corresponding predicted spectra entries"
- [other] The in-silico fragment prediction stage uses CFM-ID to process SDF compound structures and generate predicted fragment spectra: "The in-silico fragment prediction stage uses CFM-ID to process SDF compound structures and generate predicted fragment spectra"
