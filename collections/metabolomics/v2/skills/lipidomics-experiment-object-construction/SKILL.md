---
name: lipidomics-experiment-object-construction
description: Use when when you have lipidomics quantitation data (lipid abundances across samples) that you need to load into a unified, annotated R object for analysis—either from public Metabolomics Workbench studies via API, Skyline mass spectrometry software exports, or a custom numerical matrix with.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0091
  tools:
  - lipidr
  - R
  - limma
  - Metabolomics Workbench API
  - SummarizedExperiment
  - Skyline
derived_from:
- doi: 10.1021/acs.jproteome.0c00082
  title: lipidr
evidence_spans:
- Datasets can be easily downloaded and parsed into `LipidomicsExperiment` object using `lipidr` function `fetch_mw_study()`
- '`lipidr` allows users, to quickly explore public lipidomics experiments. `lipidr` provides an easy way to re-analyze and visualize these datasets.'
- Data Mining and Analysis of Lipidomics Datasets in R
- This step of the workflow requires the `limma` package to be installed.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidr_cq
    doi: 10.1021/acs.jproteome.0c00082
    title: lipidr
  dedup_kept_from: coll_lipidr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.0c00082
  all_source_dois:
  - 10.1021/acs.jproteome.0c00082
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipidomics-experiment-object-construction

## Summary

Construct a LipidomicsExperiment object in R by parsing lipidomics data from Metabolomics Workbench API, Skyline CSV exports, or numerical matrices, combined with sample annotations. This object serves as the foundational data structure for downstream quality control, multivariate analysis, and differential expression workflows in lipidr.

## When to use

When you have lipidomics quantitation data (lipid abundances across samples) that you need to load into a unified, annotated R object for analysis—either from public Metabolomics Workbench studies via API, Skyline mass spectrometry software exports, or a custom numerical matrix with clinical metadata.

## When NOT to use

- Input is already a parsed LipidomicsExperiment or SummarizedExperiment object—proceed directly to quality control or analysis.
- Sample names in the quantitation table and annotation file do not match exactly; resolve naming inconsistencies first.
- Lipid names in the input do not follow supported naming conventions (e.g., 'Cer (', 'PC (', 'TG (') and cannot be standardized via regex—consider renaming or filtering before object construction.

## Inputs

- Metabolomics Workbench study identifier (STUDY_ID string, e.g. 'ST001111')
- Skyline CSV export (columns: lipid names, samples as columns, intensity/area values)
- Numerical data matrix (CSV/table: lipids as rows, samples as columns, first row = sample names)
- Sample annotation/clinical metadata table (CSV: sample names in first column, matching quantitation table exactly)

## Outputs

- LipidomicsExperiment object (S4 object extending SummarizedExperiment, containing assays, rowData, colData)
- Parsing warnings identifying unparsed molecules with unsupported naming patterns

## How to apply

There are three primary input pathways, each producing a LipidomicsExperiment object: (1) For Metabolomics Workbench studies, use fetch_mw_study('STUDY_ID') to download and parse the dataset directly; (2) For Skyline CSV exports, use read_skyline('export.csv') to parse the quantitation table; (3) For numerical matrices, use as_lipidomics_experiment(read.csv('matrix.csv')) to convert the table where lipids are rows and samples are columns. In all cases, attach sample-level clinical annotations using add_sample_annotation(d, 'metadata.csv'), ensuring sample names match exactly between the quantitation table and annotation file. Set the logged and normalized status using set_logged() and set_normalized() functions to track data transformations. The resulting LipidomicsExperiment extends SummarizedExperiment, enabling integration with Bioconductor packages and serving as input to downstream lipidr functions (mva, de_analysis, de_design).

## Related tools

- **lipidr** (Primary R package providing fetch_mw_study(), read_skyline(), as_lipidomics_experiment(), add_sample_annotation(), set_logged(), and set_normalized() functions for LipidomicsExperiment construction and annotation.) — https://github.com/ahmohamed/lipidr
- **Metabolomics Workbench API** (Web service queried by lipidr's fetch_mw_study() to download public lipidomics studies and their metadata.)
- **SummarizedExperiment** (Bioconductor base class that LipidomicsExperiment extends, providing standardized assay, rowData, and colData slots.) — http://bioconductor.org/packages/SummarizedExperiment/
- **Skyline** (Mass spectrometry data processing software whose CSV exports (quantitation tables) are parsed directly by lipidr's read_skyline() function.)
- **R** (Programming language and runtime environment in which lipidr operates.)

## Examples

```
library(lipidr)
d <- fetch_mw_study('ST001111')
d <- set_logged(d, 'Area', TRUE)
d <- set_normalized(d, 'Area', TRUE)
```

## Evaluation signals

- Object class and structure: verify object is of class 'LipidomicsExperiment' and extends 'SummarizedExperiment' using class(d) and str(d)
- Assay slot population: confirm quantitation data (Area, Height, etc.) is present in assays(d) with dimensions matching input (lipids × samples)
- Row metadata: verify lipid names and parsed lipid class/chain information are in rowData(d) without excessive NA or unparsed entries
- Column metadata: confirm sample annotations (SampleType, Stage, Race, etc.) are in colData(d) with dimensions matching sample count
- Logging status: check set_logged(d, 'Area') and set_normalized(d, 'Area') return TRUE when those transformations have been applied
- Parsing warnings reviewed: examine console output from construction for warnings about unsupported lipid naming patterns; confirm unparsed molecules are either renamed via regex or removed

## Limitations

- Metabolomics Workbench API requires active internet connection and current study availability; if study is removed or access is restricted, fetch_mw_study() will fail.
- Skyline CSV exports require exact export format and column structure; deviations (e.g., missing molecule name column, unexpected delimiters) will cause read_skyline() parsing to fail.
- Sample name matching between quantitation and annotation tables is case-sensitive and must be exact; even leading/trailing whitespace will cause misalignment.
- Unsupported lipid naming patterns (e.g., full chemical names, non-standard abbreviations) will be flagged as unparsed and must be manually corrected using regex substitution (as shown in task_001) or removed to proceed with analysis.
- Numerical matrix input requires first row to be sample names and first column to be lipid names; any deviation from this structure will cause as_lipidomics_experiment() to parse incorrectly.

## Evidence

- [intro] Datasets can be easily downloaded and parsed into LipidomicsExperiment object using lipidr function fetch_mw_study() by supplying a study_id.: "Datasets can be easily downloaded and parsed into LipidomicsExperiment object using lipidr function fetch_mw_study() by supplying a study_id."
- [readme] lipidr represents lipidomics datasets as a LipidomicsExperiment, which extends SummarizedExperiment, to facilitate integration with other Bioconductor packages.: "lipidr represents lipidomics datasets as a LipidomicsExperiment, which extends SummarizedExperiment, to facilitate integration with other Bioconductor packages."
- [readme] lipidr can convert these 2 files to LipidomicsExperiment as follows: d <- as_lipidomics_experiment(read.csv("data_matrix.csv")); d <- add_sample_annotation(d, "data_clin.csv"): "d <- as_lipidomics_experiment(read.csv("data_matrix.csv"))
d <- add_sample_annotation(d, "data_clin.csv")"
- [readme] In lipidr: d <- read_skyline("Skyline_export.csv"); d <- add_sample_annotation(d, "data_clin.csv"): "d <- read_skyline("Skyline_export.csv")
d <- add_sample_annotation(d, "data_clin.csv")"
- [intro] Update and correct molecule names that do not follow supported patterns; setting logged and normalized status for data using set_logged() and set_normalized(): "d <- set_logged(d, "Area", TRUE)
d <- set_normalized(d, "Area", TRUE)"
- [intro] Note the warning that some molecules were not parsed because their names did not follow the supported patterns.: "Note the warning that some molecules were not parsed because their names did not follow the supported patterns."
- [intro] lipidr takes exported Skyline CSV as input, allowing for multiple methods to be analyzed together.: "lipidr takes exported Skyline CSV as input, allowing for multiple methods to be analyzed together."
- [intro] Through integration with Metabolomics Workbench API, lipidr allows users to quickly explore public lipidomics experiments.: "Through integration with Metabolomics Workbench API, lipidr allows users to quickly explore public lipidomics experiments."
