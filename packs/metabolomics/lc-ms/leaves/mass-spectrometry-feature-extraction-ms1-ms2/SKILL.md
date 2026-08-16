---
name: mass-spectrometry-feature-extraction-ms1-ms2
description: Use when when you have raw mzML files from LC-MS/MS metabolomics experiments and need to convert them into a structured feature table with accurate mass, retention time, and MS2 spectral data linked to a reference compound list.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3637
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - shinyscreen
  - R
  - devtools
  - Docker
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-feature-extraction-ms1-ms2

## Summary

Automated extraction of MS1 precursor ion features and associated MS2 fragment spectra from high-resolution mass spectrometry data using coarse/fine mass error calibration, EIC windowing, and retention time filtering. Applied to untargeted metabolomics workflows to generate a feature table with quality control metrics for downstream prescreening and statistical analysis.

## When to use

When you have raw mzML files from LC-MS/MS metabolomics experiments and need to convert them into a structured feature table with accurate mass, retention time, and MS2 spectral data linked to a reference compound list. Typical trigger: possession of multi-sample ionization-mode-specific mzML files (e.g., positive/negative mode pairs) and a CSV compound list with target m/z values.

## When NOT to use

- Input is already a pre-processed feature table or matrix — use this skill only on raw or minimally processed mzML files.
- Compound list is missing or incompatible (e.g., no m/z column or incorrect CSV format) — extraction requires a valid reference list.
- Data is from a different MS instrument type or file format (e.g., NetCDF, .raw) without prior conversion to mzML — Shinyscreen is designed for mzML input.

## Inputs

- mzML files (raw LC-MS/MS data, typically one per sample/ionization mode)
- AAs_CmpdList.csv (reference compound list with m/z, retention time, and compound metadata)
- project configuration (selected Project and Data directory paths)

## Outputs

- CSV feature table (rows: compounds; columns: samples/tags with intensity or peak area values)
- Feature-level quality control metadata (adduct, tag, QC score per entry)
- MS2 spectral data associated with each detected feature
- EIC chromatogram data for visualization

## How to apply

Load tagged mzML files (each assigned a unique ionization mode adduct such as [M+H]+ or [M−H]−) into Shinyscreen. Configure MS1 extraction parameters: set coarse error and fine error thresholds (defaults provided), define EIC window width, and retention time window constraints. Click Extract to perform isotope clustering and EIC window extraction across all files using the compound list reference. The pipeline automatically matches detected features to compound entries by m/z within the fine error tolerance and retention time bounds, then generates feature-by-sample matrices and MS2 spectra associations. Validate output by confirming all target compounds are represented as rows in the resulting feature table with populated quality control scores and tag/adduct metadata.

## Related tools

- **shinyscreen** (Primary interactive application for configuring extraction parameters, loading and tagging mzML files, running MS1/MS2 extraction, and exporting feature tables with QC metadata.) — https://gitlab.com/uniluxembourg/lcsb/eci/shinyscreen
- **R** (Host environment for Shinyscreen installation and execution; required for devtools deployment.)
- **devtools** (R package used to install Shinyscreen from the GitLab repository.)
- **Docker** (Container platform for running Shinyscreen in an isolated, reproducible environment without local R dependencies.)

## Evaluation signals

- Exported CSV feature table contains one row per target compound from the reference list with non-zero intensity values in at least one sample/tag column.
- All rows include metadata columns for adduct (e.g., [M+H]+, [M−H]−), tag (e.g., KO+, WT−), and quality control score; no missing values in these columns.
- Retention time and m/z values for each detected feature fall within the configured extraction windows (fine error and RT bounds).
- MS2 spectral data and EIC chromatograms are accessible in the Results Explorer for a representative subset of compounds; visual inspection confirms peaks are present at expected retention times.
- Feature intensity distribution across samples is consistent with biological or technical replicate structure (e.g., replicates cluster together, condition-based samples show expected separation).

## Limitations

- Extraction relies on accurate m/z values and approximate retention times in the compound list; features with poor reference data may be missed or misaligned.
- Default extraction parameters (coarse/fine error, EIC window, RT window) may require manual tuning for non-standard instruments, extreme mass ranges, or highly complex samples.
- MS2 spectral quality depends on input data; samples with low precursor intensity or poor fragmentation will yield sparse or absent MS2 data.
- No built-in isotope pattern deconvolution or in-source fragmentation filtering; manual curation of the prescreen results may be necessary in complex matrices.
- No changelog documentation provided; reproducibility across Shinyscreen versions may require explicit version pinning.

## Evidence

- [methods] Shinyscreen is a Shiny application for visualizing and analyzing high resolution mass spectrometry data.: "Shinyscreen is a Shiny application for visualizing and analyzing high resolution mass spectrometry data."
- [methods] Click the Extract button to perform MS1 coarse/fine error and EIC window extraction.: "navigate to the Configure, Extract, Prescreen tab. Click the Extract button to perform MS1 coarse/fine error and EIC window extraction"
- [methods] Extract and Prescreen steps followed by Results Explorer tab for visualization and export.: "The Shinyscreen pipeline includes Extract and Prescreen steps in the Configure, Extract, Prescreen tab, followed by a Results Explorer tab where results can be visualized and exported."
- [methods] Assign unique tags to each file and select appropriate adduct from dropdown.: "assign a unique tag to each file (such as KO+, STD+, or WT+) in the tagging section. Next, select the appropriate adduct from the dropdown list"
- [methods] Default parameters for MS1 coarse and fine error, EIC window, and retention time window.: "extraction section will display a set of default parameters for MS1 coarse and fine error, EIC window, and retention time window"
- [methods] Exported CSV file contains rows for all detected compounds with quality control scores and adduct/tag metadata.: "the exported CSV file contains rows for all detected compounds with quality control scores and adduct/tag metadata for each entry."
