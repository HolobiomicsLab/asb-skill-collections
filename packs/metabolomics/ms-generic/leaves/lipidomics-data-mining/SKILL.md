---
name: lipidomics-data-mining
description: Use when when you have quantitative lipidomics data (either from Skyline CSV export or numerical matrix format) with sample annotations and a biological grouping variable (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3656
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_2269
  tools:
  - lipidr
  - R
  - limma
  - SummarizedExperiment
  - Skyline
  - Metabolomics Workbench API
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.jproteome.0c00082
  title: lipidr
evidence_spans:
- Datasets can be easily downloaded and parsed into `LipidomicsExperiment` object using `lipidr` function `fetch_mw_study()`
- '`lipidr` allows users, to quickly explore public lipidomics experiments. `lipidr` provides an easy way to re-analyze and visualize these datasets.'
- Data Mining and Analysis of Lipidomics Datasets in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidr_cq
    doi: 10.1021/acs.jproteome.0c00082
    title: lipidr
  dedup_kept_from: coll_lipidr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.0c00082
  all_source_dois:
  - 10.1021/acs.jproteome.0c00082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipidomics-data-mining

## Summary

End-to-end mining and statistical analysis of lipidomics mass spectrometry datasets using lipidr in R, encompassing data import, quality control, multivariate and univariate analysis, and lipid set enrichment analysis to identify lipid classes and chain properties associated with biological conditions.

## When to use

When you have quantitative lipidomics data (either from Skyline CSV export or numerical matrix format) with sample annotations and a biological grouping variable (e.g., disease state, treatment), and you need to discover which lipid molecular species, classes, chain lengths, or saturation patterns are significantly altered across groups.

## When NOT to use

- Input is already a pre-aggregated feature table (e.g., class-level sums) rather than individual lipid molecular species — LSEA requires molecule-level data to compute enrichment.
- Samples lack clear grouping annotations or biological replicates — differential analysis requires sufficient sample sizes per group.
- Data has not been quality-controlled or normalized — workflow expects validated, measurement-comparable intensities.

## Inputs

- Skyline CSV export file (measured lipid intensities with method context)
- Numerical matrix CSV (lipids as rows, samples as columns, lipid names in first column)
- Sample annotation/clinical CSV (sample names in first column, categorical and numerical variables)
- LipidomicsExperiment object (intermediate R object extending SummarizedExperiment)

## Outputs

- LipidomicsExperiment object (QC-filtered, normalized lipidomics data with sample annotations)
- PCA multivariate analysis result (scores, loadings, sample clustering visualization)
- Two-group differential expression result (logFC, p-values, volcano plot)
- LSEA result object with significant_lipidsets table (lipid classes, chain properties, enrichment scores, adjusted p-values)
- Visualization plots (TIC, boxplots, volcano plots, enrichment plots)

## How to apply

Load lipidomics data into a LipidomicsExperiment object using either read_skyline() or as_lipidomics_experiment() paired with add_sample_annotation(). Perform quality control via TIC plots and boxplots, then mark data as logged and normalized. Run multivariate analysis (PCA) to assess sample separation, remove outliers if needed, and perform two-group de_analysis() to compute logFC values. Finally, apply lsea() with rank.by='logFC' to rank lipids by fold-change and compute enrichment statistics for predefined lipid sets (classes and chain-length features); extract and visualize significant_lipidsets meeting your p-value threshold (e.g., adjusted p < 0.05) to interpret which lipid biochemical features drive the observed changes.

## Related tools

- **lipidr** (Core R package for data import, QC, normalization, multivariate/univariate analysis, and lipid set enrichment on LipidomicsExperiment objects) — https://github.com/ahmohamed/lipidr
- **limma** (Underlying statistical package for differential expression analysis in two-group and multi-group comparisons)
- **SummarizedExperiment** (Bioconductor container class extended by LipidomicsExperiment for organizing assay data, sample metadata, and lipid annotations)
- **Skyline** (Mass spectrometry data processing software whose CSV exports lipidr can parse directly)
- **Metabolomics Workbench API** (Remote data repository integrated into lipidr for searching and downloading public lipidomics datasets)

## Examples

```
d <- read_skyline('Skyline_export.csv'); d <- add_sample_annotation(d, 'clin.csv'); set_logged(d, 'Area', TRUE); d <- set_normalized(d, 'Area', TRUE); two_group <- de_analysis(d, Cancer-Benign); lsea_result <- lsea(two_group, rank.by='logFC'); sig_lipidsets <- lsea_result$significant_lipidsets[lsea_result$significant_lipidsets$padj < 0.05, ]
```

## Evaluation signals

- LipidomicsExperiment object successfully created with correct sample count, lipid feature count, and annotation columns matching input files
- TIC and boxplot QC plots show consistent signal distributions after normalization; outlier removal visibly improves sample clustering in PCA
- Two-group volcano plot shows expected logFC distribution with clear separation between up- and down-regulated lipids and confidence in p-values (typically |logFC| > 1 and adjusted p < 0.05)
- Significant lipid sets table contains entries ranked by enrichment score or p-value; lipid class and chain-property terms (e.g., 'PC', 'PE', 'unsaturated C18') are human-interpretable and match biological expectations for the condition
- Enrichment plots and visualizations are reproducible; re-running lsea() with same rank.by parameter and significance threshold yields identical significant_lipidsets and p-values

## Limitations

- LSEA relies on predefined lipid sets (classes, chain lengths, unsaturation patterns); novel lipid structures or modifications not in the reference set will not be detected as enriched units.
- Two-group and ANOVA-style differential analysis assume adequate replication per group and normality or at least symmetry of logFC distribution; small sample sizes or highly skewed data may reduce statistical power.
- Molecule name parsing is strict and requires supported naming patterns; lipids with non-standard nomenclature must be manually corrected or removed before analysis.
- PCA and multivariate analysis are sensitive to batch effects and technical variation; the article found cancer stage to have no effect but race showed small effects, indicating that unmeasured or uncontrolled covariates could confound interpretation.

## Evidence

- [readme] lipidr provides an easy way to re-analyze and visualize these datasets.: "lipidr provides an easy way to re-analyze and visualize these datasets."
- [intro] Running lipid set enrichment analysis (lsea) with rank.by='logFC' on two-group differential results identifies significant lipid sets that can be extracted and visualized to show enriched lipid classes and chain unsaturations.: "Running lipid set enrichment analysis (lsea) with rank.by='logFC' on two-group differential results identifies significant lipid sets"
- [readme] A novel lipid set enrichment analysis is implemented to detect preferential regulation of certain lipid classes, total chain lengths or unsaturation patterns.: "A novel lipid set enrichment analysis is implemented to detect preferential regulation of certain lipid classes, total chain lengths or unsaturation patterns."
- [readme] LipidomicsExperiment, which extends SummarizedExperiment, to facilitate integration with other Bioconductor packages.: "LipidomicsExperiment, which extends SummarizedExperiment, to facilitate integration with other Bioconductor packages."
- [readme] Univariate analysis can be performed using any of the loaded clinical variables, which can be readily visualized as volcano plots. Multi-group comparisons and adjusting for confounding variables is also supported: "Univariate analysis can be performed using any of the loaded clinical variables, which can be readily visualized as volcano plots."
- [intro] This step of the workflow requires the limma package to be installed.: "This step of the workflow requires the limma package to be installed."
- [intro] Note the warning that some molecules were not parsed because their names did not follow the supported patterns.: "Note the warning that some molecules were not parsed because their names did not follow the supported patterns."
