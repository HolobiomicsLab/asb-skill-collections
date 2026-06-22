---
name: r-script-validation-and-execution
description: Use when when you have obtained an R-based bioinformatic program (such as DNMS2Purifier.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
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

# R Script Validation and Execution

## Summary

Validate R script syntax, function definitions, and MS/MS purification logic before executing on LC-MS/MS metabolomics data to ensure chimeric spectrum detection and removal workflows run correctly. This skill verifies that the R environment and dependencies are properly configured and that output spectra meet expected formatting and purity standards.

## When to use

When you have obtained an R-based bioinformatic program (such as DNMS2Purifier.r) for processing LC-MS/MS Data-Dependent Acquisition (DDA) spectra and need to confirm it will execute correctly on your untargeted metabolomics dataset before committing computational resources or proceeding to downstream analysis. Use this skill when you want to verify that chimeric MS/MS spectra are being correctly detected, filtered, or flagged by the program.

## When NOT to use

- If the R script has already been validated by the source authors or in a prior run and you are simply re-executing it on new data without concerns about environment changes or code integrity.
- If your input data are already processed feature tables or aligned peak matrices rather than raw DDA-mode MS/MS spectra; this skill targets raw spectral purification, not post-processed metabolite tables.
- If your metabolomics data were acquired in Targeted or Selected Reaction Monitoring (SRM/MRM) mode rather than Data-Dependent Acquisition (DDA), since DNMS2Purifier is designed specifically for DDA chimeric spectra.

## Inputs

- R script source code (e.g., DNMS2Purifier.r)
- LC-MS/MS DDA-mode spectral data (test dataset or representative subset)
- R environment with required dependencies installed

## Outputs

- Validated R script (confirmed syntactically correct)
- Purified MS/MS spectra with chimeric signals removed or flagged
- Execution log or output report documenting spectrum processing results
- Formatted output spectra ready for downstream metabolomics analysis

## How to apply

First, verify that R 4.2.1 is installed and all required dependencies for the target script are available in your environment. Load and parse the main R script (e.g., DNMS2Purifier.r) to confirm all function definitions, MS/MS purification logic, and chimeric spectrum filtering routines are syntactically correct and free of errors. Execute the program on a small representative subset of DDA-mode LC-MS/MS test data (if available in the repository or from your own preliminary acquisition) to demonstrate that chimeric spectrum detection and purification routines are functioning as intended. Validate that the output spectra are properly formatted (match the expected data structure or file format), that chimeric MS/MS signals have been successfully removed or appropriately flagged, and that no unexpected errors or data loss occurred during processing. Compare output properties (e.g., spectrum counts before/after filtering, flagged vs. purified spectra) against documented expectations to confirm correct behavior.

## Related tools

- **DNMS2Purifier.r** (Main R script for MS/MS purification and chimeric spectrum detection in DDA-mode LC-MS/MS data) — https://github.com/HuanLab/DNMS2Purifier
- **DNMS2Purifier_model_generation.r** (Companion R script for customized model training to adapt purification logic to new datasets or instrument platforms) — https://github.com/HuanLab/DNMS2Purifier
- **R** (Programming language and runtime environment (version 4.2.1 required) for executing the DNMS2Purifier scripts)

## Examples

```
source('DNMS2Purifier.r'); result <- DNMS2Purifier(input_data = 'test_DDA_spectra.mzML', output_dir = './purified_spectra/')
```

## Evaluation signals

- R script parses without syntax errors and all function definitions (MS/MS purification logic, chimeric spectrum filtering routines) are recognized by the R interpreter.
- Program executes on test DDA-mode LC-MS/MS data without runtime errors or segmentation faults; execution completes and produces output files.
- Output spectra are correctly formatted (e.g., match the expected schema for m/z, intensity, metadata fields) and can be read by downstream analysis tools.
- Spectrum count and chimeric flagging/removal statistics are consistent with program design (e.g., fewer spectra in output than input if purification removed duplicates; documented chimeric signals are marked or absent).
- Visual or quantitative spot checks of a sample of input vs. output spectra confirm that high-quality spectra are retained and low-quality or chimeric spectra are removed or flagged as intended.

## Limitations

- No changelog is provided in the repository, limiting transparency on bug fixes, feature updates, or breaking changes between versions.
- Validation is dependent on availability of representative test data; if test data are not provided or do not reflect the characteristics of your actual samples, validation may not catch dataset-specific errors or edge cases.
- The skill confirms technical execution but does not validate the statistical or biological appropriateness of the purification model for your specific instrument, chromatography method, or sample type; customized model training (via DNMS2Purifier_model_generation.r) may be needed for non-standard workflows.
- R environment reproducibility (package versions, system libraries) is not explicitly managed by the script; dependency conflicts or version mismatches may cause failures despite script validation.

## Evidence

- [other] Verify R 4.2.1 is installed and required dependencies: "Verify R 4.2.1 is installed and required dependencies for the DNMS2Purifier.r script are available."
- [other] Load and parse the script to confirm function definitions and purification logic: "Load and parse the DNMS2Purifier.r script to confirm all function definitions, MS/MS purification logic, and chimeric spectrum filtering routines are syntactically correct."
- [other] Execute on representative DDA test data to demonstrate detection and purification: "Execute the program on representative DDA-mode LC-MS/MS test data (if available in the repository) to demonstrate chimeric spectrum detection and purification."
- [other] Validate output spectra are properly formatted and chimeric signals removed: "Validate that the output spectra are properly formatted and chimeric MS/MS signals have been successfully removed or flagged."
- [readme] DNMS2Purifier is for purifying chimeric MS/MS spectra from LC-MS/MS untargeted metabolomics in DDA mode: "DNMS2Purifier is a bioinformatic solution that purifies chimeric MS/MS spectra from LC-MS/MS-based untargeted metabolomics in Data-Dependent Acquisition (DDA) mode."
- [readme] DNMS2Purifier.r is the main program for MS/MS purification: "The R script DNMS2Purifier.r is the main program for MS/MS purification"
- [readme] Program written in R version 4.2.1: "The program is written in R (ver 4.2.1)."
