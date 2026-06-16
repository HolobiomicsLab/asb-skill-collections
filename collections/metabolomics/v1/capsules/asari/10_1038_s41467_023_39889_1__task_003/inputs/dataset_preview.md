### `figures/conda_asari_screenshot.png`
_binary file, 170291 bytes_

### `figures/viz_screen_shot20220518.png`
_binary file, 454506 bytes_

### `paper.md`
```
# shuzhao-li-lab__asari

## Introduction

# Asari

[![Documentation Status](https://readthedocs.org/projects/asari/badge/?version=latest)](https://asari.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://img.shields.io/badge/DOI-doi.org%2F10.1038%2Fs41467--023--39889--1-blue)](https://doi.org/10.1038/s41467-023-39889-1)

Trackable and scalable Python program for high-resolution metabolomics data processing. 

- Taking advantage of high mass resolution to prioritize mass separation and alignment
- Peak detection on a composite map instead of repeated on individual samples
- Statistics guided peak dection, based on local maxima and prominence, selective use of smoothing
- Reproducible, track and backtrack between features and mass tracks (EICs)
- Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases
- Scalable, performance conscious, disciplined use of memory and CPU 
- Transparent, JSON centric data structures, easy to chain other tools

LC-MS application was described in Li et al. Nature Communications 14.1 (2023): 4113](https://www.nature.com/articles/s41467-023-39889-1). GC-MS workflow was added to version 1.16.6.

A web server (https://asari.app) and [full pipeline](https://pypi.org/project/pcpfm/) are available now.
A set of tutorials are hosted at https://github.com/shuzhao-li-lab/asari_pcpfm_tutorials/.


## Methods

.. asari_analyze:

.. default-domain:: py

Analyze
======================

.. automodule:: asari.analyze
    :members:


.. asari_annotate_user_table:

.. default-domain:: py

Annotate User Table
=========================

.. automodule:: asari.annotate_user_table
    :members:

.. asari_chromatograms:

.. default-domain:: py

Chromatograms
======================

.. automodule:: asari.chromatograms
    :members:


.. asari_constructors:

.. default-domain:: py

Constructors
======================

.. automodule:: asari.constructors
    :members:


.. asari_dashboard:

.. default-domain:: py

Dashboard
====
…[truncated]
```
