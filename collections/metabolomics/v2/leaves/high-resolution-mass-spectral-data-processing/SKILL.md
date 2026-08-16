---
name: high-resolution-mass-spectral-data-processing
description: Use when you have high-resolution mass-spectrometry data (Orbitrap, GC-CI-MS)
  from stable-isotope labeling experiments and need to quantify isotopologue abundances
  for a defined list of target compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3520
  tools:
  - R
  - isoSCAN
  - mzR
  - enviPat
  - Proteowizard MSconvert
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.0c02998
  title: isoSCAN
evidence_spans:
- To Install from R console
- 'To Install from R console: ```` install.packages("devtools", dependencies=TRUE)
  library(devtools)'
- install_github("jcapelladesto/isoSCAN") library(isoSCAN)
- install_github("jcapelladesto/isoSCAN")
- isoSCAN uses `mzR` package in order to read MS files
- isoSCAN makes use of __enviPat__ package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isoscan_cq
    doi: 10.1021/acs.analchem.0c02998
    title: isoSCAN
  dedup_kept_from: coll_isoscan_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c02998
  all_source_dois:
  - 10.1021/acs.analchem.0c02998
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# high-resolution-mass-spectral-data-processing

## Summary

Automated extraction of isotopologue abundances and quantification metrics (mass error, peak area, intensity) from high-resolution Orbitrap or GC-CI-MS data by converting vendor formats to centroided mzML, loading a formulaTable of target compounds, and calling the autoQ function with isotope-pattern matching via enviPat. This skill is essential when stable-isotope labeling experiments require precise measurement of M+0, M+1, M+2 isotopic forms across multiple samples.

## When to use

Apply this skill when you have high-resolution mass-spectrometry data (Orbitrap, GC-CI-MS) from stable-isotope labeling experiments and need to quantify isotopologue abundances for a defined list of target compounds. Use it specifically when your input is vendor-format raw data that must be converted to mzML, you have retention time and monoisotopic m/z values for each compound, and you want automated extraction of abundance, ppm mass error, peak area (area), and maximum intensity (maxo) for each isotopic form per sample condition.

## When NOT to use

- Input data is already in profile format and you require centroided mzML; use Proteowizard MSconvert first.
- You have low-resolution data; switch to profile-format mzML instead of centroiding (autoQ can process both but requires different preprocessing).
- Your target compound list lacks precise retention time and monoisotopic m/z values; the formulaTable columns are mandatory and missing data will cause autoQ to fail.
- You need to detect unknown or unanticipated isotopologues; autoQ is designed for a predefined formulaTable and will not discover novel compounds.

## Inputs

- Vendor-format raw mass-spectrometry files (Orbitrap .raw, GC-CI-MS proprietary formats)
- formulaTable data frame (CSV) with columns: CompoundName, mz, RT, Formula, NumAtoms
- enviPat isotopes object for isotope-pattern database
- Centroided mzML files (post-Proteowizard MSconvert conversion)

## Outputs

- Quantification table with columns: CompoundName, m/z, abundance, Isotopologue (M+0, M+1, M+2), ppm mass error, maxo (maximum intensity), area (peak area)
- Quality-control plots (rawPlot, meanRawPlot) showing peak shape and intensity across scans and samples

## How to apply

First, prepare a formulaTable data frame with columns CompoundName, mz (monoisotopic ion), RT (retention time in seconds), Formula (must match derivatized formula for high-resolution), and NumAtoms, loaded via read.csv. Next, convert your raw mass-spectrometry data from vendor format to centroided mzML using Proteowizard MSconvert (essential for high-resolution; use peakPicking=True). Load the enviPat isotopes object for isotope-pattern calculation. Call the autoQ function with parameters: labelatom='13C' (or other stable isotope), mzerror or maxppm (mass tolerance, typically a few ppm), RTwin (retention-time window around RT), minscans, SNR (signal-to-noise ratio threshold), and minwidth/maxwidth (peak width constraints in scans). The function will return a table with CompoundName, m/z, abundance, Isotopologue designation (M+0, M+1, M+2), ppm mass error, and paired maxo and area values. Inspect results using rawPlot and meanRawPlot for quality control to detect moving peaks, noise, or saturation before reporting quantification.

## Related tools

- **isoSCAN** (Core R package that implements the autoQ function for automated isotopologue extraction and quantification from mzML files) — https://github.com/jcapelladesto/isoSCAN
- **Proteowizard MSconvert** (Converts vendor-format raw data to centroided mzML format required for autoQ processing of high-resolution data)
- **mzR** (Underlying R package used by isoSCAN to read and parse mzML/mzXML files)
- **enviPat** (Provides isotope-pattern calculation and database to distinguish targeted compounds from interfering ions in high-resolution spectra)
- **R** (Runtime environment and scripting language for executing autoQ, metBarPlot, rawPlot, and meanRawPlot functions)

## Examples

```
library(isoSCAN); formulaTable <- read.csv('targets.csv'); autoQ(formulaTable=formulaTable, files='sample.mzML', labelatom='13C', maxppm=5, RTwin=30, SNR=3, minscans=5, minwidth=10, maxwidth=100)
```

## Evaluation signals

- Output table contains no NA or NaN values for CompoundName, m/z, abundance, or ppm columns for detected isotopologues; missing values indicate autoQ failed to match a compound or peak.
- Ppm mass error for detected peaks falls within the tolerance specified in maxppm parameter (typically 1–5 ppm for high-resolution Orbitrap); values outside this range suggest misidentification or miscalibration.
- M+0, M+1, M+2 abundance values sum to 100% (or close to it) for each compound per sample; large deviations suggest isotope-pattern mismatch or peak overlap.
- rawPlot and meanRawPlot inspection shows clean, symmetric peak shapes within the minwidth/maxwidth range; jagged, split, or extremely broad peaks indicate SNR, retention-time window, or formula-mismatch problems.
- Replicate samples show consistent area and maxo values (low coefficient of variation across replicates); high variance suggests process variation, calibration drift, or suboptimal SNR threshold.

## Limitations

- formulaTable Formula column must match the derivatized form of the compound for high-resolution data; incorrect or non-derivatized formulas will cause peak-pattern mismatches and missed detections.
- autoQ requires accurate retention-time windows (RTwin parameter); peaks with poor or shifting retention times may fall outside the window and be missed.
- Mass accuracy and resolution of the Orbitrap or GC-CI-MS instrument directly affect sensitivity to isotope patterns; low-resolution or poorly calibrated instruments may fail to resolve M+0, M+1, M+2 isotopologues.
- No changelog is available for the isoSCAN package; updates and bug fixes may not be documented, making reproducibility across versions potentially problematic.
- autoQ is designed for a predefined formulaTable and cannot discover novel or unlabeled compounds; all target compounds must be specified in advance.

## Evidence

- [other] The autoQ function returns for high-resolution Orbitrap data a table with columns for CompoundName, m.z, abundance, Isotopologue designation (M+0, M+1, M+2), ppm mass error, and paired maxo and area values for each isotopic form per sample condition.: "The autoQ function returns for high-resolution Orbitrap data a table with columns for CompoundName, m.z, abundance, Isotopologue designation (M+0, M+1, M+2), ppm mass error, and paired maxo and area"
- [intro] In the case of High-resolution, __please use centroiding__ (e.g. _peakPicking= True_ in MSconvert): "In the case of High-resolution, please use centroiding (e.g. peakPicking= True in MSconvert)"
- [intro] Before starting with file processing, we need to load the _targeted compounds_ as a _formulaTable_ data frame. This can be done either with `read.table` or `read.csv` functions.: "load the targeted compounds as a formulaTable data frame. This can be done either with `read.table` or `read.csv` functions"
- [intro] _formulaTable_ __must__ contain the following column names in no specific order: * __CompoundName__ * __mz__ * __RT__ * __Formula__ * __NumAtoms__: "formulaTable must contain the following column names: CompoundName, mz, RT, Formula, NumAtoms"
- [intro] This parameters refer to peak width and number of scans recorded, together with signal-to-noise ratio and mass error.: "autoQ uses parameters: minscans, SNR (signal-to-noise ratio), mzerror or maxppm (mass error), RTwin (retention time window), maxwidth and minwidth (peak width parameters)"
- [intro] `rawPlot` and `meanRawPlot` functions should be used for quality control purposes. They are useful to check for moving peaks, noisy spots or saturated peaks.: "rawPlot and meanRawPlot functions should be used for quality control purposes. They are useful to check for moving peaks, noisy spots or saturated peaks"
- [intro] The first step is file format transformation, `isoSCAN` uses `mzR` package in order to read MS files. Therefore, you will have to transform the raw data from vendor format into __mz(X)ML__ format: "transform the raw data from vendor format into mz(X)ML format using Proteowizard MSconvert or similar tools"
- [intro] Higher-resolution helps to differ targeted compounds from other ions, though the complexity of the data isoSCAN makes use of __enviPat__ package: "Higher-resolution helps to differ targeted compounds from other ions, though the complexity of the data isoSCAN makes use of enviPat package"
