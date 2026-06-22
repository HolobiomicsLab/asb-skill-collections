---
name: network-proximity-scoring
description: Use when you have (1) metabolomic hits (DAMs or enriched metabolites) mapped to seed genes, (2) a protein–protein or gene interaction network (e.g., STRING), and (3) a set of candidate disease genes that need ranking by their functional proximity to metabolomic evidence.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0209
  tools:
  - metPropagate
  - STRING database
  - label_propagation (Yuto Yamaguchi)
  - MSEA (metabolomic set enrichment analysis)
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
---

# network-proximity-scoring

## Summary

Score genes by their network proximity to metabolomic seed labels using iterative label propagation over a gene/protein interaction network. This skill prioritizes metabolic disease genes by distributing metabolomic evidence across connected network nodes, producing ranked scores that reflect both propagation confidence and topological distance from seed hits.

## When to use

Apply this skill when you have (1) metabolomic hits (DAMs or enriched metabolites) mapped to seed genes, (2) a protein–protein or gene interaction network (e.g., STRING), and (3) a set of candidate disease genes that need ranking by their functional proximity to metabolomic evidence. Use it to convert sparse metabolomic signals into genome-wide prioritized candidate lists by leveraging network structure.

## When NOT to use

- Input metabolomic data are not yet mapped to genes—perform metabolomic enrichment (e.g., MSEA, pathway annotation) first.
- No validated protein–protein or gene interaction network is available for your organism or disease context; network quality directly impacts output reliability.
- Candidate gene set is already prioritized by orthogonal high-confidence evidence (e.g., rare pathogenic variants); network propagation may dilute rather than enhance ranking.

## Inputs

- gene/protein interaction network (e.g., STRING graph file with edges and node IDs)
- seed label file (per-gene metabolomic enrichment scores or binary hits, mapped to network node IDs)
- candidate gene list (optional; may be from exome sequencing or prior QC)

## Outputs

- ranked gene scores (per-gene propagated label confidence)
- network propagation statistics (iterations, convergence metric)
- post-propagation node scores file (e.g., LPA_output format)

## How to apply

Initialize label propagation by assigning metabolomic-derived seed labels (e.g., enrichment scores or binary hits) to corresponding nodes in a gene/protein interaction network (e.g., STRING database v11). Execute iterative label-propagation algorithm that distributes seed information across connected nodes, typically using a Laplacian-based or random-walk framework. Iterate until convergence or a fixed number of steps. Compute final ranked gene scores reflecting the accumulated propagation signal and network distance from seeds. Output scores for each candidate gene, optionally filtering by a score threshold or ranking cutoff. The rationale is that genes proximal to metabolomic seeds in network topology are more likely to participate in the same perturbed pathway.

## Related tools

- **metPropagate** (Complete implementation of metabolomic-guided label propagation for disease gene prioritization; integrates metabolomic processing, label file generation, and network propagation) — https://github.com/emmagraham/metPropagate
- **STRING database** (Source of gene/protein interaction network (v11 recommended); provides node IDs and functional interaction edges)
- **label_propagation (Yuto Yamaguchi)** (Core algorithm implementation adapted within metPropagate for iterative label distribution across network nodes) — https://github.com/yamaguchiyuto/label_propagation
- **MSEA (metabolomic set enrichment analysis)** (Upstream tool to map metabolomic features (DAMs) to genes/pathways and generate enrichment scores used as seed labels)

## Examples

```
bash integration/label_propagation/run_label_prop_cluster.sh (after editing sample_name variable and placing metabolomic enrichment file in integration/enrichment_files/)
```

## Evaluation signals

- Propagated scores are continuous, non-negative, and highest at or near seed nodes; scores decay with network distance.
- Convergence: iterative propagation reaches a stable state (e.g., L2 norm of score deltas < threshold) within a reasonable iteration count.
- Candidate genes with high propagated scores are significantly enriched in genes known to be associated with metabolic disease or the disease of interest (e.g., via pathway databases, literature, or functional validation).
- Output file structure matches expected schema: each row is a gene/node with Original.Score and Score.ID columns; no missing values for candidates in the input network.
- Rank stability: re-running with minor perturbations (e.g., ±5% seed label noise, subsampled network edges) produces similar top-10 or top-20 rankings.

## Limitations

- Label propagation is sensitive to network quality and coverage; sparse or incorrect edges reduce scoring reliability. STRING v11 functional interactions may miss tissue-specific or rare isoform-level links.
- Seed label quality directly affects output: noisy or false-positive metabolomic hits will propagate spurious scores genome-wide. Rigorous statistical filtering (e.g., FDR correction, effect size thresholds) of metabolomic data upstream is critical.
- Algorithm requires convergence tuning (iteration count, damping factor); default parameters may not suit all network sizes or seed distributions. No principled stopping criterion is provided in the README.
- Output reflects network topology and seed information only; genes proximal in network but functionally unrelated to the metabolic phenotype may be false positives. Orthogonal validation (e.g., functional assays, clinical data) is recommended.
- Scalability: very large networks (>20k nodes) or highly connected hubs can slow convergence; performance on organism-specific networks beyond human STRING is not discussed.

## Evidence

- [other] metPropagate implements network-guided propagation of metabolomic information to prioritize metabolic disease genes by propagating seed labels derived from metabolomic data over a gene/protein interaction network.: "metPropagate implements network-guided propagation of metabolomic information to prioritize metabolic disease genes by propagating seed labels derived from metabolomic data over a gene/protein"
- [other] Initialize label-propagation algorithm with seed labels on network nodes. Execute iterative label-propagation to distribute seed information across connected network nodes. Compute final ranked gene scores reflecting propagation confidence and network proximity to seeds.: "Initialize label-propagation algorithm with seed labels on network nodes. Execute iterative label-propagation to distribute seed information across connected network nodes. Compute final ranked gene"
- [readme] This section contains code for the label propagation component of metPropagate. It was adapted from Yuto Yamaguchi (https://github.com/yamaguchiyuto/label_propagation).: "This section contains code for the label propagation component of metPropagate. It was adapted from Yuto Yamaguchi (https://github.com/yamaguchiyuto/label_propagation)."
- [readme] STRING_graph_file_v11_gene_list_functional_entire_db: STRING database downloaded from stringdb.org: "STRING_graph_file_v11_gene_list_functional_entire_db: STRING database downloaded from stringdb.org"
- [readme] File contains final propagated scores for each candidate gene as 'Score.ID' and the original scores for each gene as 'Original.Score.ID'.: "File contains final propagated scores for each candidate gene as 'Score.ID' and the original scores for each gene as 'Original.Score.ID'."
