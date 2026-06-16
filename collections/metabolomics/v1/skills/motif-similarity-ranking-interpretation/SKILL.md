---
name: motif-similarity-ranking-interpretation
description: Use when after executing MassQL queries against a MotifDB reference database and retrieving ranked motif matches, when you need to determine which database entries represent true structural correspondence versus spurious matches, and to decide whether a motif's top-ranking hit is sufficiently.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - MassQL
  - MotifDB
  - MS2LDA
  - Spec2Vec
derived_from:
- doi: 10.1093/bioinformatics/btx582
  title: ms2lda
evidence_spans:
- Integration with MassQL-searchable MotifDB
- Compare motifs to known entries in MotifDB
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda
    doi: 10.1093/bioinformatics/btx582
    title: ms2lda
  dedup_kept_from: coll_ms2lda
schema_version: 0.2.0
---

# motif-similarity-ranking-interpretation

## Summary

Interpret ranked MassQL-MotifDB similarity scores to assign functional meaning to discovered Mass2Motifs by evaluating match quality, ranking structure, and fragmentation pattern consistency. This skill bridges unsupervised motif discovery with reference-guided annotation by translating raw database hits into actionable substructure assignments.

## When to use

After executing MassQL queries against a MotifDB reference database and retrieving ranked motif matches, when you need to determine which database entries represent true structural correspondence versus spurious matches, and to decide whether a motif's top-ranking hit is sufficiently similar to support confident annotation.

## When NOT to use

- Input motif set has not yet been queried against MotifDB — apply MassQL query construction first.
- Match scores are unavailable or ranking structure is not preserved in the database output.
- Discovery goal is purely exploratory motif identification without reference-guided validation — skip to direct LDA interpretation.

## Inputs

- inferred motifset in JSON format (output from MS2LDA LDA modeling step)
- ranked MotifDB match records per motif (motif ID, name, composition, match score)
- original Mass2Motif fragment and neutral-loss patterns
- spectral dataset metadata (compound identities, occurrence frequencies)

## Outputs

- interpreted motif-to-database annotation assignments
- ranked similarity scores with confidence assessments
- per-motif annotation metadata (matched motif ID, name, score, structural rationale)
- annotation report documenting ranking confidence and pattern alignment

## How to apply

Load the JSON output containing ranked MotifDB matches per Mass2Motif, sorting by the provided similarity or match score (higher scores indicate greater correspondence). Examine the top-ranked entry's composition and neutral-loss patterns against the original discovered motif's fragment and neutral-loss patterns extracted from the LDA inference step; assess whether the ranked hit's mass composition aligns with the motif's observed fragments and whether neutral-loss patterns co-occur consistently. Use the ranking order as a confidence signal: a match ranked first with substantially higher score than second-ranked alternatives suggests greater specificity. Cross-reference the match against the motif's occurrence frequency across the spectral dataset and the compounds in which it appears; if a high-scoring database hit occurs in structurally diverse compounds, evaluate whether the match represents a general fragmentation pattern or a specific substructure. Document the per-motif ranking structure preserved in the JSON to enable downstream filtering or threshold-based annotation decisions.

## Related tools

- **MassQL** (query engine for constructing and executing database searches using fragment and neutral-loss patterns)
- **MotifDB** (searchable reference database containing ranked motif entries, composition, and match scores for comparison) — https://zenodo.org/records/15688609
- **MS2LDA** (generates the inferred motifset and provides LDA-learned Mass2Motif patterns as input to similarity ranking) — https://github.com/vdhooftcompmet/MS2LDA
- **Spec2Vec** (optionally supports automated annotation guidance (MAG) for motif interpretation)

## Evaluation signals

- Top-ranked MotifDB entry's mass composition and neutral-loss patterns show >80% correspondence with the original discovered motif's fragment set.
- Ranking order is monotonic or near-monotonic (scores decrease or plateau from rank 1 to N), indicating valid score ordering without artifacts.
- Per-motif JSON output preserves ranking structure with ≥2 ranked candidates per motif, enabling comparative scoring.
- Annotated motif occurs consistently across a chemically coherent compound subset (e.g., alkaloids, lipids) rather than random scatter, validating structural relevance.
- Match score spread (top score − second-place score) exceeds a domain-specific threshold (e.g., >20% relative difference), suggesting confidence in the top hit.

## Limitations

- MotifDB reference database completeness and curation directly affect match quality; sparse or outdated database entries may fail to retrieve true structural assignments.
- Ranking scores depend on MassQL query specificity; overly broad or overly narrow queries may rank spurious or missed matches.
- Neutral-loss patterns alone may not uniquely identify substructures, especially for compounds sharing common fragmentation routes; multi-evidence integration (MS/MS intensity, retention time, spectral context) is often required for high-confidence annotation.
- Top-ranked matches may reflect frequent mass motifs in the reference database rather than structurally unique substructures, potentially biasing annotation toward common fragmentations.

## Evidence

- [other] For each motif, construct a MassQL query using its fragment and neutral-loss patterns to search the MotifDB reference database.: "For each motif, construct a MassQL query using its fragment and neutral-loss patterns to search the MotifDB reference database."
- [other] Execute the MassQL search against MotifDB via the MassQL4MotifDB integration module, retrieving ranked matches sorted by similarity or match score.: "Execute the MassQL search against MotifDB via the MassQL4MotifDB integration module, retrieving ranked matches sorted by similarity or match score."
- [other] Serialize query results and MotifDB match records (motif ID, name, composition, score) to a JSON output file preserving the per-motif ranking structure.: "Serialize query results and MotifDB match records (motif ID, name, composition, score) to a JSON output file preserving the per-motif ranking structure."
- [methods] MS2LDA integrates with a MassQL-searchable MotifDB to enable comparison of discovered motifs against known database entries, supporting automated motif annotation and result retrieval.: "MS2LDA integrates with a MassQL-searchable MotifDB to enable comparison of discovered motifs against known database entries, supporting automated motif annotation and result retrieval."
- [readme] identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification: "identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification"
