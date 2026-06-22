---
name: irt-peptide-standard-matching
description: Use when you have a Thermo Fisher Scientific .raw file from an LC-MS run containing a spiked iRT peptide standard mix (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2238
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RawFileReader
  - rawrr
  - MsBackendRawFileReader
  - Biognosys iRT standard mix
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

# iRT peptide standard matching

## Summary

Align observed retention times from iRT peptide standards in LC-MS/MS data to their known indexed retention time (iRT) scores, then fit a linear regression model to establish a calibrated RT-to-iRT mapping for the experimental run. This enables normalized retention time reporting and cross-experiment comparability.

## When to use

You have a Thermo Fisher Scientific .raw file from an LC-MS run containing a spiked iRT peptide standard mix (e.g., Biognosys iRT standards), and you need to (1) calibrate retention times to a universal scale, (2) verify LC gradient linearity, or (3) enable normalized RT reporting across multiple experiments or instruments. Apply this skill when MS1-level scans are available and iRT peptides are detectable in the data.

## When NOT to use

- The .raw file does not contain iRT peptide standards or they are undetectable in the chromatographic data.
- Only MS2-level scans are available; MS1-level scans are required to extract iRT peptide chromatograms.
- The data is already in mzML or other exchange format; use rawrr only on binary .raw files from Thermo instruments.

## Inputs

- Thermo Fisher Scientific .raw file (binary format)
- iRT peptide reference table with peptide sequences and iRT scores (e.g., Biognosys iRT mix reference)
- MS1-level scan index

## Outputs

- Linear regression model object with intercept and slope coefficients
- Data frame of matched iRT peptide scans with observed RTs and known iRT scores
- R² goodness-of-fit statistic for the RT-vs-iRT relationship
- Calibrated RT values for unknown peptides in the same run

## How to apply

Extract MS1-level scan indices from the raw file header using readIndex(). Read chromatogram intensity traces for the known iRT peptides (e.g., GAGSSEPVTGLDAK, LGGNETIPHLAVAGK) using readChromatogram() and fit splines to each trace to identify apex retention times. Map each observed apex RT to its known iRT score from the Biognosys reference standard. Fit a linear model lm(rtFittedAPEX ~ iRTscore) to the matched pairs. The intercept (a) represents the predicted RT of the zero-iRT reference peptide GAGSSEPVTGLDAK, while the slope (b) reflects the gradient change rate (typically ~1.5% buffer B per minute during a 20 min gradient). High R² (indicative of highly linear behavior) confirms successful calibration. Use this calibrated model to normalize RTs from unknown peptides in the same run.

## Related tools

- **rawrr** (R package that wraps the RawFileReader .NET assembly to read spectral data, chromatograms, and file headers from Thermo .raw files) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly providing low-level C# API to access binary .raw file contents; invoked by rawrr via system calls) — https://github.com/thermofisherlsms/RawFileReader
- **MsBackendRawFileReader** (Bioconductor backend that integrates rawrr with the Spectra package for unified spectral data access and retention time calibration workflows) — https://github.com/cpanse/MsBackendRawFileReader
- **Biognosys iRT standard mix** (Reference peptide standard with known iRT scores; provides the ground truth iRT values for calibration)

## Examples

```
library(rawrr); installRawrrExe(); H <- readFileHeader('autoQC01.raw'); idx <- readIndex('autoQC01.raw'); ms1_idx <- subset(idx, msLevel == 1); chrom <- readChromatogram('autoQC01.raw', irt_peptides); rt_apex <- sapply(chrom, function(x) x$rtFitted[which.max(x$intensity)]); model <- lm(rt_apex ~ known_irt_scores); summary(model)$r.squared
```

## Evaluation signals

- R² value is ≥ 0.99, indicating highly linear retention time behavior with iRT scores and confirming successful calibration.
- Intercept (a) coefficient is within ±0.5 min of the expected RT of GAGSSEPVTGLDAK (typically 18–22 min for a 20 min LC gradient).
- Slope (b) coefficient is approximately 1.5% buffer B per minute, confirming expected LC gradient linearity; deviations suggest non-linear or irregular gradient profiles.
- All matched iRT peptides plot near the fitted regression line with residuals < ±0.5 min; large outliers indicate missed apex detection or mis-identification.
- Fitted model can be applied to unknown peptides in the same run to produce normalized RT values comparable across replicate runs or different instruments.

## Limitations

- Requires iRT peptide standards to be spiked into the sample; not applicable to data without them.
- Works only on Thermo Fisher Scientific Orbitrap .raw files; other vendor formats (Waters, AB Sciex, Bruker) require alternative raw data readers.
- Assumes MS1-level scans are present; if only MS2 data is available, iRT peptide chromatograms cannot be extracted.
- Spline fitting and apex detection may fail if iRT peptide peaks are weak, co-eluting, or obscured by background noise.
- Linear model assumes a simple linear RT-vs-iRT relationship; highly non-linear or segmented LC gradients may violate this assumption and yield poor fits.

## Evidence

- [other] Map iRT peptide scans to their known iRT scores (from Biognosys iRT peptide mix reference). Fit a linear model lm(rtFittedAPEX ~ iRTscore) to the matched retention time and iRT score pairs.: "Map iRT peptide scans to their known iRT scores (from Biognosys iRT peptide mix reference). Fit a linear model lm(rtFittedAPEX ~ iRTscore)"
- [other] Extract retention times at the maximum of the fitted intensity traces stored in the rawrrChromatogram object.: "Extract retention times at the maximum of the fitted intensity traces stored in the rawrrChromatogram object"
- [other] The fitted iRT regression model shows highly linear retention time behavior (high R²), with the intercept (a) equal to the predicted RT of the iRT peptide GAGSSEPVTGLDAK (zero iRT score reference point) and the slope (b) equivalent to the gradient change rate of approximately 1.5% buffer B per minute during the 20 min LC gradient.: "intercept (a) equal to the predicted RT of the iRT peptide GAGSSEPVTGLDAK (zero iRT score reference point) and the slope (b) equivalent to the gradient change rate of approximately 1.5% buffer B"
- [other] Read the intensity traces (chromatogram data) using readChromatogram() for the iRT peptides.: "Read the intensity traces (chromatogram data) using readChromatogram() for the iRT peptides"
- [results] using only MS1-level scans: "using only MS1-level scans"
- [methods] R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call.: "R functions requesting access to data stored in binary raw files invoke compiled C# wrapper methods using a system call"
- [intro] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [results] The corresponding R-squared indicates that the RTs behave highly linear: "The corresponding R-squared indicates that the RTs behave highly linear"
