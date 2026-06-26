---
name: correlation-coefficient-computation-across-samples
description: Use when after XCMS feature detection and retention time correction,
  when you need to group features derived from the same compound. Features from the
  same compound show correlated quantitative trends across samples;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3463
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - R
  - XCMS
  - RAMClustR
  - dynamicTreeCut
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/ac501530d
  title: RAMClust
evidence_spans:
- ramclustR function is built to use xcms data
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

# correlation-coefficient-computation-across-samples

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute Pearson correlation coefficients between quantitative feature profiles across all samples to measure co-variation patterns. This metric is multiplied with retention time similarity to produce the total similarity score used for hierarchical clustering of metabolomic features.

## When to use

After XCMS feature detection and retention time correction, when you need to group features derived from the same compound. Features from the same compound show correlated quantitative trends across samples; computing correlations between all feature pairs enables unsupervised discrimination of isotopic peaks, adducts, and fragments (which co-vary) from truly independent compounds (which do not).

## When NOT to use

- Input is already a clustered or annotated feature table with compounds pre-defined; clustering should not be re-applied.
- Data contains only a single sample or very few replicates (<3); correlation estimates become unreliable with insufficient sample variation.
- Features show bimodal or multimodal intensity distributions across samples; Pearson correlation assumes linearity and may misrepresent association.

## Inputs

- XCMS feature table (abundance matrix: samples × features, with retention time and m/z metadata)
- Feature quantitative profiles (normalized intensities across samples)
- Retention time similarity scores (0–1 normalized, pre-computed for each feature pair)

## Outputs

- Pearson correlation coefficient matrix (features × features)
- Normalized correlational similarity matrix (0–1 scale, symmetric)
- Total similarity matrix (element-wise product of retention time and correlational similarity)

## How to apply

For each pair of features in the XCMS-processed feature table, compute the Pearson correlation coefficient of their quantitative abundances across all samples. Each feature is represented as a vector of normalized intensities (one value per sample). Normalize the resulting correlation matrix to a 0–1 scale (e.g., by mapping [−1, 1] → [0, 1] or using absolute correlation). This correlational similarity score is then multiplied element-wise with the retention time similarity score (also normalized to 0–1) to produce the final total similarity matrix. Values near 1 indicate features likely derive from a single compound, while values near 0 indicate independent features. The resulting symmetric similarity matrix is input to hierarchical clustering (e.g., via dynamicTreeCut) to define feature clusters.

## Related tools

- **XCMS** (Detects and aligns features from mass spectrometry data; provides input feature table with retention times and quantitative abundances)
- **RAMClustR** (Main clustering function that orchestrates retention time similarity, correlational similarity computation, and hierarchical clustering) — https://github.com/cbroeckl/RAMClustR
- **dynamicTreeCut** (Receives the total similarity matrix and cuts the resulting dendrogram into feature clusters)
- **R** (Execution environment; Pearson correlation computation via base R or tidyverse functions)

## Examples

```
# Within R after loading XCMS object and computing retention time similarity
cor_matrix <- cor(t(featureTable))  # Pearson correlation across samples
cor_sim <- (cor_matrix + 1) / 2  # Normalize [-1, 1] to [0, 1]
total_sim <- rt_similarity * cor_sim  # Element-wise product
RC <- ramclustR(xcmsObj = xset, ExpDes = experiment)  # Full workflow including correlation computation
```

## Evaluation signals

- Correlation matrix is symmetric (corr[i,j] == corr[j,i]) and diagonal elements equal 1.0 (self-correlation).
- Normalized similarity scores fall within [0, 1]; no NaN or infinite values present.
- Features from the same known compound (e.g., isotopic variants or adducts in test data) produce correlational similarity > 0.8; unrelated features produce values < 0.3.
- Total similarity matrix (product of retention time and correlational similarities) yields feature clusters consistent with reference standards or manual inspection of mass spectra.
- Histogram of similarity scores shows bimodal distribution (peaks near 0 and near 1), indicating clear separation between same-compound and different-compound feature pairs.

## Limitations

- Pearson correlation assumes linear relationships; non-linear co-variation (e.g., saturation, sigmoidal responses) may be misclassified.
- With few samples or high missing-value proportions, correlation estimates are unstable; fillPeaks preprocessing is essential.
- Sporadic features present in only one or two samples will have undefined or unreliable correlations with other features.
- Correlational similarity alone cannot distinguish features from isobaric compounds that happen to have similar sample profiles; retention time similarity is necessary to resolve this ambiguity.
- Batch effects and systematic drift (not corrected by retcor) can inflate spurious correlations between unrelated features across samples.

## Evidence

- [other] Compute Pearson correlation coefficients between quantitative feature profiles across all samples to obtain correlational similarity scores.: "Compute Pearson correlation coefficients between quantitative feature profiles across all samples to obtain correlational similarity scores."
- [intro] two features derived from the same compound will have (approximately) the same [quantitative trend across samples]: "two features derived from the same compound will have (approximately) the same"
- [intro] Since both conditions must be met, the product of the two similarity scores provides the best approximatio of the total similarity score: "Since both conditions must be met, the product of the two similarity scores provides the best approximatio of the total similarity score"
- [intro] submitting this score matrix for heirarchical clustering, and then cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package: "submitting this score matrix for heirarchical clustering, and then cutting the resulting dendrogram into neat chunks using the dynamicTreeCut package"
- [other] RAMClustR calculates a pairwise total similarity score as the product of retention time similarity and correlational similarity scores.: "RAMClustR calculates a pairwise total similarity score as the product of retention time similarity and correlational similarity scores."
