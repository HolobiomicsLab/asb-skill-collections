---
name: dda-mode-metabolomics-data-processing
description: Use when when you have LC-MS/MS data collected in DDA mode and suspect
  that MS/MS spectra contain chimeric (multiply-charged or co-fragmented) ion signals
  that will degrade downstream spectral matching, library searching, or metabolite
  identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - R
  - DNMS2Purifier.r
  - DNMS2Purifier_model_generation.r
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# dda-mode-metabolomics-data-processing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Purify chimeric MS/MS spectra from untargeted metabolomics data acquired in Data-Dependent Acquisition (DDA) mode using DNMS2Purifier, a bioinformatic solution that removes or flags co-fragmented ion signals that confound spectral interpretation and compound identification.

## When to use

When you have LC-MS/MS data collected in DDA mode and suspect that MS/MS spectra contain chimeric (multiply-charged or co-fragmented) ion signals that will degrade downstream spectral matching, library searching, or metabolite identification. This is particularly critical for untargeted metabolomics workflows where spectral purity directly impacts annotation confidence.

## When NOT to use

- Input data is already a feature table or quantified metabolite matrix (run purification before feature extraction, not after).
- Data were acquired in targeted or parallel reaction monitoring (PRM/SRM) mode rather than untargeted DDA (DNMS2Purifier is specific to DDA mode).
- Raw spectra have already been deconvoluted or processed by another chimeric-spectrum removal tool (applying DNMS2Purifier to pre-filtered spectra may introduce redundant filtering or bias).

## Inputs

- LC-MS/MS raw data files acquired in Data-Dependent Acquisition (DDA) mode
- Precursor and fragment m/z lists with intensity values
- Scan metadata (retention time, precursor charge, isolation window)

## Outputs

- Purified MS/MS spectra with chimeric signals removed or flagged
- Annotated spectrum quality metrics (chimeric score or confidence)
- Filtered spectral library or feature table suitable for downstream matching

## How to apply

Obtain the DNMS2Purifier.r script from the HuanLab GitHub repository and confirm R 4.2.1 is installed with required dependencies available. Load the script and parse its function definitions to verify MS/MS purification logic and chimeric spectrum filtering routines are syntactically sound. Execute DNMS2Purifier.r on your DDA-mode LC-MS/MS data (typically in a format accepted by the script, such as mzML or vendor-specific formats). The program applies machine-learning or heuristic-based chimeric spectrum detection to identify and flag MS/MS scans containing multiple precursor ions or co-fragmented species. Validate the output spectra are properly formatted and that chimeric MS/MS signals have been successfully removed or annotated; cross-check purified spectra against raw data to confirm filtering logic did not remove genuine singleton spectra.

## Related tools

- **DNMS2Purifier.r** (Main R script for executing MS/MS spectrum purification on DDA-mode LC-MS/MS data; detects and filters chimeric MS/MS spectra) — https://github.com/HuanLab/DNMS2Purifier
- **DNMS2Purifier_model_generation.r** (R script for training customized chimeric spectrum detection models tailored to specific instrument or ionization method configurations) — https://github.com/HuanLab/DNMS2Purifier
- **R** (Execution environment and scripting language required to run DNMS2Purifier (version 4.2.1))

## Examples

```
Rscript DNMS2Purifier.r --input raw_dda_spectra.mzML --output purified_spectra.mzML
```

## Evaluation signals

- Output spectra conform to expected format (e.g., mzML, or the format native to the input); no malformed or truncated records.
- Chimeric spectra are correctly identified and tagged: spot-check flagged spectra to confirm they contain multiple precursor m/z peaks or fragments inconsistent with a single molecular ion.
- Singleton (non-chimeric) spectra are preserved in output: comparison of spectrum count between input and output should show only expected loss; manual inspection of a subset confirms genuine spectra were not over-filtered.
- Purified spectra show improved match scores in downstream spectral library searching compared to raw spectra, indicating reduced noise from co-fragmented ions.
- Reproducibility check: re-running DNMS2Purifier.r on the same input produces identical or equivalent output (no stochastic variation if model is fixed).

## Limitations

- DNMS2Purifier is optimized for DDA mode; applicability to other acquisition modes (PRM, SRM, data-independent acquisition) is not established in the provided documentation.
- No changelog or version history is available in the source repositories, making it difficult to track bug fixes or feature improvements across releases.
- Model performance is dependent on training data and instrument/ionization method; users may need to generate customized models via DNMS2Purifier_model_generation.r for non-standard configurations.
- Computational cost and runtime are not explicitly characterized in the provided documentation; performance on very large LC-MS/MS datasets is unknown.

## Evidence

- [readme] DNMS2Purifier is a bioinformatic solution that purifies chimeric MS/MS spectra from LC-MS/MS-based untargeted metabolomics in Data-Dependent Acquisition (DDA) mode.: "DNMS2Purifier is a bioinformatic solution that purifies chimeric MS/MS spectra from LC-MS/MS-based untargeted metabolomics in Data-Dependent Acquisition (DDA) mode."
- [readme] The R script DNMS2Purifier.r is the main program for MS/MS purification, we also provide the script DNMS2Purifier_model_generation.r for customized model training: "The R script DNMS2Purifier.r is the main program for MS/MS purification, we also provide the script DNMS2Purifier_model_generation.r for customized model training"
- [readme] The program is written in R (ver 4.2.1).: "The program is written in R (ver 4.2.1)."
- [intro] DNMS2Purifier.r serves as the main program that purifies chimeric MS/MS spectra from LC-MS/MS-based untargeted metabolomics data acquired in Data-Dependent Acquisition (DDA) mode.: "DNMS2Purifier.r serves as the main program that purifies chimeric MS/MS spectra from LC-MS/MS-based untargeted metabolomics data acquired in Data-Dependent Acquisition (DDA) mode."
- [other] Validate that the output spectra are properly formatted and chimeric MS/MS signals have been successfully removed or flagged.: "Validate that the output spectra are properly formatted and chimeric MS/MS signals have been successfully removed or flagged."
