---
name: metabolite-target-list-formatting
description: Use when you have a raw LC–MS compound metadata file (xlsx or csv) with
  heterogeneous column names and column order, and you need to prepare it for targeted
  peak detection in TARDIS.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - xcms
  - R
  - TARDIS
  - Spectra
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.5c00567
  title: tardis
evidence_spans:
- It makes use of an established retention time correction algorithm from the `xcms`
  package
- R package for *TArgeted Raw Data Integration In Spectrometry*
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tardis
    doi: 10.1021/acs.analchem.5c00567
    title: tardis
  dedup_kept_from: coll_tardis
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

# metabolite-target-list-formatting

## Summary

Construct a standardized target data.frame for LC–MS targeted metabolomics by reading compound metadata from xlsx/csv input files, validating required columns (compound ID, name, theoretical m/z, expected RT, polarity indicator), filtering by ionization mode, and reordering columns to match the expected schema for downstream peak detection in TARDIS.

## When to use

You have a raw LC–MS compound metadata file (xlsx or csv) with heterogeneous column names and column order, and you need to prepare it for targeted peak detection in TARDIS. The file must specify at least compound ID, name, m/z value, retention time (in minutes), and a polarity indicator (positive/negative ionization mode), and you intend to screen or detect peaks only for a subset of targets matching a single polarity.

## When NOT to use

- If your input file is already a correctly formatted and polarity-filtered data.frame — skip this step and pass directly to tardisPeaks().
- If your LC–MS analysis is not targeted (e.g., untargeted metabolomics with feature detection) — use an alternative feature extraction workflow such as xcms or other untargeted peak detection.
- If polarity information is missing or inconsistent across your compound list — resolve polarity assignments before attempting to format.

## Inputs

- xlsx or csv file containing compound metadata (compound ID, name, m/z, RT, polarity columns)
- Polarity selection parameter (e.g. 'positive' or 'negative')
- Column name indicating ionization mode (e.g. 'polarity', 'ionization_mode')
- List or vector of column names of interest to include in output

## Outputs

- Filtered and reformatted data.frame with columns: compound ID, compound name, m/z, RT (minutes), polarity
- R data.frame object ready for input to TARDIS tardisPeaks() function

## How to apply

Read the input xlsx or csv file containing compound metadata using R's standard file I/O functions. Validate that required columns are present: compound ID (unique identifier), compound name, theoretical or measured m/z, expected RT in minutes, and a polarity indicator column. Apply polarity filtering by subsetting rows to match the desired ionization mode (positive or negative). Select and reorder columns to conform to the standardized TARDIS target data.frame structure (typically: ID, name, m/z, RT, polarity). Return the filtered and reformatted data.frame as input to TARDIS's screening_mode=TRUE or screening_mode=FALSE peak detection functions. The rationale is that TARDIS performs polarity filtering internally during peak detection, but the target data.frame must be pre-filtered to the relevant polarity and properly ordered so that m/z and RT windows are correctly paired with their corresponding compounds.

## Related tools

- **TARDIS** (Target LC–MS peak detection and quality assessment; accepts the formatted target data.frame to screen and detect peaks in centroided .mzML files) — https://github.com/pablovgd/TARDIS
- **xcms** (Provides retention time correction algorithms used by TARDIS for aligning peaks across multiple LC–MS runs)
- **Spectra** (R package for loading MS data; data can be passed as Spectra objects into TARDIS instead of file paths)
- **R** (Programming language and environment for reading xlsx/csv files, data frame manipulation, and invoking TARDIS functions) — https://cloud.r-project.org/index.html

## Examples

```
library(TARDIS); targets <- createTargetList(input_file = 'compounds.xlsx', ionization_pos = '[M+H]+', ionization_neg = '[M-H]-', polarity = 'positive', polarity_col = 'ionization_mode', col_list = c('compound_ID', 'compound_name', 'mz', 'RT_min', 'ionization_mode'))
```

## Evaluation signals

- The output data.frame has exactly one row per target compound and contains no missing values in required columns (ID, name, m/z, RT, polarity).
- All rows in the output data.frame belong to a single polarity mode (either all 'positive' or all 'negative'); verify with `unique(output_df$polarity)` returns exactly one unique value.
- Column order and naming match the expected TARDIS schema; m/z and RT are numeric and RT values are within a plausible range (typically 0–30 minutes for standard LC).
- Passing the output data.frame to `tardisPeaks(target_list = output_df, screening_mode = TRUE, ...)` completes without column-name or data-type errors.
- EICs generated by tardisPeaks show expected target compounds visible within the specified m/z and RT windows, indicating targets were correctly formatted and paired.

## Limitations

- TARDIS performs polarity filtering internally, but the target data.frame must be pre-filtered to a single polarity for correct operation; mixing polarities will lead to incorrect m/z–RT window pairing.
- Input files must be in xlsx or csv format; other spreadsheet formats (e.g., .xls, .ods) require prior conversion.
- Retention time values must be in minutes; if RT is provided in seconds or other units, manual conversion is required before formatting.
- The function does not impute missing m/z or RT values; any row with missing m/z or RT must be removed or corrected in the input file before formatting.
- No changelog is available for TARDIS; version updates may introduce changes to the expected target data.frame schema without formal notification.

## Evidence

- [intro] compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity: "compound ID, a unique identifier; A compound Name; Theoretical or measured *m/z*; Expected RT (in minutes); A column that indicates the polarity"
- [other] The createTargetList() function accepts an input file path, positive/negative ionization patterns, a polarity selection parameter, the column name indicating ionization mode, and columns of interest; it then produces a correctly structured target data.frame: "The createTargetList() function accepts an input file path, positive/negative ionization patterns, a polarity selection parameter, the column name indicating ionization mode, and columns of interest;"
- [intro] Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed: "Polarity filtering is done within `TARDIS`, so no polarity subsetting has to be performed"
- [other] Apply polarity filtering to subset targets by ionization mode. 4. Select and reorder columns to match the standardized target data.frame structure.: "Apply polarity filtering to subset targets by ionization mode. 4. Select and reorder columns to match the standardized target data.frame structure."
- [readme] Read the vignettes for a tutorial on how to use `TARDIS` Available online: https://pablovgd.github.io/TARDIS/: "Read the vignettes for a tutorial on how to use `TARDIS` Available online: https://pablovgd.github.io/TARDIS/"
