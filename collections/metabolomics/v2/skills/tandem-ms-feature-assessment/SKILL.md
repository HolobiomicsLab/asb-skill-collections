---
name: tandem-ms-feature-assessment
description: Use when after importing raw peak tables from tandem MS/MS preprocessing
  software (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - R
  - ggplot
  - mpactr
  - data.table
  - ggplot2
  - plotly
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.2c04632
  title: MPACT
evidence_spans:
- To import these data into R, use the mpactr function
- We will be using multiple libraries for data analysis and visualization
- creating an interactive plot of input features and the filters they failed, if any,
  using `ggplot` and `plotly`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mpactr_cq
    doi: 10.1021/acs.analchem.2c04632
    title: MPACT
  dedup_kept_from: coll_mpactr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04632
  all_source_dois:
  - 10.1021/acs.analchem.2c04632
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tandem-ms-feature-assessment

## Summary

Assess and filter tandem MS/MS features to remove peak selection errors, isotopic misassignments, and non-reproducible ions introduced during preprocessing. This skill chains independent filter operations on MS1 feature tables to identify high-quality compounds for downstream metabolomics analysis.

## When to use

Apply this skill after importing raw peak tables from tandem MS/MS preprocessing software (e.g., Progenesis, MS-DIAL) when you need to remove mispicked isotopic patterns, carryover from solvent/media blanks, non-reproducible technical replicate features, or in-source fragment ions before conducting fold-change analysis, correlation studies, or compound annotation.

## When NOT to use

- Input is already a curated feature table that has been manually validated or processed by a different QC pipeline; mpactr filters assume raw preprocessing artifacts are still present.
- Tandem MS/MS data are from a non-standard preprocessing tool (e.g., vendor-specific software not compatible with Progenesis or MS-DIAL import formats); import_data() may fail or produce incorrect peak assignments.
- The analysis goal does not require removal of isotopic misassignments or blank carryover (e.g., if working with targeted assays with predefined accurate m/z values and retention times).

## Inputs

- peak_table_file_path (CSV or other Progenesis/MS-DIAL format containing m/z, retention time, and ion abundance across samples)
- metadata_file_path (CSV mapping sample names to technical replicate groups and biological groups)
- mpactr object (after import_data() call)

## Outputs

- filtered mpactr object (with per-ion filtering status attached)
- qc_summary() data.table (compound IDs with filtering status: 'passed', 'mispicked', 'group', 'replicability', 'insource')
- feature table (reduced set of high-quality MS1 features ready for downstream analysis)

## How to apply

Load the peak table and metadata into mpactr using import_data(), then apply a chain of independent filters in sequence: (1) filter_mispicked_ions() with parameters (ringwin, isowin, trwin, max_iso_shift, merge_peaks, merge_method) to merge incorrectly split isotopic patterns; (2) filter_group() to remove features overrepresented in blank samples (solvent or media blanks); (3) filter_cv() with a coefficient-of-variation threshold (e.g., cv_threshold = 0.2) to remove non-reproducible features between technical replicates; and (4) filter_insource_ions() to remove fragment ions created during ionization. Use copy_object = FALSE to chain filters efficiently. After filtering, call qc_summary() to generate a per-ion status table documenting which compounds passed or failed (and which filter caused failure), enabling transparent QC reporting and visualization.

## Related tools

- **mpactr** (Core filtering and QC package: provides filter_mispicked_ions(), filter_group(), filter_cv(), filter_insource_ions(), qc_summary(), and import_data() functions to execute the full assessment workflow.) — https://github.com/mums2/mpactr
- **R** (Runtime environment and language for loading, chaining, and inspecting filter operations on mpactr objects.)
- **data.table** (Efficient data manipulation library used by mpactr to group and pivot qc_summary() output for status counts and percentages.)
- **ggplot2** (Visualization library used to render treemap and other diagnostic plots showing filter fate and ion status distribution.)
- **plotly** (Interactive plotting library paired with ggplot to create clickable visualizations of input features and their filter outcomes.)

## Examples

```
library(mpactr); data <- import_data('cultures_peak_table.csv', 'cultures_metadata.csv', format='Progenesis'); filtered <- filter_mispicked_ions(data, ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, merge_method='sum', copy_object=FALSE); filtered <- filter_group(filtered, group_to_remove='Solvent_Blank', copy_object=FALSE); filtered <- filter_cv(filtered, cv_threshold=0.2, copy_object=FALSE); filtered <- filter_insource_ions(filtered, copy_object=FALSE); qc_table <- qc_summary(filtered); write.csv(qc_table, 'qc_summary_output.csv')
```

## Evaluation signals

- qc_summary() output contains all input compound IDs with no missing entries; each row has a valid status label ('passed' or one of the four failure modes: 'mispicked', 'group', 'replicability', 'insource').
- The number of features removed by each filter is non-negative and monotonically decreases (or remains stable) as you chain filters; no feature count increases after applying a filter.
- Technical replicate correlations improve after filtering (higher Pearson/Spearman r values computed on the filtered feature table vs. the raw table), confirming that filter_cv() and filter_mispicked_ions() are removing inconsistent signals.
- Blank sample (solvent/media) feature abundance is substantially reduced in the filtered table; verify by comparing mean ion intensity in blank samples before and after filter_group().
- Treemap visualization of qc_summary() counts shows logical distribution: a small percentage of features failing filters (typically 10–30% removed across all filters combined) and the majority passing, consistent with the intent to remove preprocessing artifacts rather than true biology.

## Limitations

- Filter parameters (ringwin, isowin, trwin, max_iso_shift, cv_threshold) are not data-adaptive; users must supply thresholds a priori, and optimal settings are sample-type and instrument-dependent. The article recommends cv_threshold = 0.2 as a starting point but does not provide guidance for tuning other parameters.
- Filters are independent, meaning they do not account for correlations between failure modes (e.g., a feature that is mispicked may also be non-reproducible); some features may fail multiple filters but are counted only once in qc_summary().
- filter_insource_ions() requires external reference patterns of in-source fragments; if not supplied or if the metabolite class is not in the reference database, the filter may have low sensitivity.
- The method assumes technical replicates are properly labeled in the metadata; mislabeled replicates will cause filter_cv() to remove true biological signals or retain noise.
- Performance with very large peak tables (>10,000 features) is not discussed; memory efficiency gains from copy_object = FALSE may be offset by computational cost of isotopic pattern matching in filter_mispicked_ions().

## Evidence

- [readme] mpactr is a collection of filters for the purpose of identifying high quality MS1 features by correcting peak selection errors introduced during the pre-processing of tandem mass spectrometry data.: "mpactr is a collection of filters for the purpose of identifying high quality MS1 features by correcting peak selection errors introduced during the pre-processing of tandem mass spectrometry data."
- [readme] filter_mispicked_ions(): removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing.: "filter_mispicked_ions(): removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing."
- [readme] filter_group(): removal of features overrepresented in a specific group of samples; for example removal of features present in solvent blanks due to carryover between samples.: "filter_group(): removal of features overrepresented in a specific group of samples; for example removal of features present in solvent blanks due to carryover between samples."
- [readme] filter_cv(): removal of non-reproducible features, or those that are inconsistent between technical replicates.: "filter_cv(): removal of non-reproducible features, or those that are inconsistent between technical replicates."
- [readme] filter_insource_ions(): removal of fragment ions created during the first ionization in the tandem MS/MS workflow.: "filter_insource_ions(): removal of fragment ions created during the first ionization in the tandem MS/MS workflow."
- [readme] All filters are independent, meaning they can be used to create a project-specific workflow: "All filters are independent, meaning they can be used to create a project-specific workflow"
- [abstract] We recommend using the default `copy_object = FALSE` as this makes for an extremely fast and memory-efficient way to chain mpactr filters together: "We recommend using the default `copy_object = FALSE` as this makes for an extremely fast and memory-efficient way to chain mpactr filters together"
- [methods] The qc_summary() function returns a data.table with compound ids and their filtering status, where failed ions are labeled with the name of the filter they failed.: "The qc_summary() function returns a data.table with compound ids and their filtering status, where failed ions are labeled with the name of the filter they failed."
- [methods] To import these data into R, use the mpactr function `import_data()`, which has the arguments: `peak_table_file_path` and `metadata_file_path`.: "To import these data into R, use the mpactr function `import_data()`, which has the arguments: `peak_table_file_path` and `metadata_file_path`."
