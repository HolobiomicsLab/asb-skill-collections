### `figures/falcon_how.png`
_binary file, 522098 bytes_

### `figures/falcon_logo.png`
_binary file, 47064 bytes_

### `paper.md`
```
# bittremieux-lab__falcon

## Introduction

_falcon_
========

![falcon](falcon_logo.png)

For more information:

* [Official code website](https://github.com/bittremieux/falcon)

The _falcon_ spectrum clustering tool uses advanced algorithmic techniques for
highly efficient processing of millions of MS/MS spectra. First,
high-resolution spectra are binned and converted to low-dimensional vectors
using feature hashing. Next, the spectrum vectors are used to construct nearest
neighbor indexes for fast similarity searching. The nearest neighbor indexes
are used to efficiently compute a sparse pairwise distance matrix without
having to exhaustively compare all spectra to each other. Finally,
density-based clustering is performed to group similar spectra into clusters.

The software is available as open-source under the BSD license.

If you use _falcon_ in your work, please cite the following publication:

- Wout Bittremieux, Kris Laukens, William Stafford Noble, Pieter C. Dorrestein.
**Large-scale tandem mass spectrum clustering using fast nearest neighbor
searching.** _Rapid Communications in Mass Spectrometry_, e9153 (2021).
[doi:10.1002/rcm.9153](https://doi.org/10.1002/rcm.9153)

Installation
------------

_falcon_ requires Python 3.8+ and is available on the Linux and OSX platforms.

You can easily install _falcon_ with pip:

    pip install falcon-ms spectrum-utils==0.3.5

Running _falcon_
----------------

_falcon_ can be run from the command line, with settings specified as
command-line arguments or set in an INI 

## Methods

_No usage/docs found._

## Results

_No examples found._

## Discussion

_No changelog found._

## References

- Source: github:bittremieux-lab__falcon
- Synthesized at: 2026-06-16T07:27:41+00:00
```
