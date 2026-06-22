---
name: precision-recall-optimization-in-spectral-annotation
description: Use when you have extracted fragmentation patterns from a collection of MS/MS spectra (using mineMS2) and have partitioned spectra into components via GNPS molecular networking (e.g., connected components, cliques, or high-similarity pairs with cosine > threshold).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3941
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
  - LC-MS
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

# precision-recall-optimization-in-spectral-annotation

## Summary

Identify and rank fragmentation patterns that optimally explain MS/MS spectral components by balancing recall (proportion of component spectra explained) and precision (proportion of explained spectra that belong to the component), using F1-score and other metrics to isolate patterns with perfect or near-perfect explanatory power. This skill is essential when coupled to GNPS molecular networks to annotate network components with chemically interpretable fragmentation patterns.

## When to use

You have extracted fragmentation patterns from a collection of MS/MS spectra (using mineMS2) and have partitioned spectra into components via GNPS molecular networking (e.g., connected components, cliques, or high-similarity pairs with cosine > threshold). You now need to determine which patterns best explain each component without overgeneralizing to unrelated spectra. Use this skill when you want to identify the single most specific and sensitive pattern per component, or to rank the top-N candidate patterns by their balance of recall and precision.

## When NOT to use

- Input spectra have not yet been discretized (m/z differences not aligned via discretizeMzDifferences with appropriate dmz and ppm tolerances); run discretization first.
- Patterns have not been mined or extracted (mineClosedSubgraphs not yet called); this skill assumes a pre-computed set of candidate patterns.
- GNPS molecular network has not been loaded or components have not been extracted (findGNPSComponents not called); component definition is a prerequisite.

## Inputs

- ms2Lib object (containing 51 MS/MS spectra with discretized m/z differences, dmz=0.007, ppm=15)
- Collection of extracted fragmentation patterns (frequent closed subgraphs)
- GNPS molecular network as igraph object (nodes=spectra, edges=cosine similarity)
- Extracted network components (connected components, cliques, or high-similarity pairs)

## Outputs

- Ranked list of patterns per component with recall, precision, size, and F1-score metrics
- Pattern–component assignment table (pattern ID, component ID, metrics)
- Annotated network (GraphML) with best-explaining pattern labels per node/component
- Visualization-ready metrics table for component-pattern pairing

## How to apply

Load the ms2Lib object (containing all spectra and their fragmentation graphs) and the GNPS molecular network as an igraph object. Call findPatternsExplainingComponents() with metric=c('recall','precision','size') and top=N (typically top=5) to compute recall (number of component spectra matched by the pattern / total component spectra), precision (number of component spectra matched / total spectra matched by pattern), and size metrics for all patterns against all extracted components. Calculate F1-score for each pattern as the harmonic mean of recall and precision. Extract and rank patterns by F1-score; patterns achieving F1=1.0 (or recall=1.0 with maximal precision) represent ideal component explainers. Use the ranking to select the best pattern for annotation or to verify that competing patterns trade off recall and precision as expected. Export the ranked results with metrics per component for downstream network visualization and chemical validation.

## Related tools

- **mineMS2** (Core package providing findPatternsExplainingComponents() function and ms2Lib class to store spectra, patterns, and fragmentation graphs) — https://github.com/odisce/mineMS2
- **igraph** (Loads and manipulates GNPS molecular network (GraphML format) and extracts network components (connected components, cliques, high-similarity pairs))
- **GNPS** (Provides the MS/MS molecular networking methodology that defines spectral components through cosine similarity thresholding; network output (GraphML) is input to this skill)
- **Cytoscape** (Visualization tool for the annotated molecular network (optional downstream step after pattern annotation))
- **R** (Host language for mineMS2 and igraph; used to execute the entire workflow)

## Examples

```
findPatternsExplainingComponents(ms2Lib, molnet.igraph, metric=c('recall','precision','size'), top=5, minSize=1, pairThreshold=0.9)
```

## Evaluation signals

- The top-ranked pattern for a component achieves recall=1.0 and precision=1.0 (F1=1.0), meaning it explains all component spectra and no spectra outside the component.
- All other patterns in the top-5 for a component maintain recall ≥ 1.0 but show precision < 1.0, confirming that the top-ranked pattern is the sole optimal explainer.
- Recall values remain constant (or decrease slightly) as you move down the ranking, while precision strictly decreases, demonstrating the precision-recall trade-off.
- The exported metrics table contains no missing or NaN values for recall, precision, size, and F1-score; all components are assigned at least one pattern.
- The annotated network GraphML file can be loaded into Cytoscape without errors and displays pattern labels and metrics as node/component attributes.

## Limitations

- The skill is sensitive to GNPS network thresholds (e.g., cosine similarity cutoff for edges, minSize for component extraction); variations in these thresholds will alter component membership and thus recall/precision rankings.
- Patterns are limited to frequent closed subgraphs (mined with count ≥ 2); very rare or singleton fragmentation motifs will not be discovered.
- The method discovers patterns independent of external spectral databases and precursor molecular formulas; chemical validation of top patterns is still necessary to confirm biological relevance.
- Discretization parameters (dmz and ppm) directly affect pattern definition; suboptimal tolerance settings may merge or fragment true m/z differences, degrading pattern quality and ranking reliability.

## Evidence

- [other] Pattern P70 achieves an F1-score of 1 for component 8 (precursor m/z 370.1283 and 404.0891), while other top-5 patterns maintain recall of 1 but have lower precision: "Pattern P70 achieves an F1-score of 1 for component 8 (precursor m/z 370.1283 and 404.0891), while other top-5 patterns maintain recall of 1 but have lower precision, indicating P70 is the only"
- [intro] mineMS2 can be coupled to GNPS molecular networking to focus on patterns that best explain network components: "This vignette describes how *mineMS2* can be **coupled to the GNPS MS/MS molecular networking** methodology to **focus on patterns that best explain components** of the network"
- [intro] Find patterns that best explain extracted network components: "*mineMS2* then enables to select the pattern that best explain each of the extracted components according to 3 metrics"
- [other] Execute findPatternsExplainingComponents with metric and top parameters: "Execute findPatternsExplainingComponents with metric=c('recall','precision','size'), top=5 to identify the five patterns best explaining each network component."
- [intro] The structure of mineMS2 patterns facilitates chemical interpretation: "the **structure of *mineMS2* patterns in the form of exact graphs** (all m/z differences of the pattern are present in all spectra containing this pattern) **facilitates their chemical"
- [intro] Three types of network components are considered: "We consider 3 type of components of the network: the **connected components** of the graph, the **cliques**, the **high similarity pairs of nodes**"
