---
name: chromatographic-peak-detection-retention-time-alignment
description: Use when you have multiple high-resolution mzML files from LC-MS/MS experiments (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - shinyscreen
  - R
  - devtools
  - Docker
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1186/s13321-025-01044-x
  title: Shinyscreen
evidence_spans:
- Shinyscreen is a Shiny application for visualizing and analyzing high resolution mass spectrometry data.
- Shinyscreen can be installed in R via `devtools`
- docker run -p 3838:3838 \ -v C:/your/path/project:/home/ssuser/projects
- docker pull registry.gitlab.com/uniluxembourg/lcsb/eci/shinyscreen:master
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_shinyscreen_cq
    doi: 10.1186/s13321-025-01044-x
    title: Shinyscreen
  dedup_kept_from: coll_shinyscreen_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-025-01044-x
  all_source_dois:
  - 10.1186/s13321-025-01044-x
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-peak-detection-retention-time-alignment

## Summary

Detect and align chromatographic peaks across LC-MS/MS runs by extracting ion chromatograms (EICs) with mass accuracy and retention time windows, then applying quality control checks to identify and filter metabolite features. This skill is essential for reproducible untargeted metabolomics when working with high-resolution mzML data and reference compound lists.

## When to use

Apply this skill when you have multiple high-resolution mzML files from LC-MS/MS experiments (e.g., KO, WT, and STD samples in positive and negative ionization modes), a validated compound list with expected m/z values, and need to extract and align detected metabolite peaks across samples to build a prescreening summary table for downstream analysis or export.

## When NOT to use

- Input mzML files are already centroided or preprocessed by external tools; Shinyscreen expects raw or vendor-centroided data with defined extraction parameters.
- Compound list is missing or contains incomplete m/z values; the skill requires accurate mass targets to define EIC windows and coarse/fine error tolerances.
- You require post-hoc retention time alignment across runs with statistical modeling; Shinyscreen's retention time window is fixed per extraction and does not perform dynamic warping or pooled calibration.

## Inputs

- mzML files (high-resolution LC-MS/MS data; e.g., KO_NEG.mzML, WT_POS.mzML)
- compound list CSV (e.g., AAs_CmpdList.csv with m/z values, names, and metadata)
- file tags and adduct assignments ([M+H]+ or [M−H]− for each file)
- Shinyscreen project configuration (project and data directory paths)

## Outputs

- extracted ion chromatograms (EICs) for each compound per sample
- prescreening summary table (CSV) with rows per compound, columns for QC scores, adduct, tag, m/z, and detection metadata
- quality-filtered feature list ready for results exploration and export

## How to apply

After configuring Shinyscreen with project and data directories and uploading a compound list (e.g., AAs_CmpdList.csv) and tagged mzML files, navigate to the Configure, Extract, Prescreen tab and click Extract to perform MS1 coarse and fine error correction and EIC window extraction using default parameters (coarse error, fine error, EIC window width, and retention time window). Then click Prescreen to run quality control checks on the extracted features, which filters peaks by signal quality and compound detection consistency. Finally, export the prescreening results via the Results Explorer tab as a CSV summary table containing QC scores, adduct assignments, and sample tags for each detected compound, enabling verification that peaks were correctly detected and aligned across the sample cohort.

## Related tools

- **shinyscreen** (interactive Shiny application for configuring, extracting, and prescreening LC-MS/MS peaks with EIC visualization and QC filtering) — https://gitlab.com/uniluxembourg/lcsb/eci/shinyscreen
- **R** (programming language runtime for Shinyscreen installation and execution)
- **devtools** (R package manager for installing Shinyscreen from source)
- **Docker** (containerization platform for deploying Shinyscreen without local R/dependency installation)

## Evaluation signals

- Exported CSV file contains one row per detected compound with non-null QC scores, adduct tags, sample identifiers, and m/z values.
- Row count in prescreening summary matches or is less than the input compound list size (no spurious duplication after extraction).
- EIC chromatograms displayed in Results Explorer show clear peaks at expected retention times for positive control and standard samples (STD_POS, STD_NEG).
- QC scores are numeric and bounded (e.g., 0–1 or 0–100 range); compounds failing QC thresholds are absent or marked as low-quality in the output table.
- File tags and adduct assignments are correctly propagated to the summary table (verify tag columns match input assignments and adduct columns reflect [M+H]+ or [M−H]− choices).

## Limitations

- Default MS1 coarse/fine error and EIC window parameters may require manual tuning for non-standard compound classes or instrument-specific mass calibration drift; no automated parameter optimization is reported in the article.
- Retention time window is static per extraction run; dynamic retention time alignment across cohorts is not supported, potentially missing co-eluting isomers or poorly retained compounds.
- Prescreening QC checks are applied uniformly across all compounds and samples; no sample-group-specific or compound-class-specific filtering rules are documented.
- No changelog or version history is provided, limiting reproducibility across tool updates.

## Evidence

- [methods] extraction_with_default_params: "Navigate to the 'Configure, Extract, Prescreen' tab and click the 'Extract' button to perform MS1 coarse/fine error and EIC window extraction using default parameters."
- [methods] prescreen_qc_checks: "Click the 'Prescreen' button to run quality control checks on extracted features."
- [methods] export_summary_table: "Navigate to the 'Results Explorer' tab and click 'Save summary table' to export the prescreening results as CSV."
- [methods] validation_csv_content: "the exported CSV file contains rows for all detected compounds with quality control scores and adduct/tag metadata for each entry."
- [methods] eic_visualization: "simply click on the corresponding row in the table. This will open up the extracted ion chromatogram (EIC), MS2 peak and MS2 spectrum"
- [methods] shinyscreen_definition: "Shinyscreen is a Shiny application for visualizing and analyzing high resolution mass spectrometry data."
- [methods] default_parameters: "extraction section will display a set of default parameters for MS1 coarse and fine error, EIC window, and retention time window"
