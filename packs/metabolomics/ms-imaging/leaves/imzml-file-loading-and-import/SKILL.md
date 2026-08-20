---
name: imzml-file-loading-and-import
description: Use when when you have one or more imzML files containing mass spectrometry imaging data and need to import them into LipidQMap for ion image extraction, isotopic correction, and quantitative analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - LipidQMap
  - Cardinal
  techniques:
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# imzml-file-loading-and-import

## Summary

Load and import imzML mass spectrometry imaging files into LipidQMap, configuring ion extraction parameters, isotope correction, and calibration settings prior to ion image display and quantitation. This skill is essential for preparing raw MSI data for downstream lipid quantitation and visualization workflows.

## When to use

When you have one or more imzML files containing mass spectrometry imaging data and need to import them into LipidQMap for ion image extraction, isotopic correction, and quantitative analysis. Typical trigger: you possess imzML data files (5 GB or larger) with hundreds to thousands of ion images that require standardized mass error tolerance, isotope overlap correction, and internal standard-based quantitation.

## When NOT to use

- Input data is not in imzML format (e.g., vendor-specific binary formats that have not been converted to imzML)
- Lipid database is missing required columns (ID, Class, Neutral Formula, Adducts) or contains formatting inconsistencies
- You intend only to perform basic mass spectrum visualization without quantitation or isotope correction; simpler MSI viewers may be more appropriate

## Inputs

- imzML file(s) (mass spectrometry imaging data in imzML format)
- Lipid species database (Excel spreadsheet with ID, Class, Neutral Formula, Adducts, M-2 Isotope, Na+ Isotope, Is standard, Standard amount, and IS columns)
- Reference m/z value (optional, for online calibration)

## Outputs

- Loaded and parsed imzML data in LipidQMap memory with ion images extracted at specified mass error tolerance
- Displayed ion images for each lipid species in the species table (togglable between raw, isotope-corrected, and quantitative views)
- Average mass spectrum for the loaded imzML file(s)
- Species bar plot for lipid class visualization

## How to apply

Open the imzML import dialog via the folder icon in the main LipidQMap window. Select one or more imzML files and specify: (1) ionization mode (positive or negative); (2) mass error tolerance in ppm for ion image extraction (instrument-dependent; 5 ppm is typical for TOF); (3) bin size for average spectrum calculation (default 5 mDa for TOF, lower for higher-resolution instruments); (4) whether to impute missing pixels using 3×3 neighborhood mean; (5) a lipid database from the dropdown; (6) isotope correction algorithm if desired (Type II correction available for [M+H]+ overlap from [M+Na]+); (7) online calibration settings if a reference m/z is available with specified ppm tolerance and minimum intensity threshold. Click 'Import Data' to initiate import. Processing time scales with file size; a 5 GB imzML with 2500 ion images completes in approximately 20 seconds on M2 Macbook hardware.

## Related tools

- **LipidQMap** (Primary application for imzML import, parsing, and ion image extraction with configurable mass error tolerance and isotope correction) — https://github.com/swinnenteam/LipidQMap
- **Cardinal** (Defines HDF5 export conventions followed by LipidQMap for downstream MSI data interchange) — https://cardinalmsi.org

## Evaluation signals

- Ion images are successfully displayed in the main window for all lipid species in the selected database without import errors
- Mass error tolerance is correctly applied: extracted ion images correspond to m/z values within the specified ppm range of the theoretical masses
- If isotope correction is enabled, toggling between Raw, Isotope corrected, and Quantitative views shows visibly different intensity distributions in the same spatial regions
- Processing time for import matches expected performance: 5 GB imzML file with 2500 ion images completes within ~20–30 seconds on comparable hardware
- Species bar plot and average mass spectrum render correctly and update when different species are selected in the species table

## Limitations

- Import speed and memory usage scale linearly with file size and number of ion images; very large files (>10 GB) may require significant RAM and processing time
- Online calibration requires a detectable reference m/z with sufficient intensity in each pixel spectrum; absence of reference signal will disable calibration for affected pixels
- Isotope correction (Type II) is only applicable if the database includes M-2 and Na+ Isotope IDs for each species; missing entries will prevent correction for those species
- Imputation of missing pixels via 3×3 mean may introduce artifacts at image edges or in sparse regions; validation against raw data is recommended for quantitative downstream use
- LipidQMap is available only for Windows 10+ and macOS with Apple silicon (M1 and later); other architectures or operating systems require developer setup

## Evidence

- [readme] In the imzML import dialog, click on the "Open Files" button to select one or more imzML files. Select if the file contains positive or negative ion mode data. Select the maximum tolerated mass error (in ppm) for extracting the ion images.: "In the imzML import dialog, click on the "Open Files" button to select one or more imzML files. Select if the file contains positive or negative ion mode data. Select the maximum tolerated mass error"
- [readme] Select the Bin size used for calculating the average spectrum (Default 5 mDa for TOF instruments, should be decreased for higher resolution instruments). Select if missing pixels should be imputated by taking the mean of the surrounding 3x3 pixels.: "Select the Bin size used for calculating the average spectrum (Default 5 mDa for TOF instruments, should be decreased for higher resolution instruments). Select if missing pixels should be imputated"
- [readme] Select which database should be used in the Database dropdown menu. Select which (if any) isotope correction algorithm should be used. Select if online calibration should be applied to the images.: "Select which database should be used in the Database dropdown menu. Select which (if any) isotope correction algorithm should be used. Select if online calibration should be applied to the images."
- [readme] Is fast, opening a 5 GB imzML file and importing and quantifying 2500 ion images takes about 20 seconds on an M2 Macbook.: "Is fast, opening a 5 GB imzML file and importing and quantifying 2500 ion images takes about 20 seconds on an M2 Macbook."
- [readme] LipidQMap is available for Windows 10 (and up) and Mac (Apple silicon, M1 and up).: "LipidQMap is available for Windows 10 (and up) and Mac (Apple silicon, M1 and up)."
- [readme] Each row in the Excel database represents a different species, and the file should contain the following columns (the column titles need to match exactly): ID, Class, Neutral Formula, Adducts, M-2 Isotope, Na+ Isotope, Is standard, Standard amount (pmol / mm2), IS.: "Each row in the Excel database represents a different species, and the file should contain the following columns (the column titles need to match exactly): ID, Class, Neutral Formula, Adducts, M-2"
