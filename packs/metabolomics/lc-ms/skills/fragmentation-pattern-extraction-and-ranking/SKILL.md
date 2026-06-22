---
name: fragmentation-pattern-extraction-and-ranking
description: Use when you have a collection of MS/MS spectra (≥2 spectra) and wish to identify fragmentation signatures common to subsets of those spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0226
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - mineMS2
  - igraph
  - R
  - GNPS
  - Cytoscape
  - MSnbase
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fragmentation-pattern-extraction-and-ranking

## Summary

Extract frequent fragmentation patterns from collections of MS/MS spectra by mining closed subgraphs of m/z differences, then rank patterns by their ability to explain network components using recall, precision, and size metrics. This skill enables discovery of shared fragmentation signatures independent of spectral database thresholds and molecular formula knowledge.

## When to use

Apply this skill when you have a collection of MS/MS spectra (≥2 spectra) and wish to identify fragmentation signatures common to subsets of those spectra. Particularly valuable when coupled to GNPS molecular networks to explain why spectral pairs or cliques cluster together, or when seeking patterns that distinguish one set of spectra from others without requiring precursor molecular formulas or external spectral libraries.

## When NOT to use

- Input collection contains fewer than 2 spectra (frequency threshold count≥2 cannot be met)
- Spectra lack sufficient structural diversity (very high cosine similarity across all pairs leaves no rank discrimination between patterns)
- Goal is to identify neutral losses only; mineMS2 patterns include any m/z difference between peaks, not just diagnostic neutral losses

## Inputs

- ms2Lib object (collection of MS/MS spectra with discretized m/z differences)
- igraph object (GNPS molecular network as adjacency graph)
- dmz parameter (absolute m/z tolerance, e.g. 0.007 Da)
- ppm parameter (relative m/z tolerance, e.g. 15 ppm)
- minSize, count thresholds for frequent subgraph mining
- cosine similarity threshold for network component extraction (e.g. 0.9)

## Outputs

- Set of extracted fragmentation patterns (closed subgraphs with m/z differences as edges)
- Pattern metrics table (recall, precision, F1-score, size for each pattern)
- Ranked pattern assignments per network component (top-N patterns per component)
- Annotated igraph object with best-explaining patterns linked to components
- GraphML export of annotated network for visualization in Cytoscape

## How to apply

First, discretize m/z differences across all spectra using dmz (absolute tolerance, e.g. 0.007 Da) and ppm (relative tolerance, e.g. 15 ppm) thresholds to align fragmentation features across the collection. Build fragmentation graphs for each spectrum with ion peaks as nodes and discretized m/z differences as edges. Mine closed subgraphs using a frequency threshold (count ≥2) and size filter to extract candidate patterns. If integrating with a molecular network, load the GNPS GraphML via igraph and extract network components (connected components, cliques, high-similarity pairs with cosine ≥ threshold such as 0.9). For each component, rank extracted patterns using findPatternsExplainingComponents with metrics c('recall','precision','size') and top=N to select the N best explainers. Patterns with recall=1.0 and precision=1.0 are optimal (F1=1.0), indicating they explain all and only the spectra in that component.

## Related tools

- **mineMS2** (Core package for discretizing m/z differences, mining closed subgraphs, and ranking patterns by recall-precision metrics) — https://github.com/odisce/mineMS2
- **igraph** (Loading and manipulating GNPS molecular networks (GraphML format) and extracting connected components, cliques, and high-similarity pairs)
- **GNPS** (Public MS/MS spectral library and molecular networking platform that supplies precursor-based similarity networks for component extraction)
- **Cytoscape** (Visualizing annotated networks with patterns and component assignments)
- **MSnbase** (Storing spectra as Spectrum2 objects and managing MS/MS metadata)

## Examples

```
discretizeMzDifferences(pnordicum.m2l, dmz=0.007, ppm=15); mineClosedSubgraphs(pnordicum.m2l, sizeMin=1, count=2); findPatternsExplainingComponents(molnet.igraph, metric=c('recall','precision','size'), top=5)
```

## Evaluation signals

- Extracted patterns are reproducible: same spectra collection and parameters (dmz, ppm, count threshold) yield identical patterns across runs
- Recall and precision scores for top-ranked patterns sum correctly per component: for a pattern explaining k spectra in a component of size n, recall = k/n and precision = k/(total spectra containing pattern)
- Optimal patterns (F1=1.0) satisfy both recall=1.0 AND precision=1.0, meaning they cover all component spectra and no non-member spectra
- Pattern size (number of edges/m/z differences) correlates with specificity: smaller patterns may explain more spectra (lower precision) while larger patterns explain fewer (higher precision)
- Annotated GraphML export is valid igraph object and can be loaded and visualized in Cytoscape without format errors

## Limitations

- Discretization tolerance (dmz, ppm) directly controls pattern granularity: overly tight tolerances yield few patterns; loose tolerances yield redundant patterns across spectra with natural drift
- Frequency threshold (count≥2) sets minimum co-occurrence; small thresholds admit noise, large thresholds miss rare but chemically important patterns
- Ranking by recall-precision-size is sensitive to component size: very small components (2–3 spectra) have limited precision variance, making rank discrimination unstable
- Patterns are independent of precursor m/z or molecular formula, so chemically implausible m/z differences may be included if they co-occur frequently
- Coupling to GNPS networks depends on threshold (e.g. cosine ≥0.9) for component extraction; changing this threshold changes which components are ranked, potentially altering pattern importance

## Evidence

- [readme] Each pattern is a graph with ion peaks as nodes and m/z differences as edges. These m/z differences can be any difference between the m/z values of two peaks of a spectrum, provided that they are frequent (i.e. detected in at least two spectra).: "Each **pattern is a graph** with **ion peaks as nodes** and **m/z differences as edges**. These m/z differences can be **any difference between the m/z values of two peaks of a spectrum**, provided"
- [intro] discretizeMzDifferences(pnordicum.m2l, dmz = 0.007, ppm = 15, maxFrags = 15): "discretizeMzDifferences(pnordicum.m2l, dmz = 0.007, ppm = 15, maxFrags = 15)"
- [intro] mineClosedSubgraphs(pnordicum.m2l, sizeMin = 1, count = 2): "mineClosedSubgraphs(pnordicum.m2l, sizeMin = 1, count = 2)"
- [intro] mineMS2 can be coupled to the GNPS MS/MS molecular networking methodology to focus on patterns that best explain components of the network: "mineMS2 can be **coupled to the GNPS MS/MS molecular networking** methodology to **focus on patterns that best explain components** of the network"
- [other] Pattern P70 achieves an F1-score of 1 for component 8 (precursor m/z 370.1283 and 404.0891), while other top-5 patterns maintain recall of 1 but have lower precision, indicating P70 is the only pattern that explains all component spectra without explaining spectra outside the component.: "Pattern P70 achieves an F1-score of 1 for component 8 (precursor m/z 370.1283 and 404.0891), while other top-5 patterns maintain recall of 1 but have lower precision"
- [readme] the structure of mineMS2 patterns in the form of exact graphs (all m/z differences of the pattern are present in all spectra containing this pattern) facilitates their chemical interpretation: "the **structure of *mineMS2* patterns in the form of exact graphs** (all m/z differences of the pattern are present in all spectra containing this pattern) **facilitates their chemical"
- [readme] Importantly, this method is independent of external spectral databases and knowledge of the molecular formula of precursor ions: "Importantly, this method is **independent of external spectral databases and knowledge of the molecular formula of precursor ions**"
