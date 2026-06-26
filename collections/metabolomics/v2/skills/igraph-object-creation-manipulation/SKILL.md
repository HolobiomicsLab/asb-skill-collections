---
name: igraph-object-creation-manipulation
description: Use when after computing pairwise correlations across features (10,000+
  in high-dimensional omics datasets) and applying correlation thresholding to retain
  only significant edges, you need to construct an igraph object that preserves edge
  weights, supports node annotation, and enables module.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3174
  - http://edamontology.org/topic_0092
  tools:
  - MetaNet
  - R
  - igraph
  - pcutils
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2025.06.26.661636v1
  title: MetaNet
evidence_spans:
- MetaNet, a high-performance R package that unifies network construction, visualization,
  and analysis across diverse omics layers.
- MetaNet, a high-performance R package that unifies network construction, visualization,
  and analysis across diverse omics layers
- MetaNet, a high-performance R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metanet_cq
    doi: 10.1101/2025.06.26.661636v1
    title: MetaNet
  dedup_kept_from: coll_metanet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.06.26.661636v1
  all_source_dois:
  - 10.1101/2025.06.26.661636v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# igraph-object-creation-manipulation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Convert thresholded correlation matrices into igraph network objects and perform flexible node/edge manipulation for downstream topological analysis and visualization. This skill bridges correlation computation and network characterization by constructing validated igraph objects with proper node and edge attributes.

## When to use

After computing pairwise correlations across features (10,000+ in high-dimensional omics datasets) and applying correlation thresholding to retain only significant edges, you need to construct an igraph object that preserves edge weights, supports node annotation, and enables module detection or topological metrics. Use this skill when preparing a correlation matrix for network visualization, multi-omics integration, or community detection.

## When NOT to use

- Input is already an igraph object — use igraph manipulation functions directly instead of reconstructing from correlation matrix.
- Correlation matrix has not been thresholded — apply statistical thresholding or significance filtering before calling c_net_build().
- Dataset contains <100 features — MetaNet's optimization assumes high-dimensional inputs (10,000+ features); standard igraph or igraph construction may suffice for smaller networks.

## Inputs

- correlation matrix (numeric matrix or data.frame with features as rows/columns)
- correlation threshold value (numeric; e.g., 0.6, 0.65)
- annotation tables (data.frame with vertex metadata: taxonomy, abundance, omics layer, etc.)

## Outputs

- igraph network object with named nodes (features), weighted edges (correlation coefficients), and vertex/edge attributes
- filtered sub-network igraph object (via c_net_filter)
- annotated multi-omics network with vertex class, size, and color attributes

## How to apply

Load a thresholded correlation matrix into R with features as both row and column names. Use MetaNet's c_net_build() function to construct an igraph object from the correlation matrix, specifying an r_threshold parameter (e.g., r ≥ 0.6 or 0.65) to filter weak edges. Attach metadata annotations using c_net_set() to assign vertex attributes (e.g., taxonomy, abundance, omics layer) and configure visualization properties (node size, color, shape). Validate the resulting igraph object by confirming node and edge counts, verifying correlation value ranges in edge weights, and checking igraph object integrity. Use c_net_filter() to extract sub-networks based on vertex or edge attributes when focusing on specific omics layers or correlation classes (intra- vs. inter-layer edges).

## Related tools

- **MetaNet** (Provides c_net_build(), c_net_set(), and c_net_filter() functions for constructing, annotating, and filtering igraph objects from correlation matrices.) — https://github.com/Asa12138/MetaNet
- **igraph** (Underlying R package upon which MetaNet's core functionality is built; used to represent and manipulate network objects.)
- **pcutils** (Companion R package providing utility functions for data transformation (e.g., t2() for matrix transposition) and example datasets used in MetaNet workflows.) — https://github.com/Asa12138/pcutils

## Examples

```
cor <- c_net_calculate(totu); net <- c_net_build(cor, r_threshold = 0.65); net <- c_net_set(net, annotation_df, vertex_class = 'Phylum'); net_filtered <- c_net_filter(net, v_group %in% c('Layer1', 'Layer2'))
```

## Evaluation signals

- Node count and edge count match expected values given the correlation threshold applied.
- All edge weights fall within the expected correlation range (e.g., [0.6, 1.0] or [-1, -0.6] ∪ [0.6, 1.0]).
- igraph object passes integrity check: is_igraph() returns TRUE and graph structure is acyclic/valid.
- Vertex attributes (class, size, group) are correctly assigned and match the input annotation tables for all nodes.
- Filtered sub-networks (via c_net_filter) contain only edges and nodes matching the specified criteria (e.g., e_class == 'intra').

## Limitations

- MetaNet's vectorized correlation algorithm is optimized for datasets with >10,000 features; performance gains diminish for smaller feature sets.
- Correlation thresholding is user-defined or statistical; no automatic threshold selection is provided by c_net_build()—threshold choice affects downstream results and must be justified.
- Multi-omics networks require aligned sample counts across all omics layers; mismatched sample sizes will trigger an error during multi_net_build().
- igraph object construction does not handle missing correlations (NA values) automatically; correlation matrix must be complete or sparsity handled prior to c_net_build().

## Evidence

- [other] Construct an igraph network object from the thresholded correlation matrix, with features as nodes and correlations as weighted edges.: "Construct an igraph network object from the thresholded correlation matrix, with features as nodes and correlations as weighted edges."
- [readme] The c_net_set function attaches multiple annotation tables to a network object and automatically configures visualization properties (Figure 2B), including color schemes, line types, node shapes, and legends.: "The c_net_set function attaches multiple annotation tables to a network object and automatically configures visualization properties (Figure 2B), including color schemes, line types, node shapes, and"
- [other] Validate network construction by checking node and edge counts, correlation value ranges, and igraph object integrity.: "Validate network construction by checking node and edge counts, correlation value ranges, and igraph object integrity."
- [readme] The c_net_filter function extracts sub-networks using flexible filters (Figure 2C), while c_net_highlight visually emphasizes selected nodes or edges (Figure 2D).: "The c_net_filter function extracts sub-networks using flexible filters (Figure 2C), while c_net_highlight visually emphasizes selected nodes or edges (Figure 2D)."
- [readme] its core functionality is built upon the widely used igraph package. Its architecture comprises several core functional modules: Calculation, Manipulation, Layout, Visualization, Topology analysis, Module analysis, Stability analysis, and I/O (Figure 1A): "its core functionality is built upon the widely used igraph package. Its architecture comprises several core functional modules: Calculation, Manipulation, Layout, Visualization, Topology analysis,"
