---
name: r-pipe-operator-chaining
description: Use when when you have a metabolomics dataset loaded into a SummarizedExperiment and need to apply a sequence of analysis steps (data loading, annotation, statistical analysis, visualization, reporting) in a reproducible, self-contained pipeline where each function's output becomes the next.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0335
  edam_topics:
  - http://edamontology.org/topic_0541
  - http://edamontology.org/topic_3172
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

# r-pipe-operator-chaining

## Summary

Chain multiple R functions together using pipe operators (magrittr %>% or base R |>) to construct linear, modular analysis pipelines without requiring intermediate variable assignments. This technique is particularly effective for metabolomics workflows where data, analysis steps, and results flow through a SummarizedExperiment container.

## When to use

When you have a metabolomics dataset loaded into a SummarizedExperiment and need to apply a sequence of analysis steps (data loading, annotation, statistical analysis, visualization, reporting) in a reproducible, self-contained pipeline where each function's output becomes the next function's input.

## When NOT to use

- When you need to inspect or manipulate intermediate results for debugging—linear pipes make it harder to access intermediate objects without refactoring
- When pipeline steps have complex conditional logic or branching paths that cannot be linearly chained
- When the analysis workflow requires parallel execution or step independence

## Inputs

- SummarizedExperiment object (initialized with metabolomics data)
- Metabolomics dataset (loaded via maplet data-loading function)

## Outputs

- SummarizedExperiment object (with pipeline steps and results embedded)
- RDS file (serialized SummarizedExperiment)

## How to apply

Initialize a SummarizedExperiment container with metabolomics data using maplet's data-loading function. Chain subsequent maplet functions (e.g., annotation, statistical analysis, visualization) by connecting them with the %>% operator from magrittr or the |> operator from base R. Each pipe operator passes the SummarizedExperiment object from one function to the next as the first argument, eliminating the need for intermediate variable assignments. Execute the complete chained pipeline script in R as a single logical unit. Save the final SummarizedExperiment object using saveRDS() to preserve the entire pipeline state and results.

## Related tools

- **maplet** (Provides functions for data loading, annotation, statistical analysis, visualization, and reporting that are chained via pipe operators to build modular metabolomics pipelines) — https://github.com/krumsieklab/maplet
- **magrittr** (Provides the %>% pipe operator for chaining function calls) — https://magrittr.tidyverse.org/
- **SummarizedExperiment** (Bioconductor package that serves as the central container for pipeline data, analysis steps, and results that flows through the pipe chain) — https://bioconductor.org/packages/release/bioc/vignettes/SummarizedExperiment/inst/doc/SummarizedExperiment.html
- **R** (Programming language runtime for executing the pipe-chained pipeline)

## Examples

```
se %>% mp_load_metabolomics_data() %>% mp_annotate_compounds() %>% mp_statistical_analysis() %>% mp_visualize() %>% mp_generate_report() -> final_se; saveRDS(final_se, 'pipeline_result.rds')
```

## Evaluation signals

- The final SummarizedExperiment object is successfully saved as an RDS file with no intermediate variable assignments in the pipeline code
- Each function in the chain accepts a SummarizedExperiment as input and returns a SummarizedExperiment (no type mismatch errors at pipe junctions)
- The pipeline script reads linearly from top to bottom without temporary assignments (se <- func1(se); se <- func2(se) anti-pattern is absent)
- Results embedded in the final SummarizedExperiment reflect the cumulative effect of all chained steps (e.g., annotations, statistics, and visualizations are all present)
- The chained pipeline runs without errors and produces identical results to a manually-written equivalent using intermediate assignments

## Limitations

- Pipe operators make intermediate debugging difficult—you must refactor the pipeline to extract intermediate results for inspection
- The %>% operator from magrittr requires an additional package dependency; base R's |> (R 4.1+) is native but may not be available in older R installations
- Complex conditional branching or multi-path workflows are not naturally expressed in linear pipe chains and may require restructuring into multiple separate pipelines or custom wrapper functions
- maplet is in active development; commits without a release tag are not guaranteed to be stable

## Evidence

- [intro] Chain functions via pipe operators: "maplet pipelines operate by chaining functions via pipe operators (either %>% from magrittr or |> from base R) that connect pipeline steps without requiring temporary variables or multiple"
- [readme] Data flow through SummarizedExperiment: "SummarizedExperiment (SE), which serves as a central repository for each pipeline's data, analysis steps, and results."
- [readme] maplet provides functions for multiple workflow steps: "maplet provides a suite of functions for interacting with this container including but not limited to data loading, annotation, statistical analysis, visualization, and reporting."
- [readme] Pipelines are simple to follow and modular: "The combination of these elements allows for the creation of pipelines which are simple to follow, highly modular, and easily reproducible."
- [readme] Pipe operators eliminate temporary variables: "This operator allows for smooth connections between pipeline steps, without the need for temporary variables or multiple assignments."
