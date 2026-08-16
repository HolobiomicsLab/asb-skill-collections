---
name: spectral-adduct-ionmode-validation
description: Use when when processing raw or aggregated mass spectra datasets (from
  .mgf, .msp, .json, or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - Python 3.12
  - spectra-hash (SPLASH)
  - FragHub
  techniques:
  - GC-MS
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-4.0
    url: eMetaboHUB/FragHub
  license_tier: noncommercial
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

# spectral-adduct-ionmode-validation

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Validates and filters mass spectra by ensuring adduct annotations are consistent with ionization mode polarity (positive adducts only in positive-mode spectra, negative adducts only in negative-mode spectra), and removes spectra with missing or malformed adduct fields. This quality control step prevents downstream analysis errors from mismatched ionization chemistry.

## When to use

When processing raw or aggregated mass spectra datasets (from .mgf, .msp, .json, or .csv files) where ionmode and adduct annotations may be inconsistent, incomplete, or incorrectly formatted—particularly when combining spectra from multiple open mass spectral libraries (OMSLs) with variable data quality or when standardizing spectra for compatibility with multiple analysis software (MSdial, MZmine, Flash Entropy Search).

## When NOT to use

- When spectra do not carry explicit ionmode or adduct metadata (e.g., raw centroided peaks with no annotations).
- When processing gas chromatography (GC) spectra, where adduct checks may require exception handling or omission.
- When the input dataset has already been validated and curated for ionmode-adduct consistency by a trusted upstream process.

## Inputs

- mass spectrum records with ionmode field ('pos' or 'neg')
- adduct annotation field (string, e.g., '[M+H]+', '[M-H]-', '[M+Na]+')
- spectrum dataset in formats: .mgf, .msp, .json, .csv

## Outputs

- filtered spectrum dataset (spectra with valid ionmode-adduct concordance)
- deletion log with detailed reasons per removed spectrum

## How to apply

Load the spectrum dataset and for each spectrum record, extract the ionmode ('pos' or 'neg') and adduct field (e.g., '[M+H]+', '[M-H]-'). Apply adduct regex pattern matching to validate adduct string format. Cross-check compatibility: flag any spectrum where a negative adduct (e.g., '[M-H]-') appears in positive-mode ionmode, or a positive adduct (e.g., '[M+H]+') appears in negative-mode ionmode. Also flag spectra with missing (null) adduct fields or adduct strings that fail regex validation. Delete all flagged spectra and log the specific deletion reason (ionmode-adduct mismatch, missing adduct, or bad adduct format) to a DELETION_REASONS subfolder for audit and troubleshooting. Retain only spectra with valid, concordant ionmode-adduct pairs in the output dataset.

## Related tools

- **Python 3.12** (execution environment for spectrum dataset loading, ionmode-adduct parsing, regex validation, filtering logic, and deletion logging)
- **spectra-hash (SPLASH)** (duplicate detection during spectrum filtering workflow (SPLASH key used to track previously processed spectra and avoid re-processing in incremental updates)) — https://github.com/berlinguyinca/spectra-hash
- **FragHub** (integrated framework implementing this adduct-ionmode validation filter as part of mass spectra standardization pipeline) — https://github.com/eMetaboHUB/FragHub

## Evaluation signals

- All retained spectra have ionmode field ('pos' or 'neg') that matches adduct polarity (positive adducts only in pos-mode, negative adducts only in neg-mode).
- All deleted spectra appear in DELETION_REASONS log with a documented reason (ionmode-adduct mismatch, missing adduct, or bad adduct regex match).
- No spectrum in the output dataset has a null or empty adduct field.
- Adduct strings in retained spectra pass regex pattern validation (e.g., conform to '[M±H]±', '[M±Na]±' patterns).
- Record count of input vs. output spectra, and count of deletions by reason category, confirm filtering was applied and is auditable.

## Limitations

- Requires explicit, well-formed ionmode and adduct fields in input records; datasets with sparse or missing annotations will lose spectra even if they are otherwise valid.
- GC spectra may require exception handling or separate validation logic, as GC instruments often do not use traditional protonation-based adducts; the article notes 'extend precursormz and adduct checks exception to all GC spectrums' as an ongoing modification.
- Adduct regex pattern accuracy depends on prior validation; if the regex pattern itself is incorrect or outdated, valid adducts may be incorrectly flagged as malformed.
- Spectra with missing InChI, SMILES, or InChIKey will be removed by downstream FragHub processing regardless of ionmode-adduct concordance; this filter alone does not guarantee retention.

## Evidence

- [other] FragHub filters spectra by deleting those where negative adducts appear in positive-mode spectra or positive adducts appear in negative-mode spectra, and removes spectra with no or bad adduct annotations.: "FragHub filters spectra by deleting those where negative adducts appear in positive-mode spectra or positive adducts appear in negative-mode spectra, and removes spectra with no or bad adduct"
- [other] For each spectrum, check if the ionmode is 'pos' or 'neg' and validate that adduct annotations are compatible (positive adducts like [M+H]+ only in pos mode, negative adducts like [M-H]- only in neg mode), using adduct regex pattern matching.: "For each spectrum, check if the ionmode is 'pos' or 'neg' and validate that adduct annotations are compatible (positive adducts like [M+H]+ only in pos mode, negative adducts like [M-H]- only in neg"
- [other] Flag and delete spectra with mismatched ionmode-adduct pairs (e.g., [M-H]- in pos mode), spectra with missing/null adduct fields, or spectra with malformed adduct strings that fail regex validation.: "Flag and delete spectra with mismatched ionmode-adduct pairs (e.g., [M-H]- in pos mode), spectra with missing/null adduct fields, or spectra with malformed adduct strings that fail regex validation."
- [other] Log the detailed deletion reason (ionmode-adduct mismatch, missing adduct, or bad adduct format) for each removed spectrum to a DELETION_REASONS subfolder.: "Log the detailed deletion reason (ionmode-adduct mismatch, missing adduct, or bad adduct format) for each removed spectrum to a DELETION_REASONS subfolder."
- [discussion] deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum: "deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum"
- [discussion] removing no or bad adduct spectrum: "removing no or bad adduct spectrum"
- [discussion] extend precursormz and adduct checks exception to all GC spectrums.: "extend precursormz and adduct checks exception to all GC spectrums."
- [readme] All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub.: "All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub."
