---
name: msp-file-parsing-edge-case-handling
description: Use when you are parsing mass spectrometry spectral library files in
  MSP format and need to guarantee that all spectrum records are either successfully
  integrated into the final dataset or explicitly logged with a reason for exclusion.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Python 3.12
  - spectra-hash (SPLASH)
  - FragHub
  techniques:
  - CE-MS
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

# MSP file parsing edge case handling

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Detect and safely handle malformed or incomplete spectrum records during line-by-line MSP file parsing to prevent silent data loss. This skill ensures that spectra with invalid metadata, missing chemical identifiers, or inconsistent adduct–ionmode combinations are logged with explicit deletion reasons rather than dropped without trace.

## When to use

You are parsing mass spectrometry spectral library files in MSP format and need to guarantee that all spectrum records are either successfully integrated into the final dataset or explicitly logged with a reason for exclusion. This is essential when the source MSP file may contain incomplete entries (missing PRECURSORMZ, ADDUCT, or chemical structure fields), malformed peak blocks, or metadata inconsistencies that could silently corrupt downstream analysis.

## When NOT to use

- Input is already a curated, pre-validated spectral database with zero tolerance for any record loss — use this skill during initial curation; do not use on production databases expecting 100% preservation.
- MSP file is guaranteed well-formed with no missing fields or adduct inconsistencies — this skill adds overhead; use only when data quality is uncertain.
- You need to preserve ALL spectra regardless of chemical identifier completeness — this skill's 'no SMILES AND no InChI AND no InChIKey' filter will delete such records.

## Inputs

- MSP format spectral library file (text, line-delimited)
- File I/O stream (line-by-line reader)
- MSP metadata fields: NAME, PRECURSORMZ, IONMODE, ADDUCT, SMILES, INCHI, INCHIKEY
- Peak list blocks (m/z–intensity pairs)

## Outputs

- Parsed and filtered spectrum list (non-deleted entries only)
- DELETION_REASONS subdirectory (one file per deleted spectrum with reason)
- Complete parsed spectrum list (serialized to output file)
- SPLASH key index for duplicate detection and incremental reprocessing

## How to apply

Load the MSP file using Python 3.12 file I/O with line-by-line parsing. For each spectrum record, extract and validate metadata fields (NAME, PRECURSORMZ, IONMODE, ADDUCT, SMILES, INCHI, INCHIKEY) according to MSP specification, skipping empty or corrupted peak blocks. Apply three sequential filter checkpoints: (1) delete spectrum if negative adduct occurs in positive ionmode or positive adduct in negative ionmode; (2) delete spectrum if no SMILES AND no InChI AND no InChIKey; (3) remove duplicate spectra by SPLASH key matching. For every deleted spectrum, write a record to the DELETION_REASONS subdirectory with the specific reason (e.g., 'negative adduct in positive ionmode', 'no chemical identifier', 'duplicate by SPLASH'). Return only the non-deleted entries serialized to the output file, with complete deletion audit trail preserved.

## Related tools

- **Python 3.12** (Line-by-line file I/O, spectrum record parsing, adduct–ionmode validation logic, and deletion logging)
- **spectra-hash (SPLASH)** (Generate and match spectral hash identifiers for duplicate detection across parsed spectra) — https://github.com/berlinguyinca/spectra-hash
- **FragHub** (Complete end-to-end MSP file standardization and filtering pipeline that integrates this edge case handling skill) — https://github.com/eMetaboHUB/FragHub

## Examples

```
python fraghub_parser.py --input library.msp --output-dir ./cleaned --deletion-log DELETION_REASONS --validate-adduct-ionmode --remove-duplicates-by-splash
```

## Evaluation signals

- All spectrum records in input MSP are accounted for: either present in output file or listed in DELETION_REASONS with explicit reason.
- No spectra with negative adduct in positive ionmode (or vice versa) appear in the output spectrum list.
- No spectra lacking all three of SMILES, InChI, and InChIKey appear in the output; all such records are logged with reason 'no chemical identifier'.
- Duplicate spectra (matched by SPLASH key) are reduced to one representative entry; removal is logged in DELETION_REASONS.
- Peak blocks with corrupted or empty entries are skipped without crashing the parser; affected spectra are logged with reason.
- Output spectrum list is deterministic and reproducible across re-runs of the same input file (i.e., same records deleted each time).

## Limitations

- The skill requires valid SPLASH calculation; malformed peak data that cannot be hashed will cause the duplicate detection step to fail or produce unreliable hashes.
- Adduct validation uses a regex pattern that may not recognize all valid adduct notations; the README notes 'fix adduct regex pattern' as an ongoing refinement, implying current pattern coverage is incomplete.
- Spectra lacking all three chemical identifiers (SMILES, InChI, InChIKey) are unconditionally deleted; there is no option to preserve them or flag for manual curation.
- No explicit validation metrics or benchmarking results provided for adduct regex pattern fixes, so real-world false positive/negative rates are undocumented.
- No details provided on how the MSP parser handles non-standard or vendor-specific metadata extensions beyond the core specification.

## Evidence

- [other] how_to_apply[1]: "1. Load MSP file using Python 3.12 file I/O with line-by-line parsing. 2. Parse spectrum metadata fields (NAME, PRECURSORMZ, IONMODE, ADDUCT, SMILES, INCHI, INCHIKEY) according to MSP specification,"
- [other] how_to_apply[2]: "3. Extract and validate m/z–intensity peak pairs for each spectrum, skipping empty or corrupted peak blocks. 4. Apply adduct–ionmode consistency checks: delete spectrum if negative adduct in positive"
- [other] how_to_apply[3]: "5. Delete spectrum if no SMILES AND no InChI AND no InChIKey. 6. Remove duplicate spectra by SPLASH key matching. 7. Log all deleted spectra with detailed reasons in DELETION_REASONS subdirectory."
- [readme] when_to_use: "Warning: All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub."
- [other] limitations[1]: "improve spectrum deletion callback by writing deleted spectrum in DELETION_REASONS sub folder with a detailed reason."
- [other] limitations[2]: "Now deleting spectrum with no SMILES no InChI **AND no inchikey**."
- [readme] related_tools[spectra-hash]: "direct integration of spectra-hash (https://github.com/berlinguyinca/spectra-hash) into fraghub."
