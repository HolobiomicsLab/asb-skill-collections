---
name: hash-based-deduplication-workflow
description: Use when when processing open mass spectrometry library (OMSL) data that may contain duplicate spectral records (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - spectra-hash
  - Python 3.12
  - FragHub
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.analchem.4c02219
  title: FragHub
evidence_spans:
- Python-3.12
- direct integration of spectra-hash (https://github.com/berlinguyinca/spectra-hash) into fraghub
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

# hash-based-deduplication-workflow

## Summary

A data quality workflow that identifies and removes duplicate mass spectra by computing spectral hash identifiers (SPLASH keys) and grouping spectra by identical hash values. This ensures a deduplicated spectral dataset while preserving the first occurrence of each unique spectrum.

## When to use

When processing open mass spectrometry library (OMSL) data that may contain duplicate spectral records (e.g., the same compound measured under identical conditions), you need to reduce redundancy while retaining one representative spectrum per unique spectral profile to improve downstream analysis efficiency and avoid biasing database search results.

## When NOT to use

- Input spectra lack complete chemical structure information (SMILES, InChI, AND InChIKey) — these should be filtered out before deduplication
- Spectra have missing or ambiguous precursor m/z and adduct annotations — address adduct validation before hash-based grouping
- Intentional spectrum replicates are part of the study design (e.g., technical replicates for quality metrics) — in this case, preserve replicates and mark them explicitly rather than deduplicating

## Inputs

- Spectral dataset in FragHub JSON format
- Mass spectrometry records with m/z and intensity pairs
- Complete spectral metadata (SMILES, InChI, InChIKey, precursor m/z, adduct information)

## Outputs

- Deduplicated spectral dataset in FragHub JSON format
- Deletion log documenting removed duplicate spectra and their SPLASH keys
- Single representative spectrum per unique SPLASH key retained in output

## How to apply

Load the spectral dataset in FragHub JSON format using Python 3.12. Compute or retrieve the SPLASH key for each spectrum using the spectra-hash tool, which generates an unambiguous, database-independent identifier based on the m/z and intensity pairs in the spectrum. Group spectra by identical SPLASH key values; spectra with the same SPLASH key are exact duplicates. For each group of identical SPLASH keys, retain only the first occurrence (or another deterministic representative) and mark all others for removal. Write the deduplicated spectral set to output, preserving the original JSON structure. The SPLASH identifier has four blocks separated by dashes (e.g., `splash10-0002-0900000000-b112e4e059e1ecf98c5f`), with the fourth block containing the unique hash that enables duplicate detection.

## Related tools

- **spectra-hash** (Computes SPLASH keys for each spectrum; core tool for spectral hashing and grouping by identical hash values) — https://github.com/berlinguyinca/spectra-hash
- **Python 3.12** (Execution environment for loading spectral dataset, orchestrating SPLASH computation, grouping by hash key, and writing deduplicated output)
- **FragHub** (Integrates spectra-hash; handles spectral dataset standardization, filtering, and deduplication workflow) — https://github.com/eMetaboHUB/FragHub

## Evaluation signals

- Total number of input spectra vs. deduplicated output spectra — verify a reduction in dataset size consistent with the expected duplicate rate
- All retained spectra have unique SPLASH keys — check that no two spectra in the output share the same SPLASH key
- First-occurrence preservation — confirm that the retained representative for each group is deterministically selected (e.g., earliest in file order)
- Deletion log completeness — verify that all removed spectra are logged with their SPLASH key, original identifier, and reason for removal
- JSON schema validity — validate that output spectra retain original JSON structure and all metadata fields (m/z, intensity, SMILES, InChI, InChIKey, precursor m/z, adduct)

## Limitations

- SPLASH keys are computed from m/z and intensity pairs only; minor spectral variations (e.g., different ionization energies, slight peak shifts due to instrument calibration drift) may produce different SPLASH keys for chemically identical spectra, resulting in missed duplicates
- Duplicate detection is exact-match based on SPLASH hash — near-duplicates or spectra with minor peak differences will not be flagged
- Requires complete spectral metadata (SMILES, InChI, InChIKey, precursor m/z, adduct); spectra lacking any of these are removed before deduplication occurs, potentially discarding useful spectral data
- FragHub has removed macOS and Linux support as of version 1.4.1, restricting execution to Windows x64

## Evidence

- [other] FragHub refactors duplicate removal by identifying spectra with identical SPLASH keys, enabling systematic deduplication of the spectral dataset.: "FragHub refactors duplicate removal by identifying spectra with identical SPLASH keys, enabling systematic deduplication of the spectral dataset."
- [other] Load the spectral dataset (in FragHub JSON format) using Python 3.12. Compute or retrieve the SPLASH key for each spectrum using the spectra-hash tool. Group spectra by identical SPLASH key values. For each group, retain a single representative spectrum (e.g., first occurrence) and mark duplicates for removal.: "Load the spectral dataset (in FragHub JSON format) using Python 3.12. Compute or retrieve the SPLASH key for each spectrum using the spectra-hash tool. Group spectra by identical SPLASH key values."
- [readme] The SPLASH (SPectraL hASH) is an unambiguous, database-independent spectral identifier, just as the InChIKey is designed to serve as a unique identifier for chemical structures. It contains separate blocks that define different layers of information, separated by dashes.: "The SPLASH (SPectraL hASH) is an unambiguous, database-independent spectral identifier, just as the InChIKey is designed to serve as a unique identifier for chemical structures. It contains separate"
- [readme] All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub.: "All spectra deemed inconsistent, i.e., those lacking SMILES and InChI, precursor m/z, and adduct information, are removed during the processing by FragHub."
- [other] direct integration of spectra-hash (https://github.com/berlinguyinca/spectra-hash) into fraghub.: "direct integration of spectra-hash (https://github.com/berlinguyinca/spectra-hash) into fraghub."
