---
name: duplicate-spectrum-detection-splash
description: Use when when processing large collections of mass spectra from multiple
  Open Mass Spectra Libraries (OMSLs) or databases that may contain redundant spectral
  records with identical m/z–intensity peak patterns but potentially different metadata
  annotations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - spectra-hash
  - Python 3.12
  techniques:
  - mass-spectrometry
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-4.0
    url: eMetaboHUB/FragHub
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

# duplicate-spectrum-detection-splash

## Summary

Detect and remove duplicate mass spectra by computing SPLASH (SPectraL hASH) keys and grouping spectra with identical hash values. This enables systematic deduplication of spectral datasets while preserving a single representative entry per group.

## When to use

When processing large collections of mass spectra from multiple Open Mass Spectra Libraries (OMSLs) or databases that may contain redundant spectral records with identical m/z–intensity peak patterns but potentially different metadata annotations. Apply this skill after parsing and validating individual spectra (e.g., after adduct–ionmode consistency checks) but before final output serialization.

## When NOT to use

- Input spectra have not yet been validated for adduct–ionmode consistency or structural identifiers (SMILES, InChI, InChIKey); apply those filters first.
- The spectral dataset is already known to contain no duplicates (e.g., after previous FragHub deduplication runs with saved SPLASH keys).
- Only in-silico spectra with intentionally identical fragmentation patterns are being processed and should be retained despite SPLASH key matches for method comparison purposes.

## Inputs

- parsed spectral dataset in FragHub JSON format
- spectrum objects with m/z–intensity peak lists
- spectrum metadata fields (NAME, PRECURSORMZ, IONMODE, ADDUCT, SMILES, INCHI, INCHIKEY)

## Outputs

- deduplicated spectral dataset in FragHub JSON format
- deletion log recording removed duplicate spectra with SPLASH keys and removal reasons

## How to apply

First, compute or retrieve the SPLASH key for each spectrum in the parsed spectral dataset using the spectra-hash tool, which generates a database-independent hashed identifier based on the m/z–intensity peak list. Second, group all spectra by their SPLASH key value to identify clusters of identical spectra. Third, for each cluster containing multiple spectra with the same SPLASH key, retain only a single representative spectrum (e.g., the first occurrence) and mark duplicates for removal. Finally, write the deduplicated spectral set to the output file in FragHub JSON format, maintaining the original JSON structure. Log removed duplicate entries with their SPLASH keys and removal reason in a separate deletion log for traceability.

## Related tools

- **spectra-hash** (Compute SPLASH keys for each spectrum; directly integrated into FragHub for deduplication workflow) — https://github.com/berlinguyinca/spectra-hash
- **Python 3.12** (Load spectral dataset, group by SPLASH key, and serialize deduplicated output)

## Evaluation signals

- All spectra in the output have unique SPLASH key values; no two spectra share identical SPLASH keys.
- Total number of output spectra equals the count of unique SPLASH keys from the input dataset.
- Deletion log records the SPLASH key, original spectrum metadata, and removal reason for each deduplicated entry.
- Output JSON structure and metadata fields are identical to input (no data loss outside duplicate removal).
- Manual spot-check: spectra removed as duplicates have identical m/z–intensity peak patterns when compared to their retained representative entry.

## Limitations

- SPLASH deduplication is deterministic only for identical peak lists; slight variations in peak m/z values (e.g., due to different instrument calibration or rounding) may fail to merge true duplicates.
- Spectra with identical peak patterns but conflicting structural identifiers (e.g., different SMILES strings for the same SPLASH key) will be merged arbitrarily based on occurrence order; no automatic conflict resolution is performed.
- The choice of 'representative' spectrum (e.g., first occurrence) is arbitrary and may not select the spectrum with the highest-quality metadata or most reliable source database.
- No explicit validation metrics or benchmarking results are provided for SPLASH deduplication accuracy against manually curated ground-truth duplicate sets.

## Evidence

- [other] FragHub refactors duplicate removal by identifying spectra with identical SPLASH keys, enabling systematic deduplication of the spectral dataset.: "FragHub refactors duplicate removal by identifying spectra with identical SPLASH keys, enabling systematic deduplication of the spectral dataset."
- [discussion] Refactoring duplicatas removal, now by sames SPLASH key.: "Refactoring duplicatas removal, now by sames SPLASH key."
- [discussion] direct integration of spectra-hash (https://github.com/berlinguyinca/spectra-hash) into fraghub.: "direct integration of spectra-hash (https://github.com/berlinguyinca/spectra-hash) into fraghub."
- [readme] The SPLASH (SPectraL hASH) is an unambiguous, database-independent spectral identifier: "The SPLASH (SPectraL hASH) is an unambiguous, database-independent spectral identifier, just as the InChIKey is designed to serve as a unique identifier for chemical structures."
- [other] Load the spectral dataset (in FragHub JSON format) using Python 3.12. Compute or retrieve the SPLASH key for each spectrum using the spectra-hash tool. Group spectra by identical SPLASH key values. For each group, retain a single representative spectrum (e.g., first occurrence) and mark duplicates for removal. Write the deduplicated spectral set to output, maintaining the original JSON structure.: "Load the spectral dataset (in FragHub JSON format) using Python 3.12. Compute or retrieve the SPLASH key for each spectrum using the spectra-hash tool. Group spectra by identical SPLASH key values."
