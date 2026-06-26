---
name: gene-network-seed-initialization
description: Use when when you have metabolomic enrichment scores for genes (e.g.,
  from MSEA analysis comparing a patient to controls) and need to prepare them as
  seed labels for label propagation over a gene/protein interaction network.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0209
  tools:
  - metPropagate
  - MSEA (Metabolite Set Enrichment Analysis)
  - STRING database
  license_tier: restricted
  provenance_tier: literature
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

# gene-network-seed-initialization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Initialize a label-propagation algorithm by mapping metabolomic hits (differentially abundant metabolites) to genes and seeding network nodes with these labels prior to propagation. This converts raw metabolomic enrichment signals into a ranked seed set that guides network-based disease gene prioritization.

## When to use

When you have metabolomic enrichment scores for genes (e.g., from MSEA analysis comparing a patient to controls) and need to prepare them as seed labels for label propagation over a gene/protein interaction network. Specifically, when metabolomic data has been processed into per-gene enrichment values and you want to propagate this signal across network neighbors to discover novel disease-associated genes.

## When NOT to use

- Metabolomic enrichment data have not yet been computed (e.g., raw intensity matrix only); use the metabolomic processing pipeline first.
- Network nodes are already pre-labeled from a different data source and you need to merge or reweight — consider a multi-source label fusion step instead.
- You are working with non-network-based gene prioritization (e.g., variant filtering by burden or annotation) where label initialization does not apply.

## Inputs

- Metabolomic enrichment file (CSV): per-gene DAM enrichment scores and p-values from MSEA analysis
- Gene interaction network (e.g., STRING database file)
- Gene-to-network-node ID mapping file
- Candidate gene list (optional, to filter seed space)

## Outputs

- Label file (intermediate): per-node seed labels formatted for label-propagation input
- Initialization summary: count and distribution of seeded vs. unseeded nodes, label statistics

## How to apply

Extract per-gene metabolomic enrichment scores from MSEA output (e.g., linear_msea_genebig_allpeaks_combined.csv, containing DAM enrichment for all HMDB-mapped genes). Map these enrichment values to nodes in a STRING protein interaction network (using gene-to-node ID mapping). Create binary or weighted seed labels: genes with significant metabolomic signal receive non-zero labels (e.g., derived from enrichment p-values or fold-changes), while non-significant genes receive zero labels. Initialize the label-propagation algorithm with these per-node labels before iterative propagation. The seed label quality directly impacts final ranked gene scores, so filter metabolomic hits using consistent thresholds (e.g., FDR-corrected significance) and verify gene-to-network mapping completeness.

## Related tools

- **metPropagate** (Integrated pipeline that performs label-propagation given initialized seed labels; encapsulates this skill as part of the full workflow) — https://github.com/emmagraham/metPropagate
- **MSEA (Metabolite Set Enrichment Analysis)** (Generates per-gene DAM enrichment scores that serve as input to seed label generation)
- **STRING database** (Source of gene/protein interaction network used to map seeds to nodes)

## Evaluation signals

- All genes in the enrichment file map to network node IDs; check for unmapped gene count and report mapping coverage (ideally >90%).
- Seed label distribution is non-trivial: verify that >10% of network nodes receive non-zero labels and label values span a meaningful range (not all identical).
- Intermediate label file format matches expected structure for label-propagation input (one node ID and label value per row, with header).
- Seed labels are derived from consistent statistical thresholds (e.g., FDR < 0.05); document threshold choice and report number of genes passing it.
- Final propagated scores are higher on average in seeded nodes compared to unseeded nodes, confirming that seeds have influenced propagation.

## Limitations

- Seed label quality depends entirely on the sensitivity and specificity of the upstream metabolomic enrichment analysis; false positives in MSEA will corrupt seed initialization.
- Gene-to-network mapping is limited by coverage: genes in the enrichment file not present in the STRING network cannot be seeded, reducing signal transmission to unmapped regions.
- Choice of enrichment threshold (e.g., p-value cutoff, fold-change minimum) is not data-driven and may require manual calibration; no automated threshold selection is provided.
- Label-propagation results are sensitive to seed label magnitude; normalization of enrichment scores to a consistent scale is recommended but not automated.

## Evidence

- [readme] Load metabolomic enrichment and network mapping; create seed labels; initialize label-propagation: "label_files contains per-gene label files based on metabolomic enrichment data used as input to label propagation (automatically generated)"
- [readme] Enrichment values from MSEA are the source of seed signals: "negative(or positive)_linear_mode_msea_genebig_allpeaks.csv (enrichment of DAMs for all genes in HMDB, given input of linear scaled intensity matrix from ESI-/+ mode data only)"
- [other] Network node seeding is explicit and required before propagation: "Initialize label-propagation algorithm with seed labels on network nodes"
- [readme] STRING network and mapping files are essential infrastructure: "STRING_graph_file_v11_gene_list_functional_entire_db: STRING database downloaded from stringdb.org; STRING_graph_file_v11_gene_to_nodeid_mapping_functional_entire_db: node_id to gene name mapping file"
- [readme] Workflow step explicitly converts enrichment to label files: "Move output file named linear_msea_genebig_allpeaks_combined.csv in METABOLOMIC_PROCESSING_PIPELINE/output/ to integration/enrichment_files. Rename it samplename_enrichment_file.csv"
