---
name: metabolomics-data-loading-into-containers
description: Use when you have raw metabolomics data (e.g., in standard bioinformatics formats supported by maplet) and need to initialize an analytical pipeline that will integrate multiple processing and analysis steps.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab741/6409851
  all_source_dois:
  - 10.1093/bioinformatics/btab741/6409851
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-data-loading-into-containers

## Summary

Load raw metabolomics datasets into a SummarizedExperiment container to enable downstream annotation, statistical analysis, visualization, and reporting within a unified, modular pipeline framework. This skill establishes the foundational data structure that supports reproducible and chainable metabolomics workflows.

## When to use

You have raw metabolomics data (e.g., in standard bioinformatics formats supported by maplet) and need to initialize an analytical pipeline that will integrate multiple processing and analysis steps. Use this skill at the start of any metabolomics analysis where you want to maintain data, metadata, and results in a single container that can be piped through downstream functions without temporary variables or multiple assignments.

## When NOT to use

- Your metabolomics data is already in a SummarizedExperiment container—skip directly to annotation or analysis steps.
- You are working with non-metabolomics omics data (e.g., genomics, proteomics) where domain-specific containers may be more appropriate.
- Your workflow requires ad-hoc, temporary variable assignments rather than a unified modular pipeline.

## Inputs

- raw metabolomics dataset (format supported by maplet data-loading functions)
- sample metadata (if separate from main data matrix)

## Outputs

- SummarizedExperiment object initialized with metabolomics data
- R object ready for piping into downstream maplet functions

## How to apply

Use maplet's data-loading function to read your raw metabolomics dataset and instantiate a SummarizedExperiment container. The SummarizedExperiment object will serve as the central repository for your pipeline's data, analysis steps, and results. This container is then passed as input to subsequent maplet functions (annotation, statistical analysis, visualization, reporting) via the %>% pipe operator from magrittr or the |> base R pipe. The modular design ensures that each step operates on the same container, eliminating the need for intermediate variable assignments and enabling a linear, readable workflow that is easy to reproduce and extend.

## Related tools

- **SummarizedExperiment** (Central container object that stores and unifies raw metabolomics data, sample metadata, analysis results, and pipeline steps) — https://bioconductor.org/packages/release/bioc/vignettes/SummarizedExperiment/inst/doc/SummarizedExperiment.html
- **maplet** (Provides data-loading functions and the ecosystem of chainable functions for metabolomics pipeline construction) — https://github.com/krumsieklab/maplet
- **magrittr** (Supplies the %>% pipe operator for connecting loaded data to downstream maplet functions without temporary variables) — https://magrittr.tidyverse.org/

## Examples

```
# Load metabolomics data into SummarizedExperiment
se <- maplet::load_metabolomics_data('raw_metabolomics.csv') %>% maplet::annotate_features()
```

## Evaluation signals

- SummarizedExperiment object is successfully created and contains metabolomics feature matrix in the assay slot
- Sample metadata (if provided) are correctly stored in the SummarizedExperiment's colData slot
- Object can be piped directly to a downstream maplet function (annotation, statistical analysis, etc.) without error or type mismatch
- saveRDS() can serialize the loaded container to disk for reproducibility and sharing
- Dimensions and data integrity are preserved: nrow matches number of metabolite features, ncol matches number of samples

## Limitations

- maplet's data-loading functions support specific metabolomics data formats; unsupported raw formats require preprocessing before loading.
- The SummarizedExperiment container is most effective in pipelines that use maplet functions downstream; mixing with non-maplet functions may require manual data extraction.
- No changelog is publicly available, so version-specific behavior and breaking changes may not be transparently documented.

## Evidence

- [readme] Central repository for metabolomics pipeline data: "SummarizedExperiment (SE), which serves as a central repository for each pipeline's data, analysis steps, and results."
- [intro] maplet data-loading function initiates container: "maplet provides a suite of functions for interacting with this container including but not limited to data loading, annotation, statistical analysis, visualization, and reporting."
- [readme] Pipe operator enables chaining without temporary variables: "This operator allows for smooth connections between pipeline steps, without the need for temporary variables or multiple assignments."
- [readme] Modular and reproducible pipeline construction: "The combination of these elements allows for the creation of pipelines which are simple to follow, highly modular, and easily reproducible."
- [other] maplet workflow initialization step: "Load metabolomics data using maplet's data-loading function and initialize a SummarizedExperiment container."
