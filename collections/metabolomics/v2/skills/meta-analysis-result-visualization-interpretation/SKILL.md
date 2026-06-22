---
name: meta-analysis-result-visualization-interpretation
description: Use when after computing a weighted meta-analysis combining p-values, fold-changes, and study sizes across multiple metabolomics studies, you need to identify which metabolites show both statistical significance (p ≤ 0.05) and biological meaningfulness (fold-change ≥ 3.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0570
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - R
  - amanida
  - volcano_plot
  - explore_plot
  - vote_plot
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted meta-analysis in R
- This vignette illustrates `Amanida` R package, which contains a collection of functions for computing a weighted meta-analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_amanida_cq
    doi: 10.1093/bioinformatics/btab591
    title: Amanida
  dedup_kept_from: coll_amanida_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab591
  all_source_dois:
  - 10.1093/bioinformatics/btab591
  - 10.3390/metabo13121167
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# meta-analysis-result-visualization-interpretation

## Summary

Apply volcano plots, vote plots, and explore plots to the outputs of metabolomics meta-analysis in order to identify compounds meeting statistical and consistency thresholds, filter false positives, and reject null hypotheses about compound significance.

## When to use

After computing a weighted meta-analysis combining p-values, fold-changes, and study sizes across multiple metabolomics studies, you need to identify which metabolites show both statistical significance (p ≤ 0.05) and biological meaningfulness (fold-change ≥ 3.5 or user-defined threshold), and verify consistency of directional trends across independent reports before drawing conclusions.

## When NOT to use

- Input dataset contains fewer than 2 independent studies per compound—visualization cannot assess consistency across reports.
- Raw metabolomics peak intensities or spectral data are available—use feature extraction and normalization workflows before meta-analysis.
- Standard deviations or raw individual-level data are available—use traditional meta-analysis tools (e.g., fixed/random effects models) rather than amanida's weighted approach designed for aggregate results without variance.

## Inputs

- amanida S4 object containing @stat table (quantitative meta-analysis results with p-values, fold-changes, and vote-counts per compound)
- amanida S4 object containing @vote table (qualitative vote-counting results)

## Outputs

- volcano plot graphic (log10(p-values) vs. log2(fold-change) with labeled compounds exceeding cut-offs)
- explore plot graphic (bar plot showing reports divided by trend with vote-counting for compounds with multiple independent reports)
- filtered compound list (compounds meeting p-value, fold-change, and consistency thresholds)

## How to apply

First, generate a volcano plot with user-defined cut-offs for p-value (typically 0.05) and fold-change (typically 3.5 for metabolomics) to identify compounds exceeding both thresholds simultaneously. Second, apply an explore plot with type='mix' and counts parameter to identify compounds appearing in multiple independent reports with consistent directional trends (all up-regulated or all down-regulated). Third, cross-validate compounds that appear in both filtered sets to confirm they meet statistical significance, biological meaningfulness, and consistency criteria. This three-step combination guards against false positives and provides evidence to reject the null hypothesis of no effect.

## Related tools

- **amanida** (computes weighted meta-analysis combining p-values, fold-changes, and study sizes; generates S4 object containing @stat and @vote tables for downstream visualization) — https://github.com/mariallr/amanida
- **volcano_plot** (visualizes quantitative meta-analysis results by plotting log10(p-values) against log2(fold-change) to identify compounds exceeding user-defined cut-offs) — https://github.com/mariallr/amanida
- **explore_plot** (visualizes qualitative vote-counting results showing reports divided by trend; type='mix' mode identifies compounds with multiple reports and consistent directional trends) — https://github.com/mariallr/amanida
- **vote_plot** (bar plot visualization of compound vote-counting results to identify consistency in directional trends across reports) — https://github.com/mariallr/amanida
- **R** (host environment for amanida package execution and visualization function calls)

## Examples

```
library(amanida); data(sample_data); amanida_result <- compute_amanida(sample_data); volcano_plot(amanida_result, cutoff = c(0.05, 3.5)); explore_plot(sample_data, type = "mix", counts = 1)
```

## Evaluation signals

- Volcano plot displays labeled compounds only above both p-value ≤ 0.05 and fold-change ≥ 3.5 thresholds (no compounds below either threshold should be labeled)
- Compounds flagged in explore_plot with type='mix' and counts=1 show consistent vote direction (all votes positive or all negative, no split reports)
- Cross-validation: compounds appearing in both volcano plot filtered set AND explore plot filtered set indicate they meet all three criteria (statistical significance, biological meaningfulness, consistency)
- Vote-count values in @vote table are computed as sum of votes (±1) divided by number of reports; values near +1 or -1 indicate high consensus across studies
- Number of compounds retained after filtering should be substantially smaller than input total, indicating stringent threshold application

## Limitations

- Vote plot and explore plot restrict output to 30 and 25 compounds respectively for readability; larger datasets may not display all significant compounds without manual subsetting.
- Visualization relies on study size (N) weighting; studies with very small sample sizes can still contribute equally if p-value and fold-change meet thresholds, potentially inflating false positives.
- Explore plot type='mix' mode requires manual inspection to confirm visual consistency; no automated consensus scoring is provided beyond vote-count.
- Fold-change cut-off of 3.5 is used in the source task but may not generalize; article recommends 2.0 as biological meaningfulness threshold in other contexts.
- Missing data is ignored during import and meta-analysis; cannot assess bias introduced by unreported results or selective reporting across studies.

## Evidence

- [other] Which metabolites show statistical significance, multiple independent reports, and consistent directional trends when applying volcano plot cut-offs (p=0.05, fold-change=3.5) and mixed-mode exploration analysis?: "Which metabolites show statistical significance, multiple independent reports, and consistent directional trends when applying volcano plot cut-offs (p=0.05, fold-change=3.5) and mixed-mode"
- [other] Hippuric acid and Phenol are identified as compounds with more than one report and statistical significance, with consistency as all reports results are in the same trend, providing evidence to reject the null hypothesis.: "Hippuric acid and Phenol are identified as compounds with more than one report and statistical significance, with consistency as all reports results are in the same trend, providing evidence to"
- [other] Filter compounds using volcano plot cutoffs: retain compounds with p-value ≤0.05 and absolute fold-change ≥3.5. Apply explore plot with type='mix' and counts=1 to identify compounds with more than one report showing consistent trend direction.: "Filter compounds using volcano plot cutoffs: retain compounds with p-value ≤0.05 and absolute fold-change ≥3.5. Apply explore plot with type='mix' and counts=1 to identify compounds with more than"
- [intro] To observe the results of meta-analysis graphically is done with a volcano plot, where the log10(p-values) are plotted against the log2(fold-change): "To observe the results of meta-analysis graphically is done with a volcano plot, where the log10(p-values) are plotted against the log2(fold-change)"
- [intro] A bar plot shows the result of vote-counting. With vote plot discrepancies in compounds behaviour are not detected at first glance, and we suggest to combine the results with the explore plot: "A bar plot shows the result of vote-counting. With vote plot discrepancies in compounds behaviour are not detected at first glance, and we suggest to combine the results with the explore plot"
- [readme] Data can be shown in three types: * type = "all": show all data * type = "sub": subset the data by a cut-off value indicated by the counts parameter * type = "mix": subset the data by a cut-off value indicated by the counts parameter and show compounds with discrepancies (reports up-regulated and down-regulated): "type = "mix": subset the data by a cut-off value indicated by the counts parameter and show compounds with discrepancies"
- [intro] in case of fold-change we recommend values higher than 2, where it is considered to have biological meaningfulness: "in case of fold-change we recommend values higher than 2, where it is considered to have biological meaningfulness"
- [intro] output is restricted to 30 compounds to facilitate the readability: "output is restricted to 30 compounds to facilitate the readability"
