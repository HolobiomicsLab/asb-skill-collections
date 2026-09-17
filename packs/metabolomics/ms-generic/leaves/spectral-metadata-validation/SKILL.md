---
name: spectral-metadata-validation
description: Use when processing heterogeneous mass spectral datasets from multiple
  open libraries (e.g., MassBank, UNPD, GMD) where structural identifiers, precursor
  m/z, and adduct information are frequently incomplete or inconsistent across records.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Python 3.12
  - RDkit
  - spectra-hash (SPLASH)
  - FragHub
  techniques:
  - mass-spectrometry
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-4.0
    url: eMetaboHUB/FragHub
  license_tier: noncommercial
  provenance_tier: literature
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

# spectral-metadata-validation

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Validates and filters mass spectra based on completeness and consistency of structural and experimental metadata (SMILES, InChI, InChIKey, precursor m/z, adduct information). This skill identifies spectra that lack critical identifiers or have conflicting ionmode/adduct pairs, enabling removal of low-quality records before downstream analysis.

## When to use

Apply this skill when processing heterogeneous mass spectral datasets from multiple open libraries (e.g., MassBank, UNPD, GMD) where structural identifiers, precursor m/z, and adduct information are frequently incomplete or inconsistent across records. Use it before standardization workflows or when preparing data for library search and spectral matching.

## When NOT to use

- Input spectra are already curated and have been validated by the source database (e.g., MassBank records with all identifiers pre-verified).
- Analysis goal requires retention of ambiguous or partial structural data for exploratory data mining or peak matching in unknown-annotation workflows.
- Spectra are from a single, well-characterized instrument or protocol known to consistently provide complete metadata (validation overhead outweighs benefit).

## Inputs

- mass spectral data file (JSON, CSV, MSP, or MGF format)
- spectral records with fields: SMILES, InChI, InChIKey, precursor_mz, adduct, ionmode (polarity)

## Outputs

- validated spectral dataset (same format as input, filtered)
- DELETION_REASONS log directory with per-spectrum deletion rationales

## How to apply

Load spectral records in JSON, CSV, MSP, or MGF format and apply a cascade of validation checks: (1) Retain only spectra where at least one of SMILES, InChI, or InChIKey is present and non-empty (delete if all three are absent). (2) Remove spectra lacking precursor m/z or valid adduct annotation. (3) Flag and delete spectra with ionmode–adduct conflicts (e.g., negative adduct in positive ionmode spectrum, or positive adduct in negative ionmode). (4) Auto-add [M+H]+ or [M-H]- in in-silico spectra if adduct is missing but ionmode is specified. (5) Log each deletion with detailed rationale to a DELETION_REASONS subdirectory for audit and debugging. Use regex pattern validation for adduct field normalization and apply ionmode key matching ('pos', 'neg') to catch misclassifications.

## Related tools

- **Python 3.12** (Primary scripting and data processing environment for iteration through spectral records and validation logic)
- **RDkit** (Offline recalculation and normalization of SMILES, InChI, and InChIKey from molecular structures to ensure consistency and fill missing identifiers)
- **spectra-hash (SPLASH)** (Generate SPLASH (Spectral Hash) keys for duplicate detection by spectral fingerprint; integrated into FragHub for tracking previously processed spectra) — https://github.com/berlinguyinca/spectra-hash
- **FragHub** (Complete end-to-end spectral standardization pipeline that applies metadata validation as a core filtering step before organizing spectra by polarity, chromatographic mode, and acquisition type) — https://github.com/eMetaboHUB/FragHub

## Evaluation signals

- All retained spectra contain at least one non-empty structural identifier (SMILES, InChI, or InChIKey); zero spectra lack all three.
- All retained spectra have non-null precursor m/z and valid adduct annotation; none are missing these fields.
- Ionmode–adduct consistency: no positive ionmode spectrum retains a negative adduct (e.g., [M-H]-), and vice versa; conflicts are logged with reason.
- DELETION_REASONS log file records the count and rationale for each deletion category (e.g., '42 spectra deleted: no SMILES AND no InChI AND no InChIKey').
- Duplicate removal by SPLASH key: spectral records with identical SPLASH hashes are flagged; only one representative is retained in output.

## Limitations

- Regex pattern fixes for adduct field validation are applied heuristically; no explicit validation metrics or benchmarking results are provided for pattern accuracy across diverse adduct nomenclatures.
- In-silico auto-addition of [M+H]+ or [M-H]- assumes ionmode is correctly labeled; misclassified or unlabeled in-silico spectra may be falsely modified.
- Offline RDkit and PubChem data used for identifier normalization may become stale; no automatic update mechanism or reproducibility information for local data sources is documented.
- GC instrument detection relies on filename suffix (e.g., '_GC') or manually maintained instrument dictionary; new GC instruments may not be recognized without manual curation.
- Precursor m/z and adduct validation exceptions for GC spectra extend to all GC spectra without instrument-specific nuance; GC-EI or GC-CI subtypes are not differentiated.
- Platform-specific limitations: macOS and Linux support have been deprecated; only Windows x64 installer is actively maintained.

## Evidence

- [other] FragHub removes spectra that lack all three structural identifiers simultaneously—a spectrum is deleted only when it has no SMILES AND no InChI AND no InChIKey, retaining spectra that possess at least one of these identifiers.: "FragHub removes spectra that lack all three structural identifiers simultaneously—a spectrum is deleted only when it has no SMILES AND no InChI AND no InChIKey"
- [other] Delete spectrum if negative adduct in positive ionmode or positive adduct in negative ionmode: "deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum"
- [other] Auto-addition of [M+H]+ or [M-H]- in In-Silico if adduct is missing.: "auto add [M+H]+ or [M-H]- in In-Silico if adduct is missing."
- [other] Improve spectrum deletion callback by writing deleted spectrum in DELETION_REASONS sub folder with a detailed reason.: "improve spectrum deletion callback by writing deleted spectrum in DELETION_REASONS sub folder with a detailed reason."
- [other] Duplicate removal by SPLASH key: "Refactoring duplicatas removal, now by sames SPLASH key."
- [readme] All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub.: "All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed"
- [other] Iterate through each spectrum record and check for the presence of SMILES, InChI, and InChIKey fields.: "Iterate through each spectrum record and check for the presence of SMILES, InChI, and InChIKey fields."
