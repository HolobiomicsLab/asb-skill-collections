---
name: label-propagation-network-algorithm
description: Use when you have a ranked list of seed genes or metabolites (e.g., from
  metabolomic enrichment analysis with MSEA scores, or exome-derived candidate genes)
  and you want to propagate their signals across a gene–protein interaction network
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_2269
  - http://edamontology.org/topic_3325
  tools:
  - metPropagate
  - Label propagation (adapted from Yuto Yamaguchi)
  - STRING database
  - XCMS / CAMERA
  license_tier: restricted
derived_from:
- doi: 10.1038/s41525-020-0132-5
  title: metPropagate
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metpropagate_cq
    doi: 10.1038/s41525-020-0132-5
    title: metPropagate
  dedup_kept_from: coll_metpropagate_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41525-020-0132-5
  all_source_dois:
  - 10.1038/s41525-020-0132-5
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# label-propagation-network-algorithm

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Label propagation iteratively distributes seed labels (e.g., from metabolomic enrichment scores) across a gene/protein interaction network to compute ranked gene scores that reflect both network proximity to seeds and propagation confidence. This skill is used to prioritize disease genes by leveraging both omics-derived signals and network topology.

## When to use

Apply this skill when you have a ranked list of seed genes or metabolites (e.g., from metabolomic enrichment analysis with MSEA scores, or exome-derived candidate genes) and you want to propagate their signals across a gene–protein interaction network (e.g., STRING database) to generate genome-wide prioritized gene rankings that incorporate network structure. Use it specifically when seed labels are sparse but high-confidence, and you want to infer related genes through network-guided diffusion rather than independent scoring.

## When NOT to use

- Input network is disconnected or extremely sparse (fewer edges than nodes); propagation will not reach most genes.
- Seed labels are already genome-wide predictions (not sparse, high-confidence signals); label propagation is redundant.
- You have no prior network or all genes are equally likely; propagation cannot differentiate based on topology.

## Inputs

- Gene/protein interaction network (e.g., STRING database: node IDs, gene names, edge list)
- Seed label file: per-gene label derived from metabolomic enrichment scores or candidate genes (binary or continuous)
- Node ID to gene name mapping file (if network uses internal node IDs)

## Outputs

- Ranked gene list with propagated scores (score per candidate gene post-propagation)
- Original seed scores per gene (for comparison and validation)
- Network propagation statistics (e.g., iteration convergence, propagation hops)

## How to apply

Initialize network nodes with binary or continuous seed labels derived from metabolomic enrichment (e.g., genes meeting significance threshold) or candidate gene lists. Execute iterative label-propagation, where at each step each node's label is updated as a weighted average of its neighbors' labels, balancing seed information (via a regularization parameter) with network diffusion. Continue iterations until convergence (or a fixed number of steps, typically 1000+ iterations for large networks). Compute final ranked gene scores reflecting both the propagation confidence and network proximity to the original seeds. Output a ranked list with propagated scores and optionally network statistics (e.g., distance to nearest seed, number of propagation hops).

## Related tools

- **metPropagate** (Primary implementation: integrates metabolomic enrichment (MSEA output) with label propagation on STRING network to prioritize metabolic disease genes) — github.com/emmagraham/metPropagate
- **Label propagation (adapted from Yuto Yamaguchi)** (Core label-propagation algorithm component; implements iterative label diffusion on network) — github.com/yamaguchiyuto/label_propagation
- **STRING database** (Source of gene/protein interaction network (v11 functional interactions used in metPropagate))
- **XCMS / CAMERA** (Upstream metabolomic preprocessing to generate intensity matrices and peak tables fed into MSEA)

## Examples

```
bash label_propagation/run_label_prop_cluster.sh
```

## Evaluation signals

- Propagated scores form a continuous, ranked distribution across all nodes (not binary); zero propagation indicates algorithm failure or disconnected network component.
- Top-ranked genes include original seed genes or their direct network neighbors; seeds should retain high or near-maximal scores post-propagation.
- Network propagation converges within a reasonable number of iterations (typically <1000 for well-connected networks); divergence or oscillation indicates parameter miscalibration.
- Propagated scores correlate with metabolomic signal strength: genes with high enrichment scores in MSEA input should have higher final scores than genes with weak or no enrichment signal.
- Output contains expected columns ('Score.ID', 'Original.Score.ID', candidate gene identifiers) with no NaN or negative scores (depending on algorithm variant).

## Limitations

- Label propagation requires a connected or well-connected network; genes in disconnected components or at network periphery receive minimal signal.
- Performance depends heavily on network quality and completeness; sparse or biased networks (e.g., well-studied proteins over-represented) can propagate biased signals.
- Propagation is unsupervised; no independent validation that propagated scores correspond to true disease causality or functional relevance—metabolomic enrichment signal itself must be validated.
- Requires manual tuning of regularization/convergence parameters; README notes use of .pbs batch scripts, implying iterative runs may be needed.
- For large networks (entire STRING db, >20k genes), computational time and memory can be substantial; no explicit scaling or parallelization documented in README.

## Evidence

- [other] metPropagate implements network-guided propagation of metabolomic information to prioritize metabolic disease genes by propagating seed labels derived from metabolomic data over a gene/protein interaction network.: "metPropagate implements network-guided propagation of metabolomic information to prioritize metabolic disease genes by propagating seed labels derived from metabolomic data over a gene/protein"
- [readme] This section contains code for the label propagation component of metPropagate. It was adapted from Yuto Yamaguchi (https://github.com/yamaguchiyuto/label_propagation).: "This section contains code for the label propagation component of metPropagate. It was adapted from Yuto Yamaguchi (https://github.com/yamaguchiyuto/label_propagation)."
- [other] Initialize label-propagation algorithm with seed labels on network nodes. Execute iterative label-propagation to distribute seed information across connected network nodes. Compute final ranked gene scores reflecting propagation confidence and network proximity to seeds.: "Initialize label-propagation algorithm with seed labels on network nodes. Execute iterative label-propagation to distribute seed information across connected network nodes. Compute final ranked gene"
- [readme] Results of label propagation will populate in integration/results/. File contains final propagated scores for each candidate gene as 'Score.ID' and the original scores for each gene as 'Original.Score.ID'.: "Results of label propagation will populate in integration/results/. File contains final propagated scores for each candidate gene as 'Score.ID' and the original scores for each gene as"
- [readme] graph_files contains input STRING network files (manually placed) - STRING_graph_file_v11_gene_list_functional_entire_db: STRING database downloaded from stringdb.org: "graph_files contains input STRING network files (manually placed) - STRING_graph_file_v11_gene_list_functional_entire_db: STRING database downloaded from stringdb.org"
