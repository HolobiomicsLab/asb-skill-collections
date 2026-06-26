---
name: metaboprep-object-manipulation
description: Use when you have imported raw (un)targeted metabolite data (from Metabolon,
  Nightingale, Olink, or SomaLogic platforms, or custom tab-delimited tables) and
  need to apply a uniform, reproducible QC and normalization pipeline.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_3172
  tools:
  - R
  - metaboprep
  - rmarkdown
  - knitr
  - ggplot2
  - dendextend
  - kableExtra
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btac059/6522114
  title: Metaboprep
evidence_spans:
- library(metaboprep)
- quality_control(m, source_layer = "input", sample_missingness = 0.2, feature_missingness
  = 0.2)
- '%\VignetteEngine{knitr::rmarkdown}'
- library(ggplot2)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboprep_cq
    doi: 10.1093/bioinformatics/btac059/6522114
    title: Metaboprep
  dedup_kept_from: coll_metaboprep_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btac059/6522114
  all_source_dois:
  - 10.1093/bioinformatics/btac059/6522114
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metaboprep-object-manipulation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct, inspect, and transform Metaboprep objects—data structures that bundle metabolite abundance matrices, sample metadata, and feature metadata—through piped operations (batch normalization, quality control) and export them as tab-delimited or HTML outputs. This is the core workflow for standardizing (un)targeted metabolomic datasets before downstream analysis.

## When to use

You have imported raw (un)targeted metabolite data (from Metabolon, Nightingale, Olink, or SomaLogic platforms, or custom tab-delimited tables) and need to apply a uniform, reproducible QC and normalization pipeline. Use this skill when you want to exclude samples or features by user-defined thresholds (sample/feature missingness, outlier distance, peak area), generate a QC report documenting exclusions, and save processed data in standardized tab-delimited format for export to other tools.

## When NOT to use

- Input data are already a processed feature table without raw sample/feature metadata or platform information—the pipeline requires structured annotation tables.
- You need real-time streaming QC or have >1 million features; the current implementation may have computational limits.
- Data have been pre-QC'd in an external tool and you only need to reformat to tab-delimited for export—use simpler export wrappers instead.

## Inputs

- Abundance matrix (rows = features/metabolites; columns = samples; values = peak area, intensity, or normalized abundance)
- Sample metadata table (rows = samples; columns = sample identifiers and covariates)
- Feature metadata table (rows = features; columns = feature identifiers, metabolite names, platform, pathway, KEGG/HMDB annotations)
- Platform/run mode annotation (column name indicating platform or ion polarity)

## Outputs

- Metaboprep object with 'input' and 'qc' data layers
- Sample exclusion summary (counts and reasons: extreme/user-defined missingness, total peak area outliers, PCA outliers)
- Feature exclusion summary (counts and reasons: extreme/user-defined missingness)
- Tab-delimited export files (processed data matrix, sample metadata, feature metadata with exclusion flags)
- HTML QC report (project_name_metaboprep_qc_report.html) with tables, summary statistics, and diagnostic plots
- Feature tree dendrogram (hierarchical clustering based on Pearson correlation, stored as dendrogram object)

## How to apply

First, construct a Metaboprep object by calling Metaboprep(data=, samples=, features=) with an abundance matrix, sample annotation table, and feature annotation table. Then apply batch_normalise() if data were collected across multiple platforms or runs, specifying the platform column and mode mapping (e.g., 'pos'/'neg' for ion modes). Next, pipe the object into quality_control() with user-defined thresholds: sample_missingness (proportion of missing values per sample), feature_missingness (proportion per feature), total_peak_area_sd (number of standard deviations from mean for total ion abundance), outlier_udist (Mahalanobis distance cutoff for PCA-based outliers), winsorize_quantile, pc_outlier_sd, and tree_cut_height. The function returns an object with an additional 'qc' data layer and exclusion flags annotated on samples and features. Finally, export the object using export(format='metaboprep') to write tab-delimited outputs (data, sample metadata, feature metadata), and optionally call generate_report(format='html', template='qc_report') to produce an interactive HTML summary showing sample/feature counts, exclusion reasons, and diagnostic plots.

## Related tools

- **metaboprep** (Primary package providing Metaboprep class, batch_normalise(), quality_control(), export(), generate_report(), and summary methods) — https://github.com/MRCIEU/metaboprep
- **rmarkdown** (Templating engine for rendering QC HTML reports from embedded R code)
- **knitr** (Document processor for Rmarkdown vignettes and QC report generation)
- **ggplot2** (Visualization of summary statistics and diagnostic plots within QC reports)
- **dendextend** (Feature tree dendrogram manipulation and annotation)
- **kableExtra** (Styled table rendering in HTML reports (kable_styling))

## Examples

```
library(metaboprep); mydata <- Metaboprep(data = mydata$data, samples = mydata$samples, features = mydata$features); mydata <- mydata |> batch_normalise(run_mode_col = "platform", run_mode_colmap = c(pos="pos", neg="neg")) |> quality_control(source_layer = "input", sample_missingness = 0.2, feature_missingness = 0.2, total_peak_area_sd = 5, outlier_udist = 5); export(mydata, directory = output_dir, format = "metaboprep"); generate_report(mydata, project_name = "my_project", output_directory = output_dir, format = "html", template = "qc_report")
```

## Evaluation signals

- Verify the returned Metaboprep object has exactly 2 data layers ('input' and 'qc') and that the 'qc' layer has fewer samples/features than 'input' (by design, exclusions are cumulative).
- Check that sample and feature metadata tables have new 'excluded' and 'reason_excluded' columns, with reasons matching the quality_control() parameters applied (e.g., 'user_defined_sample_missingness', 'user_defined_sample_totalpeakarea').
- Confirm that the HTML report file is generated at the specified output directory with the naming scheme project_name_metaboprep_qc_report.html and displays summary counts matching the summary(object) output.
- Verify that tab-delimited exports exist (.txt/.tsv files) with the same number of rows/columns as the object's 'qc' layer data frame, and that headers match feature/sample identifiers.
- Ensure feature tree dendrogram can be extracted via attr(mydata@feature_summary, 'qc_tree') and plotted without errors, confirming hierarchical clustering was computed.

## Limitations

- PCA outlier detection may warn or fail if fewer informative PCs exist than requested (max_num_pcs parameter), especially in small or low-variance datasets.
- The pipeline assumes batch effects align with platform/run_mode columns; if confounding structure exists outside these categories, batch_normalise() may not fully address it.
- No automated method is provided to select optimal thresholds (sample_missingness, feature_missingness, outlier_udist); users must set these manually or validate on a pilot dataset.
- Tree dendrogram is computed only if tree_cut_height is specified; if omitted, feature clustering information is not stored.

## Evidence

- [readme] Workflow overview and multi-platform support: "Read in and processes (un)targeted metabolite data, saving datasets in tab-delimited format for use elsewhere"
- [readme] Output types and report generation: "Provide useful summary data in the form of tab-delimited text file and a html report"
- [readme] QC function parameters and thresholds: "mydata |> quality_control( source_layer = "input", sample_missingness = 0.2, feature_missingness = 0.2, total_peak_area_sd = 5, outlier_udist = 5, outlier_treatment = "leave_be", winsorize_quantile ="
- [methods] Report generation workflow: "Call generate_report() with project name, output directory, format='html', and template='qc_report' to render the QC report"
- [methods] Export workflow: "Call export() with format='metaboprep' to write processed data, sample metadata, and feature metadata as tab-delimited text files"
- [readme] Exclusion summary inspection: "Exclusion Codes Summary: Sample Exclusions: Exclusion | Count. user_defined_sample_missingness | 2"
- [readme] Feature tree dendrogram storage: "tree <- attr(mydata@feature_summary, "qc_tree")"
