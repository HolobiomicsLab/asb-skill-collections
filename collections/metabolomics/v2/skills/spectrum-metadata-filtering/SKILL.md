---
name: spectrum-metadata-filtering
description: Use when importing mass spectra from multiple open mass spectra libraries (OMSLs) or databases with heterogeneous metadata quality. Use when you observe spectra annotated with negative adducts (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Python 3.12
  - spectra-hash
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectrum-metadata-filtering

## Summary

Filters mass spectra by validating ionmode–adduct polarity consistency and removing spectra with missing, malformed, or incompatible adduct annotations. Applied during MS data standardization to ensure only spectra with valid metadata annotations are retained in downstream analysis.

## When to use

Apply this skill when importing mass spectra from multiple open mass spectra libraries (OMSLs) or databases with heterogeneous metadata quality. Use when you observe spectra annotated with negative adducts (e.g., [M-H]−) in positive-ionmode records or vice versa, or when adduct fields are missing, null, or malformed. Necessary before standardization and organization of MS data for compatibility with analysis software such as MSdial, MZmine, or Flash Entropy Search.

## When NOT to use

- When spectra have no ionmode annotation at all; this filter requires pre-existing ionmode metadata.
- When working with gas chromatography (GC) spectra that explicitly allow adduct exceptions or lack precursor m/z annotation.
- When input spectra are already validated and curated by a trusted primary source with documented adduct accuracy.

## Inputs

- Mass spectrum records with parsed ionmode field ('pos' or 'neg')
- Adduct annotation field (string, may be null or malformed)
- Adduct regex pattern specification (for format validation)

## Outputs

- Filtered spectrum dataset retaining only valid ionmode-adduct pairs
- DELETION_REASONS log with detailed reason per removed spectrum

## How to apply

For each spectrum record, parse the ionmode field ('pos' or 'neg') and adduct annotation field. Using adduct regex pattern matching, validate that adduct strings conform to expected format and polarity: positive adducts (e.g., [M+H]+, [M+Na]+) must appear only in pos-mode spectra, and negative adducts (e.g., [M-H]−, [M+Cl]−) only in neg-mode spectra. Flag and delete spectra where (1) ionmode and adduct polarity mismatch, (2) adduct field is missing or null, or (3) adduct string fails regex validation. Log each deletion reason (ionmode-adduct mismatch, missing adduct, or malformed adduct) to a DELETION_REASONS subfolder. Retain only spectra with correct ionmode-adduct pairs and write to output.

## Related tools

- **Python 3.12** (Runtime for parsing spectrum records, regex validation of adducts, and iterative filtering logic)
- **spectra-hash** (Integrated for duplicate removal by SPLASH key during spectrum curation workflow) — https://github.com/berlinguyinca/spectra-hash

## Evaluation signals

- All retained spectra have matching ionmode-adduct polarity pairs (no [M-H]− in pos spectra, no [M+H]+ in neg spectra).
- All retained spectra have non-null, non-empty adduct fields that match the expected regex pattern for their ionmode.
- The count of deleted spectra per reason (mismatch, missing, malformed) is logged in DELETION_REASONS subfolder; sum of deleted counts plus retained spectra equals input spectrum count.
- No spectra with null or missing adduct annotations remain in the filtered output.
- Spot-check a sample of deleted spectrum records confirms each deletion reason is consistent with its logged justification.

## Limitations

- Filter does not handle spectra lacking ionmode annotation; such records cannot be validated and may cause errors or require manual intervention.
- GC spectra may have different adduct requirements or exceptions (e.g., missing precursor m/z); the filter requires explicit handling via exception lists or dataset-specific rule sets.
- Adduct regex pattern must be curated and maintained; updates to adduct terminology or new adduct formats require regex pattern revision and re-validation.
- Deletion is irreversible; spectra marked for removal should be logged to allow audit trails and recovery if deletion logic is later found to be overly strict.

## Evidence

- [other] FragHub filters spectra by deleting those where negative adducts appear in positive-mode spectra or positive adducts appear in negative-mode spectra, and removes spectra with no or bad adduct annotations.: "FragHub filters spectra by deleting those where negative adducts appear in positive-mode spectra or positive adducts appear in negative-mode spectra, and removes spectra with no or bad adduct"
- [other] For each spectrum, check if the ionmode is 'pos' or 'neg' and validate that adduct annotations are compatible (positive adducts like [M+H]+ only in pos mode, negative adducts like [M-H]- only in neg mode), using adduct regex pattern matching.: "For each spectrum, check if the ionmode is 'pos' or 'neg' and validate that adduct annotations are compatible (positive adducts like [M+H]+ only in pos mode, negative adducts like [M-H]- only in neg"
- [other] Flag and delete spectra with mismatched ionmode-adduct pairs (e.g., [M-H]- in pos mode), spectra with missing/null adduct fields, or spectra with malformed adduct strings that fail regex validation.: "Flag and delete spectra with mismatched ionmode-adduct pairs (e.g., [M-H]- in pos mode), spectra with missing/null adduct fields, or spectra with malformed adduct strings that fail regex validation."
- [other] Log the detailed deletion reason (ionmode-adduct mismatch, missing adduct, or bad adduct format) for each removed spectrum to a DELETION_REASONS subfolder.: "Log the detailed deletion reason (ionmode-adduct mismatch, missing adduct, or bad adduct format) for each removed spectrum to a DELETION_REASONS subfolder."
- [other] Write the filtered spectrum dataset (retaining only valid spectra with correct ionmode-adduct pairs) to output.: "Write the filtered spectrum dataset (retaining only valid spectra with correct ionmode-adduct pairs) to output."
- [readme] improve spectrum deletion callback by writing deleted spectrum in DELETION_REASONS sub folder with a detailed reason.: "improve spectrum deletion callback by writing deleted spectrum in DELETION_REASONS sub folder with a detailed reason."
