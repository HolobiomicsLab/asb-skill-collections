---
name: annotation-confidence-scoring
description: Use when after recursive annotation propagation has assigned metabolite
  labels to previously unannotated nodes in a two-layer metabolomic network, and before
  reporting final annotated metabolite identities.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MrnAnnoAlgo3 (MetDNA3)
  techniques:
  - LC-MS
  - NMR
  license_tier: noncommercial
  tool_license:
    tier: noncommercial
    requires_ack: true
    ref: CC-BY-NC-ND-4.0
    url: ZhuMetLab/MrnAnnoAlgo3
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

# annotation-confidence-scoring

> **License: noncommercial** — confirm your use is a permitted (noncommercial) purpose before applying; commercial use requires a separate license (see `metadata.tool_license`). <!-- asb-license-banner -->
## Summary

Validate and score confidence in propagated metabolite annotations by checking consistency with spectral similarity scores and chemical class rules within each network layer. This ensures that recursive annotation propagation produces reliable, layer-specific metabolite labels suitable for downstream metabolomic analysis.

## When to use

After recursive annotation propagation has assigned metabolite labels to previously unannotated nodes in a two-layer metabolomic network, and before reporting final annotated metabolite identities. Use this skill when you need to distinguish high-confidence annotations from speculative ones, or when harmonizing annotations across knowledge-driven and data-driven layers with different reliability characteristics.

## When NOT to use

- Input metabolites are already individually validated against reference standards via orthogonal methods (e.g., NMR, retention time matching)—direct validation supersedes propagation-based confidence scoring.
- Analyzing targeted metabolomics where all analytes are monitored with defined MRM transitions—confidence scoring is designed for untargeted discovery where annotation propagation is necessary.
- Network contains only a single layer or lacks chemical class rules for at least one layer—the dual-layer consistency check cannot be performed.

## Inputs

- two-layer network topology with knowledge-driven and data-driven layers
- seed metabolites with existing annotations from database matching
- metabolite nodes with propagated labels
- spectral similarity score matrix (experimental MS2 vs. reference spectra)
- chemical class rule set for each layer

## Outputs

- annotated network with all propagated metabolite labels
- confidence scores for each annotation
- layer-specific validation status (pass/fail per layer)

## How to apply

Following annotation propagation across both network layers, systematically validate each propagated annotation by cross-checking: (1) spectral similarity scores between the annotated metabolite's MS2 spectrum and reference spectra (checking that similarity meets layer-specific thresholds); (2) chemical class consistency rules specific to each layer (knowledge-driven rules based on biochemical pathways, data-driven rules based on experimental MS2 networks); (3) coherence of the annotation with the connectivity pattern that propagated it. Assign confidence scores reflecting both the quality of evidence and the pathway through which annotation was propagated. This validation step ensures that only annotations consistent with both spectral and chemical logic are retained for output.

## Related tools

- **MrnAnnoAlgo3 (MetDNA3)** (Core algorithm module performing recursive annotation propagation and executing the validation step that scores annotation confidence by checking consistency with spectral similarity scores and chemical class rules) — https://github.com/ZhuMetLab/MrnAnnoAlgo3

## Evaluation signals

- All output annotations have non-null confidence scores and layer-specific validation status recorded.
- Annotations with high confidence scores show spectral similarity to reference spectra above the layer-specific threshold and satisfy chemical class rules for their respective layers.
- Confidence scores correlate inversely with topological distance from seed nodes—closer propagation paths and stronger spectral support yield higher scores.
- Manual spot-check of 5–10 high-confidence and 5–10 low-confidence annotations confirms that scoring reflects biological plausibility and spectral alignment quality.
- Output annotation counts and confidence distributions are stable across repeated validation runs on the same network (reproducibility check).

## Limitations

- Confidence scoring depends critically on the completeness and accuracy of the reference spectral database—missing reference spectra will cause valid metabolites to score lower or fail validation.
- Chemical class rules are layer-specific and may conflict across layers; when inconsistency occurs, confidence scores may not fully resolve which layer's logic is more appropriate for the specific metabolite.
- Propagation distance and network topology can inflate confidence in annotations derived from weak or transitive evidence; scoring cannot distinguish between direct and multi-hop propagation paths without explicit topological weighting.
- The README notes that the full MetDNA3 implementation is available on the webserver; the GitHub module MrnAnnoAlgo3 alone may lack some validation components.

## Evidence

- [other] Validate propagated annotations by checking consistency with spectral similarity scores and chemical class rules within each layer.: "Validate propagated annotations by checking consistency with spectral similarity scores and chemical class rules within each layer."
- [readme] Integrates knowledge-driven (biochemical pathways, metabolic reaction networks) and data-driven (experimental MS2 similarity networks) layers for comprehensive and accurate metabolite annotation.: "Integrates **knowledge-driven** (biochemical pathways, metabolic reaction networks) and **data-driven** (experimental MS2 similarity networks) layers for comprehensive and accurate metabolite"
- [other] Output the annotated network with all propagated metabolite labels and confidence scores.: "Output the annotated network with all propagated metabolite labels and confidence scores."
- [readme] An efficient topology-based annotation propagation algorithm leveraging both network layers to enhance annotation coverage and accuracy.: "An efficient topology-based annotation propagation algorithm leveraging both network layers to enhance annotation coverage and accuracy."
