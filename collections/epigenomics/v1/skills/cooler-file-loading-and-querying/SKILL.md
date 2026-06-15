---
name: cooler-file-loading-and-querying
description: Use when your Hi-C data is stored in cooler format (a binary HDF5-based sparse matrix with associated genomic bins and genomic tracks); you need to programmatically access the contact matrix, bin coordinates, or track data (e.g., eigenvectors, GC content) for further analysis;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3365
  edam_topics:
  - http://edamontology.org/topic_3173
  - http://edamontology.org/topic_0654
  tools:
  - cooltools
  - cooler
  - bioframe
derived_from:
- doi: 10.1371/journal.pcbi.1012067
  title: cooltools
- doi: 10.1101/2022.10.31.514564
  title: ''
evidence_spans:
- cooltools provides a suite of computational tools with a paired python API
- cooltools leverages this format to enable flexible and reproducible analysis of high-resolution data.
- The recently-introduced cooler format readily handles storage of high-resolution datasets via a sparse data model.
- the recently-introduced cooler format readily handles storage of high-resolution datasets
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

# cooler-file-loading-and-querying

## Summary

Loading and querying high-resolution Hi-C contact matrices stored in cooler format, which is a sparse hierarchical data structure designed for efficient storage and random access to genome-wide contact frequency data. This is a foundational operation required before any downstream Hi-C analysis, including compartment detection, insulation scoring, or aggregate pattern extraction.

## When to use

Your Hi-C data is stored in cooler format (a binary HDF5-based sparse matrix with associated genomic bins and genomic tracks); you need to programmatically access the contact matrix, bin coordinates, or track data (e.g., eigenvectors, GC content) for further analysis; or you need to validate that a cooler file is well-formed and compatible with downstream tools.

## When NOT to use

- Your Hi-C data is in legacy or raw format (e.g., HiCPro .matrix and .bed files, or raw contact lists); convert or normalize to cooler first using cooler's build tools.
- You need to modify or create a new cooler file from scratch; use cooler.create_cooler() or cooler.dump_auto() instead of load-and-query.
- You are working with single-cell or very sparse Hi-C variants where the standard binned cooler model (uniform rectangular grid) is not applicable.

## Inputs

- cooler file (.cool or .mcool HDF5 archive)
- file path (string)
- optionally: desired resolution for multi-resolution files

## Outputs

- cooler.Cooler object (Python file-like accessor)
- pandas.DataFrame of bin coordinates (chrom, start, end, and any associated track columns)
- sparse contact matrix (scipy.sparse or pydata.sparse format on demand)
- metadata dictionary (genome assembly, bin size, normalization state)

## How to apply

Import the cooler library and open a .cool or .mcool file using cooler.Cooler() or cooler.open_auto() to obtain a file-like object. Query the object's attributes to retrieve bin coordinates (cooler_obj.bins()), contact data (cooler_obj.matrix()), or genomic tracks (cooler_obj.bins()[:]) in a lazy, chunk-aware manner. Use the .info dictionary to inspect metadata such as bin size, genome assembly, and normalization status. For multi-resolution .mcool files, first list available resolutions using cooler.fileops.list_coolers() and open the desired resolution. Validate file integrity by checking that bin count matches the expected genome size and that contact matrix shape is consistent (N_bins × N_bins). Leverage cooler's sparse storage model to avoid loading the entire matrix into memory—only fetch regions of interest using slice notation (e.g., cooler_obj.matrix[start:end, start:end]).

## Related tools

- **cooler** (Python library for reading and writing cooler HDF5 archives; provides file opening, bin querying, and lazy matrix access) — https://github.com/open2c/cooler
- **cooltools** (Builds on cooler to provide high-level analysis functions (saddle, insulation, compartments) that consume cooler objects) — https://github.com/open2c/cooltools
- **bioframe** (Companion library for genomic interval manipulation; often used alongside cooler for bin and track handling)

## Examples

```
import cooler
c = cooler.Cooler('sample.cool')
bins = c.bins()[:]
matrix = c.matrix(sparse=True)[0:100, 0:100]
print(c.info)
```

## Evaluation signals

- File opens without HDF5 read errors and cooler object is instantiated successfully.
- Bin coordinate DataFrame has expected shape (N_bins rows) and columns (chrom, start, end); all coordinates are non-negative integers and in ascending order within each chromosome.
- Contact matrix shape is (N_bins, N_bins) and is sparse (non-zero fraction is << 1 for typical mammalian genomes at 10 kb resolution).
- Metadata .info dictionary includes 'nbins' key matching the actual bin count, and 'binsize' or 'format' fields are present and non-null.
- Track columns (if requested) are present in bins() output and have no NaN values for valid bins, or match expected coverage statistics (e.g., eigenvector mean ≈ 0).

## Limitations

- cooler format assumes rectangular binning (uniform bin width); non-uniform or adaptive binning schemes are not natively supported.
- Very large .mcool files with many resolutions can be slow to list; pre-caching the resolution list may be needed for high-throughput workflows.
- Genomic tracks (eigenvectors, GC content) must be pre-computed and embedded in the cooler file; cooler.Cooler() does not compute them on-the-fly.
- The sparse matrix is stored in a particular compression format (default: HDF5 COO-like); direct access to underlying sparse format may require conversion to scipy.sparse or pydata.sparse.

## Evidence

- [readme] The recently-introduced cooler format readily handles storage of high-resolution datasets via a sparse data model.: "The recently-introduced ***cooler*** format readily handles storage of high-resolution datasets via a sparse data model."
- [readme] cooltools leverages this format to enable flexible and reproducible analysis of high-resolution data.: "***cooltools*** leverages this format to enable flexible and reproducible analysis of high-resolution data."
- [other] Load a cooler file and an associated eigenvector track as the first step of saddle analysis.: "Load a cooler file and an associated eigenvector track (e.g., from a prior eigs_cis calculation)."
- [other] Cooler provides structured access to cooler-format datasets storing high-resolution contact matrices and associated genomic tracks.: "Cooltools provides saddle analysis functionality as part of its high-resolution Hi-C analysis toolkit, operating on cooler-format datasets that store high-resolution contact matrices and associated"
