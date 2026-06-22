---
name: data-quality-assessment-from-molecular-descriptors
description: Use when processing spectral datasets from open mass spectra libraries (OMSLs) where structural identifiers and ionization metadata are incomplete or inconsistent.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - FragHub
  - Python 3.12
  - RDkit
  - spectra-hash (SPLASH)
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

# data-quality-assessment-from-molecular-descriptors

## Summary

Assess and filter mass spectrometry spectral data based on completeness and consistency of molecular structural identifiers (SMILES, InChI, InChIKey) and associated metadata (precursor m/z, adduct information). This skill identifies spectra lacking critical structural or ionization descriptors and removes them to ensure dataset quality and analytical reliability.

## When to use

Apply this skill when processing spectral datasets from open mass spectra libraries (OMSLs) where structural identifiers and ionization metadata are incomplete or inconsistent. Use it as a prerequisite step before standardization or comparative analysis when spectra must have unambiguous chemical structure representation and valid ion annotation. This is particularly critical when merging data from heterogeneous sources with varying metadata completeness.

## When NOT to use

- Spectra already validated and confirmed to have all three structural identifiers (SMILES AND InChI AND InChIKey present) — re-filtering adds no diagnostic value.
- Datasets where structural ambiguity is acceptable or tolerated (e.g., unknowns-only libraries, de novo fragmentation studies without reference structure requirement).
- Spectral data from sources where adduct information is intentionally omitted or unavailable (e.g., neutral loss or in-source fragmentation datasets without ionization mode specification).

## Inputs

- spectral data file (JSON format: ISO/IEC 20802-2:2016 or non-standard)
- spectrum records with fields: SMILES, InChI, InChIKey, precursor m/z, adduct, ionmode (positive/negative)

## Outputs

- filtered spectral dataset (JSON format, same as input)
- DELETION_REASONS log directory with per-spectrum deletion rationale

## How to apply

Load spectral data in JSON format (compatible with ISO/IEC 20802-2:2016 and non-standard formats) and iterate through each spectrum record to assess presence and validity of three structural identifier fields: SMILES, InChI, and InChIKey. Delete a spectrum only if ALL THREE identifiers are absent simultaneously—retain any spectrum possessing at least one non-empty identifier. Simultaneously validate precursor m/z presence and adduct field consistency: remove spectra with negative adducts in positive ionmode (or vice versa), missing/malformed adducts, or adduct-ionmode mismatches. Log each deletion with detailed rationale (which field(s) were missing or invalid) to a DELETION_REASONS subdirectory for traceability and downstream analysis of data quality bottlenecks.

## Related tools

- **FragHub** (primary execution environment; implements the multi-stage filtering pipeline including structural identifier validation, adduct-ionmode consistency checks, and deletion logging) — https://github.com/eMetaboHUB/FragHub
- **Python 3.12** (runtime language for iterating spectrum records, field presence/validity checking, conditional filtering logic, and deletion reason serialization)
- **RDkit** (optional post-filter validation: recalculation and normalization of SMILES and InChI representations to detect malformed identifiers)
- **spectra-hash (SPLASH)** (optional deduplication step: identify and remove duplicate spectra by SPLASH key before structural validation, reducing redundant filtering overhead) — https://github.com/berlinguyinca/spectra-hash

## Evaluation signals

- Verify output spectral dataset contains only records with at least one of {SMILES, InChI, InChIKey} populated and non-empty; sample records to confirm presence.
- Inspect DELETION_REASONS log: confirm all deleted spectra are documented with specific reason (e.g., 'no SMILES AND no InChI AND no InChIKey', 'negative adduct in positive ionmode', 'missing adduct').
- Cross-check deletion count and reasons against input dataset size; ensure no spectra were deleted that possessed all three structural identifiers or valid ionization metadata.
- Validate adduct-ionmode consistency in retained spectra: spot-check that positive ionmode spectra contain positive adducts ([M+H]+, [M+Na]+, etc.) and negative ionmode contain negative adducts ([M-H]-, [M+Cl]-, etc.).
- Confirm output JSON structure conforms to ISO/IEC 20802-2:2016 schema; parse and validate against schema validator or FragHub's own format checker.

## Limitations

- Binary deletion rule (all three identifiers absent) may discard spectra with two valid identifiers; for stricter quality, users must adjust the rule to require all three simultaneously.
- Deletion relies on field presence and non-empty string checks only; does not validate chemical correctness or consistency between SMILES, InChI, and InChIKey (structural coherence requires RDkit or external chemical validation).
- Adduct validation depends on correct ionmode labeling in input data; misclassified or unlabeled ionmode fields will bypass adduct consistency checks and may retain or delete spectra incorrectly.
- No handling of null/missing precursor m/z in GC spectra by default; requires explicit exception extension to GC instruments to avoid false negatives.
- Performance degrades on very large spectral datasets (>1M spectra) without multi-threading and chunk-size auto-calculation; current implementation uses auto-calculated chunk sizes but no benchmarking data provided for throughput scaling.

## Evidence

- [other] FragHub removes spectra that lack all three structural identifiers simultaneously—a spectrum is deleted only when it has no SMILES AND no InChI AND no InChIKey, retaining spectra that possess at least one of these identifiers.: "FragHub removes spectra that lack all three structural identifiers simultaneously—a spectrum is deleted only when it has no SMILES AND no InChI AND no InChIKey, retaining spectra that possess at"
- [other] Load the input spectral data file (JSON format compatible with ISO/IEC 20802-2:2016 and non-standard formats). Iterate through each spectrum record and check for the presence of SMILES, InChI, and InChIKey fields. Retain only spectra where all three identifiers (SMILES AND InChI AND InChIKey) are present and non-empty.: "Load the input spectral data file (JSON format compatible with ISO/IEC 20802-2:2016 and non-standard formats). Iterate through each spectrum record and check for the presence of SMILES, InChI, and"
- [other] Log deletion reasons for each filtered spectrum to a DELETION_REASONS subdirectory with detailed rationale.: "Log deletion reasons for each filtered spectrum to a DELETION_REASONS subdirectory with detailed rationale."
- [other] Delete spectrum if negative adduct in positive ionmode or positive adduct in negative ionmode: "deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum"
- [other] Now deleting spectrum with no SMILES no InChI **AND no inchikey**.: "Now deleting spectrum with no SMILES no InChI **AND no inchikey**."
- [readme] All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub.: "All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub."
