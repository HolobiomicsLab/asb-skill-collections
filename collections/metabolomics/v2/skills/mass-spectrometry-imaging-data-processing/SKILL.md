---
name: mass-spectrometry-imaging-data-processing
description: Use when you have raw or processed MSI data (in imzML or rMSIproc formats)
  and need to identify and annotate matrix-related peaks before statistical analysis
  or metabolite identification. Use it specifically when your MSI experiment employed
  a chemical matrix (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3929
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - rMSIcleanup
  - rMSI
  - rMSIproc
  - R
  - devtools
  techniques:
  - MS-imaging
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-020-00449-0
  title: ''
evidence_spans:
- rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI
  data
- devtools::install_github("prafols/rMSI", ref = "0.8")
- devtools::install_github("prafols/rMSIproc", ref = "0.2")
- rMSIcleanup is an open-source R package
- install.packages("devtools")
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rmsicleanup_ms_imaging_matrix_peak_annot_cq
    doi: 10.1186/s13321-020-00449-0
    title: ''
  dedup_kept_from: coll_rmsicleanup_ms_imaging_matrix_peak_annot_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-020-00449-0
  all_source_dois:
  - 10.1186/s13321-020-00449-0
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Mass-spectrometry imaging data processing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Load, preprocess, and annotate mass spectrometry imaging (MSI) peak matrices by integrating chemical formula and spatial distribution patterns to classify matrix-related ions, detect overlapping peaks, and generate transparent visual justification reports. This skill is essential for cleaning MSI datasets prior to downstream analysis by removing or flagging matrix contamination that would confound metabolite or biomarker discovery.

## When to use

Apply this skill when you have raw or processed MSI data (in imzML or rMSIproc formats) and need to identify and annotate matrix-related peaks before statistical analysis or metabolite identification. Use it specifically when your MSI experiment employed a chemical matrix (e.g., silver for SALDI, MALDI matrices) and you must distinguish genuine analyte signals from matrix background and matrix adducts across the tissue spatial domain.

## When NOT to use

- Input MSI data was acquired without a chemical matrix (e.g., native MALDI or direct analysis in real time); matrix annotation is not applicable.
- Peak matrix is already curated or has been subjected to orthogonal matrix removal methods; re-annotation may introduce redundant or conflicting labels.
- Input data is not in rMSIproc or rMSI native formats; conversion or re-processing via rMSIproc::ProcessWizard() is required first.

## Inputs

- Peak matrix file in .zip format (rMSIproc binary format)
- Processed MSI dataset file in .tar format (rMSI format)
- Chemical formula string for the matrix compound (e.g., 'Ag1', 'C7H7N1O3' for MALDI DHB)

## Outputs

- Annotation results object containing binary matrix/non-matrix labels per ion
- PDF visual report with per-ion spatial maps, formula identifiers, and classification justifications
- Cleaned peak matrix file (.zip) with matrix-related peaks removed or flagged

## How to apply

Begin by loading the peak matrix (.zip format) and full processed MSI dataset (.tar format) using rMSIproc::LoadPeakMatrix and rMSI::LoadMsiData. Apply rMSIcleanup::annotate_matrix() with the matrix chemical formula (e.g., 'Ag1' for silver) as a reference; this function evaluates each ion's chemical formula against known matrix characteristics and analyzes its spatial distribution coherence across the imaging dataset. The algorithm simultaneously runs overlapping peak detection to flag isobaric or co-localized ions that risk misclassification. Generate a transparent PDF report using rMSIcleanup::generate_pdf_report() that displays per-annotation panels showing the ion's spatial map, m/z value, chemical formula, peak overlap status, and binary matrix/non-matrix classification justification. Finally, remove annotated matrix peaks using rMSIcleanup::remove_matrix() to produce a cleaned peak matrix, and store both before and after matrices using rMSIproc::StorePeakMatrix() for reproducibility.

## Related tools

- **rMSIcleanup** (Core annotation and matrix classification engine; main entry point for annotate_matrix(), generate_pdf_report(), and remove_matrix() functions) — https://github.com/gbaquer/rMSIcleanup
- **rMSI** (Loads and parses processed MSI dataset objects (.tar format) required as input to annotation; provides spatial and spectral data structures) — https://github.com/prafols/rMSI
- **rMSIproc** (Loads peak matrix from binary .zip format; stores cleaned peak matrix after matrix removal; provides ProcessWizard() for conversion of imzML to rMSIproc format) — https://github.com/prafols/rMSIproc
- **R** (Runtime environment and language for package execution)
- **devtools** (Installation and dependency management for rMSI, rMSIproc, and rMSIcleanup from GitHub)

## Examples

```
pks <- rMSIproc::LoadPeakMatrix("Ag_Pancreas_TOF_2015_Dataset2.zip"); full <- rMSI::LoadMsiData("Ag_Pancreas_TOF_2015_Dataset2_proc.tar"); results <- rMSIcleanup::annotate_matrix(pks, "Ag1", full); rMSIcleanup::generate_pdf_report(results, pks, full, "test", folder="/home/user/"); pks_clean <- rMSIcleanup::remove_matrix(pks, results); rMSIproc::StorePeakMatrix("after.zip", pks_clean)
```

## Evaluation signals

- All ions in the output annotation object have binary matrix/non-matrix labels assigned; no NA or undefined classifications remain.
- The PDF report contains one multi-panel entry per annotated ion, with visible spatial maps, formula strings, and overlap status indicators; no missing or blank annotation pages.
- Removed matrix peaks appear in the cleaned peak matrix with zero or NA intensity values across all pixel locations; spot-check spatial maps confirm matrix signal elimination.
- Isobaric or spatially overlapping ion pairs flagged by overlapping peak detection are correctly highlighted in the report with justification text; manual review of co-localized ions confirms risk assessment accuracy.
- The cleaned peak matrix has fewer total ions than the input matrix, proportional to the matrix/non-matrix ratio; storage file size and ion count decrease monotonically.

## Limitations

- Annotation accuracy depends on correctness of the input chemical formula for the matrix compound; incorrect or ambiguous formula strings (e.g., 'Ag' vs. 'Ag1') may lead to false positives or negatives.
- The algorithm relies on spatial coherence metrics to distinguish matrix from analyte; highly localized or tissue-specific matrix deposition patterns may not be reliably separated.
- Overlapping peak detection is limited to within-sample isobaric or m/z-adjacent ions; it does not account for cross-sample adduct complexity or instrument-specific isotope patterns not represented in the chemical formula database.
- Input data must be in native rMSI/rMSIproc formats; imzML and other public MSI formats require prior conversion via rMSIproc::ProcessWizard(), which may introduce processing artifacts or parameter-dependent bias.

## Evidence

- [intro] The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related, and incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions.: "The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related, and incorporates an overlapping peak detection feature to prevent"
- [intro] The package generates a visual report to transparently justify each annotation by documenting the classification rationale, spatial distribution pattern, and peak overlap status for each ion.: "the package generates a visual report to transparently justify each annotation"
- [other] Load MSI peak data and associated chemical formulas into R; Extract spatial distribution patterns; Apply algorithm to evaluate chemical formula against known matrix characteristics; Perform overlapping peak detection; Assign binary labels; Generate visual annotation report.: "1. Load MSI peak data and associated chemical formulas into R using rMSI. 2. Extract spatial distribution patterns for each ion across the imaging dataset. 3. Apply the rMSIcleanup algorithm to"
- [readme] Basic workflow steps include loading data, annotating matrix, generating a PDF report, removing matrix peaks, and storing results.: "## 2.1. Load Data
pks<-rMSIproc::LoadPeakMatrix("[Full Path to Peak Matrix (.zip)]")  ## 2.2. Annotate Matrix
results<-rMSIcleanup::annotate_matrix(pks,"Ag1",full)  ## 2.3. Generate"
- [readme] Input data must be processed into rMSIproc format; raw imzML can be converted using ProcessWizard().: "rMSIcleanup uses data in the rMSIproc format. To annotate your own data you will have to process the imzML using the following command: > rMSIproc::ProcessWizard()"
