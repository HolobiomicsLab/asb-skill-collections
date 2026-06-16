---
name: chemical-structure-sanitization-and-validation
description: Use when you have translated or raw SMILES strings from a chemical structure curation pipeline and need to remove invalid chemical structures, resolve sanitization errors (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0338
  edam_topics:
  - http://edamontology.org/topic_0176
  - http://edamontology.org/topic_3373
  tools:
  - R
  - Python
  - sanitizing.py
  - RDKit
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus
schema_version: 0.2.0
---

# chemical-structure-sanitization-and-validation

## Summary

Validate and standardize chemical structures represented as SMILES strings by removing invalid entries, correcting structural defects, and deduplicating to produce a curated set of chemically sound unique identifiers. This step is critical in natural products databases to ensure that downstream computational analysis (docking, molecular property prediction, organism-chemistry association) operates on reliable chemical representations.

## When to use

Apply this skill when you have translated or raw SMILES strings from a chemical structure curation pipeline and need to remove invalid chemical structures, resolve sanitization errors (e.g., valence violations, missing aromaticity perception), and eliminate redundant entries before integration with organism and reference metadata. In the LOTUS workflow, this is the filtering step immediately following SMILES translation, before final integration and downstream analysis.

## When NOT to use

- Input SMILES are already manually curated and validated by domain experts; sanitization is redundant.
- Structures are represented in formats other than SMILES (e.g., InChI, MOL, SDF) without prior conversion.
- The dataset is small enough that manual inspection and curation is more practical than automated sanitization.

## Inputs

- SMILES strings (translated, TSV.GZ format, e.g., interim/tables/1_translated/structure/smiles.tsv.gz)
- Chemical structure table with identifier and SMILES columns

## Outputs

- Deduplicated, validated unique structure table (TSV.GZ format, e.g., interim/tables/1_translated/structure/unique.tsv.gz)
- Validation log documenting rejected structures and sanitization actions

## How to apply

Load the translated SMILES table (e.g., interim/tables/1_translated/structure/smiles.tsv.gz) and execute a sanitization script (such as sanitizing.py) that parses each SMILES string, validates chemical syntax and valency rules using a chemistry library (e.g., RDKit), identifies and logs invalid structures, removes entries that fail validation, deduplicates equivalent structures by canonical SMILES representation, and outputs a clean, unique structure table. The rationale is that raw SMILES from source databases often contain formatting errors, incomplete aromatic perception, or duplicates; sanitization ensures only chemically valid and non-redundant structures proceed to organism-structure pairing and computational analysis. Evaluate success by confirming (1) all entries in the output table parse without exception, (2) the number of valid structures is reported, (3) duplicates are resolved to a single canonical form per unique chemical structure, and (4) a log of rejected entries explains why each was removed.

## Related tools

- **sanitizing.py** (Validates chemical structures in SMILES format, removes invalid entries, and deduplicates to produce a unique structure table) — https://github.com/lotusnprod/lotus-processor
- **RDKit** (Underlying chemistry library used to parse, validate, and canonicalize SMILES strings during sanitization)
- **Python 3** (Execution environment for sanitizing.py and chemical structure processing scripts)

## Examples

```
python 3_cleaningAndEnriching/sanitizing.py --input interim/tables/1_translated/structure/smiles.tsv.gz --output interim/tables/1_translated/structure/unique.tsv.gz
```

## Evaluation signals

- All output SMILES parse without exception using RDKit or equivalent chemistry library validation.
- The output table contains only unique canonical SMILES representations; no two rows encode the same chemical structure.
- A validation log clearly documents the count of input structures, valid structures retained, invalid structures rejected, and duplicates collapsed.
- No null or empty SMILES entries appear in the output table; all rows are chemically valid and non-redundant.
- The output file size and row count are consistent with expected deduplication (typically a reduction from the input due to removal of invalid and duplicate entries).

## Limitations

- Sanitization relies on the quality of the upstream SMILES translation step; systematic errors in smiles.py output will propagate.
- SMILES validation assumes standard organic chemistry rules; unusual or non-standard representations (e.g., pseudo-atoms, simplified polymers) may be rejected incorrectly.
- Canonicalization and deduplication depend on the chemistry library's perception of aromaticity and resonance; different libraries or versions may classify the same structure differently.
- The workflow does not address stereochemical validation or 3D geometry; valid 2D SMILES may still yield chemically implausible 3D structures in downstream docking.

## Evidence

- [methods] Execute smiles.py to translate and standardise SMILES strings, generating interim/tables/1_translated/structure/smiles.tsv.gz. 3. Load translated SMILES and apply sanitizing.py to validate chemical structures, remove invalid entries, and deduplicate to generate interim/tables/1_translated/structure/unique.tsv.gz.: "Load translated SMILES and apply sanitizing.py to validate chemical structures, remove invalid entries, and deduplicate to generate interim/tables/1_translated/structure/unique.tsv.gz."
- [other] The LOTUS processor applies two consecutive file-to-file transformations: smiles.py converts raw SMILES from interim/tables/0_original/structure/smiles.tsv.gz, and sanitizing.py then produces the final standardized unique structure table at interim/tables/1_translated/structure/unique.tsv.gz.: "sanitizing.py then produces the final standardized unique structure table at interim/tables/1_translated/structure/unique.tsv.gz."
- [methods] 2_editing structure – SMILES processing, sanitization, and enrichment: "SMILES processing, sanitization, and enrichment"
- [methods] 231330 | 153956 (3D|2D) unique curated structures: "231330 | 153956 (3D|2D) unique curated structures"
