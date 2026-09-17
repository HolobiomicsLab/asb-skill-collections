---
name: mass-spectrometry-peak-validation
description: Use when after peak alignment across all spectra in an MSImagingExperiment
  using peakAlign(), when you need to reduce the feature set to high-confidence peaks
  by removing spurious or low-frequency detections.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Cardinal
  - R
  - Cardinal 3.6
  techniques:
  - MS-imaging
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btv146
  title: Cardinal
evidence_spans:
- library(Cardinal)
- '*Cardinal 3.6* is a major update with breaking changes. It bring support many of
  the new low-level signal processing functions'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-peak-validation

## Summary

Validate and filter aligned mass spectrometry imaging peaks by applying frequency thresholds to retain only peaks present across a sufficient proportion of pixels, reducing noise and ensuring statistical robustness of the feature set for downstream analysis.

## When to use

After peak alignment across all spectra in an MSImagingExperiment using peakAlign(), when you need to reduce the feature set to high-confidence peaks by removing spurious or low-frequency detections. Apply this skill when the aligned peak list contains many peaks with variable occurrence rates and you need to establish a minimum presence threshold (e.g., peaks appearing in >10% of pixels) before statistical or clustering analysis.

## When NOT to use

- Input peaks have not yet been aligned across spectra using peakAlign()
- Peak frequency or occurrence metadata is unavailable in the MSImagingExperiment
- You require peaks at any detection frequency, including rare/single-pixel peaks for exploratory analysis

## Inputs

- MSImagingExperiment object with peakAlign() already applied
- featureData containing aligned peak m/z values and detection frequencies

## Outputs

- MSImagingExperiment object with filtered featureData
- Subset of peaks meeting the frequency threshold

## How to apply

Load the MSImagingExperiment object containing peaks aligned across the imaging dataset via peakAlign(). Apply the subsetFeatures() function with a frequency threshold parameter (e.g., frequency > 0.1) to retain only peaks detected in more than the specified fraction of pixels. The resulting MSImagingExperiment featureData will contain a filtered set of high-confidence peaks. Verify the output by inspecting the featureData to confirm the expected number of peaks remain—this reduces false positives and ensures downstream statistical methods operate on reproducible, robust features across the spatial domain.

## Related tools

- **Cardinal** (provides peakAlign(), subsetFeatures(), and MSImagingExperiment data structure for peak filtering workflow) — github.com/kuwisdelu/Cardinal
- **Cardinal 3.6** (major update with redesigned class hierarchy and updated MSImagingExperiment class supporting out-of-memory datasets) — github.com/kuwisdelu/Cardinal
- **R** (execution environment for Cardinal library and subsetFeatures() function calls)

## Examples

```
mse_filtered <- subsetFeatures(mse_aligned, features = which(rowData(mse_aligned)$frequency > 0.1)); nrow(mse_filtered)
```

## Evaluation signals

- The resulting MSImagingExperiment featureData contains exactly the expected number of peaks matching the frequency threshold (e.g., 37 peaks for frequency > 0.1 in the reference task)
- All peaks in the filtered featureData have occurrence frequencies ≥ the specified threshold across the imaging pixel set
- No peaks below the threshold remain in the output featureData
- The structure and dimensions of the MSImagingExperiment are preserved, with only the feature subset reduced
- Peaks can be traced back to their original aligned m/z values without data corruption or loss of spatial metadata

## Limitations

- Frequency threshold choice is arbitrary and dataset-dependent; no universal cutoff recommended in the article
- The skill assumes peak alignment has already been performed; misaligned peaks will propagate biased frequencies
- Very stringent frequency thresholds may remove biologically relevant but spatially rare peaks from heterogeneous tissues
- Peak frequency alone does not account for intensity, signal-to-noise, or spatial distribution patterns

## Evidence

- [other] After filtering to peaks with frequencies > 0.1, the resulting MSImagingExperiment contains exactly 37 peaks in featureData.: "After filtering to peaks with frequencies > 0.1, the resulting MSImagingExperiment contains exactly 37 peaks in featureData."
- [other] Subset features using subsetFeatures() with a frequency threshold of > 0.1 to retain only peaks present in >10% of pixels.: "Subset features using subsetFeatures() with a frequency threshold of > 0.1 to retain only peaks present in >10% of pixels."
- [intro] Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra: "Updated MSImagingExperiment class with a new counterpart MSImagingArrays class for better representing raw spectra"
- [other] Apply peakAlign() to align detected peaks across all spectra in the imaging dataset.: "Apply peakAlign() to align detected peaks across all spectra in the imaging dataset."
