---
name: bioconductor-data-import-and-handling
description: Use when you have CE-MS test files archived in the msdata Bioconductor package and need to load them into an in-memory or on-disk R representation to extract ion electropherograms, pick peaks, or compute effective mobility transformations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - R
  - MobilityTransformR
  - msdata
  - MetaboCoreUtils
  - xcms
  - MSnbase
  - Spectra
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# bioconductor-data-import-and-handling

## Summary

Loading and structuring CE-MS experimental data from Bioconductor packages (msdata) into R objects (OnDiskMSnExp) suitable for downstream mass spectrometry processing and effective mobility transformation. This skill bridges raw mass spectrometry files and analytical workflows by leveraging standardized Bioconductor data containers.

## When to use

You have CE-MS test files archived in the msdata Bioconductor package and need to load them into an in-memory or on-disk R representation to extract ion electropherograms, pick peaks, or compute effective mobility transformations. Specifically, when you need to supply OnDiskMSnExp objects as input to functions like getMtime() that require structured metadata (m/z, migration time, intensity) and parameter specification (mz tolerance, migration time range).

## When NOT to use

- Input data are already in a processed feature matrix or peak table format; data import is not needed.
- CE-UV (capillary electrophoresis–ultraviolet) data, which use simpler effective mobility transformation not requiring the same Bioconductor import pipeline.
- Data are in a non-Bioconductor format (e.g., vendor-specific binary formats) without prior conversion to mzML or netCDF.

## Inputs

- CE-MS raw data files from msdata Bioconductor package
- OnDiskMSnExp object specification (mz-range, migration time range)

## Outputs

- OnDiskMSnExp object (in-memory representation of CE-MS spectra)
- Extracted Ion Electropherogram (EIE)
- Per-file structured table with file identifiers and extracted numeric values (e.g., migration times)

## How to apply

Load CE-MS test data from the msdata package using standard Bioconductor import functions to create OnDiskMSnExp objects. These objects encapsulate raw spectra with associated metadata (file identifiers, scan timing). Specify mz-range and migration time (MT) range parameters narrowly to ensure correct peak detection during downstream extraction and peak-picking with xcms::findChromPeaks. Compile extracted values (e.g., migration times) into per-file tables with file identifiers and numeric MT values for structured export. The choice of narrow parameter ranges is critical: broader ranges risk detecting incorrect peaks or EOF markers.

## Related tools

- **msdata** (Source repository for CE-MS test data files used to populate OnDiskMSnExp objects)
- **MSnbase** (Provides OnDiskMSnExp class and container infrastructure for mass spectrometry data representation)
- **Spectra** (Spectra access and manipulation layer for imported mass spectrometry data)
- **xcms** (Peak detection via findChromPeaks on Extracted Ion Electropherograms derived from imported data)
- **MetaboCoreUtils** (Utility functions for metabolomics data processing during import and transformation workflows)
- **MobilityTransformR** (Downstream package that consumes OnDiskMSnExp objects for effective mobility transformation) — https://github.com/LiesaSalzer/MobilityTransformR

## Examples

```
BiocManager::install("MobilityTransformR"); library(MobilityTransformR); data_files <- dir(system.file("CE-MS", package="msdata"), full.names=TRUE); mt_table <- lapply(data_files, function(f) { ems <- readMSData(f); getMtime(ems, mz=c(200, 210), mt=c(10, 30)) })
```

## Evaluation signals

- OnDiskMSnExp object is successfully instantiated with non-null slots for spectra, metadata, and file paths.
- Per-file migration time table contains one row per input CE-MS file with valid file identifier and numeric MT values (no NA or infinite values).
- Extracted Ion Electropherogram (EIE) generated using getMtime shows a single, well-resolved peak when mz-range and MT-range parameters are sufficiently narrow; broader ranges reveal multiple peaks indicating over-specification.
- Exported structured output file (e.g., CSV or TSV) has consistent schema across rows and columns matching the input file count.
- Round-trip validation: reimporting the exported table and comparing file identifiers and MT values with original extraction shows exact numeric concordance.

## Limitations

- Effective mobility transformation for CE-MS data is more complex than for CE-UV and requires careful specification of mz and migration time ranges to avoid false peak detection.
- No existing R implementation of effective mobility transformation for CE-MS existed before MobilityTransformR, limiting reproducibility of prior workflows.
- Performance may degrade if OnDiskMSnExp objects are very large or if mz/MT range parameters are too broad, leading to ambiguous or multiple peak detections.

## Evidence

- [intro] The CE-MS test data are from the `r BiocStyle::Biocpkg("msdata")` package: "The CE-MS test data are from the `r BiocStyle::Biocpkg("msdata")` package"
- [intro] The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("MSnbase")`: "The transformation is performed using functionality from the packages `r BiocStyle::Biocpkg("MSnbase")`"
- [other] The getMtime() function accepts an OnDiskMSnExp object, mz-range, and MT-range as inputs and determines the migration time of a marker peak by generating an Extracted Ion Electropherogram (EIE) and using findChromPeaks from xcms to pick the peak: "The getMtime() function accepts an OnDiskMSnExp object, mz-range, and MT-range as inputs and determines the migration time of a marker peak by generating an Extracted Ion Electropherogram (EIE) and"
- [other] narrow mz and mt ranges required to ensure correct peak detection: "narrow mz and mt ranges required to ensure correct peak detection"
- [intro] Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility: "Effective mobility transformation for CE-MS data is not as straightforward as in CE-UV and until now and to our knowledge there is no implementation in R that performs effective mobility"
- [readme] To install MobilityTransformR, use the stable version available at Bioconductor. Enter: if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager"); BiocManager::install("MobilityTransformR"): "To install MobilityTransformR, use the stable version available at Bioconductor"
