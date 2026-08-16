---
name: multiple-hypothesis-correction-in-metabolomics
description: Use when after computing raw p-values from differential metabolomics
  analysis or Fisher's exact test enrichment, and before reporting significant pathways
  or metabolites. Essential when testing multiple metabolites against multiple pathway
  hypotheses (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3678
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - fgsea
  - readr
  - readxl
  - enrichmet
  - omu (omu_summary function)
  - assign_hierarchy
  - omu_summary
  - R stats (base statistical functions)
  license_tier: restricted
derived_from:
- doi: 10.1101/2025.08.28.672951v2
  title: EnrichMET
- doi: 10.1128/mra.00129-19
  title: ''
evidence_spans:
- simplifies pathway enrichment analysis by allowing the complete workflow to be executed
  through a single R function call
- enrichmet integrates fgsea for fast MetSEA
- library(readr)
- library(readxl)
- Omu is an R package that enables rapid analysis of Metabolomics data sets
- Omu supports two univariate statistical models, t test and anova, using the functions
  ```omu_summary``` and ```anova_function``` respectively
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_enrichmet_cq
    doi: 10.1101/2025.08.28.672951v2
    title: EnrichMET
  - build: coll_omu_metabolomics_count_data_tool_cq
    doi: 10.1128/mra.00129-19
    title: omu metabolomics count data tool
  dedup_kept_from: coll_enrichmet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.08.28.672951v2
  all_source_dois:
  - 10.1101/2025.08.28.672951v2
  - 10.1128/mra.00129-19
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# multiple-hypothesis-correction-in-metabolomics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply adjusted p-value thresholds and multiple-testing corrections during metabolite set enrichment analysis to control false discovery rates across pathway and metabolite hypotheses. This prevents spurious pathway assignments when testing many metabolites and pathways simultaneously.

## When to use

After computing raw p-values from differential metabolomics analysis or Fisher's exact test enrichment, and before reporting significant pathways or metabolites. Essential when testing multiple metabolites against multiple pathway hypotheses (e.g., 20+ metabolites × 50+ pathways), where uncorrected p-values inflate Type I error.

## When NOT to use

- Input is a single metabolite or single pathway (no multiple hypothesis problem)
- Study design involves only a priori hypotheses without exploratory testing (hypothesis-driven studies with pre-registered comparisons may use less stringent correction)
- Raw p-values are already adjusted for multiple testing by the upstream differential analysis tool

## Inputs

- Raw p-values and log2 fold changes from differential analysis
- MetSEA results table with p-values and NES (Normalized Enrichment Scores)
- Pathway-to-metabolite mapping (PathwayVsMetabolites reference file)
- Metabolite count and pathway occurrence matrices

## Outputs

- Filtered MetSEA results table (pathways passing padj threshold)
- Filtered pathway enrichment table with significant pathways only
- Filtered metabolite centrality table (metabolites meeting co-occurrence cutoff)
- Summary statistics: number of pathways tested vs. passed, number of metabolites retained

## How to apply

During enrichment analysis, apply a p-value cutoff (e.g., padj < 0.05 or p < 0.05) and optional adjusted p-value filtering to control family-wise error rate or false discovery rate. The enrichmet() function filters metabolites using p_value_cutoff and applies adjusted p-value thresholds to MetSEA results before extracting significant pathway associations. Set min_pathway_occurrence and min_metabolite_occurrence parameters to enforce minimum co-occurrence thresholds, further reducing spurious pathway-metabolite pairs. Use fgsea's internal FDR correction (padj column) to identify Normalized Enrichment Scores significant at FDR < 0.05. Document all filtering thresholds in the methods section so results are reproducible and comparable across studies.

## Related tools

- **fgsea** (Computes Normalized Enrichment Scores with internal FDR correction (padj column) for metabolite set enrichment, automatically controlling false discovery across pathways)
- **enrichmet** (Wrapper function integrating fgsea and Fisher's exact test with user-configurable p_value_cutoff, min_pathway_occurrence, and min_metabolite_occurrence parameters to filter results downstream of enrichment computation) — https://github.com/biodatalab/enrichmet
- **R** (Statistical environment for implementing multiple-testing correction logic and filtering pipelines)

## Examples

```
results <- enrichmet(inputMetabolites = inputMetabolites, PathwayVsMetabolites = PathwayVsMetabolites, da_results = da_out, p_value_cutoff = 0.05, min_pathway_occurrence = 2, min_metabolite_occurrence = 1)
```

## Evaluation signals

- Verify p-value cutoff was applied consistently: count(pathways where padj < threshold) ≤ count(pathways where padj < 0.1 or p < cutoff); confirm no pathway with padj > threshold appears in final results table
- Confirm min_pathway_occurrence and min_metabolite_occurrence filters eliminated spurious low-frequency associations: check that all retained metabolite-pathway pairs appear in at least the specified minimum number of pathways/metabolites
- Check that MetSEA results show FDR-corrected significance: inspect results$MetSEA table for padj column; confirm only NES values with padj < 0.05 are highlighted in plots
- Reproducibility check: re-run enrichmet() with identical p_value_cutoff, min_pathway_occurrence, and min_metabolite_occurrence parameters and verify identical filtered results; compare row counts before/after filtering against documented thresholds
- Report effect of correction: document in methods how many raw hypotheses were tested (total metabolites × total pathways) vs. how many passed filtering; compute and report the effective correction factor (e.g., Bonferroni-equivalent)

## Limitations

- Conservative correction (e.g., Bonferroni) may reduce statistical power in high-dimensional metabolomics; FDR control (via fgsea padj) is generally preferred but depends on having sufficient samples and metabolites to estimate the null distribution accurately
- Thresholds (p_value_cutoff, min_pathway_occurrence) are data- and study-dependent; no universal defaults; setting too stringent thresholds may exclude true discoveries, while too lenient thresholds reintroduce false positives
- Multiple-testing correction assumes independence between metabolites and pathways; if metabolites are highly correlated or pathways heavily overlap, correction may be overly conservative or ineffective
- Adjusted p-values (padj) are only valid within the set of hypotheses tested; if new metabolites or pathways are added post-hoc, p-values must be recomputed

## Evidence

- [intro] p_value_cutoff parameter controls significance filtering in enrichment analysis: "Filter metabolites using p_value_cutoff parameter  [section=intro; evidence='p_value_cutoff = 0.05']"
- [intro] fgsea provides FDR-corrected p-values (padj) for metabolite set enrichment: "enrichmet integrates fgsea for fast MetSEA, igraph for topology-based metrics, and curated KEGG data for enrichment using Fisher's Exact Test—all accessible via a single function call."
- [intro] min_pathway_occurrence and min_metabolite_occurrence enforce co-occurrence thresholds to reduce spurious associations: "Filter pathways using min_pathway_occurrence parameter  [section=intro; evidence='min_pathway_occurrence = 2']; Filter metabolites using min_metabolite_occurrence parameter  [section=intro;"
- [other] MetSEA results table includes p-values and adjusted p-values for significance assessment: "Extract the MetSEA results table containing pathway names, NES values, p-values, and adjusted p-values."
- [readme] README demonstrates filtering applied during enrichment with configurable cutoff parameters: "p_value_cutoff = 0.1,  # Use a reasonable cutoff"
