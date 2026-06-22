---
name: metabolite-annotation-network-architecture
description: Use when when annotating large-scale untargeted metabolomics datasets where reference library coverage is incomplete and you need to infer metabolite identities for unannotated compounds by propagating annotations from seed metabolites (database matches or prior curation) across both.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MrnAnnoAlgo3 (MetDNA3)
  - MrnAnnoAlgo3
  - MetDNA3
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

# metabolite-annotation-network-architecture

## Summary

Design and implement a fixed two-layer interactive networking topology that bridges knowledge-driven (biochemical ontologies, metabolic reaction networks) and data-driven (MS2 spectral similarity, co-occurrence patterns) layers to enable recursive annotation propagation across metabolite networks. This architecture supports accurate large-scale metabolite annotation in untargeted metabolomics by leveraging both curated biochemical relationships and experimental mass spectrometry evidence simultaneously.

## When to use

When annotating large-scale untargeted metabolomics datasets where reference library coverage is incomplete and you need to infer metabolite identities for unannotated compounds by propagating annotations from seed metabolites (database matches or prior curation) across both knowledge-driven pathway relationships and data-driven spectral similarity networks.

## When NOT to use

- Input is a targeted metabolomics assay with complete reference library coverage — a simpler database matching approach is sufficient and more efficient.
- Metabolite compounds in the dataset have no known biochemical relationships or are not chemically related — knowledge-driven layer would be empty or uninformative.
- Raw mass spectrometry data has not been preprocessed to a feature-level matrix (e.g., still in vendor instrument format or unaligned mzML) — preprocessing and alignment must precede layer construction.

## Inputs

- Knowledge-driven layer definition (metabolic reaction network, biochemical ontology as edge list or adjacency matrix)
- Experimental mass spectrometry data (MS/MS spectra, feature abundance matrix, retention times)
- Database metabolite reference annotations (for seed nodes)
- Feature similarity/co-occurrence matrix (computed from MS2 spectra or other data-driven metrics)

## Outputs

- Two-layer interactive network topology (graph structure with nodes and weighted edges from both layers)
- Annotated metabolite network (all nodes labeled with metabolite identities and confidence scores)
- Annotation propagation report (iteration count, convergence status, per-metabolite annotation sources and confidence traces)

## How to apply

First, construct the knowledge-driven layer by encoding established metabolite relationships and biochemical ontologies as static directed graph structures (e.g., KEGG reactions, biochemical transformations). Simultaneously, build the data-driven layer from experimental mass spectrometry data by computing pairwise feature similarity (e.g., cosine similarity of MS2 spectra, retention time proximity) and co-occurrence patterns across all detected metabolite features. Implement the interactive networking topology that allows metabolite nodes to be queried and enriched through both layers in parallel, with cross-layer edge weights reflecting layer-specific confidence metrics. Initialize the recursive annotation propagation algorithm with seed metabolites bearing annotations from database matching or curated reference standards. Execute iterative propagation passes that traverse both network layers according to layer-specific connectivity rules, enriching each node's annotation candidates by aggregating confidence scores and relationships from connected nodes in both layers. At each iteration, validate propagated annotations by checking consistency with spectral similarity thresholds and chemical class rules specific to each layer. Continue until convergence (no new annotations or confidence scores stabilize) or reach a predefined iteration limit. Output the fully annotated network with propagated metabolite labels, confidence scores, and the supporting layer(s) for each annotation.

## Related tools

- **MrnAnnoAlgo3** (Core algorithm module implementing the two-layer interactive networking topology and recursive annotation propagation for metabolite annotation) — https://github.com/ZhuMetLab/MrnAnnoAlgo3
- **MetDNA3** (Ecosystem framework providing webserver deployment and full annotation pipeline for which MrnAnnoAlgo3 is the central algorithmic component) — http://metdna.zhulab.cn

## Evaluation signals

- Consistency check: Propagated annotations for the same metabolite node across multiple network traversals should have stable confidence scores (delta < 1% between iterations).
- Layer coherence: Each annotation must have supporting evidence (edge weights or confidence metrics) from at least one of the two layers; orphaned or unsupported annotations indicate propagation errors.
- Coverage gain: Compare number of annotated nodes before and after propagation; typical gains should be >50% (relative to seed annotations) for well-connected datasets.
- Reference validation: When ground-truth annotations are available for a test metabolite set, compare propagated identities against reference identities; precision and recall should both exceed 80% for high-confidence (>0.7 score) predictions.
- Convergence: Algorithm must terminate within predefined iteration limit with no divergence (confidence scores growing unbounded) or oscillation (identical annotations cycling between iterations).

## Limitations

- Architecture assumes metabolite relationships encoded in the knowledge-driven layer are accurate and sufficiently complete; sparse or biased pathway databases will reduce annotation propagation coverage.
- Data-driven layer quality depends on experimental MS2 spectral resolution and reproducibility; noisy or poor-quality spectra lead to false co-occurrence edges and erroneous annotation spread.
- Seed metabolite set must be adequately diverse and representative; homogeneous seeds (e.g., all from one metabolic pathway) will bias propagation toward that pathway at the expense of other regions of chemical space.
- Recursive propagation algorithm exhibits O(n × k × m) time complexity where n is number of metabolites, k is average node degree, and m is iteration count; very large networks (>100k compounds) may exceed practical runtime or memory constraints.

## Evidence

- [intro] Two-layer interactive networking topology (knowledge-driven and data-driven) with recursive annotation propagation enables accurate metabolite annotation: "designed to annotate metabolites through a two-layer interactive networking topology (knowledge-driven and data-driven) and recursive annotation propagation algorithms"
- [other] Knowledge-driven layer incorporates established metabolite relationships and biochemical ontologies as static graph structures: "Define the knowledge-driven layer components, incorporating established metabolite relationships and biochemical ontologies as static graph structures"
- [other] Data-driven layer derives from feature similarity and co-occurrence patterns in experimental MS data: "Define the data-driven layer components, incorporating feature similarity and co-occurrence patterns derived from experimental mass spectrometry data"
- [other] Recursive annotation propagation algorithm iteratively refines metabolite identities using confidence scores and relationships from both layers: "Implement the recursive annotation propagation algorithm that iteratively refines metabolite identities by leveraging confidence scores and relationships from both layers"
- [other] Algorithm traverses both network layers according to layer-specific connectivity rules to propagate annotations from seed metabolites: "Execute recursive annotation propagation algorithm that traverses both network layers, propagating annotations from annotated nodes to neighboring unannotated nodes according to layer-specific"
- [other] Validation requires checking consistency with spectral similarity scores and chemical class rules within each layer: "Validate propagated annotations by checking consistency with spectral similarity scores and chemical class rules within each layer"
- [readme] MrnAnnoAlgo3 provides robust computational foundation for large-scale metabolomic studies: "It provides a robust computational foundation for large-scale metabolomic studies"
- [readme] Two-layer networking integrates knowledge-driven and data-driven layers for comprehensive metabolite annotation: "Integrates **knowledge-driven** (biochemical pathways, metabolic reaction networks) and **data-driven** (experimental MS2 similarity networks) layers for comprehensive and accurate metabolite"
