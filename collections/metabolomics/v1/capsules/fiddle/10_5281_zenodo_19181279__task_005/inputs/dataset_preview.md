### `figures/fiddle_logo.png`
_binary file, 68242 bytes_

### `paper.md`
```
# JosieHong__FIDDLE

## Introduction

# FIDDLE

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19181279-blue)](https://doi.org/10.5281/zenodo.19181279)
[![Release](https://img.shields.io/github/v/release/JosieHong/FIDDLE?label=Release)](https://github.com/JosieHong/FIDDLE/releases)

[<img src="img/fiddle_logo.png" align="right" width="220">](https://github.com/JosieHong/FIDDLE)

FIDDLE is a deep learning method for predicting molecular formulas from MS/MS spectra. This repository contains the full research codebase for model training, evaluation, and paper reproduction.

- **Paper:** [Nature Communications (2025)](https://www.nature.com/articles/s41467-025-66060-9)
- **CLI and Python API:** [msfiddle](https://github.com/josiehong/msfiddle)
- **Try this demo!** [FIDDLE on Hugging Face](https://huggingface.co/spaces/J0siee/FIDDLE)

<br clear="right"/>

> **Breaking change (v2.0.0):** The rescore model has been redesigned (Siamese architecture), see details in [CHANGELOG.md](./CHANGELOG.md).


## Methods

_No usage/docs found._

## Results

_No examples found._

## Discussion

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-03-23

### Added

- `test_caffeine.py`: inference scripts for caffeine (C8H10N4O2) GNPS spectra.
- `running_scripts/retrain_031826.sh`: end-to-end retraining script for both Orbitrap and Q-TOF (031826 data).
- `train_rescore.py`: Siamese rescore trainer. Freezes the TCN spectrum encoder; trains `FormulaEncoder` + `RescoreHead` with BCE loss. Checkpoint stores `formula_encoder_state_dict` and `rescore_head_state_dict`.
- `prepare_augment_rescore.py`: unified rescore data preparation script. Takes the TCN t
…[truncated]
```
