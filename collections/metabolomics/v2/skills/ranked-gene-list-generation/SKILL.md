---
name: ranked-gene-list-generation
description: Use when you have identified significant differential metabolites (DAMs) from metabolomic profiling, mapped them to genes via enrichment (e.g., MSEA), and possess a gene/protein interaction network (e.g., STRING).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0602
  tools:
  - metPropagate
  - label_propagation module (adapted from Yuto Yamaguchi)
  - STRING database
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ranked-gene-list-generation

## Summary

Generate a prioritized ranked list of candidate genes by propagating metabolomic-derived seed labels across a gene/protein interaction network using label propagation, producing scored genes ordered by network proximity and propagation confidence to metabolomic hits.

## When to use

You have identified significant differential metabolites (DAMs) from metabolomic profiling, mapped them to genes via enrichment (e.g., MSEA), and possess a gene/protein interaction network (e.g., STRING). Use this skill when you need to prioritize which candidate genes from exome/WES data are most likely disease-relevant by leveraging the metabolomic signal propagated through protein interaction topology.

## When NOT to use

- The input metabolomic data has not been processed through enrichment analysis (MSEA or equivalent) to map individual metabolites to genes; raw peak lists alone are insufficient.
- No protein interaction network is available or the network does not contain your candidate genes (label propagation requires connected or near-connected network topology to be effective).
- You seek to rank genes by metabolomic signal alone without leveraging network structure; a simpler gene-level filtering or sorting by enrichment p-value is more appropriate.

## Inputs

- Gene/protein interaction network (e.g., STRING database file with edge list and gene-to-node-id mapping)
- Metabolomic enrichment file (gene-level DAM enrichment scores, e.g., output from MSEA)
- Candidate gene list (from exome sequencing or variant calling, e.g., Exomisher output)

## Outputs

- Ranked gene list with propagated scores (file containing gene IDs, final propagated scores, and original metabolomic scores)
- Label propagation statistics (convergence information, network coverage metrics)

## How to apply

Initialize a label-propagation algorithm with binary seed labels (1 for metabolomically enriched genes, 0 elsewhere) on nodes of a STRING protein interaction network. Execute iterative label propagation to distribute metabolomic seed information across connected network nodes, allowing signals to flow through interaction edges. The algorithm computes final propagated scores for each node reflecting both the original seed strength and network distance to enriched genes. Candidate genes from WES/exome data are then ranked by their final propagated scores, with higher scores indicating stronger integration of metabolomic evidence through network proximity. Output includes the ranked gene list with propagated scores and optionally network propagation statistics (e.g., number of iterations, convergence metrics).

## Related tools

- **metPropagate** (Implements network-guided label propagation to propagate metabolomic seed labels across gene/protein interaction network and produce ranked gene scores for disease gene prioritization) — github.com/emmagraham/metPropagate
- **label_propagation module (adapted from Yuto Yamaguchi)** (Core iterative label propagation algorithm that distributes seed information across network nodes) — github.com/emmagraham/metPropagate
- **STRING database** (Provides pre-built gene/protein interaction network used as the propagation substrate)

## Examples

```
bash integration/run_label_prop_cluster.sh (after editing sample_name variable and placing enrichment file in integration/enrichment_files/ and candidate genes in integration/wes_files/)
```

## Evaluation signals

- Verify that all seed genes (metabolomically enriched genes) have final propagated scores ≥ their original enrichment scores, indicating information preservation.
- Check that the number of genes with non-zero propagated scores is greater than the number of seed genes (indicating network propagation spread), unless the network is disconnected.
- Confirm that candidate genes directly connected to seed genes in the network receive higher propagated scores than genes at greater network distance, validating topological influence.
- Validate that output file structure matches specification: each row contains a unique gene ID, its final propagated score, and its original metabolomic score.
- Ensure label propagation convergence is achieved within a reasonable number of iterations (typically < 100 for well-connected networks) and log convergence diagnostics.

## Limitations

- Label propagation performance depends heavily on network coverage and connectivity; genes not present in the STRING network or in disconnected network components will not receive propagated scores.
- Metabolomic seed label quality directly impacts output ranking; noisy or false-positive metabolomic enrichment will propagate spurious signals through the network.
- The method assumes that protein interaction topology reflects metabolic pathway relevance, which may not hold for all metabolic diseases or in presence of missing interactions.
- Computational cost scales with network size; very large networks (>50,000 nodes) may require memory optimization or subgraph extraction.
- Label propagation parameters (damping factor, convergence threshold, number of iterations) are not explicitly tuned in the metPropagate documentation and may require empirical optimization for specific networks.

## Evidence

- [other] metPropagate implements network-guided propagation of metabolomic information to prioritize metabolic disease genes by propagating seed labels derived from metabolomic data over a gene/protein interaction network.: "metPropagate implements network-guided propagation of metabolomic information to prioritize metabolic disease genes by propagating seed labels derived from metabolomic data over a gene/protein"
- [other] Execute iterative label-propagation to distribute seed information across connected network nodes. Compute final ranked gene scores reflecting propagation confidence and network proximity to seeds.: "Execute iterative label-propagation to distribute seed information across connected network nodes. Compute final ranked gene scores reflecting propagation confidence and network proximity to seeds."
- [readme] This section contains code for the label propagation component of metPropagate. It was adapted from Yuto Yamaguchi: "This section contains code for the label propagation component of metPropagate. It was adapted from Yuto Yamaguchi"
- [readme] integration/graph_files contains input STRING network files: "integration/graph_files contains input STRING network files (manually placed)"
- [readme] LPA_output contains the post-propagation node scores: "LPA_output contains the post-propagation node scores (automatically generated)"
- [readme] File contains final propagated scores for each candidate gene as "Score.ID" and the original scores for each gene as "Original.Score.ID".: "File contains final propagated scores for each candidate gene as "Score.ID" and the original scores for each gene as "Original.Score.ID"."
