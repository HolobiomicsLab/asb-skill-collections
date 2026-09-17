---
name: spectral-metadata-grouping
description: Use when processing a mass spectrometry dataset (in FragHub JSON format
  or similar) where duplicate spectral records are suspected or known to exist. The
  input dataset should already be in a standardized format with computed or retrievable
  SPLASH keys.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - spectra-hash
  - FragHub
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

# spectral-metadata-grouping

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Group mass spectra by identical SPLASH keys to identify and remove duplicate spectral records in standardized spectral datasets. This skill enables systematic deduplication of mass spectrometry libraries by leveraging the SPLASH (SPectraL hASH) identifier—a database-independent, unambiguous spectral hash that serves as a unique fingerprint for each spectrum.

## When to use

Apply this skill when processing a mass spectrometry dataset (in FragHub JSON format or similar) where duplicate spectral records are suspected or known to exist. The input dataset should already be in a standardized format with computed or retrievable SPLASH keys. Use this skill as a quality control step before final library assembly or when merging multiple spectral databases where redundancy is likely.

## When NOT to use

- Input dataset already has known-unique spectra or has been pre-deduplicated by another method (e.g., exact m/z-intensity matching or database ID uniqueness).
- SPLASH keys are unavailable or cannot be computed (e.g., spectra lack m/z-intensity data or are in non-standard formats that spectra-hash does not support).
- The analysis goal requires retaining all variant forms of a spectrum (e.g., multiple collision energies, different instruments, or intentional replicates for meta-analysis)—in which case a different grouping strategy (e.g., by precursor m/z + adduct only) may be more appropriate.

## Inputs

- Mass spectrometry spectral dataset (FragHub JSON format, CSV, MSP, or MGF)
- Per-spectrum SPLASH key (computed via spectra-hash or pre-existing field)
- Ion m/z and intensity pairs for each spectrum

## Outputs

- Deduplicated spectral dataset in FragHub JSON format (or original format)
- Set of retained representative spectra (one per unique SPLASH key)
- Optionally: log or metadata file listing removed duplicate spectra and their corresponding SPLASH keys

## How to apply

Load the spectral dataset into memory using Python 3.12. Compute or retrieve the SPLASH key for each spectrum using the spectra-hash tool (available as a Python module or command-line utility). Group all spectra by their SPLASH key value, treating identical keys as equivalence classes. Within each group, retain a single representative spectrum (e.g., the first occurrence, or the spectrum with the highest spectral quality metric if available) and mark all others as duplicates. Write the deduplicated spectral set to output, maintaining the original JSON structure and preserving all metadata fields for retained spectra. Verify deduplication by confirming that the output dataset has fewer or equal spectra than the input, and that no two spectra in the output share the same SPLASH key.

## Related tools

- **spectra-hash** (Computes or validates SPLASH keys for each spectrum; provides Python, C++, Java, C#, and R implementations; used to generate the spectral hash identifier used as the grouping key.) — https://github.com/berlinguyinca/spectra-hash
- **FragHub** (Host application for standardizing and organizing mass spectrometry data; integrates spectra-hash directly for deduplication; orchestrates the full workflow from data loading to deduplicated output in standardized JSON format.) — https://github.com/eMetaboHUB/FragHub
- **Python 3.12** (Programming environment for implementing the grouping and deduplication workflow; used to load, parse, group, and write spectral datasets.)

## Evaluation signals

- Output spectral count is less than or equal to input spectral count; the difference equals the number of removed duplicates.
- No two spectra in the deduplicated output share the same SPLASH key (uniqueness invariant).
- All retained spectra maintain their original metadata fields and JSON structure integrity (no data loss for non-duplicate records).
- Each removed duplicate is correctly paired with an existing retained spectrum that has an identical SPLASH key.
- Spot-check: manually verify that a sample of spectra marked as duplicates do indeed have identical or near-identical m/z and intensity patterns when compared to their representative spectrum.

## Limitations

- SPLASH key computation depends on the quality and completeness of m/z and intensity data; spectra with missing or malformed peak lists may fail to generate valid SPLASH keys or may produce spurious matches.
- SPLASH is designed to hash spectral *profile* (m/z and intensity) but does not account for metadata differences (e.g., collision energy, instrument, acquisition date); two physically different experiments may yield identical SPLASH keys if their peak profiles are the same, potentially causing over-deduplication in multi-source datasets.
- The choice of which duplicate to retain (first occurrence vs. highest quality) is not determined by SPLASH; a heuristic or explicit quality metric must be supplied externally.
- Large datasets (millions of spectra) may require efficient grouping and memory management; the provided workflow does not address multi-threading or chunking strategies mentioned in FragHub discussion.
- Spectra lacking SMILES, InChI, and InChIKey may be removed by FragHub *before* deduplication is applied, reducing the effective dataset size; deduplication should be performed on the full input dataset prior to such filtering if retention of all chemically distinct spectra is desired.

## Evidence

- [other] FragHub refactors duplicate removal by identifying spectra with identical SPLASH keys, enabling systematic deduplication of the spectral dataset.: "FragHub refactors duplicate removal by identifying spectra with identical SPLASH keys, enabling systematic deduplication of the spectral dataset."
- [other] Group spectra by identical SPLASH key values. For each group, retain a single representative spectrum (e.g., first occurrence) and mark duplicates for removal.: "Group spectra by identical SPLASH key values. For each group, retain a single representative spectrum (e.g., first occurrence) and mark duplicates for removal."
- [readme] The SPLASH (SPectraL hASH) is an unambiguous, database-independent spectral identifier, just as the InChIKey is designed to serve as a unique identifier for chemical structures.: "The SPLASH (SPectraL hASH) is an unambiguous, database-independent spectral identifier, just as the InChIKey is designed to serve as a unique identifier for chemical structures."
- [other] Load the spectral dataset (in FragHub JSON format) using Python 3.12. Compute or retrieve the SPLASH key for each spectrum using the spectra-hash tool.: "Load the spectral dataset (in FragHub JSON format) using Python 3.12. Compute or retrieve the SPLASH key for each spectrum using the spectra-hash tool."
- [other] direct integration of spectra-hash (https://github.com/berlinguyinca/spectra-hash) into fraghub.: "direct integration of spectra-hash (https://github.com/berlinguyinca/spectra-hash) into fraghub."
- [other] Refactoring duplicatas removal, now by sames SPLASH key.: "Refactoring duplicatas removal, now by sames SPLASH key."
