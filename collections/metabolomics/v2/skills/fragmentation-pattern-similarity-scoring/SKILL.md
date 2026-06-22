---
name: fragmentation-pattern-similarity-scoring
description: Use when after feature detection and alignment have produced a feature table with MS/MS spectra, and you have access to a reference spectral database (e.g., xenobiotic reaction libraries or public databases).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - tidyverse
  - CluMSID
  - CluMSIDdata
  - grid
  - OrgMassSpecR
  - pheatmap
  - reshape2
  - MSMSsim
  - msentropy
  - readxl
  - MSDial (ver. 4.80)
  - Biotransformer 3.0
  techniques:
  - CE-MS
  - tandem-MS
  - NMR
derived_from:
- doi: 10.1021/acs.est.5c08558
  title: CMDN
evidence_spans:
- tidyverse
- CluMSID
- CluMSIDdata
- grid
- OrgMassSpecR
- pheatmap
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmdn_cq
    doi: 10.1021/acs.est.5c08558
    title: CMDN
  dedup_kept_from: coll_cmdn_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.est.5c08558
  all_source_dois:
  - 10.1021/acs.est.5c08558
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fragmentation-pattern-similarity-scoring

## Summary

Compute similarity scores between fragmentation patterns of unknown MS features and reference spectra to rank candidate metabolite annotations in untargeted metabolomics. This step bridges feature detection and confident metabolite identity assignment by quantifying spectral match quality.

## When to use

After feature detection and alignment have produced a feature table with MS/MS spectra, and you have access to a reference spectral database (e.g., xenobiotic reaction libraries or public databases). Use this skill when you need to rank and filter putative metabolite identities before final annotation, or when you want to assess confidence in structure assignments based on fragmentation similarity rather than exact mass alone.

## When NOT to use

- Input data lack MS/MS spectra or only include accurate mass — similarity scoring requires fragmentation patterns.
- Reference spectral database is absent or poorly representative of your expected metabolites (e.g., applying a xenobiotic database to endogenous metabolites).
- Feature table is already fully annotated by orthogonal high-confidence methods (e.g., NMR or authenticated standards).

## Inputs

- Aligned feature table (from feature detection and clustering)
- MS/MS spectra for each aligned feature
- Reference MS/MS spectral database (e.g., xenobiotic reaction metabolite library)

## Outputs

- Similarity score matrix (features × reference spectra)
- Ranked candidate metabolite annotations per feature
- Annotated feature table with metabolite identities and reaction pathway metadata

## How to apply

Apply MSMSsim to compute fragmentation pattern similarity scores between the MS/MS spectra of aligned unknown features and corresponding reference spectra. The tool calculates a quantitative match score (typically cosine-based or entropy-weighted similarity) for each feature–reference pair. Filter candidate annotations by similarity score threshold (article does not specify a cutoff; practitioner should validate against known standards). Pair similarity scoring with spectral entropy calculation (msentropy) to assess fragment complexity and boost confidence in high-similarity, high-entropy matches. Propagate high-confidence annotations across co-clustered features using CluMSID's cluster-based propagation logic. Export the ranked candidate list with similarity scores and reaction pathway metadata for manual review and final curation.

## Related tools

- **MSMSsim** (Computes fragmentation pattern similarity scores between unknown features and reference spectra)
- **msentropy** (Calculates spectral entropy to assess fragment complexity and confidence in similarity matches)
- **CluMSID** (Performs feature detection, alignment, and cluster-based annotation propagation of high-similarity matches)
- **OrgMassSpecR** (Calculates exact mass for metabolite candidates to filter and rank annotations alongside similarity scores)
- **MSDial (ver. 4.80)** (Compatible upstream software for feature detection and MS/MS spectrum extraction)
- **Biotransformer 3.0** (Compatible reference database and prediction tool for xenobiotic metabolite libraries)

## Evaluation signals

- Similarity scores are generated for all feature–reference pairs and fall within the expected range (e.g., 0–1 for normalized cosine similarity); no missing or invalid values.
- High-similarity matches (top-ranked candidates per feature) correspond to known or validated metabolites when checked against authenticated standards or literature.
- Spectral entropy values co-trend with similarity scores; high-confidence annotations exhibit both high similarity and high entropy (complex, informative fragmentation).
- Annotation propagation via CluMSID produces concordant identities within co-clustered features; within-cluster inconsistencies signal incorrect clustering or ambiguous reference matches.
- Final annotated feature table includes reaction pathway metadata and confidence metrics (similarity score and entropy); manual curation of borderline candidates (e.g., similarity 0.6–0.75) is feasible.

## Limitations

- MSMSsim scoring depends on high-quality, representative reference spectra; sparse or biased reference libraries may yield false-negative or false-positive matches.
- No universally optimal similarity score threshold is specified; practitioner must validate and set cutoffs empirically for their dataset and reference database.
- Fragmentation pattern similarity alone does not confirm identity; isomeric or closely related metabolites may produce indistinguishable spectra, requiring orthogonal confirmation (e.g., retention time, chemical standards, or NMR).
- CluMSID clustering parameters and entropy thresholds are not detailed in the article; default parameters may require tuning for different xenobiotic classes or MS instruments.

## Evidence

- [intro] Apply MSMSsim to compute fragmentation pattern similarity scores between unknown features and reference spectra.: "Apply MSMSsim to compute fragmentation pattern similarity scores between unknown features and reference spectra."
- [intro] Calculate spectral entropy using msentropy to assess fragment complexity and confidence.: "Calculate spectral entropy using msentropy to assess fragment complexity and confidence."
- [intro] Annotate metabolites by matching aligned features to xenobiotic reaction databases using OrgMassSpecR for exact mass calculation and CluMSID for cluster-based annotation propagation.: "Annotate metabolites by matching aligned features to xenobiotic reaction databases using OrgMassSpecR for exact mass calculation and CluMSID for cluster-based annotation propagation."
- [readme] CMDN is an 'top-down' untargeted metabolomics-based MS data processing framework to enable high-throughput and automated annotation of reaction-derived xenobiotic metabolites: "CMDN is an 'top-down' untargeted metabolomics-based MS data processing framework to enable high-throughput and automated annotation of reaction-derived xenobiotic metabolites"
- [readme] Other compatible software/web applications included: MSDial (ver. 4.80) Biotransformer 3.0: "Other compatible software/web applications included: MSDial (ver. 4.80) Biotransformer 3.0"
