### `paper.md`
```
# MoseleyBioinformaticsLab__MESSES

## Introduction

MESSES
~~~~~~

.. image:: https://img.shields.io/pypi/v/messes.svg
   :target: https://pypi.org/project/messes
   :alt: Current library version

.. image:: https://img.shields.io/pypi/pyversions/messes.svg
   :target: https://pypi.org/project/messes
   :alt: Supported Python versions

..
    .. image:: https://github.com/MoseleyBioinformaticsLab/messes/actions/workflows/build.yml/badge.svg
       :target: https://github.com/MoseleyBioinformaticsLab/messes/actions/workflows/build.yml
       :alt: Build status

.. image:: https://codecov.io/gh/MoseleyBioinformaticsLab/MESSES/branch/main/graphs/badge.svg?branch=main
   :target: https://codecov.io/gh/MoseleyBioinformaticsLab/MESSES
   :alt: Code coverage information

..
    .. image:: https://img.shields.io/badge/DOI-10.3390%2Fmetabo11030163-blue.svg
       :target: https://doi.org/10.3390/metabo11030163
       :alt: Citation link

.. image:: https://img.shields.io/github/stars/MoseleyBioinformaticsLab/messes.svg?style=social&label=Star
    :target: https://github.com/MoseleyBioinformaticsLab/messes
    :alt: GitHub project

|


MESSES (Metadata from Experimental SpreadSheets Extraction System) is a Python package that facilitates the conversion of tabular data into
other formats. We call it MESSES because we try to convert other people’s metadata messes into clean, well-structured, JSONized metadata. 
It was initially created to pull mass spectrometry (MS) and nuclear magnetic resonance (NMR) experimental data into a database, b

## Methods

API
===

.. automodule:: messes

extract
~~~~~~~
.. automodule:: messes.extract.extract
    :members:
    
validate
~~~~~~~~
.. automodule:: messes.validate.validate
    :members:
    
convert
~~~~~~~
.. automodule:: messes.convert.convert
    :members:
    
.. automodule:: messes.convert.user_input_checking
    :members:

.. automodule:: messes.convert.mwtab_functions
    :members:



CLI
===

Extract
~~~~~~~
The extract command
…[truncated]
```
