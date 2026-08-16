---
name: network-node-label-spreading
description: Use when you have an untargeted metabolomics dataset with a two-layer network topology already constructed (one layer representing biochemical knowledge/pathways, the other representing data-driven MS2 similarity), seed metabolites with reliable annotations from database matching or curation, and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - MrnAnnoAlgo3 (MetDNA3)
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# network-node-label-spreading

## Summary

Recursive annotation propagation over a two-layer network topology (knowledge-driven and data-driven) that spreads metabolite labels from seed annotated nodes to neighboring unannotated nodes, enhancing coverage and confidence in untargeted metabolomics. This method integrates biochemical pathway knowledge with experimental MS2 similarity networks to systematically annotate metabolites across interconnected layers.

## When to use

Use this skill when you have an untargeted metabolomics dataset with a two-layer network topology already constructed (one layer representing biochemical knowledge/pathways, the other representing data-driven MS2 similarity), seed metabolites with reliable annotations from database matching or curation, and you need to maximize annotation coverage by leveraging network connectivity rules and layer-specific relationships to label previously unannotated nodes.

## When NOT to use

- Input network topology is single-layer or lacks both knowledge-driven and data-driven components—the algorithm requires dual-layer integration.
- Seed set is too sparse or lacks high-confidence ground truth; propagation from weak or incorrect seeds will introduce systematic errors.
- Layer-specific validation rules (spectral similarity thresholds, chemical class constraints, reaction network rules) are not defined or unavailable for your metabolomic platform.

## Inputs

- two-layer interactive network topology (knowledge-driven and data-driven layers)
- seed metabolite annotations (database matches or curated labels)
- spectral similarity scores (MS2 network data)
- biochemical pathway/reaction network data (knowledge layer)

## Outputs

- annotated network with propagated metabolite labels
- confidence scores for each propagated annotation
- layer-specific evidence for each label assignment

## How to apply

Load the two-layer network topology produced by prior topology reconstruction. Identify and seed the algorithm with metabolites that already have high-confidence annotations from database matching or manual curation. Execute the recursive annotation propagation algorithm that traverses both network layers simultaneously, propagating labels from annotated nodes to topologically adjacent unannotated nodes according to layer-specific connectivity rules (biochemical feasibility in the knowledge layer, spectral similarity thresholds in the data layer). At each propagation step, validate candidate annotations by checking consistency with layer-specific evidence: spectral similarity scores and chemical class rules in the data-driven layer, and known reaction networks and metabolic plausibility in the knowledge-driven layer. Output the annotated network with all propagated metabolite labels and associated confidence scores.

## Related tools

- **MrnAnnoAlgo3 (MetDNA3)** (core algorithm module implementing recursive annotation propagation over two-layer network topology for metabolite annotation) — https://github.com/ZhuMetLab/MrnAnnoAlgo3

## Examples

```
devtools::install_github("ZhuMetLab/MrnAnnoAlgo3"); # Load two-layer network, seed annotations, and call propagation: mrnAnnoAlgo3(network_topology, seed_annotations, layer_validation_rules)
```

## Evaluation signals

- Propagated annotations maintain consistency with spectral similarity scores and chemical class rules within each respective layer; no cross-layer constraint violations occur.
- Confidence scores are well-calibrated: annotations propagated from high-confidence seeds and validated through multiple layers receive higher scores than single-layer propagations.
- Coverage metrics: proportion of previously unannotated metabolites successfully labeled by the algorithm; no annotated nodes regress to unannotated state during recursion.
- Network traversal completeness: all reachable nodes (within topological connectivity and validation thresholds) receive labels; no valid propagation paths are left unexplored.
- Validation against orthogonal evidence: propagated labels are checked against independent reference standards (authentic compound MS2 spectra, literature metabolite lists) to confirm false positive rate is acceptable.

## Limitations

- Algorithm performance depends critically on seed annotation quality; sparse or incorrect seed sets propagate errors throughout the network.
- Requires well-curated two-layer topology; incomplete or noisy network construction (e.g., spurious MS2 edges or incomplete pathway databases) reduces annotation reliability.
- Layer-specific validation rules must be pre-defined and tuned; missing or poorly calibrated thresholds (spectral similarity cutoff, chemical class compatibility rules) lead to over- or under-propagation.
- Computational performance is optimized for typical datasets (processes in ~1 hour), but extremely large or densely connected networks may require parameter tuning.
- Does not resolve isomeric ambiguity within a single layer; relies on network topology and validation rules to disambiguate; some metabolites may remain ambiguous even after propagation.

## Evidence

- [intro] Two-layer network topology integrates knowledge-driven and data-driven components with recursive annotation propagation: "designed to annotate metabolites through a two-layer interactive networking topology (knowledge-driven and data-driven) and recursive annotation propagation algorithms"
- [other] Algorithm traverses layers according to layer-specific connectivity rules and validates via spectral and chemical consistency: "Execute recursive annotation propagation algorithm that traverses both network layers, propagating annotations from annotated nodes to neighboring unannotated nodes according to layer-specific"
- [readme] Knowledge-driven layer represents biochemical pathways; data-driven layer represents MS2 similarity networks: "Integrates **knowledge-driven** (biochemical pathways, metabolic reaction networks) and **data-driven** (experimental MS2 similarity networks) layers for comprehensive and accurate metabolite"
- [readme] Recursive propagation algorithm is efficient and topology-based: "An efficient topology-based annotation propagation algorithm leveraging both network layers to enhance annotation coverage and accuracy."
- [other] Algorithm requires seed metabolites with existing annotations: "Identify seed metabolites with existing annotations from database matching or prior curation."
