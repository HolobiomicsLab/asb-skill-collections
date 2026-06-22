---
name: log-transform-normalization-for-metabolomics
description: Use when after chromatographic peak detection, fill-in of missing peaks, and retention-time-based grouping in LC-MS metabolomics workflows, apply log2 transformation when refining feature groups using correlation of abundances across samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3407
  tools:
  - MsFeatures
  - xcms
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package with additional functionality being implemented
- VignetteDepends{xcms,BiocStyle,faahKO,pheatmap,MsFeatures}
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms_cq
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/ac051437y
  all_source_dois:
  - 10.1021/ac051437y
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# log-transform-normalization-for-metabolomics

## Summary

Apply log2 transformation to feature abundance values in metabolomics LC-MS data to stabilize variance and improve the linearity of correlation-based feature grouping. This normalization step prepares filled intensity matrices for downstream abundance-similarity refinement.

## When to use

After chromatographic peak detection, fill-in of missing peaks, and retention-time-based grouping in LC-MS metabolomics workflows, apply log2 transformation when refining feature groups using correlation of abundances across samples. Log transformation is particularly indicated when feature intensities span multiple orders of magnitude and you wish to reduce the influence of highly abundant features on correlation calculations.

## When NOT to use

- When input feature values contain zero or negative intensities that cannot be log-transformed; use pseudocount addition or alternative transformations first.
- When features have already been grouped by multiple orthogonal criteria (RT, EIC shape, isotope pattern) and additional refinement risks over-segmentation.
- When abundance patterns are expected to be highly non-linear or when the sample set is too small (n < 3) to compute reliable correlations.

## Inputs

- XcmsExperiment or xcmsSet object with chromatographic peaks detected and retention-time-based grouping applied
- Filled peak intensity matrix (with fillChromPeaks() applied to recover missing signals)
- AbundanceSimilarityParam parameter object specifying correlation threshold and log2 transform

## Outputs

- Refined XcmsExperiment or xcmsSet object with feature groups split by abundance correlation
- Increased total number of feature groups (compared to retention-time grouping alone)
- Log2-transformed and correlation-ranked feature group assignments

## How to apply

Before calling groupFeatures() with AbundanceSimilarityParam for abundance-correlation refinement, set the transform parameter to 'log2' in the parameter object. The transformation is applied to the filled feature-value matrix (with filled=TRUE) to normalize the distribution of feature abundances before computing pairwise correlations. The log-transformed values stabilize variance across the intensity range, making abundance patterns more comparable across samples regardless of absolute peak height. Set the similarity threshold (e.g., 0.7) on the resulting correlation matrix to split initial retention-time groups into sub-groups of features with coherent abundance profiles. This refinement reduces false groupings of features that co-elute but have uncorrelated abundances across samples.

## Related tools

- **xcms** (Provides groupFeatures() function, XcmsExperiment/xcmsSet classes, and AbundanceSimilarityParam parameter specification for log-transform and correlation-based feature grouping) — https://github.com/sneumann/xcms
- **MsFeatures** (Defines general MS feature grouping functionality and parameter classes used by xcms for abundance-similarity refinement) — https://github.com/RforMassSpectrometry/MsFeatures

## Examples

```
groupFeatures(xmse, AbundanceSimilarityParam(threshold = 0.7, transform = log2, filled = TRUE))
```

## Evaluation signals

- Verify that the output feature group count is greater than or equal to the input retention-time grouping count (due to splitting of larger RT groups).
- Confirm that log2-transformed intensity distributions in refined groups show higher mean pairwise correlation (>0.7) compared to unrefined RT groups.
- Check that no feature appears in more than one refined feature group (no duplicates in group membership).
- Validate that all filled intensity values (including those recovered by fillChromPeaks) were successfully transformed and included in correlation calculations.
- Inspect that features within the same refined group share coherent abundance patterns across samples (visually or via correlation matrix).

## Limitations

- Log2 transformation fails or produces -∞ for zero or negative intensities; requires prior pseudocount adjustment or masking of missing values during the fill step.
- Correlation-based grouping is sensitive to outliers; extreme abundance values in a single sample can distort correlations. Robust correlation metrics (e.g., Spearman) may be preferable in high-noise datasets.
- The choice of similarity threshold (e.g., 0.7) is arbitrary and dataset-dependent; no universal threshold is recommended in the article. Over-strict thresholds may over-segment; lenient thresholds may retain false positives.
- Log transformation assumes multiplicative (not additive) noise; if error structure is primarily additive (as in some instrumental backgrounds), square-root or other transformations may be more appropriate.
- Requires filled feature matrix as input; missing-value recovery quality directly affects the reliability of downstream correlations.

## Evidence

- [other] After applying AbundanceSimilarityParam(threshold = 0.7, transform = log2) with filled = TRUE to the rt-20s grouped xmse object, many of the larger retention time-based feature groups were split into two or more sub-groups based on correlation of feature abundances: "After applying AbundanceSimilarityParam(threshold = 0.7, transform = log2) with filled = TRUE to the rt-20s grouped xmse object, many of the larger retention time-based feature groups were split into"
- [other] groupFeatures() function with AbundanceSimilarityParam(threshold=0.7, transform=log2, filled=TRUE) to refine feature groups based on correlation of feature abundances across samples: "groupFeatures() function with AbundanceSimilarityParam(threshold=0.7, transform=log2, filled=TRUE) to refine feature groups based on correlation of feature abundances across samples"
- [intro] for samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated: "for samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated"
- [intro] Features (ions) of the same compound should have similar retention time. - The abundance of features: "Features (ions) of the same compound should have similar retention time. - The abundance of features"
- [readme] Version 4 adds native support for the Spectra package to xcms and allows to perform the pre-processing on MsExperiment objects: "Version 4 adds native support for the Spectra package to xcms and allows to perform the pre-processing on MsExperiment objects"
