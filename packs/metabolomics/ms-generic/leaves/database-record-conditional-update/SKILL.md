---
name: database-record-conditional-update
description: 'Use when when processing mass spectrometry spectral records from a database
  where critical fields (e.g., adduct annotation) are absent or null, and you have
  a secondary field (e.g., ionmode: ''pos''/''neg'') that can deterministically populate
  the missing field.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - FragHub
  - Python 3.12
  - RDkit
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

# database-record-conditional-update

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Conditionally update database records based on field state and metadata consistency rules, such as auto-assigning adducts to spectra when missing. This skill ensures data completeness and consistency by applying ionization-mode-aware logic before writing records back to storage.

## When to use

When processing mass spectrometry spectral records from a database where critical fields (e.g., adduct annotation) are absent or null, and you have a secondary field (e.g., ionmode: 'pos'/'neg') that can deterministically populate the missing field. Use this skill during data standardization pipelines where consistency between ionization polarity and chemical adduct assignment must be enforced.

## When NOT to use

- When the adduct field is already populated and valid; conditional update is unnecessary.
- When ionmode is missing or ambiguous; you cannot reliably infer adduct polarity without ionization mode metadata.
- When spectra are multi-mode (mixed positive and negative ionization in a single record); the binary conditional logic cannot apply.

## Inputs

- Spectral records (JSON, CSV, MSP, or MGF format) with null/missing adduct field
- Ionmode field (string: 'pos' or 'neg') for each record
- FragHub database or file-based spectrum collection

## Outputs

- Updated spectral records with auto-assigned [M+H]+ or [M-H]- adducts
- Standardized mass spectrometry data compatible with MSdial, MZmine, or Flash Entropy Search

## How to apply

Load spectral records from the FragHub database, filtering for entries with null or missing adduct fields. Inspect the ionmode field for each record to determine ionization polarity ('pos' or 'neg'). Apply conditional logic: assign [M+H]+ adduct if ionmode is 'pos'; assign [M-H]- if ionmode is 'neg'. Validate that the assigned adduct is consistent with ionmode (no negative adducts in positive ionmode, no positive adducts in negative ionmode). Write updated records with auto-assigned adducts back to the database or output file. This approach guarantees that every spectrum has a chemically valid adduct before downstream analysis.

## Related tools

- **FragHub** (Database and standardization pipeline that loads, filters, and updates spectral records with auto-assigned adducts based on ionmode consistency) — https://github.com/eMetaboHUB/FragHub
- **Python 3.12** (Language for implementing the conditional filtering, ionmode inspection, and record update logic)
- **RDkit** (Optional tool for chemical structure validation and descriptor recalculation post-adduct assignment)

## Evaluation signals

- All spectra with previously null adduct fields now have [M+H]+ or [M-H]- assigned.
- Adduct polarity matches ionmode (all [M+H]+ adducts occur in 'pos' ionmode records; all [M-H]- occur in 'neg' records).
- No spectra are removed solely due to auto-assignment; filtering of adduct–ionmode inconsistencies occurs only for already-existing conflicting records.
- Updated records pass validation: negative adducts do not appear in positive ionmode spectra and vice versa.
- Output file schema remains compliant with ISO/IEC 20802-2:2016 .json format or selected output format (MGF, MSP, CSV).

## Limitations

- Requires ionmode field to be present and correctly populated; missing ionmode prevents reliable adduct inference.
- Does not handle multi-mode acquisition or spectra with ambiguous polarity annotations.
- Assigns only [M+H]+ and [M-H]- adducts; complex adducts (e.g., [M+Na]+, [M+2H]2+) are not auto-assigned and must be pre-existing or handled by separate logic.
- No validation is performed on whether the inferred adduct is chemically plausible for the precursor m/z and molecular formula; adduct assignment is purely rule-based.
- Spectra lacking SMILES, InChI, and InChIKey are removed during FragHub processing, independent of this adduct-assignment step.

## Evidence

- [other] FragHub implements automatic addition of [M+H]+ or [M-H]- adducts to in-silico spectra when the adduct field is absent, with selection based on ionmode consistency.: "FragHub implements automatic addition of [M+H]+ or [M-H]- adducts to in-silico spectra when the adduct field is absent, with selection based on ionmode consistency."
- [other] Load in-silico spectra records from the FragHub database, filtering for entries with missing or null adduct fields. Inspect the ionmode field for each spectrum to determine ionization polarity (pos/neg). Apply conditional logic: if ionmode is 'pos', assign [M+H]+ adduct; if ionmode is 'neg', assign [M-H]- adduct. Validate that the assigned adduct is consistent with the ionmode.: "Load in-silico spectra records from the FragHub database, filtering for entries with missing or null adduct fields. Inspect the ionmode field for each spectrum to determine ionization polarity"
- [other] Delete spectrum if negative adduct in positive ionmode or positive adduct in negative ionmode: "deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum"
- [other] auto add [M+H]+ or [M-H]- in In-Silico if adduct is missing: "auto add [M+H]+ or [M-H]- in In-Silico if adduct is missing."
- [readme] Standardized spectra produced by FragHub are compatible with multiple analysis software, including MSdial, MZmine, and Flash Entropy Search, providing users with maximum flexibility in choosing analysis tools.: "Standardized spectra produced by FragHub are compatible with multiple analysis software, including MSdial, MZmine, and Flash Entropy Search"
