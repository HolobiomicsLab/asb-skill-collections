---
name: spectral-intensity-trace-extraction
description: Use when you have a Thermo Fisher Orbitrap .raw file and need to recover the intensity profile of a specific m/z value or peptide across the LC separation dimension (chromatogram), particularly when calibrating retention times against internal standards (iRT peptides), performing quality control.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3371
  tools:
  - RawFileReader
  - rawrr
  - rawDiag
  - MsBackendRawFileReader
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- Calling a wrapper method typically results in the execution of methods defined in the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific.
- invoke compiled `C#` wrapper methods using a system call. Calling a wrapper method typically results in the execution of methods defined in the `RawFileReader` dynamic link library provided by Thermo
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr_2_cq
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_rawrr_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.10.30.362533
  all_source_dois:
  - 10.1101/2020.10.30.362533
  - 10.1021/acs.jproteome.0c00866
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-intensity-trace-extraction

## Summary

Extract intensity traces (extracted ion chromatograms or full chromatograms) from Thermo Fisher Scientific Orbitrap .raw files to recover time-resolved signal profiles for targeted peptides or compounds. This skill bridges direct binary raw file access to quantitative time-series data used in quality control, retention time calibration, and peak detection workflows.

## When to use

You have a Thermo Fisher Orbitrap .raw file and need to recover the intensity profile of a specific m/z value or peptide across the LC separation dimension (chromatogram), particularly when calibrating retention times against internal standards (iRT peptides), performing quality control diagnostics, or detecting and quantifying elution peaks for targeted analytes.

## When NOT to use

- Input is already converted to mzML or other open exchange format and you have access to standard tools like ProteoWizard; rawrr is most valuable for direct proprietary .raw access to avoid lossy conversion steps.
- You require real-time or streaming chromatogram reconstruction; rawrr is designed for batch post-acquisition analysis and file I/O to temporary disk.
- The analysis does not involve Thermo Fisher Orbitrap instruments; RawFileReader and rawrr are vendor-specific to .raw files and will not read ABSciex, Waters, or Bruker binary formats.

## Inputs

- Thermo Fisher Scientific .raw file (binary Orbitrap data)
- m/z value(s) or mass window(s) of interest (numeric range)
- optional: reference retention time standard(s) with known identity (e.g., iRT peptide mix with published iRT scores)

## Outputs

- rawrrChromatogram or rawrrChromatogramSet object (intensity trace with fitted apex retention times)
- numeric vector or data.frame of retention times at peak maxima
- optional: linear regression model (lm object) relating observed RTs to reference scores (iRT model)

## How to apply

Install the rawrr R package and its RawFileReader executable dependency via rawrr::installRawrrExe(). Load the .raw file using readFileHeader() to obtain metadata (scan count, time range, instrument type). Use readChromatogram() to extract intensity traces; the function returns a rawrrChromatogram object containing fitted intensity values across the retention time dimension. For iRT calibration specifically, extract chromatogram data for known iRT peptide mass windows, identify peak maxima (apex retention times) from the fitted traces, and map these to reference iRT scores to construct a linear model. The resulting intercept and slope encode the LC gradient behavior and provide a calibration standard for method evaluation.

## Related tools

- **rawrr** (R package wrapper providing readChromatogram() function to extract intensity traces from binary .raw files via RawFileReader API) — https://github.com/fgcz/rawrr
- **RawFileReader** (Vendor-provided C# .NET assembly (underlying engine) that performs low-level binary parsing and data extraction from Thermo .raw files) — https://github.com/thermofisherlsms/RawFileReader
- **rawDiag** (Companion R package for visualization and diagnostic interpretation of raw Orbitrap chromatograms and quality metrics) — https://github.com/fgcz/rawDiag
- **MsBackendRawFileReader** (Bioconductor backend integrating rawrr into the Spectra ecosystem for standardized on-disk spectral data access) — https://github.com/cpanse/MsBackendRawFileReader

## Examples

```
library(rawrr); installRawrrExe(); chrom <- readChromatogram('autoQC01.raw', mass=391.2843, tol=0.01); rtApex <- chrom$rtFittedAPEX; model <- lm(rtApex ~ iRTscore)
```

## Evaluation signals

- rawrrChromatogram object is successfully created with non-null intensity and retention time vectors; dimensions match the LC scan count and time range reported by readFileHeader().
- Fitted apex retention times for iRT peptides are within the expected LC gradient window (e.g., 5–20 min for a 20 min gradient) and increase monotonically with iRT score.
- Linear regression model (lm(rtFittedAPEX ~ iRTscore)) exhibits high R² (>0.99 typical for iRT) indicating highly linear retention time behavior; residuals are randomly distributed with no systematic bias.
- Intercept value matches the predicted RT of the zero-score iRT reference peptide (GAGSSEPVTGLDAK); slope value is consistent with LC gradient rate (e.g., ~1.5% buffer B per minute).
- Peak maxima coordinates are stable across replicate chromatogram extractions from the same .raw file, confirming data integrity and reproducibility.

## Limitations

- rawrr requires Windows, Linux, or macOS with .NET Core or Mono runtime installed; RawFileReader assembly is proprietary to Thermo Fisher Scientific and not open-source.
- Chromatogram extraction requires file I/O (binary .raw read → temporary disk write → R parse), making it slower than in-memory operations; batch processing many .raw files can be I/O-bound.
- The skill applies only to Thermo Orbitrap instruments and proprietary .raw format; generalization to other vendor formats (Waters, Bruker, ABSciex) requires different APIs.
- Fitted intensity traces may smooth or interpolate apex positions depending on internal smoothing algorithms in rawrr; exact peak detection parameters are not user-tunable in the standard function signature.
- iRT calibration assumes availability of the iRT peptide standard and reference scores from Biognosys; absent or contaminated iRT peaks will degrade model fit and retention time prediction reliability.

## Evidence

- [results] how the function `readChromatogram()` is called on the `R` command line to return a `rawrrChromatogramSet` object: "how the function `readChromatogram()` is called on the `R` command line to return a `rawrrChromatogramSet` object"
- [results] we now extract the RTs at the maximum of the fitted intensity traces stored in the `rawrrChromatogram` object: "we now extract the RTs at the maximum of the fitted intensity traces stored in the `rawrrChromatogram` object"
- [other] Extract retention times at the maximum of the fitted intensity traces using readChromatogram(): "Extract retention times at the maximum of the fitted intensity traces stored in the rawrrChromatogram object."
- [other] Fit a linear model lm(rtFittedAPEX ~ iRTscore) to the matched retention time and iRT score pairs.: "Fit a linear model lm(rtFittedAPEX ~ iRTscore) to the matched retention time and iRT score pairs."
- [results] The corresponding R-squared indicates that the RTs behave highly linear: "The corresponding R-squared indicates that the RTs behave highly linear"
- [intro] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [readme] The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package: "The package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package"
- [readme] provides an R interface to your instrument raw data: "provides an R interface to your instrument raw data"
