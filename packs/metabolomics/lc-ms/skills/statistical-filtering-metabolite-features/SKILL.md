---
name: statistical-filtering-metabolite-features
description: Use when when you have peak area tables (unlabeled C12 and labeled C13) from LC-MS metabolomics with sample metadata indicating case and control groups, and you need to distinguish true metabolic changes from instrumental noise or batch artifacts before attempting isotopic pairing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# statistical-filtering-metabolite-features

## Summary

Apply differential abundance analysis and statistical cutoff filtering to metabolite peak tables to identify significantly altered features between experimental groups in stable isotope tracing metabolomics. This skill prioritizes biologically relevant intermediates by removing noise and non-significant signals based on p-value and fold-change thresholds.

## When to use

When you have peak area tables (unlabeled C12 and labeled C13) from LC-MS metabolomics with sample metadata indicating case and control groups, and you need to distinguish true metabolic changes from instrumental noise or batch artifacts before attempting isotopic pairing. Specifically triggered when analyzing isotope-labeled tracer data where intermediates show significant differential abundance between genetic backgrounds (e.g., mutant vs. wild-type).

## When NOT to use

- Input peak tables are already quality-filtered or pre-thresholded by upstream tools (e.g., MS-DIAL feature detection); re-filtering risks removing valid signals.
- No clear experimental groups or controls are defined in metadata; statistical comparison requires distinct case and control cohorts.
- Data are from single replicates or very small sample sizes (n < 3 per group); p-value cutoffs become unreliable and fold-change statistics are unstable.
- Absolute peak intensities or ion counts are needed; this skill removes features, not preserving quantitative abundance for absolute quantification workflows.

## Inputs

- peak_table_unlabel (CSV: unlabeled C12 peak area matrix with features × samples)
- peak_table_label (CSV: labeled C13 peak area matrix with features × samples)
- sample_info (CSV or XLSX: metadata with sample names, group assignment, tracer_group, and other experimental variables)
- sample metadata indicating control_group and case_group identities

## Outputs

- Filtered feature set (retained after statistical thresholds)
- Differential abundance statistics table (p-values, fold-changes, adjusted p-values)
- tracer_pair_result.xlsx (ion pair matches from filtered features)
- diagnostic PDF plots summarizing statistical distributions and pairing results

## How to apply

Load peak tables and sample metadata using readr/dplyr, then execute the find_intemidates function with user-defined statistical cutoffs: p_value_cutoff (typically 0.05 with p_adjust=TRUE for multiple-testing correction) and fold_change_cutoff (e.g., 20-fold minimum change). The function performs differential analysis comparing a case group (e.g., 'MUTANT') against a control group (e.g., 'WT') across both positive and negative ionization modes separately. Features failing these thresholds are excluded from subsequent pairing workflows. The rationale is that intermediates in active metabolic pathways exhibit both statistical significance (p < 0.05) and substantial magnitude shifts (fold-change > threshold), reducing false-positive pairing of low-abundance or noisy signals.

## Related tools

- **IsoPairFinder** (Executes find_intemidates function to perform differential analysis and apply statistical filtering (p_value_cutoff, fold_change_cutoff) on dual-labeled isotope peak tables) — https://github.com/DoddLab/IsoPairFinder
- **dplyr** (Data manipulation and grouping of peak tables by sample group for differential statistics)
- **readr** (Loading CSV/XLSX peak tables and metadata into R data frames)
- **ggplot2** (Generating diagnostic plots summarizing statistical distributions and filter results)
- **tidyr** (Reshaping peak tables from wide to long format for group-wise statistical testing)

## Examples

```
find_intemidates(peak_table_unlabel = 'peak_table_C12.csv', peak_table_label = 'peak_table_C13.csv', sample_info = 'sample_info.csv', path = '~/Project/Data/', polarity = 'positive', control_group = c('WT'), case_group = c('MUTANT'), mz_tol = 10, rt_tol = 0.05, p_value_cutoff = 0.05, p_adjust = TRUE, fold_change_cutoff = 20, is_recognize_adducts = TRUE)
```

## Evaluation signals

- Output feature count is substantially reduced from input (typically 30–70% retention in real data); features below thresholds are absent from tracer_pair_result.xlsx.
- Fold-change values in output are ≥ fold_change_cutoff (e.g., ≥ 20); any retained feature has |log2(FC)| ≥ log2(threshold).
- p-values in output are ≤ p_value_cutoff (e.g., ≤ 0.05); if p_adjust=TRUE, adjusted p-values (e.g., Benjamini–Hochberg) are used.
- Diagnostic plots show clear separation of case vs. control groups for retained features in volcano plot or MA plot; filtered features cluster near fold-change = 0 or high p-value.
- Ion pairing results (tracer_pair_result.xlsx) contain only feature pairs from the filtered set; no discrepancies between statistical filtering input and pairing output.

## Limitations

- Fold-change cutoff (e.g., 20×) is arbitrary and dataset-dependent; inappropriately high thresholds may exclude true pathway intermediates with modest upregulation, while low thresholds reintroduce noise.
- p-value-based filtering assumes biological replicates and normal/log-normal abundance distributions; single replicates or heavy-tailed distributions invalidate p-value interpretation.
- Adduct recognition (is_recognize_adducts=TRUE) can conflate related features before filtering, potentially removing valid intermediate signals if isotopic labeling shifts adduct distribution.
- Polarity-specific filtering (positive/negative ion modes) is applied independently; features with variable ionization across samples may fail one polarity's thresholds and be missed in the other.
- No changelog or version control evident; reproducibility across IsoPairFinder releases depends on parameter documentation in analysis scripts.

## Evidence

- [other] Execute find_intemidates function with mz_tol=10 ppm, rt_tol=0.05 min, p_value_cutoff=0.05, fold_change_cutoff=20, adduct recognition enabled, comparing hyuA case group against WT control group: "Execute find_intemidates function with mz_tol=10 ppm, rt_tol=0.05 min, p_value_cutoff=0.05, fold_change_cutoff=20, adduct recognition enabled, comparing hyuA case group against WT control group"
- [other] The find_intemidates workflow accepts unlabeled peak tables (C12), labeled peak tables (C13), sample information metadata, and a file path as inputs to process isotope tracer data.: "The find_intemidates workflow accepts unlabeled peak tables (C12), labeled peak tables (C13), sample information metadata, and a file path as inputs to process isotope tracer data."
- [readme] It provides the a end-to-end workflow serving this objective, including (1) differential analysis; (2) merging of the redundant LC-MS features (adducts, neutral losses, and in-source fragments); (3) pairing 12C/13C features to determine potential intermediates.: "It provides the a end-to-end workflow serving this objective, including (1) differential analysis; (2) merging of the redundant LC-MS features (adducts, neutral losses, and in-source fragments); (3)"
- [readme] find_intemidates(peak_table_unlabel = 'peak_table_C12.csv', peak_table_label = 'peak_table_C13.csv', sample_info = 'sample_info.csv', path = '...', polarity = 'positive', control_group = c('WT'), case_group = c('MUTANT'), mz_tol = 10, rt_tol = 0.05, p_value_cutoff = 0.05, p_adjust = TRUE, fold_change_cutoff = 20, is_recognize_adducts = TRUE): "find_intemidates(peak_table_unlabel = 'peak_table_C12.csv', peak_table_label = 'peak_table_C13.csv', sample_info = 'sample_info.csv', path =, polarity = 'positive', control_group = c("WT"),"
- [other] Generate tracer_pair_result.xlsx containing identified ion pair matches between unlabeled and labeled peak tables. Produce diagnostic PDF plots summarizing pairing results and statistical summaries.: "Generate tracer_pair_result.xlsx containing identified ion pair matches between unlabeled and labeled peak tables. Produce diagnostic PDF plots summarizing pairing results and statistical summaries."
