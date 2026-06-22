---
name: network-diffusion-prioritization
description: Use when after clustering and filtering KEGG candidates for LC-MS features, when you have a ranked set of candidate metabolites per feature and access to a metabolite interaction network (e.g., from FELLA).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - mWISE
  - R
  - CAMERA
  - cliqueMS
  - FELLA
  - igraph
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides tools for context-based annotation of untargeted LC-MS data.
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package
- The default table of adducts and fragments is built using information from CAMERA R package
- The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS.
- information from CAMERA R package, H. Tong et al., and cliqueMS.
- we will now use the sample graph provided by FELLA R package
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

# network-diffusion-prioritization

## Summary

Applies diffusion-based prioritization on a metabolite network graph to rank candidate annotations by propagating probability scores through network topology. This skill prioritizes likely metabolite identities by leveraging context-aware network information rather than raw matching scores alone.

## When to use

After clustering and filtering KEGG candidates for LC-MS features, when you have a ranked set of candidate metabolites per feature and access to a metabolite interaction network (e.g., from FELLA). Use this skill to re-rank candidates by their network distance and topological context, especially when you want to suppress low-confidence matches and elevate contextually coherent identifications.

## When NOT to use

- Input candidate set is empty or has only one candidate per feature (diffusion will not improve ranking when there is no neighborhood context).
- Metabolite network graph is disconnected or highly fragmented (diffusion effectiveness degrades when most candidates are in isolated components).
- Upstream matching or clustering has failed to produce reliable candidate sets (diffusion amplifies noise from poor initial annotations).

## Inputs

- Clustered and filtered KEGG candidates table (output from clusterBased.filter)
- Feature intensity matrix or probability scores per candidate
- Undirected metabolite network graph (igraph object or adjacency structure)
- Quasi-molecular adduct and frequency threshold metadata

## Outputs

- Diffusion-prioritized ranked candidates table
- Final ranked results with z-score normalized diffusion scores
- Recovered peak assignments for completely filtered-out features

## How to apply

Compute diffusion input scores using the diffusion.input function, selecting either 'probability' (soft weights based on matching confidence) or 'binary' (hard presence/absence) as the input.type. Apply diffusion scoring via network propagation on an igraph-compatible undirected metabolite graph, optionally normalizing scores using z-score transformation to account for graph topology (which suppresses candidates in low-connectivity regions). Recover completely removed peaks using recoveringPeaks, then compile final ranked results using finalResults. The z-score normalization is strongly recommended to normalize diffusion scores by taking into account the topology of the graph, preventing high-degree hub nodes from artificially inflating candidate scores.

## Related tools

- **mWISE** (Executes diffusion.input and diffusion scoring functions; integrates network diffusion into the full annotation pipeline) — https://dev.b2s.club/b2slab/mWISE
- **FELLA** (Provides sample metabolite network graph (sample.graph) used for diffusion propagation)
- **igraph** (Converts and manipulates network graph structure (e.g., as.undirected) for diffusion computation)
- **R** (Runtime environment for diffusion functions and network operations)

## Examples

```
diff.input <- diffusion.input(candidates, input.type='probability'); diff.scores <- diffusion(diff.input, g.metab, scores='z'); final <- finalResults(diff.scores); perf <- performanceEvaluation(final, df.Ref, top.cmps=3)
```

## Evaluation signals

- Verify that diffusion scores are normalized (z-scores have mean ≈ 0 and SD ≈ 1) when z-score normalization is enabled, confirming topology correction is applied.
- Check that top-ranked candidates per feature have higher network connectivity or shorter paths to other high-confidence hits in the graph.
- Confirm that recoveringPeaks function successfully restores features that were removed by cluster-based filtering, with non-zero diffusion scores.
- Compare precision, recall, and F1-score against reference peaks (df.Ref) using performanceEvaluation with top.cmps argument; expect improvement over pre-diffusion rankings.
- Validate that final ranked results table contains no null or missing diffusion scores for retained candidates, and that rank order is monotonically consistent with diffusion score values.

## Limitations

- Diffusion effectiveness depends on network coverage: candidates not in the metabolite graph or in isolated components will not benefit from prioritization.
- Raw diffusion scores (without z-score normalization) can be biased by network hub nodes, artificially elevating candidates near high-degree metabolites.
- Performance is sensitive to the choice of diffusion input type (probability vs. binary); selecting the wrong input.type can worsen ranking quality.
- Recovery of completely filtered peaks via recoveringPeaks may reintroduce false positives if the original cluster-based filter removed them for valid reasons.

## Evidence

- [intro] building a final prioritized list using diffusion in networks: "building a final prioritized list using diffusion in networks"
- [intro] The different diffusion inputs can be computed using the `diffusion.input` function with probability or binary input types: "The `input.type` argument can be set to `probability` or `binary`."
- [intro] Z-score normalization accounts for graph topology in diffusion scoring: "The `z` score normalizes the diffusion scores by taking into account the topology of the graph."
- [intro] Recovery of completely removed peaks via recoveringPeaks function: "The `recoveringPeaks` function recovers the peaks that have been completely removed by the cluster-based filter."
- [intro] Final results compilation using finalResults function: "the diffusion prioritized table is built using the `finalResults` function"
