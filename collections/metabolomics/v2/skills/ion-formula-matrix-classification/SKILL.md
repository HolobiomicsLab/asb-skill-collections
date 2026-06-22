---
name: ion-formula-matrix-classification
description: Use when you have peak data from MSI experiments (stored as .zip peak matrix files) where matrix ions (e.g., silver adducts in AgLDI-MSI) dominate the spectrum and obscure analyte signals.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3179
  tools:
  - rMSIcleanup
  - rMSI
  - rMSIproc
  - R
  - devtools
derived_from:
- doi: 10.1186/s13321-020-00449-0
  title: ''
evidence_spans:
- rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI data
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Ion formula and spatial distribution matrix classification

## Summary

Classify ions detected in mass spectrometry imaging (MSI) data as matrix-related or analyte-related by integrating chemical formula matching against known matrix characteristics with spatial distribution coherence metrics. This skill automates removal of matrix-background noise from MSI datasets, improving signal-to-noise and enabling more reliable downstream analysis of tissue-localized molecular species.

## When to use

You have peak data from MSI experiments (stored as .zip peak matrix files) where matrix ions (e.g., silver adducts in AgLDI-MSI) dominate the spectrum and obscure analyte signals. You possess chemical formulas for the detected peaks and want to systematically annotate which ions arise from the matrix reagent rather than from tissue analytes, particularly when peak overlap or isobaric interference complicates manual curation.

## When NOT to use

- Peak matrix is already curated or pre-filtered for matrix ions—applying this skill again risks over-removal.
- Chemical formulas are absent or highly uncertain; the algorithm relies on formula-to-matrix matching and will produce unreliable classifications without reliable assignments.
- Matrix composition is unknown or highly variable across samples; the algorithm requires a reference matrix ion pattern or known matrix characteristics (e.g., Ag isotope patterns) to anchor classification.

## Inputs

- Peak matrix file (.zip format from rMSIproc)
- Processed MSI data file (.tar format from rMSI)
- Ion chemical formulas (m/z values with assigned molecular identities)
- Known matrix composition or matrix ion pattern library (e.g., expected Ag+ adducts)

## Outputs

- Annotated ion list with binary matrix/non-matrix labels
- Spatial distribution coherence metrics per ion
- Visual PDF report justifying each annotation
- Cleaned peak matrix (.zip) with matrix ions removed or flagged

## How to apply

Load the MSI peak matrix and chemical formulas into rMSI using rMSIproc::LoadPeakMatrix() and rMSI::LoadMsiData(). Extract spatial distribution patterns for each ion across the imaging dataset. Apply rMSIcleanup::annotate_matrix() to evaluate each ion's chemical formula against known matrix characteristics (e.g., silver-based formulas in AgLDI experiments) and compute spatial coherence metrics. The algorithm simultaneously performs overlapping peak detection to flag isobaric or co-localized ions that could be misclassified. Each ion receives a binary matrix/non-matrix label based on formula-matrix matching score and spatial distribution uniformity (matrix ions tend to distribute uniformly across tissue regions, while analyte ions cluster to specific regions). Generate a visual PDF report using rMSIcleanup::generate_pdf_report() to transparently justify each annotation, then apply rMSIcleanup::remove_matrix() to create a cleaned peak matrix.

## Related tools

- **rMSIcleanup** (Core package that implements the matrix classification algorithm (annotate_matrix), report generation, and matrix removal; must be installed via devtools) — https://github.com/gbaquer/rMSIcleanup
- **rMSI** (Provides functions to load and manage MSI data objects (LoadMsiData); required dependency for rMSIcleanup) — https://github.com/prafols/rMSI
- **rMSIproc** (Handles I/O for peak matrix files (LoadPeakMatrix, StorePeakMatrix) and MSI data preprocessing; required dependency) — https://github.com/prafols/rMSIproc
- **R** (Host language for the rMSIcleanup package and its dependencies)
- **devtools** (Package manager used to install rMSI, rMSIproc, and rMSIcleanup from GitHub)

## Examples

```
results<-rMSIcleanup::annotate_matrix(pks,"Ag1",full); rMSIcleanup::generate_pdf_report(results,pks,full,"matrix_report",folder="./output/"); pks_clean<-rMSIcleanup::remove_matrix(pks,results)
```

## Evaluation signals

- All ions in the output are assigned a binary (matrix or non-matrix) label with no missing or ambiguous classifications.
- Spatial coherence metrics for matrix-classified ions are uniformly high across the tissue region (indicating homogeneous matrix distribution), while non-matrix ions show clustered or heterogeneous spatial patterns.
- The PDF report correctly identifies overlapping peaks and flags isobaric ion pairs, preventing false positives in matrix classification.
- Cleaned peak matrix (after remove_matrix) shows reduced ion count and improved signal intensity for known tissue analytes compared to the input peak matrix.
- Chemical formula assignments in the report match the expected matrix composition (e.g., silver isotope patterns [107Ag, 109Ag] for AgLDI-MSI experiments).

## Limitations

- Relies on accurate chemical formula assignment; if formulas are misassigned or incomplete, classification accuracy degrades.
- Designed for matrix-rich datasets where matrix ions dominate; may underperform if matrix signal is already weak or sample heterogeneity is extreme.
- No discussion of performance on multiply-charged ions or unusual matrix reagents beyond silver; applicability to other matrix systems (e.g., MALDI matrices) not explicitly validated in the article.
- Overlapping peak detection mitigates but does not eliminate false positives for very dense isobaric clusters; manual validation may be needed for ambiguous ions.

## Evidence

- [intro] The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related: "The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related"
- [intro] The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions: "The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions"
- [intro] the package generates a visual report to transparently justify each annotation: "the package generates a visual report to transparently justify each annotation"
- [readme] rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI data: "rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI data"
- [readme] devtools::install_github('gbaquer/rMSIcleanup', ref = '0.1'): "devtools::install_github('gbaquer/rMSIcleanup', ref = '0.1')"
