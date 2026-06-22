---
name: la-icp-ms-image-denoising
description: Use when raw LA-ICP-MS images contain isolated spike pixels (hot spots or cold spots) caused by instrumental noise, transient ablation artifacts, or detector glitches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3382
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

# LA-ICP-MS Image Denoising via Rolling Median or Rolling Mean Filtering

## Summary

Remove spike outliers from LA-ICP-MS ablation images by comparing each pixel against a local rolling-window statistic (median or mean) and replacing outliers that exceed a user-defined threshold. This skill restores data quality before downstream quantification or image alignment.

## When to use

Apply this skill when raw LA-ICP-MS images contain isolated spike pixels (hot spots or cold spots) caused by instrumental noise, transient ablation artifacts, or detector glitches. Visual inspection or statistical profiling should reveal localized intensity anomalies that deviate sharply from their pixel neighbors. Use before image alignment, calibration application, or region-of-interest quantification.

## When NOT to use

- Image already exhibits systematic spatial structure at the scale of the window size—filtering may blur real fine features (e.g., sharp ablation boundaries, thin mineral veins).
- Spike prevalence is >50% of pixels—rolling-window filtering assumes spikes are minority outliers; heavy corruption requires alternative approaches (e.g., median-absolute-deviation-based masking, model-based reconstruction).
- Analysis requires preservation of transient temporal signals within a single pixel across replicate ablation passes—replacing individual time points may destroy kinetic information.

## Inputs

- Raw LA-ICP-MS image data (supported formats: Agilent .b, Thermo CSV/LDR, PerkinElmer ELAN, Nu Instruments Vitesse, CSV images, imzML)
- User-specified filter type (Rolling Median or Rolling Mean)
- Window size parameter (integer: 3, 5, 7, or other odd value)
- Threshold parameter (M for medians, σ for standard deviations)

## Outputs

- Filtered LA-ICP-MS image with spike outliers replaced by local statistic
- Optionally: difference map or flagged pixel coordinates for quality review
- Exportable layer or image file in pew² native or standard format

## How to apply

Load the raw LA-ICP-MS image data (line-by-line, spot-wise, or ablation-time-aligned format) into the Filtering Tool. Choose filter type: Rolling Median (threshold M = distance in medians from local median) for robust outlier suppression, or Rolling Mean (threshold σ = distance in standard deviations from local mean) for gentler smoothing. Set window size (typical 3, 5, or 7 pixels) to balance local context capture against over-smoothing. For each pixel, compute the local statistic (median or mean) excluding that pixel itself from a square neighborhood. Flag pixels where absolute deviation exceeds the threshold, then replace flagged pixels with the corresponding local statistic value. Export the filtered image as a new layer or file, comparing before/after histograms and spatial coherence to confirm spike removal without artifact introduction.

## Related tools

- **pewpew** (GUI platform for importing, visualizing, and applying Rolling Median/Rolling Mean filters to LA-ICP-MS images) — https://github.com/djdt/pewpew
- **pewlib** (Python library underlying pewpew; provides image I/O, filter logic, and data export for LA-ICP-MS workflows) — https://github.com/djdt/pewlib

## Evaluation signals

- Histogram of pixel intensities shows reduction or elimination of isolated extreme outlier bins while core distribution remains stable.
- Spatial coherence: filtered image shows smooth gradients within homogeneous regions and preserved sharp edges at known ablation or phase boundaries (visual QC or edge-detection metric).
- Pixel replacement count: report proportion of pixels flagged and replaced; typically <5–10% for well-tuned thresholds; >20% may indicate threshold too aggressive or data too noisy.
- Before/after line-scan profiles: outlier spikes should disappear; local mean/median values should be preserved in non-spiked regions.
- Consistency across replicates: filtered images from replicate sample ablations should show similar spatial patterns, confirming removal of instrumental artifacts rather than sample heterogeneity.

## Limitations

- Rolling-window filters blur or remove real fine-scale features (sub-window-sized inclusions, thin laminae) if window size is too large or threshold too low.
- Choice of window size and threshold is empirical and data-dependent; no universal guidance provided in the article for setting these parameters.
- Rolling Mean is sensitive to heavy-tailed or multimodal local distributions; Rolling Median is more robust but may perform poorly if spikes occupy >50% of pixels in a neighborhood.
- Filter is applied uniformly across all isotopes/channels; isotope-specific spike behavior (e.g., high background in one mass only) may require channel-specific thresholding (not discussed in article).
- No automated threshold selection algorithm mentioned; user must tune parameters manually or via trial-and-error, increasing workflow iteration time.

## Evidence

- [other] Rolling Median filtering compares each pixel against a local median value and uses a threshold M (distance in medians from the local median) to identify and replace outlier pixels.: "Rolling Median filtering compares each pixel against a local median value and uses a threshold M (distance in medians from the local median) to identify and replace outlier pixels."
- [other] Set the window size (typical values: 3, 5, or 7 pixels) and the threshold parameter according to the chosen filter.: "Set the window size (typical values: 3, 5, or 7 pixels) and the threshold parameter according to the chosen filter."
- [other] Replace outlier pixels with the corresponding local median (Rolling Median) or local mean (Rolling Mean), excluding the tested pixel from the local statistic.: "Replace outlier pixels with the corresponding local median (Rolling Median) or local mean (Rolling Mean), excluding the tested pixel from the local statistic."
- [readme] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib.: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib."
- [methods] Rolling Mean | σ | Distance in stddevs from the local mean: "Rolling Mean | σ | Distance in stddevs from the local mean"
