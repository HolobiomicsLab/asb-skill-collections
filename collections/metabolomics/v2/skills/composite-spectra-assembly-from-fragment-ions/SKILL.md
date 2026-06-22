---
name: composite-spectra-assembly-from-fragment-ions
description: Use when you have DDA raw mass spectrometry data (mzML, mzXML, or netCDF format) and need to reconstruct composite fragmentation spectra by associating fragment ions with their parent precursor ions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - IDSL.CSA
  - R
  - IDSL.IPA
  - IDSL.FSA
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
---

# composite-spectra-assembly-from-fragment-ions

## Summary

Deconvolute fragmentation spectra from Data Dependent Acquisition (DDA) mass spectrometry data by grouping precursor ions with their corresponding fragment ions based on retention time and m/z relationships. This skill aggregates fragment ions into composite spectra suitable for metabolite annotation and chemical structure elucidation.

## When to use

Apply this skill when you have DDA raw mass spectrometry data (mzML, mzXML, or netCDF format) and need to reconstruct composite fragmentation spectra by associating fragment ions with their parent precursor ions. Use it specifically when your analytical goal requires improved chemical structure annotation in untargeted metabolomics or exposomics workflows.

## When NOT to use

- Input data is already a feature table or processed peak list without raw mass spectrometry data — use direct annotation workflows instead.
- Analytical method is Data-Independent Acquisition (DIA) or MS1-only CSA — use the appropriate DIA or CSA deconvolution module.
- Sample size is very small (n < 5) or precursor-fragment coupling information is absent from the raw data.

## Inputs

- Raw mass spectrometry data files (mzML, mzXML, netCDF format)
- Chromatographic information (m/z-RT peaklists from IDSL.IPA)
- Aligned peak table from IDSL.IPA peak_alignment directory
- IDSL.CSA parameter spreadsheet with user-configured workflow parameters

## Outputs

- Deconvoluted composite spectra table (precursor m/z, retention time, fragment ion intensities)
- MSP spectral library files
- Adduct-annotated peaklists
- Aligned spectra metadata with chemical structure aggregation (InChIKey, SMILES, molecular formula)

## How to apply

Load raw DDA mass spectrometry data into the IDSL.CSA R package after preprocessing with IDSL.IPA to obtain chromatographic m/z-RT information. Apply the DDA-specific deconvolution algorithm to group precursor ions with fragment ions by matching retention time windows and m/z relationships. Aggregate fragment ion intensities for each precursor to generate composite spectra. Configure deconvolution parameters using the IDSL.CSA parameter spreadsheet (39 parameters across 5 sections), specifying input/output paths and thread count. The deconvolution produces structured spectra tables containing precursor m/z, retention time, and grouped fragment ion intensities, which can then be annotated against reference libraries.

## Related tools

- **IDSL.CSA** (Primary R package for DDA spectra deconvolution, peak detection, chromatogram analysis, and composite spectra generation) — https://github.com/idslme/IDSL.CSA
- **IDSL.IPA** (Prerequisite workflow for chromatographic peak detection and m/z-RT extraction before running IDSL.CSA deconvolution)
- **IDSL.FSA** (Downstream integration for MSP file annotation and fragmentation library generation)
- **R** (Execution environment and statistical computing platform)

## Examples

```
library(IDSL.CSA)
IDSL.CSA_workflow("path/to/CSA_parameters.xlsx")
```

## Evaluation signals

- Precursor m/z and retention time values are populated and fall within expected instrument ranges.
- Fragment ion intensities are non-zero and sum correctly within each precursor's spectrum.
- MSP files are generated with valid header structure (NAME, PRECURSORMZ, RETENTIONTIME, Num Peaks) and peak lists.
- Deconvoluted spectra show improved annotation scores against reference libraries compared to raw DDA spectra.
- No orphan fragment ions remain ungrouped; all ions are assigned to precursor clusters based on RT and m/z criteria.

## Limitations

- Requires prior execution of IDSL.IPA workflow; cannot work directly on raw data without chromatographic alignment.
- Performance depends on accurate precursor-fragment ion pairing; weak or missing retention time coelution may lead to incomplete deconvolution.
- Parameter sensitivity: 39 configuration parameters must be carefully tuned for different MS instruments and ionization methods; inappropriate settings can produce spurious or empty spectra.
- No changelog available in repository; version compatibility with older IDSL.IPA outputs not documented.
- Designed for high-resolution mass spectrometry (HRMS); applicability to low-resolution or quadrupole-based DDA data not specified.

## Evidence

- [readme] DDA deconvolution methodology and scope: "This package can be used for the deconvolution of fragmentation spectra obtained through various analytical methods such as MS1-only Composite Spectra deconvolution Analysis (CSA), Data Dependent"
- [other] DDA grouping procedure: "Apply the DDA-specific deconvolution algorithm to group precursor ions with their corresponding fragment ions based on retention time and m/z relationships"
- [readme] Input file format requirements: "mass spectrometry data (mzXML, mzML, netCDF) using the IDSL.CSA workflow"
- [other] Output composite spectra structure: "Output the deconvoluted spectra as a structured table or composite spectrum object containing precursor m/z, retention time, and grouped fragment ion intensities"
- [readme] Preprocessing dependency: "mass spectrometry data should be processed using the IDSL.IPA workflow to acquire chromatographic information of the peaks (m/z-RT)"
- [readme] Annotation improvement objective: "The aim of the IDSL.CSA package is to assist in streamlining the data analysis process and improving the overall chemical structure annotation in the fields of metabolomics and exposomics"
