---
name: autotuner-object-manipulation
description: Use when after AutoTuner has completed EICparams extraction and parameter estimation on raw untargeted metabolomics data (mzML, mzXML, or CDF format), and you need to pass those estimates into XCMS or MZmine2 for full dataset processing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - R
  - Autotuner
  - XCMS
  - MZmine2
  - MSconvert
derived_from:
- doi: 10.1101/812370
  title: AutoTuner parameter selection
evidence_spans:
- knitr::rmarkdown
- library(Autotuner)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_autotuner_parameter_selection_cq
    doi: 10.1101/812370
    title: AutoTuner parameter selection
  dedup_kept_from: coll_autotuner_parameter_selection_cq
schema_version: 0.2.0
---

# autotuner-object-manipulation

## Summary

Extract and format nine distinct parameter estimates from an AutoTuner object into a table suitable for direct XCMS input. This skill bridges the AutoTuner parameter optimization phase and the downstream XCMS metabolomics processing pipeline.

## When to use

After AutoTuner has completed EICparams extraction and parameter estimation on raw untargeted metabolomics data (mzML, mzXML, or CDF format), and you need to pass those estimates into XCMS or MZmine2 for full dataset processing. Specifically, when you have an AutoTuner R object containing optimized parameter estimates and need them formatted as a structured table for consumption by XCMS.

## When NOT to use

- If you have fewer than 3 raw samples — AutoTuner requires at least 3 samples for reliable parameter estimation.
- If the AutoTuner object has not yet completed the EICparams function call — returnParams depends on populated EICparams results.
- If your downstream tool is not XCMS or MZmine2 — the parameter format may not be compatible with other metabolomics processing software.

## Inputs

- AutoTuner R object (class: Autotuner) containing EICparams results
- Raw untargeted metabolomics data (minimum 3 samples in mzML/mzXML/CDF format, already processed through MSconvert if needed)

## Outputs

- Parameter estimate table (data.frame or matrix in R)
- Exported parameter table in CSV or TSV format suitable for XCMS input
- Nine distinct XCMS-compatible parameter estimates

## How to apply

Load the AutoTuner R object containing the EICparams results in R (version ≥3.6). Call the returnParams function on the AutoTuner object to extract the nine parameter estimates it has computed during the sliding window TIC analysis, peak isolation, and EIC parameter extraction phases. Format the returned parameters as a table with columns and rows suitable for XCMS input, ensuring all nine estimates are present and within expected ranges for your mass analyzer type (qTOF, orbitrap, or FTICR). Export the parameter table to a structured format (CSV or TSV) with proper delimiters and headers for downstream consumption by XCMS.

## Related tools

- **XCMS** (Downstream metabolomics data processing software that consumes the nine AutoTuner parameter estimates)
- **MZmine2** (Alternative downstream metabolomics data processing software compatible with AutoTuner parameter output)
- **R** (Environment in which AutoTuner object is loaded and returnParams function is executed)
- **Autotuner** (R package containing the AutoTuner class and returnParams method) — https://github.com/KujawinskiLaboratory/Autotuner
- **MSconvert** (Tool for pre-processing raw mass spectral data into standard formats (mzML/mzXML/CDF) before AutoTuner analysis)

## Examples

```
library(Autotuner); at_obj <- readRDS('autotuner_object.rds'); params <- returnParams(at_obj); write.csv(params, 'xcms_parameters.csv', row.names=FALSE)
```

## Evaluation signals

- The returned table contains exactly nine parameter estimates with no missing values (NA or NaN).
- All nine parameter values fall within expected ranges for the mass analyzer type used (qTOF, orbitrap, or FTICR); parameters should be plausible for chromatographic and mass spectral resolution of the instrument.
- The table structure matches XCMS parameter input requirements (correct column names, numeric data types, appropriate delimiters in exported file).
- When the exported parameter table is passed to XCMS, the software accepts it without format errors and processes the full dataset without parameter-related failures.
- Cross-validation: parameters estimated by AutoTuner on a subset of samples should be consistent when compared to parameters estimated on a different subset (reproducibility check).

## Limitations

- AutoTuner has been tested on qTOF, orbitrap, and FTICR mass analyzers; performance on other analyzer types is not documented.
- Requires at least 3 raw samples and a metadata spreadsheet linking samples to experimental factors; smaller or poorly annotated datasets may not yield robust parameter estimates.
- The nine parameter estimates are sensitive to the lag, threshold, and influence parameters used in the sliding window TIC peak identification step; suboptimal tuning of these filters can propagate to downstream parameters.
- No changelog is provided in the repository; version differences and breaking changes in the returnParams function signature are not formally tracked.

## Evidence

- [other] The returnParams function outputs parameter estimates from EICparams results and the AutoTuner object that can be entered directly into XCMS to process raw untargeted metabolomics data.: "The returnParams function outputs parameter estimates from EICparams results and the AutoTuner object that can be entered directly into XCMS"
- [intro] AutoTuner quickly finds estimates for nine distinct parameters using statistical inference.: "Using statistical inference, AutoTuner quickly finds estimates for nine distinct parameters."
- [other] The workflow involves loading the AutoTuner object, calling returnParams, formatting output, and exporting to a structured file format.: "1. Load the AutoTuner object containing EICparams estimates in R. 2. Call the returnParams function on the AutoTuner object to extract the nine parameter estimates. 3. Format the returned parameters"
- [readme] AutoTuner requires at least 3 samples of raw data and a metadata spreadsheet for input.: "For input, AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF). It also requires a spreadsheet containing at least two columns."
- [intro] AutoTuner is designed to work with raw mass spectral data processed by MSconvert.: "AutoTuner is designed to work directly with raw mass spectral data that has been processed by using MSconvert."
