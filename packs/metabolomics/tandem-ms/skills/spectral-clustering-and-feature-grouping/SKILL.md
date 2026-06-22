---
name: spectral-clustering-and-feature-grouping
description: Use when you have raw MS/MS feature data with m/z, retention time, and fragmentation spectra from an untargeted metabolomics experiment, and you need to annotate reaction-derived metabolites of xenobiotics without relying on a priori targeted methods.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0718
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2258
  tools:
  - tidyverse
  - CluMSID
  - CluMSIDdata
  - grid
  - OrgMassSpecR
  - pheatmap
  - reshape2
  - MSMSsim
  - msentropy
  - readxl
  - MSDial
  - Biotransformer
  techniques:
  - CE-MS
  - tandem-MS
derived_from:
- doi: 10.1021/acs.est.5c08558
  title: CMDN
evidence_spans:
- tidyverse
- CluMSID
- CluMSIDdata
- grid
- OrgMassSpecR
- pheatmap
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmdn_cq
    doi: 10.1021/acs.est.5c08558
    title: CMDN
  dedup_kept_from: coll_cmdn_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.est.5c08558
  all_source_dois:
  - 10.1021/acs.est.5c08558
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-clustering-and-feature-grouping

## Summary

Groups MS features by fragmentation pattern similarity and spectral entropy to propagate metabolite annotations across co-eluting or structurally related compounds in untargeted metabolomics. This is the core step in the CMDN pipeline that enables high-throughput xenobiotic metabolite discovery by clustering unknown features and assigning them to reaction pathways via reference spectra.

## When to use

You have raw MS/MS feature data with m/z, retention time, and fragmentation spectra from an untargeted metabolomics experiment, and you need to annotate reaction-derived metabolites of xenobiotics without relying on a priori targeted methods. Use this skill when you have aligned features from MSDial or similar tools and want to group features that share fragmentation characteristics so that a single high-confidence annotation can be propagated to structurally or biotransformationally related unknowns.

## When NOT to use

- Input is already a high-confidence, manually curated metabolite list — clustering will add noise.
- Fragmentation spectra are absent or extremely low quality (few fragments per precursor m/z) — MSMSsim and entropy calculations will be uninformative.
- You are working with targeted (SRM/MRM) data where features are pre-selected — spectral clustering is designed for discovery-mode untargeted data.

## Inputs

- Aligned MS feature table (m/z, retention time, peak intensity across samples)
- MS/MS fragmentation spectra for each feature (in mzML, netCDF, or text format compatible with MSDial 4.80)
- Reference MS/MS spectral library or xenobiotic reaction database
- Sample metadata (sample type, treatment group, replicate identifiers)

## Outputs

- Feature cluster assignments with cluster IDs and member counts
- Annotated feature table with metabolite identities, reaction pathway labels, and cluster membership
- Fragmentation similarity scores and spectral entropy values per feature
- Heatmap visualizations of feature clusters and annotation confidence
- Reaction pathway metadata (e.g., parent compound → Phase I/II product mass shifts)

## How to apply

Load aligned feature data (m/z, RT, MS/MS spectra) using tidyverse and readxl. Apply CluMSID with default clustering parameters to group features by fragmentation pattern similarity. Compute fragmentation similarity scores between each unknown feature cluster and reference spectra from a xenobiotic reaction database using MSMSsim. Calculate spectral entropy using msentropy for each cluster to assess fragment complexity and assign confidence to annotations. Match cluster centroids to exact masses using OrgMassSpecR and propagate metabolite identities within clusters based on highest-confidence hits. Visualize clusters and reaction pathway assignments using pheatmap and grid to confirm biological coherence (e.g., expected mass differences for phase I/II reactions) before exporting the final annotated feature table.

## Related tools

- **CluMSID** (Performs feature clustering by fragmentation pattern similarity and propagates annotations within clusters) — https://github.com/LeaveMeNotTonight/CMDN
- **MSMSsim** (Computes fragmentation pattern similarity scores between unknown feature clusters and reference spectra) — https://github.com/LeaveMeNotTonight/CMDN
- **msentropy** (Calculates spectral entropy to assess fragment complexity and assign confidence to metabolite annotations) — https://github.com/LeaveMeNotTonight/CMDN
- **OrgMassSpecR** (Performs exact mass calculation to match cluster centroids to reference metabolites) — https://github.com/LeaveMeNotTonight/CMDN
- **pheatmap** (Visualizes annotated feature clusters and reaction pathway assignments) — https://github.com/LeaveMeNotTonight/CMDN
- **MSDial** (Upstream feature detection and alignment tool (ver. 4.80) that produces input feature tables)
- **Biotransformer** (Compatible reference database for xenobiotic biotransformation reactions (ver. 3.0))
- **tidyverse** (Data wrangling and loading raw MS data and metadata) — https://github.com/LeaveMeNotTonight/CMDN

## Evaluation signals

- Feature clusters have internally consistent fragmentation patterns (high MSMSsim scores ≥ 0.7 within clusters, low between clusters).
- Spectral entropy values reflect expected fragment complexity: simpler spectra (e.g., phase II conjugates) have lower entropy; diverse fragmentation indicates phase I metabolites.
- Exact mass differences between cluster members match known biotransformation rules (e.g., +16 Da for hydroxylation, +80 Da for sulfation).
- Heatmap visualization shows tight spatial clustering of annotated features with co-occurrence across samples (high cosine similarity in intensity patterns).
- Final annotated feature table contains no conflicting metabolite identities within a single cluster; all annotations traceable to reference library or reaction database.

## Limitations

- Clustering sensitivity depends on fragmentation pattern complexity; highly similar structural isomers may merge into single clusters despite distinct metabolic origins.
- Spectral entropy is sensitive to MS/MS acquisition parameters (collision energy, resolution); inconsistent parameters across samples can distort entropy-based confidence scoring.
- No built-in handling of isobaric or near-isobaric features; requires manual or external filtering before clustering.
- Propagation of annotations assumes all cluster members are true metabolites of the same parent; co-fragmentation artifacts or contamination can propagate false positives.

## Evidence

- [other] Apply MSMSsim to compute fragmentation pattern similarity scores between unknown features and reference spectra.: "Apply MSMSsim to compute fragmentation pattern similarity scores between unknown features and reference spectra."
- [other] Calculate spectral entropy using msentropy to assess fragment complexity and confidence.: "Calculate spectral entropy using msentropy to assess fragment complexity and confidence."
- [other] Perform feature detection and alignment using CluMSID with default clustering parameters.: "Perform feature detection and alignment using CluMSID with default clustering parameters."
- [other] Annotate metabolites by matching aligned features to xenobiotic reaction databases using OrgMassSpecR for exact mass calculation and CluMSID for cluster-based annotation propagation.: "Annotate metabolites by matching aligned features to xenobiotic reaction databases using OrgMassSpecR for exact mass calculation and CluMSID for cluster-based annotation propagation."
- [other] Visualize annotated feature clusters and reaction assignments using pheatmap and grid, reshaping output with reshape2.: "Visualize annotated feature clusters and reaction assignments using pheatmap and grid, reshaping output with reshape2."
- [readme] CMDN is an "top-down" untargeted metabolomics-based MS data processing framework to enable high-throughput and automated annotation of reaction-derived xenobiotic metabolites: "CMDN is an "top-down" untargeted metabolomics-based MS data processing framework to enable high-throughput and automated annotation of reaction-derived xenobiotic metabolites"
