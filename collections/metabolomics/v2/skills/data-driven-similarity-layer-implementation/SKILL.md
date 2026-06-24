---
name: data-driven-similarity-layer-implementation
description: Use when you have untargeted metabolomics mass spectrometry data (MS2
  spectra with m/z values and intensities) and an existing knowledge-driven metabolite
  network, and you need to enhance annotation accuracy and coverage by leveraging
  experimental similarity patterns rather than relying solely on.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MrnAnnoAlgo3 (MetDNA3)
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1038/s41467-025-63536-6
  title: MetDNA3
evidence_spans:
- '`MrnAnnoAlgo3` is the core algorithm module of **MetDNA3**, designed to annotate
  metabolites'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metdna3_cq
    doi: 10.1038/s41467-025-63536-6
    title: MetDNA3
  dedup_kept_from: coll_metdna3_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-63536-6
  all_source_dois:
  - 10.1038/s41467-025-63536-6
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# data-driven-similarity-layer-implementation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct and integrate a data-driven layer into a two-layer metabolite annotation topology by extracting feature similarity and co-occurrence patterns from mass spectrometry data. This layer complements knowledge-driven annotations and enables recursive propagation of metabolite identities across experimentally-derived networks.

## When to use

You have untargeted metabolomics mass spectrometry data (MS2 spectra with m/z values and intensities) and an existing knowledge-driven metabolite network, and you need to enhance annotation accuracy and coverage by leveraging experimental similarity patterns rather than relying solely on biochemical ontologies or reaction networks.

## When NOT to use

- Input consists of targeted metabolomics data with pre-assigned metabolite identities and no ambiguity requiring network propagation.
- Mass spectrometry data quality is poor or spectral similarity metrics cannot be reliably calculated (e.g., very low MS2 spectral density, missing fragmentation data).
- The analysis goal is primarily to validate known metabolic pathways rather than discover or annotate novel metabolite features.

## Inputs

- mass spectrometry dataset (MS2 spectra with m/z values and intensity measurements)
- feature abundance or co-occurrence matrix from untargeted metabolomics experiment
- knowledge-driven metabolite network or reference annotations

## Outputs

- data-driven similarity network layer (metabolite nodes with weighted edges representing MS2 cosine similarity or co-occurrence)
- integrated two-layer interactive networking topology
- refined metabolite annotation set with propagated confidence scores

## How to apply

Extract MS2 feature similarity scores (e.g., cosine similarity between fragmentation patterns) and co-occurrence patterns (e.g., metabolites appearing together in samples or sharing spectral properties) from your experimental mass spectrometry dataset. Represent these relationships as a second network layer with metabolite nodes and weighted edges proportional to similarity or co-occurrence strength. Integrate this data-driven layer into the two-layer interactive networking topology so that metabolite nodes can be queried and enriched through both pathways simultaneously. Implement or invoke the recursive annotation propagation algorithm that iteratively refines metabolite identities by leveraging confidence scores and relationships from both the data-driven and knowledge-driven layers. Validate the combined architecture by applying it to a test metabolite set with known reference annotations and confirming that annotation outputs remain consistent and are improved relative to knowledge-driven-only or data-driven-only approaches.

## Related tools

- **MrnAnnoAlgo3 (MetDNA3)** (Core algorithm module that implements the two-layer interactive networking topology and recursive annotation propagation, integrating both knowledge-driven and data-driven layers for metabolite annotation) — https://github.com/ZhuMetLab/MrnAnnoAlgo3

## Evaluation signals

- Data-driven layer successfully connects metabolites with non-zero weighted edges, and edge weights correlate with independent validation metrics (e.g., shared biological pathways or co-expression patterns).
- Recursive annotation propagation converges (confidence scores stabilize across iterations) and produces deterministic, reproducible outputs when applied to the same input metabolite set.
- Metabolite annotation recall and precision improve when using the combined two-layer topology compared to using the data-driven layer alone or knowledge-driven layer alone, validated against reference annotations.
- No isolated or orphaned metabolite nodes in the data-driven layer; all annotated features maintain at least one edge to another node with sufficient similarity/co-occurrence confidence.
- Integration of data-driven and knowledge-driven layers produces non-redundant or conflicting annotations; conflicts are resolved via confidence scoring or explicit prioritization logic.

## Limitations

- Data-driven layer quality depends critically on MS2 spectral density and reproducibility; sparse or low-quality spectra may yield unreliable similarity networks.
- Cosine similarity thresholds and co-occurrence cutoffs are not specified in the README; users must validate these parameters empirically for their dataset.
- The recursive annotation propagation algorithm's convergence properties and sensitivity to initialization are not documented; failure modes (e.g., cycles, oscillation) are not discussed.
- MetDNA3 full functionality requires additional ecosystem modules beyond MrnAnnoAlgo3; the README does not detail which data-driven network construction steps are implemented in the algorithm module vs. the webserver.

## Evidence

- [other] Two-layer interactive networking topology combining knowledge-driven and data-driven layers with recursive annotation propagation algorithms: "designed to annotate metabolites through a two-layer interactive networking topology (knowledge-driven and data-driven) and recursive annotation propagation algorithms"
- [other] Data-driven layer incorporates feature similarity and co-occurrence patterns from mass spectrometry data: "Define the data-driven layer components, incorporating feature similarity and co-occurrence patterns derived from experimental mass spectrometry data."
- [other] Integration enables simultaneous querying and enrichment through both layers: "Implement the interactive networking topology that bridges both layers, enabling metabolite nodes to be queried and enriched through both pathways simultaneously."
- [readme] Two-layer networking integrates knowledge-driven and data-driven experimental MS2 similarity networks: "Integrates **knowledge-driven** (biochemical pathways, metabolic reaction networks) and **data-driven** (experimental MS2 similarity networks) layers for comprehensive and accurate metabolite"
- [readme] Recursive algorithm leverages both network layers to enhance annotation coverage and accuracy: "An efficient topology-based annotation propagation algorithm leveraging both network layers to enhance annotation coverage and accuracy."
