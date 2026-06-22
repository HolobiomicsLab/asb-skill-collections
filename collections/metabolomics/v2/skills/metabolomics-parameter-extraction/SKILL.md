---
name: metabolomics-parameter-extraction
description: Use when you have raw untargeted metabolomics data in mzML, mzXML, or CDF format from qTOF, Orbitrap, or FTICR mass analyzers, at least 3 samples, a sample metadata spreadsheet linking filenames to experimental factors, and need to generate optimized processing parameters for XCMS or MZmine2.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - R
  - XCMS
  - MZmine2
  - MSconvert
  - Autotuner
  - mtbls2
derived_from:
- doi: 10.1101/812370
  title: AutoTuner parameter selection
evidence_spans:
- knitr::rmarkdown
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

# metabolomics-parameter-extraction

## Summary

Extract nine dataset-specific parameter estimates from raw untargeted metabolomics data using statistical inference on extracted ion chromatograms, producing XCMS-compatible parameters without manual tuning. This skill automates the otherwise laborious process of parameter selection for metabolomics data processing pipelines.

## When to use

You have raw untargeted metabolomics data in mzML, mzXML, or CDF format from qTOF, Orbitrap, or FTICR mass analyzers, at least 3 samples, a sample metadata spreadsheet linking filenames to experimental factors, and need to generate optimized processing parameters for XCMS or MZmine2 without manual trial-and-error tuning.

## When NOT to use

- Input data is already processed or in feature table format (e.g., m/z intensity pairs without raw chromatographic structure)
- Fewer than 3 samples are available (AutoTuner requires minimum sample count for robust statistical inference)
- Raw data is from non-MS instruments or in proprietary formats that cannot be converted to mzML/mzXML/CDF

## Inputs

- Raw mass spectrometry data files (mzML, mzXML, or CDF format)
- Sample metadata spreadsheet with sample names and experimental factors
- AutoTuner R object containing EICparams results

## Outputs

- Nine distinct XCMS parameter estimates (formatted as table/CSV/TSV)
- Parameter values suitable for direct XCMS input

## How to apply

Load raw mass spectrometry data and sample metadata into the AutoTuner R package. Run sliding window analysis on the total ion current (TIC) with user-tuned lag, threshold, and influence parameters to identify peaks, then expand peak bounds via isolatePeaks to refine estimates. Call the EICparams function on extracted ion chromatograms, applying a mass threshold filter (an absolute mass error greater than the expected analytical capabilities of your mass analyzer) to extract parameter estimates. Finally, invoke the returnParams function on the AutoTuner object to output the nine parameter estimates as a formatted table suitable for direct entry into XCMS. The statistical inference approach ensures robustness across different sample types and instrument platforms.

## Related tools

- **XCMS** (Target data processing software; receives the nine extracted parameters for untargeted metabolomics feature detection and alignment)
- **MZmine2** (Alternative data processing software compatible with AutoTuner parameter output)
- **MSconvert** (Converts raw proprietary mass spectrometry formats (e.g., .raw) to open formats (mzML, mzXML, CDF) required by AutoTuner)
- **Autotuner** (R package implementing statistical inference-based parameter estimation for metabolomics data) — https://github.com/KujawinskiLaboratory/Autotuner
- **mtbls2** (R package providing raw untargeted metabolomics dataset for tutorial and validation)

## Examples

```
library(Autotuner); autoTuner_obj <- autoTuner(raw_data, sample_metadata, massThreshold=0.01); params <- returnParams(autoTuner_obj); write.csv(params, 'xcms_parameters.csv')
```

## Evaluation signals

- The returned parameter table contains exactly nine distinct numeric parameter estimates with no missing values
- Parameters are formatted consistently (e.g., all numeric, matching XCMS input schema) and can be parsed directly into XCMS without reformatting
- XCMS successfully processes the raw data using the extracted parameters without errors or warnings about invalid parameter ranges
- Resulting feature detection (number of detected m/z-RT peaks) is consistent across the sample set and does not show extreme outliers relative to expected metabolite diversity
- The parameter estimates are reproducible when AutoTuner is re-run on the same input data with identical lag, threshold, and influence settings

## Limitations

- Requires R version 3.6 or greater; compatibility with older R versions is not supported
- Minimum of 3 samples needed for robust statistical inference; smaller datasets may produce unreliable parameter estimates
- Mass threshold parameter (massThreshold) must be set greater than the expected analytical mass error of the specific mass analyzer; incorrect specification will bias parameter estimates
- Currently tested and validated only on qTOF, Orbitrap, and FTICR mass analyzers; performance on other instrument types is unknown
- No changelog documented; version tracking and breaking changes between releases are not formally tracked

## Evidence

- [intro] Using statistical inference, AutoTuner quickly finds estimates for nine distinct parameters.: "Using statistical inference, AutoTuner quickly finds estimates for nine distinct parameters."
- [intro] AutoTuner is a parameter tuning algorithm for XCMS, MZmine2, and other metabolomics data processing softwares.: "AutoTuner is a parameter tuning algorithm for XCMS, MZmine2, and other metabolomics data processing softwares."
- [other] The returnParams function outputs parameter estimates from EICparams results and the AutoTuner object that can be entered directly into XCMS to process raw untargeted metabolomics data.: "The returnParams function outputs parameter estimates from EICparams results and the AutoTuner object that can be entered directly into XCMS to process raw untargeted metabolomics data."
- [intro] The first part of AutoTuner involves the identification of peaks within the total ion current (TIC) of the samples loaded up into AutoTuner.: "The first part of AutoTuner involves the identification of peaks within the total ion current (TIC) of the samples loaded up into AutoTuner."
- [intro] The massThreshold is an absolute mass error that should be greater than the expected analytical capabilities of the mass analyzer.: "The massThreshold is an absolute mass error that should be greater than the expected analytical capabilities of the mass analyzer."
- [readme] For input, AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF).: "For input, AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF)."
- [readme] AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers.: "AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers."
