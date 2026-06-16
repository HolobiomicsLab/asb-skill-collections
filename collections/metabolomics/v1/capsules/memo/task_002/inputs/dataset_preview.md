### `paper.md`
```
# mandelbrot-project__memo

## Introduction

|GitHub Workflow Status| |GitHub| |PyPI| |Docs|

MEMO
===============
.. image:: https://github.com/mandelbrot-project/memo_publication_examples/blob/main/docs/memo_logo.jpg
   :width: 200 px
   :align: right

Description
-----------------

**M**\ s2 bas\ **E**\ d sa\ **M**\ ple vect\ **O**\ rization (**MEMO**)
is a method allowing a Retention Time (RT) agnostic alignment of
metabolomics samples using the fragmentation spectra (MS2) of their
consituents. The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted
and used to generate an *MS2 fingerprint* of the sample. These
fingerprints can in a second stage be aligned to compare different
samples. Once obtained, different filtering (remove peaks/losses from
blanks for example) and visualization techniques (MDS/PCoA, TMAP,
Heatmap, ...) can be used. MEMO suits particularly well to compare chemodiverse samples, ie with a
poor features overlap, or to compare samples with a strong RT shift,
acquired using different LC methods or even different mass spectrometers
technology (Maxiis Q-ToF vs Q-Exactive Orbitrap).

Documentation
------------------
For documentation, see our `readthedocs`_. Different examples of application and comparison to other MS/MS based metrics are available `here`_ and the corresponding notebooks are available on `GitHub`_.

Publication
-----------

If you use MEMO, please cite the following papers:
   - Gaudry A, Huber F, Nothias L-F, Cretton S, Kaiser M, Wolfender J-L, et al.

## Methods

.. memo documentation master file, created by
   sphinx-quickstart on Thu Dec 16 21:33:56 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to memo's documentation!
================================

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   API <api/memo_ms.rst>

Description
-----------------

MEMO is a method allowing a Retention Time (RT) a
…[truncated]
```
