---
name: retention-time-correlation-similarity-scoring
description: Use when when you have detected multiple features from non-targeted mass
  spectrometry and need to group them by putative compound origin.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - RAMClustR
  - R
  - dynamicTreeCut
  - XCMS
  - InterpretMSSpectrum
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/ac501530d
  title: RAMClust
evidence_spans:
- ramclustR function is built to use xcms data
- RC <- ramclustR(xcmsObj = xset, ExpDes=experiment)
- submitting this score matrix for heirarchical clustering, and then cutting the resulting
  dendrogram into neat chunks using the dynamicTreeCut package
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-correlation-similarity-scoring

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute a combined similarity score for metabolomics features by integrating retention time proximity and quantitative correlation across samples, enabling unsupervised grouping of isotopologs and adducts from the same compound. This scoring approach grounds RAMClustR's feature clustering in two independent biological and physicochemical constraints.

## When to use

When you have detected multiple features from non-targeted mass spectrometry and need to group them by putative compound origin. Use this skill when features are suspected to derive from the same compound but appear as separate signals due to isotopic peaks, in-source fragmentation, or multiple adduct forms. Trigger: you observe features with similar retention times and correlated intensities across replicate samples, but lack curated rules or spectral libraries for definitive assignment.

## When NOT to use

- Input is already a compound-level (clustered) feature table—do not re-cluster; this skill is designed for raw, unclustered feature tables from XCMS or similar peak detection.
- Features come from targeted or hypothesis-driven assays with known, curated molecular identities—this unsupervised approach may fragment known compounds or merge known isobars incorrectly.
- Retention time information is unreliable or missing entirely—the RT component of the composite score will be uninformative, degrading clustering quality.

## Inputs

- Feature abundance matrix (CSV or XCMS object): rows=samples, columns=features; feature names must encode m/z and retention time (e.g., 'mz_rt' format)
- Sample metadata or phenotype table: experimental design, batch identifiers, and sample class labels
- Retention time values for each feature (extracted from feature name or separate column)
- Ion mode (positive/negative): used for downstream molecular weight inference

## Outputs

- RAMClustR object (RC) containing clustered features grouped by compound
- Cluster assignments: each original feature assigned to a RAM cluster ID
- Cluster-level spectra (MSP format): median spectrum per cluster
- Annotation table: inferred molecular weights, putative main ions, and adduct assignments per cluster

## How to apply

Calculate two independent similarity scores for each feature pair: (1) retention time similarity based on absolute RT difference (features with approximately the same RT score higher); (2) Pearson or Spearman correlation of feature abundances across all samples (higher correlation indicates co-regulation typical of isotopologs/adducts). Multiply the two scores to produce a composite similarity that requires BOTH conditions to be met. Use this product as the edge weight in a hierarchical clustering dendrogram, then cut the dendrogram using dynamic tree cutting to yield feature clusters. Set the similarity threshold (st parameter, typically 5 ppm or mass units for retention time tolerance) to reflect your instrument's precision; features exceeding this threshold in RT difference contribute near-zero RT similarity regardless of correlation.

## Related tools

- **XCMS** (Detects features (signals) from raw mass spectrometry data and generates the feature abundance matrix that serves as input to retention-time-correlation-similarity-scoring)
- **RAMClustR** (Implements the combined RT-correlation similarity scoring and hierarchical clustering workflow; wraps the scoring approach into the main ramclustR() function) — https://github.com/cbroeckl/RAMClustR
- **dynamicTreeCut** (Cuts the hierarchical clustering dendrogram produced by RT-correlation similarity scoring into discrete clusters without requiring manual height thresholds)
- **InterpretMSSpectrum** (Provides the findMain algorithm adapted by RAMClustR for downstream molecular weight inference after clusters are formed)

## Examples

```
ramclustobj <- ramclustR(ms = "peaks.csv", pheno_csv = "phenoData.csv", st = 5, maxt = 1, blocksize = 1000)
```

## Evaluation signals

- Cluster membership invariant: all features in a cluster must have retention times within the specified tolerance (st parameter, typically ±5 ppm or mass units); visually inspect cluster RT ranges to confirm clustering did not merge features with disparate RTs.
- Correlation stability: features within a cluster exhibit sample-to-sample abundance correlation (Pearson or Spearman r) substantially higher than inter-cluster feature pairs; compute correlation matrix on SpecAbund output and compare within- vs. between-cluster distributions.
- Cluster size distribution: most clusters should contain 2–6 features (isotopologs + common adducts); clusters with >10 features may indicate undersized similarity threshold or merged isobars and warrant inspection.
- Molecular weight coherence: inferred main ions per cluster should differ by mass offsets consistent with known adducts (e.g., +1 Da for H+ gain, ±0.5 Da for doubly charged species); use do.findmain() output (ramclustobj$M) to validate.
- Reproducibility: re-run clustering on a random subset of samples or after adding technical replicates; cluster assignments should remain stable (adjusted Rand index or Fowlkes–Mallows index > 0.8).

## Limitations

- Method assumes features from the same compound have approximately the same retention time and correlated abundance; compounds co-eluting by chance or showing anticorrelated regulation will be misclassified.
- Sensitive to retention time calibration drift and quality of feature detection; poor RT correction in XCMS preprocessing or high peak detection error rates degrade RT similarity scoring.
- No built-in handling of biological or technical factors that cause systematic abundance anticorrelation (e.g., competitive ionization, sample matrix effects); pre-filtering using batch correction or blank subtraction is recommended.
- Performance on very high-dimensional feature tables (>10,000 features) may be computationally slow due to pairwise correlation calculation; blocksize parameter can be adjusted to manage memory but may affect clustering quality.
- No changelog available; version history and breaking changes are undocumented, limiting reproducibility across RAMClustR versions.

## Evidence

- [intro] The product of retention time and correlational similarity scores provides best approximation of total similarity.: "Since both conditions must be met, the product of the two similarity scores provides the best approximatio of the total similarity score"
- [intro] Features from the same compound have approximately the same retention time and quantitative correlation.: "two features derived from the same compound with have (approximately) the same retention time. The second is that two features derived from the same compound will have (approximately) the same"
- [intro] RAMClustR uses an unsupervised, platform-agnostic approach without curated rules.: "RAMClustR was designed to group features designed from the same compound using an approach which is __1.__ unsupervised, __2.__ platform agnosic, and __3.__ devoid of curated rules"
- [intro] The method groups features that represent isotopes, fragmentation, and adduction phenomena from a single compound.: "each compound is represented by several features. With any ionization method, isotopic peaks will be observed"
- [other] RAMClustR accepts CSV input via ms parameter for MS-only analysis and idmsms parameter for MS+idMS/MS analysis with timepos parameter.: "If the file contains features from MS1, assign those to the `ms` parameter. If the file contains features from MS2, assign those to the `idmsms` parameter."
