---
name: recursive-propagation-algorithm-development
description: Use when when you have constructed a two-layer metabolite annotation network (knowledge-driven and data-driven) and need to propagate initial seed annotations (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - MrnAnnoAlgo3 (MetDNA3)
  techniques:
  - CE-MS
derived_from:
- doi: 10.1038/s41467-025-63536-6
  title: MetDNA3
evidence_spans:
- '`MrnAnnoAlgo3` is the core algorithm module of **MetDNA3**, designed to annotate metabolites'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# recursive-propagation-algorithm-development

## Summary

Implement a recursive annotation propagation algorithm that iteratively refines metabolite identities by leveraging confidence scores and relationships across both knowledge-driven (biochemical ontology) and data-driven (MS2 similarity) network layers. This skill combines topology-based traversal with confidence-weighted evidence aggregation to enhance metabolite annotation coverage and accuracy in untargeted metabolomics.

## When to use

When you have constructed a two-layer metabolite annotation network (knowledge-driven and data-driven) and need to propagate initial seed annotations (e.g., from database matches or high-confidence MS2 similarity) across the network to infer identities for unannotated or ambiguous metabolite nodes. Apply this skill when annotation confidence from a single layer is insufficient or when you wish to leverage complementary evidence from both biochemical relationships and experimental co-occurrence patterns simultaneously.

## When NOT to use

- Input metabolite network is single-layer or unimodal (only knowledge-driven OR only data-driven) — the propagation algorithm's advantage derives from leveraging both layers; single-layer networks offer no comparative benefit.
- Initial seed annotations have uniformly low confidence or are sparse (< 5–10% of nodes); insufficient starting evidence will propagate noise rather than refine identities.
- Metabolite identities are already comprehensively annotated from a single authoritative database; propagation is unnecessary and may introduce conflicts.

## Inputs

- Two-layer interactive metabolite network with knowledge-driven nodes/edges (biochemical pathways, metabolic reaction networks) and data-driven nodes/edges (MS2 similarity networks from experimental mass spectrometry data)
- Seed metabolite annotations with initial confidence scores for each layer
- Edge weight matrices for both layers (e.g., reaction reliability scores, MS2 cosine similarity values)

## Outputs

- Recursively refined metabolite annotations with aggregated confidence scores across iterations
- Annotation propagation trajectories documenting which layer(s) contributed to each metabolite identity inference
- Final annotation table with coverage metrics (proportion of metabolites annotated before and after propagation)

## How to apply

Begin by defining confidence scores for initial metabolite annotations from both layers (e.g., database match reliability from knowledge-driven layer, MS2 cosine similarity from data-driven layer). Implement a recursive traversal algorithm that, for each annotated metabolite node, visits neighboring nodes in both network layers and aggregates confidence evidence from both paths. At each recursion step, compute a refined confidence score by combining parent node confidence with edge weights (e.g., reaction certainty, feature similarity quantiles) and layer-specific priors. Terminate recursion when confidence increments fall below a threshold (e.g., < 0.01) or maximum iteration depth is reached. Validate the algorithm by comparing final annotation assignments for a test metabolite set against known reference annotations, checking for improved coverage and maintained consistency across iterations.

## Related tools

- **MrnAnnoAlgo3 (MetDNA3)** (Core algorithm module that implements the two-layer interactive networking topology and recursive annotation propagation for metabolite annotation in untargeted metabolomics) — https://github.com/ZhuMetLab/MrnAnnoAlgo3

## Evaluation signals

- Annotation coverage increases monotonically across recursion iterations (or reaches stable plateau) with no decrease in already-assigned confidences.
- Aggregated confidence scores for each metabolite reflect contributions from both layers (i.e., annotated nodes show non-zero evidence from knowledge-driven AND data-driven pathways when applicable).
- Recursively annotated metabolites match reference annotations with precision ≥ 90% when compared against a test set with known identities; novel propagated annotations are chemically plausible (e.g., belong to same pathway or biochemical class as seed annotation).
- Recursion terminates within predetermined iteration count (e.g., < 50 iterations) and execution time is < 1 hour for typical untargeted metabolomics datasets (consistent with '10-fold faster' claim).
- Cross-validation on held-out seed annotations demonstrates that algorithm recovers true identities with precision comparable to or exceeding single-layer annotation methods.

## Limitations

- Algorithm performance is sensitive to the quality and completeness of the underlying two-layer network; sparse or incomplete knowledge-driven or data-driven layers will limit effective propagation.
- Confidence score aggregation is heuristic-dependent (choice of weighting scheme, layer priors, convergence threshold); different parameterizations may yield different final annotations.
- Propagation can amplify errors from initial seed annotations if incorrect high-confidence annotations are recursively reinforced across iterations; robust filtering of seed quality is critical.
- Algorithm assumes that both network layers are reasonably well-aligned (i.e., that knowledge-driven and data-driven relationships are largely congruent); highly conflicting layer evidence may produce ambiguous or contradictory annotations.

## Evidence

- [other] implement-recursive-propagation: "Implement the recursive annotation propagation algorithm that iteratively refines metabolite identities by leveraging confidence scores and relationships from both layers."
- [readme] two-layer-topology: "designed to annotate metabolites through a two-layer interactive networking topology (knowledge-driven and data-driven) and recursive annotation propagation algorithms"
- [readme] performance-claim: "Processes a typical untargeted metabolomics dataset in just one hour—over 10-fold faster than previous versions."
- [readme] layer-definitions: "Integrates knowledge-driven (biochemical pathways, metabolic reaction networks) and data-driven (experimental MS2 similarity networks) layers for comprehensive and accurate metabolite annotation."
