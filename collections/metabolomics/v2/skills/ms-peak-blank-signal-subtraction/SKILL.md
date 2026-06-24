---
name: ms-peak-blank-signal-subtraction
description: Use when you have an MS-DIAL feature table from DDA or DIA LC-MS analysis
  that includes blank injection samples (at least 3 recommended), and you need to
  eliminate features that are artifactual contamination rather than genuine metabolites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MS-CleanR
  - MS-DIAL
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.0c01594
  title: MS-CleanR
evidence_spans:
- MS-CleanR use as input MS-DIAL peak list processed in data dependent analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_cleanr_cq
    doi: 10.1021/acs.analchem.0c01594
    title: MS-CleanR
  dedup_kept_from: coll_ms_cleanr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c01594
  all_source_dois:
  - 10.1021/acs.analchem.0c01594
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS-peak-blank-signal-subtraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Remove features from an MS-DIAL peak list whose intensity in blank injection samples exceeds a user-defined threshold relative to study samples, eliminating background contamination introduced during LC-MS analysis. This is the first generic filtering operation in MS-CleanR's preprocessing workflow.

## When to use

Apply this skill when you have an MS-DIAL feature table from DDA or DIA LC-MS analysis that includes blank injection samples (at least 3 recommended), and you need to eliminate features that are artifactual contamination rather than genuine metabolites. Use it early in the MS-CleanR pipeline, before downstream feature clustering and annotation.

## When NOT to use

- Your LC-MS data contains fewer than 3 blank injections (insufficient statistical basis for blank detection)
- Your input is not a feature table but raw LC-MS data (use MS-DIAL peak picking first)
- You are analyzing targeted quantification data where all features are known to be true analytes (blank subtraction is already implicit in the assay design)

## Inputs

- MS-DIAL peak list (feature table with m/z, retention time, intensity, and sample class assignments)
- Blank injection sample intensity values
- Study sample intensity values

## Outputs

- Filtered MS-DIAL peak list with blank-contaminated features removed
- Feature retention/removal decision log (optional)

## How to apply

Load the MS-DIAL peak list containing m/z, retention time, intensity values, and sample class assignments (including blank, QC, and study samples). For each feature, calculate the median or mean intensity in blank samples and compare it to the median or mean intensity in study samples using a user-defined ratio threshold (e.g., blank intensity / study sample intensity). Remove features where the blank-to-study ratio exceeds this threshold, as these likely represent column carryover, solvent impurities, or instrument baseline noise. The threshold is tunable by the user and should be set based on the analytical platform's expected background level and the study's quality requirements.

## Related tools

- **MS-DIAL** (Peak detection and feature table generation; provides the input peak list and MS/MS spectra required for blank subtraction) — http://prime.psc.riken.jp/compms/index.html
- **MS-CleanR** (Automated blank signal subtraction and generic filtering workflow; implements the tunable threshold-based subtraction as its first step) — https://github.com/eMetaboHUB/MS-CleanR

## Evaluation signals

- Blank-derived features are removed: verify that features with blank/study intensity ratio above the user threshold are absent from the output feature table
- Study features are retained: confirm that features with high intensity in study samples and low or absent intensity in blanks are preserved in the output
- Sample class preservation: check that blank, QC, and study sample assignments remain intact in the output table (only feature rows are removed, not sample columns)
- Reproducibility: re-running with the same threshold on the same input should produce identical feature retention decisions
- Documentation: output should include or log which features were removed and their blank/study intensity ratios for audit trail

## Limitations

- Requires at least 3 blank samples explicitly marked in the MS-DIAL sample list; analysis will crash or be unreliable with fewer blanks
- Assumes blank samples and study samples are analyzed under identical instrumental conditions; if instrumental parameters drift between blank and study runs, the threshold may be non-transferable
- Cannot distinguish between true low-abundance metabolites and contamination when both occur at similar intensities; user must set the threshold carefully to avoid over-filtering genuine features
- Does not account for sample-specific contamination or sample-to-sample carryover; it only handles global blank contamination
- Sample or class names must not contain spaces or hyphens, and class names must not be a single letter, per MS-CleanR constraints

## Evidence

- [other] blank injection signal subtraction by identifying and removing features whose intensity in blank samples exceeds a user-defined threshold relative to study samples: "Subtract blank injection signals by identifying and removing features whose intensity in blank samples exceeds a user-defined threshold relative to study samples."
- [intro] Five generic filters applied, all tunable by the user: "MS-CleanR apply generic filters encompassing blank injection signal subtraction, background ions drift removal, unusual mass defect filtering, relative standard deviation threshold (RSD) based on"
- [readme] Minimum blank sample requirement: "At least 3 blanks and 3 QCs samples are needed for Blank ratio analysis. These samples must be identified as such in the MS-Dial sample list."
- [intro] Input is MS-DIAL peak list from DDA or DIA: "MS-CleanR use as input MS-DIAL peak list processed in data dependent analysis (DDA) or data independent analysis (DIA)"
- [readme] MS/MS data is required; MS1-only data will fail: "All features without MS/MS will be discarded during the first step. If data contain MS1 only, the first MS-CleanR step will crash."
