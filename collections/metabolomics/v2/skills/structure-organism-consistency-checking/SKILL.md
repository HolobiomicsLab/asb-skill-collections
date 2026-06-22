---
name: structure-organism-consistency-checking
description: Use when after curating structure-organism pairs from multiple source databases (1_curating stage), when you need to filter curated pairs into high-confidence subsets for downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3361
  tools:
  - R
  - 2_validating.R
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

# structure-organism-consistency-checking

## Summary

A validation filter that cross-references curated structure-organism pairs against organism and structure dictionaries to verify presence, consistency, and metadata completeness before promoting pairs to a high-confidence platinum collection. This skill ensures that only pairs with validated dictionary entries, consistent reference metadata, and no conflicting assertions advance downstream.

## When to use

After curating structure-organism pairs from multiple source databases (1_curating stage), when you need to filter curated pairs into high-confidence subsets for downstream analysis. Apply this skill when you have a mixed-quality set of structure-organism associations and require a mechanism to distinguish platinum-tier (high-confidence, complete metadata) pairs from lower-confidence candidates.

## When NOT to use

- Input is already a platinum or validated collection—re-validating is redundant.
- Your analysis goal requires all curated pairs, not just high-confidence ones; use the full curated table instead.
- Reference dictionaries are incomplete or not yet built; validation will have high false-negative rates.

## Inputs

- interim/tables/3_curated/table.tsv.gz (curated structure-organism pairs)
- interim/dictionary/organism/dictionary.tsv.gz (organism reference dictionary)
- interim/dictionary/structure/dictionary.tsv.gz (structure reference dictionary)
- interim/dictionary/reference/dictionaryOrganism.tsv.gz (reference organism metadata)
- interim/dictionary/reference/metadata.tsv.gz (reference literature metadata)

## Outputs

- platinum.tsv.gz (validated structure-organism pairs meeting platinum-tier standards)
- validation flags and metadata columns (retained for traceability)

## How to apply

Load the curated table (interim/tables/3_curated/table.tsv.gz) alongside organism and structure reference dictionaries (interim/dictionary/organism/dictionary.tsv.gz and interim/dictionary/structure/dictionary.tsv.gz). For each structure-organism pair, perform a lookup to confirm both the structure ID and organism ID exist in their respective dictionaries and that their metadata entries are consistent. Cross-validate reference metadata (interim/dictionary/reference/dictionaryOrganism.tsv.gz and metadata.tsv.gz) for each pair's associated literature citations to ensure no conflicting assertions. Apply quality filters to retain only pairs meeting platinum-tier standards—high-confidence mappings, complete metadata columns, and validated cross-references. Write passing pairs to platinum.tsv.gz with all validation flags and metadata columns preserved to enable traceability.

## Related tools

- **R** (Primary language for loading curated tables, dictionaries, and metadata; performing cross-reference lookups and validation logic; writing validated output.) — https://github.com/lotusnprod/lotus-processor/wiki
- **2_validating.R** (Main validation script that implements the structure-organism consistency check, dictionary cross-referencing, and platinum collection filtering.) — https://github.com/lotusnprod/lotus-processor

## Examples

```
# Run validation within lotus-processor workflow
make MODE=test lotus-bloom
# This executes 2_validating.R which loads interim/tables/3_curated/table.tsv.gz and dictionaries, performs cross-reference validation, and writes platinum.tsv.gz
```

## Evaluation signals

- Every structure ID in platinum.tsv.gz is present and consistent in interim/dictionary/structure/dictionary.tsv.gz (no orphaned structures).
- Every organism ID in platinum.tsv.gz is present and consistent in interim/dictionary/organism/dictionary.tsv.gz (no orphaned organisms).
- Every reference citation in platinum.tsv.gz has a matching entry in interim/dictionary/reference/metadata.tsv.gz with no conflicting assertions.
- Row count in platinum.tsv.gz is less than or equal to the input curated table (filtering reduces or maintains size, never increases).
- All validation flag columns and metadata columns are preserved in platinum.tsv.gz; no columns are dropped during filtering.

## Limitations

- Validation quality depends entirely on the completeness and accuracy of the reference dictionaries; missing or incorrect dictionary entries will cause false negatives.
- Conflicting assertions in reference metadata may not be detected if conflicts are not explicitly marked in dictionaryOrganism.tsv.gz or metadata.tsv.gz.
- The platinum-tier standard (e.g., definition of 'high-confidence mapping', 'complete metadata') is not formally specified in the provided documentation and may vary by curator intent.
- No changelog is documented, so version history and updates to validation rules are not traceable.

## Evidence

- [other] Cross-reference each structure-organism pair against organism dictionary and structure dictionary to verify presence and consistency: "Cross-reference each structure-organism pair against organism dictionary (interim/dictionary/organism/dictionary.tsv.gz) and structure dictionary (interim/dictionary/structure/dictionary.tsv.gz) to"
- [other] Validate reference metadata for each pair's associated literature citations: "Validate reference metadata (interim/dictionary/reference/dictionaryOrganism.tsv.gz and metadata.tsv.gz) for each pair's associated literature citations."
- [other] Apply quality filters to retain only pairs meeting platinum-tier standards: "Apply quality filters to retain only pairs meeting platinum-tier standards (e.g., high-confidence mappings, complete metadata, no conflicting assertions)."
- [methods] 3_analyzing: 1_sampling.R, 2_validating.R producing platinum.tsv.gz: "3_analyzing: 1_sampling.R, 2_validating.R producing platinum.tsv.gz"
- [other] The 2_validating.R step operates within the 3_analyzing stage as a validation filter that processes curated pairs: "The 2_validating.R step operates within the 3_analyzing stage as a validation filter that processes curated pairs and produces platinum.tsv.gz as its output."
