---
name: file-format-robustness-testing
description: Use when when processing MS spectral data from multiple open mass spectra libraries (OMSLs) in mixed formats (MSP, MGF, JSON, CSV), especially when source data exhibits missing fields, malformed entries, inconsistent adduct representations, or non-standard format variants that may cause silent.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - Python 3.12
  - spectra-hash (SPLASH)
  - RDkit
  - PubChem
  - FragHub
  techniques:
  - LC-MS
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

# file-format-robustness-testing

## Summary

Validate and standardize mass spectrometry data across heterogeneous file formats (MSP, MGF, JSON, CSV) by implementing format-specific parsers with comprehensive edge-case handling, metadata validation, and structural integrity checks to ensure consistent spectrum parsing without data loss.

## When to use

When processing MS spectral data from multiple open mass spectra libraries (OMSLs) in mixed formats (MSP, MGF, JSON, CSV), especially when source data exhibits missing fields, malformed entries, inconsistent adduct representations, or non-standard format variants that may cause silent spectrum loss or parse errors during aggregation pipelines.

## When NOT to use

- Input spectra are already in a single, internally consistent format with validated metadata and no known edge cases — direct standardization may be more efficient than full robustness testing.
- The analysis goal does not require traceability of deleted spectra (e.g., downstream tool accepts partial or lossy input) — the overhead of logging deletion reasons is not justified.
- Data volumes are so large that per-spectrum logging to disk becomes a bottleneck; streaming validation without persistent deletion records may be preferred.

## Inputs

- MSP-format spectral files (line-delimited metadata + peak blocks)
- MGF-format spectral files (MS/MS peak data)
- JSON-format spectral files (ISO/IEC 20802-2:2016 standard and non-standard variants)
- CSV-format spectral files (semicolon or tab-delimited with quoted fields)
- Spectrum metadata: NAME, PRECURSORMZ, IONMODE, ADDUCT, SMILES, InChI, InChIKey
- Peak arrays: m/z–intensity pairs

## Outputs

- Parsed and validated spectrum objects with standardized field names and values
- Deletion log files in DELETION_REASONS subdirectory (one per removed spectrum with reason)
- Deduplicated spectrum list (SPLASH-key-based duplicate removal)
- Serialized output in user-selected format (JSON, MGF, MSP, or CSV)

## How to apply

Implement format-specific line-by-line parsers (e.g., Python 3.12 file I/O) that separately handle metadata extraction (NAME, PRECURSORMZ, IONMODE, ADDUCT, SMILES, InChI, InChIKey) and peak-list blocks according to MSP/MGF/JSON specifications. At each parsing stage—metadata field validation, m/z–intensity peak pair extraction, adduct-ionmode consistency checking—log deletion reasons to a dedicated DELETION_REASONS subdirectory with detailed rationale. Apply multi-stage filtering: (1) remove spectra with negative adducts in positive ionmode or positive adducts in negative ionmode; (2) remove spectra lacking both SMILES AND InChI AND InChIKey; (3) deduplicate by SPLASH key matching. Return the complete parsed spectrum list (non-deleted entries) serialized to the output format, ensuring traceability of all removed spectra for audit and quality control.

## Related tools

- **Python 3.12** (Line-by-line file parsing, metadata extraction, and validation logic implementation)
- **spectra-hash (SPLASH)** (Duplicate spectrum detection by spectral hash key; deduplication via SPLASH key matching) — https://github.com/berlinguyinca/spectra-hash
- **RDkit** (Chemical structure validation and identifier normalization (SMILES, InChI, InChIKey recalculation))
- **PubChem** (Offline reference data for completing and validating chemical identifiers)
- **FragHub** (End-to-end MS data standardization and organization tool implementing this robustness-testing workflow) — https://github.com/eMetaboHUB/FragHub

## Examples

```
# Python 3.12 snippet to parse MSP file with robustness testing:
from pathlib import Path
with open('input.msp', 'r') as f:
    spectra = []
    deletions = Path('DELETION_REASONS')
    for spec in parse_msp_spectra(f):
        if validate_adduct_ionmode(spec) and has_identifier(spec) and not is_duplicate_by_splash(spec, spectra):
            spectra.append(spec)
        else:
            log_deletion(spec, deletions, reason='failed validation')
```

## Evaluation signals

- All spectra present in input file are accounted for in output or DELETION_REASONS logs (zero silent loss).
- Every deleted spectrum has a corresponding log entry in DELETION_REASONS subdirectory with a specific reason (e.g., 'negative adduct in positive ionmode', 'no SMILES, no InChI, no InChIKey', 'duplicate by SPLASH key').
- Adduct-ionmode consistency: no spectrum with negative adduct remains in positive ionmode output, and vice versa.
- Deduplicated spectrum set has no two entries with identical SPLASH key.
- Output spectrum records contain all mandatory fields (NAME, PRECURSORMZ, IONMODE, ADDUCT, at least one of SMILES/InChI/InChIKey, peak array) or are logged as deleted with reason.

## Limitations

- Regex pattern for adduct field parsing may fail on non-standard adduct notations not covered by existing patterns; manual curation or pattern extension required for novel formats.
- No explicit validation metrics or benchmarking provided for adduct regex pattern fixes across diverse data sources.
- Offline RDkit and PubChem data sources require manual maintenance and update; reproducibility depends on snapshot versioning and data provenance documentation.
- Local Classyfire and NPclassifier data sources lack explicit reproducibility information (version, update frequency, curation criteria).
- Multi-threading chunk-size auto-calculation lacks detailed performance profiling; may not scale optimally for all system architectures.
- MacOS and Linux support were removed in later versions; Windows x64 is the primary supported platform.

## Evidence

- [other] How does FragHub handle edge cases during MSP file parsing to ensure that spectra are not incorrectly dropped during final spectrum list generation?: "FragHub implements spectrum deletion with detailed reasons logging and applies adduct validation checks (removing spectra with negative adducts in positive ionmode or positive adducts in negative"
- [other] Workflow steps for file-format robustness testing: "Load MSP file using Python 3.12 file I/O with line-by-line parsing. Parse spectrum metadata fields (NAME, PRECURSORMZ, IONMODE, ADDUCT, SMILES, INCHI, INCHIKEY) according to MSP specification,"
- [other] Filtering and deduplication logic: "Apply adduct–ionmode consistency checks: delete spectrum if negative adduct in positive ionmode or positive adduct in negative ionmode. Delete spectrum if no SMILES AND no InChI AND no InChIKey."
- [other] Deletion logging requirement: "improve spectrum deletion callback by writing deleted spectrum in DELETION_REASONS sub folder with a detailed reason."
- [readme] Multi-format support: "First tab: Select single or multiple .json, .csv, .msp, or .mgf files."
- [readme] Data standardization objective: "FragHub is a powerful tool designed to standardize and organize mass spectrometry (MS) data from OMSLs (Open Mass Spectra Libraries)."
- [other] ISO standard compliance and non-standard format handling: "Refactoring .json reader for standard ISO/IEC 20802-2:2016 .json and non-standard formats."
- [other] Duplicate removal by SPLASH: "Refactoring duplicatas removal, now by sames SPLASH key."
