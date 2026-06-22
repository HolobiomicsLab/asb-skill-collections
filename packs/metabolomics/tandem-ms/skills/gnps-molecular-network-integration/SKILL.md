---
name: gnps-molecular-network-integration
description: Use when you have computed frequent fragmentation patterns from a collection of MS/MS spectra using mineMS2, and you want to focus pattern interpretation on subsets of spectra that form meaningful network components (connected groups, cliques, or high-similarity pairs) in a GNPS molecular network.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - mineMS2
  - igraph
  - R
  - GNPS
  - Cytoscape
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1186/s13321-025-01051-y
  title: minems2
evidence_spans:
- 'package: "`r BiocStyle::pkg_ver(''mineMS2'')`"'
- '%\VignetteDepends{igraph}'
- vignette title and package context indicate R-based package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_minems2
    doi: 10.1186/s13321-025-01051-y
    title: minems2
  dedup_kept_from: coll_minems2
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-025-01051-y
  all_source_dois:
  - 10.1186/s13321-025-01051-y
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# gnps-molecular-network-integration

## Summary

Integrate fragmentation pattern mining results with GNPS MS/MS molecular networks to identify patterns that optimally explain connected components, cliques, and high-similarity spectrum pairs. This coupling enables discovery of chemical similarities independent of network cosine-score thresholds and facilitates targeted annotation of network neighborhoods.

## When to use

You have computed frequent fragmentation patterns from a collection of MS/MS spectra using mineMS2, and you want to focus pattern interpretation on subsets of spectra that form meaningful network components (connected groups, cliques, or high-similarity pairs) in a GNPS molecular network. Use this skill when you need to filter patterns by their explanatory power for specific network regions rather than analyzing all patterns globally.

## When NOT to use

- The input spectra collection is very small (< 10 spectra) or lacks sufficient spectral diversity; the frequent pattern mining step will yield too few or overly generic patterns to meaningfully stratify network components.
- The GNPS network is fully disconnected or contains only isolated nodes; there are no meaningful components to explain.
- You need to prioritize global pattern statistics (e.g., which patterns are most frequent across the entire library) rather than component-specific explanations; this skill is network-focused and may suppress globally-abundant patterns that weakly explain individual components.

## Inputs

- ms2Lib object (discretized MS/MS spectra collection with computed m/z differences)
- igraph object (molecular network loaded from GNPS GraphML file)
- mineMS2 pattern collection (frequent subgraph mining results with pattern IDs and node/edge lists)

## Outputs

- component-pattern mapping table (component IDs, pattern ranks, F1-scores, recall, precision, pattern size)
- annotated network GraphML file (original network with pattern assignments as node/edge attributes)
- pattern metrics per component (ranked list of patterns with evaluation metrics for each network component)

## How to apply

Load the GNPS molecular network as an igraph object from a GraphML file using igraph. Extract network components using findGNPSComponents with minSize threshold (e.g., minSize=3 for cliques) and pairThreshold (e.g., 0.9 cosine score) to define high-similarity pairs. Execute findPatternsExplainingComponents with metric=c('recall','precision','size') and top=5 (or higher) to rank patterns by their ability to explain each component without over-generalizing. Compute F1-scores for each pattern per component; patterns with F1=1.0 indicate perfect explanation (all component spectra contain the pattern, no external spectra contain it). Export results as a structured table mapping component identifiers to their top-ranking patterns and metrics. Annotate the network GraphML with pattern identifiers and re-visualize in Cytoscape to highlight pattern-supported neighborhoods.

## Related tools

- **mineMS2** (Mining and representation of frequent fragmentation patterns as graphs; integration point with GNPS networks via findPatternsExplainingComponents function) — https://github.com/odisce/mineMS2
- **igraph** (Loading, parsing, and extracting connected components and cliques from molecular network GraphML files)
- **GNPS** (Public MS/MS spectral library and molecular networking platform; source of network topology and cosine-similarity edge weights)
- **Cytoscape** (Visualization of annotated molecular networks with pattern assignments overlaid as node/edge attributes)

## Evaluation signals

- Verify that all extracted network components (connected subgraphs, cliques, high-similarity pairs) have at least one pattern assigned with F1-score ≥ 0.5 (indicating partial to perfect explanation).
- Check that the top-1 pattern for each component has F1-score ≥ 0.5 and that recall and precision sum to expected behavior (recall + precision should not degrade monotonically across top-5 rankings for well-separated components).
- Confirm that patterns with F1=1.0 have all component members in their support set and zero false positives (no spectra outside the component contain all pattern edges).
- Validate that the component-pattern annotation is non-redundant: no two distinct patterns receive identical (recall, precision, size) tuples for the same component (ties may be resolved by size or pattern ID).
- Cross-check that high-similarity pairs (cosine > pairThreshold) receive different pattern explanations than their parent connected component, confirming that network-component stratification adds interpretive value.

## Limitations

- Pattern quality depends critically on m/z discretization parameters (dmz, ppm tolerance); too-coarse tolerances cause false-positive m/z merging; too-fine tolerances fragment true neutral losses. Defaults (dmz=0.007, ppm=15) are optimized for Penicillium-DB but may require tuning for other organism or ionization modes.
- findGNPSComponents requires manual choice of minSize and pairThreshold; small minSize (e.g., 1–2) will yield trivial components; large pairThreshold (e.g., >0.95) may exclude biologically related spectra. No automatic threshold selection is provided; parameter exploration is recommended.
- F1-score of 1.0 is achievable only when a pattern's support set exactly matches a network component; in practice, patterns often explain >1 component or partial overlaps, reducing interpretability for large, diffuse network regions.
- The coupling workflow does not account for spectral library database matching; patterns may represent artifacts or instrument-specific fragmentation rather than true chemical structure features.
- Performance (runtime and memory) scales with network size and pattern count; very large networks (>1000 spectra) or pattern repositories (>10,000 patterns) may require optimization or sampling.

## Evidence

- [intro] The molecular network is read using the igraph package: "The **molecular network** is read using the *igraph* package"
- [intro] Extract connected components, cliques, and high similarity pairs: "We consider 3 type of components of the network: the **connected components** of the graph, the **cliques**, the **high similarity pairs of nodes**"
- [intro] Find patterns that best explain extracted network components: "*mineMS2* then enables to select the pattern that best explain each of the extracted components according to 3 metrics"
- [intro] mineMS2 coupled to GNPS focuses on patterns explaining network components: "This vignette describes how *mineMS2* can be **coupled to the GNPS MS/MS molecular networking** methodology to **focus on patterns that best explain components** of the network"
- [intro] Annotate network with patterns and export as GraphML: "The information about each best explaining pattern can be added to the network object and exported as a *GraphML* file"
- [other] Pattern P70 achieves F1-score 1.0 while other top-5 patterns maintain recall=1 but lower precision: "Pattern P70 achieves an F1-score of 1 for component 8 (precursor m/z 370.1283 and 404.0891), while other top-5 patterns maintain recall of 1 but have lower precision"
- [intro] mineMS2 discovers similarities independent of network thresholds: "*mineMS2* therefore highlights 4 other metabolites which share the same pattern, and *mineMS2* thus enables to discover new similarities, common to multiple spectra and independent from molecular"
- [intro] High-similarity pairs defined by cosine score threshold: "the **high similarity pairs of nodes** (pairs of spectra with a cosine score superior to a threshold)"
- [intro] Discretization of m/z differences with dmz and ppm tolerances: "discretizeMzDifferences(pnordicum.m2l, dmz = 0.007, ppm = 15, maxFrags = 15)"
- [intro] findGNPSComponents with minSize and pairThreshold parameters: "findGNPSComponents(molnet.igraph, minSize = 3, pairThreshold = 0.9, ...)"
