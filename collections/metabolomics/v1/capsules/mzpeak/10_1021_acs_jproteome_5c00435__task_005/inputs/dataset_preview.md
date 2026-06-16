### `figures/chunked_layout.png`
_binary file, 107710 bytes_

### `figures/mzpeak_extract_times_2026.svg`
_binary file, 86980 bytes_

### `figures/mzpeak_file_sizes_2026.svg`
_binary file, 91450 bytes_

### `figures/packed_tables.png`
_binary file, 4751 bytes_

### `figures/point_layout.png`
_binary file, 64689 bytes_

### `figures/sciex_null_marking_delta_encoding_error.png`
_binary file, 93505 bytes_

### `figures/sparse_tables.png`
_binary file, 5000 bytes_

### `figures/thermo_null_marking_err.png`
_binary file, 81042 bytes_

### `paper.md`
```
# mobiusklein__mzpeak_prototyping

## Introduction

# mzPeak file format prototyping

**The draft specification document is available <https://hupo-psi.github.io/mzPeak-specification/>** ([source](https://github.com/HUPO-PSI/mzPeak-specification))

This repository contains prototype implementations of the mzPeak format initially described in https://pubs.acs.org/doi/10.1021/acs.jproteome.5c00435. The latest presentation of the results took place on November 11, 2025 at the HUPO conference in Toronto, Canada. The slides can be retrieved [here](https://zenodo.org/records/17747369).

The mzPeak name is currently held in trust by the OpenMS Inc. The details of the trademark are described [here](https://doi.org/10.5281/zenodo.20054899)

**NOTE**: This is a **work in progress**, no stability is guaranteed at this point.

The primary work shown here is written in Rust at the repository root, including a library for reading and writing mzPeak files, as well as command line tools for converting existing formats into mzPeak.

There is a separate Python implementation in `python/` which is a complete re-implementation for _reading_ mzPeak files using [`pyarrow`](https://arrow.apache.org/docs/python/index.html), and the PyData stack. The Python codebase does not support writing at this time although this is subject to change in the future.

There is also an R implementation in `R/`, which is also a complete re-implementation using the [`arrow`](https://arrow.apache.org/docs/r/) for _reading_ only at this time.

A separate .NET implementat

## Methods

_No usage/docs found._

## Results

_No examples found._

## Discussion

_No changelog found._

## References

- Source: github:mobiusklein__mzpeak_prototyping
- Synthesized at: 2026-06-15T13:12:31+00:00
```
