---
name: gc-ci-ms-data-processing
description: Use when you have vendor-format GC-CI-MS raw data from a stable isotope labeling experiment, a list of targeted compounds with known monoisotopic m/z, retention time, and molecular formula, and you need to extract per-isotopologue area and intensity values across multiple samples with consistent.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - R
  - isoSCAN
  - mzR
  - enviPat
  - Proteowizard MSconvert
  - devtools
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

# gc-ci-ms-data-processing

## Summary

Automated extraction of isotopologue abundances from GC-CI-MS data using the isoSCAN R package, applicable to both low- and high-resolution mass spectrometry datasets for stable isotope labeling experiments. The skill chains file format conversion, targeted compound loading, peak detection and quantification, and quality control visualization.

## When to use

You have vendor-format GC-CI-MS raw data from a stable isotope labeling experiment, a list of targeted compounds with known monoisotopic m/z, retention time, and molecular formula, and you need to extract per-isotopologue area and intensity values across multiple samples with consistent, reproducible peak-finding parameters.

## When NOT to use

- Input MS data are already in centroided format and you are processing low-resolution data (profile format is required for accurate low-resolution peak quantification).
- Your targeted compounds table is missing required columns (CompoundName, mz, RT, Formula, NumAtoms) or contains inconsistent retention time units (isoSCAN expects seconds).
- You do not have vendor raw data or mzML/mzXML files; isoSCAN requires MS data in these formats and cannot process ASCII peak lists or pre-extracted features.

## Inputs

- Vendor-format GC-CI-MS raw data files
- mzML or mzXML profile-format mass spectrometry files (low-resolution) or centroided mzML/mzXML (high-resolution)
- formulaTable data frame with columns: CompoundName, mz (monoisotopic m/z), RT (retention time in seconds), Formula, NumAtoms

## Outputs

- Per-compound isotopologue area values (when peak shape permits)
- Per-compound isotopologue maxo (maximum intensity) values
- Barplots with standard deviation error bars (via metBarPlot)
- Quality-control visualizations of raw and mean peak shapes (via rawPlot and meanRawPlot)

## How to apply

First, convert vendor-format raw files to mzML or mzXML using Proteowizard MSconvert, preserving profile format for low-resolution data or applying centroiding for high-resolution data. Load your targeted compounds as a formulaTable data frame (columns: CompoundName, mz, RT in seconds, Formula, NumAtoms) using read.csv or read.table. Call the autoQ function on the mzML files, specifying peak-finding parameters: minscans (minimum scans per peak), SNR (signal-to-noise threshold, e.g., 3), mzerror or maxppm (mass error tolerance, e.g., 0.1 Da), RTwin (retention time window in seconds, e.g., 5), and maxwidth/minwidth (peak width bounds in scans). Extract tabulated area and maxo (maximum intensity) values from the autoQ output, then apply metBarPlot for visualization and rawPlot/meanRawPlot for quality control to identify moving peaks, noise, or saturation.

## Related tools

- **isoSCAN** (R package that executes automated peak detection, isotopologue quantification, and abundance extraction from MS files via the autoQ function) — https://github.com/jcapelladesto/isoSCAN
- **mzR** (Underlying R package used by isoSCAN to read and parse mzML/mzXML mass spectrometry files)
- **Proteowizard MSconvert** (Converts vendor-format raw MS data to mzML/mzXML, with control over profile vs. centroided output format)
- **enviPat** (R package used by isoSCAN to compute isotope patterns for high-resolution data differentiation of targeted compounds from background ions)
- **devtools** (R package used to install isoSCAN from GitHub)

## Examples

```
library(isoSCAN); formulaTable <- read.csv('targets.csv'); results <- autoQ(formulaTable, mzMLfiles=list.files(pattern='.mzML'), minscans=6, SNR=3, mzerror=0.1, RTwin=5, maxwidth=4, minwidth=1); metBarPlot(results)
```

## Evaluation signals

- autoQ returns both area and maxo values for all isotopologues of targeted compounds listed in the formulaTable, or documents reason (e.g., 'peak shape does not permit area extraction') when area is absent.
- Quantified m/z values from autoQ match input formulaTable m/z values within the specified mzerror or maxppm tolerance (e.g., ±0.1 Da for low-resolution).
- Detected peaks satisfy all input filtering thresholds: minscans and maxwidth/minwidth bounds are respected, SNR is ≥ specified threshold, and retention time windows (RTwin) are honored.
- rawPlot and meanRawPlot quality-control visualizations confirm absence of moving peaks, extreme noise, or saturation artifacts that would invalidate quantification.
- metBarPlot output shows appropriate error bars (standard deviation) across replicate samples, consistent with expectation of biological/technical replication.

## Limitations

- For low-resolution data, profile format is essential; centroided low-resolution data will yield unreliable or missing area values.
- For high-resolution data, the formulaTable Formula column must match the derivatized compound formula, not the underivatized form, to enable accurate isotope-pattern matching.
- Peak width parameters (minwidth, maxwidth) and SNR thresholds are not data-adaptive; optimization may be required for different instrument configurations or sample types.
- isoSCAN is designed for GC-CI-MS; applicability to other ionization or separation modes (e.g., LC-ESI-MS) is not documented.
- No changelog or versioning documentation is available to track method or parameter stability across releases.

## Evidence

- [intro] formulaTable column requirements: "formulaTable __must__ contain the following column names in no specific order: * __CompoundName__ * __mz__ * __RT__ * __Formula__ * __NumAtoms__"
- [intro] profile format required for low-resolution: "In the case of Low-resolution. Transform the data mantaining __profile format__. This is essential for peak quantification."
- [intro] centroiding required for high-resolution: "In the case of High-resolution, __please use centroiding__ (e.g. _peakPicking= True_ in MSconvert)"
- [intro] autoQ function processes files for isotopologue abundances: "Now we can call `autoQ` function that will process the files and look for the isotopologues for each compound found in the `formulaTable`."
- [intro] autoQ parameters definition: "This parameters refer to peak width and number of scans recorded, together with signal-to-noise ratio and mass error."
- [intro] Quality control functions for peak validation: "`rawPlot` and `meanRawPlot` functions should be used for quality control purposes. They are useful to check for moving peaks, noisy spots or saturated peaks."
- [intro] mzR used for MS file reading: "isoSCAN uses `mzR` package in order to read MS files"
- [intro] enviPat for high-resolution differentiation: "Higher-resolution helps to differ targeted compounds from other ions, though the complexity of the data isoSCAN makes use of __enviPat__ package"
- [readme] Installation instructions: "install_github("jcapelladesto/isoSCAN")
library(isoSCAN)"
- [intro] Isotopologue abundance extraction capability: "The package is designed to automatically extract the abundances of isotopologues of a targeted list of compounds."
