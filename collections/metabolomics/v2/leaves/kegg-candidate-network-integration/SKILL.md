---
name: kegg-candidate-network-integration
description: Use when after cluster-based filtering has produced a set of candidate
  KEGG compounds for each feature cluster in untargeted LC-MS data, and you need to
  rank these candidates by their metabolic plausibility using network context rather
  than mass accuracy alone.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
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
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides
  tools for context-based annotation of untargeted LC-MS data.
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

# KEGG Candidate Network Integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Integrate KEGG metabolite candidates into a metabolic network graph and apply diffusion-based scoring to prioritize annotations by propagating confidence scores through network topology. This skill transforms a flat list of candidate compounds into a ranked, network-contextualized annotation table.

## When to use

Apply this skill after cluster-based filtering has produced a set of candidate KEGG compounds for each feature cluster in untargeted LC-MS data, and you need to rank these candidates by their metabolic plausibility using network context rather than mass accuracy alone. Use when you have both filtered KEGG candidates and access to a metabolite interaction network (e.g., FELLA graph).

## When NOT to use

- Input is a pre-ranked or manually curated annotation table — network integration will not add value.
- No metabolite network graph is available or applicable to your compound class (e.g., synthetic small molecules not in KEGG).
- Candidate set is extremely sparse or fragmented across disconnected network components; diffusion will not propagate meaningful scores.

## Inputs

- Filtered candidate assignments (cluster → KEGG compound mappings)
- Feature intensity matrix or feature clustering output
- Metabolite network graph (igraph object, typically FELLA sample.graph)
- Adduct/fragment annotation table (from prior matching stage)

## Outputs

- Ranked annotation table (Ranked.Tab) with columns: peak identifier, KEGG compound ID, diffusion score, z-score normalized confidence, network-integrated rank
- Recovered peaks list (compounds flagged as completely removed by filtering but recovered via network)

## How to apply

Compute diffusion input scores from filtered candidate assignments using the `diffusion.input` function with input.type set to either 'probability' (weighted by match quality) or 'binary' (presence/absence). Load or construct a metabolite network graph (typically FELLA's KEGG-derived graph via igraph). Execute `set.diffusion` on the network to propagate candidate scores through the graph topology, accounting for metabolic relationships. Apply z-score normalization to the diffusion output to account for graph structure (nodes in highly connected regions receive different baseline scores). Recover any peaks completely removed by prior filtering using `recoveringPeaks`, then merge recovered peaks with diffusion results by compound identifier. Finally, compile and rank results using the `finalResults` function to produce a Ranked.Tab table sorted by network-integrated confidence.

## Related tools

- **FELLA** (Provides pre-built KEGG metabolite network graph (sample.graph) and set.diffusion function for network propagation of scores)
- **igraph** (Underlying graph representation and manipulation; converts network to undirected format for diffusion propagation)
- **mWISE** (R package containing diffusion.input, recoveringPeaks, finalResults functions; orchestrates candidate-to-network integration workflow) — https://dev.b2s.club/b2slab/mWISE
- **R** (Execution environment for network graph operations and diffusion calculations)

## Examples

```
diffusion_scores <- set.diffusion(sample.graph, diffusion.input(filtered_candidates, input.type='probability')); recovered <- recoveringPeaks(filtered_candidates, prior_removed); final_ranks <- finalResults(diffusion_scores, recovered, scores='z')
```

## Evaluation signals

- Ranked.Tab contains no NaN or infinite values in diffusion or z-score columns; all rows correspond to input feature clusters or recovered peaks.
- Diffusion scores show expected topology-dependent variation: compounds in highly connected network regions have different baseline scores than peripheral compounds, even when input confidence is identical.
- Z-score normalization produces mean ≈ 0 and standard deviation ≈ 1 across the full result set, confirming statistical scaling.
- Recovered peaks are a non-empty subset of candidates completely filtered out in the prior stage; their re-appearance can be validated against the filtering log.
- Final rank order shows network-plausible compounds (e.g., cofactors, substrates) ranked higher than chemically similar but metabolically isolated candidates when both have similar input scores.

## Limitations

- Diffusion results depend critically on network completeness and accuracy; KEGG coverage gaps or outdated network versions will propagate through rankings.
- Z-score normalization may over-penalize or over-reward candidates in sparsely connected regions; results may not be intuitive for rare or orphan metabolites.
- Binary vs. probability input.type choice significantly affects output; no automated selection is provided — user must justify choice based on upstream confidence model.
- Network diffusion assumes metabolic plausibility correlates with graph proximity; this assumption breaks for isomers, xenobiotics, and non-KEGG compounds.

## Evidence

- [intro] The diffusion prioritization stage operates by: (1) computing diffusion input from filtered candidates using `diffusion.input`; (2) applying `set.diffusion` with z-score normalization on the FELLA graph to obtain diffusion scores; (3) recovering completely removed peaks with `recoveringPeaks`; (4) merging the recovered peaks with diffusion results by compound identifier; and (5) building a final ranked table using `finalResults` function with z-score normalization.: "The diffusion prioritization stage operates by: (1) computing diffusion input from filtered candidates using `diffusion.input`; (2) applying `set.diffusion` with z-score normalization on the FELLA"
- [intro] The different diffusion inputs can be computed using the `diffusion.input` function. The `input.type` argument can be set to `probability` or `binary`.: "The different diffusion inputs can be computed using the `diffusion.input` function. The `input.type` argument can be set to `probability` or `binary`."
- [intro] The `z` score normalizes the diffusion scores by taking into account the topology of the graph. On the other hand, when `scores = raw`, no normalization is applied.: "The `z` score normalizes the diffusion scores by taking into account the topology of the graph. On the other hand, when `scores = raw`, no normalization is applied."
- [intro] we will now use the sample graph provided by FELLA R package: "we will now use the sample graph provided by FELLA R package"
- [intro] mWISE integrates several strategies to provide a fast annotation of peak-intensity tables. It consists of three main steps aimed at i) matching mass-to-charge ratio values to KEGG database, ii) clustering and filtering the potential KEGG candidates, iii) building a final prioritized list using diffusion in networks.: "building a final prioritized list using diffusion in networks"
