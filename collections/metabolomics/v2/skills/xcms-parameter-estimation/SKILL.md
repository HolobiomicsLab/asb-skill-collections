---
name: xcms-parameter-estimation
description: Use when you have raw untargeted metabolomics data (at least 3 samples in mzML, mzXML, or CDF format) from qTOF, orbitrap, or Fourier transform ion cyclotron resonance mass analyzers and need to obtain optimized XCMS processing parameters tailored to your specific instrument and dataset rather than.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - R
  - XCMS
  - AutoTuner
  - MSconvert
derived_from:
- doi: 10.1101/812370
  title: AutoTuner parameter selection
evidence_spans:
- knitr::rmarkdown
- AutoTuner is a parameter tuning algorithm for XCMS, MZmine2, and other metabolomics data processing softwares.
- the estimates may be entered directly into XCMS to processes raw untargeted metabolomics data.
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/812370
  all_source_dois:
  - 10.1101/812370
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# XCMS parameter estimation

## Summary

Automated inference of nine dataset-specific parameters required by XCMS to process untargeted metabolomics data from raw mass spectrometry files. This skill uses statistical analysis of extracted ion chromatograms within isolated TIC peak regions to derive tuned parameter estimates suitable for direct entry into XCMS.

## When to use

Use this skill when you have raw untargeted metabolomics data (at least 3 samples in mzML, mzXML, or CDF format) from qTOF, orbitrap, or Fourier transform ion cyclotron resonance mass analyzers and need to obtain optimized XCMS processing parameters tailored to your specific instrument and dataset rather than relying on generic defaults.

## When NOT to use

- Your mass spectrometry data are already processed or feature-extracted; XCMS parameter tuning applies only to raw instrument data.
- You have fewer than 3 samples; AutoTuner requires multiple samples to achieve robust statistical inference.
- Your instrument is not among those tested: qTOF, orbitrap, or FTICR mass analyzers; AutoTuner performance on other analyzer types is not documented.

## Inputs

- At least 3 raw mass spectrometry files (mzML, mzXML, or CDF format)
- Sample metadata spreadsheet (two columns: sample name matching raw files, and experimental factor assignment)
- AutoTuner object with isolated TIC peak regions and EICparams estimates

## Outputs

- Nine distinct XCMS parameter estimates (numeric values)
- Parameter estimate table in structured format (CSV or TSV) suitable for XCMS input

## How to apply

Load your raw mass spectrometry data and experimental metadata (sample-to-condition mapping) into the AutoTuner R package. AutoTuner first identifies peaks in the total ion current (TIC) using sliding window analysis with user-tuned lag, threshold, and influence parameters. For each isolated TIC peak region, the EICparams function extracts ion chromatograms with mass-based filtering (massThresh, typically 0.005 absolute mass error) and applies gap handling (useGap=TRUE) to refine parameter estimates. AutoTuner then statistically infers the nine XCMS-relevant parameters from these EIC analyses. Finally, invoke returnParams on the resulting AutoTuner object to output a table of the nine parameter estimates in a format ready for direct XCMS input.

## Related tools

- **AutoTuner** (Automated parameter tuning engine; performs TIC peak identification, EIC extraction, and statistical inference of XCMS parameters) — https://github.com/KujawinskiLaboratory/Autotuner
- **XCMS** (Target data processing software whose parameters are estimated by AutoTuner)
- **R** (Runtime environment for installing and executing AutoTuner via devtools or BiocManager)
- **MSconvert** (Preprocessing tool for converting raw vendor instrument formats to open mzML/mzXML/CDF formats consumed by AutoTuner)

## Examples

```
library(Autotuner); at <- AutoTuner(mzML_files, pheno_metadata); at <- isolatePeaks(at); at <- EICparams(at, massThresh=0.005, useGap=TRUE); params_table <- returnParams(at)
```

## Evaluation signals

- The returnParams function successfully outputs exactly nine numeric parameter estimates without errors or missing values.
- The nine parameters can be directly parsed and entered into XCMS configuration without format conversion or data loss.
- The parameter estimates fall within biologically plausible ranges for your instrument class (e.g., ppm error estimates align with declared mass analyzer specifications).
- When XCMS is run using the estimated parameters on the same samples used for tuning, feature detection sensitivity and specificity are improved relative to XCMS defaults as measured by feature count and peak quality metrics.
- The parameter table is reproducible: re-running AutoTuner with identical inputs and random seeds produces the same nine estimates.

## Limitations

- AutoTuner requires R version 3.6 or greater and may have dependency conflicts with older or newer R versions.
- Accuracy of parameter estimates depends on having sufficient signal diversity in the input samples; low-complexity or heavily depleted samples may yield unreliable estimates.
- The sliding window analysis for TIC peak identification requires manual tuning of lag, threshold, and influence parameters; suboptimal choices can cascade through downstream parameter inference.
- AutoTuner has been tested only on qTOF, orbitrap, and FTICR mass analyzers; performance on other instrument types (e.g., triple quadrupole, ion trap) is unvalidated.

## Evidence

- [intro] Using statistical inference, AutoTuner quickly finds estimates for nine distinct parameters.: "Using statistical inference, AutoTuner quickly finds estimates for nine distinct parameters."
- [other] EICparams processes isolated TIC peak regions by extracting ion chromatograms and filtering based on a massThresh parameter (absolute mass error); when useGap=TRUE, the function applies gap-based filtering to refine parameter estimates.: "EICparams processes isolated TIC peak regions by extracting ion chromatograms and filtering based on a massThresh parameter (absolute mass error); when useGap=TRUE, the function applies gap-based"
- [other] The returnParams function outputs parameter estimates from EICparams results and the AutoTuner object that can be entered directly into XCMS to process raw untargeted metabolomics data.: "The returnParams function outputs parameter estimates from EICparams results and the AutoTuner object that can be entered directly into XCMS"
- [readme] For input, AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF).: "AutoTuner requires at least 3 samples of raw data converted from proprietary instrument formats (eg .mzML, .mzXML, or .CDF)."
- [readme] AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers.: "AutoTuner has been tested on untargeted data generated on qTOF, orbitrap and Fourier transform ion cyclotron resonance mass analyzers."
