---
name: two-layer-topology-traversal
description: Use when you have an untargeted metabolomics dataset with partial metabolite annotations (from database matching or prior curation) and need to extend annotation coverage to unannotated metabolites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  tools:
  - MrnAnnoAlgo3 (MetDNA3)
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

# two-layer-topology-traversal

## Summary

Reconstruct and traverse a two-layer interactive network topology (knowledge-driven biochemical pathways + data-driven MS2 similarity networks) to propagate metabolite annotations recursively across both layers. This skill enables accurate annotation coverage in untargeted metabolomics by leveraging both prior biological knowledge and experimental spectral similarity evidence.

## When to use

You have an untargeted metabolomics dataset with partial metabolite annotations (from database matching or prior curation) and need to extend annotation coverage to unannotated metabolites. The task is to propagate known annotations across a network of metabolites where connectivity is determined both by known biochemical relationships and by experimental MS2 spectral similarity. Use this skill when annotation gaps persist after database matching and you require layer-specific propagation rules (e.g., different connectivity thresholds or confidence criteria for knowledge-driven vs. data-driven edges).

## When NOT to use

- Input metabolites have no existing annotations or very few seed metabolites; recursive propagation requires sufficient starting annotations to be effective.
- Spectral data is unavailable or MS2 similarity scores cannot be computed; the data-driven layer depends on experimental spectral evidence.
- The biological system or sample type has poorly characterized biochemical pathways; the knowledge-driven layer depends on curated pathway databases.

## Inputs

- two-layer network topology (knowledge-driven and data-driven layers)
- seed metabolites with existing annotations
- MS2 spectral similarity scores or distance matrix
- layer-specific connectivity thresholds or rules

## Outputs

- annotated metabolite network with propagated labels
- metabolite annotations with confidence scores per layer
- validation report (spectral similarity consistency, chemical class rule conformance)

## How to apply

First, load or reconstruct the two-layer network topology, with the knowledge-driven layer encoding biochemical pathways and metabolic reaction networks, and the data-driven layer representing MS2 spectral similarity networks. Identify seed metabolites with existing annotations from database matching or curation. Execute the recursive annotation propagation algorithm (MrnAnnoAlgo3) that traverses both network layers simultaneously, propagating annotations from annotated nodes to neighboring unannotated nodes according to layer-specific connectivity rules and edge weights. Validate propagated annotations by checking consistency with spectral similarity scores and chemical class rules within each layer, using these criteria to assign confidence scores. Output the annotated network with all metabolite labels and propagated confidence scores, filtering or flagging low-confidence assignments for manual review.

## Related tools

- **MrnAnnoAlgo3 (MetDNA3)** (Core algorithm module that executes recursive annotation propagation over the two-layer network topology to annotate unannotated metabolites) — https://github.com/ZhuMetLab/MrnAnnoAlgo3

## Examples

```
devtools::install_github('ZhuMetLab/MrnAnnoAlgo3'); library(MrnAnnoAlgo3); result <- propagate_annotations(network_topology=two_layer_net, seed_annotations=annotated_mets, similarity_matrix=ms2_scores, validate=TRUE)
```

## Evaluation signals

- Annotated metabolites show increased coverage compared to seed annotations; propagated annotations should extend to previously unannotated nodes.
- Propagated annotations maintain consistency with layer-specific rules (e.g., spectral similarity scores stay above defined thresholds, chemical class assignments remain valid within the knowledge-driven layer).
- Confidence scores are differentially assigned; high-confidence annotations should have high spectral similarity and agreement across both layers, while low-confidence assignments flag potential ambiguities.
- No annotation contradictions occur within chemical class constraints or reaction network topology; a metabolite should not receive conflicting structural or functional labels.
- Algorithm runtime meets performance target (typical dataset processed in ~1 hour); execution should be 10-fold faster than previous annotation methods.

## Limitations

- Propagation quality depends on the completeness and accuracy of the underlying knowledge-driven and data-driven layers; poor pathway curation or low-quality spectral data will degrade results.
- Recursive propagation may amplify errors if erroneous seed annotations are propagated to multiple downstream nodes; seed annotation validation is critical.
- The method assumes that connectivity (biochemical and spectral) is a reliable proxy for shared chemical identity; metabolites connected by weak or spurious edges may receive incorrect annotations.
- Full MetDNA3 functionality requires additional modules beyond MrnAnnoAlgo3; the standalone algorithm module may not provide end-to-end data preprocessing or post-processing.

## Evidence

- [readme] Core algorithm concept and layer integration: "MrnAnnoAlgo3 is the core algorithm module of MetDNA3, designed to annotate metabolites through a two-layer interactive networking topology (knowledge-driven and data-driven) and recursive annotation"
- [readme] Knowledge-driven and data-driven layer definitions: "Integrates knowledge-driven (biochemical pathways, metabolic reaction networks) and data-driven (experimental MS2 similarity networks) layers for comprehensive and accurate metabolite annotation."
- [other] Workflow steps for traversal and propagation: "Execute recursive annotation propagation algorithm that traverses both network layers, propagating annotations from annotated nodes to neighboring unannotated nodes according to layer-specific"
- [other] Validation and confidence scoring: "Validate propagated annotations by checking consistency with spectral similarity scores and chemical class rules within each layer."
- [readme] Performance improvement: "Processes a typical untargeted metabolomics dataset in just one hour—over 10-fold faster than previous versions."
