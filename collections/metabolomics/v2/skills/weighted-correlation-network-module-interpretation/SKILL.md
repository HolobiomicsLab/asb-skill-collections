---
name: weighted-correlation-network-module-interpretation
description: Use when after WGCNA has identified and named metabolic correlation modules from preprocessed, normalized, and imputed metabolomic data, and you need to test whether specific modules show statistically significant association with a known sample grouping (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - MetaboDiff
  - R
  - WGCNA
  - MultiAssayExperiment
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
- The core concept of the so called "weighted" correlation analysis by Langfelder and Horvarth
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
---

# Weighted-Correlation-Network Module Interpretation

## Summary

Interpret metabolic correlation network modules by associating co-regulated metabolite clusters with sample phenotypes (e.g., tumor vs. normal) using module significance (MS) statistics. This skill enables discovery of functionally coherent metabolic signatures linked to disease state or experimental conditions.

## When to use

Apply this skill after WGCNA has identified and named metabolic correlation modules from preprocessed, normalized, and imputed metabolomic data, and you need to test whether specific modules show statistically significant association with a known sample grouping (e.g., tumor-versus-normal classification, treatment response). Use it when you want to move beyond individual metabolite significance to assess coordinated metabolite set behavior.

## When NOT to use

- Input lacks pre-computed metabolic correlation modules—conduct WGCNA network analysis first.
- Sample phenotype metadata is unavailable or incompletely annotated; the grouping factor must be present in colData.
- Individual metabolite-level statistics are sufficient for your biological question; module interpretation adds complexity without interpretive benefit.

## Inputs

- Normalized and imputed MultiAssayExperiment object with identified and named metabolic correlation modules
- Module membership assignments (output from WGCNA dynamic branch cutting)
- Sample phenotype metadata with grouping factor (e.g., 'tumor_normal' column)

## Outputs

- Module significance (MS) statistics: p-values and mean absolute metabolite significance per module
- MS_plot: visualization of module-trait associations with p-value thresholds
- Module-level association report: direction and magnitude of effect per module

## How to apply

Load a preprocessed MultiAssayExperiment object containing identified metabolic modules (from prior WGCNA steps), metabolite measurements, and sample phenotype annotations. Execute the calculate_MS function with the group_factors parameter set to the phenotype of interest (e.g., 'tumor_normal') to compute module significance: the average absolute metabolite significance per module. Generate an MS_plot with matching group_factor, p_value_cutoff=0.05, and p_adjust=FALSE to visualize module-trait associations and identify modules with p < 0.05. Inspect intermediate calculations—metabolite significance values and module eigenmetabolite vectors—to confirm they match expected output and validate the direction of effect (e.g., higher abundance in normal group). Use Benjamini-Hochberg correction if adjusting across multiple comparisons.

## Related tools

- **MetaboDiff** (Provides calculate_MS function and MS_plot visualization for computing and displaying module significance statistics and module-trait associations) — https://github.com/andreasmock/MetaboDiff
- **WGCNA** (Upstream tool for constructing metabolic correlation networks, detecting modules via dynamic branch cutting, and computing module eigenmetabolites)
- **MultiAssayExperiment** (Data container that merges metabolite assays, row metadata (metabolite annotations), and column metadata (sample phenotypes) for streamlined downstream analysis)
- **R** (Runtime environment for executing MetaboDiff, WGCNA, and statistical workflows; requires version 4.0.2 or higher)

## Examples

```
calculate_MS(mae, group_factors='tumor_normal'); MS_plot(mae, group_factor='tumor_normal', p_value_cutoff=0.05, p_adjust=FALSE)
```

## Evaluation signals

- Module significance p-values are computed and reported for each module; at least one module achieves p < 0.05 when true association exists.
- MS_plot displays modules ranked by significance with clear visualization of p-value threshold and direction of phenotype association.
- Intermediate metabolite significance values (per-metabolite association with grouping factor) and module eigenmetabolite vectors are extractable and recalculate correctly from raw data.
- Modules with low p-values show consistent direction of effect (e.g., higher metabolite abundance in normal samples) across constituent metabolites.
- Multiple-testing-corrected p-values (Benjamini-Hochberg) do not contradict unadjusted results; adjusted cutoff remains conservative.

## Limitations

- Module significance relies on mean-field averaging of metabolite significance; rare metabolites with extreme values can skew module-level statistics.
- Biweight midcorrelation, used for network construction, is robust to outliers but may mask genuine biological signals in rare metabolites.
- Minimum module size (default 5 metabolites) may exclude small, functionally important co-regulated clusters.
- Module interpretation is associative, not causal; significant association with phenotype does not imply mechanistic role or therapeutic target status.

## Evidence

- [methods] Module significance calculation and visualization: "Execute calculate_MS function on the object with group_factors parameter set to 'tumor_normal' to compute module significance statistics (average absolute metabolite significance per module)"
- [methods] Visualization and statistical thresholds: "Generate MS_plot with group_factor='tumor_normal', p_value_cutoff=0.05, and p_adjust=FALSE to visualize module-trait associations"
- [methods] Input data container structure: "The function `create_mae` merges all objects into a so called `MultiAssayExperiment` object to simplify all downstream analysis"
- [readme] Metabolic correlation network exploration: "As a key functionality, MetaboDiffs offers the exploration of sample traits in a data-derived metabolic correlation network"
- [methods] Multiple testing correction method: "The p-values are corrected for multiple testing by the Benjamini-Hochberg procedure"
