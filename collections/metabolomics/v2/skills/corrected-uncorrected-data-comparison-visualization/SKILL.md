---
name: corrected-uncorrected-data-comparison-visualization
description: Use when after preprocessing and log-transformation of metabolomics feature abundance matrices (samples as rows, metabolic features as columns), when you have multiple candidate batch-correction models (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2238
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - dbnorm
  - R
  - sva (ComBat parametric and non-parametric models)
  - R graphics (ggplot2, lattice, base R)
derived_from:
- doi: 10.1038/s41598-021-84824-3
  title: Dbnorm
- doi: 10.1007/s12561-013-9081-1
  title: ''
evidence_spans:
- dbnorm (V-0.2.2) A package for drift across batches normalization and visualization
- dbnorm contains R functions which allow visualization and removal of technical heterogeneity
- '*dbnorm* contains R functions which allow visualization and removal of technical heterogeneity'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_dbnorm_cq
    doi: 10.1038/s41598-021-84824-3
    title: Dbnorm
  dedup_kept_from: coll_dbnorm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41598-021-84824-3
  all_source_dois:
  - 10.1038/s41598-021-84824-3
  - 10.1007/s12561-013-9081-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# corrected-uncorrected-data-comparison-visualization

## Summary

Generate side-by-side diagnostic visualizations comparing raw and batch-effect-corrected metabolomics data to assess which statistical correction model (parametric vs. non-parametric ComBat, or two-stage ber procedure) best fits the dataset structure. This skill enables quantitative model selection by revealing how effectively each correction method removes technical heterogeneity while preserving biological signal.

## When to use

After preprocessing and log-transformation of metabolomics feature abundance matrices (samples as rows, metabolic features as columns), when you have multiple candidate batch-correction models (e.g., parametric ComBat, non-parametric ComBat, ber, ber-bagging) and need to choose which one minimizes batch drift without over-correcting. Use this skill when you can tolerate computational time for < 2000 features (per README guidance) and require visual + quantitative evidence to justify model selection.

## When NOT to use

- Input metabolomics matrix has > 2000 features; computational speed degrades and visualization becomes unwieldy (README explicitly recommends < 2000 features for Visodbnorm and dbnormSCORE).
- Data has not been log-transformed or normalized prior to batch correction; technical heterogeneity masking by high-abundance features will obscure true batch structure.
- Single batch only (no batch effect present); comparison functions assume multi-batch design and will not reveal meaningful differences.
- Samples are already in a normalized, integrated format (e.g., output of a prior batch-correction pipeline); reapplying correction may introduce artificial artifacts.

## Inputs

- Preprocessed metabolomics feature abundance matrix (CSV format): log-transformed, samples × features, with batch identifier in first column
- Batch design vector: assignment of samples to analytical runs or batches
- Optional: quality control (QC) replicates or analytical replicates to assess concordance post-correction

## Outputs

- Diagnostic PDF file: PCA plots and Scree plots comparing raw vs. corrected data across all models
- Diagnostic PDF file: RLA (Relative Log Abundance) plots visualized in RStudio Viewer panel
- Diagnostic PDF file: Probability density function (PDF) profile plots for raw and model-corrected feature distributions
- Diagnostic PDF file: Correlation and Score plots from dbnormSCORE() showing adjusted R² by feature and model performance summary table
- Corrected data matrices (CSV): one per applied model (ber, ber-bagging, parametric ComBat, non-parametric ComBat), stored in temporary directory
- Score table (CSV): adjusted R² values and model performance rankings for model selection decision

## How to apply

Load the preprocessed CSV matrix (with batch labels in the first column) into R and invoke the dbnorm comparison workflow: (1) Generate visualization outputs (PCA plots, Scree plots, RLA plots, probability density function profiles) for both raw and corrected datasets across all candidate models using functions like Visodbnorm() or individual dbnormBer/dbnormPcom/dbnormNPcom functions. (2) Calculate adjusted R² coefficients for each feature's dependence on batch in raw vs. corrected data using dbnormSCORE(), which quantifies how much batch variance remains after each correction. (3) Compile corrected datasets (output as CSV files) alongside diagnostic PDFs into a unified comparison report. (4) Rank models by maximum adjusted R² reduction and visual coherence of batch-corrected sample clustering in PCA space. Select the model achieving the highest batch variance removal with the most stable feature-level correction across all metabolites.

## Related tools

- **dbnorm** (R package providing Visodbnorm(), dbnormSCORE(), and individual model-specific correction functions (dbnormBer, dbnormPcom, dbnormNPcom) to generate diagnostic plots and corrected datasets for side-by-side comparison.) — https://github.com/NBDZ/dbnorm
- **sva (ComBat parametric and non-parametric models)** (Empirical Bayes batch-correction models invoked by dbnorm for comparison; implements parametric and non-parametric ComBat options referenced in visualization output.)
- **R graphics (ggplot2, lattice, base R)** (Underlying plotting libraries used by dbnorm to render PCA, Scree, RLA, and PDF profile plots.)

## Examples

```
library(dbnorm)
data <- read.csv('path/to/metabolomics_logscaled.csv', sep=',', header=T, row.names=1)
Visodbnorm(data)
dbnormSCORE(data)
```

## Evaluation signals

- PCA plot: batch-corrected samples from the same biological cohort cluster tightly in PC1–PC2 space, while uncorrected data show drift or stratification by batch. Corrected data should show reduced batch-related separation.
- Adjusted R² scores: corrected datasets exhibit mean adjusted R² ≤ 0.1–0.2 (indicating minimal batch dependence per feature), while raw data show substantially higher values (> 0.3–0.5). Model with lowest median adjusted R² across all features is preferred.
- RLA (Relative Log Abundance) plots: corrected data RLA distributions should be centered near zero with minimal skew; uncorrected data show systematic median shifts by batch. Corrected plot symmetry indicates successful centering.
- Feature-level PDF profiles: corrected distributions overlap across batches; raw distributions show shifted modes by batch. Overlapping corrected curves confirm drift removal.
- Model consistency: performance ranking from dbnormSCORE() should show one clear winner (highest R² reduction) without ties; tie or reversal by feature subset suggests poor model fit to overall data structure.

## Limitations

- dbnorm diagnostic functions are recommended for < 2000 features; larger feature sets may experience computational slowdown and compressed visualizations (README states 'suggested for less than 2000 features').
- Comparison relies on adjusted R² as a proxy for batch contamination; in datasets with strong biological batch confounding (e.g., batch 1 = diseased, batch 2 = healthy), aggressive correction may remove biological signal, which adjusted R² alone may not detect—requiring additional domain knowledge validation.
- No changelog available in repository (noted in enriched index), so version-specific behavior and model changes are undocumented; reproducibility across dbnorm versions may vary.
- Visual interpretation of PCA and PDF plots is subjective; two analysts may rank models differently. Quantitative score thresholds are not provided in the article or README, requiring domain expertise to set decision criteria.
- Assumes log-transformation and appropriate scaling of input data; failure to preprocess correctly will confound batch structure and yield misleading comparisons.

## Evidence

- [other] Generate diagnosis plots comparing corrected versus uncorrected data to highlight the effect of batch-effect correction methods (parametric and non-parametric ComBat models).: "Generate diagnosis plots comparing corrected versus uncorrected data to highlight the effect of batch-effect correction methods (parametric and non-parametric ComBat models)."
- [readme] functions using advanced statistical tools to generate several diagnosis plots to help users to choose the statistical model which better fits to their data structure: "functions using advanced statistical tools to generate several diagnosis plots to help users to choose the statistical model which better fits to their data structure"
- [readme] Graphical check such as PCA plot and Scree plot compiled into a PDF (saved in the working directory) and three .csv files (saved in a folder, intiate with Rtmpe, in Users's Temporary directory): "Graphical check such as PCA plot and Scree plot compiled into a PDF (saved in the working directory) and three .csv files"
- [readme] The RLA plots are visualized in the Viewer panel in the rstudio console.: "The RLA plots are visualized in the Viewer panel in the rstudio console."
- [readme] dbnormSCORE (data) - This function gives a quick notification about the performance of the statistical models, two-stage procedure and/or empirical Bayes methods in two setting of parametric and non-parametric as described in, implemented in the dbnorm package, in accommodating technical variability. Subsequently, the adjusted coefficient of determination or Adjusted R-Squared is calculated for each variable estimated in a regression model for its dependency to the batch level in the raw data and treated data via either of those models.: "the adjusted coefficient of determination or Adjusted R-Squared is calculated for each variable estimated in a regression model for its dependency to the batch level in the raw data and treated data"
- [readme] This function is suggested for less than 2000 features (variables).: "This function is suggested for less than 2000 features (variables)."
- [readme] Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features (variables) by which technical heterogeneity might be overlooked.: "Data to be uploaded must be normalized and scaled on the log2 to account for the high abundance features"
