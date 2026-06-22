---
name: isotope-labeling-data-integration
description: Use when you have LC-MS peak tables from parallel unlabeled and labeled (isotope-traced) sample cohorts, sample metadata defining groups and conditions, and you seek to identify metabolic intermediates that accumulate differentially in a perturbed system (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
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
  - MS-DIAL
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# isotope-labeling-data-integration

## Summary

Integrate unlabeled (C12) and labeled (C13) peak tables with sample metadata to identify intermediate metabolites in stable isotope tracing studies. This skill combines differential analysis, feature redundancy merging, and C12/C13 pairing to screen candidate pathway intermediates.

## When to use

You have LC-MS peak tables from parallel unlabeled and labeled (isotope-traced) sample cohorts, sample metadata defining groups and conditions, and you seek to identify metabolic intermediates that accumulate differentially in a perturbed system (e.g., genetic mutant vs. wild-type) when fed a labeled substrate. Apply this skill when you need to pair detected features across isotope states to prioritize biologically relevant intermediates for validation.

## When NOT to use

- Peak tables are already merged or deduplicated (i.e., adducts and neutral losses have been removed prior to this step).
- You do not have both labeled and unlabeled samples for the same biological conditions; unpaired isotope data cannot be matched.
- The study lacks a clear case–control or perturbed–wild-type design; differential analysis requires distinct group definitions.

## Inputs

- peak_table_unlabeled (C12) – CSV file with m/z, retention time, and peak area columns for each sample
- peak_table_labeled (C13) – CSV file with m/z, retention time, and peak area columns for isotope-labeled samples
- sample_info – CSV or XLSX file with sample names, group assignments, tracer labels (12C vs. 13C), and metadata
- raw mass spectrometry files (mzML) – organized in folders named 'group_tracer_group' (e.g., WT_12C, MUTANT_13C)

## Outputs

- tracer_pair_result.xlsx – table of identified C12/C13 ion pair matches with m/z, retention time, pairing statistics, fold-change, and p-values
- diagnostic PDF plots – visualizations of pairing results, feature distributions, and statistical summaries across polarities and groups

## How to apply

Load the unlabeled peak table (C12), labeled peak table (C13), and sample metadata (CSV/XLSX) into R using readr and dplyr. Execute the find_intemidates() function, specifying mz_tol (e.g., 10 ppm), rt_tol (e.g., 0.05 min), p_value_cutoff (e.g., 0.05), fold_change_cutoff (e.g., 20), and enabling adduct recognition (is_recognize_adducts = TRUE). Define control_group (e.g., WT) and case_group (e.g., MUTANT) to perform differential analysis comparing the perturbed state against the control. The function will merge redundant LC-MS features (adducts, neutral losses, in-source fragments), pair C12 and C13 ions within specified mass and retention time windows, and filter by statistical significance and fold-change thresholds across both positive and negative ionization polarities. Output includes a feature-pair results table (tracer_pair_result.xlsx) and diagnostic PDF plots summarizing pairing and statistical distributions.

## Related tools

- **IsoPairFinder** (Core R package that implements find_intemidates() for differential analysis, feature merging, and C12/C13 pairing) — https://github.com/DoddLab/IsoPairFinder
- **dplyr** (Data manipulation and sample grouping for peak table integration and filtering)
- **readr** (Loading CSV and tabular peak table data into R)
- **tidyr** (Reshaping and pivoting peak tables for sample-wise and feature-wise analysis)
- **ggplot2** (Generation of diagnostic plots for pairing results and statistical summaries)
- **MS-DIAL** (Upstream tool for peak table generation from raw mzML files prior to isotope pairing)

## Examples

```
library(IsoPairFinder)
find_intemidates(peak_table_unlabel = 'peak_table_C12.csv',
                 peak_table_label = 'peak_table_C13.csv',
                 sample_info = 'sample_info.csv',
                 path = '~/Project/Data/',
                 control_group = c('WT'),
                 case_group = c('MUTANT'),
                 mz_tol = 10,
                 rt_tol = 0.05,
                 p_value_cutoff = 0.05,
                 fold_change_cutoff = 20,
                 is_recognize_adducts = TRUE)
```

## Evaluation signals

- tracer_pair_result.xlsx contains non-empty rows with valid C12/C13 m/z pairs within specified mz_tol (10 ppm) and rt_tol (0.05 min) windows.
- Reported p-values and fold-changes meet the specified cutoffs (p < 0.05, fold_change > 20) for intermediates identified as statistically significant between case and control groups.
- Diagnostic PDF plots show distinct clustering or separation between case and control groups in the pairing statistics, indicating biological signal.
- Feature pair matches account for adducts and neutral losses (confirmed by mass defect and expected adduct mass shifts, e.g., +1.007 for [M+H]+).
- Pairing results are generated for both positive and negative ionization modes as specified in the polarity parameter.

## Limitations

- The method requires high-quality peak detection and alignment; poor peak picking or retention time alignment upstream will degrade pairing accuracy.
- Pairing relies on specified mass and retention time tolerances (mz_tol, rt_tol); misalignment or poor parameter choice can result in false positives or missed pairs.
- The workflow assumes the case and control groups are well-defined and biologically distinct; weak phenotypic differences reduce power to identify intermediates by fold-change.
- Adduct recognition is enabled by default but depends on the is_recognize_adducts parameter; disabling it may miss expected pairs if in-source fragmentation or salt-based adducts are present.
- The tool is designed for LC-MS metabolomics and may not directly transfer to other mass spectrometry platforms (e.g., GC-MS) or non-targeted imaging data.

## Evidence

- [other] The find_intemidates workflow accepts unlabeled peak tables (C12), labeled peak tables (C13), sample information metadata, and a file path as inputs to process isotope tracer data.: "The find_intemidates workflow accepts unlabeled peak tables (C12), labeled peak tables (C13), sample information metadata, and a file path as inputs to process isotope tracer data."
- [other] Execute find_intemidates function with mz_tol=10 ppm, rt_tol=0.05 min, p_value_cutoff=0.05, fold_change_cutoff=20, adduct recognition enabled, comparing hyuA case group against WT control group.: "Execute find_intemidates function with mz_tol=10 ppm, rt_tol=0.05 min, p_value_cutoff=0.05, fold_change_cutoff=20, adduct recognition enabled, comparing hyuA case group against WT control group"
- [readme] IsoPairFinder provides an end-to-end workflow including (1) differential analysis; (2) merging of redundant LC-MS features (adducts, neutral losses, and in-source fragments); (3) pairing 12C/13C features to determine potential intermediates.: "It provides the a end-to-end workflow serving this objective, including (1) differential analysis; (2) merging of the redundant LC-MS features (adducts, neutral losses, and in-source fragments); (3)"
- [other] Generate tracer_pair_result.xlsx containing identified ion pair matches between unlabeled and labeled peak tables and produce diagnostic PDF plots summarizing pairing results and statistical summaries.: "Generate tracer_pair_result.xlsx containing identified ion pair matches between unlabeled and labeled peak tables. 4. Produce diagnostic PDF plots summarizing pairing results and statistical"
- [readme] The demo data includes peak_table_C12.csv for unlabeled group and peak_table_C13.csv for labeled group, along with sample_info.csv and folders containing raw .mzML files organized by group and tracer label.: "Briefly, the files contains: - `peak_table_C12.csv`: the peak area table of unlabeled group (WT and HyuA mutants fed with uric acid) - `peak_table_C13.csv`: the peak area table of labeled group (WT"
