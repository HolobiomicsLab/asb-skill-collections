---
name: spatial-distribution-pattern-analysis
description: Use when when you have loaded MSI peak data with associated m/z values and need to disambiguate matrix ions from analyte ions. Apply this skill when chemical formula alone is insufficient (e.g., overlapping or isobaric peaks exist) and you have pixel-level spatial intensity maps for each ion.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
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

# spatial-distribution-pattern-analysis

## Summary

Extract and evaluate spatial distribution patterns of ions across a mass spectrometry imaging dataset to classify matrix-related vs. analyte signals. This skill leverages co-localization coherence and spatial heterogeneity as discriminative features alongside chemical formula matching.

## When to use

When you have loaded MSI peak data with associated m/z values and need to disambiguate matrix ions from analyte ions. Apply this skill when chemical formula alone is insufficient (e.g., overlapping or isobaric peaks exist) and you have pixel-level spatial intensity maps for each ion. Particularly useful for silver-assisted or other matrix-dependent ionization methods where matrix peaks cluster spatially.

## When NOT to use

- Input is already processed into a feature table or data matrix without spatial coordinates—spatial patterns cannot be reconstructed.
- MSI dataset lacks pixel-level spatial intensity maps or has been heavily summarized (e.g., only mean spectra per region).
- Matrix composition is unknown or highly variable across the tissue—spatial coherence assumptions may not hold.

## Inputs

- MSI peak matrix (rMSIproc .zip format or equivalent)
- Processed MSI data with pixel-level intensity maps (.tar or equivalent)
- Chemical formula assignments or m/z calibration data for each ion
- Optional: known matrix or analyte m/z reference list

## Outputs

- Binary matrix/non-matrix classification labels per ion
- Spatial coherence metrics and pattern descriptors per ion
- Visual annotation report justifying spatial classification
- Cleaned peak matrix with matrix ions flagged or removed

## How to apply

Load MSI peak data and spatial intensity maps for each ion using rMSI or rMSIproc. Extract the spatial distribution pattern—pixel-by-pixel intensity across the imaging region—for each ion m/z. Compute spatial coherence metrics (e.g., uniformity, clustering, co-localization with known matrix or analyte landmarks) to classify ions. Matrix-related ions typically exhibit uniform or highly clustered spatial patterns reflecting matrix deposition; analytes show heterogeneous or focal distributions. Cross-reference spatial patterns against chemical formula predictions to resolve ambiguous cases (e.g., isobaric peaks with different spatial signatures). Generate a visual spatial report to document each ion's classification rationale.

## Related tools

- **rMSIcleanup** (Primary annotation and spatial pattern classification engine; integrates chemical formula and spatial distribution to label ions) — https://github.com/gbaquer/rMSIcleanup
- **rMSI** (Loads and manages MSI data structures and pixel-level intensity maps required for spatial pattern extraction) — https://github.com/prafols/rMSI
- **rMSIproc** (Processes raw imzML files into peak matrices and spatial datasets; handles data I/O in standardized formats) — https://github.com/prafols/rMSIproc
- **R** (Execution environment for rMSI, rMSIproc, and rMSIcleanup packages)
- **devtools** (Dependency management and installation of rMSI, rMSIproc, and rMSIcleanup from GitHub)

## Examples

```
results <- rMSIcleanup::annotate_matrix(pks, "Ag1", full); rMSIcleanup::generate_pdf_report(results, pks, full, "test", folder="/home/user/")
```

## Evaluation signals

- Spatial patterns for each ion are reproducible: re-running on the same dataset yields identical or near-identical coherence metrics and classifications.
- Matrix ions show clustering or uniformity (low variance) across pixels; analytes show heterogeneous (high variance or focal) distributions—verified by visual inspection of generated spatial maps.
- Overlapping peak detection correctly identifies isobaric ions by distinct spatial signatures (e.g., same m/z but different spatial localization receive different labels).
- Visual report transparently justifies at least 80% of classifications with spatial coherence and chemical formula evidence; annotations align with domain knowledge of the matrix and tissue type.
- Cleaned peak matrix after matrix removal shows reduced background noise in downstream analysis without loss of analyte signal in expected tissue regions.

## Limitations

- Algorithm assumes matrix-related ions exhibit spatially coherent (uniform or highly clustered) distributions; fails when matrix is inhomogeneously distributed or analytes co-localize exactly with matrix regions.
- Overlapping peak detection relies on distinct spatial signatures; co-localized isobaric ions (identical m/z and identical spatial pattern) cannot be disambiguated by this method alone.
- Chemical formula matching requires accurate mass calibration and known ion adducts; formula misassignment or unexpected ionization products may confound spatial classification.
- Spatial resolution and pixel size affect pattern detectability; low-resolution imaging may blur distinct spatial features and reduce classification confidence.

## Evidence

- [intro] The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related: "The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related"
- [intro] The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions: "The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions"
- [intro] The package generates a visual report to transparently justify each annotation: "the package generates a visual report to transparently justify each annotation"
- [other] Extract spatial distribution patterns for each ion across the imaging dataset: "Extract spatial distribution patterns for each ion across the imaging dataset"
- [other] Assign binary matrix/non-matrix labels to each ion based on formula matching and spatial coherence metrics: "Assign binary matrix/non-matrix labels to each ion based on formula matching and spatial coherence metrics"
