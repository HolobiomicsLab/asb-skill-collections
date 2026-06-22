---
name: neutral-loss-composition-matching
description: Use when after LDA modeling has inferred a set of Mass2Motifs (in JSON format) from preprocessed MS/MS spectra and you need to annotate these motifs by retrieving matching entries from a MotifDB reference database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - MassQL
  - MotifDB
  - MS2LDA
  - Latent Dirichlet Allocation (LDA)
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

# neutral-loss-composition-matching

## Summary

Extract fragment and neutral-loss patterns from inferred Mass2Motifs and use them to construct MassQL queries for searching a MotifDB reference database, enabling automated matching of discovered motifs against known entries ranked by similarity score.

## When to use

Apply this skill after LDA modeling has inferred a set of Mass2Motifs (in JSON format) from preprocessed MS/MS spectra and you need to annotate these motifs by retrieving matching entries from a MotifDB reference database. Use it when your discovery workflow requires automated ranking and retrieval of database hits to support motif interpretation and structure elucidation.

## When NOT to use

- The input motifset has not yet been inferred by LDA; run the LDA modeling step first.
- MotifDB is not accessible or not searchable via MassQL; ensure the MassQL4MotifDB integration is configured.
- Motifs lack sufficient fragment or neutral-loss information to construct valid MassQL queries (e.g., sparse or ambiguous patterns).

## Inputs

- inferred motifset (JSON format from LDA modeling step)
- mass composition patterns (fragment m/z values per motif)
- neutral-loss patterns (per motif)
- MotifDB reference database

## Outputs

- ranked MotifDB match records per motif (JSON)
- match scores and similarity rankings
- motif ID, name, and composition for each database hit

## How to apply

Load the motifset JSON output from the LDA modeling step and extract the fragment m/z values and neutral-loss patterns for each Mass2Motif. For each motif, construct a MassQL query encoding its mass composition and neutral-loss signatures. Execute the MassQL search against the MotifDB reference database via the MassQL4MotifDB integration module, which retrieves ranked matches sorted by similarity or match score. Serialize the query results and MotifDB match records (including motif ID, name, composition, and score) to a JSON output file preserving the per-motif ranking structure. Validate output by confirming each motif has a ranked list of database matches and that scores are within expected similarity ranges.

## Related tools

- **MassQL** (Query language for constructing searches against mass spectrometry motif databases using fragment and neutral-loss patterns)
- **MotifDB** (Reference database of known mass spectrometry motifs against which discovered motifs are compared and matched)
- **MS2LDA** (Framework that produces the inferred motifset (JSON) via LDA; integration point for MotifDB matching workflow) — https://github.com/vdhooftcompmet/MS2LDA
- **Latent Dirichlet Allocation (LDA)** (Statistical model used to infer Mass2Motifs from preprocessed spectra; output motifs are the input to this skill)

## Evaluation signals

- Output JSON contains a ranked match list for every motif in the input motifset with no missing entries.
- Each ranked match includes motif ID, name, composition, and similarity/match score fields as specified.
- Match scores are numeric, within a defined range (e.g., 0–1 or 0–100), and sorted in descending order per motif.
- MassQL query construction succeeds for all motifs; failed queries are logged with diagnostic messages.
- Per-motif ranking structure is preserved in output JSON, allowing downstream visualization and manual review of top matches.

## Limitations

- Motif matching quality depends on MotifDB completeness and the precision of the MassQL query construction; sparse or ambiguous motif patterns may yield low-confidence matches.
- Search performance scales with MotifDB size; large reference databases may require computational optimization or query filtering.
- Neutral-loss pattern extraction may be incomplete if the LDA model insufficiently captures loss signatures in the training data; validation against experimental MS/MS spectra is recommended.

## Evidence

- [other] Load the inferred motifset (JSON format) produced by the LDA modeling step, extracting mass composition and neutral-loss patterns for each Mass2Motif.: "Load the inferred motifset (JSON format) produced by the LDA modeling step, extracting mass composition and neutral-loss patterns for each Mass2Motif."
- [other] For each motif, construct a MassQL query using its fragment and neutral-loss patterns to search the MotifDB reference database.: "For each motif, construct a MassQL query using its fragment and neutral-loss patterns to search the MotifDB reference database."
- [other] Execute the MassQL search against MotifDB via the MassQL4MotifDB integration module, retrieving ranked matches sorted by similarity or match score.: "Execute the MassQL search against MotifDB via the MassQL4MotifDB integration module, retrieving ranked matches sorted by similarity or match score."
- [other] Serialize query results and MotifDB match records (motif ID, name, composition, score) to a JSON output file preserving the per-motif ranking structure.: "Serialize query results and MotifDB match records (motif ID, name, composition, score) to a JSON output file preserving the per-motif ranking structure."
- [readme] MS2LDA integrates with a MassQL-searchable MotifDB to enable comparison of discovered motifs against known database entries, supporting automated motif annotation and result retrieval.: "MS2LDA integrates with a MassQL-searchable MotifDB to enable comparison of discovered motifs against known database entries, supporting automated motif annotation and result retrieval."
