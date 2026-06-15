---
name: hi-c-expected-value-calculation
description: Use when you have a cooler-format Hi-C contact matrix and need to establish a genome-wide baseline contact frequency by genomic distance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3297
  - http://edamontology.org/topic_0736
  tools:
  - cooler
  - cooltools
  - Python
derived_from:
- doi: 10.1371/journal.pcbi.1012067
  title: cooltools
- doi: 10.1101/2022.10.31.514564
  title: ''
evidence_spans: []
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

# hi-c-expected-value-calculation

## Summary

Compute expected contact frequency as a function of genomic distance from a Hi-C contact matrix, producing a distance-binned expected value table that serves as a null model for detecting significant interactions and normalizing contact probability P(s) curves.

## When to use

You have a cooler-format Hi-C contact matrix and need to establish a genome-wide baseline contact frequency by genomic distance. This is essential when you want to normalize observed contacts, compute O/E ratios, generate P(s) smoothing pipelines, or identify deviation from random polymer behavior. Use this skill before applying downstream analyses like saddle plots, insulation scoring, or contact probability smoothing.

## When NOT to use

- You only have raw read counts and no contact matrix binned into a cooler file — first construct the Hi-C contact matrix.
- Your Hi-C dataset has extreme sparsity or low coverage (< 10 million valid contacts) — expected values will be unreliable and noise-dominated.
- You are working with a single locus or a small region and do not need genome-wide baseline statistics.

## Inputs

- cooler file (.cool or .mcool format)
- bin resolution (in base pairs, typically 5 kb – 100 kb)
- optional: bin-level mask or filter (e.g., list of bad bins to exclude)

## Outputs

- expected_cis table (TSV format with columns: dist_bp, contact_frequency, n_valid)
- optionally: expected_trans table for inter-chromosomal contacts

## How to apply

Load a cooler Hi-C contact matrix at a chosen bin resolution (e.g., 10 kb or coarser). Use cooltools' expected module to sum contact counts across all pairs of bins at each genomic distance, accounting for valid bin pairs via masking or filtering. The function iterates over distance lags, aggregates contacts, normalizes by the number of valid bin pairs at each distance, and produces a table with columns: distance in base pairs (dist_bp), contact frequency (count or normalized frequency), and bin pair count statistics (n_valid). Export the resulting expected_cis table as TSV format. This precomputed table is then used as input to downstream smoothing (logbin_expected) or O/E normalization workflows.

## Related tools

- **cooler** (Library for storing and querying Hi-C contact matrices in HDF5-based format; provides bin indexing and bin-pair iteration required for expected value summation.) — https://github.com/open2c/cooler
- **cooltools** (Python package providing the expected module and logbin_expected function for computing and smoothing expected contact frequency tables from cooler inputs.) — https://github.com/open2c/cooltools
- **Python** (Programming language environment for executing cooltools and cooler workflows.)

## Evaluation signals

- Output TSV has exactly three numeric columns (dist_bp, contact_frequency, n_valid) with monotonically increasing distance values and strictly positive contact frequencies.
- Contact frequency decreases monotonically with increasing genomic distance (reflecting polymer decay law), with no spurious jumps or inverted regions.
- n_valid (bin pair count) decreases with distance due to finite genome size; values should decline smoothly without gaps.
- Expected table can be successfully loaded and used as input to logbin_expected smoothing without schema errors or missing values.
- Sum of n_valid across all distances matches the expected total number of valid cis bin pairs (genome length / bin size)^2 / 2, accounting for masking.

## Limitations

- Expected values are genome-wide averages and do not capture local sequence effects, chromatin state, or topologically associating domain (TAD) structure; they serve as a null model only.
- Bad bins (low coverage, unmappable, or artifact-prone) must be masked before calculation, or they will bias expected values toward artificially low frequencies at small distances.
- Very large genomic distances (> 50 Mb in many organisms) have small n_valid and therefore noisy expected values; smoothing or aggregation is recommended.
- Expected values depend on sequencing depth and read quality; datasets with different library sizes or quality filters will produce non-comparable expected tables.
- The expected module API and smoothing functionality (logbin_expected) are noted as unstable in the cooltools documentation.

## Evidence

- [readme] The most prominent feature in Hi-C maps: "how to calculate contact frequency as a function of genomic distance-- the most prominent feature in Hi-C maps"
- [other] Cooltools includes new functionality for smoothing P(s) and its derivatives: "New functionality for smoothing P(s) and derivatives (API is not yet stable)"
- [other] Load precomputed expected_cis table (TSV format with columns dist_bp, contact_frequency, n_valid): "Load precomputed expected_cis table (TSV format with columns dist_bp, contact_frequency, n_valid) from a deposited cooler-derived dataset"
- [intro] Cooltools enables high-resolution Hi-C analysis in Python: "enabling high-resolution Hi-C analysis in Python"
- [intro] Cooler format handles high-resolution Hi-C data: "The recently-introduced ***cooler*** format readily handles storage of high-resolution datasets"
