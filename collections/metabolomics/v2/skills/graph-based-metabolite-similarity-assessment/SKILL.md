---
name: graph-based-metabolite-similarity-assessment
description: Use when you have a collection of MS/MS spectra (stored as Spectrum2
  objects in an ms2Lib class) and need to identify which spectra share identical fragmentation
  patterns—particularly when coupled to a GNPS molecular network to focus on explaining
  network components (connected components, cliques.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0081
  tools:
  - mineMS2
  - igraph
  - R
  - MSnbase
  - GNPS
  - Cytoscape
  techniques:
  - LC-MS
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# graph-based-metabolite-similarity-assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and compare fragmentation patterns represented as m/z-difference graphs across MS/MS spectra to identify metabolite similarities independent of external databases or molecular formulas. This skill enables discovery of common structural features shared by subsets of spectra, facilitating untargeted metabolite annotation and network component interpretation.

## When to use

Apply this skill when you have a collection of MS/MS spectra (stored as Spectrum2 objects in an ms2Lib class) and need to identify which spectra share identical fragmentation patterns—particularly when coupled to a GNPS molecular network to focus on explaining network components (connected components, cliques, or high-similarity pairs with cosine > threshold). Use this skill when external spectral databases or precursor molecular formulas are unavailable or when you want to discover pattern-based similarities independent of network similarity thresholds.

## When NOT to use

- When only a single spectrum or <2 spectra are available (patterns require count≥2 for frequency definition)
- When precursor molecular formulas and external spectral databases are already integrated and sufficient for your annotation goal (this skill discovers complementary, database-independent patterns)
- When network components are already well-annotated or when you only need to rank spectra by global cosine similarity without interpreting shared fragmentation logic

## Inputs

- ms2Lib object containing discretized m/z differences and fragmentation graphs (from Spectrum2 objects, dmz and ppm parameters applied)
- GNPS molecular network in GraphML or igraph format with cosine similarity edge weights
- Extracted network components (as subgraphs of connected nodes, cliques, or high-similarity pairs)

## Outputs

- Ranked set of fragmentation patterns (closed subgraphs) per network component, with recall, precision, and F1-score metrics
- Pattern-to-component assignments identifying which patterns best explain each component
- Annotated molecular network (GraphML) with best-explaining patterns added as node/edge attributes
- Structured result table with pattern IDs, component IDs, F1-scores, and candidate molecular formulas for m/z differences (≤200 Da)

## How to apply

Begin by discretizing m/z differences within each spectrum using specified dmz and ppm tolerances (e.g., dmz=0.007, ppm=15) to align differences across the collection. Construct fragmentation graphs for each spectrum by representing ion peaks as nodes and m/z differences as edges. Extract frequent closed subgraphs (patterns) appearing in at least count≥2 spectra using a frequent-subgraph mining algorithm, optionally filtering by minimum pattern size (sizeMin≥1). Load the GNPS molecular network as an igraph object and extract components (connected components, cliques with minSize≥3, or high-similarity node pairs with cosine score > pairThreshold, e.g., >0.9). For each component, rank extracted patterns using recall-precision-size metrics and select the top-K patterns (e.g., top=5) that best explain each component. A pattern achieves perfect F1-score when it recalls all spectra in a component (recall=1.0) without explaining spectra outside the component (precision=1.0). Validate results by verifying F1-scores and confirming patterns are chemically interpretable as exact graphs.

## Related tools

- **mineMS2** (Core package for discretizing m/z differences, constructing fragmentation graphs, extracting frequent closed subgraphs (patterns), and ranking patterns by recall-precision-size metrics) — https://github.com/odisce/mineMS2
- **igraph** (Loading, parsing, and manipulating GNPS molecular networks; extracting connected components, cliques, and node pairs; representing patterns and fragmentation graphs as formal graph objects)
- **MSnbase** (Providing Spectrum2 class objects for storing and organizing MS/MS spectral data and metadata)
- **GNPS** (Source of molecular networks (GraphML format) that define spectrum similarity relationships and network structure for component extraction and pattern interpretation)
- **Cytoscape** (Visualization of annotated molecular networks with best-explaining patterns overlaid)

## Examples

```
findPatternsExplainingComponents(pnordicum.m2l, gnps.network.igraph, metric=c('recall','precision','size'), top=5, minSize=3, pairThreshold=0.9)
```

## Evaluation signals

- Verify that all patterns extracted have count≥2 (appear in at least two spectra) and that all m/z differences in each pattern are exact matches across all member spectra (no probabilistic edges)
- Confirm that F1-scores are correctly computed as 2×(recall×precision)/(recall+precision) for each pattern-component pair, with perfect F1=1.0 only when recall=1.0 AND precision=1.0
- Check that patterns explaining network components show recall=1.0 (pattern explains all spectra in the component) with varying precision values reflecting whether the pattern also explains spectra outside the component
- Validate that extracted component types match the requested filters (connected components, cliques with minSize≥3, or pairs with cosine similarity > pairThreshold)
- Confirm that m/z differences in top-ranked patterns have candidate molecular formulas computed (displayed for candidates ≤200 Da) and that chemical interpretations are plausible (e.g., neutral losses, inter-pathway m/z gaps)

## Limitations

- Pattern quality depends on dmz and ppm tolerance parameters; overly strict tolerances may fragment true patterns across multiple graph instances, while loose tolerances may merge distinct chemical pathways. Optimal values (e.g., dmz=0.007, ppm=15) must be validated per dataset.
- Patterns require count≥2 frequency threshold; rare fragmentation pathways present in only one spectrum will not be discovered.
- Network component structure (connected component vs. clique vs. pair) is determined by GNPS network construction parameters (cosine threshold, minimum match); components unrelated by shared patterns may still be grouped if connected transitively through intermediate spectra.
- F1-score ranking may not fully capture chemical relevance; patterns with perfect F1=1.0 are statistically optimal but may represent coincidental m/z alignments rather than true structural relationships. Chemical inspection of candidate molecular formulas is recommended.
- Patterns are represented as exact graphs (all edges present in all member spectra); minor spectral variation or noise may prevent pattern recognition in similar spectra that differ by a few m/z values.

## Evidence

- [readme] Each pattern is a graph with ion peaks as nodes and m/z differences as edges. These m/z differences can be any difference between the m/z values of two peaks of a spectrum, provided that they are frequent (i.e. detected in at least two spectra).: "Each **pattern is a graph** with **ion peaks as nodes** and **m/z differences as edges**. These m/z differences can be **any difference between the m/z values of two peaks of a spectrum**, provided"
- [readme] The structure of mineMS2 patterns in the form of exact graphs (all m/z differences of the pattern are present in all spectra containing this pattern) facilitates their chemical interpretation.: "the **structure of *mineMS2* patterns in the form of exact graphs** (all m/z differences of the pattern are present in all spectra containing this pattern) **facilitates their chemical"
- [readme] mineMS2 can be coupled to the GNPS MS/MS molecular networking methodology to focus on patterns that best explain components of the network.: "*mineMS2* can be further **coupled to the GNPS MS/MS molecular networking** methodology (Watrous *et al.*, 2012) to **focus on patterns that best explain components** of the network."
- [other] Pattern P70 achieves an F1-score of 1 for component 8 (precursor m/z 370.1283 and 404.0891), while other top-5 patterns maintain recall of 1 but have lower precision, indicating P70 is the only pattern that explains all component spectra without explaining spectra outside the component.: "Pattern P70 achieves an F1-score of 1 for component 8 (precursor m/z 370.1283 and 404.0891), while other top-5 patterns maintain recall of 1 but have lower precision, indicating P70 is the only"
- [other] Execute findPatternsExplainingComponents with metric=c('recall','precision','size'), top=5 to identify the five patterns best explaining each network component.: "Execute findPatternsExplainingComponents with metric=c('recall','precision','size'), top=5 to identify the five patterns best explaining each network component."
- [intro] We consider 3 type of components of the network: the connected components of the graph, the cliques, the high similarity pairs of nodes (pairs of spectra with a cosine score superior to a threshold).: "We consider 3 type of components of the network: the **connected components** of the graph, the **cliques**, the **high similarity pairs of nodes** (pairs of spectra with a cosine score superior to a"
- [other] The molecular network is read using the igraph package and extracted using findGNPSComponents with minSize threshold and cosine similarity filtering.: "Load the GNPS molecular network as an igraph object and extract network components using findGNPSComponents with minSize threshold and cosine similarity filtering."
