---
name: extracted-ion-chromatogram-peak-shape-similarity
description: Use when after features have been grouped by retention time similarity
  and abundance correlation across samples, but before downstream annotation or compound
  identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0092
  tools:
  - MsFeatures
  - xcms
  - MSnbase
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")`
  package with additional functionality being implemented
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Extracted-Ion-Chromatogram Peak-Shape Similarity Grouping

## Summary

Refine feature groups by grouping features with similar extracted ion chromatogram (EIC) peak shapes using correlation metrics, reducing false feature associations that survive retention time and abundance-based grouping. This is the final refinement step in multi-stage LC-MS feature compounding.

## When to use

After features have been grouped by retention time similarity and abundance correlation across samples, but before downstream annotation or compound identification. Apply this step when you have a pre-grouped xmse object and need to validate that co-grouped features truly originate from the same compound by examining the shape and temporal profile of their chromatographic peaks across the samples.

## When NOT to use

- Input is raw LC-MS data with no prior grouping; apply retention-time and abundance grouping first.
- Feature groups contain only a single feature; EIC shape comparison requires at least two features per group to be meaningful.
- Dataset lacks replicate samples across which to compute abundance correlation; EIC similarity is most reliable when at least 2 samples (n ≥ 2) contain strong signal for the features.

## Inputs

- xmse object (XcmsExperiment or OnDiskMSnExp) with features already grouped by retention time and/or abundance correlation
- EicSimilarityParam object specifying threshold (0.0–1.0 correlation coefficient) and n (number of top samples to evaluate)

## Outputs

- xmse object with refined feature groups based on EIC peak-shape similarity
- Numeric count of distinct feature groups after EIC-based refinement

## How to apply

Load a feature-grouped xmse object (output from an AbundanceSimilarityParam or SimilarRtimeParam grouping step) into the R environment using xcms. Call groupFeatures() with EicSimilarityParam, specifying a correlation threshold (e.g., 0.7) and the number of top samples by abundance to use for EIC comparison (e.g., n=2). The function computes pairwise EIC similarity by extracting the ion chromatogram for each feature, calculating peak shape correlation coefficients between features within each existing group, and then splitting groups whose internal correlations fall below the threshold. Extract and report the final count of feature groups; a reduction in group count indicates that dissimilar EIC shapes have been separated, improving specificity of feature-to-compound assignments.

## Related tools

- **xcms** (Provides groupFeatures() function, EicSimilarityParam class, and xmse data container for LC-MS feature grouping and EIC extraction.) — https://github.com/sneumann/xcms
- **MsFeatures** (Defines general MS feature grouping functionality and parameter classes used by xcms for grouping workflows.)
- **MSnbase** (Provides core MS data container classes underlying xmse objects.)

## Examples

```
groupFeatures(xmse, param = EicSimilarityParam(threshold = 0.7, n = 2))
```

## Evaluation signals

- Final feature group count is lower than input count, confirming that some groups were split based on EIC dissimilarity.
- All features within each final group have EIC correlation ≥ threshold; spot-check by extracting chromPeaks() for a group and visually comparing peak shapes or correlation coefficients.
- Features that were co-grouped by retention time/abundance but have markedly different peak shapes (e.g., broad vs. sharp, early vs. late elution within retention window) are now in separate groups.
- Output xmse object retains all original features and metadata; no features are removed, only redistributed among groups.
- Reproducibility: re-running groupFeatures() with identical threshold and n parameters on the same input produces identical group assignments.

## Limitations

- EIC similarity is computed only on the top n samples (by abundance) per feature within each group; samples with low or missing signal contribute no information, potentially masking rare or low-abundance features.
- Threshold selection (e.g., 0.7) is empirical and dataset-dependent; no universal optimal value is provided by the article or documentation.
- Features with very low intensity or noisy chromatographic peaks may have artificially low EIC correlations even if they originate from the same compound, leading to false group splits.
- Performance scales with the number and size of input feature groups; very large groups may require substantial computation time.

## Evidence

- [intro] EIC similarity rationale: "Features (ions) of the same compound should have similar retention time. The abundance of features"
- [intro] Workflow step description: "Further refine feature groups based on similarity of extracted ion chromatogram peak shapes"
- [other] Task-specific finding: "The grouping based on EIC correlation resulted in the 2289 features being grouped into 589 distinct feature groups."
- [intro] Function signature: "groupFeatures(xmse, EicSimilarityParam(threshold = 0.7, n = 2))"
- [intro] Compounding goal: "Compounding aims now at grouping such features presumably representing signal from the same originating compound to reduce data set complexity"
