---
name: feature-frequency-filtering-imaging
description: Use when after peak alignment across all spectra in an imaging dataset, use this skill when you have detected many peaks but need to reduce false positives and sparse features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - Cardinal
  - R
  - Cardinal 3.6
  - BiocParallel
derived_from:
- doi: 10.1093/bioinformatics/btv146
  title: Cardinal
evidence_spans:
- library(Cardinal)
- '*Cardinal 3.6* is a major update with breaking changes. It bring support many of the new low-level signal processing functions'
- 'Once installed, Cardinal can be loaded with library(): library(Cardinal)'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cardinal_cq
    doi: 10.1093/bioinformatics/btv146
    title: Cardinal
  dedup_kept_from: coll_cardinal_cq
schema_version: 0.2.0
---

# feature-frequency-filtering-imaging

## Summary

Filter mass spectrometry imaging features (peaks) by their frequency of occurrence across the spatial dataset, retaining only those present in a minimum fraction of pixels. This skill reduces noise and feature dimensionality while preserving biologically relevant peaks in MSImagingExperiment objects.

## When to use

After peak alignment across all spectra in an imaging dataset, use this skill when you have detected many peaks but need to reduce false positives and sparse features. Apply it when you want to retain only peaks that appear consistently across >10% (or another threshold) of pixels, ensuring the final feature set reflects reproducible spectral signatures rather than noise or instrument artifacts.

## When NOT to use

- Input peaks have not been aligned across spectra; run peakAlign() first.
- You are filtering based on intensity, m/z range, or other criteria unrelated to spatial frequency.
- Your analysis requires all detected peaks, including rare or unique spatial signatures; frequency filtering may discard biologically meaningful minority features.

## Inputs

- MSImagingExperiment object with aligned peaks from peakAlign()
- featureData containing detected and aligned peaks across all spectra

## Outputs

- Filtered MSImagingExperiment object with reduced featureData
- Subset of peaks passing the frequency threshold (e.g., 37 retained peaks)

## How to apply

First, load the MSImagingExperiment object containing aligned peaks from peakAlign(). Then apply subsetFeatures() with a frequency threshold (e.g., > 0.1 for >10% pixel occurrence). The function filters featureData to retain only peaks meeting the frequency criterion. Verify the result by checking that the resulting MSImagingExperiment's featureData contains the expected number of peaks (e.g., 37 in the reference workflow). The frequency threshold should be tuned based on your imaging resolution, sample heterogeneity, and downstream analysis goals—higher thresholds yield more conservative, spatially robust feature sets.

## Related tools

- **Cardinal** (Provides peakAlign() for spectral peak alignment and subsetFeatures() for frequency-based filtering of MSImagingExperiment objects) — github.com/kuwisdelu/Cardinal
- **Cardinal 3.6** (Updated MSImagingExperiment class and spectral processing functions supporting peak alignment and feature subsetting workflows) — github.com/kuwisdelu/Cardinal
- **BiocParallel** (Optional: enables parallel processing of filtering operations across large imaging datasets)

## Examples

```
# After peakAlign() has been applied:
data_filtered <- subsetFeatures(data_aligned, features = which(featureFrequency(data_aligned) > 0.1))
# Verify result:
nrow(featureData(data_filtered))  # Should equal 37 or target count
```

## Evaluation signals

- The resulting MSImagingExperiment contains exactly the expected number of peaks (verify featureData row count matches target, e.g., 37 peaks).
- All retained peaks have frequency values ≥ the threshold (e.g., all > 0.1); spot-check a random sample of featureData.
- Spatial distribution of retained peaks is consistent across pixels; visualize using image() to confirm peaks are not concentrated in isolated regions.
- The filtering step removes spurious or low-frequency noise peaks; compare featureData before and after to confirm dimensionality reduction.
- Downstream statistical analysis (e.g., PCA, clustering via spatialKMeans) produces interpretable spatial patterns using the filtered feature set.

## Limitations

- Frequency filtering is conservative and may discard rare but biologically meaningful peaks present in <10% of pixels; tune the threshold carefully for your application.
- The method assumes peak alignment was successful; misaligned peaks will have artificially reduced frequencies and may be incorrectly filtered out.
- Frequency filtering does not account for peak intensity, signal-to-noise ratio, or biological relevance; combine with intensity-based or annotation-based filtering for more refined feature selection.
- Very heterogeneous samples with spatially localized metabolites may lose important features if the frequency threshold is set too high.

## Evidence

- [other] Subset features using subsetFeatures() with a frequency threshold of > 0.1 to retain only peaks present in >10% of pixels.: "Subset features using subsetFeatures() with a frequency threshold of > 0.1 to retain only peaks present in >10% of pixels."
- [other] After filtering to peaks with frequencies > 0.1, the resulting MSImagingExperiment contains exactly 37 peaks in featureData.: "After filtering to peaks with frequencies > 0.1, the resulting MSImagingExperiment contains exactly 37 peaks in featureData."
- [other] Apply peakAlign() to align detected peaks across all spectra in the imaging dataset.: "Apply peakAlign() to align detected peaks across all spectra in the imaging dataset."
- [intro] Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra: "Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra"
- [intro] Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option: "Parallel processing support via the BiocParallel package for all pre-processing methods and any statistical analysis methods with a BPPARAM option"
