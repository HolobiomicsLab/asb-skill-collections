---
name: mass-spectrometry-feature-similarity-modeling
description: Use when when you have an untargeted metabolomics dataset with MS2 fragmentation spectra and need to annotate metabolites beyond what reference databases alone provide.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3346
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MrnAnnoAlgo3 (MetDNA3)
  techniques:
  - direct-infusion-MS
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

# mass-spectrometry-feature-similarity-modeling

## Summary

Build and leverage data-driven feature similarity networks from experimental mass spectrometry (MS2) data to enrich metabolite annotations by propagating identity confidence scores across co-occurring or spectrally similar metabolite nodes. This skill integrates MS2 similarity patterns as a complementary layer within a two-layer metabolite annotation topology.

## When to use

When you have an untargeted metabolomics dataset with MS2 fragmentation spectra and need to annotate metabolites beyond what reference databases alone provide. Use this skill when experimental co-occurrence patterns or spectral similarities between unknown and partially-annotated metabolites can guide confidence propagation, or when you wish to leverage data-driven relationships alongside knowledge-driven biochemical networks to improve coverage and accuracy.

## When NOT to use

- Input dataset lacks MS2 fragmentation spectra (MS1-only or direct infusion data without fragmentation).
- Metabolites are already fully annotated by targeted reference database matching; no propagation benefit exists.
- No seed reference annotations are available to initiate confidence propagation.

## Inputs

- Untargeted metabolomics dataset (mzML or NetCDF format)
- MS2 fragmentation spectra with m/z values and intensities
- Partial reference annotations or seed metabolite identities
- Feature abundance or co-occurrence matrix

## Outputs

- Data-driven MS2 similarity network (graph with edge weights)
- Metabolite annotations enriched by propagation confidence scores
- Annotation coverage metrics comparing reference-only vs. propagated assignments

## How to apply

Construct a data-driven layer by computing feature similarity from MS2 spectra (e.g., using cosine similarity or mass difference patterns from your experimental dataset). Embed this similarity network as a graph where metabolite nodes are connected by co-occurrence or spectral relatedness edges, each weighted by a confidence or similarity score. Implement recursive annotation propagation that iteratively refines metabolite identities by traversing both the data-driven similarity graph and a knowledge-driven biochemical pathway graph simultaneously. At each iteration, propagate annotation confidence from seed nodes (e.g., reference-matched metabolites) to neighboring nodes, using both network layers to accumulate evidence. Validate propagation by confirming that annotation outputs remain consistent and that confidence scores converge when applied to a test set with known reference annotations.

## Related tools

- **MrnAnnoAlgo3 (MetDNA3)** (Core algorithm module that implements the two-layer interactive networking topology combining knowledge-driven and data-driven (MS2 similarity) layers with recursive annotation propagation) — https://github.com/ZhuMetLab/MrnAnnoAlgo3

## Examples

```
devtools::install_github("ZhuMetLab/MrnAnnoAlgo3"); library(MrnAnnoAlgo3); # Build data-driven MS2 similarity network and invoke recursive propagation on untargeted metabolomics dataset with partial reference annotations
```

## Evaluation signals

- Data-driven similarity network exhibits non-zero edge weights between metabolites with high MS2 spectral similarity (cosine > threshold) or significant co-occurrence patterns.
- Annotation propagation converges (confidence scores stabilize) across iterations on a test metabolite set.
- Metabolites matched to reference annotations maintain consistent identities after recursive propagation (no conflicting reassignments).
- Annotation coverage increases when propagation is enabled compared to reference-only matching alone.
- Confidence scores for propagated annotations correlate with independent validation (e.g., retention time or standard compound verification).

## Limitations

- Propagation accuracy depends on quality and completeness of seed annotations; sparse or incorrect reference assignments can propagate false identities.
- MS2 spectral similarity alone may conflate isomeric or structurally similar metabolites that are not biochemically related.
- Performance scales with dataset size; large-scale metabolomics (>10,000 features) requires efficient graph representation to stay within computational budget.
- Feature co-occurrence patterns may reflect batch effects, sample contamination, or technical artifacts rather than true metabolic relationships.

## Evidence

- [readme] Data-driven layer definition and role: "Integrates **knowledge-driven** (biochemical pathways, metabolic reaction networks) and **data-driven** (experimental MS2 similarity networks) layers for comprehensive and accurate metabolite"
- [readme] Recursive annotation propagation mechanism: "An efficient topology-based annotation propagation algorithm leveraging both network layers to enhance annotation coverage and accuracy."
- [intro] Two-layer topology for metabolite annotation: "designed to annotate metabolites through a two-layer interactive networking topology (knowledge-driven and data-driven) and recursive annotation propagation algorithms"
- [other] Validation approach for propagation: "Validate that the combined architecture produces consistent annotation outputs when applied to a test metabolite set with known reference annotations."
