---
name: eigenmetabolite-direction-of-effect-validation
description: Use when after computing module significance (MS) statistics for metabolic
  modules against a sample grouping factor (e.g., tumor vs. normal), and detecting
  a statistically significant module association (p < 0.05).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0769
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

# Eigenmetabolite Direction-of-Effect Validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validates the biological directionality of metabolic module associations by verifying that module eigenmetabolite values and constituent metabolite abundances show concordant directional effects (e.g., higher in normal vs. tumor samples). This confirms that module significance associations reflect genuine metabolic shifts rather than statistical artifacts.

## When to use

After computing module significance (MS) statistics for metabolic modules against a sample grouping factor (e.g., tumor vs. normal), and detecting a statistically significant module association (p < 0.05). Use this skill to confirm that the direction and magnitude of the eigenmetabolite effect aligns with the biological hypothesis and intermediate metabolite significance values before reporting module-trait associations.

## When NOT to use

- Module significance p-value ≥ 0.05 (association not statistically significant; no direction to validate)
- Single metabolite analysis (eigenmetabolite validation applies only to correlation-derived modules with multiple members)
- Unnormalized or unimputed data (direction of effect cannot be reliably determined without preprocessing)

## Inputs

- Preprocessed MultiAssayExperiment object with normalized and imputed metabolomic data
- Identified metabolic correlation modules from WGCNA (module eigenvectors and member metabolite identities)
- Sample grouping factor (e.g., 'tumor_normal' column in colData)
- Module significance statistics (p-values, effect sizes) from calculate_MS function

## Outputs

- Validated module-trait association with confirmed directional effect
- MS_plot visualization showing eigenmetabolite distribution by group
- Intermediate metabolite significance values per module member
- Validation report confirming concordance between module and constituent metabolite directions

## How to apply

Extract the eigenmetabolite (first principal component) values for the module of interest from the module eigenvector computed during WGCNA. Stratify eigenmetabolite values by the sample grouping factor and verify the direction of effect (e.g., mean eigenmetabolite abundance in normal samples > tumor samples, or vice versa). Compute average absolute metabolite significance (MS metric) for individual metabolites within the module to ensure constituent metabolites show concordant directional shifts. Use the MS_plot visualization with the grouping factor to inspect effect direction graphically. Compare intermediate metabolite significance values against the module-level p-value and effect direction to confirm internal consistency. If eigenmetabolite direction contradicts the biological hypothesis or constituent metabolite directions are discordant, re-examine module composition, outliers, or normalization parameters before validation.

## Related tools

- **MetaboDiff** (Provides calculate_MS function to compute module significance statistics and MS_plot for visualizing eigenmetabolite distributions by sample grouping; offers quality_plot and downstream statistical reporting.) — https://github.com/andreasmock/MetaboDiff
- **WGCNA** (Computes module eigenvectors and metabolite-to-module assignments used in eigenmetabolite extraction and direction validation.)
- **MultiAssayExperiment** (Stores normalized/imputed metabolomic assay data, row metadata (metabolite annotations), and column metadata (sample grouping factors) required for eigenmetabolite and significance calculations.)

## Examples

```
calculate_MS(mae, group_factors='tumor_normal'); MS_plot(mae, group_factor='tumor_normal', p_value_cutoff=0.05, p_adjust=FALSE)
```

## Evaluation signals

- Eigenmetabolite mean values show consistent directional separation between sample groups (e.g., normal > tumor or vice versa, with minimal overlap in distributions)
- Individual metabolite significance values within the module show concordant directionality with the module-level eigenmetabolite effect (constituent metabolites shift in the same direction)
- Module significance p-value < 0.05 and effect size (absolute metabolite significance) matches the magnitude of directional shift visualized in MS_plot
- Eigenmetabolite calculations (first principal component of module members) reproduce expected values when recomputed from raw normalized metabolite abundances
- No inversion or contradiction between MS_plot effect direction and biological hypothesis (e.g., if tumor samples are expected to show metabolic stress, eigenmetabolite should reflect expected pathway dysregulation)

## Limitations

- Eigenmetabolite direction depends on arbitrary sign convention of PCA first component; visual confirmation via MS_plot or constituent metabolite inspection is required to disambiguate biological meaning
- Validation assumes normalization and imputation were applied correctly; artifacts from variance stabilizing normalization (vsn) or k-nearest neighbor imputation (cutoff=0.4) can distort metabolite abundances and inflate apparent effect sizes
- Module composition and eigenmetabolite sensitivity to outliers within the module; prior outlier detection via k-means clustering and removal may be necessary to prevent spurious direction reversals
- Biweight midcorrelation similarity used in WGCNA provides robustness to outliers but does not eliminate confounding by unmeasured covariates; direction of effect must be validated against known metabolic biology

## Evidence

- [other] Extract and validate that Module 2 shows p-value < 0.05 and direction of effect (higher abundance in normal group).: "Extract and validate that Module 2 shows p-value < 0.05 and direction of effect (higher abundance in normal group)."
- [other] Verify intermediate metabolite significance values and module eigenmetabolite calculations match expected output.: "Verify intermediate metabolite significance values and module eigenmetabolite calculations match expected output."
- [methods] The function `calculate_MS` merges all objects into a so called `MultiAssayExperiment` object to simplify all downstream analysis.: "average absolute metabolite significance per module"
- [other] Generate MS_plot with group_factor='tumor_normal', p_value_cutoff=0.05, and p_adjust=FALSE to visualize module-trait associations.: "Generate MS_plot with group_factor='tumor_normal', p_value_cutoff=0.05, and p_adjust=FALSE to visualize module-trait associations."
- [readme] As a key functionality, MetaboDiffs offers the exploration of sample traits in a data-derived metabolic correlation network.: "As a key functionality, MetaboDiffs offers the exploration of sample traits in a data-derived metabolic correlation network."
