---
name: spectral-similarity-network-construction
description: Use when after acquiring MS/MS spectral data from untargeted metabolomics experiments and having candidate transformed structures from biotransformation rule application.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  tools:
  - BAM
  - PROXIMAL2
  - GNN-SOM
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.4c01565
  title: bam
evidence_spans:
- HassounLab/BAM
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bam
    doi: 10.1021/acs.analchem.4c01565
    title: bam
  dedup_kept_from: coll_bam
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c01565
  all_source_dois:
  - 10.1021/acs.analchem.4c01565
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-similarity-network-construction

## Summary

Construct a similarity network from untargeted metabolomics MS/MS spectral data by computing pairwise spectral similarity scores and filtering edges to retain high-confidence spectral matches. This network serves as the foundation for identifying molecular families and annotating candidate structures in metabolomic discovery workflows.

## When to use

Apply this skill after acquiring MS/MS spectral data from untargeted metabolomics experiments and having candidate transformed structures from biotransformation rule application. Use it when you need to organize large numbers of MS features into putative molecular families based on spectral similarity, as a prerequisite for clustering-based annotation and structure prediction in the BAM workflow.

## When NOT to use

- Input MS data lacks MS/MS fragmentation spectra (MS1-only data requires alternative approaches)
- You need targeted structural annotation without family context (direct database matching is more appropriate)
- Dataset is too small or spectral quality too poor to compute reliable pairwise similarity (network is likely to be disconnected or noise-dominated)

## Inputs

- MS/MS spectral data (feature spectra from untargeted metabolomics analysis)
- Candidate transformed structures from biotransformation rules module
- MS1/MS2 feature identifiers and mass values

## Outputs

- Molecular network file (GraphML, JSON, or GXF format)
- Feature annotation table (linking MS features to predicted structures and network cluster membership)
- Network node-edge representation with spectral similarity scores

## How to apply

Compute spectral similarity scores (e.g., cosine similarity or variant) between all feature pairs in the MS/MS dataset. Filter edges by applying a similarity threshold to retain only high-confidence spectral matches—this threshold should be tuned based on your dataset's quality and the desired specificity/sensitivity balance. Construct a graph representation where nodes are MS features and edges represent spectral similarities passing the threshold. The resulting network is then subjected to graph-based clustering or community detection to identify connected components that represent putative molecular families. Nodes are subsequently annotated with candidate structures from biotransformation rule output and exported in a standard format (GraphML, JSON, or GXF) alongside a feature annotation table linking each MS feature to its network cluster membership.

## Related tools

- **BAM** (Orchestrates the complete biotransformation-based annotation pipeline, with spectral-similarity-network-construction as a core global molecular networking component) — https://github.com/HassounLab/BAM
- **PROXIMAL2** (Upstream biotransformation rule generation and candidate structure prediction feeding into network annotation) — https://github.com/HassounLab/PROXIMAL2
- **GNN-SOM** (Graph neural network–based site-of-metabolism prediction for ranking and refining candidate structures in the molecular network) — https://github.com/HassounLab/GNN-SOM

## Evaluation signals

- All MS features in the input dataset are represented as nodes in the output network graph
- Pairwise spectral similarity scores are computed for all feature pairs and stored with edges above the threshold
- Connected components (molecular families) are identifiable in the network and correspond to coherent mass/chemical space clusters
- Feature annotation table contains no missing entries and correctly links each MS feature to its candidate structure(s) and assigned network cluster
- Network file parses correctly in standard graph visualization/analysis tools (Cytoscape, NetworkX, etc.) with valid node and edge attributes

## Limitations

- Spectral similarity threshold is dataset-dependent and must be tuned empirically; no universal threshold is provided in the source material
- Quality and completeness of the output annotation depend critically on the correctness and coverage of the upstream biotransformation rules
- Spectral similarity alone does not guarantee structural correctness; candidates must be validated by additional evidence (MS/MS fragmentation patterns, chemical plausibility, reference spectra)
- The method assumes reproducible MS/MS fragmentation patterns; highly variable or noisy spectra may produce unreliable similarity scores and fragmented networks

## Evidence

- [other] Construct a similarity network by computing spectral similarity scores (e.g., cosine similarity or variant thereof) between all feature pairs in the dataset.: "Construct a similarity network by computing spectral similarity scores (e.g., cosine similarity or variant thereof) between all feature pairs in the dataset."
- [other] Filter edges based on a similarity threshold to retain only high-confidence spectral matches.: "Filter edges based on a similarity threshold to retain only high-confidence spectral matches."
- [other] Apply graph-based clustering or community detection to identify connected components representing putative molecular families.: "Apply graph-based clustering or community detection to identify connected components representing putative molecular families."
- [other] Annotate each network node with the corresponding candidate structures from the biotransformation rules output and associate with MS1/MS2 features.: "Annotate each network node with the corresponding candidate structures from the biotransformation rules output and associate with MS1/MS2 features."
- [other] BAM implements a method that combines biotransformation rules and global molecular networking as components for molecular structure discovery from untargeted metabolomics data.: "BAM implements a method that combines biotransformation rules and global molecular networking as components for molecular structure discovery from untargeted metabolomics data."
