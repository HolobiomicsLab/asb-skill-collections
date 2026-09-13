---
name: spectrum-metadata-extraction-validation
description: Use when when ingesting heterogeneous MS spectral data from multiple
  open-access libraries (OMS libraries) where metadata completeness and correctness
  are uncertain.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - Python
  - spectra-hash (SPLASH)
  - RDkit
  - PubChem
  - Python 3.12
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

# spectrum-metadata-extraction-validation

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Extract and validate critical metadata fields (NAME, PRECURSORMZ, IONMODE, ADDUCT, SMILES, InChI, InChIKey) from mass spectrometry data files (MSP, MGF, JSON, CSV), applying consistency checks to remove spectra with missing or conflicting chemical identifiers and ion-mode/adduct incompatibilities. This ensures only complete, internally consistent spectra are retained for downstream analysis.

## When to use

When ingesting heterogeneous MS spectral data from multiple open-access libraries (OMS libraries) where metadata completeness and correctness are uncertain. Trigger this skill if your input files contain spectra lacking adduct information, mismatched ionization modes, or absent chemical structure identifiers (SMILES/InChI/InChIKey). Apply before any spectral matching, fingerprinting, or library construction.

## When NOT to use

- If your input spectra are already curated and you have prior assurance that all contain valid SMILES, InChI, InChIKey, and consistent adduct/ionmode pairs—metadata extraction becomes redundant.
- If you are processing only in-silico spectra with predicted or computational adducts where real ionmode/adduct conflicts are not meaningful; consider relaxing the adduct-ionmode consistency check for in-silico data.
- If your workflow requires retention of all spectra regardless of metadata completeness (e.g., for exploratory or quality assessment purposes); this skill enforces strict filtering and will discard incomplete entries.

## Inputs

- MSP file (line-by-line text format with NAME, PRECURSORMZ, IONMODE, ADDUCT, SMILES, INCHI, INCHIKEY metadata fields)
- MGF file (mascot generic format)
- JSON file (ISO/IEC 20802-2:2016 compliant or non-standard format)
- CSV file (semicolon or tab-separated, with peaks column and metadata columns)

## Outputs

- Parsed spectrum list (array of spectrum objects with validated metadata)
- Serialized spectra in output format (JSON, MGF, MSP, or CSV)
- DELETION_REASONS log subdirectory (detailed justification for each removed spectrum)

## How to apply

Parse each spectrum entry line-by-line from the input file (MSP, MGF, JSON, or CSV format), extracting metadata fields according to the file's specification. For each spectrum, apply a hierarchical validation pipeline: (1) Check that PRECURSORMZ and IONMODE are non-empty and properly formatted. (2) Validate adduct field for consistency with ionmode using regex patterns (e.g., reject negative adducts in positive-ionmode spectra, or positive adducts in negative-ionmode spectra). (3) Reject any spectrum with no SMILES AND no InChI AND no InChIKey simultaneously. (4) Remove duplicates by SPLASH (SPectraL hASH) key matching. (5) Log all deletions with detailed reasons in a DELETION_REASONS subdirectory for traceability. Return only non-deleted spectra serialized to the output format. The rationale is that spectra lacking both ion-mode/adduct coherence and chemical structure data cannot be reliably matched or identified downstream.

## Related tools

- **spectra-hash (SPLASH)** (Compute SPectraL hASH identifiers for duplicate detection and spectrum identity verification during metadata extraction) — https://github.com/berlinguyinca/spectra-hash
- **RDkit** (Validate and normalize SMILES strings and recalculate chemical descriptors from parsed structure identifiers)
- **PubChem** (Offline reference for validating and completing InChI/InChIKey data linked to parsed structures)
- **Python 3.12** (Runtime environment for file I/O, line-by-line parsing, regex-based metadata validation, and logging) — https://www.python.org

## Evaluation signals

- All retained spectra contain non-empty PRECURSORMZ, IONMODE, and ADDUCT fields with properly formatted values.
- No retained spectrum has both a negative adduct in positive-ionmode context or a positive adduct in negative-ionmode context.
- Every retained spectrum has at least one of SMILES, InChI, or InChIKey populated; verify count of spectra with all three identifiers present.
- Duplicate spectra (same SPLASH key) appear only once in output; cross-check output spectrum count against input count minus logged deletions.
- DELETION_REASONS log contains one entry per deleted spectrum with justification (e.g., 'negative adduct in positive ionmode', 'no SMILES, InChI, or InChIKey', 'duplicate SPLASH key'); total deletion count matches input count minus output count.

## Limitations

- Regex patterns for adduct validation may require case-sensitive or format-specific tuning; adducts with non-standard notation (e.g., abbreviations or regional conventions) may be incorrectly rejected.
- SPLASH key computation depends on peak list format and intensity normalization; duplicate detection assumes peak data is complete and consistent across files.
- GC spectra are treated differently (extension of precursor m/z and adduct checks to GC spectra); some GC instruments may lack precursor m/z or have ambiguous adduct assignments, requiring manual review.
- Offline RDkit and PubChem reference data may become stale; no automatic mechanism for updating local Classyfire or NPclassifier data is documented.
- The metadata validation pipeline removes all spectra with missing or conflicting data; no partial recovery or imputation is attempted, which may cause loss of otherwise valuable spectral information.

## Evidence

- [other] Parse spectrum metadata fields (NAME, PRECURSORMZ, IONMODE, ADDUCT, SMILES, INCHI, INCHIKEY) according to MSP specification, handling missing or malformed entries.: "Parse spectrum metadata fields (NAME, PRECURSORMZ, IONMODE, ADDUCT, SMILES, INCHI, INCHIKEY) according to MSP specification, handling missing or malformed entries."
- [other] Apply adduct–ionmode consistency checks: delete spectrum if negative adduct in positive ionmode or positive adduct in negative ionmode.: "Apply adduct–ionmode consistency checks: delete spectrum if negative adduct in positive ionmode or positive adduct in negative ionmode."
- [other] Delete spectrum if no SMILES AND no InChI AND no InChIKey.: "Delete spectrum if no SMILES AND no InChI AND no InChIKey."
- [other] Remove duplicate spectra by SPLASH key matching.: "Remove duplicate spectra by SPLASH key matching."
- [other] Log all deleted spectra with detailed reasons in DELETION_REASONS subdirectory.: "Log all deleted spectra with detailed reasons in DELETION_REASONS subdirectory."
- [readme] All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub.: "All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub."
- [discussion] deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum: "deleting spectrum if neg adduct in pos spectrum, or pos adduct in neg spectrum"
- [discussion] Now deleting spectrum with no SMILES no InChI **AND no inchikey**.: "Now deleting spectrum with no SMILES no InChI **AND no inchikey**."
