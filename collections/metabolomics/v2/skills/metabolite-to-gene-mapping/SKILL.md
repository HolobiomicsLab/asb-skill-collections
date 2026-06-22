---
name: metabolite-to-gene-mapping
description: Use when you have metabolomic data (e.g., from LC-MS or GC-MS comparing patient to controls) showing differential abundant metabolites (DAMs), candidate genes from exome sequencing or variant calling, and access to a protein–protein or gene–gene interaction network (e.g., STRING).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - metPropagate
  - XCMS
  - STRING Database v11
  - HMDB
  - Exomiser
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

# Reconstruct the label-propagation algorithm for prioritizing metabolic disease genes

## Summary

Map differential abundant metabolites (DAMs) to genes via enrichment scoring, then propagate metabolomic seed labels across a gene/protein interaction network to generate ranked scores for metabolic disease gene prioritization. This skill bridges metabolomic discovery (dysregulated metabolites) to genomic interpretation (candidate disease genes) by network diffusion.

## When to use

You have metabolomic data (e.g., from LC-MS or GC-MS comparing patient to controls) showing differential abundant metabolites (DAMs), candidate genes from exome sequencing or variant calling, and access to a protein–protein or gene–gene interaction network (e.g., STRING). Use this skill when you need to rank candidate genes by their proximity to metabolomic signals in the network, especially in rare metabolic disease diagnosis where metabolomic hits provide orthogonal evidence beyond genomic burden alone.

## When NOT to use

- Input is already a pre-ranked gene list without underlying metabolomic data — label propagation adds value only when seeded with strong metabolomic signals.
- Metabolomic data quality is poor (e.g., >50% missing intensity values, low metabolite identification rate <20% of features matched to HMDB) — propagation will amplify noise.
- No interaction network is available or the network is extremely sparse (<<1% edge density) — label propagation requires sufficient network connectivity to diffuse metabolomic information.

## Inputs

- ESI+/ESI− mode metabolomics intensity matrices (CSV: sample_ID × m/z feature)
- Peak tables from XCMS or equivalent preprocessing (m/z, retention time, p-value)
- HMDB metabolite database (CSV: exact mass, HMDB ID, gene associations)
- STRING protein–protein interaction network (node_id, gene_name, edge_score)
- Candidate gene list from exome sequencing or variant prioritization (e.g., Exomiser output CSV)

## Outputs

- Per-gene metabolomic enrichment scores (CSV: gene, DAM_count, MSEA_pvalue, enrichment_score)
- Binary seed label file for label propagation (per-gene: gene_id, label ∈ {0, 1})
- Propagated gene scores after label diffusion (CSV: gene_id, original_score, propagated_score, rank)
- Network propagation statistics (iteration count, convergence threshold met, label distribution)

## How to apply

First, convert raw metabolomic intensity matrices (ESI+/ESI− mode) through log or linear scaling and exact mass matching against HMDB to identify significant features and map them to metabolites. Next, perform metabolite set enrichment analysis (MSEA) to compute per-gene enrichment scores reflecting the concentration of DAMs associated with each gene. Then, construct binary seed labels: genes with significant metabolomic enrichment receive label 1 (metabolomic hits), others receive 0. Initialize a label-propagation algorithm on the STRING network graph (or equivalent PPI) seeded with these labels. Execute iterative propagation (typically 100 iterations or until convergence) where each node's label is updated as a weighted average of its neighbors' labels, weighted by network edge confidence. Finally, compute final ranked gene scores reflecting both the original metabolomic signal strength and network-guided diffusion, ranking candidates by propagated score. This approach ensures that genes not directly hit by metabolomic data but closely connected to metabolomic hits are elevated in ranking.

## Related tools

- **metPropagate** (Complete implementation of metabolomic processing, label propagation, and gene ranking; orchestrates MSEA, label construction, and network diffusion) — https://github.com/emmagraham/metPropagate
- **XCMS** (Untargeted LC-MS/GC-MS peak detection and feature alignment to produce intensity matrices and peak tables input to metabolomic processing pipeline)
- **STRING Database v11** (Provides gene/protein interaction network (nodes: genes, edges: functional associations with confidence scores) used as substrate for label propagation)
- **HMDB** (Reference metabolite database for exact mass matching of m/z features to metabolite IDs and retrieval of gene–metabolite associations for enrichment scoring)
- **Exomiser** (Produces candidate gene lists from variant calls; output format (CSV) directly compatible as input to metPropagate integration pipeline)

## Examples

```
bash integration/run_label_prop_cluster.sh; outputs will be in integration/results/ containing propagated and original gene scores
```

## Evaluation signals

- Metabolomic feature-to-metabolite matching rate: ≥20% of input m/z values successfully mapped to HMDB entries (indicative of data quality and reference database coverage).
- Seed label distribution: ≥5 genes with label=1 (metabolomic hits) to provide meaningful network propagation; ≤100% sparsity (all genes labeled 0) suggests weak metabolomic signal.
- Label propagation convergence: achieved within maximum iteration limit and label update magnitude <threshold (typically 1e-6) between consecutive iterations.
- Output gene ranking schema: propagated_score ≥ original_score for all genes (label propagation should not decrease ranks, only reorder); presence of original_score and propagated_score columns enabling comparison.
- Network coverage: ≥80% of input candidate genes present in STRING graph (unmapped genes cannot be scored via propagation and should be flagged).

## Limitations

- Label propagation performance depends critically on network quality and coverage; sparse or incomplete PPI networks (e.g., missing tissue-specific interactions) may fail to connect metabolomic hits to true disease genes.
- Metabolomic enrichment scoring (MSEA) assumes metabolites are reliably identified; exact mass matching alone is ambiguous for isobaric or isomeric metabolites, potentially yielding spurious gene–metabolite associations.
- The method assumes that genes associated with differential abundant metabolites are enriched for disease causality, which may not hold if DAMs are secondary or adaptive responses rather than primary perturbations.
- No changelog documented; version tracking and reproducibility depend on fixing STRING database version (README specifies STRING v11) and HMDB version (README mentions v4) to maintain exact mass matching and network structure.

## Evidence

- [other] metPropagate implements network-guided propagation of metabolomic information to prioritize metabolic disease genes by propagating seed labels derived from metabolomic data over a gene/protein interaction network.: "metPropagate implements network-guided propagation of metabolomic information to prioritize metabolic disease genes by propagating seed labels derived from metabolomic data over a gene/protein"
- [other] Initialize label-propagation algorithm with seed labels on network nodes. 3. Execute iterative label-propagation to distribute seed information across connected network nodes. 4. Compute final ranked gene scores reflecting propagation confidence and network proximity to seeds.: "Initialize label-propagation algorithm with seed labels on network nodes. Execute iterative label-propagation to distribute seed information across connected network nodes. Compute final ranked gene"
- [readme] The XCMS code used to generate these files is commented out in the first section of the preprocessing.R file. ... neg_mode or pos_mode/linear_raw_intensities.csv ... neg_mode or pos_mode/negative(or positive)_linear_mode_msea_genebig_allpeaks.csv (enrichment of DAMs for all genes in HMDB, given input of linear scaled intensity matrix from ESI-/+ mode data only): "linear scaled input intensity matrix from ESI-/+ mode data only) ... neg_mode or pos_mode/negative(or positive)_linear_mode_msea_genebig_allpeaks.csv (enrichment of DAMs for all genes in HMDB"
- [readme] This section contains code for the label propagation component of metPropagate. It was adapted from Yuto Yamaguchi: "This section contains code for the label propagation component of metPropagate"
- [readme] STRING_graph_file_v11_gene_list_functional_entire_db: STRING database downloaded from stringdb.org: "STRING_graph_file_v11_gene_list_functional_entire_db: STRING database downloaded from stringdb.org"
- [readme] intermediate_label_file_sampleA is an example of a label file that is input to label propagation: "intermediate_label_file_sampleA is an example of a label file that is input to label propagation"
- [readme] Results of label propagation will populate in *integration/results/*. File contains final propagated scores for each candidate gene as "Score.ID" and the original scores for each gene as "Original.Score.ID".: "File contains final propagated scores for each candidate gene as "Score.ID" and the original scores for each gene as "Original.Score.ID""
