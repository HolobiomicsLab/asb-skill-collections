---
name: mass-spectrometry-feature-clustering
description: Use when after XCMS feature detection and alignment when you have a CSV-formatted feature table with m/z and retention time annotations and want to deduplicate isotopic peaks, adducts, and in-source fragments into compound-level clusters before molecular weight inference or spectral matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - RAMClustR
  - R
  - dynamicTreeCut
  - XCMS
  - InterpretMSSpectrum
  - MSFinder
  - Sirius
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1021/ac501530d
  title: RAMClust
evidence_spans:
- ramclustR function is built to use xcms data
- RC <- ramclustR(xcmsObj = xset, ExpDes=experiment)
- submitting this score matrix for heirarchical clustering, and then cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package
- cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ramclust_cq
    doi: 10.1021/ac501530d
    title: RAMClust
  dedup_kept_from: coll_ramclust_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac501530d
  all_source_dois:
  - 10.1021/ac501530d
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-feature-clustering

## Summary

Groups multiple mass spectrometry features derived from the same compound using unsupervised clustering based on retention time similarity and quantitative correlation across samples. This skill resolves the isotopic peaks and adduction artifacts inherent to MS ionization into coherent molecular entities before annotation.

## When to use

Apply this skill after XCMS feature detection and alignment when you have a CSV-formatted feature table with m/z and retention time annotations and want to deduplicate isotopic peaks, adducts, and in-source fragments into compound-level clusters before molecular weight inference or spectral matching.

## When NOT to use

- Input is already a deconvoluted compound-level feature table (features already represent molecular entities rather than raw MS signals)
- Tandem MS/MS data only with no MS1 features — ramclustR requires retention time or correlation structure to group features
- Data from targeted MS assays where each feature corresponds to a single known analyte by design

## Inputs

- CSV feature table with columns: sample names (first column by default), m/z_RT formatted feature identifiers (delimiter configurable)
- Phenotype/experimental design CSV or R data frame (batch, order, QC tags for normalization)
- XCMS xcmsSet object (alternative to CSV)

## Outputs

- RAMClustR object (ramclustobj) containing: clustered feature membership, representative retention times per cluster, molecular weight annotations (via do.findmain), spectra in MSP format suitable for MSFinder or Sirius import
- Abundance matrix (SpecAbund) with clusters as rows and samples as columns
- Annotation table (ann) with inferred molecular weights and scoring metrics

## How to apply

Load a CSV feature table (MS-only or MS+idMS/MS) into ramclustR, specifying the feature delimiter (default 'mz_rt'), sample name column position, and similarity threshold (st parameter, typically 5 for correlation-based cutoff). The function computes a product score combining retention time proximity and Pearson correlation of feature abundances across samples; hierarchical clustering via dynamicTreeCut then partitions features into groups where members share approximately the same retention time and quantitative trend. For MS+idMS/MS data, additionally specify the timepos parameter indicating where retention time appears in the feature identifier. Execute the main ramclustR function or use the stepwise workflow (rc.ramclustr, do.findmain) depending on whether you are starting from XCMS objects or CSV files.

## Related tools

- **XCMS** (Upstream feature detection and retention time alignment; outputs feature table or xcmsSet object consumed by ramclustR)
- **dynamicTreeCut** (Dendrogram cutting strategy applied to hierarchical clustering of feature similarity scores)
- **InterpretMSSpectrum** (Provides findMain scoring method adapted for molecular weight inference in do.findmain function)
- **MSFinder** (Downstream tool for spectral matching and structural annotation; accepts .mat format spectra exported by ramclustR)
- **Sirius** (Downstream tool for structural annotation via MS/MS fragmentation; accepts .ms format spectra exported by ramclustR)
- **R** (Execution environment for ramclustR functions and data manipulation) — https://github.com/cbroeckl/RAMClustR

## Examples

```
ramclustobj <- ramclustR(ms = 'peaks.csv', pheno_csv = 'phenoData.csv', st = 5, maxt = 1, blocksize = 1000); ramclustobj <- do.findmain(ramclustobj, mode = 'positive', mzabs.error = 0.02, ppm.error = 10)
```

## Evaluation signals

- Cluster composition: each cluster contains 2+ features with Pearson correlation > 0.7 and retention time difference < expected drift window
- Retention time consistency: all features within a cluster have approximately the same RT (within instrument RT correction tolerance, typically ±0.2 min for LC-MS)
- Quantitative coherence: feature abundance profiles across samples are correlated; features co-occur in high- and low-intensity samples
- Molecular weight annotations (ramclustobj$ann) are populated and agree ~90% of the time between findMain and ramclustR scoring methods
- Output spectra can be imported into MSFinder (.mat format) or Sirius (.ms format) without format errors; cluster size distribution is biologically plausible (majority of clusters 2–5 features)

## Limitations

- No changelog or version history is documented, making reproducibility across releases uncertain
- Clustering quality depends on sufficient sample replication and correlation structure; sparse or highly variable datasets may produce over-fragmented clusters
- Retention time correction and grouping in upstream XCMS step (group, retcor, group again) critically affect cluster membership; poor RT alignment upstream propagates to ramclustR
- findMain molecular weight inference assumes ionization mode is known (positive or negative) and does not account for salt or solvent adducts; mzabs.error and ppm.error tolerances must be tuned to instrument mass accuracy
- Performance scales with feature table size; blocksize parameter (default 1000) should be adjusted for very large datasets to manage memory and computation

## Evidence

- [intro] Each compound is represented by multiple features due to isotopic peaks and fragmentation/adduction: "each compound is represented by several features. With any ionization method, isotopic peaks will be observed"
- [intro] Clustering uses both retention time and quantitative correlation: "two features derived from the same compound will have (approximately) the same retention time. The second is that two features derived from the same compound will have (approximately) the same"
- [intro] Product of RT and correlation scores provides best similarity approximation: "Since both conditions must be met, the product of the two similarity scores provides the best approximatio of the total similarity score"
- [intro] Unsupervised, platform-agnostic clustering without curated rules: "RAMClustR was designed to group features designed from the same compound using an approach which is __1.__ unsupervised, __2.__ platform agnosic, and __3.__ devoid of curated rules"
- [readme] MS parameter accepts CSV feature tables; idmsms parameter enables MS+MS/MS combined input: "If the file contains features from MS1, assign those to the `ms` parameter. If the file contains features from MS2, assign those to the `idmsms` parameter."
- [readme] Feature column naming convention and delimiter configuration: "Choose input file with feature column names `mz_rt` (expected by default). Column with sample name is expected to be first (by default). These can be adjusted with the `featdelim` and `sampNameCol`"
- [intro] dynamicTreeCut package used for dendrogram cutting: "submitting this score matrix for heirarchical clustering, and then cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package"
- [intro] findMain and ramclustR scoring methods have ~90% agreement: "In practice we find that the two scoring methods agree about 90% of the time."
