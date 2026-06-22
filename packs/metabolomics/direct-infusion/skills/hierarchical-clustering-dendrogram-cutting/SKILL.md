---
name: hierarchical-clustering-dendrogram-cutting
description: Use when after XCMS feature detection, grouping, retention time correction, and missing value filling have produced an aligned feature matrix, when you need to group features (m/z, retention time pairs) that likely originate from the same metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - RAMClustR
  - dynamicTreeCut
  - R
  - InterpretMSSpectrum
  - XCMS
  - MSFinder
  - Sirius
  techniques:
  - direct-infusion-MS
  - tandem-MS
derived_from:
- doi: 10.1021/ac501530d
  title: RAMClust
evidence_spans:
- ramclustR function is built to use xcms data
- RC <- ramclustR(xcmsObj = xset, ExpDes=experiment)
- submitting this score matrix for heirarchical clustering, and then cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package
- cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package
- We have adapted the 'findMain' function from the 'InterpretMSSpectrum' CRAN package
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

# hierarchical-clustering-dendrogram-cutting

## Summary

Group mass spectrometry features derived from the same compound by hierarchical clustering on retention time and intensity correlation similarity scores, then partition the resulting dendrogram using dynamic tree cutting to yield feature clusters. This skill is applied to metabolomics feature tables after XCMS alignment to collapse isotopic peaks, adducts, and fragments into compound-level clusters.

## When to use

Apply this skill after XCMS feature detection, grouping, retention time correction, and missing value filling have produced an aligned feature matrix, when you need to group features (m/z, retention time pairs) that likely originate from the same metabolite. Trigger conditions: (1) input is an XCMS xcmsSet object or a feature abundance matrix with sample-wise intensity measurements and feature retention time/mass annotations; (2) you aim to reduce feature redundancy caused by isotopic peaks, in-source fragmentation, and adduction phenomena; (3) you expect features from the same compound to share approximately equal retention times and similar quantitative trends across samples.

## When NOT to use

- Input is already a curated compound table or a pre-clustered feature matrix — clustering will introduce redundant or conflicting assignments.
- Features lack retention time information or come from platforms where RT is not meaningful (e.g., direct infusion MS without chromatography).
- Feature abundance data contains >50% missing values before imputation, as correlation estimates become unreliable and dendrogram structure degrades.

## Inputs

- XCMS xcmsSet object (preprocessed with feature detection, grouping, retention time correction, regrouping, and missing value imputation)
- Feature abundance matrix with sample columns and feature columns named by m/z and retention time (e.g., 'mz_rt' delimited)
- Experiment design metadata (batch, sample order, quality control sample labels)

## Outputs

- RC object (RAMClustR cluster object) containing feature-to-cluster assignments
- SpecAbund matrix: spectral abundance (clustered feature intensity sums per sample)
- .msp format spectral file(s) in 'spectra' directory for external software interpretation (MSFinder, Sirius)
- Annotated cluster table with inferred molecular weights and retention times

## How to apply

Compute a similarity score matrix by taking the product of two components: (1) retention time similarity (features with equal or near-equal RT score highest) and (2) Pearson correlation of feature abundance profiles across all samples. Submit this score matrix to hierarchical clustering (typically Ward linkage or similar), then apply the dynamicTreeCut algorithm to automatically cut the dendrogram into clusters. The product weighting ensures that features must satisfy both retention time co-localization AND correlated intensity variation to be clustered together. Tune the sensitivity using dynamicTreeCut parameters (e.g., tree height thresholds) and inspect the resulting RC object to verify that each cluster contains multiple features with near-identical RT and high correlation. Export the .msp spectral files for manual validation in external annotation software if high-confidence molecular weight inference is required.

## Related tools

- **RAMClustR** (Main clustering function that wraps hierarchical clustering and dynamic tree cutting; produces RC object and exports spectral .msp files) — https://github.com/cbroeckl/RAMClustR
- **dynamicTreeCut** (R package providing automatic dendrogram partitioning algorithm; called internally by RAMClustR to cut clustering tree into feature clusters)
- **XCMS** (Upstream tool for feature detection, grouping, and retention time correction; produces xcmsSet object that serves as input to hierarchical clustering)
- **InterpretMSSpectrum** (CRAN package providing findMain function adapted by RAMClustR for molecular weight inference from cluster spectra)
- **MSFinder** (External software for interpreting and annotating .msp spectral files exported from RC object)
- **Sirius** (External software for interpreting and annotating .ms spectral files exported from RC object)

## Examples

```
RC <- ramclustR(xcmsObj = xset, ExpDes = experiment); RC <- do.findmain(RC, mode = "positive", mzabs.error = 0.02, ppm.error = 10)
```

## Evaluation signals

- Each cluster contains 2–10 features with retention times within ~±0.2 min (or platform-dependent tolerance) and Pearson correlation ≥0.7 across sample intensities.
- Spectral .msp file is generated in the working 'spectra' directory and contains one entry per cluster with merged MS/MS fragments or isotopic peaks.
- RC$SpecAbund matrix has dimensions (number of clusters) × (number of samples) with non-negative numeric intensities; no NaN or Inf values.
- Molecular weight inference via do.findmain agrees ≥90% of the time with orthogonal spectral matching methods (findMain scoring), indicating consistent cluster composition.
- No cluster contains features with retention times differing by >1 min or with negative or near-zero correlations, suggesting over-clustering or misalignment.

## Limitations

- No changelog or version history is documented in the repository, making it difficult to track breaking changes or algorithm refinements across releases.
- Performance depends critically on the quality of upstream XCMS preprocessing (feature detection, RT correction); poor RT alignment or missing value handling can propagate into spurious clusters.
- Correlation-based clustering may fail if the same compound exhibits highly variable ionization or abundance across sample conditions (e.g., zero intensity in some samples despite biological relevance).
- The product-based similarity score (RT × correlation) does not account for features from different ionization modes or compound isomers that co-elute with identical RT; manual curation may be required.
- Large datasets (>10,000 features) may be computationally expensive for hierarchical clustering and dynamic tree cutting; blocksize parameter can mitigate but may sacrifice clustering accuracy.

## Evidence

- [intro] RT and correlation similarity rationale: "two features derived from the same compound will have (approximately) the same retention time. The second is that two features derived from the same compound will have (approximately) the same"
- [intro] Product scoring method: "Since both conditions must be met, the product of the two similarity scores provides the best approximatio of the total similarity score"
- [intro] Dynamic tree cutting algorithm: "submitting this score matrix for heirarchical clustering, and then cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package"
- [intro] RC object outputs: "Running ramclustR on an XCMS xcmsSet object produces: (1) an RC object with each XCMS feature assigned to a cluster, (2) a new 'spectra' directory containing a .msp file named after the project with"
- [intro] .msp export for external software: "The 'mat' contains spectra in .mat format suitable for import into MSFinder software"
- [readme] README stepwise workflow example: "ramclustObj <- rc.ramclustr(ramclustObj = ramclustObj)"
