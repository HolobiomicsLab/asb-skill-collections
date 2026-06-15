---
name: compartment-strength-quantification
description: Use when when you have a binned Hi-C cooler file, an associated eigenvector track (from prior eigs_cis calculation), and need to measure how strongly the genome is partitioned into active (A) and inactive (B) compartments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2940
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

# compartment-strength-quantification

## Summary

Quantify the asymmetry of A/B compartment interactions in Hi-C contact matrices by computing saddle strength—a scalar metric derived from a 2D saddle matrix aggregating contact frequency by digitized eigenvector compartment pairs. This metric summarizes the degree to which the genome is partitioned into spatially segregated A and B compartments.

## When to use

When you have a binned Hi-C cooler file, an associated eigenvector track (from prior eigs_cis calculation), and need to measure how strongly the genome is partitioned into active (A) and inactive (B) compartments. Use this skill to produce a single scalar metric that quantifies compartment interaction asymmetry across a chromosome or genome, enabling comparison of compartmentalization strength across cell types, conditions, or timepoints.

## When NOT to use

- The input eigenvector track has not been validated or is from a different resolution/genome version than the cooler file—compartment calls must be derived from the same contact matrix.
- The cooler file contains fewer than ~5 kb resolution bins or has severe sparsity in high-interaction regions; saddle matrices require sufficient contact counts per bin pair to estimate meaningful interaction frequencies.
- You need strand-level or allele-specific compartment strength; saddle analysis aggregates across the entire input track and does not decompose by strand or haplotype.

## Inputs

- cooler file (.cool or .mcool) containing binned Hi-C contact matrix
- eigenvector track (1D array indexed by genomic bins, typically from eigs_cis)
- bin annotation table (bin_id, chrom, start, end for filtering/masking)

## Outputs

- 2D saddle matrix (saddledata array, shape n_bins × n_bins, contact frequency by compartment pair)
- saddle strength scalar (quantifies A/B compartment interaction asymmetry)
- NPZ file containing saddledata and metadata

## How to apply

First, load a cooler Hi-C matrix and its associated eigenvector track (typically computed from principal component analysis on the contact matrix). Apply cooltools.digitize to bin the continuous eigenvector values into discrete compartment categories, typically using 2–5 quantile-based bins (commonly 2 for A/B classification). Call cooltools.saddle with the digitized track and cooler object to compute the 2D saddle matrix, which aggregates contact frequency for all bin pairs of the two compartment types. Extract the untransformed saddledata array and compute saddle strength as a scalar metric—conventionally the log2 ratio of (A–A + B–B interactions) to (A–B interactions)—which quantifies the preferential self-interaction of each compartment type. Validate the computation by confirming the output array dimensions match expected (n_bins × n_bins), the NPZ file structure is intact, and the saddle strength value is within realistic bounds (typically 0.5–3.0 for mammalian genomes).

## Related tools

- **cooltools** (Core library providing digitize() and saddle() functions for binning eigenvector tracks and computing saddle matrices and strength metrics) — https://github.com/open2c/cooltools
- **cooler** (Sparse HDF5-based format for storage and retrieval of high-resolution contact matrices and associated genomic tracks) — https://github.com/open2c/cooler
- **Python** (Programming language for accessing cooltools API, handling eigenvector and cooler file I/O, and computing saddle strength metrics)

## Examples

```
from cooltools import saddle, digitize; import cooler; c = cooler.Cooler('sample.cool'); eigvec = eigvec_track_from_file('eigvec.txt'); digitized = digitize(eigvec, n_bins=2); s, saddledata = saddle(c, digitized); print(f'Saddle strength: {s:.2f}')
```

## Evaluation signals

- NPZ output file is valid HDF5 and contains saddledata array with shape (n_compartment_bins, n_compartment_bins) matching the number of eigenvector quantile bins used in digitization
- Saddle strength value is a finite positive scalar (typically 0.5–3.0 for mammalian genomes); negative or infinite values indicate computation or data quality issues
- Diagonal elements of saddledata (A–A and B–B interactions) are substantially higher than off-diagonal elements (A–B interactions), confirming compartment segregation
- Saddle matrix is symmetric (or nearly symmetric, within numerical tolerance), as compartment interaction is a symmetric relationship
- Repeated computation with different random seeds or subsets of input chromosomes produces saddle strength values within ±0.1 log2 units, confirming robustness

## Limitations

- Saddle strength is sensitive to the choice of digitization threshold (number and placement of bins); different quantile schemes or fixed thresholds can yield different metrics. The article does not prescribe a standard threshold, so comparison across studies requires consistent binning strategies.
- The saddle.mask_bad_bins method is available to filter bins based on Hi-C-level quality flags, but the article notes this feature is optional; omitting masking may bias strength estimates if bad bins preferentially occur in one compartment type.
- Saddle analysis aggregates across entire chromosomes or chromosomal regions; local compartment switches or dynamic transitions are smoothed out in the global metric. Saddle strength does not resolve sub-kilobase compartment heterogeneity.
- The smoothing API for P(s) and other derivatives mentioned in the article is noted as unstable, limiting downstream normalization or visualization of saddle matrices in some versions of cooltools.

## Evidence

- [other] Apply cooltools.digitize to bin the eigenvector values into discrete compartment categories (typically 2–5 bins) according to quantile or fixed thresholds.: "Apply cooltools.digitize to bin the eigenvector values into discrete compartment categories (typically 2–5 bins) according to quantile or fixed thresholds."
- [other] Call cooltools.saddle with the digitized track and cooler object to compute the 2D saddle matrix aggregating Hi-C contact frequency by compartment pair.: "Call cooltools.saddle with the digitized track and cooler object to compute the 2D saddle matrix aggregating Hi-C contact frequency by compartment pair."
- [other] Extract and save the saddledata array (untransformed) to an NPZ file and compute saddle strength as a scalar metric quantifying A/B compartment interaction asymmetry.: "Extract and save the saddledata array (untransformed) to an NPZ file and compute saddle strength as a scalar metric quantifying A/B compartment interaction asymmetry."
- [other] What are the input and output specifications for the cooltools.saddle function when applied to binned eigenvector track data from a cooler Hi-C matrix file?: "What are the input and output specifications for the cooltools.saddle function when applied to binned eigenvector track data from a cooler Hi-C matrix file?"
- [other] Cooltools provides saddle analysis functionality as part of its high-resolution Hi-C analysis toolkit, operating on cooler-format datasets that store high-resolution contact matrices and associated genomic tracks.: "Cooltools provides saddle analysis functionality as part of its high-resolution Hi-C analysis toolkit, operating on cooler-format datasets that store high-resolution contact matrices and associated"
- [readme] how to extract eigenvectors and create saddleplots reflecting A/B compartments: "how to extract eigenvectors and create saddleplots reflecting A/B compartments"
- [other] Added `saddle.mask_bad_bins` method to filter bins in a track based on Hi-C bin-level filtering: "Added `saddle.mask_bad_bins` method to filter bins in a track based on Hi-C bin-level filtering"
