---
name: spatial-overlap-quantification
description: Use when you have two co-registered LA-ICP-MS element channel images and need to determine whether their spatial distributions are correlated.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3452
  - http://edamontology.org/topic_0092
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

# Spatial Overlap Quantification

## Summary

Quantify spatial colocalization between two co-registered element channels in LA-ICP-MS images using Pearson R, Li ICQ, and Manders coefficients (via Costes-based thresholding). This skill enables objective assessment of whether two elemental distributions overlap spatially beyond random chance.

## When to use

Apply this skill when you have two co-registered LA-ICP-MS element channel images and need to determine whether their spatial distributions are correlated. Use it when you want to move beyond visual inspection to obtain quantitative, reproducible overlap metrics suitable for statistical comparison across multiple samples or regions.

## When NOT to use

- Images are not co-registered or pixel-aligned; perform image alignment first.
- You are analyzing a single element channel or comparing an element to a non-spatial property (e.g., time series intensity); this skill requires at least two spatially overlaid channels.
- Your research goal is purely qualitative assessment or visualization; colocalization coefficients add precision but require interpretation alongside visual inspection.

## Inputs

- Two co-registered LA-ICP-MS element channel images (in pewpew-supported formats: Agilent .b, Thermo CSV/LDR, PerkinElmer ELAN .xl, Nu Vitesse, or delimited CSV)
- Optional region-of-interest selection mask for focused analysis

## Outputs

- Pearson R coefficient (correlation strength, range −1 to +1)
- Pearson R probability (ρ, estimated from random shuffles)
- Li ICQ coefficient (independent colocalization quotient)
- Manders M1 and M2 coefficients (fraction of channel 1 and 2 signal colocalizing)
- Exported coefficient table or clipboard-ready summary

## How to apply

Load two co-registered element images into the Colocalisation Dialog via image or selection context menu. Compute Li ICQ coefficient over the entire image region or selected area to detect non-random spatial association. Compute Pearson R coefficient and optionally calculate its probability (ρ) by comparing the R value to those of random shuffles of the input image to assess statistical significance. Compute Manders coefficients using the Costes thresholding method to quantify the fraction of each channel's signal that colocalizes with the other. Display and export all coefficients together to enable integrated interpretation of overlap strength, direction, and statistical support.

## Related tools

- **pewpew** (GUI container for loading co-registered LA-ICP-MS images, invoking the Colocalisation Dialog, and exporting computed coefficients) — https://github.com/djdt/pewpew
- **pewlib** (Python library underlying pewpew; provides image import, preprocessing, and coefficient computation APIs for scripted colocalization workflows) — https://github.com/djdt/pewlib

## Evaluation signals

- Pearson R value is within expected range [−1, +1]; probability (ρ) is between 0 and 1 and reflects statistical significance relative to randomized shuffles.
- Manders M1 and M2 coefficients are each in the range [0, 1], representing the fraction of each channel colocalizing after Costes thresholding.
- Li ICQ is non-zero and consistent with visual inspection; positive ICQ suggests non-random colocalization, negative suggests segregation.
- Computed coefficients on the same image pair are reproducible when recalculated; identical region selections yield identical coefficient values.
- Coefficients exported to clipboard or file match displayed values in the Colocalisation Dialog left panel with no rounding errors beyond display precision.

## Limitations

- Colocalization coefficients are sensitive to image registration accuracy; misalignment will artificially reduce overlap metrics.
- Manders coefficients depend on the Costes thresholding method, which assumes a linear relationship between background and signal; may not be appropriate for highly non-linear intensity distributions.
- Pearson R can be inflated by extreme outlier pixels; visual inspection of coefficient histograms and regional variation is recommended.
- Li ICQ requires sufficient spatial variation in both channels to be meaningful; images with uniform or near-zero signal across regions may yield unstable coefficients.

## Evidence

- [other] Pearson R, Li ICQ, and Manders coefficients (via Costes thresholding method) to quantify spatial relationships: "The Colocalisation Dialog computes Pearson R, Li ICQ, and Manders coefficients (via Costes thresholding method) to quantify spatial relationships between two element channels in co-registered images."
- [other] Load two co-registered element images via context menu: "Load two co-registered element images (channels) into the Colocalisation Dialog via image or selection context menu."
- [other] Compute Li ICQ coefficient over the entire image region: "Compute Li ICQ coefficient over the entire image region."
- [other] Pearson R probability by comparing to random shuffles: "Compute Pearson R coefficient over the entire image region and optionally calculate its probability (ρ) by comparing the R value to those of random shuffles of the input."
- [other] Manders coefficients using Costes thresholding method: "Compute Manders coefficients using the Costes thresholding method on the image or selected region."
- [other] Display coefficients in dialog left panel and enable export: "Display all calculated coefficients in the dialog left panel and enable export via context menu or copy-to-clipboard."
- [readme] Pew² GUI for importing and processing LA-ICP-MS data: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib"
- [readme] Pewlib supports imports from multiple vendor formats: "Pewlib is a library for importing, processing and exporting LA-ICP-MS data. Currently exports from Agilent, Thermo and PerkinElmer software is supported, as well as delimited text images."
