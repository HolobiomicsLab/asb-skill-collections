---
name: eigenvector-digitization-into-compartment-bins
description: Use when you have computed eigenvector values from a prior eigs_cis calculation on a cooler Hi-C matrix and need to classify genomic regions into discrete A/B compartment categories before performing saddle analysis or computing compartment-level contact asymmetry metrics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
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

# eigenvector-digitization-into-compartment-bins

## Summary

Discretize continuous eigenvector values from Hi-C compartment analysis into categorical bins (typically 2–5 levels) representing A/B compartment states using quantile or fixed thresholds. This preprocessing step converts a continuous genomic track into a discrete compartment assignment required for downstream saddle plot analysis and compartment interaction quantification.

## When to use

You have computed eigenvector values from a prior eigs_cis calculation on a cooler Hi-C matrix and need to classify genomic regions into discrete A/B compartment categories before performing saddle analysis or computing compartment-level contact asymmetry metrics.

## When NOT to use

- Eigenvector values are missing or NaN for large fractions of the genome (no meaningful bins can be defined)
- The eigenvector track and cooler have mismatched bin resolutions or genomic coordinates
- You are performing continuous (non-binned) compartment strength analysis and do not need discrete categorical assignments

## Inputs

- cooler Hi-C matrix file (h5 format)
- eigenvector track (1D numpy array or bedGraph, indexed by genomic bins)
- binning parameters (bin edges, quantile thresholds, or bin count)

## Outputs

- digitized compartment track (1D array of integer bin labels, same length as input eigenvector)
- bin boundary definitions or threshold values used for digitization

## How to apply

Load the eigenvector track (a 1D array indexed by genomic bins) alongside the cooler Hi-C object. Apply cooltools.digitize to partition eigenvector values according to quantile-based or fixed thresholds into 2–5 discrete bins, each representing a compartment strength class. The choice of binning strategy (quantile vs. fixed threshold) should reflect whether you prioritize balanced bin populations or absolute eigenvector magnitude cutoffs. Validate that the output digitized track has the correct length (matching the number of bins in the cooler) and that bin labels are numeric (typically 0–4). This discretized track is then passed to cooltools.saddle to aggregate contact frequencies by compartment pair.

## Related tools

- **cooltools** (Provides the digitize function to bin eigenvector values into discrete compartment categories) — https://github.com/open2c/cooltools
- **cooler** (Stores and provides access to the Hi-C contact matrix and associated genomic bin metadata) — https://github.com/open2c/cooler
- **Python** (Scripting environment for loading, manipulating, and validating eigenvector and cooler data)

## Examples

```
from cooltools import digitize; import cooler; c = cooler.Cooler('sample.cool'); digitized = digitize(eigenvector_track, bins=5, method='quantile'); saddle_matrix = cooltools.saddle(c, digitized)
```

## Evaluation signals

- Output digitized array length matches the input eigenvector length and the cooler bin count
- All bin labels are numeric integers within the expected range (e.g., 0–4 for 5 bins)
- Bin boundary thresholds monotonically increase (for quantile binning, quantile values should span [0, 1])
- No NaN or invalid values remain in the digitized output; missing eigenvector values are either masked or handled consistently
- Downstream saddle analysis on the digitized track produces a valid 2D saddle matrix with positive contact frequencies and interpretable A/B compartment interaction patterns

## Limitations

- Digitization is lossy: continuous eigenvector information is discarded; results depend on the choice of bin edges and bin count
- Regions with missing or very low eigenvector values (e.g., pericentromeric or heterochromatic regions) may be over- or under-represented in boundary bins
- The API and smoothing behavior for eigenvector tracks is still under development in cooltools; parameter names and defaults may change between releases
- Digitization assumes eigenvector values are approximately unimodal or bimodal; multimodal or highly skewed distributions may not digitize cleanly into interpretable compartment bins

## Evidence

- [other] Apply cooltools.digitize to bin the eigenvector values into discrete compartment categories (typically 2–5 bins) according to quantile or fixed thresholds.: "Apply cooltools.digitize to bin the eigenvector values into discrete compartment categories (typically 2–5 bins) according to quantile or fixed thresholds."
- [other] Load a cooler file and an associated eigenvector track (e.g., from a prior eigs_cis calculation).: "Load a cooler file and an associated eigenvector track (e.g., from a prior eigs_cis calculation)."
- [other] Call cooltools.saddle with the digitized track and cooler object to compute the 2D saddle matrix aggregating Hi-C contact frequency by compartment pair.: "Call cooltools.saddle with the digitized track and cooler object to compute the 2D saddle matrix aggregating Hi-C contact frequency by compartment pair."
- [other] cooltools provides saddle analysis functionality as part of its high-resolution Hi-C analysis toolkit, operating on cooler-format datasets that store high-resolution contact matrices and associated genomic tracks.: "cooltools provides saddle analysis functionality as part of its high-resolution Hi-C analysis toolkit, operating on cooler-format datasets that store high-resolution contact matrices and associated"
- [readme] The recently-introduced cooler format readily handles storage of high-resolution datasets via a sparse data model.: "The recently-introduced cooler format readily handles storage of high-resolution datasets via a sparse data model."
