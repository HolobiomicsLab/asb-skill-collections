---
name: feature-vector-naming-convention
description: Use when when applying sequential transformations to a metabolomics feature
  intensity table (samples × compounds) and you need to maintain a traceable record
  of original feature identities through each processing stage.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - GetFeatistics
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1515/jib-2025-0047
  title: GetFeatistics
evidence_spans:
- R (version ≥ 4.3.1)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_getfeatistics_cq
    doi: 10.1515/jib-2025-0047
    title: GetFeatistics
  dedup_kept_from: coll_getfeatistics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1515/jib-2025-0047
  all_source_dois:
  - 10.1515/jib-2025-0047
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-vector-naming-convention

## Summary

Establish and track compound feature naming conventions across sequential data transformations in metabolomics workflows. This skill ensures reproducibility and traceability by automatically generating intermediate column name vectors with standardized suffixes that document each transformation step (missing value replacement, log transformation, scaling).

## When to use

When applying sequential transformations to a metabolomics feature intensity table (samples × compounds) and you need to maintain a traceable record of original feature identities through each processing stage. Specifically required when using the transf_data function with missing_replace, log_transf, or scaling options enabled, to automatically preserve and document intermediate column names.

## When NOT to use

- Input is already a fully processed feature table with transformations already applied and original column names are no longer needed
- Workflow requires non-sequential or custom transformation orders not supported by transf_data default pipeline
- Feature names do not require traceability or downstream reference in subsequent statistical models

## Inputs

- Feature intensity table (samples in rows, compounds in columns, numeric values)
- Column names of original features (character vector)
- Transformation parameter configuration (missing_replace: logical, log_transf: logical, scaling: character specifying scale type)
- Naming convention prefixes for intermediate vectors (vect_names_transf and name_vect_names arguments)

## Outputs

- Transformed feature table with compound suffixes (_mr, _mr_ln, _mr_ln_paretosc)
- Named column vectors saved in global environment documenting original feature identities
- Intermediate name vectors with specified prefixes (e.g., name_vect_names_mr, name_vect_names_mr_ln, name_vect_names_mr_ln_paretosc)

## How to apply

The transf_data function applies transformations sequentially and automatically generates naming vectors at each step: (1) missing value replacement produces columns with _mr suffix; (2) log transformation produces _ln suffix; (3) scaling (mean_scale, auto_scale, pareto_scale, or range_scale) produces suffix codes (e.g., paretosc for pareto scaling). Set the vect_names_transf argument to TRUE and specify name_vect_names prefixes to automatically save intermediate column name vectors in the global environment. These vectors document original feature names and their transformed identifiers, enabling downstream functions to correctly reference columns and supporting audit trails of data provenance.

## Related tools

- **GetFeatistics** (Implements transf_data function that applies sequential transformations with automatic naming convention generation and vect_names_transf tracking of intermediate vectors) — https://github.com/FrigerioGianfranco/GetFeatistics
- **R** (Runtime environment for executing transf_data function and managing named vectors in global environment; version ≥ 4.3.1 required)

## Examples

```
# Load feature table and legend; apply transf_data with vect_names_transf=TRUE to generate intermediate naming vectors
library(GetFeatistics)
result <- transf_data(feat_table, missing_replace=TRUE, log_transf=TRUE, scaling='pareto_scale', vect_names_transf=TRUE, name_vect_names='compound')
# Access naming vectors: compound_mr, compound_mr_ln, compound_mr_ln_paretosc in global environment
```

## Evaluation signals

- Verify that output column names contain expected suffixes in correct sequence: _mr (missing replacement), _mr_ln (log-transform applied), _mr_ln_paretosc (Pareto scaling applied)
- Confirm that intermediate name vectors exist in global environment with prefixes specified in name_vect_names argument
- Cross-check that column count at each transformation stage matches expected naming vector length
- Validate that original feature names are recoverable by referencing the most basic name vector (e.g., name_vect_names_mr entries map to original identities)
- Confirm downstream statistical functions can access and correctly reference transformed columns using the tracked naming vectors

## Limitations

- Naming convention only tracks the three sequential transformations (missing replacement, log, scaling) implemented in transf_data; custom or alternative transformation pipelines require manual name management
- Global environment name vector assignments may create namespace collisions if name_vect_names prefixes are not sufficiently unique across multiple transf_data calls
- Pareto scaling suffix ('paretosc') and other scale types use fixed abbreviations; renaming or alternative conventions require modification of transf_data source code

## Evidence

- [other] Sequential transformation suffixes and naming tracking: "Output includes columns with compound suffixes (_mr, _mr_ln, _mr_ln_paretosc) and the vect_names_transf argument automatically saves intermediate column name vectors in the global environment"
- [other] Transformation order and suffix semantics: "The transf_data function applies transformations sequentially: missing values are replaced (suffix _mr), followed by log transformation (suffix _ln), then scaling options including mean_scale,"
- [other] Naming convention purpose and implementation: "Construct and save name vectors documenting the original feature names and their transformed column identifiers for each of the three transformations (_mr, _ln, paretosc)"
- [intro] Data transformation input requirements: "The first should contain the intensities of peak area. Samples in rows, analysed compounds in columns"
