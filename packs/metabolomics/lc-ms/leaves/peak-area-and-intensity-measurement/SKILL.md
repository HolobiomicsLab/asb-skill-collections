---
name: peak-area-and-intensity-measurement
description: Use when when you have vendor-format GC-CI-MS or LC-MS data from stable
  isotope labeling experiments, a target list of compounds with known monoisotopic
  m/z, retention time, and elemental formula, and you need per-isotopologue area and
  intensity values for quantification or downstream statistical.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - R
  - isoSCAN
  - mzR
  - enviPat
  - Proteowizard MSconvert
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# peak-area-and-intensity-measurement

## Summary

Automated extraction of per-compound isotopologue peak area and maximum intensity (maxo) values from low- or high-resolution MS data using the isoSCAN autoQ function. This skill quantifies metabolite abundances in stable isotope labeling experiments by detecting peaks within specified mass-error and retention-time windows.

## When to use

When you have vendor-format GC-CI-MS or LC-MS data from stable isotope labeling experiments, a target list of compounds with known monoisotopic m/z, retention time, and elemental formula, and you need per-isotopologue area and intensity values for quantification or downstream statistical comparison. Low-resolution data must be in profile format; high-resolution data should be centroided.

## When NOT to use

- Input is already in centroided format and you are processing low-resolution data — profile format is essential for accurate peak quantification in low-resolution.
- Raw vendor format has not been converted to mzML/mzXML — autoQ requires mzR-compatible formats.
- Your target compounds list lacks retention time or monoisotopic m/z values — formulaTable must contain both for peak detection within RTwin and mzerror windows.

## Inputs

- formulaTable data frame (columns: CompoundName, mz, RT, Formula, NumAtoms)
- mzML or mzXML files in profile format (low-resolution) or centroided (high-resolution)
- autoQ function parameters: minscans, SNR, mzerror/maxppm, RTwin, maxwidth, minwidth

## Outputs

- Per-compound isotopologue area values (when peak shape permits)
- Per-compound isotopologue maxo (maximum intensity) values
- Tabulated quantification results for each isotopologue

## How to apply

Load your target compounds into a formulaTable data frame with columns CompoundName, mz (monoisotopic ion), RT (retention time in seconds), Formula, and NumAtoms using read.csv or read.table. Convert raw vendor files to mzML or mzXML format using Proteowizard MSconvert, preserving profile format for low-resolution or applying peak-picking for high-resolution. Call the autoQ function on the mzML files, specifying peak-finding parameters: minscans (minimum scans per peak, typically 6), SNR (signal-to-noise threshold, e.g. 3), mzerror or maxppm (mass error tolerance, e.g. 0.1 Da or ppm), RTwin (retention time window in seconds, e.g. 5), and maxwidth and minwidth (peak width bounds in scans). The function returns both area and maxo intensity values for each isotopologue; area values are reliable when peak shape is Gaussian, and maxo is consistently returned across all peaks.

## Related tools

- **isoSCAN** (R package that implements autoQ function for automated isotopologue peak area and intensity extraction from MS files) — https://github.com/jcapelladesto/isoSCAN
- **mzR** (R package used by isoSCAN to read mzML/mzXML MS files)
- **Proteowizard MSconvert** (Converts vendor-format raw MS data to mzML/mzXML, with format preservation (profile) or peak-picking (centroid) options)
- **enviPat** (R package for isotope pattern simulation; used by isoSCAN to differentiate targeted compounds from background ions in complex data)

## Examples

```
library(isoSCAN); formulaTable <- read.csv('targets.csv'); autoQ(files='sample.mzML', formulaTable=formulaTable, minscans=6, SNR=3, mzerror=0.1, RTwin=5, maxwidth=4, minwidth=1)
```

## Evaluation signals

- Both area and maxo values are returned for all isotopologues in the target list; if area is NA, check peak shape quality with rawPlot or meanRawPlot.
- Returned m/z values fall within mzerror (or maxppm) tolerance of formulaTable mz entries, and retention times fall within RTwin of formulaTable RT.
- Peak widths (in scans) in the output fall between minwidth and maxwidth parameters; peaks outside this range should be flagged.
- Standard deviation error bars in metBarPlot output are proportional to within-replicate variance; high variance may indicate noisy peaks or saturation.
- Raw and mean intensity plots show smooth, unimodal peak shapes without drift, saturation, or multiple modes within the RTwin — deviations suggest parameter tuning is needed.

## Limitations

- Low-resolution data requires profile format input; centroided low-resolution data will produce inaccurate or missing area values.
- High-resolution data benefits from higher mass resolution to distinguish targeted compounds from other ions, but isoSCAN can process both — resolution affects confidence in peak assignment.
- Area values are reliable only when peak shape permits (typically Gaussian); irregular or saturated peaks return NA for area but maxo is still computed.
- formulaTable Formula column must match the derivatized formula for high-resolution data; incorrect formulas will cause isotope pattern mismatch.
- Performance and peak detection accuracy depend critically on parameter tuning (minscans, SNR, mzerror, RTwin); no single set of parameters is universal across different instruments, sample types, or resolution modes.

## Evidence

- [other] autoQ processing of low-resolution Quadrupole data with parameters minscans=6, SNR=3, mzerror=0.1, RTwin=5, maxwidth=4, minwidth=1 yields both area and maxo values for isotopologues: "autoQ processing of low-resolution Quadrupole data with parameters minscans=6, SNR=3, mzerror=0.1, RTwin=5, maxwidth=4, minwidth=1 yields both area and maxo values for isotopologues of compounds like"
- [intro] formulaTable must contain columns CompoundName, mz, RT, Formula, NumAtoms: "Before starting with file processing, we need to load the _targeted compounds_ as a _formulaTable_ data frame. This can be done either with `read.table` or `read.csv` functions."
- [intro] For low-resolution, profile format is essential; for high-resolution, centroiding should be used: "In the case of Low-resolution. Transform the data mantaining __profile format__. This is essential for peak quantification."
- [intro] isoSCAN uses mzR to read MS files; raw data must be transformed to mz(X)ML format: "The first step is file format transformation, `isoSCAN` uses `mzR` package in order to read MS files. Therefore, you will have to transform the raw data from vendor format into __mz(X)ML__ format"
- [intro] autoQ function processes files and extracts isotopologue abundances: "Now we can call `autoQ` function that will process the files and look for the isotopologues for each compound found in the `formulaTable`."
- [intro] autoQ parameters refer to peak width, number of scans, SNR, and mass error: "This parameters refer to peak width and number of scans recorded, together with signal-to-noise ratio and mass error."
- [intro] rawPlot and meanRawPlot functions used for quality control of peak shape: "`rawPlot` and `meanRawPlot` functions should be used for quality control purposes. They are useful to check for moving peaks, noisy spots or saturated peaks."
