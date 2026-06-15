---
name: multi-assay-data-integration-and-harmonization
description: Use when you have independent LC-MS assays (e.g., positive and negative ionization modes, different lipid profiling assays, or different chromatographic methods) analyzed on the same sample cohort and want to integrate them into a single discriminant or regression model without losing assay-level.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - Python
  - mbpls
  - pandas
  - numpy
  - scikit-learn
  - matplotlib
  - nPYc toolbox
  - XCMS
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- MAMSI is a Python framework
- 'It is based on MB_PLS package: Baum et al., (2019). Multiblock PLS: Block dependent prediction modeling for Python.'
- import pandas as pd
- import numpy as np
- from sklearn.model_selection import train_test_split
- from matplotlib import pyplot as plt
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mamsi
    doi: 10.1021/acs.analchem.5c01327
    title: mamsi
  dedup_kept_from: coll_mamsi
schema_version: 0.2.0
---

# multi-assay-data-integration-and-harmonization

## Summary

Load, prefix, and harmonize multi-assay LC-MS metabolomics intensity matrices (e.g., HPOS, LPOS, LNEG) into a unified block structure suitable for Multi-Block PLS modelling and cross-assay feature linking. This skill ensures assay identity is preserved in column names and sample correspondence is maintained across all blocks before statistical integration.

## When to use

You have independent LC-MS assays (e.g., positive and negative ionization modes, different lipid profiling assays, or different chromatographic methods) analyzed on the same sample cohort and want to integrate them into a single discriminant or regression model without losing assay-level interpretability. Use this skill when raw intensity matrices are stored separately and require harmonization before Multi-Block PLS fitting or feature selection.

## When NOT to use

- Input intensity matrices already have assay identifiers embedded in column names (e.g., 'HPOS_mz123_rt45') — prefixing would create redundant or conflicting annotations.
- Samples are not in identical order or row indices do not match exactly across assays — harmonization will introduce silent misalignment errors.
- You are integrating data from a single assay or mode (e.g., only LPOS) — Multi-Block PLS is designed for ≥2 blocks and offers no advantage over single-block PLS for univariate data.

## Inputs

- multi-assay LC-MS intensity matrices (one pandas DataFrame per assay, e.g., HPOS, LPOS, LNEG)
- sample metadata table with response variable (numeric phenotype or class label)
- assay names or abbreviations (e.g., 'HPOS', 'LPOS', 'LNEG') for column prefixing

## Outputs

- list of harmonized intensity DataFrames with assay-prefixed column names
- numeric response vector (y) aligned to sample rows
- metadata table with sample identifiers and phenotype annotation

## How to apply

Load each assay's intensity matrix as a pandas DataFrame and add an assay-specific prefix to all feature column names (e.g., 'HPOS_' for HILIC positive, 'LPOS_' for lipidomic positive, 'LNEG_' for lipidomic negative). Ensure all DataFrames share an identical row index (sample identifiers) and are aligned in the same order. Verify that no column name collisions exist across assays after prefixing. This assay-level prefix annotation is critical for later interpretation of Multi-Block VIP scores and structural clustering, as it allows tracing each significant feature back to its originating assay and ionization mode. Prepare the metadata table separately with matching sample identifiers and response variable (e.g., disease status or phenotype encoded as numeric). The harmonized blocks are then passed as a list to MamsiPls.fit() or MamsiPls.estimate_lv() for subsequent modelling.

## Related tools

- **pandas** (Load, align, and manipulate intensity matrices; add assay-specific prefixes to column names)
- **mbpls** (Accept harmonized multi-assay blocks as input for Multi-Block PLS fitting and latent variable estimation) — https://github.com/kopeckylukas/py-mamsi
- **scikit-learn** (Perform train–test split while maintaining sample correspondence across blocks)
- **nPYc toolbox** (Pre-process raw LC-MS data before intensity matrix export (optional upstream step))
- **XCMS** (Pre-process raw LC-MS chromatograms before feature intensity extraction (optional upstream step))

## Examples

```
import pandas as pd
hpos = pd.read_csv('alz_hpos.csv').add_prefix('HPOS_')
lpos = pd.read_csv('alz_lpos.csv').add_prefix('LPOS_')
lneg = pd.read_csv('alz_lneg.csv').add_prefix('LNEG_')
y = pd.read_csv('metadata.csv')['Gender'].apply(lambda x: 1 if x == 'Female' else 0)
from sklearn.model_selection import train_test_split
hpos_train, hpos_test, lpos_train, lpos_test, lneg_train, lneg_test, y_train, y_test = train_test_split(hpos, lpos, lneg, y, test_size=0.1, random_state=42)
```

## Evaluation signals

- Each assay DataFrame has an assay-specific prefix on all feature column names (e.g., 'HPOS_', 'LPOS_', 'LNEG_') with no collisions across blocks after concatenation.
- Row indices (sample identifiers) are identical and in the same order across all assay DataFrames; concatenating along columns does not introduce NaN values or duplicates.
- All numeric values in intensity matrices are non-negative and on a consistent scale (e.g., all raw peak intensities or all log-transformed); no mixed scaling or unit mismatches.
- Response vector (y) has length equal to the number of rows in each assay DataFrame; binary or multiclass labels are numeric (0, 1, 2, …) rather than categorical strings.
- Metadata table and intensity matrices share the same sample identifiers and row order; spot-checking first and last sample IDs confirms alignment.

## Limitations

- Assay-specific prefixes are arbitrary; they do not encode analytical metadata (e.g., MS mode, ionization polarity, chromatographic method) beyond the prefix string itself. Document the prefix scheme separately (e.g., 'HPOS = HILIC positive, LPOS = lipidomic reversed-phase positive').
- Prefixing assumes no m/z or RT overlap across assays — if the same metabolite is detected by multiple assays at identical or near-identical m/z and RT, prefixing alone will not merge or de-duplicate them. Structural clustering via MamsiStructSearch is required to identify cross-assay links post-hoc.
- Harmonization does not handle missing values (NaN) within intensity matrices; rows or features with missing data must be imputed or removed before concatenation to avoid downstream errors in MB-PLS fitting.
- Sample size imbalance or batch effects across assays are not corrected during harmonization; normalization and batch correction should be performed upstream (e.g., via nPYc toolbox) before prefixing and concatenation.

## Evidence

- [other] Load and prepare multi-assay LC-MS intensity data (HPOS, LPOS, LNEG) and metadata using pandas, adding assay-specific prefixes to column names.: "Load and prepare multi-assay LC-MS intensity data (HPOS, LPOS, LNEG) and metadata using pandas, adding assay-specific prefixes to column names."
- [readme] hpos = pd.read_csv('./sample_data/alz_hpos.csv').add_prefix('HPOS_')
lpos = pd.read_csv('./sample_data/alz_lpos.csv').add_prefix('LPOS_')
lneg = pd.read_csv('./sample_data/alz_lneg.csv').add_prefix('LNEG_'): "hpos = pd.read_csv('./sample_data/alz_hpos.csv').add_prefix('HPOS_')
lpos = pd.read_csv('./sample_data/alz_lpos.csv').add_prefix('LPOS_')
lneg = pd.read_csv('./sample_data/alz_lneg.csv').add_prefix('L"
- [other] Split data into training (90%) and testing (10%) subsets using scikit-learn's train_test_split with random_state=42, maintaining sample correspondence across blocks.: "Split data into training (90%) and testing (10%) subsets using scikit-learn's train_test_split with random_state=42, maintaining sample correspondence across blocks."
- [readme] MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry datasets: "MAMSI is a Python framework designed for the integration of multi-assay mass spectrometry datasets"
- [readme] the framework was tested on metabolomics phenotyping data, but it should be usable with other types of LC-MS data: "the framework was tested on metabolomics phenotyping data, but it should be usable with other types of LC-MS data"
