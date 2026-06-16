### `figures/plot.png`
_binary file, 30925 bytes_

### `paper.md`
```
# pymzML__pymzML

## Introduction


############
Introduction
############


.. image:: https://github.com/pymzml/pymzML/actions/workflows/pages/pages-build-deployment/badge.svg
   :target: https://pymzml.github.io/pymzML/
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/pymzML.svg
   :target: https://pypi.org/project/pymzML/

.. image:: https://pepy.tech/badge/pymzml
   :target: https://pepy.tech/project/pymzml

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: As long it is black

.. image:: http://depsy.org/api/package/pypi/pymzML/badge.svg
  :target: http://depsy.org/package/python/pymzML
  :alt: Research software impact


*******************
General information
*******************

Module to parse mzML data in Python based on cElementTree

Copyright 2010-2024 by:

    | M. Kösters,
    | J. Leufken,
    | T. Bald,
    | A. Niehues,
    | S. Schulze,
    | K. Sugimoto,
    | R.P. Zahedi,
    | M. Hippler,
    | S.A. Leidel,
    | C. Fufezan,



===================
Contact information
===================

Please refer to:

    | Dr. Christian Fufezan
    | Group Leader Experimental Bioinformatics
    | Cellzome GmbH
    | R&D Platform Technology & Science
    | GSK
    | Germany
    | eMail: christian@fufezan.net
    |
    | https://fufezan.net


*******
Summary
*******

pymzML is an extension to Python that offers
    * a) easy access to mass spectrometry (MS) data that allows the rapid development of tools
    * b

## Methods

Implementing an own file class
===============================

In  order to make pymzML accept other kinds of mzML data (e.g databases), one can
implement an own wrapper similiar to the ones discussed before.
In the following, an example for building and accessing a SQL database containing single spectra will be shown.


Creating the wrapper
---------------------

At first, a database with a specific layout needs to be created. Here, we use a sin
…[truncated]
```
