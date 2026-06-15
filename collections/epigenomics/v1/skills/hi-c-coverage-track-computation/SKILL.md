---
name: hi-c-coverage-track-computation
description: Use when you have a cooler file (.cool or .mcool) from a Hi-C experiment and need to generate a genome-wide track of per-bin sequencing depth to assess coverage uniformity, identify poorly sequenced regions, or normalize downstream analyses by local sequencing intensity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3179
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

# hi-c-coverage-track-computation

## Summary

Compute per-bin sequencing depth (coverage) from cooler-formatted Hi-C contact matrices using cooltools.coverage(), producing a normalized track of bin-level read abundance across the genome. This quantifies the aggregate sequencing depth at each genomic bin, a key quality control and normalization step in high-resolution Hi-C analysis.

## When to use

Apply this skill when you have a cooler file (.cool or .mcool) from a Hi-C experiment and need to generate a genome-wide track of per-bin sequencing depth to assess coverage uniformity, identify poorly sequenced regions, or normalize downstream analyses by local sequencing intensity. Use it before downstream Hi-C computations (e.g., insulation, contact scaling, saddle point analysis) that may be confounded by uneven sequencing depth.

## When NOT to use

- Input is already a pre-computed coverage track or bigWig file — skip directly to downstream use.
- Analysis goal requires only the total contact count per chromosome, not per-bin resolution.
- Cooler file is empty or contains no valid contact pairs (malformed or failed sequencing).

## Inputs

- cooler file (.cool or .mcool format) — a HDF5-based contact matrix from Hi-C sequencing
- cooler.Cooler object loaded in memory from a cooler file

## Outputs

- pandas Series indexed by genomic bins with per-bin coverage values (sequencing depth)
- bedGraph, CSV, or TSV file with columns: chromosome, start, end, coverage

## How to apply

Install cooltools in development mode (pip install -e .) to access bundled test datasets and the cooltools library. Load a cooler object from a .cool or .mcool file using the cooler library (e.g., cooler.Cooler(path)). Call cooltools.coverage() on the loaded cooler object, optionally specifying whether to store total cis counts back into the cooler file metadata. The function returns a pandas Series or track indexed by genomic bins with coverage values (total sequencing depth per bin). Export the result to a tabular format (bedGraph, CSV, or TSV) containing bin coordinates (chrom, start, end) and corresponding coverage values. Validate the output by checking row counts match the total number of bins in the cooler file and that coverage values are non-negative and non-zero for expected genomic regions.

## Related tools

- **cooltools** (Provides the coverage() function to compute per-bin sequencing depth from cooler contact matrices) — https://github.com/open2c/cooltools
- **cooler** (Handles loading, parsing, and in-memory access to Hi-C contact matrices in cooler format (.cool, .mcool)) — https://github.com/open2c/cooler
- **Python** (Execution environment for cooltools and cooler libraries)

## Examples

```
import cooler; import cooltools; c = cooler.Cooler('micro_c_hESC.cool'); coverage = cooltools.coverage(c, store_in_cooler=True); coverage.to_csv('coverage.tsv', sep='\t', header=['coverage'])
```

## Evaluation signals

- Output pandas Series or file has one entry per genomic bin in the cooler; row count matches cooler.nbins
- All coverage values are non-negative; zero coverage appears only in unmappable or filtered bins
- Coverage values show expected patterns: higher in regions of known high contact frequency, lower in heterochromatin or unsequenced gaps
- Output file parses as valid bedGraph or tabular format with correct column order and no NaN/inf values for valid bins
- Re-loading the cooler after coverage computation confirms cis counts stored in metadata (if requested) match the sum of coverage values across cis pairs

## Limitations

- Coverage reflects only sequenced read pairs; it does not account for mappability, GC bias, or other biases inherent to Hi-C library preparation.
- Per-bin coverage is sensitive to bin resolution: lower-resolution bins aggregate over larger genomic windows and may mask local sequencing artifacts.
- Cooler file must have valid contact pairs; empty or corrupted matrices will produce zero or undefined coverage.
- The cooltools.coverage() API is documented in function docstrings but lacks a published specification of exact output format in the article; users should inspect the function signature and available parameters.
- Cis-only coverage computation may not reflect total sequencing effort if trans (inter-chromosomal) pairs are abundant or important to the analysis.

## Evidence

- [other] 1: "Install cooltools in development mode using pip install -e . to enable access to the bundled micro-C hESC test dataset. 2. Load the test cooler file (micro-C hESC) using the cooler library."
- [other] 2: "Call cooltools.coverage() on the loaded cooler object to compute per-bin sequencing depth, optionally specifying whether to store total cis counts in the cooler as indicated in the function signature."
- [other] 3: "Export the resulting coverage track to bedGraph or tabular format (CSV/TSV) containing bin coordinates and coverage values."
- [intro] 4: "The recently-introduced cooler format readily handles storage of high-resolution datasets"
- [intro] 5: "Larger datasets increase the challenges at each step of computational analysis, from storage, to memory, to researchers' time."
