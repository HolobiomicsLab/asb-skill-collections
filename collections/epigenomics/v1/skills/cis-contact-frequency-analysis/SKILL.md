---
name: cis-contact-frequency-analysis
description: Use when when you have loaded a cooler file containing Hi-C contact matrices and need to quantify how contact probability decays with genomic distance within a single chromosome.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0097
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

# cis-contact-frequency-analysis

## Summary

Compute and analyze contact frequency as a function of genomic distance within the same chromosome (cis contacts) using cooler-formatted Hi-C matrices. This is a foundational Hi-C analysis that reveals the prominent distance-dependent decay of chromatin contacts.

## When to use

When you have loaded a cooler file containing Hi-C contact matrices and need to quantify how contact probability decays with genomic distance within a single chromosome. This is typically one of the first analyses performed on Hi-C data to characterize the global organizational properties of chromatin and to validate data quality before proceeding to domain-level or structural feature detection.

## When NOT to use

- Input cooler file is already filtered, normalized, and pre-computed contact frequency tables exist — use those directly instead of recalculating.
- Trans (inter-chromosomal) contact analysis is the primary goal — this skill is specific to cis contacts within a single chromosome.
- You need to detect specific chromatin structures (TADs, loops, compartments) rather than global distance-decay properties — use domain-detection or loop-calling methods instead.

## Inputs

- cooler file (.cool or .mcool) containing Hi-C contact matrix
- target chromosome identifier
- genomic distance binning specification (bin size in base pairs)

## Outputs

- distance-binned contact frequency table (CSV/TSV with genomic separation and contact counts)
- P(s) curve (contact probability vs. genomic distance)
- visualization (log–log plot of contact frequency vs. distance)

## How to apply

Load the cooler file using the cooler library and extract the contact matrix for a target chromosome. Use cooltools functions to compute per-bin sequencing depth (coverage) to normalize for bias, then aggregate contacts across genomic distance bins (e.g., 1 kb, 5 kb, 10 kb bins) to produce a distance-binned contact frequency vector. Optionally compute the P(s) curve (probability of contact as a function of separation distance s) and smooth it to reduce noise. Export the results as a tabular format (CSV/TSV) with bin coordinates and normalized contact counts, and visualize as a log–log plot to assess the power-law decay characteristic of polymer-like chromatin behavior.

## Related tools

- **cooltools** (primary analysis library providing cis contact frequency computation and curve smoothing functions) — https://github.com/open2c/cooltools
- **cooler** (file format and I/O library for loading and querying Hi-C contact matrices) — https://github.com/open2c/cooler
- **Python** (scripting language for data manipulation, normalization, and export)

## Examples

```
import cooler; import cooltools; c = cooler.Cooler('sample.mcool::resolutions/5000'); coverage = cooltools.coverage(c, store_cis_counts=True); print(coverage.head())
```

## Evaluation signals

- Contact frequency decreases monotonically with increasing genomic distance (no unexplained inversions in the P(s) curve).
- Log–log plot of contact frequency vs. distance exhibits expected power-law behavior characteristic of polymer physics (slope between −1 and −2).
- Contact counts at shortest distances (same bin or adjacent bins) are higher than at larger separations by at least 1–2 orders of magnitude.
- Tabular output row counts match the number of distance bins specified and contain no NaN or negative values.
- Bias-normalized contact frequencies are consistent across replicates or technical duplicates (if available).

## Limitations

- Contact frequency calculation assumes uniform sequencing depth across bins; if bins have highly variable coverage, bias normalization (e.g., ICE, KNIGHT, or other balancing methods) must be applied first.
- P(s) smoothing is implemented but the API is not yet stable according to the article, so future changes to smoothing parameters or functionality may occur.
- Results are sensitive to cooler file resolution (bin size); coarser bins lose fine-scale distance detail and may obscure local structural features.
- Cis contacts exclude important trans-chromosomal interactions; a complete chromatin organization picture requires separate trans analysis.

## Evidence

- [readme] how to calculate contact frequency as a function of genomic distance-- the most prominent feature in Hi-C maps: "how to calculate contact frequency as a function of genomic distance-- the most prominent feature in Hi-C maps"
- [other] Call cooltools.coverage() on the loaded cooler object to compute per-bin sequencing depth: "Call cooltools.coverage() on the loaded cooler object to compute per-bin sequencing depth, optionally specifying whether to store total cis counts"
- [discussion] New functionality for smoothing P(s) and derivatives (API is not yet stable): "New functionality for smoothing P(s) and derivatives (API is not yet stable)"
- [intro] The recently-introduced cooler format readily handles storage of high-resolution datasets: "The recently-introduced ***cooler*** format readily handles storage of high-resolution datasets"
