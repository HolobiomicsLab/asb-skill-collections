---
name: chromatographic-feature-refinement
description: Use when after performing retention-time-based grouping on LC-MS data (e.g., with a 10–20 second window) and observing that many feature groups contain features with similar retention times but dissimilar abundance patterns across samples or different extracted ion chromatogram peak shapes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MsFeatures
  - xcms
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-feature-refinement

## Summary

Refine LC-MS feature groups by applying correlation-based or peak-shape-based similarity thresholds after initial retention-time grouping to split co-eluting features from different compounds and improve annotation specificity. This skill reduces false positive feature groupings caused by similar retention times but distinct abundance patterns or peak morphologies.

## When to use

After performing retention-time-based grouping on LC-MS data (e.g., with a 10–20 second window) and observing that many feature groups contain features with similar retention times but dissimilar abundance patterns across samples or different extracted ion chromatogram peak shapes. This occurs when retention time alone is insufficient to discriminate features from different compounds that happen to co-elute.

## When NOT to use

- Input feature groups are already refined by abundance or peak shape and further splitting would fragment true co-eluting features from the same compound.
- Sample abundances are not normally distributed or are highly skewed, making log2 transformation and Pearson correlation unreliable without additional normalization.
- Extracted ion chromatogram peak shape data is unavailable or highly noisy, rendering EicSimilarityParam unreliable.

## Inputs

- XcmsExperiment object with retention-time-based feature grouping applied
- filled feature value matrix (log2-transformed, with missing values imputed)

## Outputs

- XcmsExperiment object with refined (typically increased) number of feature groups
- Total feature group count after refinement

## How to apply

Load a pre-grouped XcmsExperiment object (output from retention-time-based grouping). Apply groupFeatures() with either AbundanceSimilarityParam (for abundance-based refinement) or EicSimilarityParam (for peak-shape-based refinement). For abundance refinement, set a threshold (e.g., 0.7) on log2-transformed filled feature values to split groups where pairwise correlations fall below the threshold; use filled=TRUE to impute missing peaks before correlation. For peak-shape refinement, use EicSimilarityParam with a threshold (e.g., 0.7) and specify the number of samples (n=2) to compare. The rationale is that features of the same compound should exhibit both correlated abundances across samples and similar peak morphologies; features failing these criteria likely originate from different compounds and should be separated into distinct groups. Extract and compare the resulting total feature group count to the input count to verify refinement has occurred.

## Related tools

- **xcms** (Provides groupFeatures() function and AbundanceSimilarityParam/EicSimilarityParam classes for retention-time and correlation-based feature grouping refinement) — https://github.com/sneumann/xcms
- **MsFeatures** (Defines general MS feature grouping functionality and parameter classes used by xcms) — https://github.com/RforMassSpectrometry/MsFeatures

## Examples

```
groupFeatures(xmse, param = AbundanceSimilarityParam(threshold = 0.7, transform = log2), filled = TRUE)
```

## Evaluation signals

- Total feature group count increases substantially from the initial retention-time-only grouping, indicating successful splitting of larger groups into smaller, more homogeneous sub-groups.
- Inspect correlation matrix or peak-shape similarity matrix for refined groups: values within groups should exceed the specified threshold, and values between groups should fall below it.
- Verify that the resulting feature groups have more similar retention times, abundances, and/or peak shapes within each group compared to the initial grouping.
- Cross-check that no single-feature groups are created unless they represent genuine singletons after refinement (i.e., no spurious over-fragmentation).
- Confirm that downstream annotation (e.g., database matching) shows improved specificity or reduced conflicting ion identifications per group.

## Limitations

- Abundance-based refinement assumes log2-transformed, normally distributed feature abundances; highly skewed or zero-inflated data may yield unreliable correlations. The filled=TRUE option requires robust peak-filling algorithm output to avoid false correlations from imputed values.
- Peak-shape refinement (EicSimilarityParam) is sensitive to noise and requires well-defined, reproducible extracted ion chromatogram morphologies; noisy or broad peaks may prevent meaningful similarity comparison.
- The choice of similarity threshold (e.g., 0.7) is data- and compound-dependent; inappropriate thresholds may cause under-splitting (true compounds remain grouped) or over-splitting (isotopologues or adducts are incorrectly separated).
- Missing or partially detected chromatographic peaks in some samples can bias abundance correlations; the article notes that missing signals must be filled using signal integration at feature locations for reliability.

## Evidence

- [intro] Abundance-based refinement mechanism and parameters: "Apply groupFeatures() function with AbundanceSimilarityParam(threshold=0.7, transform=log2, filled=TRUE) to refine feature groups based on correlation of feature abundances across samples."
- [intro] Peak-shape refinement mechanism: "Further refine feature groups based on similarity of extracted ion chromatogram peak shapes"
- [intro] Compound features and grouping assumptions: "Features (ions) of the same compound should have similar retention time. The abundance of features"
- [intro] Missing data handling for abundance refinement: "for samples in which no chromatographic peak for a feature was detected, all signal from the m/z - retention time range defined based on the detected chromatographic peaks was integrated"
- [other] Observed outcome of abundance-based refinement on faahKO dataset: "many of the larger retention time-based feature groups were split into two or more sub-groups based on correlation of feature abundances, with the total number of feature groups increasing"
