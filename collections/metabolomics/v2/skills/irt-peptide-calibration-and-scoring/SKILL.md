---
name: irt-peptide-calibration-and-scoring
description: Use when when you need to assess whether retention times measured on a given LC-MS run follow the expected linear relationship defined by iRT peptide standards (e.g., Pierce or Biognosys iRT peptides).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - RawFileReader
  - R base (stats::lm)
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- rawrr::readSpectrum
- Our .NET 8.0 [@dotnet] precompiled wrapper methods are bundled, including the runtime, in the `r BiocStyle::Biocpkg('rawrr')` executable file
- The extracted information is written to a temporary location on the harddrive, read back into memory and parsed into `R` objects using RawFileReader API
- 'ThermoFisher.CommonCore dlls can be obtained through: https://github.com/thermofisherlsms/RawFileReader'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_rawrr
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

# iRT-peptide-calibration-and-scoring

## Summary

Validates retention time (RT) linearity and instrument calibration by fitting a linear regression model to extracted ion chromatograms (XICs) of known iRT peptide standards, using their annotated iRT scores as the independent variable. The R-squared value (target ≥0.99) quantifies the degree of linear RT behavior across the peptide set.

## When to use

When you need to assess whether retention times measured on a given LC-MS run follow the expected linear relationship defined by iRT peptide standards (e.g., Pierce or Biognosys iRT peptides). This is appropriate when you have extracted XICs for 11+ known iRT peptides from a raw mass spectrometry file and want to validate instrument RT calibration quality or establish a RT prediction model for peptide identification.

## When NOT to use

- When the input raw file does not contain iRT peptide standards or the peptides were not ionized/detected (XICs are empty or sparse).
- When fewer than 5–6 iRT peptides are confidently detected; the regression requires sufficient degrees of freedom and coverage of the RT range.
- When you are analyzing a non-Orbitrap or non-Thermo instrument; the rawrr package is specific to Thermo Fisher Scientific .NET assemblies and .raw files.

## Inputs

- Thermo Fisher Scientific .raw file (Orbitrap instrument data)
- List of known iRT peptide precursor m/z values
- Annotated iRT reference scores (e.g., Pierce iRT standard peptides)
- Mass tolerance parameter (e.g., 10 ppm)

## Outputs

- rawrrChromatogram object (fitted intensity traces)
- Vector of rtFittedAPEX values (observed RT at peak maximum for each peptide)
- Linear regression model object (lm class in R)
- R-squared value quantifying RT linearity
- Residual plot or diagnostic statistics

## How to apply

Extract precursor m/z values and measured retention times for each iRT peptide standard using the rawrr::readChromatogram() function with mass tolerance ~10 ppm and XIC filter type. Fit intensity traces stored in rawrrChromatogram objects to identify the retention time at maximum intensity (rtFittedAPEX) for each peptide. Construct a linear regression model lm(rtFittedAPEX ~ iRTscore) where iRTscore is the annotated reference score for each peptide. Report the resulting R-squared value; values ≥0.99 indicate highly linear RT behavior and good instrument calibration. Lower R-squared values may suggest drift, temperature variation, or column degradation.

## Related tools

- **rawrr** (R package providing direct access to Thermo Orbitrap .raw file data; used to read file headers, extract XICs, and retrieve spectrum metadata) — https://github.com/fgcz/rawrr
- **RawFileReader** (.NET assembly (C#) underlying rawrr; implements low-level chromatogram and spectrum reading from binary .raw files) — https://github.com/thermofisherlsms/RawFileReader
- **R base (stats::lm)** (Fits linear regression model to RT observations and iRT scores; computes R-squared and residuals)

## Examples

```
C <- rawrr::readChromatogram(rawfile, mass = iRTmz, tol = 10, type = "xic", filter = "ms"); m <- lm(rtFittedAPEX ~ iRTscore); summary(m)$r.squared
```

## Evaluation signals

- R-squared value is ≥0.99 for iRT regression, confirming highly linear RT behavior across the 11+ peptides.
- Residual plot shows no systematic trend (e.g., funnel or sine pattern), indicating homoscedasticity and model validity.
- All iRT peptides are detected (non-empty XICs) and rtFittedAPEX values span the full RT range of the run without outliers.
- Fitted model coefficients (intercept and slope) are stable across replicate measurements of the same raw file, indicating reproducibility.
- Root mean square error (RMSE) or mean absolute error (MAE) of predicted vs. observed RT is <0.5 min, depending on method-specific tolerance.

## Limitations

- The rawrr package and RawFileReader .NET assembly are specific to Thermo Fisher Scientific Orbitrap instruments and .raw files; not applicable to other vendor formats (e.g., Bruker .d, Waters .raw, AB Sciex .wiff).
- On Windows systems, the decimal symbol must be configured as '.' for proper data extraction; regional locale settings can cause parsing errors.
- The quality of the regression depends on confident detection and annotation of iRT peptides; missing or misidentified peptides (e.g., due to ionization suppression or coelution) will reduce R-squared.
- RT linearity assumes stable column conditions and temperature; significant drift or column degradation during the run can artificially lower R-squared even with good instrument calibration.
- The choice of mass tolerance (e.g., 10 ppm) and XIC extraction filter directly affects which scans are included; too loose a tolerance may capture co-eluting interferents, biasing rtFittedAPEX.

## Evidence

- [results] Extract precursor m/z and RT using rawrr::readChromatogram() with mass tolerance and XIC filter: "Extract precursor m/z values and retention times for known iRT peptide standards using rawrr::readChromatogram() with mass tolerance 10 ppm and XIC filter."
- [results] Fit intensity traces to extract rtFittedAPEX and construct linear regression model: "we extract the RTs at the maximum of the fitted intensity traces stored in the `rawrrChromatogram` object and fit a linear model"
- [results] R-squared of 0.9999 indicates highly linear RT behavior: "The corresponding R-squared indicates that the RTs behave highly linear"
- [intro] rawrr wraps RawFileReader .NET assembly for direct access to Orbitrap data: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [intro] Gap in R ecosystem for raw data reading; rawrr closes this for direct analysis pipelines: "A library providing raw data reading would finally close the gap and facilitate modular end-to-end analysis pipeline development in R"
- [discussion] Windows decimal symbol configuration requirement: "On Windows, the decimal symbol has to be configured as a '.'!"
- [methods] iRT regression model fitting on known peptide standards: "Fit intensity traces stored in rawrrChromatogram objects to extract retention times at maximum intensity (rtFittedAPEX)."
