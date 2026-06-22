---
name: mass-fragment-pattern-querying
description: Use when after LDA modeling has produced an inferred motifset (JSON format) containing Mass2Motifs with fragment and neutral-loss patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3088
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MassQL
  - MotifDB
  - MS2LDA
  - MAG (Mass2Motif Annotation Guidance)
  - Spec2Vec
  techniques:
  - mass-spectrometry
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1073/pnas.1608041113
  all_source_dois:
  - 10.1073/pnas.1608041113
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-fragment-pattern-querying

## Summary

Query a MassQL-searchable MotifDB reference database using fragment and neutral-loss patterns extracted from MS2LDA-inferred Mass2Motifs to retrieve ranked database matches for motif annotation. This skill bridges unsupervised motif discovery with reference-based validation and automated substructure annotation.

## When to use

Apply this skill after LDA modeling has produced an inferred motifset (JSON format) containing Mass2Motifs with fragment and neutral-loss patterns. Use it when you need to assign biological or chemical meaning to discovered motifs by comparing them against known entries in MotifDB, or when you want to rank and prioritize motif hits for downstream structural elucidation.

## When NOT to use

- Input motifset is empty or contains no fragment/neutral-loss patterns (no meaningful features to query).
- MotifDB reference database is unavailable or not pre-indexed for MassQL queries.
- You have already manually curated motif annotations and do not need automated reference matching.

## Inputs

- Inferred motifset JSON (from MS2LDA LDA modeling step, containing Mass2Motifs with fragment m/z and neutral-loss patterns)
- MotifDB reference database (MassQL-searchable, containing known motifs with their fragment and loss compositions)

## Outputs

- Ranked MotifDB match results (JSON file per motif, sorted by similarity/match score)
- Motif annotation table (motif ID, name, matched MotifDB entries, match scores, mass compositions)

## How to apply

Load the motifset JSON output from the MS2LDA modeling step and extract the mass composition and neutral-loss patterns for each Mass2Motif. For each motif, construct a MassQL query string using its fragment m/z values and neutral-loss patterns as search constraints. Execute the MassQL query against the MotifDB reference database via the MassQL4MotifDB integration module, which returns ranked matches sorted by similarity or match score (typically cosine similarity or spectral dot product). Serialize the ranked results—including motif ID, name, mass composition, and match score—into a JSON output file that preserves the per-motif ranking structure. The rationale is that comparing inferred motifs to curated reference entries reduces false-positive motifs and accelerates annotation by leveraging existing knowledge of fragmentation patterns.

## Related tools

- **MassQL** (Query language for constructing and executing fragment/neutral-loss searches against MotifDB)
- **MotifDB** (Reference database of known mass spectrometry fragmentation motifs, indexed for MassQL queries) — https://zenodo.org/records/15688609
- **MS2LDA** (Upstream topic modeling tool that produces the inferred motifset (JSON format) input to this skill) — https://github.com/vdhooftcompmet/MS2LDA
- **MAG (Mass2Motif Annotation Guidance)** (Automated annotation module that uses MotifDB matches to assign substructure meaning to Mass2Motifs) — https://github.com/vdhooftcompmet/MS2LDA
- **Spec2Vec** (Embedding and similarity metric used in conjunction with MotifDB matching for enhanced annotation) — https://zenodo.org/records/15688609

## Evaluation signals

- All Mass2Motifs in the input motifset have at least one MotifDB match with a valid match score (e.g., cosine similarity ≥ 0.5 or configured threshold).
- Output JSON preserves per-motif ranking structure and includes motif ID, matched MotifDB entry names, match scores, and mass compositions without data loss.
- Match scores are monotonically ranked (highest score first) within each motif's result list.
- Fragment and neutral-loss patterns used to construct the MassQL query are traceable in the output (e.g., via query provenance or metadata fields).
- MotifDB matches can be validated against the original fragmentation patterns in the inferred motifset (e.g., by comparing fragment m/z lists and loss values).

## Limitations

- Requires a pre-built, MassQL-indexed MotifDB reference database; results depend on the completeness and curation quality of that database.
- Match score interpretation and ranking may vary depending on the similarity metric used by MotifDB (cosine similarity, dot product, other); no universally agreed threshold for 'high-confidence' match is stated in the article.
- Motifs with highly unusual fragmentation patterns or those from understudied chemical classes may not find confident matches in MotifDB, limiting annotation.
- The skill does not validate whether matched MotifDB entries are actually correct or biologically relevant for the user's sample; automated matches still require expert curation.

## Evidence

- [other] MS2LDA integrates with a MassQL-searchable MotifDB to enable comparison of discovered motifs against known database entries, supporting automated motif annotation and result retrieval.: "MS2LDA integrates with a MassQL-searchable MotifDB to enable comparison of discovered motifs against known database entries"
- [other] For each motif, construct a MassQL query using its fragment and neutral-loss patterns to search the MotifDB reference database.: "For each motif, construct a MassQL query using its fragment and neutral-loss patterns to search the MotifDB reference database"
- [other] Execute the MassQL search against MotifDB via the MassQL4MotifDB integration module, retrieving ranked matches sorted by similarity or match score.: "Execute the MassQL search against MotifDB via the MassQL4MotifDB integration module, retrieving ranked matches sorted by similarity or match score"
- [other] Serialize query results and MotifDB match records (motif ID, name, composition, score) to a JSON output file preserving the per-motif ranking structure.: "Serialize query results and MotifDB match records (motif ID, name, composition, score) to a JSON output file preserving the per-motif ranking structure"
- [other] Load the inferred motifset (JSON format) produced by the LDA modeling step, extracting mass composition and neutral-loss patterns for each Mass2Motif.: "Load the inferred motifset (JSON format) produced by the LDA modeling step, extracting mass composition and neutral-loss patterns"
- [methods] Integration with MassQL-searchable MotifDB: "Integration with MassQL-searchable MotifDB"
- [readme] This tool significantly enhances the capabilities described in the original MS2LDA paper (2016), offering users an integrated workflow with improved usability, detailed visualizations: "This tool significantly enhances the capabilities described in the original MS2LDA paper (2016), offering users an integrated workflow"
