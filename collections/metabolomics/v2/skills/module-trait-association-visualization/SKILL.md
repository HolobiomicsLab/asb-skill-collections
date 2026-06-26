---
name: module-trait-association-visualization
description: Use when after identifying and naming metabolic correlation modules from
  WGCNA on normalized, imputed metabolomic data, and you need to assess whether specific
  modules associate significantly with a binary or categorical sample trait (e.g.,
  disease status, treatment group).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MetaboDiff
  - R
  - WGCNA
  - MultiAssayExperiment
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/bty344
  title: MetaboDiff
- doi: 10.1158/0008-5472.can-14-1490
  title: ''
evidence_spans:
- '`MetaboDiff` is available for all operating systems and can be installed via Github'
- met = knn_impute(met,cutoff=0.4)
- The `MetaboDiff` R package requires R version 4.0.2 or higher.
- The `MetaboDiff` R package requires R version 4.0.2 or higher
- install.packages("WGCNA")
- The core concept of the so called "weighted" correlation analysis by Langfelder
  and Horvarth
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodiff_cq
    doi: 10.1093/bioinformatics/bty344
    title: MetaboDiff
  dedup_kept_from: coll_metabodiff_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/bty344
  all_source_dois:
  - 10.1093/bioinformatics/bty344
  - 10.1158/0008-5472.can-14-1490
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# module-trait-association-visualization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Visualizes statistical associations between metabolic correlation modules and sample groupings (e.g., tumor vs. normal) using module significance (MS) metrics. This skill enables identification of which metabolic modules show significant trait-dependent abundance patterns, facilitating biological interpretation of network-derived modules.

## When to use

After identifying and naming metabolic correlation modules from WGCNA on normalized, imputed metabolomic data, and you need to assess whether specific modules associate significantly with a binary or categorical sample trait (e.g., disease status, treatment group). Apply this skill when the research question targets module-level, not individual metabolite, associations with phenotype.

## When NOT to use

- Input metabolomic data is not yet normalized or imputed; preprocess with variance stabilizing normalization (vsn) and k-nearest neighbor imputation first.
- Metabolic modules have not been identified or assigned; run WGCNA with dynamic branch cutting (minimum module size ≥5 metabolites) before trait association.
- Sample grouping variable is continuous; use correlation-based module-trait association (e.g., module eigenvector vs. quantitative trait) instead.

## Inputs

- Preprocessed MultiAssayExperiment object with normalized and imputed metabolite measurements
- Identified metabolic correlation modules (WGCNA output with named module assignments)
- Sample metadata with binary or categorical grouping variable (e.g., tumor_normal, treatment status)
- Module eigenmetabolites (computed via prior WGCNA steps)

## Outputs

- Module significance (MS) statistics table with p-values, effect sizes, and adjusted p-values per module
- MS_plot visualization showing module-trait associations with significance threshold overlay
- Intermediate metabolite significance values (per-metabolite contribution to module significance)
- Direction of effect annotation (higher/lower abundance in each trait group)

## How to apply

Execute the calculate_MS function on a preprocessed MultiAssayExperiment object with the group_factor parameter set to the sample trait of interest (e.g., 'tumor_normal'). This computes module significance as the average absolute metabolite significance per module. Generate an MS_plot with the same group_factor, a p-value cutoff (typically 0.05), and specify p_adjust parameter to control multiple testing correction (Benjamini-Hochberg recommended). Extract p-values and effect direction (e.g., higher abundance in normal group) for each module. Validate that intermediate metabolite significance values and module eigenmetabolite calculations match expected output by comparing against raw correlation matrices and sample metadata.

## Related tools

- **MetaboDiff** (Provides calculate_MS and MS_plot functions for computing and visualizing module significance statistics and module-trait associations in metabolomic data) — https://github.com/andreasmock/MetaboDiff
- **WGCNA** (Prerequisite tool for generating metabolic correlation modules and module eigenmetabolites required as input to calculate_MS)
- **MultiAssayExperiment** (Data container object that merges assay (metabolite measurements), rowData (metabolite annotations), and colData (sample metadata) into unified structure for downstream analysis)
- **R** (Programming environment for executing MetaboDiff functions; requires version 4.0.2 or higher)

## Examples

```
calculate_MS(met, group_factor="tumor_normal"); MS_plot(met, group_factor="tumor_normal", p_value_cutoff=0.05, p_adjust=FALSE)
```

## Evaluation signals

- Module significance p-values are computed for all modules; values < 0.05 indicate statistically significant module-trait associations at the specified alpha level.
- MS_plot displays modules ranked by significance with horizontal p-value threshold line at 0.05 (or adjusted cutoff); modules above the line are significant.
- Extracted effect direction (sign and magnitude) is consistent with the underlying module eigenmetabolite-to-trait correlation direction.
- Intermediate metabolite significance values sum (or average) correctly to reported module significance; spot-check against raw metabolite-trait associations.
- Multiple testing-corrected p-values (when p_adjust=TRUE using Benjamini-Hochberg) show expected inflation-correction compared to raw p-values.

## Limitations

- Module significance relies on correctly identified modules; poorly separated clusters or suboptimal branch-cutting parameters propagate into inflated or deflated associations.
- The method aggregates metabolite-level signals into module summaries; individual metabolite outliers or biologically heterogeneous modules may obscure signals.
- Statistical power depends on sample size and trait group balance; small sample sizes or extreme imbalance reduce power to detect module associations.
- Assumes linear or monotonic metabolite-trait relationships; non-linear associations may not be captured by average metabolite significance.
- Module traits are evaluated at p < 0.05 by default; no guidance provided in the article for threshold selection or effect size minimums in small sample contexts.

## Evidence

- [other] MetaboDiff provides module significance calculation functionality for assessing associations between metabolic modules and sample groupings.: "MetaboDiff provides module significance calculation functionality (calculate_MS / MS_plot) for assessing associations between metabolic modules and sample groupings."
- [other] MS calculation computes average absolute metabolite significance per module.: "Execute calculate_MS function on the object with group_factors parameter set to 'tumor_normal' to compute module significance statistics (average absolute metabolite significance per module)."
- [readme] MetaboDiff offers exploration of sample traits in data-derived metabolic correlation networks.: "As a key functionality, MetaboDiffs offers the exploration of sample traits in a data-derived metabolic correlation network."
- [other] MS_plot visualization with p-value cutoff and adjustment options.: "Generate MS_plot with group_factor='tumor_normal', p_value_cutoff=0.05, and p_adjust=FALSE to visualize module-trait associations."
- [other] Module significance p-values < 0.05 indicate significant associations.: "Extract and validate that Module 2 shows p-value < 0.05 and direction of effect (higher abundance in normal group)."
- [methods] Benjamini-Hochberg correction for multiple testing is applied.: "The p-values are corrected for multiple testing by the Benjamini-Hochberg procedure."
- [readme] MetaboDiff enables differential metabolomic analysis from measurement tables.: "The MetaboDiff packages aims to provide a low-level entry to differential metabolomic analysis with R by starting off with the table of metabolite measurements."
