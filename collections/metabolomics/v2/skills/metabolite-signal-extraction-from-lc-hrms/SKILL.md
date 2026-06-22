---
name: metabolite-signal-extraction-from-lc-hrms
description: Use when you have raw untargeted LC/HRMS data (mzXML, mzML, or netCDF format) from population-scale studies (n > 500 samples) and need to extract a comprehensive peaklist with aligned features across all samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3637
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0091
  tools:
  - IDSL.IPA
  - R
  - MZmine 2
  - xcms
  - MS-DIAL
  - RnetCDF
  - IDSL.UFA
  - IDSL.CSA
derived_from:
- doi: 10.1021/acs.jproteome.2c00120
  title: IDSL.IPA
evidence_spans:
- '**Intrinsic Peak Analysis (IPA)** by the [**Integrated Data Science Laboratory for Metabolomics and Exposomics (IDSL.ME)**](https://www.idsl.me) is a light-weight R package'
- light-weight R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idsl_ipa_cq
    doi: 10.1021/acs.jproteome.2c00120
    title: IDSL.IPA
  dedup_kept_from: coll_idsl_ipa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00120
  all_source_dois:
  - 10.1021/acs.jproteome.2c00120
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-signal-extraction-from-lc-hrms

## Summary

Extraction of metabolite peaks from untargeted LC/HRMS data through a multi-stage algorithmic pipeline that begins with EIC candidate generation, followed by peak detection, property evaluation, and batch-wise retention time correction. This skill is essential for generating high-quality feature tables from population-scale metabolomics studies where sensitivity and specificity across hundreds of samples are critical.

## When to use

Apply this skill when you have raw untargeted LC/HRMS data (mzXML, mzML, or netCDF format) from population-scale studies (n > 500 samples) and need to extract a comprehensive peaklist with aligned features across all samples. The skill is particularly valuable when you require 19+ chromatographic peak properties (peak area, S/N, tailing factor, isotope ratios, etc.) and must correct for retention time drift across multiple analytical batches.

## When NOT to use

- Input is already a processed peak feature table or peaklist; use peak alignment/annotation instead.
- Targeted analysis with a small number of known m/z-RT pairs; use IPA_targeted function instead.
- Data from only a single analytical batch where retention time correction is not needed (though still applicable).

## Inputs

- raw LC/HRMS data files in mzXML, mzML, or netCDF format
- IPA parameter spreadsheet (IPA_parameters.xlsx) with user-defined thresholds
- MS1-level high-resolution mass spectrometry scans
- retention time correction reference markers (for multi-batch studies)

## Outputs

- individual peaklists per HRMS file in .Rdata and .csv formats
- peak alignment tables across all samples
- untargeted extracted ion chromatograms (EICs) in batch-aggregated form
- 19-property peak feature table (area, S/N, width, isotope ratios, tailing, gaussianity, etc.)
- batch-corrected retention time indices
- pairwise correlation lists for aligned peak heights and gap-filled tables

## How to apply

Load raw LC/HRMS data (mzXML, mzML, or netCDF) into IDSL.IPA using the IPA_workflow function with a parameter spreadsheet. The algorithm first generates EIC candidates by binning mass spectral data across the full m/z range and applying intensity thresholding and noise filtering to retain only significant signals. Peak detection follows, calculating 19 chromatographic properties including peak area, signal-to-noise ratio (using baseline, xcms, and RMS methods), nIsoPair, RCS, peak width, asymmetry factor, and gaussian-like metrics. After individual-file peak detection, implement retention time correction across batches using endogenous reference markers for multi-batch studies, and finally perform peak alignment and annotation. Parameter selection is guided by a user-friendly spreadsheet (IPA_parameters.xlsx) that allows adjustment of thresholds, processing threads, and EIC output options.

## Related tools

- **IDSL.IPA** (Primary extraction engine; implements EIC candidate generation, peak detection, property evaluation, mass correction, and batch retention time correction) — https://github.com/idslme/IDSL.IPA
- **R** (Execution environment for IDSL.IPA package)
- **MZmine 2** (Comparative peak-picking tool; IDSL.IPA outperforms it in sensitivity, specificity, and speed)
- **xcms** (Comparative peak-picking tool; used as reference for S/N calculation method; outperformed by IDSL.IPA)
- **MS-DIAL** (Comparative peak-picking tool; outperformed by IDSL.IPA)
- **RnetCDF** (Optional dependency for processing netCDF/CDF mass spectrometry data) — https://CRAN.R-project.org/package=RNetCDF
- **IDSL.UFA** (Downstream integration: molecular formula annotation of aligned peaks) — https://github.com/idslme/IDSL.UFA
- **IDSL.CSA** (Downstream integration: clustering recurring ions to generate composite spectra) — https://github.com/idslme/IDSL.CSA

## Examples

```
library(IDSL.IPA)
IPA_workflow("/path/to/IPA_parameters.xlsx")
```

## Evaluation signals

- Individual peaklists contain all 19 chromatographic peak properties and match expected column schema (peak area, S/N, nIsoPair, RCS, asymmetry factor, tailing factor, etc.).
- Peak alignment tables show consistent number of detected features per sample with <5% missing values in gap-filled tables for valid peaks.
- Retention time correction reduces inter-batch RT drift to within ±0.1 minutes across batches (when reference markers are used).
- EIC output images (if PARAM0009='YES') display clean, resolved chromatographic peaks with appropriate signal-to-noise ratios and minimal baseline noise.
- Pairwise correlation lists identify expected isotope pairs (13C offset ~1.003 Da for doubly-charged ions, etc.) and known adduct relationships at biologically plausible correlation thresholds.

## Limitations

- Requires high-resolution mass spectrometry data; applicability to low-resolution instruments (unit mass) is not stated.
- Multi-batch retention time correction relies on availability of endogenous reference markers; studies without reliable RTs standards may experience residual batch effects.
- Population-scale applicability emphasized for n > 500 samples; performance and computational cost for smaller studies not explicitly characterized.
- Positive and negative ionization modes must be processed separately; combined polarity analysis not supported.
- Peak annotation step requires integration with external tools (IDSL.UFA, IDSL.UFAx); standalone peak detection does not provide metabolite identity.

## Evidence

- [readme] extracts peaks for organic small molecules from untargeted liquid chromatography high resolution mass spectrometry (LC/HRMS) data in population scale projects: "extracts peaks for organic small molecules from untargeted liquid chromatography high resolution mass spectrometry (LC/HRMS) data in population scale projects"
- [other] IDSL.IPA implements extracted ion chromatogram (EIC) candidate generation as the first algorithmic stage in a suite of algorithms that also includes peak detection, peak property evaluation, recursive mass correction, retention time correction across multiple batches, and peak annotation.: "IDSL.IPA implements extracted ion chromatogram (EIC) candidate generation as the first algorithmic stage in a suite of algorithms that also includes peak detection, peak property evaluation,"
- [other] Extract ion chromatograms by binning mass spectral data across the full m/z range to identify candidate signals. Apply intensity thresholding and noise filtering to retain only significant EIC candidates.: "Extract ion chromatograms by binning mass spectral data across the full m/z range to identify candidate signals. Apply intensity thresholding and noise filtering to retain only significant EIC"
- [readme] Calculating 19 chromatographic peak properties such as peak area, nIsoPair, RCS, cumulated intensity, R<sup>13</sup>C, peak width, RPW, number of separation trays, asymmetry factor, USP tailing factor, skewness using derivative method, symmetry using pseudo-moments, skewness using pseudo-moments, gaussianity, S/N using baseline, S/N using the *xcms* method, S/N using the RMS method, and sharpness.: "Calculating 19 chromatographic peak properties such as peak area, nIsoPair, RCS, cumulated intensity, R<sup>13</sup>C, peak width, RPW, number of separation trays, asymmetry factor, USP tailing"
- [readme] Retention time correction using endogenous reference markers for multi-batch large scale studies: "Retention time correction using endogenous reference markers for multi-batch large scale studies"
- [readme] IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, *xcms*, and MS-DIAL in terms of sensitivity, specificity and speed.: "IDSL.IPA is able to outperform similar peak picking tools such as MZmine 2, *xcms*, and MS-DIAL in terms of sensitivity, specificity and speed."
- [readme] Parameter selection through a user-friendly and well-described parameter spreadsheet: "Parameter selection through a user-friendly and well-described parameter spreadsheet"
- [readme] To process your mass spectrometry data (mzXML, mzML, netCDF), download the IPA parameter spreadsheet and select the parameters accordingly and then use this spreadsheet as the input for the `IPA_workflow` function: "To process your mass spectrometry data (mzXML, mzML, netCDF), download the IPA parameter spreadsheet and select the parameters accordingly and then use this spreadsheet as the input for the"
