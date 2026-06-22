---
name: r-workflow-scripting-for-analytical-chemistry
description: Use when you have raw CE-MS or LC-MS instrument files (stored as OnDiskMSnExp objects or similar Bioconductor containers) and need to extract quantitative features (migration times, m/z values, peak intensities) by orchestrating multiple R packages in a controlled, documented sequence.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - R
  - MobilityTransformR
  - msdata
  - MetaboCoreUtils
  - xcms
  - MSnbase
  - Spectra
  techniques:
  - LC-MS
  - CE-MS
derived_from:
- doi: 10.1093/bioinformatics/btac441
  title: MobilityTransformR
evidence_spans:
- there is no implementation in R that performs effective mobility transformation of CE-MS(/MS) data
- Description and usage of MobilityTransformR
- compute Procaine's effective mobility using mobilityTransform
- The CE-MS test data are from the `r BiocStyle::Biocpkg("msdata")` package
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("MetaboCoreUtils")`
- The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("xcms")`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mobilitytransformr_cq
    doi: 10.1093/bioinformatics/btac441
    title: MobilityTransformR
  dedup_kept_from: coll_mobilitytransformr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac441
  all_source_dois:
  - 10.1093/bioinformatics/btac441
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# R workflow scripting for analytical chemistry

## Summary

Construct multi-step R pipelines that chain specialized analytical chemistry packages (xcms, MSnbase, Spectra, MetaboCoreUtils) to process raw mass spectrometry or capillary electrophoresis–mass spectrometry data through signal detection, peak picking, and feature extraction. This skill is essential when raw instrumental data must be transformed into standardized, reproducible feature tables for downstream chemometric or metabolomic analysis.

## When to use

Apply this skill when you have raw CE-MS or LC-MS instrument files (stored as OnDiskMSnExp objects or similar Bioconductor containers) and need to extract quantitative features (migration times, m/z values, peak intensities) by orchestrating multiple R packages in a controlled, documented sequence. Specifically use it when you must combine ion extraction (via Extracted Ion Electropherogram generation), peak detection (via xcms::findChromPeaks), parameter tuning, and structured output—tasks that require scripting rather than point-and-click tools.

## When NOT to use

- Input is already a preprocessed feature table or peak matrix—this skill is for raw data processing, not table-level transformation.
- The analytical chemistry workflow requires custom or proprietary vendor software incompatible with open-source R ecosystems (e.g., instrument-specific binary formats without open parsers).
- Only point-and-click visualization or summary statistics are needed; scripting overhead is unjustified for one-off exploratory plots.

## Inputs

- Raw CE-MS or LC-MS data files (in mzML, mzXML, or netCDF format)
- OnDiskMSnExp object or equivalent Bioconductor container
- Chemical marker definitions (m/z range, expected migration time or retention time window)
- Peak-finding algorithm parameters (centWave bandwidth, noise threshold, signal-to-noise ratio cutoff)

## Outputs

- Per-file feature table (CSV or data frame) with file identifiers, marker names, extracted migration times, m/z values, and peak intensities
- Extracted Ion Electropherogram (EIE) plots or numerical traces
- Structured output file containing both positive and negative effective mobilities (if applicable)
- R workspace (.RData) or Bioconductor object preserving intermediate results for quality control

## How to apply

Structure the workflow in discrete, parameterized steps: (1) Load raw MS data files into R using MSnbase or Spectra, wrapping them in OnDiskMSnExp objects for memory efficiency. (2) Define chemical markers (e.g., EOF markers in CE-MS) by their m/z range and expected migration time window. (3) Generate an Extracted Ion Electropherogram (EIE) for each marker using narrow m/z tolerance and migration time range filters to isolate the peak of interest. (4) Apply xcms::findChromPeaks with appropriate algorithm parameters (typically centWave or matchedFilter) to detect and quantify the marker peak. (5) Compile results into a per-file table with file identifiers, marker identities, and extracted features (migration time, intensity, area). (6) Export the final feature table in a structured format (CSV, RData, or HDF5) for downstream statistical or metabolomic analysis. Document each parameter choice (mz tolerance, chromatographic peak-finding settings) in comments or a configuration file, as narrow ranges are required for correct peak detection.

## Related tools

- **xcms** (Detects and quantifies peaks in Extracted Ion Electropherograms using findChromPeaks algorithm)
- **MSnbase** (Provides infrastructure for loading and manipulating raw MS data as OnDiskMSnExp objects)
- **Spectra** (Modern backend for MS spectrum representation and manipulation in Bioconductor workflows)
- **MetaboCoreUtils** (Supplies utility functions for effective mobility transformation and feature table operations in CE-MS pipelines)
- **MobilityTransformR** (Wraps core transformation logic for CE-MS effective mobility; called within R scripts for EOF marker extraction and scale normalization) — https://github.com/LiesaSalzer/MobilityTransformR
- **msdata** (Provides example CE-MS and LC-MS test files for pipeline validation and reproducible workflow development)

## Examples

```
library(MobilityTransformR); library(msdata); data_files <- dir(system.file('lcms', package='msdata'), full.names=TRUE)[1:2]; mse <- readMSData(data_files, mode='onDisk'); mt_table <- getMtime(mse, mz=c(120.0, 122.0), mt_range=c(50, 150)); write.csv(mt_table, 'extracted_migration_times.csv', row.names=FALSE)
```

## Evaluation signals

- Per-file feature table contains no missing values for core columns (file_id, marker_name, migration_time, m/z, intensity) and all rows correspond to detected peaks above the configured signal-to-noise ratio threshold.
- Extracted migration times or effective mobilities fall within the user-specified range windows and show expected stability (low coefficient of variation across replicate injections if available).
- Extracted Ion Electropherogram plots display isolated, single-peak regions for each marker, confirming that mz tolerance and migration time filters were sufficiently narrow.
- Output file schema matches the declared format (number of columns, data types, row counts) and can be reimported without parsing errors.
- xcms::findChromPeaks algorithm reports non-zero peak counts for all input files and marker ranges; zero-count files indicate misconfigured parameters or genuine signal absence requiring investigation.

## Limitations

- Effective mobility transformation for CE-MS data is more complex than for CE-UV and requires careful parameter tuning; narrow mz and migration time ranges are mandatory to ensure correct peak detection, and suboptimal ranges lead to false or missed peaks.
- Electroosmotic flow variations cause migration time fluctuations within the same electrophoretic system, requiring either effective mobility normalization (via EOF marker extraction) or per-run calibration for reproducibility.
- Memory overhead grows with raw data file size; OnDiskMSnExp objects mitigate this but still require sufficient RAM for metadata and intermediate EIE traces during peak picking.
- No R implementation for effective mobility transformation existed before MobilityTransformR, so workflows built on this skill require adoption of or interface to this package; alternative CE-MS pipelines (e.g., ROMANCE software) produce separate output files for positive and negative mobilities, complicating cross-platform comparisons.

## Evidence

- [other] The getMtime() function accepts an OnDiskMSnExp object, mz-range, and MT-range as inputs and determines the migration time of a marker peak by generating an Extracted Ion Electropherogram (EIE) and using findChromPeaks from xcms to pick the peak, with narrow mz and mt ranges required to ensure correct peak detection.: "The getMtime() function accepts an OnDiskMSnExp object, mz-range, and MT-range as inputs and determines the migration time of a marker peak by generating an Extracted Ion Electropherogram (EIE) and"
- [intro] The transformation is performed using functionality from the packages MetaboCoreUtils, xcms, MSnbase, and Spectra.: "The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("MetaboCoreUtils")`, `r BiocStyle::Biocpkg("xcms")`, `r BiocStyle::Biocpkg("MSnbase")`, and `r"
- [intro] there is no implementation in R that performs effective mobility transformation of CE-MS(/MS) data: "there is no implementation in R that performs effective mobility transformation of CE-MS(/MS) data"
- [intro] the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT: "the effective mobility µ_eff of a compound remains stable in the same electrophoretic system. The use of an effective mobility scale instead of a migration time scale circumvents the drawback of MT"
- [readme] To install MobilityTransformR, use the stable version available at Bioconductor. Enter: if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager"); BiocManager::install("MobilityTransformR"): "To install MobilityTransformR, use the stable version available at Bioconductor. Enter: if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager");"
