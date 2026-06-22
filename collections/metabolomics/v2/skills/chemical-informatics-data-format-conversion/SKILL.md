---
name: chemical-informatics-data-format-conversion
description: Use when when you have raw SMILES strings collected from multiple external databases that require standardization and deduplication before integration into a unified chemical structure database. Specifically, apply this skill when you need to convert interim/tables/0_original/structure/smiles.tsv.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3837
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_2258
  tools:
  - R
  - Python
  - smiles.py
  - sanitizing.py
  - Python 3
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- standardizing.R, 1_integrating.R, 1_cleaningOriginal.R, 4_cleaningTaxonomy.R, 5_addingOTL.R
- 1_integrating.R
- 221[[smiles.py]], 260[[3_cleaningAndEnriching/sanitizing.py]]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.7554/eLife.70780
  all_source_dois:
  - 10.7554/eLife.70780
  - 10.1007/s00044-016-1764-y
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-informatics-data-format-conversion

## Summary

Convert and standardize raw chemical structure notations (SMILES strings) into validated, deduplicated structural identifiers (standardized SMILES and InChI) through sequential file-to-file transformations. This skill is essential in natural products curation pipelines where structure data from heterogeneous sources must be normalized and validated before downstream chemical analysis.

## When to use

When you have raw SMILES strings collected from multiple external databases that require standardization and deduplication before integration into a unified chemical structure database. Specifically, apply this skill when you need to convert interim/tables/0_original/structure/smiles.tsv.gz (raw SMILES from the gathering layer) into validated, unique structural identifiers that can be confidently linked to organism and reference data.

## When NOT to use

- Input is already a validated, deduplicated unique structure table (e.g., from a trusted, pre-curated source).
- Raw data contains chemical structures in formats other than SMILES (e.g., MOL, SDF) without a prior conversion step to SMILES.
- You need to preserve all raw SMILES variants (including duplicates and minor stereoisomers) without merging them into canonical forms.

## Inputs

- interim/tables/0_original/structure/smiles.tsv.gz (raw SMILES strings from gathering layer)

## Outputs

- interim/tables/1_translated/structure/smiles.tsv.gz (standardized SMILES)
- interim/tables/1_translated/structure/unique.tsv.gz (deduplicated, validated structure identifiers)

## How to apply

Execute two consecutive transformation steps: (1) Run smiles.py on the raw SMILES table to translate and standardize SMILES strings according to chemical validity rules, producing an intermediate standardized SMILES table. (2) Apply sanitizing.py to the translated SMILES to validate chemical structures, remove invalid entries (e.g., malformed SMILES that cannot be parsed), and deduplicate identical structures, generating the final unique structure table. The rationale is that raw SMILES from external sources often contain syntax errors, non-canonical forms, or duplicates; two-stage processing ensures both format compliance and chemical validity before structural identifiers are linked to organism and literature metadata.

## Related tools

- **smiles.py** (Translates and standardizes raw SMILES strings from interim/tables/0_original/structure/smiles.tsv.gz into canonical form) — https://github.com/lotusnprod/lotus-processor
- **sanitizing.py** (Validates chemical structures from translated SMILES, removes invalid entries, and deduplicates to generate the final unique structure table) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (Execution environment for smiles.py and sanitizing.py scripts) — https://github.com/lotusnprod/lotus-processor

## Examples

```
python scripts/smiles.py --input interim/tables/0_original/structure/smiles.tsv.gz --output interim/tables/1_translated/structure/smiles.tsv.gz && python scripts/sanitizing.py --input interim/tables/1_translated/structure/smiles.tsv.gz --output interim/tables/1_translated/structure/unique.tsv.gz
```

## Evaluation signals

- All raw SMILES in the input file are successfully parsed and converted to standardized canonical form with no errors in smiles.py output.
- The number of unique structures in unique.tsv.gz is less than or equal to the number of translated SMILES (deduplication has occurred or is zero).
- Invalid SMILES strings (those that fail chemical validity checks in sanitizing.py) are documented and excluded from the unique structure table.
- Cross-validation: a random sample of structures in unique.tsv.gz can be converted back to SMILES and compared to the original raw SMILES to confirm standardization consistency.
- File schema validation: unique.tsv.gz contains expected columns (e.g., structure ID, canonical SMILES, InChI) with no null values in critical fields.

## Limitations

- SMILES standardization is lossy for stereochemical detail when the input SMILES lacks explicit stereochemical annotation; minor stereoisomers will be merged into the canonical form.
- The sanitizing step removes structures that fail chemical validity rules, which may result in loss of data if source databases contain non-standard or ambiguous notations.
- Very large raw SMILES tables (>1M entries) may experience performance bottlenecks depending on Python environment memory and CPU resources.
- The skill requires that both smiles.py and sanitizing.py scripts are present and properly configured in the lotus-processor repository; modifications to these scripts will alter output behavior.

## Evidence

- [methods] smiles.py converts raw SMILES from interim/tables/0_original/structure/smiles.tsv.gz, and sanitizing.py then produces the final standardized unique structure table at interim/tables/1_translated/structure/unique.tsv.gz: "The LOTUS processor applies two consecutive file-to-file transformations: smiles.py converts raw SMILES from interim/tables/0_original/structure/smiles.tsv.gz, and sanitizing.py then produces the"
- [methods] Load raw SMILES table from interim/tables/0_original/structure/smiles.tsv.gz using Python. Execute smiles.py to translate and standardise SMILES strings, generating interim/tables/1_translated/structure/smiles.tsv.gz. Load translated SMILES and apply sanitizing.py to validate chemical structures, remove invalid entries, and deduplicate to generate interim/tables/1_translated/structure/unique.tsv.gz.: "1. Load raw SMILES table from interim/tables/0_original/structure/smiles.tsv.gz using Python. 2. Execute smiles.py to translate and standardise SMILES strings, generating"
- [methods] 2_editing structure – SMILES processing, sanitization, and enrichment with workflow evidence showing file-to-file transformations: "220([interim/tables/0_original/structure/smiles.tsv.gz]) --> 221[[smiles.py]] --> 222([interim/tables/1_translated/structure/smiles.tsv.gz])"
- [readme] Python 3 is listed as a required tool in the README system requirements: "- R
- Python 3
- Java >= 17"
- [intro] LOTUS is described as a comprehensive collection of documented structure-organism pairs constructed from external databases requiring standardization: "*LOTUS* is a comprehensive collection of documented structure-organism pairs. Within the frame of current computational approaches in Natural Products research and related fields, these documented"
