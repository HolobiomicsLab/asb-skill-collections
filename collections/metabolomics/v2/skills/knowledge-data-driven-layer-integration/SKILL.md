---
name: knowledge-data-driven-layer-integration
description: Use when you have untargeted metabolomics data (MS/MS spectra) and need to annotate metabolites at scale.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
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

# knowledge-data-driven-layer-integration

## Summary

Integrate knowledge-driven (biochemical pathways, metabolic reaction networks) and data-driven (experimental MS2 similarity networks) layers into a unified two-layer network topology to enable recursive annotation propagation for comprehensive metabolite annotation in untargeted metabolomics. This skill underpins accurate, high-coverage metabolite identification in large-scale studies.

## When to use

Apply this skill when you have untargeted metabolomics data (MS/MS spectra) and need to annotate metabolites at scale. Specifically use this skill when: (1) you have seed metabolites with known annotations from database matching or prior curation, (2) you need to propagate annotations to unannotated metabolites via network topology rather than direct spectral matching alone, and (3) you want to leverage both curated biochemical knowledge (pathways, reaction networks) and empirical MS2 similarity simultaneously to improve annotation coverage and confidence.

## When NOT to use

- Input metabolomics data contains only low-quality or unreliable MS2 spectra with poor spectral similarity scores—propagation will amplify errors across the network.
- Seed set is very small or biased toward a narrow chemical class—propagation may not generalize to novel structural classes.
- You have a curated, fully annotated metabolite reference library and do not need annotation propagation—direct spectral matching is more efficient.

## Inputs

- Two-layer network topology (knowledge-driven and data-driven layers)
- Seed metabolites with existing annotations (from database matching or curation)
- MS2 spectral similarity scores
- Biochemical pathway and metabolic reaction network data
- Chemical class or structural classification rules

## Outputs

- Annotated two-layer network with propagated metabolite labels
- Confidence scores for each propagated annotation
- Layer-specific validation flags (spectral similarity, chemical class consistency)

## How to apply

Construct a two-layer network by first loading or building a knowledge-driven layer from biochemical pathways and metabolic reaction databases and a data-driven layer from experimental MS2 spectral similarity networks. Identify seed metabolites with existing annotations from database hits or manual curation. Execute a recursive annotation propagation algorithm that traverses both network layers simultaneously, propagating labels from annotated nodes to neighboring unannotated nodes according to layer-specific connectivity rules (e.g., biochemical plausibility in the knowledge layer, spectral similarity thresholds in the data layer). Validate propagated annotations by checking consistency with spectral similarity scores and chemical class rules within each layer to filter low-confidence assignments. Output the annotated network with metabolite labels and associated confidence scores for each propagated annotation.

## Related tools

- **MrnAnnoAlgo3 (MetDNA3)** (Core algorithm module implementing recursive annotation propagation and two-layer network integration for metabolite annotation) — https://github.com/ZhuMetLab/MrnAnnoAlgo3

## Examples

```
devtools::install_github("ZhuMetLab/MrnAnnoAlgo3"); library(MrnAnnoAlgo3); # Load two-layer network, seed annotations, and spectral similarity data; result <- propagate_annotations(network_topology, seed_metabolites, similarity_threshold=0.7, validation_rules=chemical_class_rules)
```

## Evaluation signals

- Verify that the number of annotated metabolites increases after propagation compared to seed set alone, indicating successful label propagation.
- Check that propagated annotations maintain consistency with spectral similarity scores (e.g., high-confidence propagations occur at network edges with high cosine similarity or similar layer-specific metrics).
- Validate chemical class coherence: annotations propagated within the knowledge-driven layer should respect biochemical plausibility and known metabolic transformations.
- Compare confidence score distributions before and after validation filtering; low-confidence annotations should be filtered out and excluded from downstream analysis.
- Cross-check propagated annotations against independent reference databases or prior literature to assess accuracy and false discovery rate.

## Limitations

- Annotation propagation quality depends critically on seed set quality and size; a small or biased seed set may propagate incorrect labels across the network.
- Layer-specific connectivity rules must be well-calibrated; miscalibrated thresholds (e.g., spectral similarity cutoff, pathway distance) can lead to over- or under-propagation.
- The algorithm assumes that annotated neighbors are more likely to be annotated correctly, which may not hold in regions of the network with high ambiguity or noise.
- Recursive propagation can introduce cascading errors if early-stage misannotations are not caught and propagated to downstream nodes.
- Full MetDNA3 functionality requires additional modules beyond MrnAnnoAlgo3; the README notes that core functions are provided via the MetDNA3 webserver.

## Evidence

- [intro] Two-layer interactive networking topology (knowledge-driven and data-driven) with recursive annotation propagation enables accurate metabolite annotation: "designed to annotate metabolites through a two-layer interactive networking topology (knowledge-driven and data-driven) and recursive annotation propagation algorithms"
- [readme] Knowledge layer integrates biochemical pathways and metabolic reaction networks; data layer integrates experimental MS2 similarity networks: "Integrates **knowledge-driven** (biochemical pathways, metabolic reaction networks) and **data-driven** (experimental MS2 similarity networks) layers for comprehensive and accurate metabolite"
- [readme] Annotation propagation is topology-based, leveraging both network layers to enhance coverage and accuracy: "An efficient topology-based annotation propagation algorithm leveraging both network layers to enhance annotation coverage and accuracy."
- [other] Validation step checks consistency with spectral similarity scores and chemical class rules within each layer: "Validate propagated annotations by checking consistency with spectral similarity scores and chemical class rules within each layer."
- [readme] Performance improvement over prior versions enables processing of large-scale datasets efficiently: "Processes a typical untargeted metabolomics dataset in just one hour—over **10-fold faster** than previous versions."
