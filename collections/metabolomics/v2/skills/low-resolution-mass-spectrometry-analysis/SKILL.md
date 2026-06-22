---
name: low-resolution-mass-spectrometry-analysis
description: Use when you have low-resolution MS data (e.g., from quadrupole instruments) in vendor format, a list of target compounds with known monoisotopic m/z and retention times, and need to extract per-isotopologue area and intensity values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - R
  - isoSCAN
  - mzR
  - enviPat
  - Proteowizard MSconvert
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

# low-resolution-mass-spectrometry-analysis

## Summary

Automated extraction of isotopologue abundances from low-resolution GC-CI-MS data by processing profile-format mzML files with peak-finding parameters tuned for lower mass accuracy and wider peak widths. This skill enables quantification of stable isotope labeling experiments where centroiding is inappropriate and profile mode preserves essential peak shape information.

## When to use

You have low-resolution MS data (e.g., from quadrupole instruments) in vendor format, a list of target compounds with known monoisotopic m/z and retention times, and need to extract per-isotopologue area and intensity values. Profile format must be preserved during format conversion (not centroided). Use when peak shape variation or low mass resolution makes high-resolution peak-picking unsuitable.

## When NOT to use

- Input files are already centroided or in centroid format — profile mode is essential for low-resolution peak quantification
- Target compound list is missing retention time values or accurate monoisotopic m/z — formulaTable must contain all required columns
- Data is from high-resolution instruments (e.g., TOF or Orbitrap) — use centroiding and tighter mass error parameters instead

## Inputs

- vendor-format raw mass spectrometry files (from quadrupole or equivalent low-resolution instrument)
- formulaTable data frame with columns: CompoundName, mz, RT, Formula, NumAtoms
- profile-format mzML files (converted from vendor format, not centroided)

## Outputs

- per-compound isotopologue area values (when peak shape permits quantification)
- per-compound isotopologue maxo (maximum intensity) values
- quality control plots (rawPlot, meanRawPlot, metBarPlot output)

## How to apply

First, convert raw vendor files to mzML format using Proteowizard MSconvert while maintaining profile format (do not apply peak picking). Load target compounds into a formulaTable data frame with columns CompoundName, mz, RT (seconds), Formula, and NumAtoms using read.csv or read.table. Call the autoQ function specifying low-resolution-appropriate parameters: minscans (typically 6), SNR threshold (e.g., 3), mzerror or maxppm (e.g., 0.1 Da for low-resolution quadrupole), RTwin (retention time window in seconds, e.g., 5), and peak width bounds (maxwidth and minwidth in scans, e.g., maxwidth=4, minwidth=1). The function will return both area and maxo (maximum intensity) values for each isotopologue; area may be absent if peak shape prevents reliable quantification. Verify output by plotting with metBarPlot and inspecting peak quality using rawPlot and meanRawPlot to detect moving peaks, noise, or saturation.

## Related tools

- **isoSCAN** (R package that implements autoQ and associated peak quantification, plotting, and QC functions for isotopologue extraction from GC-CI-MS data) — https://github.com/jcapelladesto/isoSCAN
- **mzR** (R package used by isoSCAN to parse and read mzML/mzXML MS data files)
- **Proteowizard MSconvert** (Converts vendor-format raw MS files to mzML format while preserving profile mode for low-resolution data)
- **enviPat** (R package used by isoSCAN to compute isotope patterns and distinguish targeted compounds from background ions)

## Examples

```
library(isoSCAN)
formTable <- read.csv('quadrupole_targets.csv')
autoQ(files='sample.mzML', formulaTable=formTable, minscans=6, SNR=3, mzerror=0.1, RTwin=5, maxwidth=4, minwidth=1)
```

## Evaluation signals

- All target compounds from formulaTable are represented in autoQ output with per-isotopologue maxo values returned consistently
- Area values are present for isotopologues where peak shape permits (check via rawPlot inspection for non-saturated, non-noisy peaks)
- Mean intensity values plotted by metBarPlot show expected relative abundances across isotopologues consistent with stable isotope labeling design
- rawPlot and meanRawPlot QC inspection reveals no systematic moving peaks, saturation, or excessive noise that would invalidate quantification
- Observed mass error (difference between detected m/z and formulaTable m/z) stays within the specified mzerror tolerance (e.g., ±0.1 Da)

## Limitations

- Low-resolution data may fail to resolve isotopologues with overlapping m/z patterns; higher resolution is preferred when available
- Area quantification is not returned when peak shape degrades (e.g., saturated or severely noisy peaks); maxo intensity is more robust but less precise
- formulaTable Formula column must exactly match the derivatized compound formula used in the experiment; mismatches prevent correct isotope pattern matching
- Peak detection depends critically on tuning minscans, SNR, RTwin, and peak width parameters; suboptimal values may miss weak isotopologues or incorrectly assign background noise
- Retention time must be known in advance for each compound; retention time drift or co-elution with other compounds will compromise isotopologue assignment

## Evidence

- [intro] For low-resolution data, profile format is essential: "In the case of Low-resolution. Transform the data mantaining __profile format__. This is essential for peak quantification."
- [intro] autoQ parameters for peak detection on low-resolution data: "This parameters refer to peak width and number of scans recorded, together with signal-to-noise ratio and mass error."
- [intro] formulaTable structure requirements: "_formulaTable_ __must__ contain the following column names in no specific order: * __CompoundName__ * __mz__ * __RT__ * __Formula__ * __NumAtoms__"
- [other] autoQ output for low-resolution quadrupole data: "autoQ processing of low-resolution Quadrupole data with parameters minscans=6, SNR=3, mzerror=0.1, RTwin=5, maxwidth=4, minwidth=1 yields both area and maxo values for isotopologues of compounds like"
- [intro] QC workflow for validating peak quality: "`rawPlot` and `meanRawPlot` functions should be used for quality control purposes. They are useful to check for moving peaks, noisy spots or saturated peaks."
- [intro] File format conversion workflow: "The first step is file format transformation, `isoSCAN` uses `mzR` package in order to read MS files. Therefore, you will have to transform the raw data from vendor format into __mz(X)ML__ format"
