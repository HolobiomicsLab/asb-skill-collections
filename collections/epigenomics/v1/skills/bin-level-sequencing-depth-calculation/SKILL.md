---
name: bin-level-sequencing-depth-calculation
description: Use when you have a cooler file (.cool or .mcool) from a Hi-C or micro-C experiment and need to quantify the total number of sequencing reads assigned to each genomic bin to assess coverage uniformity, identify poorly-sequenced regions, or prepare bin-level weights for downstream normalization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
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

# bin-level-sequencing-depth-calculation

## Summary

Compute per-bin sequencing depth (coverage) from a cooler Hi-C contact matrix using cooltools.coverage(), producing a bedGraph or tabular track of read counts per genomic bin. This enables quality assessment and normalization of high-resolution chromosome conformation capture datasets.

## When to use

You have a cooler file (.cool or .mcool) from a Hi-C or micro-C experiment and need to quantify the total number of sequencing reads assigned to each genomic bin to assess coverage uniformity, identify poorly-sequenced regions, or prepare bin-level weights for downstream normalization. Specifically useful when the cooler object is already loaded in memory and you want to export coverage as a track file (bedGraph or tabular CSV/TSV).

## When NOT to use

- Input data is already a normalized or log-transformed contact matrix (coverage calculation assumes raw counts).
- You need trans (inter-chromosomal) coverage only; cooltools.coverage() by default computes cis (intra-chromosomal) counts.
- The cooler file has no valid bin or contact data (e.g., empty or corrupted cooler).

## Inputs

- cooler contact matrix object (loaded via cooler.Cooler() or cooler.open_cooler())
- Hi-C or micro-C cooler file (.cool or .mcool format)

## Outputs

- bedGraph file or tabular track (CSV/TSV) with columns: chromosome, start, end, coverage
- optionally, cis count column stored in cooler HDF5 metadata

## How to apply

Load a cooler contact matrix object using the cooler library, then call cooltools.coverage() on it to compute per-bin sequencing depth. The function signature permits optionally storing total cis counts as a new column in the cooler HDF5 file. After computation, export the resulting coverage array (bin coordinates + coverage values) to bedGraph or tabular format (CSV/TSV). Validate the output by checking that the number of rows matches the total bin count in the cooler object's bins table, and that coverage values are non-negative integers or floats reflecting read accumulation per bin.

## Related tools

- **cooltools** (Primary library providing the coverage() function to compute per-bin sequencing depth from cooler contact matrices) — https://github.com/open2c/cooltools
- **cooler** (HDF5-backed format and library for storing and loading high-resolution Hi-C contact matrices and bin tables) — https://github.com/open2c/cooler
- **Python** (Programming language environment for executing cooltools and cooler function calls)

## Examples

```
from cooler import Cooler; import cooltools.coverage as cov; c = Cooler('test.cool'); depth = cov.coverage(c); depth.to_csv('coverage.bedGraph', sep='\t', header=False, index=False)
```

## Evaluation signals

- Output file has exactly N rows, where N equals the total number of bins in the cooler.bins table (cooler.nbins).
- All coverage values are non-negative and match the sum of read counts per bin across all contacts involving that bin.
- bedGraph output has valid format: tab-delimited, 4 columns (chrom, chromStart, chromEnd, value), with coordinates consistent with the cooler bin table.
- Coverage values for bins with zero reads are 0 (or NaN if filtered), not missing or negative.
- If cis counts are stored in the cooler, they match the exported coverage values and can be retrieved via cooler object column access (e.g., cooler['cis_count']).

## Limitations

- cooltools.coverage() computes cis (intra-chromosomal) coverage by default; trans (inter-chromosomal) coverage requires separate handling or manual aggregation.
- Output format and API stability are not yet fully documented in the article; refer to function docstrings and inline examples in the cooltools repository.
- Memory usage scales with the number of bins and contact matrix density; very large cooler files (>10 billion contacts) may require chunked or out-of-core processing.
- Coverage calculation assumes all contacts in the cooler have equal weight; if the cooler was pre-normalized (e.g., by ICE or other methods), the reported coverage will reflect weighted counts, not raw sequencing depth.

## Evidence

- [intro] Larger datasets increase the challenges at each step of computational analysis, from storage, to memory, to researchers' time.: "Larger datasets increase the challenges at each step of computational analysis, from storage, to memory, to researchers' time."
- [other] Install in editable development mode using pip install -e . to enable access to bundled test datasets.: "install in "editable" (i.e. development) mode using the `-e` option"
- [methods] Call cooltools.coverage() on the loaded cooler object to compute per-bin sequencing depth, optionally specifying whether to store total cis counts in the cooler as indicated in the function signature.: "Call cooltools.coverage() on the loaded cooler object to compute per-bin sequencing depth, optionally specifying whether to store total cis counts in the cooler as indicated in the function signature."
- [intro] The recently-introduced cooler format readily handles storage of high-resolution datasets.: "The recently-introduced ***cooler*** format readily handles storage of high-resolution datasets"
