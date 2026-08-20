---
name: ms-adduct-annotation-and-recognition
description: Use when when processing LC-MS peak tables from isotope tracing experiments where multiple ionization adducts ([M+H]+, [M+Na]+, [M+NH4]+, etc.) and in-source fragments have generated redundant features at different m/z values that represent the same underlying metabolite.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - devtools
  - BiocManager
  - dplyr
  - tidyr
  - readr
  - stringr
  - tibble
  - purrr
  - ggplot2
  - IsoPairFinder
  techniques:
  - LC-MS
derived_from:
- doi: 10.1101/2021.12.05.471237v2
  title: isopair
evidence_spans:
- To install the **IsoPairFinder** package, you can use the following command in R
- if (!require(devtools))
- if (!require(BiocManager))
- required_pkgs <- c("dplyr","tidyr","readr", "stringr", "tibble", "purrr",
- devtools::install_github("DoddLab/IsoPairFinder")
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_isopairfinder_cq
    doi: 10.1101/2021.12.05.471237v2
    title: isopair
  dedup_kept_from: coll_isopairfinder_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2021.12.05.471237v2
  all_source_dois:
  - 10.1101/2021.12.05.471237v2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ms-adduct-annotation-and-recognition

## Summary

Automated recognition and annotation of MS adducts, neutral losses, and in-source fragments to merge redundant LC-MS features into canonical peak identities. This skill enables deduplication of isotope-labeled and unlabeled peak tables before pairing intermediates in stable isotope tracing metabolomics.

## When to use

When processing LC-MS peak tables from isotope tracing experiments where multiple ionization adducts ([M+H]+, [M+Na]+, [M+NH4]+, etc.) and in-source fragments have generated redundant features at different m/z values that represent the same underlying metabolite. Apply this skill as a prerequisite step before pairing 12C/13C features, especially when comparing unlabeled (C12) and labeled (C13) peak tables where adduct patterns may differ between conditions.

## When NOT to use

- When your peak table has already been deduplicated or merged by an upstream tool (e.g., XCMS grouping or MS-DIAL adduct clustering) — applying recognition a second time may remove valid features.
- When analyzing non-isotope-labeled metabolomics data where adduct annotation alone (without 12C/13C pairing context) is the goal — use a dedicated adduct annotation tool instead.
- When working with data from instruments or ionization methods where adduct patterns are non-standard or instrument-specific and not covered by the built-in recognition rules.

## Inputs

- peak_table_C12.csv (unlabeled peak area table with m/z, retention time, and peak intensities)
- peak_table_C13.csv (labeled peak area table with m/z, retention time, and peak intensities)
- sample_info.csv (sample metadata including group, tracer_group, and sample identifiers)
- file path to project directory containing sample groups and raw data folders

## Outputs

- Merged/deduplicated peak table with redundant adducts and neutral losses consolidated
- tracer_pair_result.xlsx (ion pair matches between deduplicated C12 and C13 features)
- Diagnostic PDF plots summarizing pairing results and statistical summaries

## How to apply

Enable the `is_recognize_adducts` parameter (set to TRUE) within the find_intemidates function call. The function accepts the unlabeled peak table (C12.csv), labeled peak table (C13.csv), sample metadata, and analysis path. Internally, the workflow merges redundant adduct variants and neutral-loss derivatives across the peak tables using mass-to-charge (m/z) and retention time (RT) tolerances (mz_tol=10 ppm, rt_tol=0.05 min by default). This preprocessing consolidates multiple ionization states of the same metabolite into single canonical features before downstream differential analysis and 12C/13C pairing. The adduct recognition reduces false negatives in tracer-pair matching by ensuring that isotope pairs are compared at the consolidated feature level, not at the raw peak level where adduct variants could obscure true matches.

## Related tools

- **IsoPairFinder** (Primary workflow orchestrator that embeds adduct recognition as a preprocessing step within find_intemidates function) — https://github.com/DoddLab/IsoPairFinder
- **dplyr** (Data manipulation and feature merging during adduct consolidation)
- **tidyr** (Data reshaping and normalization of peak tables before adduct matching)
- **readr** (Efficient reading of peak table CSV files and sample metadata)
- **ggplot2** (Visualization of adduct recognition results and pairing diagnostics in PDF output)

## Examples

```
find_intemidates(peak_table_unlabel = 'peak_table_C12.csv', peak_table_label = 'peak_table_C13.csv', sample_info = 'sample_info.csv', path = './', control_group = c('WT'), case_group = c('MUTANT'), mz_tol = 10, rt_tol = 0.05, is_recognize_adducts = TRUE)
```

## Evaluation signals

- Verify that redundant m/z peaks within mz_tol (±10 ppm) and rt_tol (±0.05 min) windows have been consolidated into single canonical features in the output peak table.
- Check tracer_pair_result.xlsx for higher pairing success rate (more ion pair matches) compared to running find_intemidates with is_recognize_adducts=FALSE.
- Inspect diagnostic PDF plots to confirm that adduct variants (e.g., [M+H]+ and [M+Na]+ of the same compound) are represented by a single merged feature line, not separate traces.
- Validate that the number of unique features in the merged output is fewer than the input (indicating successful consolidation) while retaining the biochemically relevant intermediate identifications.
- Cross-check peak intensity distributions — merged features should show combined or representative intensity values that reflect the original adduct variants.

## Limitations

- Adduct recognition rules are built-in and may not cover non-standard or exotic ionization adducts specific to particular instruments or sample matrices.
- The fixed mz_tol (10 ppm) and rt_tol (0.05 min) may be too stringent or too permissive depending on mass spectrometer resolution and chromatographic peak width; manual tuning may be needed for unusual sample types.
- Neutral loss patterns vary by metabolite class — the built-in recognition may misattribute or fail to detect in-source fragments for understudied compound classes.
- No changelog is available in the repository documentation, so the evolution and validation history of adduct recognition rules cannot be independently reviewed.

## Evidence

- [readme] The find_intemidates workflow provides an end-to-end workflow serving this objective, including (1) differential analysis; (2) merging of the redundant LC-MS features (adducts, neutral losses, and in-source fragments); (3) pairing 12C/13C features to determine potential intermediates.: "merging of the redundant LC-MS features (adducts, neutral losses, and in-source fragments)"
- [other] Execute find_intemidates function with mz_tol=10 ppm, rt_tol=0.05 min, p_value_cutoff=0.05, fold_change_cutoff=20, adduct recognition enabled, comparing hyuA case group against WT control group across positive and negative polarities.: "mz_tol=10 ppm, rt_tol=0.05 min, p_value_cutoff=0.05, fold_change_cutoff=20, adduct recognition enabled"
- [readme] find_intemidates(peak_table_unlabel = 'peak_table_C12.csv', peak_table_label = 'peak_table_C13.csv', sample_info = 'sample_info.csv', path = '~/Project/00_Uric_Acid_project/Data/20250817_submit_test/', polarity = 'positive', control_group = c("WT"), case_group = c('MUTANT'), mz_tol = 10, rt_tol = 0.05, p_value_cutoff = 0.05, p_adjust = TRUE, fold_change_cutoff = 20, is_recognize_adducts = TRUE): "is_recognize_adducts = TRUE"
- [other] Generate tracer_pair_result.xlsx containing identified ion pair matches between unlabeled and labeled peak tables. Produce diagnostic PDF plots summarizing pairing results and statistical summaries.: "Generate tracer_pair_result.xlsx containing identified ion pair matches between unlabeled and labeled peak tables. Produce diagnostic PDF plots summarizing pairing results"
