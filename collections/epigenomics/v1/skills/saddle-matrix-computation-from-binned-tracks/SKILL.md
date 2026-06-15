---
name: saddle-matrix-computation-from-binned-tracks
description: Use when you have a cooler Hi-C contact matrix file and an associated eigenvector track (from prior eigs_cis calculation or similar), and you need to quantify the preferential interaction patterns between A and B chromatin compartments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0654
  tools:
  - cooltools
  - cooler
  - Python
derived_from:
- doi: 10.1371/journal.pcbi.1012067
  title: cooltools
- doi: 10.1101/2022.10.31.514564
  title: ''
evidence_spans:
- cooltools provides a suite of computational tools with a paired python API
- cooltools leverages this format to enable flexible and reproducible analysis of high-resolution data.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cooltools
    doi: 10.1371/journal.pcbi.1012067
    title: cooltools
  dedup_kept_from: coll_cooltools
schema_version: 0.2.0
---

# saddle-matrix-computation-from-binned-tracks

## Summary

Compute a 2D saddle matrix that aggregates Hi-C contact frequency by genomic compartment pair, quantifying A/B compartment interaction asymmetry. This skill transforms digitized eigenvector tracks (binned into discrete compartment categories) and a cooler Hi-C contact matrix into a saddle strength metric and full saddledata array.

## When to use

You have a cooler Hi-C contact matrix file and an associated eigenvector track (from prior eigs_cis calculation or similar), and you need to quantify the preferential interaction patterns between A and B chromatin compartments. Use this skill when you want to measure compartment organization strength via the saddle plot, a classical 2D aggregation metric in genome architecture analysis.

## When NOT to use

- Eigenvector track is missing or not yet computed from the Hi-C matrix.
- Hi-C data is not in cooler format or lacks bin-level coordinate metadata.
- Your goal is to visualize contact maps directly rather than quantify compartment interaction patterns.

## Inputs

- cooler file (.cool or .mcool) containing binned Hi-C contact matrix
- eigenvector track array (continuous values per genomic bin, e.g. from eigs_cis)
- compartment binning parameters (number of bins or quantile thresholds)

## Outputs

- saddle matrix (2D NumPy array, shape: n_bins × n_bins)
- saddledata (untransformed saddle matrix, typically saved to NPZ file)
- saddle strength (scalar float quantifying A/B compartment interaction asymmetry)
- digitized track (binned eigenvector values, integer class labels per bin)

## How to apply

First, load the cooler file and its paired eigenvector track using cooler and bioframe APIs. Apply cooltools.digitize to bin the continuous eigenvector values into discrete compartment categories (typically 2–5 bins defined by quantiles or fixed thresholds). Call cooltools.saddle with the digitized track and cooler object to compute the 2D saddle matrix aggregating contact frequency by compartment pair. The saddle function performs quantile-based binning and cross-tabulation, producing both the untransformed saddledata array and a saddle strength scalar. Extract and validate the NPZ output file structure, confirm matrix dimensions match the number of bins, and verify saddle strength falls within expected ranges (typically 0–1 or higher for strong compartmentalization). The key rationale is that the digitized track reduces continuous variation to discrete classes, enabling robust aggregation across many loci.

## Related tools

- **cooltools** (Core library providing cooltools.saddle and cooltools.digitize functions for compartment binning and saddle matrix computation) — https://github.com/open2c/cooltools
- **cooler** (Format and API for storing and accessing high-resolution Hi-C contact matrices and bin metadata) — https://github.com/open2c/cooler
- **Python** (Execution environment and NumPy/SciPy backend for array operations and aggregation)

## Examples

```
from cooltools import saddle, digitize; import cooler; c = cooler.Cooler('data.cool'); track = c.bins[:]['eigenvector']; digitized = digitize(track, n_bins=3); saddledata, saddle_strength = saddle(c, track=digitized)
```

## Evaluation signals

- NPZ output file exists and contains saddledata array with correct shape (n_bins, n_bins).
- Saddle strength scalar is a finite float within the expected range for the input dataset (typically 0–1 or higher for strong A/B segregation).
- Digitized track contains only integer bin labels matching the specified number of bins (e.g., 0, 1, 2 for 3 bins).
- Saddle matrix diagonal elements (within-compartment pairs) are higher than off-diagonal elements (across-compartment pairs), indicating expected compartment homophily.
- Matrix dimensions equal n_bins × n_bins and are symmetric or near-symmetric, reflecting the symmetric nature of Hi-C contacts.

## Limitations

- The saddle.mask_bad_bins method for filtering bins based on Hi-C quality thresholds is available but requires separate application; the core saddle function does not automatically exclude low-quality bins.
- The eigenvector sign is ambiguous (can be flipped); users must define a convention to ensure consistent A/B assignment across replicates or cell types.
- Saddle strength is sensitive to the choice of binning strategy (number of bins and quantile thresholds); results are not directly comparable across different digitization schemes.

## Evidence

- [other] Apply cooltools.digitize to bin the eigenvector values into discrete compartment categories (typically 2–5 bins) according to quantile or fixed thresholds.: "Apply cooltools.digitize to bin the eigenvector values into discrete compartment categories (typically 2–5 bins) according to quantile or fixed thresholds"
- [other] Call cooltools.saddle with the digitized track and cooler object to compute the 2D saddle matrix aggregating Hi-C contact frequency by compartment pair.: "Call cooltools.saddle with the digitized track and cooler object to compute the 2D saddle matrix aggregating Hi-C contact frequency by compartment pair"
- [other] Extract and save the saddledata array (untransformed) to an NPZ file and compute saddle strength as a scalar metric quantifying A/B compartment interaction asymmetry.: "Extract and save the saddledata array (untransformed) to an NPZ file and compute saddle strength as a scalar metric quantifying A/B compartment interaction asymmetry"
- [other] Validate output by confirming NPZ file structure, matrix dimensions, and saddle strength value are within expected ranges for the input dataset.: "Validate output by confirming NPZ file structure, matrix dimensions, and saddle strength value are within expected ranges for the input dataset"
- [other] cooltools provides saddle analysis functionality as part of its high-resolution Hi-C analysis toolkit, operating on cooler-format datasets that store high-resolution contact matrices and associated genomic tracks.: "Cooltools provides saddle analysis functionality as part of its high-resolution Hi-C analysis toolkit, operating on cooler-format datasets that store high-resolution contact matrices and associated"
- [readme] The recently-introduced cooler format readily handles storage of high-resolution datasets via a sparse data model.: "The recently-introduced cooler format readily handles storage of high-resolution datasets via a sparse data model"
- [readme] Compartments and Saddles: how to extract eigenvectors and create saddleplots reflecting A/B compartments.: "Compartments and Saddles: how to extract eigenvectors and create saddleplots reflecting A/B compartments"
- [other] Added saddle.mask_bad_bins method to filter bins in a track based on Hi-C bin-level filtering: "Added saddle.mask_bad_bins method to filter bins in a track based on Hi-C bin-level filtering"
