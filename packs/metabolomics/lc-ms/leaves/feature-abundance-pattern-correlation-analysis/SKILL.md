---
name: feature-abundance-pattern-correlation-analysis
description: Use when after initial retention-time-based feature grouping has been
  performed on LC-MS data but before final EIC similarity refinement.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MsFeatures
  - xcms
  - BiocParallel
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

# feature-abundance-pattern-correlation-analysis

## Summary

Refine feature groups by measuring correlation of feature abundance patterns across samples, grouping features with correlated intensity profiles that likely originate from the same compound. This step reduces false feature associations that survived retention-time-only grouping and prepares data for downstream EIC-based refinement.

## When to use

After initial retention-time-based feature grouping has been performed on LC-MS data but before final EIC similarity refinement. Use this skill when you have a pre-grouped xmse object and need to identify which features truly co-vary across samples, which is a strong indicator of common compound origin. Particularly valuable when sample-to-sample intensity variation is high or when retention time alone groups features from different compounds.

## When NOT to use

- Input features have not yet been grouped by retention time; use SimilarRtimeParam first.
- Sample set contains only 1–2 replicates; correlation estimates are unreliable with very small sample counts.
- Data are from untargeted analysis with high dynamic range and many missing values that cannot be reliably filled; consider alternative grouping strategies.

## Inputs

- xmse object (XcmsExperiment or xcmsSet) grouped by retention time
- numeric intensity matrix with features as rows and samples as columns
- optional: filled chromatographic peak data (from fillChromPeaks step)

## Outputs

- xmse object with refined feature groups based on abundance correlation
- reduced feature group count (fewer, more specific groups than input)
- group assignments and feature-to-group mapping

## How to apply

Load the retention-time-grouped xmse object into the R environment and call groupFeatures() with AbundanceSimilarityParam, specifying a correlation threshold (e.g., 0.7) and an appropriate intensity transformation (log2 is recommended to normalize intensity distributions). Set filled=TRUE to ensure missing peak data are filled before correlation calculation, preventing spurious correlations from missing values. The function computes pairwise Pearson correlations of log-transformed abundances across all samples for each feature pair within a retention-time group, retaining feature pairs exceeding the threshold. This produces a refined xmse object with fewer, more homogeneous feature groups. Subsequently pass this output to EicSimilarityParam-based groupFeatures() for final EIC peak-shape refinement.

## Related tools

- **xcms** (Primary framework; provides groupFeatures() function and data containers (XcmsExperiment, xcmsSet) for feature grouping and abundance correlation) — https://github.com/sneumann/xcms
- **MsFeatures** (Defines general feature grouping interfaces and parameter classes (AbundanceSimilarityParam) used by xcms) — https://github.com/RforMassSpectrometry/MsFeatures
- **BiocParallel** (Enables parallel computation of pairwise correlations across features when processing large feature sets)

## Examples

```
groupFeatures(xmse, AbundanceSimilarityParam(threshold = 0.7, transform = log2), filled = TRUE)
```

## Evaluation signals

- Feature group count decreases after applying AbundanceSimilarityParam compared to input (retention-time-only groups), confirming that spurious RT-based associations have been filtered.
- Selected feature groups show pairwise Pearson correlation coefficients ≥ threshold (e.g., ≥ 0.7) when abundance patterns are recalculated on output; inspect via featureDefinitions(xmse) and peakData(xmse).
- Remaining groups are smaller and more internally homogeneous than input groups, with reduced m/z spread within each group (indicating fewer 'satellite' features).
- Output xmse object passes validation checks (validObject(xmse) == TRUE) and retains consistent sample and peak metadata.
- Final feature group count is consistent and reproducible across multiple independent runs with identical parameters.

## Limitations

- Correlation-based grouping assumes abundance patterns reflect shared biochemical origin; technical artifacts (contamination, instrumental variation) can create spurious correlations.
- Log-transformation (log2) assumes multiplicative noise model; if noise is predominantly additive, alternative transformations may be more appropriate.
- Threshold selection (e.g., 0.7) is somewhat arbitrary; no universally optimal value exists across all metabolomics datasets; user should validate against independent methods (e.g., MS/MS matching).
- Small sample sizes (n < 5) yield unstable correlation estimates with high variance; results may not generalize to larger cohorts.
- Missing values (zero or NA) in the peak matrix can inflate or deflate correlation estimates if not properly handled by fillChromPeaks; carefully inspect fill parameters.

## Evidence

- [intro] AbundanceSimilarityParam grouping methodology: "Refine feature groups based on correlation of feature abundances across samples"
- [intro] Threshold and transformation specification: "groupFeatures(xmse, AbundanceSimilarityParam(threshold = 0.7, transform = log2), filled = TRUE)"
- [intro] Rationale for abundance-based grouping: "Features (ions) of the same compound should have similar retention time. The abundance of features"
- [intro] Position in workflow sequence: "Further refine feature groups based on similarity of extracted ion chromatogram peak shapes"
- [readme] Tool support and integration: "Version 4 adds native support for the Spectra package to xcms and allows to perform the pre-processing on MsExperiment objects"
