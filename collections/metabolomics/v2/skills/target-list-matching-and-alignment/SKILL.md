---
name: target-list-matching-and-alignment
description: Use when you have LC-MS data (mzML or netCDF format) and a predefined
  list of target metabolites with known m/z values and retention time windows that
  you wish to extract and quantify.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - JPA
  - R
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.3390/metabo12030212
  title: JPA
evidence_spans:
- JPA is a comprehensive and integrated metabolomics data processing software.
- JPA is a comprehensive and integrated metabolomics data processing software
- '''JPA'' is written in R and its source code is publicly available'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_jpa_cq
    doi: 10.3390/metabo12030212
    title: JPA
  dedup_kept_from: coll_jpa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12030212
  all_source_dois:
  - 10.3390/metabo12030212
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# target-list-matching-and-alignment

## Summary

Match and extract metabolic features from LC-MS data against a user-supplied target list of known m/z values and retention times. This skill is essential for targeted metabolomics workflows where you want to recover specific analytes of interest rather than performing untargeted discovery.

## When to use

You have LC-MS data (mzML or netCDF format) and a predefined list of target metabolites with known m/z values and retention time windows that you wish to extract and quantify. Use this when your analysis goal is to confirm the presence and measure the intensity of specific compounds rather than discover new features.

## When NOT to use

- Your goal is to discover novel or unexpected metabolites — use MS1 peak picking or MS2 recognition instead
- Input is already an aligned multi-sample feature table from another tool
- You are processing full-scan or DIA (data-independent acquisition) datasets — the targeted extraction module is designed for DDA (data-dependent) LC-MS data

## Inputs

- raw LC-MS data files in mzML or netCDF format
- target list (CSV or tabular format) with columns: m/z, retention time, and optional metabolite identifiers

## Outputs

- feature table (dataframe with columns: m/z, retention time, intensity, sample identifier)
- CSV export of extracted targeted features with sample-wise measurements

## How to apply

Load raw LC-MS data (mzML or netCDF format) into the JPA package. Prepare a target list containing m/z values, retention times, and optional identifiers for each target compound. Apply the JPA targeted-list extraction module to match features in the LC-MS data against the target list using user-specified m/z tolerance (typically in ppm) and retention time tolerance windows (in seconds). Features are considered matches when their observed m/z and retention time fall within the specified tolerances relative to the target list entries. Compile all matched features into a feature table (rows = features, columns = samples and m/z, retention time, intensity values) and export as CSV for downstream analysis.

## Related tools

- **JPA** (targeted-list extraction module that matches and extracts features from LC-MS data using m/z and retention time matching against a user-supplied target list) — https://github.com/HuanLab/JPA.git
- **R** (programming environment for running JPA package; R version 4.0.0 or above required)

## Examples

```
featureTable <- targeted.extraction(dir = "X:/Users/JPAtest_20210330/multiDDA", target_list = "targets.csv", mz.tol = 10, rt.tol = 60)
```

## Evaluation signals

- All rows in the output feature table have m/z values within specified ppm tolerance of corresponding target list entries
- Retention times of extracted features fall within user-specified retention time windows (in seconds) for their matched targets
- Feature table contains expected columns (m/z, retention time, retention time min/max, intensity, sample identifier)
- Number of features extracted per sample is consistent with expected detection rate for the target compounds
- CSV export is properly formatted with no missing or truncated values in intensity or metadata columns

## Limitations

- Targeted extraction only recovers features that match entries in the user-supplied target list; unknown or unexpected metabolites will not be detected
- Extraction accuracy depends critically on the accuracy and completeness of the target list (m/z and retention time values); systematic errors in the target list will propagate to the feature table
- The skill is not suitable for full-scan or DIA data; it is designed specifically for DDA LC-MS workflows
- Matching relies on user-specified m/z and retention time tolerances; poorly chosen tolerances may result in false positives (non-target features matched) or false negatives (target features missed)
- Features outside specified m/z and retention time windows will not be recovered, even if they represent the target compound with slight retention time drift or mass calibration variation

## Evidence

- [other] The targeted-list extraction module identify and extract metabolic features that match a user-supplied target list from LC-MS data: "the JPA targeted-list extraction module identify and extract metabolic features that match a user-supplied target list from LC-MS data"
- [other] Apply the JPA targeted-list extraction module matching features in the LC-MS data against the target list, retrieving features within specified m/z and retention time tolerances: "Apply the JPA targeted-list extraction module to match features in the LC-MS data against the target list, retrieving features within specified m/z and retention time tolerances"
- [other] Prepare a user-supplied target list containing target m/z values, retention times, and other identifiers: "Prepare a user-supplied target list containing target m/z values, retention times, and other identifiers"
- [other] Compile extracted features into a feature table (rows = features, columns = samples/measurements and m/z, retention time, intensity values): "Compile extracted features into a feature table (rows = features, columns = samples/measurements and m/z, retention time, intensity values)"
- [readme] Please do not use this function when processing full-scan or DIA data set: "Please do not use this function when processing full-scan or DIA data set!"
