---
name: feature-similarity-network-construction
description: Use when you have a filtered MS-DIAL peak list (post-generic filtering,
  containing m/z, retention time, and peak intensity metrics) and need to identify
  groups of co-eluting or structurally similar features before extracting parental
  signals or annotating metabolites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0360
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MS-CleanR
  - MS-DIAL
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.0c01594
  title: MS-CleanR
evidence_spans:
- MS-CleanR use as input MS-DIAL peak list processed in data dependent analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_cleanr_cq
    doi: 10.1021/acs.analchem.0c01594
    title: MS-CleanR
  dedup_kept_from: coll_ms_cleanr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c01594
  all_source_dois:
  - 10.1021/acs.analchem.0c01594
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-similarity-network-construction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct a feature similarity network from LC-MS peak lists by computing pairwise similarities based on MS-DIAL peak character estimation (peak shape and chromatographic properties), then apply community detection to identify feature clusters prior to parental signal extraction. This skill bridges raw peak detection and downstream annotation by grouping related signals that likely derive from the same metabolite.

## When to use

Apply this skill when you have a filtered MS-DIAL peak list (post-generic filtering, containing m/z, retention time, and peak intensity metrics) and need to identify groups of co-eluting or structurally similar features before extracting parental signals or annotating metabolites. Use it specifically when MS/MS data are available (DDA or DIA mode) and you want to collapse redundant features into clusters based on chromatographic and spectral shape similarities rather than treating each peak independently.

## When NOT to use

- Input peak list contains only MS1 data without MS/MS spectra — MS-CleanR will crash in the first step if MS/MS is absent.
- Features are already annotated and merged into a final metabolite list — re-clustering risks losing annotation confidence.
- Peak list has not undergone generic filtering (blank subtraction, RSD thresholding, mass defect filtering) — noisy or artifact peaks will distort similarity calculations.

## Inputs

- Filtered MS-DIAL peak list (m/z, retention time, peak intensity, MS/MS spectra)
- Sample class metadata (for optional PI/NI mode merging)
- MS-DIAL peak character estimation parameters (shape similarity thresholds)

## Outputs

- Feature similarity network (graph object or adjacency matrix)
- Clustered feature table with cluster IDs assigned to all peaks
- Community detection results (modularity scores, cluster membership)
- Optional merged PI/NI mode cluster annotations

## How to apply

Load the filtered MS-DIAL peak list and apply the MS-DIAL peak character estimation algorithm to compute feature-to-feature similarity based on peak shape characteristics and chromatographic co-elution behavior. Construct a feature similarity network (graph) where nodes are peaks and edge weights are similarity scores. Apply multi-level optimization of the modularity algorithm to detect communities (clusters) within this network, assigning each feature a cluster ID. Optionally, if both positive and negative ionization modes are present, merge PI and NI mode clusters using the same modularity algorithm. Export the resulting clustered feature table with cluster membership annotations for use in the subsequent parental signal extraction step.

## Related tools

- **MS-DIAL** (Provides peak character estimation algorithm and peak detection; must be v4.00 or higher) — http://prime.psc.riken.jp/compms/index.html
- **MS-CleanR** (Orchestrates feature similarity network construction and modularity-based clustering) — https://github.com/eMetaboHUB/MS-CleanR

## Evaluation signals

- All features in the input peak list are assigned a cluster ID; no features are orphaned.
- Cluster sizes follow expected metabolite complexity (e.g., adducts, isotopes, fragments typically cluster with m/z spacing and retention time overlap < 0.2 min).
- Modularity scores are ≥ 0.3, indicating non-random community structure in the feature network.
- Clustered features show concordant MS/MS fragmentation patterns and peak shapes within each cluster (checked via manual inspection or cosine similarity of spectra).
- If PI and NI modes are merged, cluster sizes increase proportionally and PI/NI pairs (e.g., [M+H]+ / [M−H]−) are co-assigned.

## Limitations

- Requires at least one MS/MS spectrum per feature; MS1-only data will cause failure. (README: 'All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash.')
- Feature clustering is sensitive to peak character estimation parameters and modularity algorithm settings; suboptimal tuning may over-fragment or over-merge clusters.
- Active development of MS-CleanR has halted; future MS-DIAL 5.x versions integrate parts of this functionality but MS-CleanR itself will not receive updates. (README: 'Since the active development of MSDial 5.x and the integration of a part of MScleanR, this tool will no longer be maintained.')
- Sample names and class labels must not contain spaces or hyphens, and class names must be more than one letter, or clustering may fail or produce incorrect ionization mode merging.

## Evidence

- [other] Apply MS-DIAL peak character estimation algorithm to compute feature similarity based on peak shape and chromatographic properties: "Apply MS-DIAL peak character estimation algorithm to compute feature similarity based on peak shape and chromatographic properties."
- [other] Construct a feature similarity network and apply multi-level optimization of modularity algorithm to identify feature clusters: "Construct a feature similarity network and apply multi-level optimization of modularity algorithm to identify feature clusters."
- [other] Optionally merge positive ionization mode (PI) and negative ionization mode (NI) clusters if both modes are present: "Optionally, MS-CleanR can merge PI and NI mode during this step"
- [readme] All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash.: "All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash."
- [readme] Feature clustering method based on MS-DIAL peak character estimation algorithm followed by parental signal extraction using multi-level optimization of modularity algorithm: "feature clustering method based on MS-DIAL peak character estimation algorithm followed by parental signal extraction using multi-level optimization of modularity algorithm"
