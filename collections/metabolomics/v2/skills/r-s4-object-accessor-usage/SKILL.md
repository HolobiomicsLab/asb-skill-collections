---
name: r-s4-object-accessor-usage
description: Use when you have constructed or received a SummarizedExperiment object
  (or similar S4 class) containing MS feature tables, counts matrices, or sample-level
  metadata, and need to retrieve specific slots (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3437
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - SummarizedExperiment
  - mzrtsim
  techniques:
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c01213
  title: mzrtsim
evidence_spans:
- if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
  BiocManager::install("mzrtsim")
- For seamless integration with Bioconductor workflows, use `mzrtsim_se()` which wraps
  the simulation in a `SummarizedExperiment`
- github.com__yufree__mzrtsim
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzrtsim_cq
    doi: 10.1021/acs.analchem.5c01213
    title: mzrtsim
  dedup_kept_from: coll_mzrtsim_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01213
  all_source_dois:
  - 10.1021/acs.analchem.5c01213
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# R S4 Object Accessor Usage

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Access and extract data from S4 objects (particularly SummarizedExperiment) using standard Bioconductor accessor functions like assay() and colData(). This skill enables standardized, type-safe retrieval of counts matrices, sample metadata, and assay annotations from complex biological data structures.

## When to use

You have constructed or received a SummarizedExperiment object (or similar S4 class) containing MS feature tables, counts matrices, or sample-level metadata, and need to retrieve specific slots (e.g., abundance data, sample annotations, experimental design) in a way that respects Bioconductor conventions and maintains object integrity.

## When NOT to use

- Input is a base R data.frame or matrix—use standard subsetting ([, ]) instead.
- You need to modify object structure—use replacement accessors (assay()<- , colData()<-) rather than this extraction skill.
- S4 object does not define accessor methods (check class definition or slot names); direct @ slot access may be necessary.

## Inputs

- SummarizedExperiment object
- S4 object with defined accessor methods

## Outputs

- counts matrix (numeric, rows=features, cols=samples)
- colData DataFrame (sample metadata with condition/batch assignments)
- rowData DataFrame (feature annotations)
- assay(type) results (generic matrix or array)

## How to apply

After instantiating a SummarizedExperiment object (e.g., via mzrtsim_se()), use accessor functions to retrieve data rather than direct slot access (@ operator). Call SummarizedExperiment::assay() to extract the counts matrix, SummarizedExperiment::colData() to retrieve sample-level metadata including condition and batch labels, and other specialized accessors (e.g., rowData()) for feature-level annotations. Verify that returned objects match expected dimensions and data types—e.g., assay() returns a matrix with features as rows and samples as columns; colData() returns a DataFrame with sample identifiers as row names and experimental variables (condition, batch) as columns.

## Related tools

- **SummarizedExperiment** (S4 class providing assay(), colData(), and rowData() accessor methods for storing and retrieving counts, sample metadata, and feature annotations) — https://bioconductor.org/packages/SummarizedExperiment
- **mzrtsim** (Generates SummarizedExperiment objects via mzrtsim_se() wrapping simulated LC/GC-MS peak tables with condition and batch effects) — https://github.com/yufree/mzrtsim
- **R** (Runtime environment for S4 object instantiation and accessor method invocation)

## Examples

```
library(SummarizedExperiment); se <- mzrtsim_se(); counts_mat <- assay(se); sample_md <- colData(se)
```

## Evaluation signals

- assay() returns a numeric matrix with non-zero dimensions matching the number of features and samples in the object.
- colData() returns a DataFrame with row names equal to sample identifiers and columns including condition and batch variables.
- Accessor calls do not raise 'slot not found' or 'method not defined' errors.
- Retrieved count values and metadata are consistent with simulation parameters (e.g., expected condition contrasts visible in abundance patterns).
- Object structure remains intact after accessor calls—no unintended side effects or data corruption.

## Limitations

- Accessor methods are class-specific; SummarizedExperiment accessors will not work on other S4 classes without similar method definitions.
- Accessor functions return references or shallow copies depending on implementation; modifying returned objects may or may not affect the parent S4 object.
- Large SummarizedExperiment objects (e.g., many samples or features) may consume significant memory when fully materialized via assay().

## Evidence

- [other] mzrtsim_se() produces a SummarizedExperiment object containing a 'counts' assay and colData that can be accessed via standard Bioconductor accessors such as SummarizedExperiment::assay() and SummarizedExperiment::colData().: "mzrtsim_se() produces a SummarizedExperiment object containing a 'counts' assay and colData that can be accessed via standard Bioconductor accessors such as SummarizedExperiment::assay() and"
- [other] Verify that the resulting object exposes counts via the assay() accessor and colData via the colData() accessor per Bioconductor conventions.: "Verify that the resulting object exposes counts via the assay() accessor and colData via the colData() accessor per Bioconductor conventions."
- [intro] For seamless integration with Bioconductor workflows, use `mzrtsim_se()` which wraps the simulation in a `SummarizedExperiment`: "For seamless integration with Bioconductor workflows, use `mzrtsim_se()` which wraps the simulation in a `SummarizedExperiment`"
- [other] Construct column metadata (colData) from simulation parameters including sample identifiers, condition assignments, and batch labels.: "Construct column metadata (colData) from simulation parameters including sample identifiers, condition assignments, and batch labels."
