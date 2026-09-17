---
name: xenobiotic-metabolite-annotation-from-ms-ms
description: Use when you have aligned MS/MS feature tables (e.g., from MSDial ver.
  4.80) representing unknown metabolites suspected to be Phase I/II transformation
  products of xenobiotics, and you need to assign both chemical identity and biotransformation
  pathway context to each feature.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
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
  - Biotransformer 3.0
  - MSDial
  techniques:
  - CE-MS
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# xenobiotic-metabolite-annotation-from-ms-ms

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

A top-down untargeted metabolomics workflow that automates high-throughput annotation of reaction-derived xenobiotic metabolites by matching MS/MS fragmentation patterns and spectral entropy signatures against reference databases. This skill bridges raw MS data to curated metabolite identity assignments via clustering, similarity scoring, and reaction pathway propagation.

## When to use

Apply this skill when you have aligned MS/MS feature tables (e.g., from MSDial ver. 4.80) representing unknown metabolites suspected to be Phase I/II transformation products of xenobiotics, and you need to assign both chemical identity and biotransformation pathway context to each feature. Particularly useful when dealing with large numbers of unknowns where manual spectroscopic interpretation is infeasible.

## When NOT to use

- Input data are already curated, manually-validated metabolite identities (not unknown features requiring annotation).
- Only low-resolution MS data or single MS (MS1-only) are available; the workflow requires tandem MS/MS fragmentation patterns.
- The xenobiotic metabolites of interest are not represented in available reference libraries or Biotransformer reaction rule sets.

## Inputs

- Raw MS/MS feature table (aligned, from MSDial or equivalent)
- Sample metadata table (xlsx, csv, or tsv format)
- Reference MS/MS spectra library for xenobiotic metabolites
- Biotransformation reaction database (e.g., Biotransformer 3.0 output or custom pathway annotations)

## Outputs

- Annotated feature table with metabolite identities, exact masses, and confidence scores
- Cluster-based reaction pathway assignments linking features to parent xenobiotic and transformation reactions
- Heatmap visualizations of feature clusters with annotation propagation
- Spectral entropy and similarity score matrices for quality assessment

## How to apply

Load raw MS feature data and metadata using readxl and tidyverse into R. Perform feature clustering using CluMSID with default parameters to group spectro-chemically related features. Compute MS/MS fragmentation pattern similarity scores between unknown features and reference xenobiotic metabolite spectra using MSMSsim. Calculate spectral entropy for each feature using msentropy to assess fragment complexity and confidence in annotations. Match features to xenobiotic biotransformation databases by: (1) calculating exact mass matches using OrgMassSpecR, (2) propagating annotations within CluMSID clusters, and (3) cross-referencing with known reaction pathways from Biotransformer 3.0 or equivalent databases. Visualize annotated clusters using pheatmap and grid; reshape and export final annotated feature table with metabolite identities and reaction metadata using reshape2.

## Related tools

- **CluMSID** (Performs feature clustering and spectroscopic grouping to enable annotation propagation within chemically related feature clusters)
- **MSMSsim** (Computes fragmentation pattern similarity scores between unknown features and reference spectra to support metabolite identity matching)
- **msentropy** (Calculates spectral entropy to assess fragment complexity and confidence in metabolite annotations)
- **OrgMassSpecR** (Calculates exact mass values to enable accurate matching of features to xenobiotic databases and reaction products)
- **Biotransformer 3.0** (Provides biotransformation reaction rules and metabolite pathway databases for xenobiotic transformation products)
- **MSDial** (Upstream tool (ver. 4.80) for raw MS data processing, feature detection, and alignment prior to CMDN annotation pipeline)
- **tidyverse** (Data loading, reshaping, and manipulation of metadata and feature tables in R)
- **pheatmap** (Visualization of annotated feature clusters and reaction pathway assignments)

## Evaluation signals

- All features in the output table carry non-null metabolite annotations linked to xenobiotic transformation reactions (no orphaned unknown features unless explicitly flagged as low-confidence).
- Spectral entropy scores are within expected range (typically 0–1 or 0–100 scale depending on msentropy settings) and show inverse correlation with annotation confidence: higher entropy for ambiguous spectra should correspond to lower MSMSsim similarity scores.
- Cluster-level annotation propagation is consistent: features within the same CluMSID cluster share the same or closely related metabolite assignments, indicating correct grouping logic.
- Exact mass differences between annotated features and expected biotransformation products fall within instrument tolerance (typically ≤ 5 ppm for high-resolution MS).
- Visual heatmap displays show clear clustering structure with annotation labels coherent across rows/columns, indicating successful integration of similarity, entropy, and database matching steps.

## Limitations

- Annotation accuracy depends critically on completeness and quality of the xenobiotic metabolite reference library and Biotransformer reaction rules; rare or non-canonical transformations may not be captured.
- The workflow requires installation of ten R dependencies; version compatibility and dependency conflicts are not explicitly managed in the README.
- No version control or changelog is provided for the CMDN pipeline, making reproducibility and tracking of methodological updates difficult.
- Cluster-based annotation propagation can amplify errors if seed features within a cluster are misannotated; no explicit false-discovery rate or quality-filtering cutoffs are described.

## Evidence

- [readme] CMDN is a top-down untargeted metabolomics-based MS data processing framework for high-throughput and automated annotation of reaction-derived xenobiotic metabolites: "Compound metabolite discovery network (CMDN) is an "top-down" untargeted metabolomics-based MS data processing framework to enable high-throughput and automated annotation of reaction-derived"
- [intro] Ten R packages required for CMDN pipeline implementation: "The CMDN pipeline requires installation of ten R packages (tidyverse, CluMSID, CluMSIDdata, grid, OrgMassSpecR, pheatmap, reshape2, MSMSsim, msentropy, readxl)"
- [readme] Software compatibility and version requirements: "MSDial (ver. 4.80) and Biotransformer 3.0"
- [intro] Feature detection and clustering workflow step: "Perform feature detection and alignment using CluMSID with default clustering parameters."
- [intro] Similarity scoring and entropy calculation for annotation confidence: "Apply MSMSsim to compute fragmentation pattern similarity scores between unknown features and reference spectra. Calculate spectral entropy using msentropy to assess fragment complexity and"
- [intro] Annotation matching and propagation methodology: "Annotate metabolites by matching aligned features to xenobiotic reaction databases using OrgMassSpecR for exact mass calculation and CluMSID for cluster-based annotation propagation."
- [intro] Visualization and export of final results: "Visualize annotated feature clusters and reaction assignments using pheatmap and grid, reshaping output with reshape2. Export final annotated feature table with metabolite identities and reaction"
