---
name: msimagingexperiment-subset-operations
description: Use when after peak alignment with peakAlign(), when you have an MSImagingExperiment with many detected peaks but want to retain only those present in a sufficient fraction of pixels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Cardinal
  - R
  - Cardinal 3.6
  - BiocParallel
  techniques:
  - mass-spectrometry
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btv146
  all_source_dois:
  - 10.1093/bioinformatics/btv146
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MSImagingExperiment subset operations

## Summary

Subset features in a Cardinal MSImagingExperiment object based on frequency thresholds to retain only peaks present in a minimum proportion of pixels. This skill filters detected and aligned peaks to reduce feature dimensionality while preserving spatially informative mass-to-charge ratios.

## When to use

After peak alignment with peakAlign(), when you have an MSImagingExperiment with many detected peaks but want to retain only those present in a sufficient fraction of pixels. Use this when peak sparsity is high and you need to focus statistical analysis on robustly observed features rather than rare or noisy peaks.

## When NOT to use

- Peak alignment has not yet been applied — subsetFeatures() operates on aligned peak sets, not raw detected peaks.
- You require all detected peaks for downstream statistical modeling that explicitly handles sparsity (e.g., zero-inflated models).
- Your analysis goal is to preserve rare or region-specific biomarkers that appear in <10% of pixels.

## Inputs

- MSImagingExperiment object (post-peakAlign)
- frequency threshold parameter (numeric, typically 0.0–1.0)

## Outputs

- MSImagingExperiment object with filtered featureData
- Subset of peaks meeting frequency criterion

## How to apply

Apply subsetFeatures() to the aligned MSImagingExperiment object with a frequency threshold parameter (e.g., freq > 0.1 to retain peaks present in >10% of pixels). The function filters the featureData by computing the proportion of non-zero or detected peaks in each m/z bin across all spectra and removes those failing the threshold. This reduces feature dimensionality while preserving peaks with consistent spatial or spectral support. Verify the output by checking the featureData of the resulting MSImagingExperiment to confirm the expected number of retained peaks.

## Related tools

- **Cardinal 3.6** (Provides peakAlign() for pre-subset peak alignment and subsetFeatures() for frequency-based filtering of MSImagingExperiment featureData) — https://github.com/kuwisdelu/Cardinal
- **R** (Execution environment for loading Cardinal library and running subset operations)
- **BiocParallel** (Optional parallel processing backend for accelerating subset operations on large imaging datasets)

## Examples

```
# Load Cardinal, import aligned MSImagingExperiment, and subset to peaks with frequency > 0.1
library(Cardinal)
mse_aligned <- peakAlign(mse_detected)
mse_filtered <- subsetFeatures(mse_aligned, freq > 0.1)
print(nrow(featureData(mse_filtered)))  # Should print 37
```

## Evaluation signals

- Verify featureData of the output MSImagingExperiment contains exactly the expected number of peaks after filtering (e.g., 37 peaks for freq > 0.1 threshold).
- Confirm all retained peaks have frequency ≥ threshold across the imaging dataset pixels.
- Check that no peaks below the frequency threshold remain in the output object.
- Validate that the m/z values and other feature annotations are preserved correctly in the filtered featureData.
- Compare feature count before and after subsetting to ensure expected magnitude of dimensionality reduction.

## Limitations

- Threshold selection (e.g., 0.1) is user-defined and may require empirical justification or sensitivity analysis; no guidance is provided in the article for threshold selection.
- Frequency is computed across all pixels; spatial heterogeneity or region-specific peaks with lower global frequency will be discarded.
- The skill assumes peaks are already aligned; misalignment prior to subsetting will produce spurious frequency counts.

## Evidence

- [other] Peak frequency filtering via subsetFeatures: "Subset features using subsetFeatures() with a frequency threshold of > 0.1 to retain only peaks present in >10% of pixels."
- [other] Output verification on featureData: "Verify that the featureData of the resulting MSImagingExperiment contains exactly 37 peaks."
- [intro] MSImagingExperiment class structure: "Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra"
- [other] Peak alignment prerequisite: "Apply peakAlign() to align detected peaks across all spectra in the imaging dataset."
