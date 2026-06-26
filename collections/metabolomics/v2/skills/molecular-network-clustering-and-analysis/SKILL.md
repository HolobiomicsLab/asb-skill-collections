---
name: molecular-network-clustering-and-analysis
description: Use when after generating candidate transformed structures from biotransformation
  rules and when you have MS/MS spectral feature data that you wish to organize into
  putative molecular families.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3925
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - BAM
  - PROXIMAL2
  - GNN-SOM
  techniques:
  - LC-MS
  - NMR
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-network-clustering-and-analysis

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill constructs spectral similarity networks from untargeted metabolomics MS/MS data, applies graph-based clustering to identify molecular families, and annotates network nodes with predicted structures from biotransformation rules. It is essential for discovering unknown metabolites by connecting structurally related compounds in high-dimensional spectral space.

## When to use

Apply this skill after generating candidate transformed structures from biotransformation rules and when you have MS/MS spectral feature data that you wish to organize into putative molecular families. Use it when you need to annotate unknown features by leveraging spectral similarity and structural relationships predicted by biotransformation networks.

## When NOT to use

- Input spectra are already assigned to known reference compounds with high confidence; targeted annotation is more appropriate.
- MS/MS spectral data are missing or of insufficient quality to compute reliable similarity scores.
- The biotransformation rules module has not been run; candidate structures are not available.

## Inputs

- Candidate transformed structures (SMILES format, from biotransformation rules output)
- MS/MS spectral feature data (MS1/MS2 peak lists with m/z and intensity)
- Spectral similarity metric (cosine similarity or variant)
- Similarity threshold parameter

## Outputs

- Molecular network file (GraphML, JSON, or GXF format)
- Feature annotation table (MS feature → predicted structure(s) and network cluster membership)

## How to apply

Load candidate transformed structures from the biotransformation-rules module output together with MS/MS spectral data. Compute spectral similarity scores (e.g., cosine similarity) between all feature pairs in the dataset. Filter edges using a similarity threshold to retain only high-confidence spectral matches. Apply graph-based clustering or community detection algorithms to identify connected components representing putative molecular families. Annotate each network node with corresponding candidate structures and MS1/MS2 feature associations. Export the molecular network in a standard format (GraphML, JSON, or GXF) and generate a feature annotation table linking each MS feature to predicted structure(s) and network cluster membership.

## Related tools

- **BAM** (Orchestrates biotransformation-based annotation and global molecular networking for structure discovery) — https://github.com/HassounLab/BAM
- **PROXIMAL2** (Generates biotransformation rules and candidate structures used as input to molecular network annotation) — https://github.com/HassounLab/PROXIMAL2
- **GNN-SOM** (Predicts site-of-metabolism and ranks enzymatic products for biotransformation candidate ranking) — https://github.com/HassounLab/GNN-SOM

## Evaluation signals

- Network contains no isolated nodes (every feature either clusters with similar spectra or is annotated with a biotransformation candidate).
- Edges in the network exhibit spectral similarity scores above the defined threshold; no spurious low-confidence matches remain.
- Connected components (molecular families) are non-overlapping and each node is assigned to exactly one cluster.
- Feature annotation table contains valid SMILES/InChI strings for predicted structures and explicit cluster IDs.
- Graph structure validates: degree distribution, modularity, and cluster size distributions are consistent with expected biotransformation family relationships.

## Limitations

- Spectral similarity thresholds are sensitive to MS/MS collision energy and instrumentation; threshold tuning may be required across different datasets.
- Graph-based clustering results depend on the completeness and accuracy of the underlying biotransformation rules; incomplete or incorrect rules will propagate errors into network annotation.
- Molecular families identified by spectral similarity may include structural isomers or unrelated compounds with similar fragmentation patterns; validation against orthogonal data (e.g., retention time, NMR) is recommended.
- The method requires pre-computed MS/MS spectra; data quality issues (low signal-to-noise, contamination) can compromise similarity scoring and clustering.

## Evidence

- [other] Construct a similarity network by computing spectral similarity scores (e.g., cosine similarity or variant thereof) between all feature pairs in the dataset.: "Construct a similarity network by computing spectral similarity scores (e.g., cosine similarity or variant thereof) between all feature pairs"
- [other] Filter edges based on a similarity threshold to retain only high-confidence spectral matches.: "Filter edges based on a similarity threshold to retain only high-confidence spectral matches."
- [other] Apply graph-based clustering or community detection to identify connected components representing putative molecular families.: "Apply graph-based clustering or community detection to identify connected components representing putative molecular families."
- [intro] BAM method uses biotransformation rules and global molecular networking for structure annotation: "BAM method uses biotransformation rules and global molecular networking for structure annotation"
- [other] Export the molecular network in a standard format (e.g., GraphML, JSON, or GXF) and generate a feature annotation table linking each MS feature to its predicted structure(s) and network cluster membership.: "Export the molecular network in a standard format (e.g., GraphML, JSON, or GXF) and generate a feature annotation table linking each MS feature to its predicted structure(s) and network cluster"
