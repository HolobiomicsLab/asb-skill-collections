---
name: knowledge-graph-integration-design
description: Use when designing a metabolite annotation workflow that must simultaneously leverage established biochemical knowledge (pathway databases, reaction networks) and experimental evidence (mass spectrometry feature similarity, co-occurrence patterns).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0625
  tools:
  - MrnAnnoAlgo3 (MetDNA3)
  - MrnAnnoAlgo3
  - MetDNA3
  techniques:
  - tandem-MS
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

# knowledge-graph-integration-design

## Summary

Design and implement a two-layer interactive networking topology that bridges knowledge-driven (biochemical pathways, metabolic reaction networks) and data-driven (experimental MS2 similarity networks) graph structures to enable recursive annotation propagation across metabolite networks. This skill is essential when building comprehensive metabolite annotation systems that require both static ontological reasoning and dynamic empirical evidence.

## When to use

Apply this skill when designing a metabolite annotation workflow that must simultaneously leverage established biochemical knowledge (pathway databases, reaction networks) and experimental evidence (mass spectrometry feature similarity, co-occurrence patterns). Specifically use it when your input includes both a reference knowledge base of known metabolite relationships and experimental MS2/feature data that can reveal data-driven associations, and your goal is to achieve higher annotation coverage and accuracy than either layer alone would provide.

## When NOT to use

- Input metabolite set is already fully annotated or requires only targeted annotation of a pre-defined list — the recursive propagation overhead adds no value.
- Knowledge base is absent, incomplete, or unreliable — the knowledge-driven layer cannot meaningfully constrain the annotation space.
- Experimental data lacks feature-level similarity or co-occurrence signals (e.g., single-replicate studies with no biological or technical replicates) — the data-driven layer cannot be reliably constructed.

## Inputs

- knowledge base of metabolite relationships and biochemical ontologies (graph structure: nodes, edges, edge weights)
- experimental mass spectrometry data or feature similarity matrix (e.g., MS2 spectral similarity, feature co-occurrence patterns)
- metabolite reference set with known ground-truth annotations (for validation)
- untargeted metabolomics dataset requiring annotation

## Outputs

- two-layer interactive network topology (knowledge-driven and data-driven graph structures)
- recursive annotation propagation results (annotated metabolites with confidence scores)
- validated annotation outputs for test metabolite set
- network traversal logs (which nodes/edges were activated during propagation)

## How to apply

First, define the knowledge-driven layer by incorporating established metabolite relationships and biochemical ontologies as static graph structures (nodes = metabolites, edges = known biochemical transformations or pathway associations). Second, define the data-driven layer by deriving feature similarity and co-occurrence patterns from experimental mass spectrometry data (nodes = metabolites, edges = empirical similarity scores or co-abundance signals). Third, implement an interactive networking topology that bridges both layers, allowing metabolite nodes to be queried and enriched through both pathways simultaneously — this typically involves edge-merging or dual-path traversal logic. Fourth, implement a recursive annotation propagation algorithm that iteratively refines metabolite identities by leveraging confidence scores and relationships from both layers, propagating annotations across the network until convergence or a stopping threshold is reached. Fifth, validate that the combined architecture produces consistent annotation outputs when applied to a test metabolite set with known reference annotations, checking that annotation coverage and precision improve over single-layer baselines.

## Related tools

- **MrnAnnoAlgo3** (core algorithm module implementing two-layer interactive networking topology and recursive annotation propagation for metabolite annotation) — https://github.com/ZhuMetLab/MrnAnnoAlgo3
- **MetDNA3** (full ecosystem integrating MrnAnnoAlgo3 as the core algorithm module; provides webserver interface and additional modules for large-scale metabolomic studies) — http://metdna.zhulab.cn

## Examples

```
devtools::install_github('ZhuMetLab/MrnAnnoAlgo3'); library(MrnAnnoAlgo3); result <- annotate_metabolites(knowledge_graph = kg, data_graph = dg, metabolite_features = features, max_iterations = 10)
```

## Evaluation signals

- Annotation consistency check: when applied to the same test metabolite set multiple times or with different random seeds, the algorithm should produce identical or near-identical annotations (if stochastic, check convergence distribution).
- Dual-layer activation: verify that metabolites are successfully enriched through both knowledge-driven and data-driven pathways by tracing network traversal logs and confirming both layer contributions are present.
- Coverage and precision improvement: compare annotation counts and accuracy (F1, precision, recall against ground-truth) for the combined two-layer system against single-layer baselines (knowledge-driven only, data-driven only) — combined system should exceed both.
- Confidence score monotonicity: annotation confidence scores should increase or remain stable as propagation iterations proceed (no sudden reversals or oscillations).
- Propagation termination: verify that the recursive propagation algorithm reaches a stopping condition (convergence, max iterations, or no new annotations in final round) rather than running indefinitely.

## Limitations

- Requires high-quality, well-curated knowledge base; incomplete or incorrect ontologies will propagate errors across the entire network.
- Data-driven layer quality depends on experimental design and feature extraction fidelity — batch effects, instrumental noise, or poor feature alignment will corrupt similarity/co-occurrence signals.
- Computational cost scales with network size; typical untargeted metabolomics datasets process in ~1 hour, but very large cohorts or databases may require optimization.
- Citation status uncertain; the primary citation for MetDNA3 is listed as 'Coming Soon' in the README, limiting reproducibility claims and impact tracking.
- Full MetDNA3 functionality requires additional modules beyond MrnAnnoAlgo3; the algorithm alone is a core component, not a standalone end-to-end pipeline.

## Evidence

- [intro] two-layer interactive networking topology combining knowledge-driven and data-driven layers with recursive annotation propagation algorithms: "designed to annotate metabolites through a two-layer interactive networking topology (knowledge-driven and data-driven) and recursive annotation propagation algorithms"
- [readme] knowledge-driven layer uses established metabolite relationships and biochemical ontologies; data-driven layer uses feature similarity and co-occurrence patterns from MS data: "Integrates **knowledge-driven** (biochemical pathways, metabolic reaction networks) and **data-driven** (experimental MS2 similarity networks) layers for comprehensive and accurate metabolite"
- [readme] recursive propagation algorithm leverages both network layers to enhance annotation coverage and accuracy: "An efficient topology-based annotation propagation algorithm leveraging both network layers to enhance annotation coverage and accuracy."
- [readme] practical performance metric: processes typical untargeted metabolomics dataset in one hour, over 10-fold faster than previous versions: "Processes a typical untargeted metabolomics dataset in just one hour—over **10-fold faster** than previous versions."
- [other] validation workflow: test on metabolite set with known reference annotations to confirm combined architecture produces consistent outputs: "Validate that the combined architecture produces consistent annotation outputs when applied to a test metabolite set with known reference annotations."
