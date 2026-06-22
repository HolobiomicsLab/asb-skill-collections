---
name: ranked-annotation-prioritization
description: Use when you have completed cluster-based filtering of KEGG candidate assignments in untargeted LC-MS metabolomics and need to rank those candidates by biological plausibility using a metabolite interaction network. Specifically, use it after `clusterBased.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - mWISE
  - R
  - FELLA
  - igraph
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ranked-annotation-prioritization

## Summary

This skill reconstructs the diffusion prioritization stage of metabolomics annotation, which combines network-propagated diffusion scores with recovered peaks to build a final ranked compound annotation table. It is essential for converting cluster-filtered KEGG candidates into a context-aware, metabolite-network-informed ranking that prioritizes biologically plausible annotations.

## When to use

Apply this skill when you have completed cluster-based filtering of KEGG candidate assignments in untargeted LC-MS metabolomics and need to rank those candidates by biological plausibility using a metabolite interaction network. Specifically, use it after `clusterBased.filter` has assigned quasi-molecular adducts to feature clusters, but before delivering a final annotated peak table to the user.

## When NOT to use

- Input is already a fully annotated feature table or peak-intensity matrix; this skill applies only after cluster-based candidate filtering
- No KEGG metabolite network graph is available; diffusion propagation requires a connected network representation
- All peaks have been retained by cluster-based filtering and no recovery step is needed (skill is still applicable but the recovery step would be trivial)

## Inputs

- Cluster-filtered candidate assignments (output from clusterBased.filter)
- Sample FELLA graph (igraph object representing KEGG metabolite network)
- Feature-to-cluster mapping with intensity information

## Outputs

- Ranked.Tab: final ranked annotation table sorted by diffusion-prioritized scores
- Recovered peaks: peaks restored from complete removal by cluster-based filtering

## How to apply

The diffusion prioritization workflow operates in five steps. First, compute diffusion input scores from the cluster-filtered candidates using the `diffusion.input` function with `input.type` set to either 'probability' (soft scores) or 'binary' (hard assignments). Second, execute `set.diffusion` on the FELLA sample.graph to propagate scores through the metabolite network, allowing metabolites connected to high-scoring candidates to inherit signal. Third, apply z-score normalization to the diffusion scores to account for network topology and degree bias (setting `scores = z` rather than `raw`). Fourth, use `recoveringPeaks` to restore peaks that were completely removed by cluster-based filtering, merging them back by compound identifier. Fifth, compile and rank the final results using the `finalResults` function with z-score normalization, producing the `Ranked.Tab` output sorted by diffusion score.

## Related tools

- **mWISE** (R package providing diffusion.input, set.diffusion, recoveringPeaks, and finalResults functions for ranked prioritization) — https://dev.b2s.club/b2slab/mWISE
- **FELLA** (Provides the sample.graph metabolite network (igraph object) used for diffusion score propagation)
- **igraph** (Graph manipulation library; used to construct and traverse the undirected metabolite network)
- **R** (Execution environment for mWISE functions and statistical normalization (z-score calculation))

## Examples

```
diffusion.scores <- set.diffusion(diffusion.input(candidates, input.type='probability'), sample.graph); recovered <- recoveringPeaks(filtered.candidates); final <- finalResults(merge(diffusion.scores, recovered, by='compound_id'), scores='z')
```

## Evaluation signals

- Diffusion scores are computed for all cluster-filtered candidates and fall within a biologically plausible range (typically normalized to z-scores with mean 0, SD 1)
- Recovered peaks are successfully merged back into the final table by compound identifier with no duplicates or missing values
- The Ranked.Tab output is sorted in descending order by diffusion score, with the highest-scoring candidate per peak ranked first
- Z-score normalization has been applied; raw diffusion scores should NOT appear in the final output
- The final table schema includes columns for mass-to-charge ratio, cluster ID, compound identifier, diffusion score, and rank position

## Limitations

- Diffusion prioritization depends entirely on the quality and completeness of the underlying KEGG metabolite network; missing or misannotated edges may bias propagation
- Peaks completely removed by cluster-based filtering are recovered, but their diffusion scores may be lower due to lack of supporting evidence in the filtered candidate set
- Z-score normalization assumes the distribution of diffusion scores approximates a normal distribution; severely skewed networks may produce unintuitive rankings
- The method is sensitive to the `input.type` parameter (probability vs. binary); choice of input mode can substantially affect final rankings

## Evidence

- [intro] The diffusion prioritization stage operates by: (1) computing diffusion input from filtered candidates using `diffusion.input`; (2) applying `set.diffusion` with z-score normalization on the FELLA graph to obtain diffusion scores; (3) recovering completely removed peaks with `recoveringPeaks`; (4) merging the recovered peaks with diffusion results by compound identifier; and (5) building a final ranked table using `finalResults` function with z-score normalization.: "The diffusion prioritization stage operates by: (1) computing diffusion input from filtered candidates using `diffusion.input`; (2) applying `set.diffusion` with z-score normalization on the FELLA"
- [intro] The different diffusion inputs can be computed using the `diffusion.input` function. The `input.type` argument can be set to `probability` or `binary`.: "The different diffusion inputs can be computed using the `diffusion.input` function. The `input.type` argument can be set to `probability` or `binary`."
- [intro] The `z` score normalizes the diffusion scores by taking into account the topology of the graph. On the other hand, when `scores = raw`, no normalization is applied.: "The `z` score normalizes the diffusion scores by taking into account the topology of the graph. On the other hand, when `scores = raw`, no normalization is applied."
- [intro] The `recoveringPeaks` function recovers the peaks that have been completely removed by the cluster-based filter.: "The `recoveringPeaks` function recovers the peaks that have been completely removed by the cluster-based filter."
- [intro] mWISE integrates several strategies to provide a fast annotation of peak-intensity tables. It consists of three main steps aimed at i) matching mass-to-charge ratio values to KEGG database, ii) clustering and filtering the potential KEGG candidates, and building a final prioritized list using diffusion in networks: "mWISE integrates several strategies to provide a fast annotation of peak-intensity tables. It consists of three main steps aimed at i) matching mass-to-charge ratio values to KEGG database, ii)"
