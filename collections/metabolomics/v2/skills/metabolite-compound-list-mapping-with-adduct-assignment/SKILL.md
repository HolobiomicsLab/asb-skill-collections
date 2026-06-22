---
name: metabolite-compound-list-mapping-with-adduct-assignment
description: Use when when you have mzML files from targeted or untargeted metabolomics experiments run in multiple ionization modes (e.g., KO_NEG, KO_POS, STD_NEG, STD_POS, WT_NEG, WT_POS) and a CSV list of reference compounds (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - shinyscreen
  - R
  - devtools
  - Docker
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

# metabolite-compound-list-mapping-with-adduct-assignment

## Summary

Upload a curated compound list (CSV) and assign ionization-mode-specific adducts ([M+H]+ or [M−H]−) to each mzML data file in Shinyscreen, enabling accurate feature extraction and prescreening against known metabolites. This skill bridges experimental design (positive/negative ionization modes) and computational mass-spec processing.

## When to use

When you have mzML files from targeted or untargeted metabolomics experiments run in multiple ionization modes (e.g., KO_NEG, KO_POS, STD_NEG, STD_POS, WT_NEG, WT_POS) and a CSV list of reference compounds (e.g., amino acids, lipids) that you want to map to detected features with mode-appropriate adduct masses. Use this skill before MS1 extraction and prescreening to ensure that the extraction window and feature detection are calibrated to the correct m/z values for each ionization mode.

## When NOT to use

- If you have only a single ionization mode (e.g., all files are positive-mode) and do not need multi-mode comparison—the skill's multi-mode tagging and adduct assignment overhead is unnecessary.
- If your compound list already contains ion-specific masses (e.g., [M+H]+ m/z values pre-calculated) rather than neutral masses—you would need to either recalculate the list or manually adjust adduct assignments, making the CSV upload less straightforward.
- If you are performing discovery-mode metabolomics without a reference compound list; use an untargeted extraction workflow instead.

## Inputs

- CSV compound list file (e.g., AAs_CmpdList.csv with columns: compound name, neutral mass, chemical formula)
- mzML mass spectrometry data files (six or more files, organized by sample type and ionization mode)
- Shinyscreen project directory structure (project/ and data/ folders)

## Outputs

- Tagged data table with compound list assignment, file tags, and adduct assignments for each mzML file
- Project metadata file saved in Shinyscreen (prerequisite for Extract and Prescreen steps)
- m/z-corrected feature extraction windows used by downstream Extract step

## How to apply

In Shinyscreen's Project tab, first upload the reference compound list CSV (e.g., AAs_CmpdList.csv) via 'Select Compound List'. Then load your mzML files via 'Select datafiles' and assign a unique tag to each file (e.g., KO+, KO−, STD+, STD−, WT+, WT−) to identify genotype and ionization mode. For each tagged file, select the appropriate adduct from a dropdown list—[M+H]+ for positive-mode files, [M−H]− for negative-mode files—which determines the m/z offset applied during subsequent MS1 coarse/fine error correction and EIC window extraction. Select all tagged files and click 'Fill table' to populate the data table, then save the project. The adduct assignment ensures that neutral mass in the compound list is converted to the correct measured ion mass (neutral mass + adduct mass offset) for each file, enabling accurate feature-to-compound matching during extraction and prescreening.

## Related tools

- **shinyscreen** (web UI for uploading compound lists, tagging mzML files, assigning adducts, and configuring the Extract and Prescreen pipeline) — https://gitlab.com/uniluxembourg/lcsb/eci/shinyscreen
- **R** (runtime environment for Shinyscreen application and downstream analysis)
- **devtools** (R package manager for installing Shinyscreen from source)
- **Docker** (containerization for reproducible Shinyscreen deployment with preset project/data directories)

## Evaluation signals

- The 'Fill table' action successfully populates a data table with rows for each mzML file, each row displaying the correct tag, assigned adduct ([M+H]+ or [M−H]−), and compound set (reference to the uploaded CSV).
- After project save and navigation to 'Configure, Extract, Prescreen' tab, the Extract step runs without errors and produces EIC windows that are correctly offset by the assigned adduct mass (verify by spot-checking one known compound: neutral mass + adduct offset should match the extracted m/z range).
- Prescreening results (in 'Results Explorer' > 'Save summary table') contain rows only for features matching the adduct and ionization mode of each file (e.g., no [M−H]− features in a positive-mode file).
- The exported CSV summary table includes columns for adduct, tag, compound name, measured m/z, neutral mass match, and quality control score, confirming end-to-end mapping from CSV to detected features.
- Project metadata file (.rds or similar) is successfully written to the project directory, allowing the project to be reopened and Extract/Prescreen steps to be rerun without re-entering compound list or adduct assignments.

## Limitations

- Adduct assignment is currently a manual dropdown selection per file; no automatic detection based on file name or header metadata. If many files must be tagged, the UI can become tedious.
- The compound list CSV must be in a specific format (e.g., columns for name, neutral mass, formula); malformed or missing columns will cause silent failures or incomplete matching during extraction.
- Adduct assignment is per-file, not per-compound; all instances of a compound are searched with the same adduct offset within a file, so dual-mode adducts (e.g., [M+H]+ and [M+Na]+ in the same sample) require separate file entries or manual post-processing.
- No changelog or versioning documented for Shinyscreen, so reproducibility across installations or over time may be affected by updates to adduct definitions or m/z calculation logic.

## Evidence

- [methods] assign a unique tag to each file (such as `KO+`, `STD+`, or `WT+`) in the tagging section. Next, select the appropriate adduct from the dropdown list: "assign a unique tag to each file (such as `KO+`, `STD+`, or `WT+`) in the tagging section. Next, select the appropriate adduct from the dropdown list"
- [methods] Click the **"Select Compound List"** button in the UI and select `AAs_CmpdList.csv` from your `project/` directory.: "Click the **"Select Compound List"** button in the UI and select `AAs_CmpdList.csv` from your `project/` directory."
- [methods] select all the files and click **"Fill table"**. This action will populate the data table: "select all the files and click **"Fill table"**. This action will populate the data table"
- [methods] make sure to save the project from the **Project** tab, this is a crucial step before proceeding for extraction and prescreening.: "make sure to save the project from the **Project** tab, this is a crucial step before proceeding for extraction and prescreening."
- [methods] extraction section will display a set of default parameters for MS1 coarse and fine error, EIC window, and retention time window: "extraction section will display a set of default parameters for MS1 coarse and fine error, EIC window, and retention time window"
- [other] the exported CSV file contains rows for all detected compounds with quality control scores and adduct/tag metadata for each entry.: "the exported CSV file contains rows for all detected compounds with quality control scores and adduct/tag metadata for each entry."
