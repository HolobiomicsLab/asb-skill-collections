---
name: lc-ms-feature-grouping-and-compounding
description: Use when after chromatographic peak detection on preprocessed LC-MS data, when you have hundreds or thousands of individual m/z × retention-time peaks and need to associate them into biologically meaningful feature groups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MsFeatures
  - pheatmap
  - xcms
  - MSnbase
derived_from:
- doi: 10.1021/acs.analchem.5c04338
  title: xcms
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package
- library(pheatmap)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms
    doi: 10.1021/acs.analchem.5c04338
    title: xcms
  dedup_kept_from: coll_xcms
schema_version: 0.2.0
---

# LC-MS Feature Grouping and Compounding

## Summary

A multi-stage hierarchical workflow to group detected LC-MS chromatographic peaks into feature groups and sub-groups based on retention time similarity, abundance correlation patterns across samples, and extracted ion chromatogram (EIC) shape. This skill is essential for collapsing redundant ion signals from the same metabolite (e.g., isotopologues, adducts, fragments) into interpretable compound-level features.

## When to use

After chromatographic peak detection on preprocessed LC-MS data, when you have hundreds or thousands of individual m/z × retention-time peaks and need to associate them into biologically meaningful feature groups. Apply this skill particularly when data shows multiple peaks at similar retention times (suggesting different ionization forms of the same compound) or when you need to validate grouping quality by examining pairwise abundance correlations (e.g., checking whether features within a group truly co-vary across samples with correlation ≥ 0.7).

## When NOT to use

- Input is already a curated feature table or annotated compound list—you are re-grouping already-grouped data
- Chromatographic peaks have not been detected yet—you must run peak detection (findChromPeaks or equivalent) before grouping
- Samples lack sufficient replication or biological variation—abundance-correlation-based refinement requires multiple samples with distinct abundance patterns to be effective

## Inputs

- Chromatographic peaks from xcms findChromPeaks() output (detected m/z, retention time, intensity across samples)
- Retention-time-based feature groups (output of groupFeatures(..., SimilarRtimeParam(...)))
- Abundance matrix (feature intensities × samples, optionally log2-transformed and gap-filled)

## Outputs

- Refined feature group assignments (grouping with sub-group identifiers for each peak)
- Pairwise abundance correlation matrix or heatmap per feature group
- Feature sub-group counts and composition (which peaks belong to which sub-groups)
- Visualization of feature groups in m/z–retention-time space with sub-group connections

## How to apply

Start by performing initial grouping using SimilarRtimeParam with a retention-time tolerance (e.g., 20-second window) to cluster peaks detected within the same chromatographic elution window. Next, refine these retention-time groups using AbundanceSimilarityParam with a correlation threshold (e.g., threshold=0.7) and a transform strategy (e.g., log2, filled=TRUE) to split groups where features do not co-vary in abundance across samples—this identifies sub-groups representing chemically distinct features. Optionally apply a third refinement using EicSimilarityParam to sub-group further based on shape similarity of extracted ion chromatograms. For each refined feature group, compute pairwise abundance correlations and visualize them (e.g., heatmap) to verify that the grouping criterion was met; features with correlation below the threshold should either be moved to separate groups or flagged as ambiguous. The rationale is that true adducts/isotopologues of a single metabolite must have: (1) similar retention time (same elution), (2) correlated peak heights across samples (same relative abundance), and (3) similar peak shape (same chromatographic behavior).

## Related tools

- **xcms** (Provides core peak detection (findChromPeaks with CentWaveParam) and groupFeatures() function for multi-stage retention-time, abundance-correlation, and EIC-based feature grouping) — https://github.com/sneumann/xcms
- **MsFeatures** (Defines general MS feature grouping functionality and parameter classes (SimilarRtimeParam, AbundanceSimilarityParam, EicSimilarityParam) used by xcms)
- **pheatmap** (Visualizes pairwise abundance correlations within feature groups as heatmaps to assess grouping quality)
- **MSnbase** (Provides data container classes for chromatographic peaks and spectra)

## Examples

```
groupFeatures(fts, param = AbundanceSimilarityParam(threshold = 0.7, transform = 'log2', filled = TRUE))
```

## Evaluation signals

- Total count of output feature sub-groups is as expected given the input retention-time groups and abundance-correlation threshold (e.g., 159 features grouped into 94 feature groups after stage 1, then further refined by abundance correlation)
- Pairwise correlation heatmap for a feature group shows that features within a sub-group have mutual correlations ≥ the specified threshold (e.g., ≥ 0.7), and features in different sub-groups have correlations below threshold
- No feature is assigned to multiple sub-groups; all detected peaks are assigned to exactly one sub-group
- Visualization of grouped features in m/z–retention-time space shows that connected features cluster tightly in retention time and that sub-groups are clearly separated by abundance pattern
- Gap-filled intensities (for samples where a feature was not detected) are present and used in correlation calculation without introducing artificial correlations or biasing the result

## Limitations

- Not all features within a retention-time group may be members of the same abundance-correlation sub-group; some peaks within FG.040 show weak correlations despite being clustered by retention time, requiring manual or expert review
- Abundance-correlation-based refinement is sensitive to missing peak detections and depends on gap-filling accuracy; if gap-filling is inaccurate, spurious or inflated correlations may result
- The choice of abundance-similarity threshold (e.g., 0.7) and transformation strategy (e.g., log2) is user-specified and not automatically optimized; different thresholds may produce different numbers and compositions of sub-groups
- EIC-based refinement (EicSimilarityParam) may fail or produce ambiguous results if extracted ion chromatograms have poor signal-to-noise or overlapping elution profiles

## Evidence

- [intro] Features (ions) of the same compound should have similar retention time. The abundance of features (ions) of the same compound should have a similar pattern across samples. The peak shape of EICs of features of the same compound should be similar: "Features (ions) of the same compound should have similar retention time. The abundance of features (ions) of the same compound should have a similar pattern across samples. The peak shape of"
- [other] After applying AbundanceSimilarityParam(threshold=0.7, transform=log2, filled=TRUE), the 159 features were grouped into 94 feature groups. Within FG.040, pairwise correlation analysis reveals that not all features show correlation above the 0.7 threshold—for example, clear correlation is present between FT273 and FT274, and between FT143 and FT273, but other features within this retention time group show weaker correlations.: "After applying AbundanceSimilarityParam(threshold=0.7, transform=log2, filled=TRUE), the 159 features were grouped into 94 feature groups. Within FG.040, pairwise correlation analysis reveals that"
- [intro] SimilarRtimeParam: perform an initial grouping based on similar retention time.: "SimilarRtimeParam: perform an initial grouping based on similar retention time."
- [intro] AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples.: "AbundanceSimilarityParam: perform a feature grouping based on correlation of feature abundances (values) across samples."
- [intro] EicSimilarityParam: perform a feature grouping based on correlation of EICs.: "EicSimilarityParam: perform a feature grouping based on correlation of EICs."
- [intro] Retention time-based feature grouping with 20-second window grouped features into feature groups; abundance correlation-based refinement further split groups; EIC similarity analysis provided additional sub-grouping: "Grouping by similar retention time grouped the in total features into feature groups. Many of the larger retention time-based feature groups have been splitted into two or more sub-groups based on"
- [intro] for samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated.: "for samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated."
- [readme] The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data.: "The *xcms* R package provides functionality to efficiently preprocess LC-MS (as well as GC-MS and LC-MS/MS) data."
