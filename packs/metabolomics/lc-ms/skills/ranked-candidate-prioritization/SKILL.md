---
name: ranked-candidate-prioritization
description: Use when you have a feature quantification table (m/z, retention time, peak areas) and candidate metabolite annotations (chemical identifiers, MS/MS spectra matches, or SIRIUS/GNPS predictions) linked to a sample organism or taxon, and you need to prioritize which candidates are most biochemically.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3437
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0154
  tools:
  - R
  - Docker
  - tima
  - LOTUS
  - SIRIUS v5/v6
  - GNPS-FBMN
  techniques:
  - LC-MS
derived_from:
- doi: 10.3389/fpls.2019.01329
  title: tima
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ranked-candidate-prioritization

## Summary

Rank and weight candidate metabolite annotations by integrating taxonomic provenance information to produce a final scored and confidence-ordered annotation table. This skill addresses the core problem of annotation ambiguity: given multiple m/z and retention-time matches, which candidate is most likely correct for the sample's organism?

## When to use

You have a feature quantification table (m/z, retention time, peak areas) and candidate metabolite annotations (chemical identifiers, MS/MS spectra matches, or SIRIUS/GNPS predictions) linked to a sample organism or taxon, and you need to prioritize which candidates are most biochemically plausible in that organism's metabolism rather than treating all matches equally.

## When NOT to use

- Input candidates are already manually validated or represent a single organism's known set of metabolites (single-source reference library with no ambiguity).
- Sample organism taxonomy is unknown or unavailable; without taxon context, taxonomic weighting cannot be computed.
- Annotation task is untargeted global discovery with no prior metabolite reference; ranking will degrade if reference databases are incomplete or misannotated.

## Inputs

- feature quantification table (.csv/.tsv with feature ID, m/z, retention time, sample intensity columns)
- candidate metabolite annotations (structure IDs, chemical names, m/z, retention time, match scores from spectral library, SIRIUS, or GNPS-FBMN)
- sample metadata linking samples to organism/taxon identifiers
- taxonomic reference database (e.g., LOTUS structure-organism pairs, HMDB, BMDB, BiGG, or custom library)
- spectral similarity scores or pre-computed MS/MS match confidence values

## Outputs

- ranked annotation table (.csv/.tsv) with columns: feature ID, m/z, retention time, candidate structure, annotation confidence score, taxonomic weight, composite ranking score, organism context, plausibility flag
- top-1 or top-N annotation per feature with full scoring breakdown for downstream use or validation

## How to apply

Load candidate annotations alongside the sample's organism/taxon context and a taxonomic reference database (e.g., LOTUS with >650k structure-organism pairs). For each candidate, compute a taxonomic score that reflects whether the putative metabolite is documented in, chemically native to, or commonly found in the sample's taxon or its phylogenetic neighbors. Weight each annotation by this taxonomic likelihood. Combine the annotation confidence score (e.g., spectral similarity, m/z accuracy) with the taxonomic weight to produce a composite ranking score. Rank all candidates by this composite score (annotation confidence × taxonomic weight) and output a final annotation table ordered by descending rank, with confidence, taxonomic weight, and supporting evidence columns retained for interpretation and filtering.

## Related tools

- **tima** (Implements the complete taxonomically-informed annotation pipeline with built-in candidate ranking, weighting, and scoring using LOTUS and other metabolite reference libraries.) — https://github.com/taxonomicallyinformedannotation/tima
- **R** (Primary implementation language for tima's annotation scoring, weighting, and ranking engine.)
- **Docker** (Containerized runtime environment for tima annotation pipeline, encapsulating all dependencies and taxonomic reference data.) — https://hub.docker.com/r/adafede/tima-r/
- **LOTUS** (Default structure-organism pairs reference database (>650k pairs) used to assign taxonomic plausibility weights to candidate metabolites.) — https://lotusnprod.github.io/lotus-manuscript/
- **SIRIUS v5/v6** (Optional input: molecular formula and structure predictions that provide initial annotation confidence scores before taxonomic ranking.)
- **GNPS-FBMN** (Optional input: spectral library matches and networking results that generate candidate annotation lists with initial similarity scores.)

## Examples

```
tima::run_app()
# or via Docker:
docker run --user tima-user --memory="12g" -v "$(pwd)/.tima/data:/home/tima-user/.tima/data" -p 3838:3838 adafede/tima-r
```

## Evaluation signals

- Composite ranking scores are monotonically ordered (descending) with no NaN or Inf values; all candidates have non-negative scores.
- Taxonomic weights are in plausible range (e.g., 0–1 or 0–100) and reflect biological distance: metabolites native to sample taxon have higher weight than distant phylogenetic relatives.
- Top-ranked candidate per feature has highest combined score and is documented in (or biochemically plausible for) the sample organism according to the reference database.
- Candidates ranked below are either from distantly related taxa, have lower spectral/structural match confidence, or lack supporting biochemical evidence in the reference library.
- Annotation table includes retained feature ID, m/z, retention time, and organism context; no data loss during merging of confidence and taxonomic scores.

## Limitations

- Ranking quality depends on completeness and accuracy of the taxonomic reference database; metabolites not in LOTUS or other library cannot be weighted and default to low or zero taxonomic score, risking false negatives.
- Sample organism taxonomy must be provided and correctly mapped to reference database taxonomy; misidentified or ambiguous organism context will propagate incorrect weights.
- Composite score integrates annotation confidence and taxonomic weight multiplicatively; if either component is zero or very low, the product may suppress valid candidates even if one component is high.
- Pipeline assumes MS/MS spectra or other annotation confidence scores are available; features with no spectral data or external predictions cannot be ranked and may be filtered or assigned default scores.
- Metabolites rare in the reference database or from organisms with sparse coverage in LOTUS may be systematically deprioritized even if genuinely present in the sample.

## Evidence

- [other] Filter candidate annotations by taxonomic relevance: for each candidate, determine whether the putative metabolite is chemically plausible or biochemically documented in the sample's taxon or its biological neighbors.: "Filter candidate annotations by taxonomic relevance: for each candidate, determine whether the putative metabolite is chemically plausible or biochemically documented in the sample's taxon or its"
- [other] Weight each annotation by a taxonomic score reflecting the metabolic likelihood in the organism's lineage (higher weight for metabolites native to or commonly found in that taxon or phylogenetic relatives).: "Weight each annotation by a taxonomic score reflecting the metabolic likelihood in the organism's lineage (higher weight for metabolites native to or commonly found in that taxon or phylogenetic"
- [other] Rank all candidates by their combined score (annotation confidence × taxonomic weight) and output the final scored and ranked annotation table.: "Rank all candidates by their combined score (annotation confidence × taxonomic weight) and output the final scored and ranked annotation table."
- [other] The tima tool implements an annotation pipeline with a documented workflow that has been iteratively improved since its initial publication: "The tima tool implements an annotation pipeline with a documented workflow that has been iteratively improved since its initial publication in Frontiers in Plant Science"
- [readme] Structure-organism pairs library - We provide LOTUS (>650k pairs) as default: "Structure-organism pairs library - We provide LOTUS (>650k pairs) as default"
