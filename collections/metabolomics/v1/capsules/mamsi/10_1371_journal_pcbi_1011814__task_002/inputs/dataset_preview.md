### `figures/MAMSI_logo.png`
_binary file, 31516 bytes_

### `figures/MAMSI_logo.svg`
_binary file, 9744 bytes_

### `figures/confusion_matrix.png`
_binary file, 12041 bytes_

### `figures/correlation_heatmap.png`
_binary file, 286462 bytes_

### `figures/lv_estimation.png`
_binary file, 99647 bytes_

### `figures/mb-vip.png`
_binary file, 30964 bytes_

### `figures/network.png`
_binary file, 122160 bytes_

### `figures/null_models_distribution.png`
_binary file, 39104 bytes_

### `figures/silhouette_plot.png`
_binary file, 24159 bytes_

### `paper.md`
```
# kopeckylukas__py-mamsi

## Introduction

# MAMSI
![MAMSI_logo](https://github.com/kopeckylukas/py-mamsi/blob/main/docs/images/MAMSI_logo.png?raw=true)

[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://github.com/kopeckylukas/py-mamsi/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/docs-available-brightgreen.svg)](https://kopeckylukas.github.io/py-mamsi/) 
[![pages-build-deployment](https://github.com/kopeckylukas/py-mamsi/actions/workflows/pages/pages-build-deployment/badge.svg)](https://kopeckylukas.github.io/py-mamsi/)
[![PyPI version](https://img.shields.io/pypi/v/mamsi.svg)](https://pypi.org/project/mamsi/)
[![DOI](https://zenodo.org/badge/823594568.svg)](https://zenodo.org/doi/10.5281/zenodo.13619607)

MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry datasets. 
In addition, the MAMSI framework provides a platform for linking statistically significant features of untargeted multi-assay liquid chromatography – mass spectrometry (LC-MS) metabolomics datasets into clusters defined by their structural properties based on mass-to-charge ratio (*m/z*) and retention time (*RT*).

*N.B. the framework was tested on metabolomics phenotyping data, but it should be usable with other types of LC-MS data.*



## Methods

#


## MamsiPls
[source](https://github.com/kopeckylukas/py-mamsi/blob/main/mamsi/mamsi_pls.py/#L23)
```python 
MamsiPls(
   n_components = 2, full_svd = False, method = 'NIPALS', standardize = True,
   max_tol = 1e-14, nipals_convergence_norm = 2, calc_all = True, sparse_data = False,
   copy = True
)
```


---
A class that extends the MB_PLS class by extra methods convenient in Chemometrics and Metabolomics research. 
It is based on MB-PLS package: Baum et al., (2019). Multiblock PLS: Block dependent prediction modeling for Python.
This wrapper has some extra methods convenient in Chemometrics and Metabolomics research.

For a full list of methods, please refer to the MB-PL
…[truncated]
```
