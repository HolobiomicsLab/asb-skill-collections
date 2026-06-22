---
name: mass-spectral-feature-grouping
description: Use when you have untargeted metabolomics MS/MS spectra from multiple features and need to identify which features belong to the same molecular family or are related by biotransformation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - BAM
  - PROXIMAL2
  - GNN-SOM
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

# mass-spectral-feature-grouping

## Summary

Group MS features into molecular families by constructing a similarity network from MS/MS spectral data, filtering edges by similarity threshold, and applying graph-based clustering to identify connected components. This groups features that likely derive from related molecular structures or biotransformation products.

## When to use

You have untargeted metabolomics MS/MS spectra from multiple features and need to identify which features belong to the same molecular family or are related by biotransformation. Use this skill when you want to collapse high-dimensional feature data into interpretable molecular groups before or after structure annotation.

## When NOT to use

- Your input is already a feature table or quantification matrix without MS/MS spectra — you need the actual spectral similarity information.
- You have only targeted quantification data for known metabolites and do not need to discover molecular families.
- MS/MS spectral data are of very low quality or missing for most features, making similarity computation unreliable.

## Inputs

- MS/MS spectral data matrix (feature × m/z intensity pairs)
- Feature metadata (e.g., retention time, precursor m/z, feature ID)
- Similarity threshold parameter (numeric, unitless or %; e.g., 0.5–0.9 for cosine similarity)

## Outputs

- Molecular network in standard graph format (GraphML, JSON, or GXF)
- Cluster/community assignments (feature ID → cluster ID mapping)
- Network node list with cluster membership and optionally candidate structure annotations
- Feature annotation table linking MS features to predicted structures and network cluster membership

## How to apply

Load all MS/MS spectral data for your feature set. Compute spectral similarity scores (e.g., cosine similarity) between all feature pairs to construct a complete similarity network. Filter edges by applying a similarity threshold (e.g., retain only pairs above a cutoff value) to retain only high-confidence spectral matches and reduce noise. Apply graph-based clustering or community detection algorithms (e.g., modularity optimization or connected-component analysis) to partition the filtered network into clusters. Each cluster represents a putative molecular family. Optionally annotate each node in the resulting clusters with candidate structures from biotransformation rule predictions or reference spectral libraries to validate family membership.

## Related tools

- **BAM** (Implements the complete biotransformation-based annotation workflow including global molecular networking for feature grouping and structure discovery) — https://github.com/HassounLab/BAM
- **PROXIMAL2** (Upstream tool used by BAM to generate biotransformation rules and operator sets for candidate structure prediction) — https://github.com/HassounLab/PROXIMAL2
- **GNN-SOM** (Integrated with BAM for site-of-metabolism prediction and ranking of promiscuous enzymatic products) — https://github.com/HassounLab/GNN-SOM

## Evaluation signals

- Network connectivity statistics: verify that the filtered network has expected edge density and connected component size distribution (no single giant component for random data).
- Cluster homogeneity: check that features within the same cluster have spectral similarity scores above the applied threshold, and inter-cluster pairs fall below it.
- Annotation coherence: if candidate structures are available, verify that features in the same cluster are annotated with structures related by plausible biotransformation rules (e.g., oxidation, methylation, conjugation).
- GraphML/JSON schema validation: ensure exported network files conform to the declared graph format and contain required node/edge attributes (node IDs, similarity scores, cluster IDs).
- Feature coverage: verify that all input features appear in the output network and are assigned to exactly one cluster (no orphaned or multiply-assigned features).

## Limitations

- Similarity threshold selection is not fully automated and must be tuned for your spectral data type and quality; inappropriate thresholds can merge unrelated families or fragment true families.
- Clustering quality depends on MS/MS spectral data quality; low signal-to-noise or incomplete fragmentation patterns reduce discriminative power for similarity computation.
- The method is sensitive to the choice of similarity metric (cosine, modified cosine, spectral entropy distance); different metrics may yield different network structures.
- No changelog is provided in the repository, limiting tracking of updates or bug fixes to the networking implementation.
- The skill identifies spectral similarity and graph connectivity but does not directly validate that grouped features arise from the same biological compound or biotransformation product without downstream annotation.

## Evidence

- [other] Construct a similarity network by computing spectral similarity scores (e.g., cosine similarity or variant thereof) between all feature pairs in the dataset.: "Construct a similarity network by computing spectral similarity scores (e.g., cosine similarity or variant thereof) between all feature pairs"
- [other] Filter edges based on a similarity threshold to retain only high-confidence spectral matches.: "Filter edges based on a similarity threshold to retain only high-confidence spectral matches."
- [other] Apply graph-based clustering or community detection to identify connected components representing putative molecular families.: "Apply graph-based clustering or community detection to identify connected components representing putative molecular families."
- [intro] BAM method uses biotransformation rules and global molecular networking for structure annotation: "BAM method uses biotransformation rules and global molecular networking for structure annotation"
- [other] Export the molecular network in a standard format (e.g., GraphML, JSON, or GXF) and generate a feature annotation table: "Export the molecular network in a standard format (e.g., GraphML, JSON, or GXF) and generate a feature annotation table"
