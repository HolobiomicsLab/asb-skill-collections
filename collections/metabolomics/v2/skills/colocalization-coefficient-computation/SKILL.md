---
name: colocalization-coefficient-computation
description: Use when you have two co-registered LA-ICP-MS element channel images and need to quantify whether their spatial distributions are statistically correlated or independent. Use it specifically when investigating whether two elements co-occur spatially (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3500
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

# colocalization-coefficient-computation

## Summary

Quantifies spatial relationships between two co-registered element channels in LA-ICP-MS images by computing Pearson R, Li ICQ, and Manders coefficients (via Costes thresholding). This skill enables detection and measurement of elemental colocalization patterns critical for understanding spatial distribution relationships in imaging mass spectrometry data.

## When to use

Apply this skill when you have two co-registered LA-ICP-MS element channel images and need to quantify whether their spatial distributions are statistically correlated or independent. Use it specifically when investigating whether two elements co-occur spatially (e.g., in tissue samples), or when comparing colocalization strength across multiple sample regions or conditions.

## When NOT to use

- Input channels are not spatially co-registered or have different pixel sizes — colocalization coefficients will be meaningless if spatial alignment is poor.
- Single channel or unregistered images — colocalization requires paired, aligned data.
- Fully synthetic or noise-only images — real colocalization cannot be detected in absence of signal structure.

## Inputs

- Two co-registered LA-ICP-MS element channel images (same spatial dimensions and pixel alignment)
- Selected region of interest (optional; if not specified, entire image region is used)
- Intensity threshold parameters for Costes method (optional; method auto-determines if not specified)

## Outputs

- Pearson R coefficient (correlation strength, range −1 to +1)
- Pearson R probability (ρ) from random shuffle comparison (if requested)
- Li ICQ coefficient (intensity correlation quotient, range −0.5 to +0.5)
- Manders M1 and M2 coefficients (fraction of ch1 colocalizing with ch2, and vice versa, range 0 to 1)
- Exported coefficient table (via context menu or clipboard)

## How to apply

Load two co-registered element images (channels) into the Colocalisation Dialog via the image or selection context menu in pewpew. Compute Li ICQ coefficient over the entire image region to assess correlation independent of intensity. Compute Pearson R coefficient and optionally its probability (ρ) by comparing the R value to those of random shuffles of the input data to assess statistical significance. Compute Manders coefficients using the Costes thresholding method on the image or selected region to quantify the fraction of each channel overlapping with the other above threshold. The Costes method automatically determines intensity thresholds to reduce noise-driven false colocalization. Display all coefficients in the dialog left panel and export results via context menu or copy-to-clipboard for downstream analysis.

## Related tools

- **pewpew** (GUI application that hosts the Colocalisation Dialog and loads, aligns, and processes LA-ICP-MS images prior to coefficient computation) — https://github.com/djdt/pewpew
- **pewlib** (Python library underlying pewpew that implements coefficient computation algorithms and image processing operations) — https://github.com/djdt/pewlib

## Evaluation signals

- Pearson R and Li ICQ coefficients lie within their theoretical ranges (R: −1 to +1; ICQ: −0.5 to +0.5) and are consistent with visual inspection of channel overlap.
- Manders M1 and M2 coefficients each fall in range [0, 1] and sum is not constrained (they measure independent fractions of overlap).
- Pearson R probability (ρ) is smaller for genuinely colocalized channels than for random shuffles of the same data, confirming statistical significance.
- Costes thresholding produces integer threshold values for each channel that exclude low-intensity noise voxels; verify that thresholds do not eliminate signal-bearing voxels.
- Coefficients computed on selected region match those on full image when region contains the region of interest; values should be robust to region choice if colocalization is genuine and locally uniform.

## Limitations

- Pearson R and Li ICQ are sensitive to intensity bias and can be inflated by systematic differences in signal level between channels; use Manders coefficients as complementary metrics to assess overlap independent of intensity.
- Costes thresholding method assumes Gaussian noise model; performance degrades on heavy-tailed or outlier-rich noise distributions common in some LA-ICP-MS acquisitions.
- Colocalization coefficients measure spatial overlap but do not establish causation or functional interaction; high colocalization can reflect coincidental spatial distribution rather than true biological association.
- Results are valid only for co-registered images; even small misalignment (subpixel) can substantially reduce coefficient values and lead to false negatives.

## Evidence

- [other] The Colocalisation Dialog computes Pearson R, Li ICQ, and Manders coefficients (via Costes thresholding method) to quantify spatial relationships between two element channels in co-registered images.: "The Colocalisation Dialog computes Pearson R, Li ICQ, and Manders coefficients (via Costes thresholding method) to quantify spatial relationships between two element channels in co-registered images."
- [other] Load two co-registered element images (channels) into the Colocalisation Dialog via image or selection context menu. Compute Li ICQ coefficient over the entire image region. Compute Pearson R coefficient over the entire image region and optionally calculate its probability (ρ) by comparing the R value to those of random shuffles of the input.: "Load two co-registered element images (channels) into the Colocalisation Dialog via image or selection context menu. Compute Li ICQ coefficient over the entire image region. Compute Pearson R"
- [other] Compute Manders coefficients using the Costes thresholding method on the image or selected region. Display all calculated coefficients in the dialog left panel and enable export via context menu or copy-to-clipboard.: "Compute Manders coefficients using the Costes thresholding method on the image or selected region. Display all calculated coefficients in the dialog left panel and enable export via context menu or"
- [readme] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib"
- [readme] Pewlib is a library for importing, processing and exporting LA-ICP-MS data.: "Pewlib is a library for importing, processing and exporting LA-ICP-MS data."
