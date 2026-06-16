### `figures/ContainerShow_axis.png`
_binary file, 36779 bytes_

### `figures/ContainerShow_channel.png`
_binary file, 95400 bytes_

### `figures/ContainerShow_channelwise.png`
_binary file, 91924 bytes_

### `figures/ContainerShow_channelwise_segmentation.png`
_binary file, 129565 bytes_

### `figures/ContainerShow_imshow_kwargs.png`
_binary file, 122974 bytes_

### `figures/ContainerShow_library_id.png`
_binary file, 119898 bytes_

### `figures/ContainerShow_scale_mask_circle_crop.png`
_binary file, 51525 bytes_

### `figures/ContainerShow_segmentation.png`
_binary file, 140839 bytes_

### `figures/ContainerShow_transpose_channelwise_False_False.png`
_binary file, 67164 bytes_

### `figures/ContainerShow_transpose_channelwise_False_True.png`
_binary file, 180591 bytes_

### `figures/ContainerShow_transpose_channelwise_True_False.png`
_binary file, 236892 bytes_

### `figures/ContainerShow_transpose_channelwise_True_True.png`
_binary file, 76745 bytes_

### `figures/DetectTissue_detect_tissue_felzenszwalb.png`
_binary file, 5995 bytes_

### `figures/DetectTissue_detect_tissue_otsu.png`
_binary file, 6849 bytes_

### `figures/figure1.png`
_binary file, 911945 bytes_

### `figures/squidpy_horizontal.png`
_binary file, 29642 bytes_

### `figures/squidpy_vertical.png`
_binary file, 20146 bytes_

### `figures/test_img.jpg`
_binary file, 229870 bytes_

### `figures/tissue_hires_image.png`
_binary file, 20014 bytes_

### `figures/tissue_lowres_image.png`
_binary file, 518124 bytes_

### `paper.md`
```
# scverse__squidpy

## Introduction

[![Build](https://github.com/scverse/squidpy/actions/workflows/build.yaml/badge.svg)](https://github.com/scverse/squidpy/actions/workflows/build.yaml)
[![Test](https://github.com/scverse/squidpy/actions/workflows/test.yaml/badge.svg)](https://github.com/scverse/squidpy/actions/workflows/test.yaml)
[![codecov](https://codecov.io/gh/scverse/squidpy/graph/badge.svg)](https://codecov.io/gh/scverse/squidpy)
[![License](https://img.shields.io/github/license/scverse/squidpy)](https://opensource.org/licenses/BSD-3-Clause)
[![PyPI](https://img.shields.io/pypi/v/squidpy.svg)](https://pypi.org/project/squidpy/)
[![Python Version](https://img.shields.io/pypi/pyversions/squidpy)](https://pypi.org/project/squidpy/)
[![Read the Docs](https://img.shields.io/readthedocs/squidpy/latest.svg?label=Read%20the%20Docs)](https://squidpy.readthedocs.io/en/stable)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

# Squidpy - Spatial Single Cell Analysis in Python

Squidpy is the scverse toolkit for scalable analysis and visualization of spatial molecular data.
It builds on [scanpy](https://scanpy.readthedocs.io/en/stable/) and [anndata](https://anndata.readthedocs.io/en/stable/), providing streamlined APIs for feature extraction, spatial statistics, and interactive exploration of tissue sections together with microscopy images.

![Squidpy overview](https://raw.githubusercontent.com/scverse/squidpy/ma

## Methods

{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
    {% block methods %}
    {%- if methods %}
    .. rubric:: {{ _('Methods') }}

    .. autosummary::
        :toctree: .
    {% for item in methods %}
    {%- if item not in ['__init__'] %}
        ~{{ name }}.{{ item }}
    {%- endif %}
    {%- endfor %}
    {%- for item in all_methods %}
    {%- if item in ['__call__'] %}
        ~{{ name }}.{{
…[truncated]
```
