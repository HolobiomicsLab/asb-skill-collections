---
name: mass-spectral-feature-alignment
description: Use when when you have separate LC-MS peak tables for unlabeled (C12) and labeled (C13) isotope tracer experiments and need to identify which features correspond to the same metabolite across the two labeling conditions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
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

# mass-spectral-feature-alignment

## Summary

Align unlabeled (C12) and labeled (C13) mass spectrometry peak tables by matching m/z and retention time coordinates within specified tolerances, enabling pairing of isotope-labeled feature pairs for tracer metabolomics. This skill identifies candidate intermediate metabolites by recognizing which peaks shift systematically between unlabeled and labeled sample groups.

## When to use

When you have separate LC-MS peak tables for unlabeled (C12) and labeled (C13) isotope tracer experiments and need to identify which features correspond to the same metabolite across the two labeling conditions. Apply this skill after peak detection and differential abundance analysis, when you want to systematically match features across isotope conditions using mass accuracy and chromatographic retention.

## When NOT to use

- Input peak tables are already aligned or merged across isotope conditions (feature pairing is a prerequisite, not a post-processing step).
- You only have a single isotope labeling condition (C12 or C13 alone); alignment requires both unlabeled and labeled peak tables.
- Raw LC-MS data have not been processed into peak tables; this skill operates on already-detected and quantified features, not on raw mzML/NetCDF files.

## Inputs

- unlabeled peak table (C12, CSV format with m/z, retention time, peak area, feature ID)
- labeled peak table (C13, CSV format with m/z, retention time, peak area, feature ID)
- sample information metadata (CSV/XLSX with sample names, group assignment, tracer_group column)
- file path to raw MS data directory (optional, for adduct recognition and MS2 validation)

## Outputs

- tracer_pair_result.xlsx (matched C12–C13 feature pairs with m/z, retention time, fold-change, p-value, pairing confidence)
- diagnostic PDF plots (feature pairing summary, statistical distribution of matches, ion pair scatter plots)
- merged feature table (redundant adducts/fragments consolidated before pairing)

## How to apply

Load the unlabeled (C12) and labeled (C13) peak tables, along with sample metadata indicating group membership (e.g., control vs. case) and isotope labeling status. Execute the find_intemidates function with specified m/z tolerance (default 10 ppm), retention time tolerance (default 0.05 min), and optionally enable adduct recognition to account for in-source fragments and neutral losses. The function performs differential analysis between case and control groups, merges redundant features (adducts, neutral losses, in-source fragments), and then pairs C12 and C13 peaks based on coordinate proximity. Apply statistical filters (p_value_cutoff=0.05, fold_change_cutoff=20) to retain only significantly dysregulated features in both isotope conditions. The output includes a feature-pair result table (xlsx) identifying which C12 peaks match which C13 peaks, plus diagnostic PDF plots showing pairing statistics and validation.

## Related tools

- **IsoPairFinder** (R package implementing find_intemidates function for paired feature alignment across C12/C13 peak tables with differential analysis and adduct merging) — https://github.com/DoddLab/IsoPairFinder
- **dplyr** (Data manipulation and filtering of peak tables and alignment results)
- **tidyr** (Reshaping and reformatting peak table structures for alignment)
- **readr** (Reading CSV/XLSX peak tables and sample metadata into R)
- **ggplot2** (Generating diagnostic scatter plots and distribution visualizations of feature pair alignment)

## Examples

```
find_intemidates(peak_table_unlabel = 'peak_table_C12.csv',
                 peak_table_label = 'peak_table_C13.csv',
                 sample_info = 'sample_info.csv',
                 path = '~/Project/Data/',
                 polarity = 'positive',
                 control_group = c('WT'),
                 case_group = c('MUTANT'),
                 mz_tol = 10,
                 rt_tol = 0.05,
                 fold_change_cutoff = 20,
                 is_recognize_adducts = TRUE)
```

## Evaluation signals

- Paired feature count: verify that the output xlsx contains a reasonable number of matched C12–C13 pairs (>10% of input features is typical for tracer studies); absence of pairs suggests tolerance parameters are too strict.
- M/z and retention time deltas: inspect the distribution of mass differences (should cluster near 1.003 Da for single C13 substitution, or multiples thereof) and RT differences (should be <0.05 min for true pairs).
- Fold-change and p-value filtering: confirm that retained pairs show concordant direction of change (e.g., both C12 and C13 features elevated in case group) and meet the specified thresholds (p<0.05, fold_change>20).
- PDF diagnostic plots: visual scatter plots should show clear clustering of pair coordinates along diagonal; absence of clustering indicates tolerance parameters need adjustment.
- Adduct annotation consistency: if adduct recognition is enabled, paired features should have consistent or complementary adduct annotations (e.g., [M+H]+ in C12 matched to [M+H]+ in C13); mismatches suggest merging or pairing errors.

## Limitations

- M/z and RT tolerance parameters (10 ppm, 0.05 min) must be tuned to the specific LC-MS instrument and chromatographic method; poorly calibrated instruments or highly variable retention times will cause missed or spurious pairings.
- Adduct recognition depends on in-source fragmentation patterns and ionization efficiency, which vary by metabolite class; some metabolites may produce unexpected or absent adducts, reducing pairing success.
- Statistical filtering (p_value_cutoff, fold_change_cutoff) assumes sufficient biological replicates and consistent sample preparation; underpowered or noisy studies may fail to identify true tracer pairs.
- Feature merging (consolidation of adducts and neutral losses) relies on accurate mass accuracy and mass defect calculations; high-mass or complex metabolites with overlapping isotope patterns may merge incorrectly.
- The skill assumes that unlabeled and labeled samples are derived from the same biological source and processed identically; batch effects, different extraction protocols, or instrumental drift between C12 and C13 runs can inflate false pairing rates.

## Evidence

- [other] find_intemidates workflow accepts unlabeled peak tables (C12), labeled peak tables (C13), sample information metadata, and a file path as inputs: "The find_intemidates workflow accepts unlabeled peak tables (C12), labeled peak tables (C13), sample information metadata, and a file path as inputs to process isotope tracer data."
- [other] Execute find_intemidates with mz_tol=10 ppm, rt_tol=0.05 min, fold_change_cutoff=20, adduct recognition enabled: "Execute find_intemidates function with mz_tol=10 ppm, rt_tol=0.05 min, p_value_cutoff=0.05, fold_change_cutoff=20, adduct recognition enabled, comparing hyuA case group against WT control group"
- [other] Generates tracer_pair_result.xlsx containing identified ion pair matches and diagnostic PDF plots summarizing pairing results: "Generate tracer_pair_result.xlsx containing identified ion pair matches between unlabeled and labeled peak tables. 4. Produce diagnostic PDF plots summarizing pairing results and statistical"
- [readme] IsoPairFinder provides end-to-end workflow including differential analysis, merging redundant LC-MS features (adducts, neutral losses, in-source fragments), and pairing 12C/13C features: "It provides the a end-to-end workflow serving this objective, including (1) differential analysis; (2) merging of the redundant LC-MS features (adducts, neutral losses, and in-source fragments); (3)"
- [readme] Demo data includes peak_table_C12.csv (unlabeled group) and peak_table_C13.csv (labeled group) processed by MS-DIAL: "- `peak_table_C12.csv` / `peak_table_C13.csv`: Peak tables for 12C and 13C labeled samples."
