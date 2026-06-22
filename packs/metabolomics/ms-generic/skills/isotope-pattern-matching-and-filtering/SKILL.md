---
name: isotope-pattern-matching-and-filtering
description: Use when you have high-resolution centroided mzML files from Orbitrap or similar instruments, a target compound list with known formulas and monoisotopic m/z values, and need to quantify isotopologue abundances (M+0, M+1, M+2, etc.) for stable isotope labeling experiments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3365
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - R
  - isoSCAN
  - mzR
  - enviPat
  - Proteowizard MSconvert
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.analchem.0c02998
  title: isoSCAN
evidence_spans:
- To Install from R console
- 'To Install from R console: ```` install.packages("devtools", dependencies=TRUE) library(devtools)'
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# isotope-pattern-matching-and-filtering

## Summary

Automatically extract and quantify isotopologue abundances from centroided high-resolution mass spectrometry data by matching observed m/z patterns against theoretical isotope patterns calculated for target compounds. This skill enables stable isotope labeling quantification in GC-CI-MS and Orbitrap workflows by filtering peaks based on mass error, signal-to-noise ratio, and retention time windows.

## When to use

Apply this skill when you have high-resolution centroided mzML files from Orbitrap or similar instruments, a target compound list with known formulas and monoisotopic m/z values, and need to quantify isotopologue abundances (M+0, M+1, M+2, etc.) for stable isotope labeling experiments. Use it specifically when you want to automatically extract peak area, maximum intensity, and mass error (ppm) for each isotopic form rather than manually inspecting spectra.

## When NOT to use

- Input files are in profile mode rather than centroided; use profile format for low-resolution data instead.
- Raw vendor format data has not been converted to mzML; convert via Proteowizard MSconvert first.
- Target compound formula is unknown or not derivatized (for high-resolution); autoQ requires exact chemical formula matching.
- Data is from low-resolution instruments where profile format is essential; high-resolution centroided workflow will fail on profile low-res data.

## Inputs

- formulaTable data frame with columns: CompoundName, mz, RT (seconds), Formula, NumAtoms
- Centroided high-resolution mzML files (Orbitrap or equivalent)
- enviPat isotopes object for theoretical isotope pattern calculation
- Target label atom (e.g., '13C') and labeling scheme specification

## Outputs

- Quantification table with columns: CompoundName, m/z, abundance, isotopologue designation (M+0, M+1, M+2), ppm mass error, area, maxo (maximum intensity) per sample
- Paired peak metrics (area and maxo) for each isotopic form per compound and condition

## How to apply

Load a formulaTable data frame containing CompoundName, mz (monoisotopic m/z), RT (retention time in seconds), Formula, and NumAtoms columns using read.csv. Ensure high-resolution mzML files have been centroided (e.g., via Proteowizard MSconvert with peakPicking=True). Call the autoQ function with the formulaTable, specifying parameters for the target label atom (e.g., labelatom='13C'), mass error tolerance (mzerror or maxppm in ppm), retention time window (RTwin), signal-to-noise ratio threshold (SNR), peak width bounds (minwidth, maxwidth), and minimum number of scans (minscans). The function leverages the enviPat package to compute theoretical isotope patterns and filters observed peaks by mass accuracy and signal quality. Capture the returned quantification table containing columns for CompoundName, m/z, abundance, isotopologue designation (M+0, M+1, M+2), ppm error, and paired area and maxo (maximum intensity) values per sample condition.

## Related tools

- **isoSCAN** (Executes autoQ function to automatically match observed isotope patterns against theoretical patterns and extract quantification metrics (abundance, ppm, area, maxo) for target isotopologues.) — https://github.com/jcapelladesto/isoSCAN
- **enviPat** (Computes theoretical isotope patterns and abundance ratios for target compound formulas to enable pattern matching against observed m/z features.)
- **mzR** (Reads mzML/mzXML format mass spectrometry files to provide raw spectral data for peak detection and quantification.)
- **Proteowizard MSconvert** (Converts vendor-format raw MS data into centroided mzML format with peakPicking enabled, required preprocessing step for high-resolution workflows.)
- **R** (Execution environment for loading data frames, calling autoQ, and manipulating quantification results.)

## Examples

```
library(isoSCAN); formulaTable <- read.csv('compounds.csv'); autoQ(formulaTable, path='./mzml_files/', labelatom='13C', mzerror=5, RTwin=60, SNR=3, minscans=5, minwidth=3, maxwidth=30)
```

## Evaluation signals

- Returned quantification table has one row per isotopologue per compound per sample, with non-null abundance, ppm, area, and maxo values.
- Mass error (ppm) values fall within the specified mzerror/maxppm tolerance for all reported peaks; outliers suggest parameter tuning or artifact peaks.
- Peak area and maxo (intensity) values are consistent in magnitude and rank order within a sample (e.g., M+0 typically largest for unlabeled or minimally labeled samples).
- Signal-to-noise ratio for quantified peaks meets or exceeds the SNR threshold; peaks below SNR should be absent or flagged.
- Retention time of matched peaks falls within ±RTwin seconds of the formulaTable RT value for each compound.
- Isotopologue designations (M+0, M+1, M+2, etc.) match expected theoretical m/z spacing from the enviPat pattern.

## Limitations

- High-resolution data requires exact Formula matching (including derivatization groups); mismatched formulas will fail to find isotope patterns.
- Peak detection depends critically on SNR, RTwin, minwidth, and maxwidth parameters; suboptimal parameter choice leads to missed or false-positive isotopologue calls.
- Centroiding preprocessing is mandatory for high-resolution; profile mode will produce incorrect results and should use alternative low-resolution pathway.
- Moving peaks, noisy spots, or saturated peaks may yield unreliable quantification; rawPlot and meanRawPlot quality control functions should be used to inspect results.
- No automatic changelog or versioning is provided; reproducibility requires explicit isoSCAN version pinning and parameter documentation.

## Evidence

- [other] The autoQ function returns quantification table with isotopologue metrics: "The autoQ function returns for high-resolution Orbitrap data a table with columns for CompoundName, m.z, abundance, Isotopologue designation (M+0, M+1, M+2), ppm mass error, and paired maxo and area"
- [intro] formulaTable must contain specific columns: "_formulaTable_ __must__ contain the following column names in no specific order: * __CompoundName__ * __mz__ * __RT__ * __Formula__ * __NumAtoms__"
- [intro] High-resolution data requires centroiding: "In the case of High-resolution, __please use centroiding__ (e.g. _peakPicking= True_ in MSconvert)"
- [intro] autoQ function parameters for peak filtering: "This parameters refer to peak width and number of scans recorded, together with signal-to-noise ratio and mass error."
- [intro] enviPat used for isotope pattern calculation: "Higher-resolution helps to differ targeted compounds from other ions, though the complexity of the data isoSCAN makes use of __enviPat__ package"
- [intro] Quality control functions for peak inspection: "`rawPlot` and `meanRawPlot` functions should be used for quality control purposes. They are useful to check for moving peaks, noisy spots or saturated peaks."
- [readme] Installation and library loading: "install_github("jcapelladesto/isoSCAN")
library(isoSCAN)"
- [intro] Package capability and scope: "The package is designed to automatically extract the abundances of isotopologues of a targeted list of compounds."
