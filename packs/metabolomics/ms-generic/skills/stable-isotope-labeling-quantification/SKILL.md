---
name: stable-isotope-labeling-quantification
description: Use when you have centroided high-resolution Orbitrap mzML files from stable isotope labeling experiments and need to measure isotopologue abundances (M+0, M+1, M+2, etc.) for a defined list of target compounds with 13C or other isotopic labels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
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

# stable-isotope-labeling-quantification

## Summary

Automated extraction and quantification of isotopologue abundances from high-resolution mass spectrometry data (Orbitrap mzML files) using the autoQ function in isoSCAN. This skill enables measurement of 13C-labeled compound patterns with ppm mass error, peak area, and intensity metrics.

## When to use

Use this skill when you have centroided high-resolution Orbitrap mzML files from stable isotope labeling experiments and need to measure isotopologue abundances (M+0, M+1, M+2, etc.) for a defined list of target compounds with 13C or other isotopic labels. Trigger conditions: (1) you have a formulaTable of target compounds with monoisotopic m/z, retention time, and molecular formula; (2) raw data has been converted to mzML format and centroided; (3) you need paired quantification outputs (abundance, ppm error, peak area, maxo intensity) for each isotopic form per sample.

## When NOT to use

- Input is low-resolution MS data in profile format — use profile-format isoSCAN instead; autoQ requires centroided high-resolution input.
- Target compounds have not been converted to mzML format — autoQ depends on mzR, which requires mzML or mzXML; vendor-format files must be converted first.
- You need only peak detection without isotope quantification — use a general peak-picking tool instead; autoQ is optimized for multi-isotopologue extraction.

## Inputs

- formulaTable data frame (columns: CompoundName, mz, RT, Formula, NumAtoms)
- High-resolution centroided Orbitrap mzML files
- enviPat isotopes object for isotope pattern definition

## Outputs

- Quantification table with columns: CompoundName, m/z, abundance, Isotopologue designation (M+0, M+1, M+2), ppm mass error, maxo (maximum intensity), area (integrated peak area)

## How to apply

Load a formulaTable data frame containing CompoundName, mz, RT, Formula, and NumAtoms columns using read.csv. Transform vendor-format raw data into centroided mzML format using Proteowizard MSconvert (essential for high-resolution data). Load the enviPat isotopes object for isotope pattern calculation. Call the autoQ function with parameters: labelatom='13C', mzerror or maxppm tolerance (typically 5–10 ppm for Orbitrap), RTwin (retention time window in seconds), minscans, SNR (signal-to-noise ratio threshold), and minwidth/maxwidth (peak width constraints). The function returns a table with columns for CompoundName, m/z, abundance, Isotopologue designation (M+0, M+1, M+2), ppm mass error, and paired maxo and area values for each isotopic form. Rationale: isoSCAN's autoQ is specifically designed to handle the complexity of high-resolution isotope pattern deconvolution using enviPat and enforces quality thresholds (SNR, peak width, scan count) to filter noise and false positives.

## Related tools

- **isoSCAN** (R package that implements autoQ function for automated isotopologue extraction and quantification) — github.com/jcapelladesto/isoSCAN
- **mzR** (Reads centroided mzML/mzXML files into memory for isoSCAN processing)
- **enviPat** (Generates theoretical isotope patterns for targeted compound formulas to enable isotopologue deconvolution)
- **Proteowizard MSconvert** (Converts vendor-format raw MS data to centroided mzML format required by autoQ)

## Examples

```
library(isoSCAN); formulaTable <- read.csv('targets.csv'); autoQ(formulaTable, mzmldir='./centroided_mzML/', labelatom='13C', maxppm=5, RTwin=30, SNR=3, minscans=10, minwidth=0.1, maxwidth=0.5)
```

## Evaluation signals

- Quantification table contains all expected compounds from formulaTable without missing rows (100% matching rate).
- ppm mass error values fall within specified tolerance (e.g., all ≤ 5 ppm for Orbitrap high-resolution).
- Isotopologue designations (M+0, M+1, M+2) are present and correctly ordered by increasing mass; abundance values sum to ~100% or documented baseline.
- Peak area and maxo (maximum intensity) values are positive, non-zero, and consistent with SNR threshold applied (SNR ≥ user-specified minimum).
- Quality control plots (rawPlot, meanRawPlot) show no saturated peaks, excessive noise, or moving peaks within retention time window.

## Limitations

- autoQ requires formulaTable Formula column to match the derivatized form of the compound; incorrect or incomplete formulas will fail isotope pattern matching.
- High-resolution data must be centroided before input; profile-format Orbitrap files will produce incorrect quantification.
- SNR and peak-width thresholds (minscans, minwidth, maxwidth) are user-configurable but lack default guidance; suboptimal choices may miss low-abundance isotopologues or include noise.
- enviPat isotope patterns are calculated assuming natural or specified labeling; non-uniform labeling or enrichment isotopes not in enviPat's database may not be handled correctly.

## Evidence

- [intro] The package is designed to automatically extract the abundances of isotopologues of a targeted list of compounds.: "The package is designed to automatically extract the abundances of isotopologues of a targeted list of compounds."
- [intro] For high-resolution data, centroiding should be used.: "In the case of High-resolution, __please use centroiding__ (e.g. _peakPicking= True_ in MSconvert)"
- [intro] formulaTable must contain specific columns in no particular order.: "_formulaTable_ __must__ contain the following column names in no specific order: * __CompoundName__ * __mz__ * __RT__ * __Formula__ * __NumAtoms__"
- [intro] autoQ function parameters and their meaning.: "This parameters refer to peak width and number of scans recorded, together with signal-to-noise ratio and mass error."
- [other] Output structure of autoQ for high-resolution Orbitrap data.: "The autoQ function returns for high-resolution Orbitrap data a table with columns for CompoundName, m.z, abundance, Isotopologue designation (M+0, M+1, M+2), ppm mass error, and paired maxo and area"
