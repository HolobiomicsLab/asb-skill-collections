---
name: ms-ms-spectrum-purification
description: Use when processing LC-MS/MS data acquired in DDA mode that contains chimeric (co-fragmented) MS/MS spectra—i.e., when a single MS/MS scan contains fragments from multiple precursor ions due to co-isolation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# ms-ms-spectrum-purification

## Summary

DNMS2Purifier purifies chimeric MS/MS spectra from LC-MS/MS untargeted metabolomics data acquired in Data-Dependent Acquisition (DDA) mode by detecting and removing co-isolated peptide or metabolite signals that contaminate individual MS/MS scans. This skill is essential for improving the quality and interpretability of downstream spectral matching and metabolite annotation.

## When to use

Apply this skill when processing LC-MS/MS data acquired in DDA mode that contains chimeric (co-fragmented) MS/MS spectra—i.e., when a single MS/MS scan contains fragments from multiple precursor ions due to co-isolation. Typical triggers include: (1) unexplained peaks in MS/MS spectra that do not match the nominal precursor mass, (2) low-quality spectral database matches despite high precursor signal, or (3) ambiguous metabolite identifications in untargeted metabolomics workflows.

## When NOT to use

- Input data is already fragmented or pre-processed by another chimeric filtering tool (avoid double-filtering).
- Data acquired in targeted MS/MS mode (Selected Reaction Monitoring, SRM) or Parallel Reaction Monitoring (PRM), where co-isolation is intentionally controlled and less prevalent.
- MS/MS spectra have already been manually curated or validated against a reference spectral library; repurification may introduce unnecessary noise.

## Inputs

- LC-MS/MS raw data in DDA mode (mzML, netCDF, or equivalent parseable format)
- Precursor m/z list with scan identifiers
- MS/MS fragment ion intensity vectors per scan

## Outputs

- Purified MS/MS spectral dataset with chimeric scans removed or flagged
- QC report indicating number of chimeric scans detected and removed
- Formatted spectrum file suitable for downstream spectral matching or annotation

## How to apply

Load raw DDA-mode LC-MS/MS data (in a format parseable by R, such as mzML or netCDF) into the DNMS2Purifier.r main program running under R 4.2.1. The program applies chimeric spectrum detection logic to identify MS/MS scans where fragment ion intensities deviate from expected patterns for a single precursor. For each scan, the algorithm evaluates whether isolated fragments are consistent with the declared precursor m/z; scans failing this consistency check are flagged or removed. Execute the program on representative test data to validate that output spectra are properly formatted and that chimeric signals have been successfully removed or flagged. Optionally, use DNMS2Purifier_model_generation.r to train a customized classifier on your instrument or sample type if the default model does not fit your data distribution.

## Related tools

- **DNMS2Purifier.r** (Main execution script for MS/MS spectrum purification; orchestrates chimeric detection and filtering logic on DDA LC-MS/MS data.) — https://github.com/HuanLab/DNMS2Purifier
- **DNMS2Purifier_model_generation.r** (Auxiliary script for training a customized chimeric spectrum classifier on user-supplied training data; enables adaptation to instrument platform or metabolite class.) — https://github.com/HuanLab/DNMS2Purifier
- **R** (Runtime environment (version 4.2.1 required) for executing DNMS2Purifier.r and dependency libraries.)

## Examples

```
Rscript DNMS2Purifier.r --input raw_dda_data.mzML --output purified_spectra.mzML
```

## Evaluation signals

- Output spectra conform to expected format (e.g., m/z–intensity pairs, valid precursor mass annotations) with no malformed records.
- Chimeric scans are consistently identified (i.e., repeated runs on the same input produce identical flagged/removed scan lists, indicating deterministic behavior).
- Fragment ion mass-to-charge ratios in purified spectra remain within instrument resolution (e.g., ±5 ppm for high-resolution MS) of theoretical values for the declared precursor.
- Downstream spectral matching scores (e.g., cosine similarity to reference spectra) are higher for purified spectra than for uncleaned spectra from the same sample.
- Manual inspection of a random sample of removed scans confirms that they contain fragments not explainable by the isolated precursor alone (e.g., unexpected peaks, multiple mass ladders).

## Limitations

- No changelog or version history provided; reproducibility across versions may be uncertain.
- Default model training data and thresholds not fully documented in available READMEs; performance on underrepresented instrument types or novel metabolite classes is unvalidated.
- Requires R 4.2.1 specifically; compatibility with other R versions not stated.
- User manual format (Word document) may not be machine-readable or portable; script dependencies and exact parameter tuning are not detailed in the README.

## Evidence

- [readme] DNMS2Purifier is a bioinformatic solution that purifies chimeric MS/MS spectra from LC-MS/MS-based untargeted metabolomics in Data-Dependent Acquisition (DDA) mode.: "DNMS2Purifier is a bioinformatic solution that purifies chimeric MS/MS spectra from LC-MS/MS-based untargeted metabolomics in Data-Dependent Acquisition (DDA) mode."
- [readme] The R script DNMS2Purifier.r is the main program for MS/MS purification, we also provide the script DNMS2Purifier_model_generation.r for customized model training.: "The R script DNMS2Purifier.r is the main program for MS/MS purification, we also provide the script DNMS2Purifier_model_generation.r for customized model training."
- [readme] The program is written in R (ver 4.2.1).: "The program is written in R (ver 4.2.1)."
- [other] Verify R 4.2.1 is installed and required dependencies for the DNMS2Purifier.r script are available.: "Verify R 4.2.1 is installed and required dependencies for the DNMS2Purifier.r script are available."
- [other] Validate that the output spectra are properly formatted and chimeric MS/MS signals have been successfully removed or flagged.: "Validate that the output spectra are properly formatted and chimeric MS/MS signals have been successfully removed or flagged."
