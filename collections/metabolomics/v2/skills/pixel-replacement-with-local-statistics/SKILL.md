---
name: pixel-replacement-with-local-statistics
description: Use when lA-ICP-MS image data contains isolated spike outliers (single or few pixels with anomalously high or low intensities relative to their local neighborhood) that distort quantitative analysis or visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3050
  tools:
  - pewpew
  - pewlib
  - Python
derived_from:
- doi: 10.1021/acs.analchem.1c02138
  title: Pew2
- doi: 10.1529/biophysj.103.038422
  title: ''
evidence_spans:
- The built in `Filtering Tool` removes spikes by comparing pixel values to a locally defined threshold
- '|pewpew| is an open-source LA-ICP-MS data import and processing application'
- based on the python library pewlib_
- python library [pewlib]
- python library
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pew2_cq
    doi: 10.1021/acs.analchem.1c02138
    title: Pew2
  dedup_kept_from: coll_pew2_cq
schema_version: 0.2.0
---

# pixel-replacement-with-local-statistics

## Summary

Replace outlier pixels in LA-ICP-MS image data by comparing each pixel against a local rolling-window statistic (median or mean) and substituting values that exceed a threshold with the corresponding local statistic. This removes spike artifacts while preserving spatial structure in elemental distribution maps.

## When to use

Apply this skill when LA-ICP-MS image data contains isolated spike outliers (single or few pixels with anomalously high or low intensities relative to their local neighborhood) that distort quantitative analysis or visualization. Typical triggers: raw pixel intensity distributions show heavy tails, visual inspection reveals salt-and-pepper noise, or filtering is required before downstream image alignment, region selection, or calibration export.

## When NOT to use

- Input contains valid sharp compositional boundaries or true elemental peaks that should not be smoothed; Rolling filters will blur legitimate fine structure.
- Spike artifacts are systematic rather than isolated (e.g., entire detector strip malfunction); bulk correction or rejection of affected data is more appropriate.
- Data has already been spike-corrected by hardware or instrument software; reapplication may over-smooth legitimate signal.

## Inputs

- Raw LA-ICP-MS image data (line-by-line, spot-wise, or ablation-time-aligned)
- Pixel intensity matrix (2D or multi-channel)
- Window size (integer: 3, 5, or 7 pixels)
- Threshold parameter (M in medians or σ in standard deviations)

## Outputs

- Filtered LA-ICP-MS image with spike outliers replaced
- New image layer or exported filtered image file
- Difference map (optional: original minus filtered, showing replaced pixels)

## How to apply

Load raw LA-ICP-MS image data into pewpew. Choose the filter type: Rolling Median (threshold M = distance in medians from local median) or Rolling Mean (threshold σ = distance in standard deviations from local mean). Set window size (typical values 3, 5, or 7 pixels) and threshold parameter. The filter compares each pixel's absolute deviation against the chosen threshold using the local statistic calculated from the neighborhood excluding the tested pixel itself. Pixels exceeding the threshold are replaced with the corresponding local median or mean value. Apply the filter across all pixels and layers. Output the filtered image as a new layer or export. Parameter choice depends on data distribution: Rolling Median is robust to extreme outliers; Rolling Mean is more sensitive to small deviations and better for removing systematic bias.

## Related tools

- **pewpew** (GUI for importing, visualizing, and applying Rolling Median/Mean filters to LA-ICP-MS image data) — https://github.com/djdt/pewpew
- **pewlib** (Python library implementing Rolling Median and Rolling Mean filter kernels and pixel replacement logic) — https://github.com/djdt/pewlib
- **Python** (Language for scripting filter application and batch processing of LA-ICP-MS images via pewlib)

## Evaluation signals

- Verify pixel-level replacement: confirm that pixels with absolute deviation > threshold (in medians or stddevs) were replaced; pixels below threshold remain unchanged.
- Check output image schema: filtered image has same spatial dimensions and data type as input; no NaN or Inf values introduced except at image boundaries (if applicable).
- Visual inspection: spike/noise artifacts should be visually attenuated; local spatial structure and elemental boundaries should remain intact; compare before/after histograms and look for reduced tail in intensity distribution.
- Stability check: re-running the same filter on the same input with identical parameters produces identical output.
- Downstream performance: filtered image should show improved visual clarity, more consistent region-of-interest statistics, and reduced noise when exported for calibration or quantitation steps.

## Limitations

- Window size and threshold are manual hyperparameters; no automatic selection provided in pewpew. Suboptimal choices can either over-smooth valid signal or leave outliers undetected.
- Rolling Median and Rolling Mean assume outliers are sparse and localized; dense noise or spatially correlated artifacts may not be well removed.
- Excludes the tested pixel itself from the local statistic, which can cause edge effects near image boundaries or interfaces between distinct compositional regions.
- Effectiveness depends on the noise model: Rolling filters work best for Gaussian or symmetric heavy-tailed noise; systematic detector artifacts or drift are not addressed.

## Evidence

- [other] Rolling Median filtering compares each pixel against a local median value and uses a threshold M (distance in medians from the local median) to identify and replace outlier pixels.: "Rolling Median filtering compares each pixel against a local median value and uses a threshold M (distance in medians from the local median) to identify and replace outlier pixels."
- [other] Set the window size (typical values: 3, 5, or 7 pixels) and the threshold parameter according to the chosen filter. Apply the filter to identify pixels where the absolute deviation exceeds the threshold. Replace outlier pixels with the corresponding local median (Rolling Median) or local mean (Rolling Mean), excluding the tested pixel from the local statistic.: "Set the window size (typical values: 3, 5, or 7 pixels) and the threshold parameter according to the chosen filter. Apply the filter to identify pixels where the absolute deviation exceeds the"
- [readme] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data"
- [readme] Pewlib is a library for importing, processing and exporting LA-ICP-MS data.: "Pewlib is a library for importing, processing and exporting LA-ICP-MS data."
