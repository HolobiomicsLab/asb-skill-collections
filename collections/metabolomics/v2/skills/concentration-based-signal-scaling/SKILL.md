---
name: concentration-based-signal-scaling
description: Use when you have loaded m/z peak data with metadata that includes a
  concentration column representing sample loading mass or volume, and systematic
  intensity variation across samples is suspected to reflect preparation differences
  rather than true biological variation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - MetaboShiny
  - R
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1007/s11306-020-01717-8
  title: MetaboShiny
evidence_spans:
- Welcome to the info page on MetaboShiny
- Welcome to the info page on MetaboShiny! We are currently on BioRXiv
- Through R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboshiny_cq
    doi: 10.1007/s11306-020-01717-8
    title: MetaboShiny
  dedup_kept_from: coll_metaboshiny_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-020-01717-8
  all_source_dois:
  - 10.1007/s11306-020-01717-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# concentration-based-signal-scaling

## Summary

Normalize metabolomic m/z peak intensities by accounting for sample-specific concentration differences to enable valid cross-sample and cross-batch comparisons. This skill corrects for variable sample loading that would otherwise confound downstream statistical and identification analyses.

## When to use

Apply this skill when you have loaded m/z peak data with metadata that includes a concentration column representing sample loading mass or volume, and systematic intensity variation across samples is suspected to reflect preparation differences rather than true biological variation. The skill is particularly critical before batch correction or when comparing samples prepared at different concentrations.

## When NOT to use

- Metadata lacks a concentration or sample-loading column — skip to filtering and normalization step instead.
- All samples were prepared at nominally identical concentrations and no concentration metadata exists — concentration-based scaling is unnecessary.
- Peak intensities have already been normalized by an upstream processing tool (e.g., XCMS or MSnbase output already accounts for concentration).

## Inputs

- m/z peak intensity table (rows=m/z features, columns=samples; accepted formats: MetaboAnalyst-like, MetaboShiny native, Metabolights)
- metadata table with 'sample', 'individual', and concentration columns
- batch identifiers (if multi-batch study)

## Outputs

- concentration-normalized m/z peak intensity table
- pre- and post-normalization intensity distribution plots for validation

## How to apply

After loading m/z peak files and metadata into MetaboShiny, identify the metadata column representing concentration (e.g., sample mass, volume, or normalized loading). In the 'Batches and concentration' normalization section, select this concentration variable and apply it as a normalization factor. The software will then scale peak intensities by dividing by the corresponding sample concentration, converting absolute intensities to concentration-normalized values. This step should precede or be integrated with filtering and data transformation (log, cubic root, or none) and scaling methods (autoscale, Pareto, range, or mean-center). Verify that post-normalization intensity distributions across samples become more uniform by examining the pre- and post-normalization distribution plots MetaboShiny generates for random m/z values.

## Related tools

- **MetaboShiny** (interactive R/Shiny application that implements concentration-based scaling in the 'Batches and concentration' normalization module) — https://github.com/joannawolthuis/MetaboShiny
- **R** (runtime environment for MetaboShiny normalization functions)

## Examples

```
# In MetaboShiny R console after loading data:
# 1. Click 'Get options' in Batches and concentration panel
# 2. Select concentration column (e.g., 'sample_mass_ng') from dropdown
# 3. Select batch column if present (e.g., 'batch_id')
# 4. Proceed to Filtering and normalization step with concentration-scaled intensities
```

## Evaluation signals

- Concentration-normalized intensities for a given m/z feature across samples show reduced variance proportional to sample concentration differences pre-normalization.
- Distribution plots confirm that median and interquartile ranges of peak intensities become more uniform across samples after concentration scaling.
- Subsequent batch-effect correction and statistical tests (e.g., t-test, ANOVA) show improved p-values and effect sizes because biological signal is no longer masked by preparation artifacts.
- Intensity ratios between samples of known concentration differences approach expected values (e.g., 2× concentration ≈ 2× normalized intensity).

## Limitations

- Requires accurate, complete concentration metadata; missing or mislabeled concentration values will introduce systematic bias or data loss.
- Linear scaling assumes intensity is proportional to concentration across the full dynamic range; nonlinear detector response or concentration-dependent ionization efficiency may violate this assumption.
- Cannot correct for concentration differences if they are confounded with batch effects; batch correction should be applied first or in parallel.
- Does not account for individual compound-level concentration sensitivity; all m/z features are scaled by the same sample concentration.

## Evidence

- [intro] Normalization by concentration accounts for differences in sample loading: "Normalize peak intensities by concentration to account for differences in sample loading."
- [readme] MetaboShiny provides dedicated UI for selecting concentration metadata: "If applicable, select the variable that represents concentration in your data."
- [readme] Concentration normalization is prerequisite to filtering and transformation: "If your metadata only contains one batch and no column that represents concentration, then you can skip this part and continue to the Filtering and normalization step."
- [readme] MetaboShiny validates normalization via pre/post distribution plots: "After normalization, the distribution of pre- and post-normalized peak values will be plotted for a randomly selected set of m/z values and samples, so the user can see how the data distribution has"
