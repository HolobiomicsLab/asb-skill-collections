---
name: targeted-feature-extraction-from-lcms
description: Use when you have a curated target list of m/z values, retention times, and identifiers for specific metabolites of interest, and you want to extract only those features from LC-MS data (mzML or netCDF format) rather than performing untargeted feature discovery.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3637
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - JPA
  - R
  - XCMS
derived_from:
- doi: 10.3390/metabo12030212
  title: JPA
evidence_spans:
- JPA is a comprehensive and integrated metabolomics data processing software.
- JPA is a comprehensive and integrated metabolomics data processing software
- '''JPA'' is written in R and its source code is publicly available'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_jpa_cq
    doi: 10.3390/metabo12030212
    title: JPA
  dedup_kept_from: coll_jpa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12030212
  all_source_dois:
  - 10.3390/metabo12030212
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# targeted-feature-extraction-from-lcms

## Summary

Extract metabolic features from LC-MS data by matching detected m/z and retention time peaks against a user-supplied target list with specified mass and temporal tolerances. This skill is used when you have a predefined set of metabolite targets and need to retrieve their intensity values across multiple samples.

## When to use

You have a curated target list of m/z values, retention times, and identifiers for specific metabolites of interest, and you want to extract only those features from LC-MS data (mzML or netCDF format) rather than performing untargeted feature discovery. This is appropriate for hypothesis-driven metabolomics studies where you monitor a known set of compounds across a cohort.

## When NOT to use

- You are performing untargeted metabolomics and want to discover all metabolic features without a predefined list — use MS1 peak picking or MS2 recognition instead.
- Your input is already an aligned feature table from another tool — targeted extraction is designed for raw LC-MS data.
- You are processing full-scan or DIA (data-independent acquisition) datasets without precursor m/z and retention time data.

## Inputs

- Raw LC-MS data files (mzML or netCDF format)
- User-supplied target list (CSV or tabular format with m/z, retention time, and optional identifiers)

## Outputs

- Feature table (CSV or tabular format with rows=features, columns=samples/measurements and m/z, retention time, intensity values)
- Compiled extracted features matching the target list

## How to apply

Load raw LC-MS data (mzML or netCDF) and a target list (containing m/z, retention time, and optional identifiers) into the JPA R package. Apply the targeted-list extraction module to match features in the LC-MS data against targets within user-defined m/z and retention time tolerances (e.g., ±10 ppm for m/z, ±60 seconds for retention time). The module returns features that fall within these windows and compiles them into a feature table with rows as features and columns as samples, m/z, retention time, and intensity values. The extracted feature table can then be exported as CSV for downstream statistical analysis.

## Related tools

- **JPA** (R package that implements the targeted-list extraction module to match LC-MS features against user-supplied targets and compile extracted feature tables) — https://github.com/HuanLab/JPA.git
- **R** (Programming language and environment for running JPA and executing the targeted extraction workflow)
- **XCMS** (Embedded within JPA for preprocessing and feature alignment prior to targeted extraction) — https://rdrr.io/bioc/xcms/man/

## Evaluation signals

- Feature table contains only m/z and retention time values that fall within the specified tolerances of the supplied target list.
- Number of extracted features matches or is less than the number of targets (some targets may not be detected in all samples).
- Feature table columns include sample identifiers, m/z, retention time, and intensity values with no missing required fields.
- Intensity values are non-negative and within the expected range for the LC-MS instrument used.
- CSV export is valid and can be loaded without parsing errors into downstream analysis tools.

## Limitations

- Extracted features are only returned if they fall within user-defined m/z and retention time tolerances; targets outside those windows will not be detected.
- The skill requires accurate m/z and retention time values in the target list; errors in the target list will lead to missed or incorrectly matched features.
- Isobaric or near-isobaric compounds may be conflated if they co-elute or fall within the retention time tolerance window.
- Do not use this function when processing full-scan or DIA datasets as noted in the JPA documentation.

## Evidence

- [other] How does the JPA targeted-list extraction module identify and extract metabolic features that match a user-supplied target list from LC-MS data?: "JPA targeted-list extraction module identify and extract metabolic features that match a user-supplied target list from LC-MS data"
- [other] Apply the JPA targeted-list extraction module to match features in the LC-MS data against the target list, retrieving features within specified m/z and retention time tolerances.: "Apply the JPA targeted-list extraction module to match features in the LC-MS data against the target list, retrieving features within specified m/z and retention time tolerances"
- [other] Compile extracted features into a feature table (rows = features, columns = samples/measurements and m/z, retention time, intensity values).: "Compile extracted features into a feature table (rows = features, columns = samples/measurements and m/z, retention time, intensity values)"
- [readme] Part 4: Extracting features using a targeted list: "Part 4: Extracting features using a targeted list"
- [readme] JPA is a comprehensive and integrated metabolomics data processing software. It extract both Gaussian and non-Gaussian shaped metabolic features. It also performs sample alignment, adduct and metabolite annotations.: "JPA is a comprehensive and integrated metabolomics data processing software. It extract both Gaussian and non-Gaussian shaped metabolic features"
