---
name: retention-time-based-ion-association
description: Use when when processing Data Dependent Acquisition (DDA) raw mass spectrometry data (mzML or mzXML format) and you need to deconvolute fragmentation spectra by matching precursor ions to their corresponding fragment ions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - IDSL.CSA
  - R
  - IDSL.IPA
  techniques:
  - CE-MS
derived_from:
- doi: 10.1021/acs.analchem.3c00376
  title: IDSL.CSA
evidence_spans:
- The **Composite Spectra Analysis (IDSL.CSA)** R package for the analysis of mass spectrometry data
- The **Composite Spectra Analysis (IDSL.CSA)** R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idsl_csa_cq
    doi: 10.1021/acs.analchem.3c00376
    title: IDSL.CSA
  dedup_kept_from: coll_idsl_csa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c00376
  all_source_dois:
  - 10.1021/acs.analchem.3c00376
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-based-ion-association

## Summary

Associate precursor ions with their fragment ions by leveraging retention time (RT) and mass-to-charge ratio (m/z) alignment during DDA mass spectrometry data deconvolution. This skill groups fragmentation spectra based on temporal and mass co-occurrence to reconstruct accurate composite MS/MS spectra for chemical annotation.

## When to use

When processing Data Dependent Acquisition (DDA) raw mass spectrometry data (mzML or mzXML format) and you need to deconvolute fragmentation spectra by matching precursor ions to their corresponding fragment ions. Specifically apply this skill when your input includes both MS1 (precursor) and MS/MS (fragment) signals and you require aggregated, precursor-ion-centric composite spectra for downstream chemical structure annotation.

## When NOT to use

- Input data is already a feature matrix or aligned peak table (no raw MS/MS spectra available)
- Data were acquired using Data-Independent Acquisition (DIA) or MS1-only methods (use CSA or DIA workflows instead)
- Retention time information is missing or unreliable (RT-based grouping will fail)

## Inputs

- Raw DDA mass spectrometry data file (mzML or mzXML format)
- Retention time and m/z values for precursor ions (MS1 level)
- Retention time and m/z values for fragment ions (MS/MS level)
- IDSL.CSA parameter spreadsheet with DDA-specific settings

## Outputs

- Deconvoluted fragmentation spectra table with precursor m/z, retention time, and aggregated fragment ion intensities
- Composite spectrum objects indexed by precursor ion identity
- Grouped ion assignments (precursor-to-fragment mappings)
- MSP files or annotated spectra suitable for chemical structure database matching

## How to apply

Load DDA raw mass spectrometry data (mzML or mzXML) into IDSL.CSA. Apply the DDA-specific deconvolution algorithm, which groups precursor ions with fragment ions by comparing retention time proximity and m/z relationships between the two scan levels. The algorithm aggregates all fragment ion intensities associated with each precursor ion to generate deconvoluted composite spectra. Output the results as a structured table or spectrum object containing precursor m/z, retention time, and grouped fragment ion intensities. Validate output by confirming that each precursor ion is matched to fragment ions occurring within the expected retention time window and that the m/z relationships satisfy MS/MS fragmentation logic (fragment m/z ≤ precursor m/z).

## Related tools

- **IDSL.CSA** (Implements DDA deconvolution algorithm that groups precursor and fragment ions by RT and m/z; generates deconvoluted composite spectra and aggregated spectrum tables) — https://github.com/idslme/IDSL.CSA
- **R** (Host environment for IDSL.CSA package execution and parameter configuration)
- **IDSL.IPA** (Prerequisite workflow: generates chromatographic information (m/z-RT) and aligned peaklists required as input to IDSL.CSA DDA workflow) — https://github.com/idslme/IDSL.IPA

## Examples

```
library(IDSL.CSA)
IDSL.CSA_workflow("Address of the CSA parameter spreadsheet")
```

## Evaluation signals

- Each precursor ion in output is matched to one or more fragment ions with m/z values ≤ precursor m/z
- Fragment ions grouped to a precursor all share retention time values within an acceptable window (typically ±0.5–2 min, depending on chromatographic resolution)
- Deconvoluted spectra contain non-zero fragment ion intensities aggregated from all MS/MS scans matching the precursor
- Output spectra table has consistent schema: precursor m/z, RT, fragment m/z array, fragment intensity array, and scan count
- Composite spectra pass validation against reference MS/MS spectral libraries (e.g., cosine similarity match > 0.7 for known compounds)

## Limitations

- Retention time-based grouping assumes consistent chromatographic behavior within a sample; poor peak resolution or co-elution of isomers can lead to incorrect precursor-fragment associations
- Algorithm performance depends on accurate m/z calibration and retention time tracking; instrumental drift or miscalibration will degrade ion matching
- DDA workflow is not applicable to Data-Independent Acquisition (DIA) or MS1-only CSA data; separate workflows are required for those methods
- Large sample cohorts (n > 500) require parallel processing configuration to avoid long runtimes; computational resources scale with data volume and parameter complexity

## Evidence

- [other] Apply the DDA-specific deconvolution algorithm to group precursor ions with their corresponding fragment ions based on retention time and m/z relationships.: "Apply the DDA-specific deconvolution algorithm to group precursor ions with their corresponding fragment ions based on retention time and m/z relationships."
- [other] IDSL.CSA is designed to deconvolute fragmentation spectra from Data Dependent Acquisition (DDA) among various analytical methods including MS1-only CSA and DIA methods.: "IDSL.CSA is designed to deconvolute fragmentation spectra from Data Dependent Acquisition (DDA) among various analytical methods"
- [other] Load the DDA raw mass spectrometry data file (mzML or mzXML format) into the IDSL.CSA R package.: "Load the DDA raw mass spectrometry data file (mzML or mzXML format) into the IDSL.CSA R package."
- [other] Generate deconvoluted fragmentation spectra by aggregating fragment ions associated with each precursor ion.: "Generate deconvoluted fragmentation spectra by aggregating fragment ions associated with each precursor ion."
- [readme] Peak detection and chromatogram deconvolution for various fragmentation data analyses including Composite Spectra Analysis (CSA), Data Dependent Acquisition (DDA), and Data-Independent Acquisition (DIA): "Peak detection and chromatogram deconvolution for various fragmentation data analyses including Composite Spectra Analysis (CSA), Data Dependent Acquisition (DDA), and Data-Independent Acquisition"
- [readme] Prior to processing your mass spectrometry data (mzXML, mzML, netCDF) using the IDSL.CSA workflow, mass spectrometry data should be processed using the IDSL.IPA workflow to acquire chromatographic information of the peaks (m/z-RT).: "mass spectrometry data should be processed using the IDSL.IPA workflow to acquire chromatographic information of the peaks (m/z-RT)"
