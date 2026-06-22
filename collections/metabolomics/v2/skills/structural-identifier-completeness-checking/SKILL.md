---
name: structural-identifier-completeness-checking
description: Use when preprocessing open mass spectrometry libraries (OMSLs) or aggregated spectral datasets where structural identifiers are inconsistently populated.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0630
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - Python 3.12
  - FragHub
  - RDkit
  - PubChem
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.analchem.4c02219
  title: FragHub
evidence_spans:
- Python-3.12
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fraghub_cq
    doi: 10.1021/acs.analchem.4c02219
    title: FragHub
  dedup_kept_from: coll_fraghub_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c02219
  all_source_dois:
  - 10.1021/acs.analchem.4c02219
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# structural-identifier-completeness-checking

## Summary

A filtering skill that removes mass spectra lacking complete chemical structure identifiers (SMILES, InChI, and InChIKey) from spectral datasets. This ensures that downstream analysis workflows receive only spectra with sufficient structural annotation to support reliable compound identification and cross-database mapping.

## When to use

Apply this skill when preprocessing open mass spectrometry libraries (OMSLs) or aggregated spectral datasets where structural identifiers are inconsistently populated. Specifically, use it before standardization pipelines or when preparing data for tools like MSdial, MZmine, or spectral similarity searches that depend on reliable chemical structure information for matching and annotation.

## When NOT to use

- When the spectral dataset is already known to be complete and validated for structural identifiers (i.e., preprocessing has already been performed).
- When downstream analysis explicitly requires only subsets of structural identifiers (e.g., InChIKey-only matching via ontology services like PubChem or ClassyFire, which may tolerate missing SMILES or InChI).
- When the goal is to recover or repair missing identifiers rather than filter them; in such cases, use enrichment or recalculation workflows (e.g., RDkit or PubChem data completion) before or instead of deletion.

## Inputs

- JSON-formatted mass spectral data (ISO/IEC 20802-2:2016 or non-standard variants)
- Alternative spectral formats: .msp, .mgf, .csv files
- Each spectrum record with optional SMILES, InChI, and InChIKey fields

## Outputs

- Filtered JSON spectral dataset containing only spectra with all three structural identifiers (SMILES, InChI, InChIKey) present and non-empty
- DELETION_REASONS subdirectory with detailed logs of each filtered spectrum and its removal justification
- Counts or summary of retained vs. deleted spectra

## How to apply

Iterate through each spectrum record in the input spectral data file (JSON format compatible with ISO/IEC 20802-2:2016 or non-standard formats such as .msp, .mgf, or .csv) and evaluate the presence and non-emptiness of three fields: SMILES, InChI, and InChIKey. A spectrum is retained only if it contains all three identifiers simultaneously. A spectrum is deleted only when it has no SMILES AND no InChI AND no InChIKey (i.e., the deletion criterion uses AND logic, not OR). For each deleted spectrum, log the deletion reason to a DELETION_REASONS subdirectory with detailed rationale. Write retained spectra to the output file in the same input format. This ensures data consistency while preserving spectra that possess at least one structural identifier, which may be recoverable or supplemented in parallel enrichment workflows.

## Related tools

- **Python 3.12** (Language for implementing the filtering logic and file I/O operations)
- **FragHub** (Higher-level spectral standardization and filtering pipeline that integrates this structural-identifier-completeness check as a mandatory preprocessing step) — https://github.com/eMetaboHUB/FragHub
- **RDkit** (Optional downstream tool for recalculation and normalization of retained SMILES, InChI, and InChIKey identifiers to ensure consistency)
- **PubChem** (Optional data source for enriching retained spectra with additional structural and ontological metadata via InChIKey lookups)

## Evaluation signals

- All retained spectra must contain non-empty SMILES, InChI, and InChIKey fields; any spectrum missing any of these three fields indicates incorrect application.
- The set of deleted spectra should contain only those with no SMILES AND no InChI AND no InChIKey; any spectrum with at least one identifier present should remain in the output.
- DELETION_REASONS log files must exist for all deleted spectra and document the specific deletion criterion (e.g., 'no SMILES, no InChI, no InChIKey').
- Output file format and schema must match the input format (JSON structure preserved, or equivalent .msp/.mgf/CSV re-serialization).
- Retention rate should be consistent with expectation; unusually high deletion rates (>90%) may indicate data quality issues in the input library or incorrect filter logic (e.g., treating AND as OR).

## Limitations

- This skill is purely a deletion filter and does not repair or recover missing identifiers; spectra with incomplete structural information are permanently removed, making incremental recovery impossible without external enrichment sources.
- The skill assumes that SMILES, InChI, and InChIKey fields are consistently named and structured in the input; non-standard or malformed field names may be silently ignored, leading to false deletions.
- No validation is performed on the chemical validity or consistency of retained identifiers (e.g., whether SMILES and InChI encode the same structure); this skill checks only presence, not correctness.
- Large spectral datasets may generate large DELETION_REASONS logs; disk space and I/O performance may be affected if millions of spectra are filtered.
- The skill does not handle or prioritize identifiers by quality or source; if multiple InChIKey values exist (e.g., from different calculators), only presence is checked, not consistency or preferred version.

## Evidence

- [other] Finding from task_001: "FragHub removes spectra that lack all three structural identifiers simultaneously—a spectrum is deleted only when it has no SMILES AND no InChI AND no InChIKey, retaining spectra that possess at"
- [other] Workflow from task_001: "Iterate through each spectrum record and check for the presence of SMILES, InChI, and InChIKey fields. Retain only spectra where all three identifiers (SMILES AND InChI AND InChIKey) are present and"
- [readme] FragHub README warning: "All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub."
- [other] FragHub discussion evidence: "Now deleting spectrum with no SMILES no InChI **AND no inchikey**."
- [other] Workflow specification: "Load the input spectral data file (JSON format compatible with ISO/IEC 20802-2:2016 and non-standard formats). Write retained spectra to the output file in the same JSON format. Log deletion reasons"
