---
name: mass-spectrometry-prediction-modeling
description: Use when when you have a collection of compound structures in SDF format (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0599
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_2275
  tools:
  - CFM-ID
  techniques:
  - LC-MS
derived_from:
- doi: 10.3389/fchem.2022.908572
  title: DNA adduct database
evidence_spans:
- CFM-ID
- the CFM-ID spectra, the Chemdraw files, the mol files and the SDF files of the DNA adducts
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-prediction-modeling

## Summary

Use computational tools to predict fragment mass spectra from chemical compound structures, enabling in-silico annotation and reference library construction for untargeted metabolomics and adductomics. This skill bridges structural chemistry with experimental MS data without requiring physical sample analysis.

## When to use

When you have a collection of compound structures in SDF format (e.g., DNA adducts, drug metabolites, xenobiotic conjugates) and need to generate reference fragmentation patterns at specific ionization levels and mass ranges to populate or validate predicted fragment spectral databases for untargeted MS screening.

## When NOT to use

- Input compounds lack defined chemical structures or contain only SMILES/InChI strings without 3D coordinate information needed by CFM-ID
- Experimental MS/MS spectra are already available and validated; prediction is redundant
- Target compounds are outside CFM-ID's chemical scope (e.g., highly charged biomolecules, organometallic complexes)

## Inputs

- SDF format file containing compound structures (2D or 3D coordinates)
- Ionization mode specification (e.g., positive, negative ESI)
- Target mass range (e.g., m/z window for fragment detection)

## Outputs

- Predicted fragment spectra database (structured, matching reference resource format)
- Per-compound predicted MS/MS spectral records with m/z and relative intensity values
- Validation report confirming input–output correspondence

## How to apply

Load compound structures from SDF files containing the target chemical entities. Execute CFM-ID on each structure, specifying the appropriate ionization mode (e.g., positive/negative ESI) and mass range window relevant to your analytical platform. Compile the predicted fragment spectra into a structured database format matching your reference resource schema. Validate completeness by confirming that every input compound has a corresponding predicted spectrum entry and that fragments fall within the specified mass range. The workflow generates in-silico MS/MS signatures that serve as query candidates for spectral matching against experimental data.

## Related tools

- **CFM-ID** (Computational engine for predicting fragment spectra from compound structures at specified ionization levels and mass ranges)

## Evaluation signals

- All input compounds from the SDF file have corresponding entries in the predicted fragments database (100% coverage)
- Predicted fragment m/z values fall within the specified mass range and match chemical fragmentation rules for the ionization mode used
- Database schema and format match the deposited predicted-fragments online resource specification (columns, data types, record structure)
- No null or malformed spectrum entries in output; each compound has at least one predicted fragment
- Consistency check: re-running CFM-ID on a subset of compounds produces identical spectra

## Limitations

- CFM-ID predictions are in-silico approximations; absolute intensity ratios may diverge from experimental MS/MS data depending on instrument type and collision energy
- Prediction accuracy depends on compound structure quality in the SDF file; missing or incorrect stereochemistry, charges, or coordinates will compromise fragmentation modeling
- The workflow does not account for instrument-specific phenomena (e.g., neutral loss pathways, rearrangements) or adduct-specific fragmentation behaviors not encoded in CFM-ID's training data

## Evidence

- [other] The in-silico fragment prediction stage uses CFM-ID to process SDF compound structures and generate predicted fragment spectra: "The in-silico fragment prediction stage uses CFM-ID to process SDF compound structures and generate predicted fragment spectra, with results deposited in the predicted fragments database."
- [other] Load compound structures from the SDF format file containing DNA adduct compounds. Execute CFM-ID on each compound structure to predict fragment spectra at the appropriate ionization level and mass range.: "Load compound structures from the SDF format file containing DNA adduct compounds. Execute CFM-ID on each compound structure to predict fragment spectra at the appropriate ionization level and mass"
- [other] Compile predicted fragment spectra into a structured database matching the format of the deposited predicted-fragments online resource.: "Compile predicted fragment spectra into a structured database matching the format of the deposited predicted-fragments online resource."
- [intro] Multiple formats and access points are available for the DNA adductomics database: Excel, Word, online interactive versions, SDF compound files, experimental and predicted fragment databases: "Multiple formats and access points are available for the DNA adductomics database: Excel, Word, online interactive versions, SDF compound files, experimental and predicted fragment databases"
