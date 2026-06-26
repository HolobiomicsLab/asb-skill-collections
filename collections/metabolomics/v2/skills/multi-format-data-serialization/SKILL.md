---
name: multi-format-data-serialization
description: 'Use when after completing quality control, batch normalization, and
  outlier assessment on a Metaboprep object, when you need to: (1) save processed
  data matrices and metadata in human-readable tab-delimited format for use in other
  statistical or visualization tools;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0637
  - http://edamontology.org/topic_3172
  tools:
  - R
  - rmarkdown
  - knitr
  - ggplot2
  - metaboprep
  - dendextend
  - kableExtra
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btac059/6522114
  title: Metaboprep
evidence_spans:
- library(metaboprep)
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

# multi-format-data-serialization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Export processed metabolomic data and quality control outputs from an in-memory Metaboprep object into multiple serialized formats (tab-delimited text files, HTML reports) for downstream analysis, archival, and cross-platform compatibility. This skill bridges the gap between interactive R-based QC and format-agnostic data sharing.

## When to use

After completing quality control, batch normalization, and outlier assessment on a Metaboprep object, when you need to: (1) save processed data matrices and metadata in human-readable tab-delimited format for use in other statistical or visualization tools; (2) generate a comprehensive HTML QC report documenting sample and feature summaries, filtering decisions, and diagnostic plots; or (3) archive the final QC-filtered dataset in a reproducible, portable format. Use this skill when your downstream analysis requires data formats other than R binary objects (e.g., CSV for Excel, TSV for Unix pipelines, or HTML for stakeholder review).

## When NOT to use

- The Metaboprep object has not yet completed quality_control() — export before QC will serialize raw or incompletely validated data.
- You need to continue iterative QC refinement in R — exporting to text formats loses the structured Metaboprep object and requires re-import to modify.
- Your downstream tool natively reads R .RData or .rds binary formats — serialization to text adds unnecessary I/O overhead.

## Inputs

- Metaboprep object (post-quality_control, post-batch_normalise)
- Project name (string)
- Output directory path (string)

## Outputs

- Tab-delimited data matrix (.txt or .tsv) with samples × features
- Tab-delimited sample metadata (.txt or .tsv) with exclusion codes and reasons
- Tab-delimited feature metadata (.txt or .tsv) with annotations and exclusion codes
- HTML quality control report (.html) with summary statistics, plots, and dendrograms

## How to apply

After running quality_control() on a Metaboprep object, call export() with format='metaboprep' and a specified output directory to serialize three tab-delimited files: processed data matrix, sample metadata (with exclusion flags and reasons), and feature metadata (with pathway annotations and exclusion codes). In parallel, call generate_report() with the same Metaboprep object, specifying project name, output directory, format='html', and template='qc_report' to render an HTML document via rmarkdown and knitr. The HTML report should contain feature and sample summary statistics, exclusion summaries, and visualizations (dendrograms via dendextend, styled tables via kableExtra, and ggplot2 plots). Verify output by checking for the presence and integrity of all files: project_name_metaboprep_qc_report.html plus associated .txt/.tsv exports. Ensure row and column counts in exported matrices match the post-QC object dimensions.

## Related tools

- **metaboprep** (Core R package providing Metaboprep object structure, export() and generate_report() functions, and QC pipeline state management.) — https://github.com/MRCIEU/metaboprep
- **rmarkdown** (Renders the QC report template into HTML format from R-generated content.)
- **knitr** (Processes dynamic code chunks and template rendering for the HTML report.)
- **ggplot2** (Generates statistical plots (e.g., PCA, missingness heatmaps) embedded in the HTML report.)
- **dendextend** (Creates annotated dendrograms of hierarchical feature clustering for the HTML report.)
- **kableExtra** (Styles and formats data summary tables in the HTML report with kable_styling().)

## Examples

```
mydata |> generate_report(project = "my_study", output_dir = "./qc_reports", format = "html", template = "qc_report"); export(mydata, directory = "./qc_reports", format = "metaboprep")
```

## Evaluation signals

- All three tab-delimited files (.txt or .tsv) are written to the specified output directory with non-zero byte count and parseable structure (header row + data rows).
- HTML report file (project_name_metaboprep_qc_report.html) is generated and renders without errors in a web browser, displaying summary tables and plots.
- Row count in exported data matrix equals the number of non-excluded samples in the post-QC Metaboprep object; column count equals the number of non-excluded features.
- Sample metadata export includes exclusion codes (e.g., 'user_defined_sample_missingness', 'user_defined_sample_pca_outlier') for all excluded samples; feature metadata includes pathway and KEGG annotations.
- HTML report displays the exclusion summary table matching the counts and reasons reported by summary(Metaboprep_object).

## Limitations

- The export() function does not preserve interactive R object state — exported TSV/CSV files lose the Metaboprep class and must be re-imported as data.frames for further R processing.
- HTML report generation depends on template availability (template='qc_report') and rmarkdown/knitr execution; missing dependencies or malformed templates will cause report generation to fail without returning intermediate plots.
- Tab-delimited export enforces lossy conversion of complex R objects (e.g., hierarchical clustering trees, PCA loadings) to text; full diagnostic metadata must be recovered from the HTML report or reimported Metaboprep object.
- No changelog is maintained in the package, limiting audit trails for report version history across iterations.

## Evidence

- [other] The metaboprep package generates useful summary data in the form of tab-delimited text files and an HTML report as outputs from the report generation step.: "Call generate_report() with project name, output directory, format='html', and template='qc_report' to render the QC report. 3. Call export() with format='metaboprep' to write processed data, sample"
- [readme] Provide useful summary data in the form of tab-delimited text file and a html report: "Provide useful summary data in the form of tab-delimited text file and a html report"
- [other] Verify that the HTML report file (project_name_metaboprep_qc_report.html) and associated tab-delimited exports (.txt/.tsv) exist in the output directory.: "Verify that the HTML report file (project_name_metaboprep_qc_report.html) and associated tab-delimited exports (.txt/.tsv) exist in the output directory"
- [readme] Read in and processes (un)targeted metabolite data, saving datasets in tab-delimited format for use elsewhere: "Read in and processes (un)targeted metabolite data, saving datasets in tab-delimited format for use elsewhere"
- [methods] Export Metaboprep function signature and usage context: "export(mydata, directory = output_dir, format = "metaboprep")"
