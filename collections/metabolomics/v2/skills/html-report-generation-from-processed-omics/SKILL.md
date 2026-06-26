---
name: html-report-generation-from-processed-omics
description: Use when after completing batch normalization and quality control filtering
  on a Metaboprep object, when you need to communicate QC decisions, visualize exclusion
  patterns, and export final processed data for downstream analysis or sharing with
  collaborators.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3172
  tools:
  - R
  - rmarkdown
  - knitr
  - ggplot2
  - metaboprep
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

# html-report-generation-from-processed-omics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate publication-ready HTML quality control reports and tab-delimited summary exports from processed metabolomics data objects. This skill produces interactive visual summaries and machine-readable outputs after data normalization and quality control filtering.

## When to use

After completing batch normalization and quality control filtering on a Metaboprep object, when you need to communicate QC decisions, visualize exclusion patterns, and export final processed data for downstream analysis or sharing with collaborators.

## When NOT to use

- Input Metaboprep object has not yet undergone quality_control() — report will reflect unfiltered raw data only
- Output directory does not exist or lacks write permissions
- Data has already been exported in final form and only HTML visualization is needed (use generate_report alone)

## Inputs

- Metaboprep object (post batch_normalise and post quality_control)
- project name (string)
- output directory path (string)

## Outputs

- HTML QC report file (project_name_metaboprep_qc_report.html)
- Tab-delimited processed data matrix (.txt or .tsv)
- Tab-delimited sample metadata (.txt or .tsv)
- Tab-delimited feature metadata (.txt or .tsv)

## How to apply

Load the quality-controlled Metaboprep object (post-batch_normalise and post-quality_control). Call generate_report() with the project name, output directory, format='html', and template='qc_report' to render an interactive HTML report summarizing sample and feature exclusion statistics, diagnostic plots, and QC thresholds applied. Simultaneously call export() with format='metaboprep' to write the processed data matrix, sample metadata, and feature metadata as tab-delimited text files (.txt/.tsv) to the same output directory. The report template uses rmarkdown and knitr to knit ggplot2-based visualizations and kableExtra-styled tables. Verify that the HTML file (project_name_metaboprep_qc_report.html) and corresponding .txt/.tsv files exist and contain expected row/column counts matching the QC-filtered Metaboprep object.

## Related tools

- **metaboprep** (R package providing generate_report() and export() methods for Metaboprep objects) — https://github.com/MRCIEU/metaboprep
- **rmarkdown** (Renders R markdown templates to HTML report)
- **knitr** (Executes embedded R code blocks within markdown during report generation)
- **ggplot2** (Produces statistical graphics embedded in the QC report)
- **kableExtra** (Formats and styles summary tables in the HTML report)

## Examples

```
mydata <- mydata |> quality_control(source_layer = "input", sample_missingness = 0.2, feature_missingness = 0.2); generate_report(mydata, project_name = "my_study", output_dir = "./results", format = "html", template = "qc_report"); export(mydata, directory = "./results", format = "metaboprep")
```

## Evaluation signals

- HTML file exists at expected path and is valid HTML (can be opened in a web browser)
- Tab-delimited text files exist with expected filenames and contain data matching QC-filtered Metaboprep object dimensions (rows = samples/features, columns = metadata fields)
- Report visually displays exclusion counts and codes matching the Exclusion Codes Summary from summary(mydata)
- Sample and feature counts in exported files are consistent with the reduced sample and feature count after quality_control filtering
- HTML report contains functional visualizations (dendrograms, summary plots) rendered without rendering errors

## Limitations

- Report generation requires rmarkdown and knitr to be installed; rendering may fail if dependencies are missing or incompatible
- Large datasets (>10,000 features or >1,000 samples) may produce HTML files that are slow to load or render in some web browsers
- The qc_report template is tailored to metabolomics; application to other omics data types (proteomics, genomics) may require custom templates
- Export format is currently limited to tab-delimited text; other formats (Excel, HDF5, NetCDF) are not supported by export(format='metaboprep')

## Evidence

- [methods] Call generate_report() with project name, output directory, format='html', and template='qc_report': "Call generate_report() with project name, output directory, format='html', and template='qc_report' to render the QC report."
- [methods] Call export() to write processed data, sample metadata, and feature metadata as tab-delimited text files: "Call export() with format='metaboprep' to write processed data, sample metadata, and feature metadata as tab-delimited text files to the specified output directory."
- [methods] Verify that HTML report file and tab-delimited exports exist in output directory: "Verify that the HTML report file (project_name_metaboprep_qc_report.html) and associated tab-delimited exports (.txt/.tsv) exist in the output directory."
- [intro] Generate summary data as tab-delimited text file and html report: "Provide useful summary data in the form of tab-delimited text file and a html report"
- [readme] Metaboprep generates tab-delimited text files and HTML report as outputs: "Provide useful summary data in the form of tab-delimited text file and a html report."
