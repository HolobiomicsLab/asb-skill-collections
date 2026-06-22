---
name: mass-spectrometry-target-list-preparation
description: Use when you have a raw .xlsx or tabular file listing candidate compounds with theoretical or measured m/z values, expected retention times, and ionization polarities, and you need to feed this into TARDIS or another targeted LC–MS analysis pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3674
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0629
  tools:
  - TARDIS
  - R
  techniques:
  - mass-spectrometry
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00567
  all_source_dois:
  - 10.1021/acs.analchem.5c00567
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-target-list-preparation

## Summary

Preparation of a TARDIS-compatible target list by loading a compound spreadsheet, filtering by ionization polarity, and extracting required metadata columns (ID, name, m/z, RT) into a standardized data.frame. This is the prerequisite step that enables targeted peak detection and integration in LC–MS metabolomics workflows.

## When to use

You have a raw .xlsx or tabular file listing candidate compounds with theoretical or measured m/z values, expected retention times, and ionization polarities, and you need to feed this into TARDIS or another targeted LC–MS analysis pipeline. Specifically, use this skill when you are preparing to perform screening-mode peak detection to check if targets are visible within your m/z and RT windows before full-batch analysis.

## When NOT to use

- Input is already a curated, single-polarity TARDIS target list object—skip to screening mode directly.
- You lack retention time information or theoretical m/z values—TARDIS requires both RT and m/z for peak detection window definition.
- Ionization mode information is not present or cannot be reliably parsed from the input file—polarity subsetting cannot be performed accurately.

## Inputs

- Raw .xlsx or CSV target file with columns: compound ID, compound name, m/z (theoretical or measured), retention time (minutes), and ionization polarity indicator

## Outputs

- TARDIS-compatible target list data.frame or object with standardized columns (ID, name, m/z, RT) and single-polarity filtering applied

## How to apply

Load the targets spreadsheet into R as a data.frame. Identify the column containing ionization mode information (e.g., positive/negative polarity) and apply the appropriate pos_pattern and neg_pattern regular expressions to filter rows to a single polarity of interest. Extract and retain exactly four required columns: a unique compound ID, a compound name, theoretical or measured m/z value, and expected RT in minutes. Pass the filtered and subset data.frame to the TARDIS createTargetList() function with the selected polarity parameters to generate a TARDIS-compatible target list object. Polarity filtering is performed within TARDIS itself, so this step ensures the input is clean and properly formatted before screening-mode validation.

## Related tools

- **TARDIS** (Accepts the prepared target list data.frame and uses it to define m/z and RT windows for targeted peak detection and integration in LC–MS data) — https://github.com/pablovgd/TARDIS
- **R** (Language and environment for loading, filtering, and formatting the target spreadsheet into a TARDIS-compatible data.frame using base and tidyverse functions)

## Examples

```
target_list <- createTargetList(file = 'targets.xlsx', pos_pattern = 'positive|pos|\\+', neg_pattern = 'negative|neg|-', polarity = 'positive', ion_column = 'ionization_mode', columns_of_interest = c('id', 'name', 'mz', 'rt'))
```

## Evaluation signals

- The output data.frame contains exactly four columns in the correct order (ID, name, m/z, RT) with no missing values.
- All rows in the output correspond to a single, consistent ionization polarity (all positive or all negative); verify by inspecting the polarity column before subsetting.
- m/z values are numeric and within the expected range for your mass spectrometer (e.g., 50–2000 m/z); RT values are numeric and in minutes with realistic ranges (e.g., 0–30 min).
- The data.frame passes TARDIS's internal schema validation when passed to createTargetList(); no warnings about missing or malformed columns are raised.
- Row count is consistent with the number of target compounds selected after polarity filtering; spot-check a few rows to confirm ID, name, m/z, and RT are populated correctly.

## Limitations

- If ionization mode patterns (pos_pattern, neg_pattern) do not match the nomenclature in your input file, polarity filtering will fail silently or retain wrong rows; inspect the raw file to confirm pattern syntax.
- TARDIS requires retention times to be in minutes; if your input uses seconds or other units, manual conversion is required before createTargetList().
- Multiple ionization adducts or isotopes for the same compound are not automatically resolved; if your input lists m/z for [M+H]+, [M+Na]+, and [M+K]+ separately, these must be treated as separate rows or manually consolidated.
- No changelog or version control for the target list is built into this preparation step; tracking changes to compound definitions, m/z values, or RT windows requires external documentation.

## Evidence

- [intro] requirement_for_input_columns: "Following columns at least need to be present for each compound: A compound ID, a unique identifier, A compound Name, Theoretical or measured *m/z*, Expected RT (in minutes), A column that indicates"
- [other] function_and_parameters: "The createTargetList() function accepts parameters including file path, pos_pattern and neg_pattern for ionization modes, polarity selection, ion_column name, and columns_of_interest list (id, name,"
- [intro] polarity_filtering_location: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [other] output_compatibility: "producing a formatted data.frame compatible with TARDIS peak detection"
- [intro] screening_mode_context: "First, we perform a screening step to check if our targets are visible within our *m/z* and RT windows"
