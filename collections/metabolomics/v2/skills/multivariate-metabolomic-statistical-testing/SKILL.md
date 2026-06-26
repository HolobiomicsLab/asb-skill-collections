---
name: multivariate-metabolomic-statistical-testing
description: Use when after WGCNA-derived metabolic modules have been identified and
  named in a normalized, imputed MultiAssayExperiment object, and you need to test
  whether specific modules show statistically significant association with a binary
  or categorical sample grouping (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0639
  - http://edamontology.org/topic_3172
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

# Multivariate Metabolomic Statistical Testing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute module significance (MS) statistics to assess associations between metabolic correlation modules and sample groupings (e.g., tumor vs. normal) using averaged absolute metabolite significance per module. This skill enables detection of statistically significant metabolic modules linked to phenotypic traits in preprocessed metabolomic data.

## When to use

Apply this skill after WGCNA-derived metabolic modules have been identified and named in a normalized, imputed MultiAssayExperiment object, and you need to test whether specific modules show statistically significant association with a binary or categorical sample grouping (e.g., tumor vs. normal tissue, disease vs. control). Use when the research question asks: 'Does this metabolic module significantly correlate with the sample phenotype?'

## When NOT to use

- Metabolic modules have not yet been identified (run WGCNA with dynamic branch cutting first).
- Data has not been normalized and imputed; missing values or batch effects will invalidate MS calculations.
- Sample grouping column is not present or is continuous rather than categorical—module significance is designed for discrete trait associations.

## Inputs

- Normalized and imputed MultiAssayExperiment object
- Identified and named metabolic correlation modules from prior WGCNA analysis
- Sample phenotype grouping column (e.g., 'tumor_normal' factor)

## Outputs

- Module significance (MS) statistics with p-values per module
- MS_plot visualization of module-trait associations
- Filtered list of significant modules (p < 0.05)
- Direction and magnitude of module effect per phenotype group

## How to apply

Execute the `calculate_MS` function on the preprocessed MultiAssayExperiment object with the `group_factors` parameter set to the column name defining your sample grouping (e.g., 'tumor_normal'). This computes the average absolute metabolite significance per module, where metabolite significance is the correlation between individual metabolite abundance and the sample trait. Then generate an `MS_plot` with the same `group_factor`, set `p_value_cutoff=0.05`, and `p_adjust=FALSE` (or apply Benjamini-Hochberg correction if multiple testing correction is desired) to visualize module-trait associations. Extract p-values for each module; modules with p < 0.05 are considered significantly associated with the phenotype. Verify intermediate calculations by inspecting metabolite significance values and module eigenmetabolite values to confirm they match expected behavior (e.g., direction of effect consistent with biological hypothesis).

## Related tools

- **MetaboDiff** (Provides calculate_MS and MS_plot functions for computing and visualizing module significance statistics in metabolomic data) — https://github.com/andreasmock/MetaboDiff
- **WGCNA** (Upstream tool for identifying metabolic correlation modules via hierarchical clustering and dynamic branch cutting that serve as input to module significance calculation)
- **MultiAssayExperiment** (Container object format for storing assay (metabolite abundance), rowData (metabolite annotation), and colData (sample phenotypes) required by MetaboDiff functions)
- **R** (Programming language and runtime for executing MetaboDiff workflows and statistical calculations)

## Examples

```
calculate_MS(mae, group_factors='tumor_normal'); MS_plot(mae, group_factor='tumor_normal', p_value_cutoff=0.05, p_adjust=FALSE)
```

## Evaluation signals

- Module significance p-values are in the range [0, 1] and are reported for all identified modules.
- Modules with p < 0.05 show consistent direction of effect (e.g., higher average metabolite abundance in one phenotype group vs. the other) aligned with biological hypothesis.
- Intermediate metabolite significance values (per-metabolite correlation with trait) and module eigenmetabolite values are numerically consistent and reproducible across re-runs.
- MS_plot legend and color scheme correctly reflect the group_factor grouping and p-value threshold applied.
- Number and identity of significant modules remain stable when p_adjust is toggled (Benjamini-Hochberg correction should reduce false positives but not eliminate true signals).

## Limitations

- Module significance assumes modules have already been robustly identified; quality of MS depends on upstream WGCNA module assignments and parameter choices (e.g., dynamic branch cutting threshold, minimum module size).
- MS metric is based on average absolute metabolite significance, which may mask heterogeneity within modules; if only a subset of metabolites drive the association, average-based metrics may underestimate or dilute the signal.
- Statistical testing does not account for metabolite co-measurement error or inter-module correlations; modules with overlapping metabolite sets may show spurious or inflated significance.
- Multiple testing correction (Benjamini-Hochberg) can be applied but is not automatic; researchers must decide whether to apply it based on the number of modules being tested.

## Evidence

- [methods] Module significance calculation functionality: "MetaboDiff provides module significance calculation functionality (calculate_MS / MS_plot) for assessing associations between metabolic modules and sample groupings."
- [methods] MS metric definition: "execute calculate_MS function on the object with group_factors parameter set to 'tumor_normal' to compute module significance statistics (average absolute metabolite significance per module)"
- [methods] Visualization and interpretation: "Generate MS_plot with group_factor='tumor_normal', p_value_cutoff=0.05, and p_adjust=FALSE to visualize module-trait associations"
- [methods] Validation approach: "Extract and validate that Module 2 shows p-value < 0.05 and direction of effect (higher abundance in normal group). Verify intermediate metabolite significance values and module eigenmetabolite"
- [readme] MetaboDiff core functionality: "As a key functionality, MetaboDiffs offers the exploration of sample traits in a data-derived metabolic correlation network."
- [methods] Multiple testing correction procedure: "The p-values are corrected for multiple testing by the Benjamini-Hochberg procedure."
