---
name: taxonomic-weighting-in-annotation
description: Use when you have a feature table with candidate metabolite annotations
  (m/z, retention time, chemical identifiers) and MS/MS spectra, and you know the
  organism or taxon of origin for your samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3761
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3391
  tools:
  - R
  - Docker
  - tima (Taxonomically Informed Metabolite Annotation)
  - LOTUS
  - SIRIUS
  - GNPS-FBMN
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# taxonomic-weighting-in-annotation

## Summary

Score and rank candidate metabolite annotations by weighting them according to taxonomic plausibility within the sample organism's lineage and biochemically documented metabolite occurrence patterns. This skill integrates organism context with spectral/chemical evidence to reduce false-positive identifications and prioritize metabolites native to or commonly found in the sample's taxon or phylogenetic relatives.

## When to use

You have a feature table with candidate metabolite annotations (m/z, retention time, chemical identifiers) and MS/MS spectra, and you know the organism or taxon of origin for your samples. You want to filter and rank candidates not just by spectral similarity or chemical plausibility alone, but by likelihood of natural occurrence in that organism's metabolic context, to reduce misidentifications from ubiquitous metabolites or artifacts.

## When NOT to use

- Samples are from mixed or unknown organisms where reliable taxonomic assignment is not possible
- You lack a taxonomic reference database or biochemical occurrence data (structure-organism pairs) for your organism or its phylogenetic group
- Your input feature table does not include m/z and retention time information, or lacks sufficient spectral data (MS/MS) for similarity matching

## Inputs

- Feature quantification table (.csv/.tsv) containing feature ID, retention time (m/z), m/z, and sample intensity columns
- MS/MS spectra file (.mgf) with fragment spectra for features
- Sample metadata (.csv/.tsv) linking samples to organism/taxon identifiers
- Taxonomic reference database or spectral library (e.g., LOTUS, ISDB, or custom)
- Pre-computed or live spectral similarity scores (or external annotations from SIRIUS, GNPS-FBMN)

## Outputs

- Scored and ranked annotation table with combined scores (annotation confidence × taxonomic weight)
- Filtered candidate annotations stratified by taxonomic relevance to the sample organism
- Per-annotation taxonomic weight scores reflecting metabolic likelihood in the organism's lineage

## How to apply

Load your feature quantification table (.csv/.tsv with feature ID, retention time, m/z, sample intensities), MS/MS spectra file (.mgf), and sample metadata linking samples to organisms. Retrieve or construct a taxonomic reference database (e.g., LOTUS with >650k structure-organism pairs, or ISDB) and compute or load pre-computed spectral similarity scores. For each candidate annotation, determine whether the putative metabolite is biochemically documented in the sample's taxon or its biological neighbors using the reference database. Weight each annotation by a taxonomic score reflecting metabolic likelihood in the organism's lineage, giving higher weight to metabolites native to or commonly found in that taxon or its phylogenetic relatives. Finally, rank all candidates by their combined score (annotation confidence × taxonomic weight) and output the final scored and ranked annotation table.

## Related tools

- **tima (Taxonomically Informed Metabolite Annotation)** (Implements the complete annotation workflow including taxonomic filtering, weighting, and ranking; provides R package, Shiny app, and Docker containerization) — https://github.com/taxonomicallyinformedannotation/tima
- **LOTUS** (Provides >650k structure-organism pairs as the default taxonomic reference database for metabolite occurrence in taxa) — https://lotusnprod.github.io/lotus-manuscript/
- **SIRIUS** (Generates external molecular formula and structure annotations (v5/v6) that can be integrated as annotation confidence inputs)
- **GNPS-FBMN** (Provides spectral library matching and networking results that can be incorporated as pre-scored candidate annotations)

## Examples

```
tima::run_app()
# Or via Docker: docker run --user tima-user --memory="12g" -v "$(pwd)/.tima/_targets:/home/tima-user/.tima/_targets" -v "$(pwd)/.tima/data:/home/tima-user/.tima/data" -p 3838:3838 adafede/tima-r
```

## Evaluation signals

- Output annotation table contains a taxonomic weight column with scores reflecting metabolic likelihood; higher weights correlate with metabolites documented in the sample organism or its phylogenetic neighbors
- Combined ranking score (annotation confidence × taxonomic weight) is monotonically applied; candidates filtered out by taxonomic plausibility have near-zero or null weights
- Downstream validation: metabolite identities with high combined scores should match biochemical literature for that organism's natural products or common metabolites; low-scoring candidates that survive filtering should be rare/exotic for that taxon
- Schema validation: output contains one row per candidate with consistent m/z, retention time, chemical identifiers, annotation source, spectral similarity score, and taxonomic weight; no missing or NaN weights for ranked candidates

## Limitations

- Taxonomic weighting depends on the completeness and accuracy of the reference database (e.g., LOTUS); sparse or biased taxon coverage can lead to false negatives (correct metabolites penalized) or false positives (known metabolites in poorly documented organisms inflated in rank)
- Phylogenetic distance metrics and thresholds for 'biological neighbors' are not explicitly parameterized in the workflow description; sensitivity to relatedness definition may vary across taxa
- The approach assumes metabolite occurrence is non-random and lineage-specific; cosmopolitan or horizontally transferred metabolites may be systematically underweighted or overweighted depending on reference data biases

## Evidence

- [other] Filter candidate annotations by taxonomic relevance: for each candidate, determine whether the putative metabolite is chemically plausible or biochemically documented in the sample's taxon or its biological neighbors.: "Filter candidate annotations by taxonomic relevance: for each candidate, determine whether the putative metabolite is chemically plausible or biochemically documented in the sample's taxon or its"
- [other] Weight each annotation by a taxonomic score reflecting the metabolic likelihood in the organism's lineage (higher weight for metabolites native to or commonly found in that taxon or phylogenetic relatives).: "Weight each annotation by a taxonomic score reflecting the metabolic likelihood in the organism's lineage (higher weight for metabolites native to or commonly found in that taxon or phylogenetic"
- [other] Rank all candidates by their combined score (annotation confidence × taxonomic weight) and output the final scored and ranked annotation table.: "Rank all candidates by their combined score (annotation confidence × taxonomic weight) and output the final scored and ranked annotation table."
- [readme] Structure-organism pairs library - We provide LOTUS (>650k pairs) as default; External annotations - SIRIUS (v5/v6), GNPS-FBMN results: "Structure-organism pairs library - We provide LOTUS (>650k pairs) as default; External annotations - SIRIUS (v5/v6), GNPS-FBMN results"
- [readme] Feature quantification table (.csv/.tsv) - Peak areas/heights across samples; MS/MS spectra file (.mgf) - Fragment spectra for each or some features; Sample metadata (.csv/.tsv) - Links samples to organisms: "Feature quantification table (.csv/.tsv) - Peak areas/heights across samples; MS/MS spectra file (.mgf) - Fragment spectra for each or some features; Sample metadata (.csv/.tsv) - Links samples to"
