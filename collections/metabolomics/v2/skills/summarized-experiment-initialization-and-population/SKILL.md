---
name: summarized-experiment-initialization-and-population
description: Use when when beginning a metabolomics analysis workflow in maplet, you have raw or preprocessed metabolomics data (assay measurements) and associated sample metadata (colData) or feature annotations (rowData), and you need to create a single, unified container that will hold data, intermediate.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3891
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - SummarizedExperiment
  - magrittr
  - maplet
derived_from:
- doi: 10.1093/bioinformatics/btab741/6409851
  title: maplet
evidence_spans:
- maplet is an R package
- The toolbox builds upon the bioconductor package SummarizedExperiment (SE)
- maplet is designed to work with a pipe operator - either the popular %>% operator from the magrittr package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_maplet_cq
    doi: 10.1093/bioinformatics/btab741/6409851
    title: maplet
  dedup_kept_from: coll_maplet_cq
schema_version: 0.2.0
---

# summarized-experiment-initialization-and-population

## Summary

Initialize and populate a SummarizedExperiment container with metabolomics data and metadata to serve as the central repository for a maplet analysis pipeline. This skill establishes the foundational data structure that enables modular, reproducible chaining of downstream analysis steps.

## When to use

When beginning a metabolomics analysis workflow in maplet, you have raw or preprocessed metabolomics data (assay measurements) and associated sample metadata (colData) or feature annotations (rowData), and you need to create a single, unified container that will hold data, intermediate analysis results, and outputs throughout the pipeline.

## When NOT to use

- Your metabolomics data is already loaded in an existing SummarizedExperiment object and you only need to add or modify a subset of metadata.
- You are working with non-metabolomics data (e.g., genomics, proteomics) that does not align with maplet's metabolomics-specific design.
- Your pipeline does not require unified metadata tracking or modular function chaining.

## Inputs

- Raw or preprocessed metabolomics assay data (intensity matrix: features × samples)
- Sample metadata (colData: sample-level annotations)
- Feature annotations (rowData: metabolite identifiers, chemical properties)

## Outputs

- SummarizedExperiment object initialized and populated with assay, colData, and rowData slots

## How to apply

Load your metabolomics data using maplet's data-loading functions, which initialize a SummarizedExperiment (SE) object by populating assay slots with quantified metabolite intensities, colData with sample-level metadata, and rowData with feature-level annotations. The SE container is constructed to accept subsequent maplet functions (annotation, statistical analysis, visualization, reporting) via pipe operators (either %>% from magrittr or |> from base R), enabling seamless chaining without temporary variables. Verify that the SE object correctly contains dimensions matching your input data and that metadata is properly aligned to rows (features) and columns (samples) before proceeding to downstream pipeline steps.

## Related tools

- **SummarizedExperiment** (Central container class that stores assay data, sample metadata (colData), and feature annotations (rowData) for the maplet pipeline.) — https://bioconductor.org/packages/release/bioc/vignettes/SummarizedExperiment/inst/doc/SummarizedExperiment.html
- **maplet** (Provides data-loading functions to initialize and populate SummarizedExperiment objects with metabolomics data.) — https://github.com/krumsieklab/maplet
- **magrittr** (Enables pipe operator (%>%) for seamless chaining of maplet functions that operate on the populated SummarizedExperiment object.) — https://magrittr.tidyverse.org/

## Examples

```
# Load metabolomics data and initialize SummarizedExperiment
se <- maplet::load_metabolomics_data(intensity_matrix, sample_metadata, feature_annotations) %>% maplet::annotate_features()
```

## Evaluation signals

- The SummarizedExperiment object is successfully created without errors.
- Assay matrix dimensions match input data: rows equal number of features, columns equal number of samples.
- colData rows correspond 1:1 with assay columns (samples); rowData rows correspond 1:1 with assay rows (features).
- The SE object can be piped directly into downstream maplet functions without loss of metadata or assay data.
- saveRDS() successfully serializes the populated SE object for later retrieval and reproducibility.

## Limitations

- SummarizedExperiment initialization requires careful alignment of feature and sample dimensions; mismatched row/column counts will cause pipeline errors.
- maplet's data-loading functions are optimized for metabolomics datasets; non-metabolomics data may require manual SE construction.
- The README notes that maplet is in active development and commits without release tags are not guaranteed to be stable.

## Evidence

- [readme] Central repository role: "SummarizedExperiment (SE), which serves as a central repository for each pipeline's data, analysis steps, and results."
- [intro] Data-loading function purpose: "maplet provides a suite of functions for interacting with this container including but not limited to data loading, annotation, statistical analysis, visualization, and reporting."
- [readme] Pipe operator integration: "This operator allows for smooth connections between pipeline steps, without the need for temporary variables or multiple assignments."
- [readme] Self-contained pipeline architecture: "It allows users to create self-contained analytical pipelines."
