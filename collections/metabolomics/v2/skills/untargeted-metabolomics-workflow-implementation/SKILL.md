---
name: untargeted-metabolomics-workflow-implementation
description: Use when you have LC-MS/MS data acquired in DDA mode from untargeted metabolomics experiments and need to remove chimeric (co-fragmented) MS/MS spectra that result from multiple precursor ions fragmented simultaneously.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - R
  - DNMS2Purifier.r
  - DNMS2Purifier_model_generation.r
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.3c00736
  title: DNMS2Purifier
evidence_spans:
- The program is written in R (ver 4.2.1).
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dnms2purifier_cq
    doi: 10.1021/acs.analchem.3c00736
    title: DNMS2Purifier
  dedup_kept_from: coll_dnms2purifier_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c00736
  all_source_dois:
  - 10.1021/acs.analchem.3c00736
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# untargeted-metabolomics-workflow-implementation

## Summary

Implementation of an untargeted LC-MS/MS metabolomics workflow using DNMS2Purifier to detect and remove chimeric MS/MS spectra acquired in Data-Dependent Acquisition (DDA) mode. This skill ensures data quality in untargeted metabolomics studies by purifying MS/MS spectra before downstream spectral library matching and metabolite identification.

## When to use

Apply this skill when you have LC-MS/MS data acquired in DDA mode from untargeted metabolomics experiments and need to remove chimeric (co-fragmented) MS/MS spectra that result from multiple precursor ions fragmented simultaneously. Use it as a pre-processing step before spectral matching, annotation, or quantification workflows.

## When NOT to use

- Input data acquired in Targeted MS/MS (SRM/MRM) mode rather than DDA — DNMS2Purifier is designed specifically for DDA-mode data.
- MS/MS spectra already pre-processed by other chimeric filtering methods — applying redundant purification may introduce artifacts.
- Single-precursor isolation with no co-fragmentation expected — the purification overhead adds no value.

## Inputs

- LC-MS/MS raw data files acquired in DDA mode (mzML, NetCDF, or vendor format)
- MS/MS spectrum table with m/z and intensity pairs
- Pre-trained chimeric spectrum detection model (included in repository)

## Outputs

- Purified MS/MS spectra dataset with chimeric signals removed or flagged
- Spectrum metadata indicating purification status per MS/MS scan
- Quality control report of chimeric spectra identified and filtered

## How to apply

First, verify R version 4.2.1 is installed and obtain the DNMS2Purifier.r script from the HuanLab GitHub repository. Load the script to confirm all MS/MS purification logic and chimeric spectrum filtering routines are syntactically correct. Execute DNMS2Purifier.r on your DDA-mode LC-MS/MS data (typically in mzML or NetCDF format); the program analyzes MS/MS spectra to identify and flag chimeric signals based on trained statistical models. For customized training on instrument-specific data, optionally use the accompanying DNMS2Purifier_model_generation.r script to retrain the detection model. Validate output by confirming that all spectra are properly formatted and that chimeric MS/MS signals have been successfully flagged or removed.

## Related tools

- **DNMS2Purifier.r** (Main R script that executes MS/MS purification on DDA-mode LC-MS/MS data to identify and remove chimeric spectra) — https://github.com/HuanLab/DNMS2Purifier
- **DNMS2Purifier_model_generation.r** (Optional R script for retraining the chimeric spectrum detection model on custom LC-MS/MS datasets) — https://github.com/HuanLab/DNMS2Purifier
- **R** (Runtime environment (version 4.2.1) required to execute DNMS2Purifier scripts)

## Examples

```
Rscript DNMS2Purifier.r --input dda_data.mzML --output purified_spectra.csv --model trained_model.RData
```

## Evaluation signals

- Output spectra conform to expected MS/MS format (m/z, intensity pairs with valid metadata)
- All input spectra are accounted for in output (either passed, flagged, or removed with documented reason)
- Chimeric spectrum detection rate is stable and reproducible across technical replicates
- Peak intensity distribution and fragment patterns in purified spectra match known reference standards for non-chimeric spectra
- False positive rate of chimeric flagging remains <5% when validated against manually curated spectra

## Limitations

- No changelog available in repository — version history and bug fixes are not formally documented.
- Model performance depends on DDA acquisition parameters; custom retraining may be required for different MS instrument platforms or acquisition settings.
- Purification accuracy may degrade for low-abundance metabolites or complex mixtures with extensive co-elution.
- Requires R 4.2.1 specifically; compatibility with newer or older R versions is not stated.

## Evidence

- [readme] DNMS2Purifier is a bioinformatic solution that purifies chimeric MS/MS spectra from LC-MS/MS-based untargeted metabolomics in Data-Dependent Acquisition (DDA) mode.: "DNMS2Purifier is a bioinformatic solution that purifies chimeric MS/MS spectra from LC-MS/MS-based untargeted metabolomics in Data-Dependent Acquisition (DDA) mode."
- [readme] The R script DNMS2Purifier.r is the main program for MS/MS purification, we also provide the script DNMS2Purifier_model_generation.r for customized model training: "The R script DNMS2Purifier.r is the main program for MS/MS purification, we also provide the script DNMS2Purifier_model_generation.r for customized model training"
- [readme] The program is written in R (ver 4.2.1).: "The program is written in R (ver 4.2.1)."
- [other] Verify R 4.2.1 is installed and required dependencies for the DNMS2Purifier.r script are available.: "Verify R 4.2.1 is installed and required dependencies for the DNMS2Purifier.r script are available."
- [other] Load and parse the DNMS2Purifier.r script to confirm all function definitions, MS/MS purification logic, and chimeric spectrum filtering routines are syntactically correct.: "Load and parse the DNMS2Purifier.r script to confirm all function definitions, MS/MS purification logic, and chimeric spectrum filtering routines are syntactically correct."
- [other] Execute the program on representative DDA-mode LC-MS/MS test data (if available in the repository) to demonstrate chimeric spectrum detection and purification.: "Execute the program on representative DDA-mode LC-MS/MS test data (if available in the repository) to demonstrate chimeric spectrum detection and purification."
- [other] Validate that the output spectra are properly formatted and chimeric MS/MS signals have been successfully removed or flagged.: "Validate that the output spectra are properly formatted and chimeric MS/MS signals have been successfully removed or flagged."
