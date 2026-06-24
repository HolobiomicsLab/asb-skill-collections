---
name: tracer-metabolite-pair-matching
description: Use when you have acquired LC-MS peak tables from both unlabeled (12C)
  and isotope-labeled (13C) samples from a stable isotope tracing experiment, paired
  with sample metadata distinguishing case and control groups, and you need to systematically
  identify which unlabeled features correspond to.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3407
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
  license_tier: restricted
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

# tracer-metabolite-pair-matching

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identifies and matches 12C/13C isotope-labeled metabolite pairs in stable isotope tracing metabolomics to discover biochemical pathway intermediates. This skill applies differential analysis, feature redundancy merging, and statistical pairing to pinpoint candidate intermediate metabolites between unlabeled and labeled peak tables.

## When to use

Apply this skill when you have acquired LC-MS peak tables from both unlabeled (12C) and isotope-labeled (13C) samples from a stable isotope tracing experiment, paired with sample metadata distinguishing case and control groups, and you need to systematically identify which unlabeled features correspond to intermediates in a labeled tracer pathway.

## When NOT to use

- Input peak tables are not normalized or are derived from different MS instruments or processing pipelines—inconsistent preprocessing will produce unreliable pairings.
- Sample information lacks clear case/control group designations or tracer_group labels—the function requires these to perform differential analysis.
- You seek to identify fragments or neutral losses without first merging redundant adducts—use adduct merging as a prerequisite step.
- Retention time or mass calibration is poor (>0.1 min RT drift or >50 ppm uncalibrated m/z)—tolerance windows will not capture true pairs.

## Inputs

- peak_table_C12.csv (unlabeled LC-MS peak area table with m/z, retention time, and sample abundance columns)
- peak_table_C13.csv (labeled LC-MS peak area table with matching structure)
- sample_info.csv or .xlsx (metadata: sample names, group assignments, tracer_group labels, polarity)

## Outputs

- tracer_pair_result.xlsx (matched 12C/13C ion pairs with pairing statistics)
- diagnostic PDF plots (pairing results summary, statistical distributions, feature match visualizations)

## How to apply

Load unlabeled (C12) and labeled (C13) peak tables (CSV format) and sample metadata (XLSX or CSV) into R using readr and dplyr. Execute the find_intemidates function, specifying case and control groups (e.g., hyuA mutant vs WT), mass tolerance (10 ppm typical), retention time tolerance (0.05 min typical), statistical thresholds (p_value_cutoff=0.05, fold_change_cutoff=20), and enabling adduct recognition to merge redundant features (adducts, neutral losses, in-source fragments). The function performs differential analysis between case and control groups across positive and negative ionization modes, then pairs C12 and C13 features within specified mass and retention time tolerances. Evaluate success by examining the generated tracer_pair_result.xlsx for ion pair matches and diagnostic PDF plots showing pairing statistics and feature distributions.

## Related tools

- **IsoPairFinder** (R package that implements the find_intemidates function for isotope pair matching, feature merging, and differential analysis.) — https://github.com/DoddLab/IsoPairFinder
- **dplyr** (Performs data manipulation and filtering on peak tables and metadata.)
- **readr** (Loads CSV and tabular input files (peak tables, sample metadata).)
- **ggplot2** (Generates diagnostic plots for visualization of pairing results and statistical summaries.)
- **tidyr** (Reshapes and reformats peak tables and results for downstream analysis.)

## Examples

```
library(IsoPairFinder); find_intemidates(peak_table_unlabel='peak_table_C12.csv', peak_table_label='peak_table_C13.csv', sample_info='sample_info.csv', path='~/Project/Data/', polarity='positive', control_group=c('WT'), case_group=c('MUTANT'), mz_tol=10, rt_tol=0.05, p_value_cutoff=0.05, fold_change_cutoff=20, is_recognize_adducts=TRUE)
```

## Evaluation signals

- tracer_pair_result.xlsx contains matched pairs with non-zero counts for both positive and negative ionization modes; verify no spurious pairings by spot-checking mass differences (expect ≈1–12 Da for typical 13C-labeled metabolites).
- Diagnostic PDF plots show pairing frequency histograms and statistical distributions with expected peaks near the specified m/z and retention time tolerances (±10 ppm, ±0.05 min).
- Fold-change and p-value distributions in plots conform to specified cutoffs (p<0.05, fold_change>20); verify case group shows elevated labeled peak intensities relative to control.
- Feature redundancy merging reduced duplicate ions; validate by checking that adduct-annotated features (e.g., [M+H]+, [M+Na]+) are consolidated into single representative pairs.
- Paired feature counts scale reasonably with sample size and metabolite complexity (typically 100–1000 pairs for uric acid pathway data); anomalously low counts (<10) suggest mass/RT calibration issues or incorrect group assignments.

## Limitations

- Requires high-quality, well-preprocessed peak tables from MS-DIAL or equivalent; poor peak detection or alignment upstream will propagate into spurious or missed pairs.
- Performance depends on appropriate tolerance parameters (mz_tol, rt_tol) tuned to specific LC-MS instrument and method; generic defaults may fail on different platforms or chromatographic resolutions.
- Adduct recognition is enabled by default but may misidentify or merge non-redundant features if spectral databases or adduct libraries are incomplete or misconfigured.
- Statistical power for differential analysis (fold_change_cutoff, p_value_cutoff) assumes adequate biological replication; small sample sizes or high between-replicate variance can increase false negatives.
- Does not directly validate pairing candidates via MS/MS spectroscopy or authentic standards; validation requires manual inspection or secondary metabolite identification workflows.

## Evidence

- [other] The find_intemidates workflow accepts unlabeled peak tables (C12), labeled peak tables (C13), sample information metadata, and a file path as inputs to process isotope tracer data.: "The find_intemidates workflow accepts unlabeled peak tables (C12), labeled peak tables (C13), sample information metadata, and a file path as inputs"
- [other] Execute find_intemidates function with mz_tol=10 ppm, rt_tol=0.05 min, p_value_cutoff=0.05, fold_change_cutoff=20, adduct recognition enabled, comparing hyuA case group against WT control group across positive and negative polarities.: "Execute find_intemidates function with mz_tol=10 ppm, rt_tol=0.05 min, p_value_cutoff=0.05, fold_change_cutoff=20, adduct recognition enabled"
- [other] Generate tracer_pair_result.xlsx containing identified ion pair matches between unlabeled and labeled peak tables. Produce diagnostic PDF plots summarizing pairing results and statistical summaries.: "Generate tracer_pair_result.xlsx containing identified ion pair matches between unlabeled and labeled peak tables. Produce diagnostic PDF plots"
- [readme] IsoPairFinder is an R package designed to identify the pathway intermediate feature pairs in stable isotope tracing metabolomics studies. It provides end-to-end workflow including (1) differential analysis; (2) merging of redundant LC-MS features (adducts, neutral losses, in-source fragments); (3) pairing 12C/13C features.: "identify the pathway intermediate feature pairs in stable isotope tracing metabolomics studies. By integrating genetic manipulation techniques, it enables researchers to efficiently screen candidate"
- [readme] Peak tables are processed by MS-DIAL to generate peak tables. This demo data includes processed peak tables and raw mass spectrometry files.: "The raw data are processed by the MS-DIAL to generate peak tables. This demo data includes processed peak tables"
