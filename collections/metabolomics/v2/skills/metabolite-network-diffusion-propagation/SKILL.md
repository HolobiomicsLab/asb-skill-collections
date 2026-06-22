---
name: metabolite-network-diffusion-propagation
description: Use when after cluster-based filtering of KEGG candidates has produced a set of candidate metabolites with assigned scores, but before final annotation ranking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3359
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - mWISE
  - R
  - FELLA
  - igraph
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides tools for context-based annotation of untargeted LC-MS data.
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package
- we will now use the sample graph provided by FELLA R package
- g.metab <- igraph::as.undirected(sample.graph)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwise_cq
    doi: 10.1021/acs.analchem.1c00238
    title: mWISE
  dedup_kept_from: coll_mwise_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c00238
  all_source_dois:
  - 10.1021/acs.analchem.1c00238
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-network-diffusion-propagation

## Summary

Propagate candidate metabolite scores through a KEGG-derived metabolic network graph to prioritize annotations by network proximity and topology. This skill ranks metabolite identifications by diffusing association scores across the network, accounting for graph structure via z-score normalization, to produce a final ranked annotation table.

## When to use

After cluster-based filtering of KEGG candidates has produced a set of candidate metabolites with assigned scores, but before final annotation ranking. Use this skill when you need to leverage metabolic network context to disambiguate or re-rank candidates—particularly when multiple compounds map to the same peak cluster and you want to prioritize compounds that are topologically central or connected to high-scoring neighbors in the KEGG metabolite network.

## When NOT to use

- Input candidate set is empty or contains no valid KEGG compound identifiers that map to the graph
- KEGG metabolite network graph is unavailable, incomplete, or does not cover the metabolite space of interest
- All peaks have been retained by cluster-based filtering and no recovery of removed peaks is needed (though diffusion prioritization may still be useful)

## Inputs

- cluster-filtered candidate assignments (compound identifiers with cluster membership and p-value or frequency scores)
- FELLA sample.graph (igraph object: undirected metabolite network from KEGG database)
- input.type specification ('probability' or 'binary')

## Outputs

- diffusion scores (propagated association values with z-score normalization)
- recovered peaks (features completely removed by cluster-based filtering)
- Ranked.Tab (final ranked annotation table, ordered by diffusion-prioritized scores)

## How to apply

Compute diffusion input scores from cluster-filtered candidate assignments using the `diffusion.input` function with `input.type` set to either 'probability' (continuous scores) or 'binary' (presence/absence). Execute `set.diffusion` on the sample.graph (FELLA R package) to propagate these scores through the metabolite network, allowing high scores to influence neighbors and cascade through connected pathways. Apply z-score normalization to the resulting diffusion scores to account for network topology and node degree heterogeneity. Recover peaks that were completely removed during cluster-based filtering using `recoveringPeaks`, then merge these recovered peaks with diffusion results by compound identifier. Finally, compile and rank all results using the `finalResults` function with z-score normalization to generate the final diffusion-prioritized ranked annotation table (Ranked.Tab output).

## Related tools

- **FELLA** (Provides the sample.graph (metabolite network) and set.diffusion function for network-based score propagation with graph topology integration)
- **igraph** (Underlying graph representation and manipulation library; used to construct and traverse the undirected metabolite network)
- **mWISE** (Parent package providing diffusion.input, recoveringPeaks, and finalResults functions; orchestrates the full diffusion prioritization workflow) — https://dev.b2s.club/b2slab/mWISE
- **R** (Execution environment for all diffusion computation, graph operations, and statistical normalization)

## Examples

```
diffusion_scores <- set.diffusion(method = 'z', object = sample.graph, scores = diffusion.input(candidates_filtered, input.type = 'probability')); recovered <- recoveringPeaks(candidates_all, candidates_filtered); ranked_tab <- finalResults(diffusion_scores, recovered, scores = 'z')
```

## Evaluation signals

- Diffusion scores are properly z-score normalized: mean ≈ 0, standard deviation ≈ 1; no NaN or infinite values
- All recovered peaks are successfully merged back into the diffusion results by compound identifier; no missing or duplicated compound entries in final Ranked.Tab
- Final Ranked.Tab is sorted in descending order by diffusion score; ranks are monotonically increasing or decreasing as expected
- Compounds with high-scoring neighbors in the KEGG network receive higher diffusion scores than isolated low-scoring candidates, confirming network topology influence
- Number of rows in final Ranked.Tab equals the union of diffusion-scored candidates and recovered peaks; no data loss

## Limitations

- Diffusion prioritization relies on KEGG network completeness and accuracy; missing or incorrect pathway edges will propagate biased scores
- Z-score normalization assumes a roughly normal distribution of raw diffusion scores; highly skewed or bimodal score distributions may not normalize effectively
- Recovered peaks (completely filtered candidates) are re-ranked by diffusion without their original cluster context, potentially placing them lower in the final table regardless of network position
- Network diffusion is sensitive to starting score distribution (input.type choice) and graph density; sparse or disconnected subgraphs may produce uninformative diffusion
- The FELLA sample.graph represents a static metabolic network snapshot; real metabolic capability and context-specific pathway activation are not captured

## Evidence

- [other] The diffusion prioritization stage operates by: (1) computing diffusion input from filtered candidates using `diffusion.input`; (2) applying `set.diffusion` with z-score normalization on the FELLA graph to obtain diffusion scores; (3) recovering completely removed peaks with `recoveringPeaks`; (4) merging the recovered peaks with diffusion results by compound identifier; and (5) building a final ranked table using `finalResults` function with z-score normalization.: "The diffusion prioritization stage operates by: (1) computing diffusion input from filtered candidates using `diffusion.input`; (2) applying `set.diffusion` with z-score normalization on the FELLA"
- [intro] The different diffusion inputs can be computed using the `diffusion.input` function. The `input.type` argument can be set to `probability` or `binary`.: "The different diffusion inputs can be computed using the `diffusion.input` function. The `input.type` argument can be set to `probability` or `binary`."
- [intro] The `z` score normalizes the diffusion scores by taking into account the topology of the graph. On the other hand, when `scores = raw`, no normalization is applied.: "The `z` score normalizes the diffusion scores by taking into account the topology of the graph. On the other hand, when `scores = raw`, no normalization is applied."
- [intro] we will now use the sample graph provided by FELLA R package: "we will now use the sample graph provided by FELLA R package"
- [intro] mWISE integrates several strategies to provide a fast annotation of peak-intensity tables. It consists of three main steps aimed at i) matching mass-to-charge ratio values to KEGG database, ii) clustering and filtering the potential KEGG candidates, iii) building a final prioritized list using diffusion in networks: "building a final prioritized list using diffusion in networks"
