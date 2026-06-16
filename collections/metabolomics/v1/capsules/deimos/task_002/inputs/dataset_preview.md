### `figures/icon.png`
_binary file, 16026 bytes_

### `figures/logo.png`
_binary file, 36358 bytes_

### `figures/overview.png`
_binary file, 195316 bytes_

### `paper.md`
```
# pnnl__deimos

## Introduction

DEIMoS
=======
DEIMoS, or Data Extraction for Integrated Multidimensional Spectrometry, is a Python application 
programming interface and command-line tool for high-dimensional mass spectrometry (MS) data 
analysis workflows that offers ease of development and access to efficient algorithmic implementations. 
Functionality includes feature detection, feature alignment, collision cross section (CCS) calibration, 
isotope detection, and MS/MS spectral deconvolution, with the output comprising detected features aligned 
across study samples and characterized by mass, CCS, tandem mass spectra, and isotopic signature. 
Notably, DEIMoS operates on N-dimensional data, largely agnostic to acquisition instrumentation; 
algorithm implementations simultaneously utilize all dimensions to (i) offer greater separation between features, 
thus improving detection sensitivity, (ii) increase alignment/feature matching confidence among datasets, 
and (iii) mitigate convolution artifacts in tandem mass spectra.

For installation instructions, usage overview, project information, and API reference, please see our [documentation](https://deimos.readthedocs.io).

Citing DEIMoS
-------------
If you would like to reference deimos in an academic paper, we ask you include the following.

* DEIMoS, version 1.6.2 http://github.com/pnnl/deimos (accessed MMM YYYY)
* Colby, S.M., Chang, C.H., Bade, J.L., Nunez, J.R., Blumer, M.R., Orton, D.J., Bloodsworth, K.J., Nakayasu, E.S., Smith, R.D, Ibrahim, Y.M. an

## Methods

=========
alignment
=========

.. automodule:: deimos.alignment
	:members:
	:private-members:
	:undoc-members:


===========
calibration
===========

.. automodule:: deimos.calibration
	:members:
	:private-members:
	:undoc-members:


===
cli
===

.. automodule:: deimos.cli
	:members:
	:private-members:
	:undoc-members:


=============
deconvolution
=============

.. automodule:: deimos.deconvolution
	:members:
	:private-members:
	:undoc-members:


=
…[truncated]
```
