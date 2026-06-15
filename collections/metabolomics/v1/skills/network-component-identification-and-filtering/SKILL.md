---
name: network-component-identification-and-filtering
description: Use when you have a GNPS GraphML molecular network and need to isolate cohesive subsets of spectra (components) before analyzing which fragmentation patterns explain them.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - mineMS2
  - igraph
  - R
  - GNPS
derived_from:
- doi: 10.1186/s13321-025-01051-y
  title: minems2
evidence_spans:
- 'package: "`r BiocStyle::pkg_ver(''mineMS2'')`"'
- '%\VignetteDepends{igraph}'
- vignette title and package context indicate R-based package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_minems2
    doi: 10.1186/s13321-025-01051-y
    title: minems2
  dedup_kept_from: coll_minems2
schema_version: 0.2.0
---

# network-component-identification-and-filtering

## Summary

Extract and filter distinct network components (connected components, cliques, and high-similarity node pairs) from MS/MS molecular networks, applying cosine similarity and minimum size thresholds to isolate spectra groups suitable for pattern explanation analysis.

## When to use

Apply this skill when you have a GNPS GraphML molecular network and need to isolate cohesive subsets of spectra (components) before analyzing which fragmentation patterns best explain them. Use it when your research requires ranking patterns by their ability to explain specific network-defined groups of spectra with high recall and precision.

## When NOT to use

- Network has not yet been generated; construct molecular networks first using cosine similarity on raw MS/MS spectra.
- You are analyzing individual spectra without a network context; use this only on networked, similarity-linked spectrum collections.
- The precursor ion m/z values or spectral metadata are missing; component extraction requires node metadata for interpretation.

## Inputs

- GNPS molecular network as GraphML file
- igraph object representation of the network
- minimum component size threshold (integer)
- cosine similarity threshold (0–1 range, typically ≥0.9 for high-similarity pairs)

## Outputs

- list of connected components with member node IDs
- list of maximal cliques with member node IDs
- list of high-similarity node pairs meeting cosine threshold
- component membership table (node → component ID mapping)
- optionally, updated igraph object with component annotations

## How to apply

Load the molecular network as an igraph object using the igraph package. Extract three types of components: connected components of the full graph, maximal cliques with minimum size ≥3, and high-similarity pairs of nodes with cosine score threshold ≥0.9. For each component type, apply size filtering (minSize parameter) to retain only components of biological relevance. Filter edges by cosine similarity to ensure component membership reflects spectral relatedness. Export the filtered component assignments (node lists and their membership labels) for downstream pattern-explanation ranking.

## Related tools

- **igraph** (Parse GraphML network, extract connected components, cliques, and apply graph filters for component identification)
- **GNPS** (Generate the molecular network by cosine similarity clustering of MS/MS spectra; provides the input GraphML network structure)
- **mineMS2** (Accept extracted network components and rank fragmentation patterns by recall, precision, and size metrics to identify best-explaining patterns per component) — https://github.com/odisce/mineMS2

## Examples

```
findGNPSComponents(molnet.igraph, minSize=3, pairThreshold=0.9)
```

## Evaluation signals

- Component membership is non-overlapping within a component type (connected components are mutually exclusive; cliques may overlap but are correctly identified as maximal).
- All nodes in a component meet the cosine similarity threshold; verify by spot-checking edge scores in the original network.
- Component size distribution reflects biological structure: connected components typically larger, high-similarity pairs small (n=2) but highly specific.
- Component assignments are stable across repeated extractions (deterministic given fixed thresholds and network version).
- Downstream pattern-explanation F1-scores correlate with component homogeneity: well-separated components allow high-precision pattern explanations.

## Limitations

- Component extraction is sensitive to cosine similarity threshold (default 0.9 for pairs); lowering increases pair counts but may introduce noise.
- Minsize filtering discards small but biologically relevant components; balance between statistical power and preservation of rare metabolite clusters.
- Network topology is fixed at extraction time; dynamic updates (new spectra added) require re-extraction of all components.
- Clique-based components may miss hierarchical or fuzzy cluster structures present in the spectrum space but not captured by strict maximal cliques.

## Evidence

- [intro] We consider 3 type of components of the network: the connected components of the graph, the cliques, the high similarity pairs of nodes: "We consider 3 type of components of the network: the connected components of the graph, the cliques, the high similarity pairs of nodes"
- [intro] The molecular network is read using the igraph package: "The **molecular network** is read using the *igraph* package"
- [intro] findGNPSComponents with minSize threshold and cosine similarity filtering: "Extract network components using findGNPSComponents with minSize threshold and cosine similarity filtering"
- [intro] the high similarity pairs of nodes (pairs of spectra with a cosine score superior to a threshold): "the **high similarity pairs of nodes** (pairs of spectra with a cosine score superior to a threshold)"
- [intro] Select cliques with minimum size threshold: "findGNPSComponents(molnet.igraph, minSize = 3, pairThreshold = 0.9, ...)"
