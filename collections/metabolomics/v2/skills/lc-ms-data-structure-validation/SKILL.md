---
name: lc-ms-data-structure-validation
description: Use when before launching TARDIS peak detection on a new LC–MS dataset or target compound list. Apply this skill when you have raw MS data files in vendor formats (e.g., .raw, .d) and/or a spreadsheet-based target list (.xlsx or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - TARDIS
  - R
  - MSConvert (ProteoWizard)
  - Spectra
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- Targeted peak integration of LC-MS data using TARDIS
- rmarkdown::html_document
- Quick start for targeted peak integration of LC-MS data using TARDIS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tardis_cq
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  dedup_kept_from: coll_tardis_cq
schema_version: 0.2.0
---

# lc-ms-data-structure-validation

## Summary

Validate that raw LC–MS data files are in centroided .mzML format and that compound target lists contain required columns (ID, name, m/z, RT, polarity) before targeted peak integration. This prerequisite check ensures TARDIS can correctly parse MS spectra and match targets to detected peaks.

## When to use

Before launching TARDIS peak detection on a new LC–MS dataset or target compound list. Apply this skill when you have raw MS data files in vendor formats (e.g., .raw, .d) and/or a spreadsheet-based target list (.xlsx or .csv) that you plan to use for automated peak integration and quality metrics extraction.

## When NOT to use

- Data is already centroided and in .mzML format — skip file conversion.
- Target list is already loaded into a TARDIS-compatible MsExperiment object.
- Peak detection has already been run; use this skill only during initial data setup, not for troubleshooting existing results.

## Inputs

- Raw MS data files (vendor format: .raw, .d, .ms, etc.)
- Target compound list (.xlsx, .csv, or other tabular format with columns: ID, Name, m/z, RT, Polarity)

## Outputs

- Centroided .mzML files (validated for TARDIS input)
- Validated target data.frame with required columns and correct data types
- Screening mode results showing target visibility in m/z–RT windows

## How to apply

First, convert raw MS data files to centroided .mzML format using MSConvert (ProteoWizard) — this is a mandatory preprocessing step because TARDIS requires centroided spectra and the .mzML standard for compatibility. Second, load your target compound list (e.g., from targets.xlsx) into R and verify that it contains at least five columns: a unique compound ID, a compound name, theoretical or measured m/z value, expected RT (in minutes), and a polarity indicator (positive or negative ionization mode). Third, check that the ID column contains unique values, m/z and RT columns are numeric, and polarity values match the pos_pattern and neg_pattern strings you intend to pass to TARDIS (e.g., 'POS' and 'NEG'). If any required column is missing or malformed, the createTargetList() function will fail or produce unreliable target-to-peak matching. Finally, perform a screening run (screening_mode = TRUE in TARDIS) on a subset of your files to confirm that targets are visible within your m/z and RT windows; this catches configuration errors before processing entire datasets.

## Related tools

- **MSConvert (ProteoWizard)** (Convert raw vendor MS data files to centroided .mzML format, a mandatory preprocessing step for TARDIS input)
- **TARDIS** (Perform targeted peak detection and quality assessment after data structure validation; requires centroided .mzML files and a validated target data.frame) — https://github.com/pablovgd/TARDIS
- **R** (Load, inspect, and validate target compound lists using base R and dplyr; call createTargetList() to format targets for TARDIS) — https://cloud.r-project.org/
- **Spectra** (Load centroided MS data as Spectra objects for downstream integration with TARDIS)

## Examples

```
library(TARDIS); targets <- read.xlsx('targets.xlsx'); validated_targets <- createTargetList(file = targets, pos_pattern = 'POS', neg_pattern = 'NEG', polarity = 'positive', ion_column = 'Polarity', columns_of_interest = list(id = 'CompoundID', name = 'Name', mz = 'mz', rt = 'RT'))
```

## Evaluation signals

- All raw MS data files successfully convert to centroided .mzML without errors or warnings from MSConvert.
- Target data.frame contains exactly five required columns (ID, Name, m/z, RT, Polarity) with correct data types: ID and Name are character/string, m/z and RT are numeric, Polarity is character matching pos_pattern or neg_pattern.
- No duplicate values in the ID column; row count matches the number of unique target compounds intended for analysis.
- Screening mode (screening_mode = TRUE) runs without error and produces visible extracted ion chromatograms (EICs) for ≥80% of targets, confirming that targets fall within specified m/z and RT windows.
- TARDIS createTargetList() function executes without errors and returns a TARDIS-compatible target list object ready for peak detection.

## Limitations

- File conversion to .mzML using MSConvert is required and may be time-consuming for large datasets; vendor-specific metadata may be lost during conversion.
- Polarity filtering is performed within TARDIS after target list creation, so ensure polarity values in the target list exactly match the pos_pattern and neg_pattern parameters you provide; mismatches will cause targets to be silently excluded.
- Empty spectra filtering within TARDIS can produce sawtooth profiles in data with multiple overlapping m/z scan windows; inspect EICs during screening mode to detect and address this artifact.
- The validation step does not verify the accuracy or biological relevance of the target compound list — it only checks structural requirements and data types.

## Evidence

- [intro] File conversion requirement: "Input files need to be converted to the .mzML format and have to be centroided"
- [intro] Target data.frame column requirements: "Following columns at least need to be present for each compound: A compound ID, a unique identifier, A compound Name, Theoretical or measured *m/z*, Expected RT (in minutes), A column that indicates"
- [intro] Polarity filtering location and parameter names: "the patterns for positive and negative ionization, the polarity of interest, the columnn that contains the ionization mode"
- [intro] Screening mode verification step: "First, we perform a screening step to check if our targets are visible within our *m/z* and RT windows"
- [other] createTargetList() function parameters and output: "The createTargetList() function accepts parameters including file path, pos_pattern and neg_pattern for ionization modes, polarity selection, ion_column name, and columns_of_interest list (id, name,"
- [intro] MSConvert prerequisite for centroiding: "For file conversion using MSConvert (ProteoWizard)"
- [intro] Empty spectra filtering artifact: "you will notice that peaks will have a sawtooth profile, because of the filtering of empty spectra within TARDIS"
