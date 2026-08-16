---
name: metabolite-annotation-scoring
description: Use when you have a feature table with candidate metabolite annotations (m/z, retention time, chemical identifiers) from MS/MS spectra or external tools (SIRIUS, GNPS), sample metadata linking samples to organisms, and you need to prioritize candidates by both annotation quality AND biological.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3678
  tools:
  - R
  - Docker
  - tima (Taxonomically Informed Metabolite Annotation)
  - LOTUS
  - SIRIUS
  - GNPS-FBMN
  techniques:
  - LC-MS
derived_from:
- doi: 10.3389/fpls.2019.01329
  title: tima
- doi: 10.1038/nbt.3597
  title: ''
- doi: 10.1038/s41592-019-0344-8
  title: ''
evidence_spans:
- '[![r-universe badge](https://taxonomicallyinformedannotation.r-universe.dev/tima/badges/version?&color=blue&style=classic.png)]'
- '[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white.png)]'
- '[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white.png)](https://hub.docker.com/r/adafede/tima-r/)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tima_cq
    doi: 10.3389/fpls.2019.01329
    title: tima
  dedup_kept_from: coll_tima_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fpls.2019.01329
  all_source_dois:
  - 10.3389/fpls.2019.01329
  - 10.1038/nbt.3597
  - 10.1038/s41592-019-0344-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-annotation-scoring

## Summary

Rank candidate metabolite annotations by combining spectral/structural confidence scores with taxonomic likelihood weights, ensuring only biochemically plausible metabolites are prioritized for the sample's organism and its phylogenetic relatives. This skill integrates mass spectrometry evidence with biological context to reduce false-positive annotations.

## When to use

You have a feature table with candidate metabolite annotations (m/z, retention time, chemical identifiers) from MS/MS spectra or external tools (SIRIUS, GNPS), sample metadata linking samples to organisms, and you need to prioritize candidates by both annotation quality AND biological relevance to the sample's taxon. Use this skill when unfiltered annotation lists are too long, when multiple tools have produced overlapping but ranked candidates, or when you need reproducible triage before manual curation.

## When NOT to use

- Input is already a validated, single-best annotation per feature (no candidate set to rank).
- Sample organism is unknown or not in the taxonomic reference database; taxonomic filtering will be uninformative.
- Spectral data is unavailable and no external annotation tool (SIRIUS, GNPS) output exists to provide annotation confidence scores.

## Inputs

- feature quantification table (CSV/TSV with feature ID, retention time, m/z, sample intensities)
- candidate metabolite annotations (with chemical identifiers, spectral similarity scores or MS/MS match scores)
- sample metadata (links samples to organism/taxon identifiers)
- taxonomic reference database (structure-organism pairs; LOTUS or custom)
- spectral library or pre-computed similarity scores (optional; from SIRIUS, GNPS, or in-house MassBank)

## Outputs

- scored and ranked annotation table (feature ID, candidate metabolite, annotation_confidence, taxonomic_weight, combined_score, rank)
- filtered candidate set (top-ranked annotations per feature, optionally thresholded by combined score)
- audit trail (which metabolites were filtered and why, for reproducibility)

## How to apply

Load the candidate metabolite annotations alongside the organism/taxon context for each sample. Retrieve or pre-compute a taxonomic reference database (e.g., LOTUS >650k structure-organism pairs) and optional spectral similarity scores. For each candidate, filter by taxonomic relevance: determine whether the putative metabolite is chemically plausible or biochemically documented in the sample's taxon or its phylogenetic neighbors using the reference database. Assign each annotation a taxonomic weight reflecting the metabolic likelihood in the organism's lineage (higher weight for metabolites native to or commonly found in that taxon). Combine the annotation confidence score (e.g., spectral match score, SIRIUS rank) with the taxonomic weight via multiplication or a documented formula. Rank all candidates by the combined score (annotation_confidence × taxonomic_weight) and output a scored, ranked annotation table. Validate that low-scoring metabolites are either rare in the taxon or absent, and that top-ranked metabolites align with known biochemistry of the organism.

## Related tools

- **tima (Taxonomically Informed Metabolite Annotation)** (reference implementation of the annotation scoring and taxonomic weighting workflow; provides R package, Shiny app, and Docker container for end-to-end pipeline) — https://github.com/taxonomicallyinformedannotation/tima
- **LOTUS** (default taxonomic reference database (>650k structure-organism pairs) for biochemical plausibility filtering) — https://lotusnprod.github.io/lotus-manuscript/
- **SIRIUS** (external annotation tool producing ranked structural candidates and confidence scores (versions 5/6 compatible)) — https://doi.org/10.1038/s41592-019-0344-8
- **GNPS-FBMN** (optional external annotation source providing spectral cluster matches and confidence metrics) — https://doi.org/10.1038/nbt.3597

## Examples

```
tima::run_app()
# Or via CLI: docker run -v "$(pwd)/.tima/data:/home/tima-user/.tima/data" adafede/tima-r
```

## Evaluation signals

- Combined score is the product (or documented combination) of annotation_confidence and taxonomic_weight, and is monotonically related to rank (higher score → lower rank number).
- Taxonomic weights are ≥ 0 and reflect the organism's phylogenetic distance to reference organisms in the database; metabolites native to the sample's taxon score higher than those from distant clades.
- Candidate metabolites filtered out have taxonomic_weight = 0 (absent from taxon and relatives) or are documented as biochemically implausible in the README/logs.
- Top-ranked annotations (rank 1–3 per feature) are manually validated against curated literature or confirmed biochemical pathways for the organism; false-positive rate is reported.
- Reproducibility: re-running the pipeline with the same inputs, reference database version, and scoring formula produces identical ranks and scores.

## Limitations

- Taxonomic reference database (LOTUS, ISDB) has incomplete coverage; rare or novel metabolites in under-studied organisms may be penalized or absent, leading to false negatives.
- Scoring formula (e.g., multiplication of confidence × weight) assumes independence of spectral and taxonomic evidence; interactions (e.g., a high-confidence match to a rare metabolite) may not be captured.
- Performance degrades when annotation confidence scores from SIRIUS or GNPS are unreliable or absent; the skill is optimized for data with ranked candidate lists, not single-hit scenarios.
- Taxonomic weighting requires correct organism identification and taxonomy; misidentified or mislabeled samples will produce misleading scores.
- No automated validation of scoring output; manual curation is still needed to catch edge cases (e.g., isomers, adducts) and confirm biological relevance.

## Evidence

- [other] Filter candidate annotations by taxonomic relevance: for each candidate, determine whether the putative metabolite is chemically plausible or biochemically documented in the sample's taxon or its biological neighbors.: "Filter candidate annotations by taxonomic relevance: for each candidate, determine whether the putative metabolite is chemically plausible or biochemically documented in the sample's taxon or its"
- [other] Weight each annotation by a taxonomic score reflecting the metabolic likelihood in the organism's lineage (higher weight for metabolites native to or commonly found in that taxon or phylogenetic relatives).: "Weight each annotation by a taxonomic score reflecting the metabolic likelihood in the organism's lineage (higher weight for metabolites native to or commonly found in that taxon or phylogenetic"
- [other] Rank all candidates by their combined score (annotation confidence × taxonomic weight) and output the final scored and ranked annotation table.: "Rank all candidates by their combined score (annotation confidence × taxonomic weight) and output the final scored and ranked annotation table."
- [readme] The initial work is available at https://doi.org/10.3389/fpls.2019.01329, with many improvements made since then.: "The initial work is available at https://doi.org/10.3389/fpls.2019.01329, with many improvements made since then."
- [other] Retrieve or load the taxonomic reference database and spectral library (or similarity scores pre-computed).: "Retrieve or load the taxonomic reference database and spectral library (or similarity scores pre-computed)."
