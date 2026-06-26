---
name: metabolite-significance-filtering-volcano-plot
description: Use when you have meta-analyzed metabolomic results from multiple studies
  with p-values and fold-change estimates (e.g., from amanida quantitative meta-analysis),
  and you need to identify compounds that meet both statistical rigor (p ≤ 0.05) and
  biological magnitude (|fold-change| ≥ 3.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0623
  tools:
  - R
  - amanida
  - webchem
  - PubChem
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioinformatics/btab591
  title: Amanida
- doi: 10.3390/metabo13121167
  title: ''
evidence_spans:
- Amanida R package, which contains a collection of functions for computing a weighted
  meta-analysis in R
- This vignette illustrates `Amanida` R package, which contains a collection of functions
  for computing a weighted meta-analysis
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-significance-filtering-volcano-plot

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Filter metabolites from meta-analysis results using statistical significance (p-value) and biological effect size (fold-change) thresholds applied to a volcano plot, then cross-validate consistency across multiple independent studies to identify robust biomarker candidates. This skill separates statistically and biologically meaningful metabolites from noise in multi-study metabolomic datasets.

## When to use

You have meta-analyzed metabolomic results from multiple studies with p-values and fold-change estimates (e.g., from amanida quantitative meta-analysis), and you need to identify compounds that meet both statistical rigor (p ≤ 0.05) and biological magnitude (|fold-change| ≥ 3.5) while also showing directional consistency across independent reports. This is especially useful when raw data and standard deviations are unavailable, and you want to reject the null hypothesis of no effect for candidate metabolites.

## When NOT to use

- Input is raw, single-study metabolomic data without meta-analysis aggregation across multiple independent reports — use univariate statistical testing instead.
- You require standard deviation or confidence intervals for effect size calculation — amanida is designed to work without these; standard meta-analysis tools may be more appropriate.
- The fold-change threshold must be < 2 or the p-value < 0.01 due to discovery stringency — the recommended thresholds (p=0.05, |FC|=3.5) assume moderate multiple-testing correction and biological meaningfulness.

## Inputs

- Meta-analyzed metabolomic dataset (CSV, XLS, or TXT format)
- Tabular data with columns: identifier (compound name or PubChem ID), p-value, fold-change, N (study size), reference (bibliographic source)

## Outputs

- Filtered compound list meeting p-value and fold-change cutoffs
- Volcano plot visualization showing filtered metabolites and cutoff boundaries
- Explore plot visualization showing compounds with directional consistency across reports
- Cross-validated list of metabolites meeting both statistical significance and consistency thresholds

## How to apply

Load meta-analyzed results containing identifier, p-value, fold-change, and study size columns into R using amanida's `amanida_read` function. Apply volcano plot cutoffs (typically p-value ≤ 0.05 and absolute fold-change ≥ 3.5) to filter compounds meeting statistical and biological thresholds simultaneously. Visualize filtered results using `volcano_plot` to confirm the selection graphically. To ensure robustness, apply the `explore_plot` function with type='mix' and counts=1 to identify compounds present in multiple independent reports with consistent directional trends (all up-regulated or all down-regulated). Cross-validate that candidate metabolites (e.g., Hippuric acid, Phenol) appear in both the volcano-filtered set and the consistency-filtered set, confirming they meet combined thresholds for significance, effect size, and directional consistency across studies.

## Related tools

- **amanida** (R package that performs weighted meta-analysis on p-values and fold-changes, computes volcano plots with user-defined cutoffs, and generates explore plots for consistency detection across studies) — https://github.com/mariallr/amanida
- **webchem** (R package used to harmonize and validate compound identifiers (chemical names, InChI, SMILES) by converting to PubChem ID before filtering)
- **R** (Statistical computing environment in which amanida and volcano/explore plotting functions are executed)
- **PubChem** (Public database providing standardized compound identifiers and metadata (Molecular Formula, SMILES, InChIKey, cross-links to KEGG, ChEBI, HMDB, Drugbank) for validated metabolite annotation)

## Examples

```
library(amanida); data(sample_data); result <- compute_amanida(sample_data, comp.inf=FALSE); volcano_plot(result, cutoff=c(0.05, 3.5)); explore_plot(sample_data, type='mix', counts=1)
```

## Evaluation signals

- Volcano plot displays expected bimodal distribution with filtered metabolites positioned beyond both p-value (y-axis, log10 scale) and fold-change (x-axis, log2 scale) cutoff thresholds.
- Filtered compound list contains only entries with p-value ≤ 0.05 AND |fold-change| ≥ 3.5; no compounds violating either threshold appear in the output.
- Explore plot with type='mix' and counts=1 identifies compounds appearing in ≥ 2 independent reports with consistent directional trend (either all up-regulated or all down-regulated, no mixed signs).
- Cross-validation confirms that candidate metabolites (e.g., Hippuric acid, Phenol) appear in both the volcano-filtered dataset and the consistency-filtered explore plot output.
- Compound identifiers are harmonized to a standard nomenclature (e.g., PubChem ID) and checked for duplicates before filtering; output includes harmonized IDs and associated metadata (KEGG, ChEBI, HMDB links) for traceability.

## Limitations

- Volcano plot filtering alone does not detect discrepancies in directional trends across studies; compounds may meet significance and magnitude cutoffs but show conflicting up/down regulation across reports — always cross-validate with explore plot (type='mix').
- Vote plot and explore plot outputs are restricted to 30 and 25 compounds respectively for readability, which may mask relevant compounds in large-scale screening; consider iterative filtering or manual inspection of full sorted lists.
- Negative fold-change values are automatically converted to positive reciprocals (1/value), which can obscure the original directionality if not documented; verify fold-change sign handling in the amanida output report.
- The method assumes fold-change values ≥ 2 have biological meaningfulness, but this is a heuristic; domain-specific validation (e.g., literature review, functional assays) is required to confirm biological relevance.
- Missing data is ignored during import, which may lead to biased effect estimates if missingness is not random; document and report the proportion of missing values per compound.

## Evidence

- [other] Filter compounds using volcano plot cutoffs: retain compounds with p-value ≤0.05 and absolute fold-change ≥3.5.: "Filter compounds using volcano plot cutoffs: retain compounds with p-value ≤0.05 and absolute fold-change ≥3.5."
- [other] Apply explore plot with type='mix' and counts=1 to identify compounds with more than one report showing consistent trend direction.: "Apply explore plot with type='mix' and counts=1 to identify compounds with more than one report showing consistent trend direction."
- [intro] To observe the results of meta-analysis graphically is done with a volcano plot, where the log10(p-values) are plotted against the log2(fold-change): "To observe the results of meta-analysis graphically is done with a volcano plot, where the log10(p-values) are plotted against the log2(fold-change)"
- [intro] A bar plot shows the result of vote-counting. With vote plot discrepancies in compounds behaviour are not detected at first glance, and we suggest to combine the results with the explore plot: "With vote plot discrepancies in compounds behaviour are not detected at first glance, and we suggest to combine the results with the explore plot"
- [intro] P-value: weighted p-values combination, which is a variant of Fisher's method. A gamma distribution is used to assign non-integral weights proportional to study size to each p-value.: "P-value: weighted p-values combination, which is a variant of Fisher's method. A gamma distribution is used to assign non-integral weights proportional to study size"
- [other] Hippuric acid and Phenol are identified as compounds with more than one report and statistical significance, with consistency as all reports results are in the same trend: "Hippuric acid and Phenol are identified as compounds with more than one report and statistical significance, with consistency as all reports results are in the same trend"
- [readme] type = "mix": subset the data by a cut-off value indicated by the counts parameter and show compounds with discrepancies (reports up-regulated and down-regulated): "type = "mix": subset the data by a cut-off value indicated by the counts parameter and show compounds with discrepancies"
- [intro] in case of fold-change we recommend values higher than 2, where it is considered to have biological meaningfulness: "in case of fold-change we recommend values higher than 2, where it is considered to have biological meaningfulness"
