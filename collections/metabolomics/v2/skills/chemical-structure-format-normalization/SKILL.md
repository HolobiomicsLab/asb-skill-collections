---
name: chemical-structure-format-normalization
description: Use when when integrating chemical structure data from multiple source databases that represent the same compound in different notations (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0209
  tools:
  - R
  - Python 3
  - Make
derived_from:
- doi: 10.7554/eLife.70780
  title: lotus
- doi: 10.1007/s00044-016-1764-y
  title: ''
evidence_spans:
- db/../standardizing.R, common.R
- 1_integrating.R
- Python scripts for data parsing and transformation
- 221[[smiles.py]]
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

# chemical-structure-format-normalization

## Summary

Convert and standardize chemical structure representations (SMILES, InChI, nominal identifiers) into consistent, deduplicated formats to enable accurate counting and matching of unique curated structures across 3D and 2D representations in natural products databases.

## When to use

When integrating chemical structure data from multiple source databases that represent the same compound in different notations (e.g., SMILES, InChI, or database-specific identifiers), and you need to establish a canonical form to count unique structures and enable structure-organism pair deduplication. Trigger: presence of multiple format representations in the same dataset or requirement to reconcile structures across heterogeneous sources.

## When NOT to use

- When the input is already a deduplicated structure table with validated canonical identifiers.
- When the analysis goal does not require cross-database reconciliation or structure-organism pair counting.
- When chemical structure representation differences are explicitly meaningful to the study (e.g., investigating tautomers or stereoisomers as distinct biological entities).

## Inputs

- Raw or interim structure-organism pair dataset (TSV or gzipped TSV format)
- Structure identifiers in mixed formats (SMILES, InChI, database-specific nominal IDs)
- Metadata indicating dimensionality (3D vs 2D representation)

## Outputs

- Deduplicated canonical structure identifiers (single format per compound)
- Count of unique curated structures by dimensionality (3D and 2D separate)
- Mapping table linking original identifiers to canonical forms
- Structured summary table (CSV or TSV) with unique structure metrics

## How to apply

Load structure records from the raw or interim dataset (e.g., platinum.tsv.gz) and standardize all representations by converting to a canonical format (SMILES or InChI preferred). Apply chemical structure sanitization (e.g., via RDKit in Python or equivalent R libraries) to normalize valence, remove salts, and standardize stereochemistry notation. Deduplicate by grouping normalized forms and retaining a single canonical identifier per unique structure. Separately track 3D and 2D structure representations, as the LOTUS platinum dataset maintains distinct counts (231330 in 3D, 153956 in 2D). Validate the resulting unique structure count against expected aggregates and document the format choices and exclusion criteria used.

## Related tools

- **R** (Structure standardization and deduplication scripting; used in cleaning and integration workflows (1_cleaningOriginal.R, 3_cleaningTranslated.R)) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (Chemical structure sanitization and normalization via RDKit or equivalent libraries; used in sanitizing.py and smiles.py scripts) — https://github.com/lotusnprod/lotus-processor
- **Make** (Orchestration and execution of standardization and cleaning pipelines across workflow stages) — https://github.com/lotusnprod/lotus-processor

## Examples

```
python sanitizing.py --input interim/tables/raw_structures.tsv --output interim/tables/normalized_structures.tsv --format smiles --deduplicate --split_by_dimensionality
```

## Evaluation signals

- Unique structure count matches reported aggregates: 231330 (3D) and 153956 (2D) curated structures.
- No duplicate canonical identifiers remain in the deduplicated output; each unique structure maps to exactly one canonical form.
- 3D and 2D structure representations are tracked separately and produce expected ratio and format-specific counts.
- Deduplicated structures link consistently to structure-organism pairs, with final pair count matching expected aggregate (588694 total; 484174 in 3D|2D format).
- Comparison of input and output identifier cardinality shows appropriate reduction through normalization and deduplication.

## Limitations

- Different chemical structure formats (SMILES, InChI) may encode the same compound with non-canonical variations; standardization rules must be explicitly documented and reproducible.
- Stereochemical ambiguity or unspecified stereoisomers in source data may lead to false deduplication or false distinction depending on sanitization settings.
- Separate tracking of 3D and 2D representations increases complexity; the same compound may have multiple entries if both forms are present, potentially inflating unique structure counts if not carefully managed.
- No changelog is available in the repository, so version history and updates to normalization protocols are not documented; reproducibility may be compromised across releases.

## Evidence

- [other] Extract and deduplicate structure identifiers (SMILES, InChI, or nominal identifiers) to count unique curated structures, separately for 3D and 2D structure representations.: "Extract and deduplicate structure identifiers (SMILES, InChI, or nominal identifiers) to count unique curated structures, separately for 3D and 2D structure representations."
- [other] 231330 unique curated structures in 3D and 153956 in 2D format from 42166 unique organisms: "231330 | 153956 (3D|2D) unique curated structures and 42166 unique organisms"
- [other] 588694 unique referenced structure-organism pairs split by dimensionality: "588694 | 484174 (3D|2D) unique referenced structure-organism pairs"
- [readme] Standardization and cleaning occur during data curation stage using R and Python scripts: "R - Python 3 - Java >= 17"
- [other] Comprehensive workflow includes standardization, translation, and cleaning substeps: "1_gathering: db/../standardizing.R, common.R, tcm.R"
