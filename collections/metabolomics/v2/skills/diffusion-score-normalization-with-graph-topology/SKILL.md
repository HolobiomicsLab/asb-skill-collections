---
name: diffusion-score-normalization-with-graph-topology
description: Use when after propagating diffusion scores through the FELLA metabolite network using set.diffusion, when raw diffusion scores would otherwise favor candidates in high-degree regions or penalize those in sparse regions. Use this normalization when building the final ranked annotation table (Ranked.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0821
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
---

# diffusion-score-normalization-with-graph-topology

## Summary

Apply z-score normalization to diffusion scores computed over a metabolite network (FELLA graph) to account for local and global network topology effects, ensuring fair ranking of candidates across regions of varying network density. This prevents bias toward highly connected metabolites or sparse subgraphs when prioritizing annotation candidates.

## When to use

After propagating diffusion scores through the FELLA metabolite network using set.diffusion, when raw diffusion scores would otherwise favor candidates in high-degree regions or penalize those in sparse regions. Use this normalization when building the final ranked annotation table (Ranked.Tab) to ensure candidates are prioritized by biological relevance rather than network architecture artifacts.

## When NOT to use

- Input data lacks network topology or uses a flat candidate list without graph structure (raw scores may be appropriate).
- The FELLA graph is already highly uniform in node degree or the analysis goal explicitly requires raw diffusion scores for interpretability.

## Inputs

- diffusion input scores (probability or binary; from diffusion.input function output)
- sample.graph (FELLA igraph object representing metabolite network)
- filtered candidate assignments (from cluster-based filtering stage)

## Outputs

- z-score normalized diffusion scores (per metabolite/compound)
- diffusion-prioritized Ranked.Tab (final ranked annotation table)

## How to apply

Execute set.diffusion on the sample.graph (FELLA R package igraph object) with the computed diffusion input scores (from diffusion.input function using probability or binary input.type). Apply z-score normalization by setting the scores parameter to 'z' rather than 'raw' — this normalizes each diffusion score by subtracting the mean and dividing by the standard deviation of scores across the graph, accounting for the topology. The z-score transformation corrects for systematic bias introduced by network structure (e.g., hub metabolites with higher baseline connectivity). Pass the normalized scores to the finalResults function to compile the diffusion-prioritized ranked table. This ensures that the final Ranked.Tab output reflects metabolite relevance conditioned on network structure, not raw connectivity.

## Related tools

- **FELLA** (Provides the metabolite network graph (sample.graph) and set.diffusion function for score propagation over igraph-compatible network structures)
- **igraph** (Underlying graph data structure and topology representation used by FELLA; enables z-score calculation across network-wide score distributions)
- **mWISE** (Orchestrates the full diffusion prioritization workflow, including diffusion.input computation, set.diffusion execution with normalization, and finalResults compilation) — https://dev.b2s.club/b2slab/mWISE

## Examples

```
set.diffusion(diffusion.input(filtered_candidates, input.type='probability'), sample.graph, scores='z'); finalResults(diffusion_scores_normalized, recovered_peaks)
```

## Evaluation signals

- Z-score normalized diffusion scores should have mean ≈ 0 and standard deviation ≈ 1 across the graph (verify via summary statistics on the normalized score vector).
- Candidates in sparse subgraphs should rank comparably to candidates in high-degree regions when corrected for biological signal (compare rank distributions before/after normalization).
- Final Ranked.Tab should show no systematic bias toward hub metabolites; instead, ranking reflects convergent evidence from input probabilities and network diffusion.
- Raw and z-normalized scores should have same rank order when corrected for scale; verify Spearman correlation ≈ 1.0 between raw and normalized scores.
- Recovered peaks (from recoveringPeaks function) should be incorporated into the final ranked output, preserving candidates that were filtered in earlier stages but later recovered.

## Limitations

- Z-score normalization assumes approximate normality of score distribution; highly skewed or bimodal distributions may produce misleading normalized scores.
- Network topology artifacts (e.g., disconnected components or star-like subgraphs in KEGG) are not eliminated, only scaled; biological interpretation still depends on KEGG graph quality.
- The diffusion prioritization stage relies on accurate cluster-based filtering upstream; if true metabolite candidates were removed in clustering, normalization cannot recover them (only peaks removed entirely by filtering are recovered by recoveringPeaks).

## Evidence

- [intro] The z score normalizes the diffusion scores by taking into account the topology of the graph.: "The `z` score normalizes the diffusion scores by taking into account the topology of the graph. On the other hand, when `scores = raw`, no normalization is applied."
- [intro] set.diffusion is applied with z-score normalization on FELLA graph to obtain diffusion scores as part of diffusion prioritization.: "applying `set.diffusion` with z-score normalization on the FELLA graph to obtain diffusion scores"
- [intro] The diffusion prioritization stage builds final ranked results using the finalResults function with z-score normalization.: "building a final ranked table using `finalResults` function with z-score normalization."
- [intro] Diffusion input scores are computed using the diffusion.input function with input.type set to probability or binary.: "The different diffusion inputs can be computed using the `diffusion.input` function. The `input.type` argument can be set to `probability` or `binary`."
