---
name: chromatographic-peak-shape-comparison
description: Use when after retention-time-based and abundance-correlation-based feature grouping have produced composite feature groups, and you need to identify which features within a group actually represent different compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3370
  tools:
  - MsFeatures
  - xcms
  - Spectra
derived_from:
- doi: 10.1021/ac051437y
  title: XCMS
evidence_spans:
- General MS feature grouping functionality if defined by the `r Biocpkg("MsFeatures")` package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_xcms
    doi: 10.1021/ac051437y
    title: XCMS
  dedup_kept_from: coll_xcms
schema_version: 0.2.0
---

# chromatographic-peak-shape-comparison

## Summary

Compare extracted ion chromatogram (EIC) peak shapes across co-eluting features to detect and separate features belonging to different compounds that share similar retention times and m/z values. This skill identifies subtle retention-time shifts and peak morphology differences that distinguish features of distinct compounds from genuine isotopologue or adduct variants.

## When to use

Apply this skill after retention-time-based and abundance-correlation-based feature grouping have produced composite feature groups, and you need to identify which features within a group actually represent different compounds. Use it specifically when EIC visual inspection or quantitative EIC-correlation analysis (via EicSimilarityParam) reveals that some features in a group have shifted retention times, distinct peak shoulders, or uncorrelated peak shapes across samples—indicators that they originate from different molecular entities rather than the same compound.

## When NOT to use

- Input is already a feature table (quantified abundances only, without raw chromatographic peak data or EIC reconstructions)—EIC shape comparison requires access to raw intensity-time traces.
- Feature groups are already well-separated by retention time (e.g., peak-width resolution > 20 s apart)—EIC-similarity refinement adds little value when groups are already chromatographically distinct.
- Only MS/MS spectral data are available, without accompanying EIC or chromatographic peak information—peak shape comparison is inherently a chromatographic, not spectral, operation.

## Inputs

- XcmsExperiment or xcmsSet object with abundance-correlation-refined feature groups (from AbundanceSimilarityParam step)
- Pre-processed LC-MS data in mzML or NetCDF format
- Feature group metadata table with m/z, retention time, and per-sample abundances

## Outputs

- XcmsExperiment or grouped object with EIC-similarity-refined feature groups (sub-groups created where EIC correlation < threshold)
- Final feature group count and inventory (typically increased, as large groups subdivide)
- Overlay EIC plots showing peak shape comparisons for selected feature groups (e.g., FG.013.001, FG.045.001)
- Quantitative EIC-correlation matrix (if extracted)

## How to apply

Load abundance-correlation-refined feature groups (output from AbundanceSimilarityParam) into xcms/MsFeatures. Apply the groupFeatures() function with EicSimilarityParam, setting a correlation threshold (e.g., 0.7) and sample count (n=2, meaning correlation computed across the top n samples by abundance). This step computes pairwise EIC correlations among features within each group and subdivides groups where correlation falls below the threshold. Extract the final feature group count and generate overlay EIC plots (via plotEICs() or equivalent) for feature groups showing subdivision. Visually inspect plots for features with shifted retention times, distinct peak shapes, or asymmetric morphology—these signal real chemical separation. The rationale: peak shape similarity is an independent constraint on feature grouping, orthogonal to retention time and abundance correlation, and refines away false co-groupings arising from overlapping chromatographic backgrounds or cross-talk.

## Related tools

- **xcms** (Provides groupFeatures() function with EicSimilarityParam to compute EIC correlations and perform hierarchical subdivision of feature groups based on peak-shape similarity.) — https://github.com/sneumann/xcms
- **MsFeatures** (Supplies general MS feature grouping functionality and parameter classes (EicSimilarityParam) to configure EIC-based similarity thresholds and sample counts.)
- **Spectra** (Used in xcms v4+ to represent and manipulate chromatographic and spectral data structures underlying EIC extraction and visualization.)

## Examples

```
groupFeatures(feature_groups_obj, EicSimilarityParam(threshold=0.7, n=2))
```

## Evaluation signals

- Final feature group count increases (or stays same) after EIC-similarity refinement relative to abundance-similarity output, indicating successful sub-grouping.
- Feature groups targeted for EIC-similarity refinement (e.g., FG.013.001, FG.045.001) display visually distinct sub-groups in overlay EIC plots, with at least one feature showing a shifted retention time (e.g., 5–15 s lag) or asymmetric peak morphology relative to co-eluting features.
- EIC-correlation coefficients for sub-divided features fall below the specified threshold (e.g., < 0.7); correlations within sub-groups exceed the threshold.
- No spurious sub-grouping occurs: genuinely co-eluting features of the same compound (e.g., isotopologue M, M+1; or [M+H]⁺ and [M+Na]⁺ adducts) remain grouped together, with EIC correlations > threshold.
- Overlay EIC plots show overlay concordance (peak apexes aligned, peak widths similar) within refined sub-groups, and discordance (offset apexes, different widths, or distinct shoulders) between sub-groups.

## Limitations

- EIC-similarity refinement depends on signal-to-noise ratio and peak resolution; low-intensity features or heavily overlapped peaks may produce noisy or unreliable EIC correlations, leading to false sub-grouping or failure to detect real separations.
- The threshold parameter (e.g., 0.7) is user-specified and data-dependent; no universal default is given in the article. Practitioners must calibrate thresholds on pilot data or domain expertise to avoid over- or under-subdivision.
- EIC correlation is computed only across the top n samples (n=2 in the example); for low-abundance features or sparse feature occurrence across the sample cohort, the correlation may be unstable or undefined, reducing reliability of the refinement.
- Gap-filling (integration of signal in m/z–retention time windows where peaks are absent) can introduce artifact correlations or mask true EIC differences if applied before EIC-similarity analysis; timing and interaction with gap-filling are not fully addressed in the article.
- Visual EIC interpretation is subjective; differences in peak shape may be subtle (e.g., shoulder, asymmetry, tail) and require expert judgment to distinguish signal from noise or instrumental artifact.

## Evidence

- [intro] Features (ions) of the same compound should have similar retention time. The abundance of features (ions) of the same compound should have a similar pattern across samples. The peak shape of EICs of features of the same compound should be similar: "Features (ions) of the same compound should have similar retention time. The abundance of features (ions) of the same compound should have a similar pattern across samples. The peak shape of"
- [intro] EicSimilarityParam: perform a feature grouping based on correlation of EICs.: "EicSimilarityParam: perform a feature grouping based on correlation of EICs."
- [other] After EIC similarity analysis with threshold 0.7 and n=2, features within feature groups FG.013.001 and FG.045.001 were subdivided into separate sub-groups, with one feature in FG.013.001 showing a shifted retention time in EIC plots that distinguished it from co-eluting features: "After EIC similarity analysis with threshold 0.7 and n=2, features within feature groups FG.013.001 and FG.045.001 were subdivided into separate sub-groups, with one feature in FG.013.001 showing a"
- [other] Apply groupFeatures() function with EicSimilarityParam specifying threshold=0.7 and n=2 to perform feature grouping based on EIC similarity correlation across the refined groups.: "Apply groupFeatures() function with EicSimilarityParam specifying threshold=0.7 and n=2 to perform feature grouping based on EIC similarity correlation"
- [other] Generate overlay EIC plots for feature groups FG.013.001 and FG.045.001 using the plotEICs() or comparable visualization function to display peak shape similarity.: "Generate overlay EIC plots for feature groups FG.013.001 and FG.045.001 using the plotEICs() or comparable visualization function to display peak shape similarity."
