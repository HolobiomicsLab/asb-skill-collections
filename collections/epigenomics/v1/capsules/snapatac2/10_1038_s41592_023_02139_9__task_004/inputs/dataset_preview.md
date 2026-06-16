### `figures/docker-windows-tutorial-0.png`
_binary file, 131 bytes_

### `figures/docker-windows-tutorial-1.png`
_binary file, 131 bytes_

### `figures/docker-windows-tutorial-2.png`
_binary file, 131 bytes_

### `figures/func+export_coverage.svg`
_binary file, 129 bytes_

### `figures/func+import_data.svg`
_binary file, 130 bytes_

### `paper.md`
```
# scverse__SnapATAC2

## Introduction

SnapATAC2: A Python/Rust package for single-cell epigenomics analysis
=====================================================================

[![PyPI](https://img.shields.io/pypi/v/snapatac2)](https://pypi.org/project/snapatac2/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/snapatac2)](https://pypistats.org/packages/snapatac2)
[![Continuous integration](https://github.com/scverse/SnapATAC2/workflows/test-python-package/badge.svg)](https://github.com/scverse/SnapATAC2/actions/workflows/test_python.yml)
[![GitHub Repo stars](https://img.shields.io/github/stars/scverse/SnapATAC2?style=social)](https://github.com/scverse/SnapATAC2/stargazers)

> [!TIP]
> Got raw fastq files? Check out our new single-cell preprocessing package [precellar](https://github.com/regulatory-genomics/precellar)!

SnapATAC2 is a flexible, versatile, and scalable single-cell omics analysis framework, featuring:

- Scale to more than 10 million cells.
- Blazingly fast preprocessing tools for BAM to fragment files conversion and count matrix generation.
- Matrix-free spectral embedding algorithm that is applicable to a wide range of single-cell omics data, including single-cell ATAC-seq, single-cell RNA-seq, single-cell Hi-C, and single-cell methylation.
- Efficient and scalable co-embedding algorithm for single-cell multi-omics data integration.
- End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling, differ

## Methods

{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

   {% block attributes %}
   {% if attributes %}
   .. rubric:: Attributes

   .. autosummary::
      :toctree: .
   {% for item in attributes %}
      ~{{ objname }}.{{ item }}
   {%- endfor %}
   {% endif %}
   {% endblock %}

   {% block methods %}
   {% if methods %}
   .. rubric:: Methods

   .. autosummary::
      :toctree: .
   {% for item
…[truncated]
```
