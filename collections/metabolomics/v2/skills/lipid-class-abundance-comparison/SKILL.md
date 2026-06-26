---
name: lipid-class-abundance-comparison
description: 'Use when you have a LipidomicsExperiment object with logged and normalized
  Area measurements, sample-level phenotype annotations (e.g., SampleType: Cancer,
  Benign, Metastasis), and you want to identify which lipid classes show consistent
  directional change across all samples within a group.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3668
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - lipidr
  - limma
  - R
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jproteome.0c00082
  title: lipidr
evidence_spans:
- Datasets can be easily downloaded and parsed into `LipidomicsExperiment` object
  using `lipidr` function `fetch_mw_study()`
- '`lipidr` allows users, to quickly explore public lipidomics experiments. `lipidr`
  provides an easy way to re-analyze and visualize these datasets.'
- This step of the workflow requires the `limma` package to be installed.
- Data Mining and Analysis of Lipidomics Datasets in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidr_cq
    doi: 10.1021/acs.jproteome.0c00082
    title: lipidr
  dedup_kept_from: coll_lipidr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.0c00082
  all_source_dois:
  - 10.1021/acs.jproteome.0c00082
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-class-abundance-comparison

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compare abundance patterns of lipid classes (e.g., phosphatidylcholines, cardiolipins, triglycerides) across sample groups to identify which lipid classes are systematically up- or down-regulated in disease versus control states. This skill enables discovery of lipid biomarker signatures by quantifying and visualizing differential regulation at the lipid class level rather than individual lipid species.

## When to use

Apply this skill when you have a LipidomicsExperiment object with logged and normalized Area measurements, sample-level phenotype annotations (e.g., SampleType: Cancer, Benign, Metastasis), and you want to identify which lipid classes show consistent directional change across all samples within a group. Particularly useful after outlier removal and when prior PCA or quality control suggests biological separation between groups.

## When NOT to use

- Input data is unnormalized or not log-transformed; normalize and log the data first using set_normalized() and set_logged().
- Sample size is very small (n < 3 per group); limma requires sufficient replication to estimate variance reliably.
- You want to identify individual lipid species biomarkers rather than class-level trends; use univariate species-level analysis instead.

## Inputs

- LipidomicsExperiment object (logged and normalized Area measurements)
- Sample phenotype annotations (SampleType, Stage, Race, or other grouping variable)
- Outlier sample identifiers for removal (optional but recommended)

## Outputs

- Differential expression results (log2-fold-change, adjusted p-value, test statistic per lipid)
- Volcano plot(s) showing log2FC vs. -log10(p-value) with lipids colored by class
- Summary table of lipid class regulation patterns (up-, down-, or non-regulated classes per contrast)

## How to apply

Load a LipidomicsExperiment object from lipidr with pre-processed, logged, and normalized Area measurements. Remove outlier samples using column subsetting (e.g., exclude flagged samples 18 and 42). Perform two-group differential expression analysis using de_analysis() with contrasts of interest (e.g., Cancer-Benign, Cancer-Metastasis), which leverages the limma package to compute log2-fold-change and adjusted p-values per lipid. Generate volcano plots using plot_results_volcano() to visualize log2FC and -log10(p-value) for each lipid, then aggregate results by lipid class to identify classes where the majority of members are significantly up- or down-regulated in the same direction (e.g., PCs and PGs up-regulated, CLs and TGs down-regulated). Interpret the pattern as evidence of coordinated class-level regulation rather than random individual lipid shifts.

## Related tools

- **lipidr** (Loads LipidomicsExperiment objects, wraps limma differential analysis via de_analysis(), and generates volcano plots via plot_results_volcano() to visualize lipid class regulation.) — https://github.com/ahmohamed/lipidr
- **limma** (Performs statistical differential expression testing (log2FC, adjusted p-value computation) for each lipid species using moderated t-statistics.)

## Examples

```
two_group <- de_analysis(d, Cancer~Benign, Cancer~Metastasis); plot_results_volcano(two_group)
```

## Evaluation signals

- Volcano plot shows distinct clusters of lipids by class, with consistent direction (e.g., all PCs in upper right, all CLs in lower left), indicating real class-level regulation rather than scattered noise.
- Adjusted p-values for class members are consistently small (< 0.05) and log2FC values have the same sign within each class, confirming coordinated regulation.
- Number of significantly regulated lipids per class is consistent with biological prior (e.g., multiple PCs and PGs simultaneously up-regulated in cancer vs. benign is plausible for membrane remodeling).
- Comparison across multiple contrasts (e.g., Cancer-Benign and Cancer-Metastasis) shows that class-level patterns are reproducible in the first contrast but not in the second (as shown in source article), supporting specificity.
- Visual inspection of volcano plot reproduces the published finding (e.g., PCs and PGs up-regulated, CLs and TGs down-regulated in cancer tissues).

## Limitations

- Lipid class abundance comparison assumes that lipid class membership is correctly annotated in the input LipidomicsExperiment; mis-annotated or ambiguously named lipids (flagged during parsing) should be manually reviewed or removed before aggregation.
- The skill does not account for confounder variables (e.g., Race, Cancer Stage) automatically; use de_design() with model formulae to adjust for covariates if needed.
- Class-level aggregation can mask heterogeneous regulation within a class (e.g., some PC species up-regulated, others down-regulated); inspect individual species volcano plots to verify.
- Small effect sizes or high within-group variance can reduce power to detect class-level regulation; quality control and outlier removal are essential pre-requisites.

## Evidence

- [other] Phosphatidylcholines (PCs) and phosphatidylglycerols (PGs) are up-regulated while cardiolipins (CLs) and triglycerides (TGs) are down-regulated in cancer tissues compared to benign samples.: "Phosphatidylcholines (PCs) and phosphatidylglycerols (PGs) are up-regulated while cardiolipins (CLs) and triglycerides (TGs) are down-regulated in cancer tissues compared to benign samples."
- [other] Perform two-group differential expression analysis using de_analysis() with Cancer-Benign and Cancer-Metastasis contrasts, leveraging the limma package for statistical testing.: "Perform two-group differential expression analysis using de_analysis() with Cancer-Benign and Cancer-Metastasis contrasts, leveraging the limma package for statistical testing."
- [other] Generate volcano plots using plot_results_volcano() to visualize log2-fold-change and adjusted p-values, highlighting lipid classes (PCs, PGs, CLs, TGs) with differential regulation.: "Generate volcano plots using plot_results_volcano() to visualize log2-fold-change and adjusted p-values, highlighting lipid classes (PCs, PGs, CLs, TGs) with differential regulation."
- [intro] A fairly large difference is observed between cancer and benign samples, with PCs and PGs up-regulated and CLs and TGs down-regulated in cancer tissues.: "A fairly large difference is observed between cancer and benign samples, with PCs and PGs up-regulated and CLs and TGs down-regulated in cancer tissues."
- [intro] This step of the workflow requires the limma package to be installed.: "This step of the workflow requires the limma package to be installed."
- [readme] lipidr represents lipidomics datasets as a LipidomicsExperiment, which extends SummarizedExperiment, to facilitate integration with other Bioconductor packages.: "lipidr represents lipidomics datasets as a LipidomicsExperiment, which extends SummarizedExperiment, to facilitate integration with other Bioconductor packages."
