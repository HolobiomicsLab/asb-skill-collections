---
name: differential-lipid-expression-analysis
description: Use when when you have a LipidomicsExperiment object with logged and normalized Area measurements, sample grouping metadata (e.g., SampleType, Stage, Race), and a research question about whether specific lipid molecules or classes differ significantly between two or more sample groups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3668
  edam_topics:
  - http://edamontology.org/topic_3050
  - http://edamontology.org/topic_0091
  tools:
  - lipidr
  - limma
  - R
  - Metabolomics Workbench API
derived_from:
- doi: 10.1021/acs.jproteome.0c00082
  title: lipidr
evidence_spans:
- Datasets can be easily downloaded and parsed into `LipidomicsExperiment` object using `lipidr` function `fetch_mw_study()`
- '`lipidr` allows users, to quickly explore public lipidomics experiments. `lipidr` provides an easy way to re-analyze and visualize these datasets.'
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
---

# differential-lipid-expression-analysis

## Summary

Identify lipid molecules with significant abundance changes between sample groups (e.g., cancer vs. benign tissue) using limma-based statistical testing within the lipidr framework. This skill enables discovery of lipid class regulation patterns and their association with biological conditions or clinical variables.

## When to use

When you have a LipidomicsExperiment object with logged and normalized Area measurements, sample grouping metadata (e.g., SampleType, Stage, Race), and a research question about whether specific lipid molecules or classes differ significantly between two or more sample groups. Common triggers include: comparing disease states (cancer vs. benign), comparing disease severity (cancer stage), or testing multifactorial designs (SampleType corrected for confounders like Race).

## When NOT to use

- Input data are not logged and normalized; raw or partially processed Area measurements will inflate variance and reduce statistical power.
- No clear sample grouping variable or metadata is available to define contrasts (e.g., missing SampleType or Stage annotations).
- Sample size is very small (< 3 samples per group) or severely imbalanced, risking unstable limma estimates and unreliable p-values.

## Inputs

- LipidomicsExperiment object with logged and normalized Area measurements
- Sample annotation table with grouping variables (SampleType, Stage, Race, etc.)
- Optional: list of outlier sample identifiers for removal

## Outputs

- Two-group or multi-group differential expression results object (from de_analysis or de_design)
- Volcano plot(s) showing log2-fold-change vs. adjusted p-value for each lipid
- significant_molecules table with lipid identifiers, fold-changes, p-values, and adjusted p-values
- Identified regulated lipid classes (e.g., PCs up-regulated, CLs down-regulated)

## How to apply

First, perform quality control by removing outlier samples (e.g., via column subsetting) and verifying logged/normalized status. For two-group comparisons (e.g., Cancer vs. Benign), use de_analysis() with explicit contrasts (e.g., 'Cancer-Benign', 'Cancer-Metastasis') leveraging the limma package for statistical testing; visualize results with volcano plots showing log2-fold-change and adjusted p-values to highlight differential lipid classes. For multi-group comparisons (e.g., ANOVA-style across cancer stages), use de_design() with formula notation (e.g., '~ Stage') to test all groups simultaneously; extract the significant_molecules table and filter by adjusted p-value threshold (typically p_adj < 0.05) to identify regulated lipids. In factorial designs, use de_design() with adjusted formulas (e.g., '~ SampleType + Race') to correct for confounding variables while examining the primary grouping variable.

## Related tools

- **lipidr** (Primary framework for LipidomicsExperiment object construction, QC, and differential analysis interface (de_analysis, de_design, plot_results_volcano functions)) — https://github.com/ahmohamed/lipidr
- **limma** (Statistical engine for linear modeling and hypothesis testing in two-group and multi-group differential expression analysis)
- **Metabolomics Workbench API** (Optional data source for fetching public lipidomics studies (e.g., ST001111) via fetch_mw_study()) — https://www.metabolomicsworkbench.org

## Examples

```
two_group <- de_analysis(d, Cancer-Benign, Cancer-Metastasis); plot_results_volcano(two_group)
```

## Evaluation signals

- Volcano plot displays expected separation: log2-fold-changes distant from zero for known regulated lipids, with adjusted p-values well below 0.05 threshold for significant molecules.
- significant_molecules table is non-empty for two-group comparisons of distinct sample types (e.g., Cancer vs. Benign), and conversely contains no or very few significant hits for neutral contrasts (e.g., Cancer Stage when no stage effect exists).
- Lipid class patterns align with biological expectation: e.g., PCs and PGs up-regulated while CLs and TGs down-regulated when comparing cancer to benign tissue (ST001111 finding).
- Outlier removal (e.g., samples 18 and 42) demonstrably improves volcano plot separation or reduces false-positive counts compared to pre-filtered data.
- Multi-group results show consistent direction of regulation across relevant pairwise contrasts when applicable (e.g., Cancer-Benign and Cancer-Metastasis both show same lipid class trends).

## Limitations

- Cancer Stage does not always show significant lipid associations even in large datasets; negative results (no significant molecules) are valid but may reflect biological homogeneity or insufficient statistical power rather than true absence of regulation.
- Two-group comparisons (e.g., Cancer vs. Benign) may show mild separation in PCA but fail to discriminate between related phenotypes (e.g., Cancer vs. Metastasis clusters overlap), limiting discriminatory power for some contrasts.
- Race and other confounding variables can introduce small but measurable effects in factorial designs; failure to adjust for these in de_design() formula may bias estimates of the primary grouping variable.
- Limma assumes roughly equal variance across groups; severe heteroscedasticity in lipid abundance may require transformation or robust methods beyond the standard pipeline.

## Evidence

- [intro] This step of the workflow requires the limma package to be installed.: "This step of the workflow requires the limma package to be installed."
- [intro] Perform two-group differential expression analysis using de_analysis() with Cancer-Benign and Cancer-Metastasis contrasts, leveraging the limma package for statistical testing.: "Perform two-group differential expression analysis using de_analysis() with Cancer-Benign and Cancer-Metastasis contrasts, leveraging the limma package for statistical testing."
- [intro] Generate volcano plots using plot_results_volcano() to visualize log2-fold-change and adjusted p-values, highlighting lipid classes (PCs, PGs, CLs, TGs) with differential regulation.: "Generate volcano plots using plot_results_volcano() to visualize log2-fold-change and adjusted p-values, highlighting lipid classes (PCs, PGs, CLs, TGs) with differential regulation."
- [intro] Apply de_design() function with formula ~ Stage to perform ANOVA-style multi-group differential expression analysis using limma.: "Apply de_design() function with formula ~ Stage to perform ANOVA-style multi-group differential expression analysis using limma."
- [intro] A fairly large difference is observed between cancer and benign samples, with PCs and PGs up-regulated and CLs and TGs down-regulated in cancer tissues.: "A fairly large difference is observed between cancer and benign samples, with PCs and PGs up-regulated and CLs and TGs down-regulated in cancer tissues."
- [intro] Surprisingly, Cancer Stage does not appear to affect lipid molecules profiled in this experiment.: "Surprisingly, Cancer Stage does not appear to affect lipid molecules profiled in this experiment."
- [readme] Univariate analysis can be performed using any of the loaded clinical variables, which can be readily visualized as volcano plots. Multi-group comparisons and adjusting for confounding variables is also supported: "Univariate analysis can be performed using any of the loaded clinical variables, which can be readily visualized as volcano plots. Multi-group comparisons and adjusting for confounding variables is"
