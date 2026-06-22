---
name: molecular-duplicate-detection-and-deduplication
description: Use when after SMILES standardization when you have a table of translated SMILES strings (e.g., interim/tables/1_translated/structure/smiles.tsv.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3324
  - http://edamontology.org/topic_0602
  tools:
  - R
  - Python
  - sanitizing.py
  - Python 3
  - smiles.py
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-duplicate-detection-and-deduplication

## Summary

Identifies and removes duplicate chemical structures from a translated SMILES table by validating structural integrity and consolidating redundant entries into a unique structure registry. This step is essential in natural products databases to ensure each distinct molecular entity is represented only once, even when sourced from multiple databases or represented in multiple formats.

## When to use

Apply this skill after SMILES standardization when you have a table of translated SMILES strings (e.g., interim/tables/1_translated/structure/smiles.tsv.gz) and need to generate a canonical, non-redundant structure table suitable for downstream analyses such as compound annotation, structure-organism pairing, or chemical similarity searches. Use it when duplicate entries arising from multi-source curation or format variation could confound enumeration, retrieval, or statistical analyses.

## When NOT to use

- Input is a pre-deduplicated structure table or a non-SMILES chemical format (e.g., InChI, molfile) without prior SMILES conversion.
- Duplicate detection is not desired because you need to preserve source-specific variant records (e.g., for traceability or multi-version tracking).
- Your goal is to retain stereoisomers or tautomers as separate entities; deduplication may conflate them depending on canonicalization depth.

## Inputs

- translated SMILES table (TSV.GZ format, e.g., interim/tables/1_translated/structure/smiles.tsv.gz)
- SMILES strings with structure identifiers and optional metadata (organism, source database, references)

## Outputs

- deduplicated unique structure table (TSV.GZ format, e.g., interim/tables/1_translated/structure/unique.tsv.gz)
- structure validation report (invalid/unparseable entries log, if generated)

## How to apply

Load the translated SMILES table using Python and apply the sanitizing.py script to validate chemical structures by parsing SMILES strings and confirming structural validity. Remove entries with invalid or unparseable SMILES. Then deduplicate the validated structures by consolidating identical molecular graphs into single canonical records, typically retaining metadata (source references, organism associations) for merged duplicates. The output is a deduplicated unique structure table (e.g., interim/tables/1_translated/structure/unique.tsv.gz) with each row representing one distinct chemical entity. Validation success is indicated by a reduction in row count (duplicates removed), successful parsing of all retained entries, and consistency of structure identifiers across the table.

## Related tools

- **sanitizing.py** (validates chemical structures from SMILES strings, removes invalid entries, and deduplicates to produce the unique structure table) — https://github.com/lotusnprod/lotus-processor
- **Python 3** (execution environment for sanitizing.py and SMILES parsing/validation) — https://www.python.org
- **smiles.py** (prior standardization step that translates raw SMILES into a format suitable for sanitization and deduplication) — https://github.com/lotusnprod/lotus-processor

## Examples

```
python 3_cleaningAndEnriching/sanitizing.py --input interim/tables/1_translated/structure/smiles.tsv.gz --output interim/tables/1_translated/structure/unique.tsv.gz
```

## Evaluation signals

- Output unique structure table has fewer rows than input translated SMILES table (duplicates successfully removed).
- All entries in the output table parse successfully as valid chemical structures (no unparseable SMILES in final output).
- Row count in output matches the count of distinct molecular graphs in the input (deduplication is complete and lossless for valid structures).
- Merged duplicate records retain associated metadata (organism, reference identifiers, source database) via aggregation or representative selection.
- Schema consistency: output table has expected columns (structure ID, canonical SMILES, InChI, or equivalent) and no null values in required fields.

## Limitations

- Deduplication relies on SMILES canonicalization, which may differ across cheminformatics libraries; structures considered distinct in one tool may be identical in another.
- Stereoisomers and tautomers may be collapsed into a single entry if the canonicalization does not distinguish them, potentially losing chemical specificity.
- Invalid or malformed SMILES strings are removed entirely, not corrected; this can result in data loss if source structures are not well-curated.
- Performance and memory usage scale with input table size; very large structure sets may require chunking or distributed processing.
- The skill does not resolve conflicting metadata (e.g., different organism assignments for the same structure); manual or rule-based curation may be needed post-deduplication.

## Evidence

- [methods] sanitizing step that validates chemical structures, removes invalid entries, and deduplicates: "apply sanitizing.py to validate chemical structures, remove invalid entries, and deduplicate to generate interim/tables/1_translated/structure/unique.tsv.gz"
- [methods] SMILES standardization and deduplication workflow in LOTUS: "The LOTUS processor applies two consecutive file-to-file transformations: smiles.py converts raw SMILES from interim/tables/0_original/structure/smiles.tsv.gz, and sanitizing.py then produces the"
- [methods] unique curated structures output: "231330 | 153956 (3D|2D) unique curated structures"
- [methods] SMILES processing and sanitization workflow step definition: "2_editing structure – SMILES processing, sanitization, and enrichment"
- [readme] repository structure and tools for processing: "Python 3 ... within the frame of current computational approaches in Natural Products research and related fields, these documented structure-organism pairs"
