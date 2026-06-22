---
name: multivariate-lipid-metabolite-analysis
description: Use when you have integrated, normalized lipidomic and metabolomic feature tables from the Multi-ABLE method or similar concurrent multiomics workflows, with matched sample phenotypes (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - R
  - MultiABLER
  - limma
  - ProteoMM
derived_from:
- doi: 10.1016/j.isci.2023.106881
  title: MultiABLER
- doi: 10.1021/acs.analchem.9b01842
  title: ''
evidence_spans:
- MultiABLER is a set of R functions
- MultiABLER is a set of R functions forms a seamless workflow
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_multiabler_cq
    doi: 10.1016/j.isci.2023.106881
    title: MultiABLER
  dedup_kept_from: coll_multiabler_cq
schema_version: 0.2.0
---

# Multivariate Analysis of Lipids and Metabolites

## Summary

Apply multivariate statistical methods to identify differential lipids and metabolites associated with biological phenotypes (e.g., atherosclerosis) from integrated lipidomic and metabolomic datasets. This skill enables detection of molecular signatures across multiple lipid and metabolite features simultaneously, rather than univariate feature-by-feature testing.

## When to use

You have integrated, normalized lipidomic and metabolomic feature tables from the Multi-ABLE method or similar concurrent multiomics workflows, with matched sample phenotypes (e.g., diseased vs. control arterial tissue), and you need to discover which lipids and metabolites co-vary with or discriminate between phenotypic groups. Use this when univariate testing would lose power due to high dimensionality and when biological interpretation requires systems-level lipid/metabolite signatures.

## When NOT to use

- Input feature tables are not normalized or aligned across samples — preprocess with MultiABLER's normalization and preprocessing functions first.
- Phenotype or group assignment is missing or ambiguous — multivariate analysis requires clear sample stratification.
- You are analyzing a single individual or unpaired samples — multivariate statistical inference requires replicate samples per phenotype group.

## Inputs

- Normalized lipidomic feature matrix (samples × lipid features, intensity or abundance values)
- Normalized metabolomic feature matrix (samples × metabolite features, intensity or abundance values)
- Sample metadata table (sample ID, phenotype/group assignment, batch/technical covariates)
- Feature annotation tables (lipid class, metabolite identity, m/z, retention time, or chemical formula)

## Outputs

- Ranked differential lipid and metabolite table (feature name, log2 fold-change, p-value, adjusted p-value, effect size)
- Multivariate statistical model fit object (coefficients, residuals, model diagnostics)
- Quality control and visualization plots (PCA, heatmaps, volcano plots, feature abundance distributions by phenotype)
- Statistical summary report (number of significant lipids/metabolites, effect size distributions, pathway or class-level summaries)

## How to apply

Load preprocessed and aligned lipidomic and metabolomic feature matrices (output from normalization and spectral alignment steps) along with sample metadata defining phenotypes (e.g., atherosclerosis status). Apply multivariate statistical functions from MultiABLER (or equivalent frameworks using limma and ProteoMM) to model feature abundance as a function of phenotype, controlling for batch and technical effects. Extract ranked lists of differential lipids and metabolites with associated p-values and effect sizes. Validate results by cross-checking consistency across lipid classes and metabolite chemical families, and by generating multivariate plots (e.g., PCA, heatmaps) that show phenotypic separation driven by these features. Judge success by statistical significance (e.g., adjusted p < 0.05), biological coherence (e.g., expected lipid species dysregulation in atherosclerosis), and reproducibility of top-ranked features.

## Related tools

- **MultiABLER** (R package providing multivariate analysis functions (differential lipid/metabolite detection, model fitting, visualization) for integrated lipidomic and metabolomic data) — https://github.com/holab-hku/MultiABLER
- **limma** (Bioconductor package used by MultiABLER for linear modeling and statistical testing of differential features across phenotypes) — https://www.bioconductor.org/packages/release/bioc/html/limma.html
- **ProteoMM** (Bioconductor package dependency for multivariate analysis and feature modeling in MultiABLER) — https://www.bioconductor.org/packages/release/bioc/html/ProteoMM.html
- **R** (Programming language and environment in which MultiABLER functions are executed)

## Examples

```
devtools::install_github("holab-hku/MultiABLER", dependencies = TRUE); source("MultiABLER.r"); result <- multivariate_analysis(lipid_data, metabolite_data, phenotype_vector, batch_covariates)
```

## Evaluation signals

- Significant differential lipids and metabolites (adjusted p < 0.05) are biologically coherent with the phenotype (e.g., dysregulated lipid classes known to associate with atherosclerosis in prior literature).
- Multivariate visualizations (PCA, heatmaps) show clear phenotypic separation driven by the identified differential features, with minimal overlap between groups.
- Log2 fold-changes and effect sizes are consistent in direction and magnitude across biological replicates and lipid/metabolite chemical families.
- Statistical model diagnostics (residual normality, homoscedasticity, variance-covariance structure) meet assumptions of the chosen multivariate test (e.g., linear model, PERMANOVA).
- Top-ranked features remain significant after sensitivity analysis (e.g., removal of outlier samples, alternative statistical methods, cross-validation).

## Limitations

- MultiABLER is purpose-built for data generated by the Multi-ABLE method; application to other concurrent lipidomic/metabolomic platforms requires validation and possible adaptation of preprocessing and normalization steps.
- Multivariate analysis assumes sufficient sample replication per phenotype group; small sample sizes reduce statistical power and increase false discovery risk despite multiple testing correction.
- Identified differential lipids and metabolites are correlative, not causal; validation via targeted follow-up experiments (e.g., stable isotope tracing, metabolic flux analysis) is needed to establish mechanistic roles.

## Evidence

- [other] Run the multivariate analysis functions to identify differential lipids and metabolites associated with atherosclerosis phenotypes.: "Run the multivariate analysis functions to identify differential lipids and metabolites associated with atherosclerosis phenotypes"
- [readme] MultiABLER is a set of R functions forms a seamless workflow that supports integrative processing and analysis of lipidomic and metabolomic data generated by the Multi-ABLE method: "MultiABLER is a set of R functions forms a seamless workflow that supports integrative processing and analysis of lipidomic and metabolomic data generated by the Multi-ABLE method"
- [readme] install the following packges in R and run the funcions in MultiABLER.r: "install the following packges in R and run the funcions in MultiABLER.r"
- [other] Execute the integrated preprocessing functions to normalize and align spectral features across samples.: "Execute the integrated preprocessing functions to normalize and align spectral features across samples"
