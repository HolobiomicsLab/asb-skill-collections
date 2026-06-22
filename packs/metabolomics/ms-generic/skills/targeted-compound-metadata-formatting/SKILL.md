---
name: targeted-compound-metadata-formatting
description: Use when you have a raw list of target compounds (in .xlsx, CSV, or database form) with heterogeneous column names and layouts, and you need to prepare it for targeted peak detection, EIC extraction, or quality metric calculation in TARDIS or similar LC–MS metabolomics tools.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# targeted-compound-metadata-formatting

## Summary

Construct a standardized data.frame of targeted compound metadata (ID, name, m/z, RT, polarity) from raw source files (e.g., .xlsx targets list) for use as input to targeted peak detection workflows in LC–MS. This skill ensures that compound descriptors meet the schema and content requirements of downstream analysis tools like TARDIS.

## When to use

You have a raw list of target compounds (in .xlsx, CSV, or database form) with heterogeneous column names and layouts, and you need to prepare it for targeted peak detection, EIC extraction, or quality metric calculation in TARDIS or similar LC–MS metabolomics tools. Apply this skill before performing screening-mode validation or full peak detection runs.

## When NOT to use

- Input is already a validated TARDIS target list object or a previously formatted peak detection input.
- Target list contains only one ionization mode and no polarity filtering is needed.
- You are performing exploratory, non-targeted metabolomics (discovery mode) rather than targeted compound screening.

## Inputs

- raw target file (.xlsx, .csv, or data.frame) with compound metadata
- ionization mode specification (positive or negative pattern)
- column name mapping or specification

## Outputs

- TARDIS-compatible target data.frame with columns: ID, Name, m/z, RT, Polarity
- filtered and formatted compound metadata object ready for peak detection

## How to apply

Load the target compound file into R as a data.frame. Filter rows to retain only compounds matching your ionization mode of interest (positive or negative polarity) by applying the appropriate pos_pattern or neg_pattern regex to the ionization-mode column. Extract and rename columns to match the required TARDIS schema: a unique compound ID, a compound Name, Theoretical or measured m/z, Expected RT in minutes, and a Polarity column. Pass the resulting formatted data.frame to createTargetList() with the selected polarity parameter. Validate that all required columns are present and non-null, and that m/z and RT values are numeric and within expected ranges for your method.

## Related tools

- **TARDIS** (accepts formatted target list data.frame and performs targeted peak integration and quality metric calculation) — https://github.com/pablovgd/TARDIS
- **R** (environment for loading, filtering, and transforming target file into data.frame)

## Examples

```
target_data <- read.xlsx('targets.xlsx'); target_data_pos <- target_data[target_data$ionization_mode == 'positive', ]; target_list <- createTargetList(file='targets.xlsx', pos_pattern='positive', neg_pattern='negative', polarity='positive', ion_column='ionization_mode', columns_of_interest=c('id', 'name', 'mz', 'rt'))
```

## Evaluation signals

- Output data.frame contains exactly the required columns (ID, Name, m/z, RT, Polarity) with no NAs in critical fields.
- All m/z values are numeric, positive, and within expected mass range for your instrument; all RT values are numeric and in minutes.
- Polarity column contains only the selected ionization mode(s); no rows from opposite polarity remain.
- TARDIS createTargetList() function accepts the output without schema or type errors.
- Row count matches expected number of target compounds for the selected polarity after filtering.

## Limitations

- The skill does not validate that m/z or RT values are chemically or chromatographically plausible—only that they are numeric and non-null.
- Polarity filtering relies on correct regex patterns (pos_pattern, neg_pattern) in the ionization-mode column; incorrect or ambiguous patterns may result in silent mis-filtering.
- No automatic handling of duplicate compound IDs or names; users must resolve ambiguities before passing to TARDIS.
- If the raw file is missing required columns entirely, no fallback or imputation is performed; the workflow will fail downstream.

## Evidence

- [intro] Column specification requirement: "Following columns at least need to be present for each compound: A compound ID, a unique identifier, A compound Name, Theoretical or measured *m/z*, Expected RT (in minutes), A column that indicates"
- [intro] Polarity filtering mechanism: "the patterns for positive and negative ionization, the polarity of interest, the columnn that contains the ionization mode"
- [other] createTargetList function input and output: "The createTargetList() function accepts parameters including file path, pos_pattern and neg_pattern for ionization modes, polarity selection, ion_column name, and columns_of_interest list (id, name,"
- [other] Workflow for positive-polarity filtering: "1. Load the targets.xlsx file into R as a data.frame. 2. Filter rows to retain only positive-polarity compounds. 3. Extract and retain the required columns: compound ID, compound name,"
- [intro] TARDIS polarity handling: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
