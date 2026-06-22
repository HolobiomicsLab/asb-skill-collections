---
name: reference-quality-validation
description: Use when when you have curated structure-organism pairs with associated reference metadata and need to verify that each pair's literature citations are present, non-conflicting, and complete before publishing them as a high-confidence validated dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3407
  tools:
  - R
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- db/../standardizing.R, common.R
- 1_integrating.R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lotus_cq
    doi: 10.7554/eLife.70780
    title: lotus
  dedup_kept_from: coll_lotus_cq
schema_version: 0.2.0
---

# reference-quality-validation

## Summary

Validates structure-organism pairs against curated reference dictionaries and metadata to ensure literature citations are complete, consistent, and meet platinum-tier quality standards before inclusion in a validated collection. This skill filters curated data by cross-referencing assertions against organism, structure, and reference authority records.

## When to use

When you have curated structure-organism pairs with associated reference metadata and need to verify that each pair's literature citations are present, non-conflicting, and complete before publishing them as a high-confidence validated dataset. Specifically: after curation (2_curating stage) and before public release, to ensure only pairs with verified reference provenance advance to platinum-tier collections.

## When NOT to use

- Input pairs have not yet passed the curation stage (2_curating) — validation presupposes cleaned, integrated organism and structure records.
- Reference dictionaries are themselves uncurated or missing authority records — validation depends on complete, authoritative reference data.
- Your goal is exploratory analysis rather than publication-grade quality assurance — this skill is designed specifically for high-confidence filtered releases.

## Inputs

- interim/tables/3_curated/table.tsv.gz (curated structure-organism pairs)
- interim/dictionary/organism/dictionary.tsv.gz (organism authority dictionary)
- interim/dictionary/structure/dictionary.tsv.gz (structure authority dictionary)
- interim/dictionary/reference/dictionaryOrganism.tsv.gz (reference organism metadata)
- interim/dictionary/reference/metadata.tsv.gz (reference literature metadata)

## Outputs

- platinum.tsv.gz (validated structure-organism pairs meeting platinum-tier standards)
- Validation flags and metadata columns (preserved for traceability)

## How to apply

Load the curated table (interim/tables/3_curated/table.tsv.gz) together with three reference dictionaries: organism dictionary, structure dictionary, and reference metadata dictionaries. For each structure-organism pair, perform cross-reference checks against the organism and structure dictionaries to confirm both entities exist and are consistently encoded. Then validate the associated reference metadata (literature citations, organism assertions, and any secondary metadata) against the reference dictionary authority records to ensure completeness and absence of conflicting assertions. Apply quality filters to retain only pairs meeting platinum-tier standards (e.g., high-confidence mappings with full metadata). Write passing pairs to the output table (platinum.tsv.gz) preserving all validation flags and metadata columns for traceability.

## Related tools

- **R** (Executes the 2_validating.R script for cross-reference checking and quality filtering of structure-organism pairs against dictionaries.) — https://github.com/lotusnprod/lotus-processor

## Evaluation signals

- All pairs in platinum.tsv.gz have corresponding entries in both organism and structure reference dictionaries (no null/unresolved references).
- Reference metadata columns are complete (no missing literature IDs, organism assertions, or citation provenance) for 100% of passing pairs.
- No conflicting reference assertions remain in output (e.g., the same pair is not associated with contradictory organism or structure assignments).
- Validation flags columns are populated and consistently documented for audit trail; rejected pairs are logged with rationale.
- Row count in platinum.tsv.gz is ≤ row count in curated input table, confirming that filtering (not inflation) has occurred.

## Limitations

- Validation quality depends entirely on the completeness and accuracy of the three reference dictionaries — garbage-in dictionaries will pass invalid pairs.
- The skill cannot detect errors in reference metadata that are already consistently recorded in the authority dictionaries (e.g., a systematic misidentification of an organism in the reference metadata will not be caught).
- Platinum-tier standards are defined by the LOTUS project and may not align with other natural products databases or validation schemes.

## Evidence

- [other] Cross-reference each structure-organism pair against organism dictionary and structure dictionary to verify presence and consistency.: "Cross-reference each structure-organism pair against organism dictionary (interim/dictionary/organism/dictionary.tsv.gz) and structure dictionary (interim/dictionary/structure/dictionary.tsv.gz) to"
- [other] Validate reference metadata for each pair's associated literature citations.: "Validate reference metadata (interim/dictionary/reference/dictionaryOrganism.tsv.gz and metadata.tsv.gz) for each pair's associated literature citations."
- [other] Apply quality filters to retain only pairs meeting platinum-tier standards.: "Apply quality filters to retain only pairs meeting platinum-tier standards (e.g., high-confidence mappings, complete metadata, no conflicting assertions)."
- [other] The 2_validating.R step operates within the 3_analyzing stage as a validation filter.: "The 2_validating.R step operates within the 3_analyzing stage as a validation filter that processes curated pairs and produces platinum.tsv.gz as its output."
- [readme] LOTUS is a comprehensive collection of documented structure-organism pairs.: "*LOTUS* is a comprehensive collection of documented structure-organism pairs. Within the frame of current computational approaches in Natural Products research"
