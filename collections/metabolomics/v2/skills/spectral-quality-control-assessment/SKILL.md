---
name: spectral-quality-control-assessment
description: Use when after MS1 extraction (coarse/fine error correction, EIC window
  extraction) and retention time windowing on a set of mzML files tagged with ionization
  mode and compound adducts.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - shinyscreen
  - R
  - devtools
  - Docker
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1186/s13321-025-01044-x
  title: Shinyscreen
evidence_spans:
- Shinyscreen is a Shiny application for visualizing and analyzing high resolution
  mass spectrometry data.
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

# spectral-quality-control-assessment

## Summary

Execute quality control checks on extracted high-resolution mass spectrometry features via the Shinyscreen Prescreen step to assign QC scores and filter compounds before downstream analysis. This skill evaluates the integrity and reliability of detected features across MS1 and MS2 data.

## When to use

Apply this skill after MS1 extraction (coarse/fine error correction, EIC window extraction) and retention time windowing on a set of mzML files tagged with ionization mode and compound adducts. Use it when you need to assess the reliability of detected features before visualization, grouping, or export of prescreening summary tables for publication or further analysis.

## When NOT to use

- Input files have not yet undergone MS1/MS2 extraction or lack assigned tags and adduct annotations.
- Prescreen results are already available and only visualization or re-sorting is needed.
- Low-resolution or unit-mass accuracy data where MS1 coarse/fine error correction cannot be reliably applied.

## Inputs

- extracted mzML feature table from MS1/MS2 extraction step (internal Shinyscreen format)
- MS1 coarse error, MS1 fine error, EIC window, and retention time window parameters
- tagged and adduct-assigned file metadata (e.g., KO+, KO−, STD+, STD−, WT+, WT− with [M+H]+ or [M−H]− adducts)

## Outputs

- prescreening summary table (CSV format) with rows for each detected compound
- quality control scores and metadata (adduct, tag) for each feature
- grouped and sorted results filterable by adduct, tag, quality, or m/z

## How to apply

After navigating to the Configure, Extract, Prescreen tab in Shinyscreen and completing MS1/MS2 extraction with default or user-adjusted parameters (MS1 coarse error, MS1 fine error, EIC window, retention time window), click the Prescreen button to run automated quality control checks on all extracted features. The Prescreen step applies internal QC criteria (not explicitly enumerated in the article) to assign quality scores and metadata tags (adduct, file tag) to each detected compound row. Proceed to the Results Explorer tab, where you can group and sort results by adduct, tag, quality score, or m/z using dropdown filters to identify high-confidence features. Export the filtered prescreening summary table as CSV for validation: the file should contain rows for all detected compounds with quality control scores and adduct/tag metadata for each entry. Use the Plot Controls panel to refine retention time and intensity ranges if needed to support manual spot-checking of borderline QC assignments.

## Related tools

- **shinyscreen** (R Shiny application that implements the Configure, Extract, Prescreen workflow and provides the interactive Prescreen button and Results Explorer for QC assessment and export.) — https://gitlab.com/uniluxembourg/lcsb/eci/shinyscreen
- **R** (Runtime environment for executing Shinyscreen and its underlying statistical and mass spectrometry processing libraries.)
- **devtools** (R package manager used to install Shinyscreen from source repository.)
- **Docker** (Containerization platform for reproducible deployment of Shinyscreen with all dependencies pre-configured.)

## Evaluation signals

- Exported CSV file contains one row per detected compound with no missing quality control score or adduct/tag metadata fields.
- All compounds from the uploaded mzML files are represented in the prescreening summary table (no unexplained omissions).
- Quality scores are numeric, span a consistent range (e.g., 0–1 or 0–100), and show variation across compounds indicating discrimination between high- and low-confidence features.
- Grouping and sorting by adduct, tag, quality, or m/z produces expected reordering of rows without data loss or corruption.
- EIC and MS2 spectrum visualizations for randomly selected compounds (clicked from the Results Explorer table) display coherent signals consistent with their assigned QC scores.

## Limitations

- QC criteria and scoring algorithm are not explicitly documented in the article, making it difficult to audit or adjust thresholds.
- Default MS1 coarse/fine error and EIC window parameters may not be optimal for all compound classes or ionization modes; user adjustment may be necessary.
- Prescreen step does not provide per-compound diagnostic messages (e.g., reason for low QC score), limiting troubleshooting of failing features.

## Evidence

- [methods] Prescreen step definition and purpose: "Click the **Prescreen** button to run quality control checks."
- [methods] Prescreen output validation criterion: "the exported CSV file contains rows for all detected compounds with quality control scores and adduct/tag metadata for each entry."
- [methods] Results Explorer filtering and grouping capability: "You can group and sort the results using dropdown filters like `adduct`, `tag`, `quality`, or `m/z`."
- [methods] Extraction parameter defaults that precede Prescreen: "extraction section will display a set of default parameters for MS1 coarse and fine error, EIC window, and retention time window"
- [methods] Plot Controls refinement during QC assessment: "Plot Controls panel allows users to refine the display by adjusting the retention time and intensity ranges."
