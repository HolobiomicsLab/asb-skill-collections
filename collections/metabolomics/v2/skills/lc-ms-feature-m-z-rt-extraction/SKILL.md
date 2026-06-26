---
name: lc-ms-feature-m-z-rt-extraction
description: Use when you have preprocessed LC-MS intensity data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - pandas
  - numpy
  - scipy
  - scikit-learn
  - matplotlib
  - MamsiStructSearch
  - XCMS
  - nPYc toolbox
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.5c01327
  title: mamsi
- doi: 10.1371/journal.pcbi.1011814
  title: ''
evidence_spans:
- MAMSI is a Python framework
- import pandas as pd
- import numpy as np
- scipy
- 'Dependencies: scipy'
- from sklearn.model_selection import train_test_split
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mamsi
    doi: 10.1021/acs.analchem.5c01327
    title: mamsi
  dedup_kept_from: coll_mamsi
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01327
  all_source_dois:
  - 10.1021/acs.analchem.5c01327
  - 10.1371/journal.pcbi.1011814
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# LC-MS Feature m/z-RT Extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract mass-to-charge ratio (m/z) and retention time (RT) metadata from preprocessed LC-MS intensity data to enable downstream structural clustering and annotation. This skill converts raw LC-MS feature tables into a structured format where each feature is annotated with its chromatographic and mass spectrometric properties.

## When to use

You have preprocessed LC-MS intensity data (e.g., from XCMS or nPYc toolbox) with column names encoding assay, retention time, and m/z information (format: AssayName_RTsec_m/zvalue) and need to link statistically significant features into structural clusters defined by isotopologue and adduct signatures. Apply this skill as the first step in the MamsiStructSearch workflow, immediately after selecting features of interest (e.g., via MB-VIP and permutation testing).

## When NOT to use

- Input LC-MS table lacks properly formatted column headers encoding retention time and m/z (e.g., raw XCMS output without assay/RT/m/z parsing)
- Features have already been manually annotated or linked into structural clusters; re-extraction would be redundant
- Data are from targeted (e.g., MRM) rather than untargeted LC-MS workflows, as targeted assays typically do not require isotopologue/adduct clustering

## Inputs

- Preprocessed LC-MS intensity matrix with column names in format (AssayName)_(RTsec)_(m/z)m/z
- Optional: retention time tolerance window (rt_win) in seconds
- Optional: mass tolerance threshold (ppm) for matching

## Outputs

- Feature metadata table with extracted m/z, RT, and assay columns
- MamsiStructSearch object with loaded LC-MS data ready for structural clustering

## How to apply

Load the preprocessed LC-MS intensity table (with columns formatted as AssayName_RTsec_m/zvalue) into MamsiStructSearch using the .load_lcms() method, which parses column headers to extract m/z, RT, and assay metadata for each feature. The method automatically tokenizes the column names to recover the underlying mass and retention time values. Define retention time tolerance (rt_win, default 5 seconds) and mass tolerance (ppm, default 15 ppm) parameters based on your instrument's mass accuracy and chromatographic resolution. These parameters control subsequent searches for isotopologue signatures (mass differences of 1.00335 Da within each RT window) and adduct signatures (hypothetical neutral mass matches). The extraction output is a structured feature metadata table that serves as input to structural and correlation clustering steps.

## Related tools

- **MamsiStructSearch** (Python class that loads LC-MS data, parses column metadata, and enables downstream structural clustering via .load_lcms()) — https://github.com/kopeckylukas/py-mamsi
- **XCMS** (Upstream preprocessor producing intensity matrices from raw LC-MS data (mzML, netCDF))
- **nPYc toolbox** (Complementary preprocessing tool for LC-MS data quality control and feature table generation)
- **pandas** (Data frame manipulation for formatting and subsetting LC-MS feature tables before loading into MamsiStructSearch)

## Examples

```
from mamsi.mamsi_struct_search import MamsiStructSearch
struct = MamsiStructSearch(rt_win=5, ppm=10)
struct.load_lcms(selected)
struct.get_structural_clusters(annotate=True)
```

## Evaluation signals

- Extracted m/z and RT values match the expected ranges for the LC-MS assay (e.g., m/z 50–1200 Da, RT 0–600 seconds for typical UPLC)
- Feature metadata table has no missing values in m/z, RT, or assay columns after extraction
- Column name parsing succeeds for all features; no features are excluded or truncated due to malformed headers
- Downstream structural clustering produces isotopologue and adduct clusters consistent with expected metabolite biochemistry (e.g., adjacent m/z values within rt_win tolerance are grouped)
- Cross-assay feature links using [M+H]+ / [M-H]− reference masses are detected, indicating proper RT and m/z alignment across positive and negative ion modes

## Limitations

- Relies on strict column name format (AssayName_RTsec_m/z); non-standard headers will fail to parse, requiring manual reformatting upstream
- Default parameters (rt_win=5 sec, ppm=15) are tuned for National Phenome Centre assays; different LC-MS platforms or chromatographic methods may require empirical re-optimization
- Extraction does not handle missing or zero m/z / RT values gracefully; input data must be cleaned of non-detects beforehand
- Automated annotation is only supported for assays analyzed by the National Phenome Centre using peakPantheR ROI files; other chromatographies require manual annotation or alternative tools

## Evidence

- [other] Load preprocessed LC-MS intensity data with column names in format (AssayName)_(RTsec)_(m/z)m/z into MamsiStructSearch using .load_lcms() to extract feature metadata (m/z, RT, assay).: "Load preprocessed LC-MS intensity data with column names in format (AssayName)_(RTsec)_(m/z)m/z into MamsiStructSearch using .load_lcms() to extract feature metadata"
- [other] Define retention time tolerance window (rt_win, default 5 seconds) and mass tolerance (ppm, default 15 ppm) for structural matching.: "Define retention time tolerance window (rt_win, default 5 seconds) and mass tolerance (ppm, default 15 ppm) for structural matching."
- [methods] Subsequently, data were pre-processed using XCMS and nPYc toolbox.: "Subsequently, data were pre-processed using XCMS and nPYc toolbox"
- [methods] each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da between mass-to-charge ratios (m/z) of the features: "each RT window is searched for isotopologue signatures by searching mass differences of 1.00335 Da between mass-to-charge ratios (m/z)"
- [intro] the framework was tested on metabolomics phenotyping data, but it should be usable with other types of LC-MS data.: "the framework was tested on metabolomics phenotyping data, but it should be usable with other types of LC-MS data"
