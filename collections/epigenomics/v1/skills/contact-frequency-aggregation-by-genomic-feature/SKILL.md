---
name: contact-frequency-aggregation-by-genomic-feature
description: Use when you have a cooler Hi-C contact matrix, a set of genomic features (e.g., CTCF peaks, enhancers, or TAD boundaries defined in BED format), and want to quantify average contact patterns around those features to detect local organization principles.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0798
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0092
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

# contact-frequency-aggregation-by-genomic-feature

## Summary

Aggregate Hi-C contact frequencies around genomic features (e.g., CTCF binding sites) to identify local topological patterns and average interaction strengths. This skill extracts enriched contact neighborhoods and reveals how specific proteins or regulatory elements organize chromosome structure.

## When to use

You have a cooler Hi-C contact matrix, a set of genomic features (e.g., CTCF peaks, enhancers, or TAD boundaries defined in BED format), and want to quantify average contact patterns around those features to detect local organization principles. Use this when investigating how specific architectural proteins or cis-regulatory elements shape three-dimensional genome folding.

## When NOT to use

- Input Hi-C data has not been normalized for sequencing depth or bin-level biases; apply iterative correction or ICE normalization first.
- Genomic features are very sparse (<<100 sites per chromosome) or have extreme size variation; aggregation may produce unstable averages.
- You are interested in single-feature contact patterns rather than aggregate behavior; use direct contact extraction or focused visualization instead.

## Inputs

- cooler Hi-C contact matrix file (.cool or .mcool)
- genomic feature coordinates (BED format or similar track defining feature locations)
- bin size and genome reference (implicit in cooler file)

## Outputs

- 2D pileup matrix (aggregated contacts around features, typically N×N array)
- average contact frequency heatmap
- enrichment metric or fold-change relative to genome-wide contact distance curve

## How to apply

Load a cooler file containing the binned Hi-C contact matrix and a BED or similar feature track defining genomic regions of interest. Extract or pre-compute the set of genomic coordinates for each feature (e.g., CTCF binding sites from ChIP-seq). Use cooltools' pileup or aggregation functions to stack contact matrices centered on each feature, normalizing by genomic distance to account for the distance-decay of contact frequency. Average the stacked matrices to produce a consensus 2D map showing how contacts are enriched or depleted relative to the feature. Evaluate the output by examining whether the resulting heatmap shows symmetry (expected around a central feature) and whether contact strength falls away from the feature center; compare against random or shuffled feature coordinates as a null model.

## Related tools

- **cooltools** (provides pileup and aggregation API to stack Hi-C contacts around feature coordinates and compute average interaction matrices) — https://github.com/open2c/cooltools
- **cooler** (stores and retrieves binned Hi-C contact matrices in a sparse, efficient HDF5-based format compatible with pileup operations) — https://github.com/open2c/cooler
- **Python** (scripting language enabling flexible coordinate loading, matrix manipulation, and statistical validation of pileup results)

## Evaluation signals

- Output pileup matrix has expected shape (typically symmetric around the central feature); dimensions match the specified window size in bins.
- Contact enrichment is highest at the feature center and decays towards edges; symmetry around the diagonal indicates proper feature centering.
- Comparison against shuffled feature coordinates or genome-wide background shows statistically significant enrichment (e.g., fold-change > 1.5–2.0).
- NPZ or HDF5 output file is created with correct data type (float64) and no NaN or infinite values in valid regions.
- Visual inspection of heatmap shows expected architectural signatures (e.g., for CTCF: cross-shaped or stripe pattern indicating long-range interactions; for TAD boundaries: elevated corner contacts).

## Limitations

- Pileup quality degrades at chromosomal boundaries or when features cluster; edge effects must be masked or excluded from statistical summaries.
- Contact frequency is strongly modulated by genomic distance; raw pileups conflate distance-dependent and feature-specific effects; distance normalization or detrending is recommended.
- Sparse or irregularly distributed features may produce unreliable aggregate patterns; minimum feature count (typically >50–100 per region) is advisable.
- Low-resolution Hi-C data (>10 kb bins) limits spatial precision of feature-contact associations; results may reflect coarse structural domains rather than specific protein–DNA interactions.
- API for smoothing P(s) distance curves and derivatives is not yet stable; reproducibility across cooltools versions may be affected.

## Evidence

- [readme] how to create avearge maps around genomic features like CTCF: "[Pileups and Average Patterns](https://cooltools.readthedocs.io/en/latest/notebooks/pileup_CTCF.html): how to create avearge maps around genomic features like CTCF."
- [readme] cooler format stores binned contact matrices efficiently: "The recently-introduced ***cooler*** format readily handles storage of high-resolution datasets via a sparse data model."
- [readme] cooltools provides aggregation functionality for Hi-C analysis: "***cooltools*** provides a suite of computational tools with a paired python API and command line access, which facilitates workflows either on high-performance computing clusters or via custom"
