---
name: sample-metadata-stratification-and-filtering
description: Use when when you have retrieved a large, heterogeneous collection of tandem MS files from ReDU or MassIVE and need to isolate a subset sharing specific sample characteristics (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - ReDU
  - MassIVE
  - GNPS
  - Emperor
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41592-020-0916-7
  title: ReDU
- doi: 10.1186/2047-217x-2-16
  title: ''
evidence_spans:
- Validation of the ReDU sample information template using the drag-and-drop validator
- ReDU only interacts with MassIVE
- data uploaded to MassIVE as a public dataset
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_redu_cq
    doi: 10.1038/s41592-020-0916-7
    title: ReDU
  dedup_kept_from: coll_redu_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-020-0916-7
  all_source_dois:
  - 10.1038/s41592-020-0916-7
  - 10.1186/2047-217x-2-16
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-metadata-stratification-and-filtering

## Summary

Stratify and filter mass spectrometry samples by their metadata attributes (e.g., organism, sample type, geography) to enable targeted reanalysis and comparison of chemical annotations within ReDU. This skill reduces the scope of exploratory analysis by selecting cohesive subsets of public tandem MS data sharing common sample information properties.

## When to use

When you have retrieved a large, heterogeneous collection of tandem MS files from ReDU or MassIVE and need to isolate a subset sharing specific sample characteristics (e.g., samples from a particular organism, body site, or geographic region) before computing PCA or comparing chemical annotations across a more homogeneous group.

## When NOT to use

- You have only a small number of files (< 10) and manual curation is more practical than filtering logic.
- Your research question requires comparison across all known metabolomic diversity (unfiltered, global analysis) rather than within-group exploration.
- Sample metadata is sparse, incomplete, or not standardized according to the ReDU template — filtering will yield ambiguous or empty results.

## Inputs

- ReDU database (populated with public MassIVE tandem MS files)
- Sample metadata attributes (organism, sample type, geography, tissue, body site, etc.)
- Validated ReDU sample information template entries for each file

## Outputs

- Filtered subset of MassIVE file IDs meeting all active filter criteria
- List of chemical annotations (m/z, retention time, GNPS spectral match identifiers) for selected files
- Sample metadata table corresponding to filtered files (for downstream visualization or statistical analysis)

## How to apply

Use the ReDU File Selector interface to apply filters via the Sample Information categories displayed as orange buttons in the center of the screen. Each filter criterion is applied cumulatively and appears as a red box in the Attribute Filters Panel (upper-right corner); the File Selector dynamically updates to show only files matching all active filters. Filters are based on validated sample metadata fields from the ReDU sample information template (e.g., organism, sample origin, sample type). Apply filters iteratively: start with broad stratification (e.g., organism), then narrow to secondary attributes (e.g., tissue or sample type) to balance statistical power with homogeneity. The resulting filtered file list becomes the input for downstream analyses such as PCA via chemical annotation matrix extraction or spectral library matching workflows.

## Related tools

- **ReDU** (Web platform providing the File Selector UI, sample metadata index, and attribute filtering interface to query and subset public tandem MS files by sample information category) — https://github.com/mwang87/ReDU-MS2-GNPS
- **MassIVE** (Public data repository hosting raw and processed mass spectrometry datasets; ReDU indexes and filters MassIVE files via sample metadata)
- **GNPS** (Provides spectral library matching and chemical annotations (GNPS identifiers, confidence levels) that populate the chemical annotation matrix extracted for filtered file subsets) — https://github.com/CCMS-UCSD/GNPSDocumentation
- **Emperor** (Downstream visualization tool that accepts the filtered sample metadata and chemical annotation PCA results for interactive 3D/2D exploration and coloring by metadata stratification variable) — https://github.com/biocore/emperor

## Evaluation signals

- The File Selector displays a reduced count of files matching all active filter criteria and shows each active filter as a red box in the Attribute Filters Panel (upper-right).
- Exported file list and metadata table contain only entries satisfying every applied filter condition (e.g., all samples are organism='Homo sapiens' AND sample_type='blood').
- The filtered chemical annotation matrix (rows=files, columns=features) contains no entries from files outside the filter criteria and has fewer rows than the unfiltered matrix.
- Emperor visualization of the filtered subset shows coherent clustering or separation by the stratification variable used for filtering, compared to noisy/dispersed patterns in unfiltered data.
- Downstream statistical tests (e.g., PERMANOVA on PCA scores) show stronger effect sizes or lower p-values when computed on the filtered, more homogeneous subset than on unfiltered data.

## Limitations

- Metadata completeness and standardization varies across submitted datasets; some files may have missing or ambiguous sample information fields, reducing effective filter specificity.
- Over-stratification (too many sequential filters) may yield very small file counts (< 3–5), reducing statistical power for downstream analyses like PCA.
- Filtering is applied only to validated sample metadata; unmapped or non-standardized metadata fields cannot be used as filter criteria and may hide relevant sample attributes.
- The ReDU sample information template requires manual curation by data submitters; inconsistent terminology or abbreviations across datasets can lead to unexpected filter results despite seemingly identical filter selections.

## Evidence

- [abstract] The orange buttons in the center of the screen correspond to Sample Information categories: "The orange buttons in the center of the screen correspond to Sample Information categories"
- [abstract] If filter/s are used, they will appear as red box/boxes in the Attribute Filters Panel (upper-right corner) of the page: "If filter/s are used, they will appear as red box/boxes in the Attribute Filters Panel (upper-right corner) of the page"
- [other] Query the ReDU database to retrieve chemical annotation matrices for selected MassIVE files, with rows as files and columns as annotated chemical features: "Query the ReDU database to retrieve chemical annotation matrices for selected MassIVE files, with rows as files and columns as annotated chemical features (m/z, retention time, GNPS annotations)"
- [methods] Fill in sample information using drop-downs when applicable: "Fill in sample information using drop-downs when applicable"
- [readme] ReDU is a community-minded approach to find and reuse public data containing tandem MS data at the repository scale: "ReDU is a community-minded approach to find and reuse public data containing tandem MS data at the repository scale. ReDU is a launchpad for co- or re-analysis of public data via the Global Natural"
