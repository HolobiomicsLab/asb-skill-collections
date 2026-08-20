---
name: metabolic-module-significance-calculation
description: 'Use when after you have constructed metabolic correlation modules via
  WGCNA on normalized and imputed metabolomic data, and you want to test whether specific
  modules (e.g., Module 2: Creatine/Glutathione metabolism) associate significantly
  with a categorical sample trait.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0885
  - http://edamontology.org/topic_3172
  tools:
  - MetaboDiff
  - R
  - WGCNA
  - MultiAssayExperiment
  license_tier: restricted
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

# metabolic-module-significance-calculation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Calculates module significance (MS) statistics to assess whether metabolic correlation modules show statistically significant associations with sample groupings (e.g., tumor vs. normal). This skill quantifies the average absolute metabolite significance per module and tests for differential module-trait relationships in preprocessed metabolomic data.

## When to use

Apply this skill after you have constructed metabolic correlation modules via WGCNA on normalized and imputed metabolomic data, and you want to test whether specific modules (e.g., Module 2: Creatine/Glutathione metabolism) associate significantly with a categorical sample trait. Use it when you need to go beyond individual metabolite associations to module-level statistical significance with p-values and effect direction.

## When NOT to use

- Metabolomic data has not yet been normalized (vsn) and imputed (knn with cutoff ≥ 0.4) — perform preprocessing first.
- Metabolic modules have not yet been identified via WGCNA — construct modules before calculating module significance.
- Sample grouping variable is continuous rather than categorical — MS is designed for discrete trait groupings.

## Inputs

- MultiAssayExperiment object with normalized metabolite measurements
- Metabolite rowData containing module assignments from prior WGCNA
- Sample colData with categorical trait annotation (e.g., tumor_normal grouping)

## Outputs

- Module significance (MS) statistics per module and trait
- P-values and effect estimates for module-trait associations
- MS_plot visualization of module-trait associations
- Metabolite significance values (average absolute per module)
- Module eigenmetabolite values

## How to apply

Load a MultiAssayExperiment object containing preprocessed metabolomic data (normalized via variance stabilizing normalization, imputed via k-nearest neighbor with cutoff ≥ 0.4, outliers removed) and metabolic modules identified from prior WGCNA steps with named module assignments in the rowData. Execute the calculate_MS function with the group_factors parameter set to the trait of interest (e.g., 'tumor_normal') to compute average absolute metabolite significance per module. Generate an MS_plot with the same group_factor, p_value_cutoff=0.05, and p_adjust=FALSE to visualize module-trait associations. Extract modules meeting p < 0.05 significance threshold and verify the direction of effect (e.g., higher or lower abundance in the specified group). Validate intermediate metabolite significance values and module eigenmetabolite calculations against expected output to confirm correctness.

## Related tools

- **MetaboDiff** (Primary package providing calculate_MS and MS_plot functions for module significance computation and visualization) — https://github.com/andreasmock/MetaboDiff
- **WGCNA** (Prerequisite tool for constructing metabolic correlation modules prior to significance calculation)
- **MultiAssayExperiment** (Data structure housing normalized assay data, rowData (module assignments), and colData (sample traits))
- **R** (Execution environment (≥4.0.2 required) for MetaboDiff functions)

## Examples

```
met_ms <- calculate_MS(mae_object, group_factors='tumor_normal'); MS_plot(met_ms, group_factor='tumor_normal', p_value_cutoff=0.05, p_adjust=FALSE)
```

## Evaluation signals

- Module significance p-values are correctly computed and meet or exceed the specified p_value_cutoff (e.g., p < 0.05 for modules of interest).
- MS_plot visualization shows modules color-coded by significance level and grouped by sample trait, with effect directions (e.g., 'higher in normal') readable.
- Extracted intermediate metabolite significance values (average absolute per module) are non-negative and consistent with individual metabolite-trait associations.
- Module eigenmetabolite calculations (first principal component of module metabolites) match expected output and are correlated with sample trait grouping.
- Benjamini-Hochberg multiple testing correction is applied when p_adjust=TRUE, reducing p-values monotonically without dropping below uncorrected values.

## Limitations

- Module significance depends on the quality of prior WGCNA module construction; poorly defined modules will yield unreliable significance estimates.
- The MS metric averages metabolite significance across the module, which may mask heterogeneity in individual metabolite-trait associations within the module.
- Minimum module size filtering (default ≥ 5 metabolites) may exclude small but biologically important modules from significance testing.
- Multiple testing correction (Benjamini-Hochberg) is recommended but optional; failing to apply it increases false discovery rate when testing many modules.

## Evidence

- [methods] Module significance calculation validates Module 2 association with tumor vs. normal grouping: "Execute calculate_MS function on the object with group_factors parameter set to 'tumor_normal' to compute module significance statistics (average absolute metabolite significance per module)."
- [methods] Output visualization confirms module-trait associations with p-value filtering: "Generate MS_plot with group_factor='tumor_normal', p_value_cutoff=0.05, and p_adjust=FALSE to visualize module-trait associations."
- [intro] MetaboDiff provides core module significance functionality: "As a key functionality, MetaboDiffs offers the exploration of sample traits in a data-derived metabolic correlation network."
- [methods] Validation includes intermediate metabolite and eigenmetabolite values: "Verify intermediate metabolite significance values and module eigenmetabolite calculations match expected output."
- [methods] Biweight midcorrelation and dynamic branch cutting underpin module construction: "Biweight midcorrelation was used as a similiarity measure as it is more robust to outliers than the absolute correlation coefficient"
