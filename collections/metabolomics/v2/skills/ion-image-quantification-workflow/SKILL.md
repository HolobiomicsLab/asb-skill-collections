---
name: ion-image-quantification-workflow
description: Use when when you have imzML mass spectrometry imaging data files and need to convert raw ion image intensities into quantitative lipid abundance (pmol/mm²) using known internal standards.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - LipidQMap
  - Cardinal
  techniques:
  - LC-MS
  - direct-infusion-MS
  - MS-imaging
derived_from:
- doi: 10.1101/2025.10.15.682422v1
  title: LipidQMap
evidence_spans:
- LipidQMap writes MSI exports as HDF5 containers
- LipidQMap writes MSI exports as HDF5 containers that follow the [`Cardinal::HDF5`](https://cardinalmsi.org) conventions.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidqmap_cq
    doi: 10.1101/2025.10.15.682422v1
    title: LipidQMap
  dedup_kept_from: coll_lipidqmap_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.10.15.682422v1
  all_source_dois:
  - 10.1101/2025.10.15.682422v1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-image-quantification-workflow

## Summary

A workflow for accurate quantitation of Mass Spectrometry Imaging (MSI) data by importing imzML files, applying isotopic correction, and quantifying lipid ion images against user-defined internal standards. This workflow enables conversion of raw ion intensities to quantitative lipid abundance measurements.

## When to use

When you have imzML mass spectrometry imaging data files and need to convert raw ion image intensities into quantitative lipid abundance (pmol/mm²) using known internal standards. Typical triggers include: (1) you have a 5 GB or larger imzML file with hundreds to thousands of ion images to process; (2) you need to correct for isotopic overlap (e.g., [M+H]+ contamination from [M+Na]+ adducts) before quantification; (3) you have selected specific lipid species of interest to quantify against spiked internal standards.

## When NOT to use

- Input is non-imaging mass spectrometry data (e.g., liquid chromatography–MS, direct infusion without spatial information) — use untargeted MS quantification workflows instead.
- Input imzML files are in negative ion mode but your database and internal standards are only defined for positive ion mode — reconfigure or create ion-mode-specific databases first.
- You do not have a well-characterized internal standard spiked onto your tissue samples — quantitation will fail; use semi-quantitative (relative intensity) workflows instead.

## Inputs

- imzML data file (mass spectrometry imaging format)
- Excel database of lipid species (with columns: ID, Class, Neutral Formula, Adducts, M-2 Isotope, Na+ Isotope, Is standard, Standard amount (pmol/mm²), IS)
- Ion mode designation (positive or negative)
- Mass error tolerance (ppm)
- Internal standard species identifier

## Outputs

- Quantitative ion images (pmol/mm² per lipid species)
- Raw ion intensity images (optional)
- Isotope-corrected ion images (optional)
- Exported images as individual files or combined panels (PNG/TIFF format)
- Species bar plot (average intensity per lipid class)
- Average mass spectrum visualization

## How to apply

Install LipidQMap on an M2 or later Apple silicon Mac or Windows 10/11 system. Open the imzML import dialog and select one or more imzML files, specifying ion mode (positive/negative), mass accuracy tolerance (ppm), and bin size for average spectrum calculation (default 5 mDa for TOF). Choose whether to apply Type II isotopic correction (to resolve [M+H]+ from [M+Na]+ overlap) and select an internal standard lipid species from a user-editable Excel database. Import the file(s) — on M2 hardware, a 5 GB file with 2500 ion images quantifies in ~20 seconds. After import, toggle between Raw, Isotope Corrected, and Quantified views in the main window. Mark lipid species for export in the Species table (column 'Export'), then save images via the 'Save images' dialog, choosing between individual unfiltered 1:1 pixel images, individually scaled/filtered images, or combined panels.

## Related tools

- **LipidQMap** (Primary GUI application for ion image import, isotopic correction, quantitation, and export in this workflow) — https://github.com/swinnenteam/LipidQMap
- **Cardinal** (MSI data format standard; LipidQMap exports quantified images as HDF5 containers following Cardinal::HDF5 conventions) — https://cardinalmsi.org

## Evaluation signals

- Processing time for a 5 GB imzML file with 2500 ion images should be approximately 20 seconds on M2 hardware; significantly slower times indicate system bottlenecks or data format issues.
- All selected lipid species in the Species table should have an entry in the Quantified data view with non-zero intensities where the internal standard signal is detectable; zero or NaN values indicate quantitation failure.
- Isotope-corrected and Quantitative image views should show visibly reduced noise/artifacts compared to Raw view when Type II isotopic correction is enabled, particularly at high m/z regions where adduct overlap occurs.
- Exported image files should have pixel-to-pixel correspondence with the original imzML spatial dimensions (verify pixel counts match original dataset metadata).
- Species bar plot should show consistent class-level intensity distributions across replicates when multiple imzML files are loaded; large unexplained variations suggest calibration or standard spiking issues.

## Limitations

- LipidQMap is currently available only for Windows 10+ and Apple silicon Macs (M1 and up); not available for Intel-based Macs, Linux, or older Windows versions.
- Type II isotopic correction assumes known mass difference and intensity ratios between [M+H]+ and [M+Na]+ adducts; correction accuracy depends on accurate database entries for M-2 Isotope and Na+ Isotope reference species.
- Quantitation accuracy is entirely dependent on the quality and uniformity of the internal standard spike; inhomogeneous standard distribution across tissue will produce spatially-variable quantitation errors.
- Manual editing of the Excel database is required; no automated lipid identification or formula validation is performed during import.
- No changelog is available in the repository, limiting tracking of bug fixes and feature improvements across versions.

## Evidence

- [readme] LipidQMap is a program to support accurate quantitation of Mass Spectrometry Imaging data.: "LipidQMap is a program to support accurate quantitation of Mass Spectrometry Imaging data."
- [readme] Works on imzML data files and can open multiple imzML files simultaneously.: "Works on imzML data files and can open multiple imzML files simultaneously."
- [readme] Can perform Type II isotopic correction, and can correct [M+H]+ adducts for isotopic overlap from [M+Na]+ adducts.: "Can perform Type II isotopic correction, and can correct [M+H]+ adducts for isotopic overlap from [M+Na]+ adducts."
- [readme] Performs quantitation based on user defined internal standards.: "Performs quantitation based on user defined internal standards."
- [readme] Is fast, opening a 5 GB imzML file and importing and quantifying 2500 ion images takes about 20 seconds on an M2 Macbook.: "Is fast, opening a 5 GB imzML file and importing and quantifying 2500 ion images takes about 20 seconds on an M2 Macbook."
- [readme] Can toggle view between raw, isotope corrected and quantified images.: "Can toggle view between raw, isotope corrected and quantified images."
- [readme] LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions.: "LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions."
- [readme] Select the maximum tolerated mass error (in ppm) for extracting the ion images.: "Select the maximum tolerated mass error (in ppm) for extracting the ion images."
- [readme] Each row in the Excel database represents a different species, and the file should contain the following columns (the column titles need to match exactly): ID, Class, Neutral Formula, Adducts, M-2 Isotope, Na+ Isotope, Is standard, Standard amount (pmol / mm2), IS.: "Each row in the Excel database represents a different species, and the file should contain the following columns (the column titles need to match exactly): ID, Class, Neutral Formula, Adducts, M-2"
- [readme] LipidQMap is available for Windows 10 (and up) and Mac (Apple silicon, M1 and up).: "LipidQMap is available for Windows 10 (and up) and Mac (Apple silicon, M1 and up)."
