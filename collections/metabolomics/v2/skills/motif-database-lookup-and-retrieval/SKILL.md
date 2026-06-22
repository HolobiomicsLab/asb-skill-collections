---
name: motif-database-lookup-and-retrieval
description: Use when after completing the MS2LDA LDA modeling step when you have a JSON-serialized inferred motifset (Mass2Motifs with fragment and neutral-loss patterns) and need to annotate those motifs by comparing them against a curated MotifDB reference database to identify known structural subpatterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - MassQL
  - MotifDB
  - MS2LDA
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- Integration with MassQL-searchable MotifDB
- Compare motifs to known entries in MotifDB
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda
schema_version: 0.2.0
---

# motif-database-lookup-and-retrieval

## Summary

This skill reconstructs the MotifDB motif-matching step that converts discovered MS2LDA Mass2Motifs into MassQL queries to retrieve and rank database hits from a searchable MotifDB reference. It enables automated comparison of inferred motifs against known entries, supporting motif annotation and results export.

## When to use

Apply this skill after completing the MS2LDA LDA modeling step when you have a JSON-serialized inferred motifset (Mass2Motifs with fragment and neutral-loss patterns) and need to annotate those motifs by comparing them against a curated MotifDB reference database to identify known structural subpatterns and retrieve ranked matches.

## When NOT to use

- Input motifset is missing or malformed (required fields: fragment patterns, neutral-loss patterns per Mass2Motif)
- MotifDB is unavailable or not indexed for MassQL queries
- The discovered motifs are already manually curated or derived from known compounds (database lookup adds minimal value in validation contexts)

## Inputs

- JSON-serialized motifset from MS2LDA LDA modeling step (containing Mass2Motif definitions with fragment masses and neutral losses)
- MotifDB reference database (searchable via MassQL)

## Outputs

- JSON file with ranked MotifDB matches per Mass2Motif (motif ID, database entry name, composition, match scores)
- Annotated motif set with database cross-references

## How to apply

Load the inferred motifset in JSON format from the LDA modeling output, extracting mass composition and neutral-loss patterns for each Mass2Motif. For each motif, construct a MassQL query using its fragment and neutral-loss patterns as search parameters. Execute the MassQL search against the MotifDB reference database via the MassQL4MotifDB integration module, which returns ranked matches sorted by similarity or match score. Serialize the query results and MotifDB match records (motif ID, name, composition, match score) to a JSON output file that preserves the per-motif ranking structure. The ranking score guides interpretation of which database entries best explain the observed fragmentation patterns.

## Related tools

- **MassQL** (Query language used to construct and execute searches against MotifDB using fragment and neutral-loss patterns from discovered motifs)
- **MotifDB** (Searchable reference database of known mass spectrometry motifs and fragmentation patterns against which discovered motifs are compared) — https://zenodo.org/records/15688609
- **MS2LDA** (Topic modeling framework that infers Mass2Motifs; output motifset feeds into this database lookup skill) — https://github.com/vdhooftcompmet/MS2LDA

## Evaluation signals

- Verify that the output JSON is well-formed and contains all input motifs with at least one ranked MotifDB match (or explicit 'no match' entries)
- Check that ranked matches are ordered by descending match score within each motif's results
- Confirm that each output record includes required fields: motif ID, database entry name, composition match, and numeric score
- Validate that the per-motif ranking structure preserves the correspondence between input Mass2Motifs and their top database hits
- Compare the number of successfully matched motifs against total input motifs; unexpectedly low match rate may indicate query construction or database indexing issues

## Limitations

- Match quality depends on the completeness and curation of the MotifDB reference database; rare or novel fragmentation patterns may not retrieve any hits
- MassQL query construction from motif patterns may yield low specificity if neutral-loss and fragment patterns are ambiguous or overlapping across database entries
- Ranking score thresholds for 'true' matches are not specified in the article; users must interpret match scores in context of their application (e.g., annotation confidence vs. hypothesis generation)
- The skill assumes MotifDB is pre-indexed and accessible via MassQL; performance and availability depend on external infrastructure maintenance

## Evidence

- [other] MS2LDA integrates with a MassQL-searchable MotifDB to enable comparison of discovered motifs against known database entries: "MS2LDA integrates with a MassQL-searchable MotifDB to enable comparison of discovered motifs against known database entries, supporting automated motif annotation and result retrieval."
- [other] For each motif, construct a MassQL query using its fragment and neutral-loss patterns to search the MotifDB reference database: "For each motif, construct a MassQL query using its fragment and neutral-loss patterns to search the MotifDB reference database."
- [other] Execute the MassQL search against MotifDB via the MassQL4MotifDB integration module, retrieving ranked matches sorted by similarity or match score: "Execute the MassQL search against MotifDB via the MassQL4MotifDB integration module, retrieving ranked matches sorted by similarity or match score."
- [other] Serialize query results and MotifDB match records to a JSON output file preserving the per-motif ranking structure: "Serialize query results and MotifDB match records (motif ID, name, composition, score) to a JSON output file preserving the per-motif ranking structure."
- [readme] offering users an integrated workflow with improved usability, detailed visualizations, and a searchable motif database (MotifDB): "offering users an integrated workflow with improved usability, detailed visualizations, and a searchable motif database (MotifDB)"
