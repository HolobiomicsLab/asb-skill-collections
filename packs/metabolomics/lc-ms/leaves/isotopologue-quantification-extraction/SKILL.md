---
name: isotopologue-quantification-extraction
description: Use when you have GC-CI-MS or LC-MS data in mzML format targeting a defined
  set of compounds with known monoisotopic mass, retention time, and chemical formula,
  and you need per-isotopologue (M+0, M+1, M+2, etc.) quantification metrics (area,
  maxo intensity, abundance).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
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

# isotopologue-quantification-extraction

## Summary

Automated extraction of isotopologue abundances, areas, and intensities from low- and high-resolution mass spectrometry data using the isoSCAN/autoQ pipeline. This skill quantifies labeled and unlabeled forms of target compounds in stable isotope labeling experiments by matching peak signatures against calculated isotope patterns.

## When to use

Apply this skill when you have GC-CI-MS or LC-MS data in mzML format targeting a defined set of compounds with known monoisotopic mass, retention time, and chemical formula, and you need per-isotopologue (M+0, M+1, M+2, etc.) quantification metrics (area, maxo intensity, abundance). Use it when your research question requires distinguishing between isotopic forms of the same compound across multiple samples or conditions.

## When NOT to use

- Input mzML files are in centroided format for low-resolution data (profile format is essential for accurate peak quantification)
- Raw data has not been converted to mzML format or formulaTable is missing required columns (CompoundName, mz, RT, Formula, NumAtoms)
- Compounds have overlapping retention times or m/z values that exceed the specified mass error tolerance (mzerror/maxppm), preventing reliable isotopologue discrimination

## Inputs

- formulaTable data frame (columns: CompoundName, mz, RT, Formula, NumAtoms)
- mzML files in profile format (low-resolution) or centroided format (high-resolution)
- enviPat isotopes object (for isotope pattern calculation)
- autoQ function parameters (minscans, SNR, mzerror/maxppm, RTwin, maxwidth, minwidth, labelatom)

## Outputs

- Quantification table with columns: CompoundName, m.z, isotopologue designation (M+0, M+1, M+2), abundance, ppm mass error, area, maxo (maximum intensity) per sample
- Quality control plots (rawPlot, meanRawPlot) flagging peak shape anomalies

## How to apply

First, prepare a formulaTable data frame with columns CompoundName, mz (monoisotopic ion), RT (retention time in seconds), Formula (derivatized formula for high-resolution), and NumAtoms, loaded via read.csv. Convert raw MS data to mzML format using Proteowizard MSconvert, preserving profile format for low-resolution data or applying centroiding for high-resolution (Orbitrap) data. Call the autoQ function with the formulaTable and mzML files, specifying parameters: minscans (minimum scans per peak, typically 6), SNR (signal-to-noise threshold, typically 3), mzerror or maxppm (mass error tolerance, e.g., 0.1 Da or 5 ppm), RTwin (retention time window in seconds, typically 5), and maxwidth/minwidth (peak width bounds in scans). For labeled experiments, specify labelatom='13C'. Extract the resulting table containing per-compound isotopologue designations (M+0, M+1, M+2) with paired area and maxo values, ppm mass error, and abundance metrics. Validate results using rawPlot and meanRawPlot for quality control to identify moving peaks, noise, or saturation artifacts.

## Related tools

- **isoSCAN** (Primary R package providing the autoQ function for automated isotopologue extraction and quantification from mzML files) — https://github.com/jcapelladesto/isoSCAN
- **mzR** (R package used by isoSCAN to parse and read mzML/mzXML mass spectrometry files)
- **Proteowizard MSconvert** (Converts vendor-format raw MS data into mzML format with user-selectable profile or centroided output)
- **enviPat** (R package that calculates isotope patterns for high-resolution mass spectrometry to enable isotopologue identification)

## Examples

```
library(isoSCAN); formulaTable <- read.csv('targets.csv'); autoQ(formulaTable, mzMLfiles=c('sample1.mzML','sample2.mzML'), minscans=6, SNR=3, mzerror=0.1, RTwin=5, maxwidth=4, minwidth=1, labelatom='13C')
```

## Evaluation signals

- autoQ output table contains all target compounds from formulaTable with isotopologue designations (M+0, M+1, M+2) and non-null area and maxo values (when peak shape permits)
- Returned ppm mass error values are within specified mzerror/maxppm tolerance for each isotopologue peak
- Ratio of M+1 to M+0 abundance (or M+2/M+0 for doubly labeled compounds) matches theoretical labeling fraction within ±5% when validated against synthetic mixtures or known standards
- rawPlot and meanRawPlot quality control plots show stable, smooth peak profiles without drift, noise spikes, or saturation artifacts across replicate samples
- Area and maxo values increase monotonically with compound concentration in a dose-response experiment (R² > 0.98 for standard curves)

## Limitations

- Profile format is essential for low-resolution data; centroided files will yield inaccurate or missing quantification
- High-resolution data requires derivatized formula in formulaTable; mismatch with actual derivatization will cause isotopologue pattern misalignment and peak misidentification
- Peak quantification fails or returns only maxo (not area) when peak shape is severely distorted, overlapped, or saturated; manual review via rawPlot is required
- Retention time window (RTwin) and mass error tolerance (mzerror/maxppm) must be tuned per instrument and chromatography method; inappropriate settings cause false positives or missed isotopologues
- No changelog or versioning information provided; compatibility with R version, mzR, and enviPat version updates is undocumented

## Evidence

- [intro] isoSCAN primary design goal: "The package is designed to automatically extract the abundances of isotopologues of a targeted list of compounds."
- [intro] Low-resolution format requirement: "In the case of Low-resolution. Transform the data mantaining __profile format__. This is essential for peak quantification."
- [intro] High-resolution format requirement: "In the case of High-resolution, __please use centroiding__ (e.g. _peakPicking= True_ in MSconvert)"
- [intro] formulaTable required columns: "_formulaTable_ __must__ contain the following column names in no specific order: * __CompoundName__ * __mz__ * __RT__ * __Formula__ * __NumAtoms__"
- [intro] autoQ parameter specification: "This parameters refer to peak width and number of scans recorded, together with signal-to-noise ratio and mass error."
- [intro] Workflow: load compounds and process files: "Before starting with file processing, we need to load the _targeted compounds_ as a _formulaTable_ data frame. This can be done either with `read.table` or `read.csv` functions."
- [intro] Workflow: call autoQ function: "Now we can call `autoQ` function that will process the files and look for the isotopologues for each compound found in the `formulaTable`."
- [intro] Quality control functions: "`rawPlot` and `meanRawPlot` functions should be used for quality control purposes. They are useful to check for moving peaks, noisy spots or saturated peaks."
- [other] Low-resolution Quadrupole autoQ output: "autoQ processing of low-resolution Quadrupole data with parameters minscans=6, SNR=3, mzerror=0.1, RTwin=5, maxwidth=4, minwidth=1 yields both area and maxo values for isotopologues"
- [other] High-resolution Orbitrap autoQ output: "The autoQ function returns for high-resolution Orbitrap data a table with columns for CompoundName, m.z, abundance, Isotopologue designation (M+0, M+1, M+2), ppm mass error, and paired maxo and area"
