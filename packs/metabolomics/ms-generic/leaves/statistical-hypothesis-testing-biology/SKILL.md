---
name: statistical-hypothesis-testing-biology
description: Use when you have a metabolite abundance table (rows=metabolites, columns=samples)
  from Metabolomics Workbench format and need to test whether specific metabolites
  or metabolite classes are significantly enriched in particular biological pathways
  or conditions, beyond what would be expected by.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2269
  tools:
  - Python (pandas, NumPy, SciPy)
  - Statistical analysis libraries (scipy.stats for enrichment tests)
  - MetENP
  - KEGGREST
  - pathview
  - scipy.stats
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2020.11.20.391912
  title: MetENP
evidence_spans:
- MetENP
- enrichment statistics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metenp_cq
    doi: 10.1101/2020.11.20.391912
    title: MetENP
  dedup_kept_from: coll_metenp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.11.20.391912
  all_source_dois:
  - 10.1101/2020.11.20.391912
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Statistical Hypothesis Testing in Biology

## Summary

Apply statistical tests to identify significantly enriched metabolite pathways and metabolite classes from metabolomics abundance data. This skill combines normalization, mapping, and hypothesis testing (Fisher's exact test, hypergeometric test, rank-based enrichment) with multiple-testing correction to produce validated enrichment rankings.

## When to use

You have a metabolite abundance table (rows=metabolites, columns=samples) from Metabolomics Workbench format and need to test whether specific metabolites or metabolite classes are significantly enriched in particular biological pathways or conditions, beyond what would be expected by chance.

## When NOT to use

- Your metabolite table is already collapsed to pathway-level aggregates or summary statistics; enrichment testing requires individual metabolite observations.
- You have fewer than ~10–20 metabolites per pathway; statistical power is insufficient for reliable enrichment inference.
- Your sample size is very small (n < 3 per group); enrichment p-values will be unreliable without sufficient replication.

## Inputs

- metabolite abundance table (rows=metabolites, columns=samples) in Metabolomics Workbench format
- metabolite identifiers (names or KEGG IDs)
- metabolite-to-pathway mapping database (e.g., KEGG pathway annotations)
- sample metadata (groups/conditions for stratified testing, optional)

## Outputs

- enrichment results table with pathway identifiers, enrichment scores, raw p-values, and adjusted p-values
- ranked list of significantly enriched pathways (filtered by adjusted p-value threshold, typically p < 0.05)
- enrichment visualizations (dotplots, pathway network plots, heatmaps showing metabolite direction of change)

## How to apply

First, normalize metabolite abundances across samples using log-transformation or quantile normalization to stabilize variance. Second, map metabolites to pathway or ontology identifiers using a metabolite-to-pathway cross-reference database (e.g., KEGG). Third, compute enrichment statistics for each pathway using either Fisher's exact test (for binary presence/absence), hypergeometric test (for count-based enrichment), or rank-based enrichment scores depending on whether your data is categorical or continuous. Fourth, apply multiple-testing correction (Benjamini–Hochberg) to control false discovery rate across all tested pathways. Finally, rank pathways by adjusted p-value and enrichment score to identify the most significant findings. The rationale is that raw p-values across hundreds of pathway tests will have inflated false positives without correction.

## Related tools

- **MetENP** (R package that implements metabolite enrichment analysis with Fisher's exact test, pathway mapping to KEGG, and Benjamini–Hochberg p-value correction; includes visualization of enriched pathways and metabolite abundance changes) — https://github.com/metabolomicsworkbench/MetENP
- **KEGGREST** (R/Bioconductor package for querying KEGG database to retrieve pathway definitions and metabolite-to-pathway mappings)
- **pathview** (R/Bioconductor package for visualizing enriched pathways with metabolite abundance overlays)
- **scipy.stats** (Python library providing Fisher's exact test and hypergeometric test implementations for enrichment score computation)

## Examples

```
.libPaths(c(paste0(Sys.getenv('HOME'), '/.local/R'), .libPaths())); library('MetENP'); metab_enrich <- path_enrichmentscore(metabolite_table, metabolite_to_pathway_map, test='fisher', p_adjust='BH')
```

## Evaluation signals

- Adjusted p-values are uniformly larger than raw p-values and follow expected FDR control (median adjusted p-value ≈ raw p-value × number of tests, or lower if many true positives exist).
- Enrichment results are reproducible: re-running the pipeline with the same inputs produces identical p-values and rankings.
- Pathways with enrichment p-value < 0.05 (adjusted) contain significantly more mapped metabolites than expected under the null model; quantify via manual spot-check of top 5 pathways.
- Metabolite-to-pathway mappings are complete and consistent (no metabolites are mapped to zero pathways; pathway coverage is ≥ 70% of input metabolites).
- Multiple-testing correction reduces the proportion of enriched pathways at p < 0.05 compared to uncorrected analysis; typically from 20–30% down to 5–10% under the null.

## Limitations

- Enrichment statistics assume independence between pathways; overlapping pathways (shared metabolites) may inflate or deflate p-values for related pathways.
- The choice of enrichment test (Fisher vs. hypergeometric vs. rank-based) assumes different data distributions; misspecification can lead to inflated false positives or negatives.
- Metabolite-to-pathway mappings are only as complete as the reference database (e.g., KEGG); unmapped or incorrectly annotated metabolites bias enrichment scores.
- Small sample sizes per group (n < 3) yield unreliable p-values; consider pooling or alternative methods (e.g., permutation testing) when replication is limited.
- MetENP is an R package; it does not natively handle raw mass spectrometry data or mzML files; input must be a pre-processed, validated abundance table.

## Evidence

- [other] MetENP performs metabolite enrichment analysis to identify enriched pathways from metabolomics data.: "MetENP performs metabolite enrichment analysis to identify enriched pathways from metabolomics data."
- [other] Normalize metabolite abundances across samples using appropriate scaling (e.g., log-transformation or quantile normalization).: "Normalize metabolite abundances across samples using appropriate scaling (e.g., log-transformation or quantile normalization)."
- [other] Compute enrichment statistics (e.g., Fisher's exact test, hypergeometric test, or rank-based enrichment score) for each pathway.: "Compute enrichment statistics (e.g., Fisher's exact test, hypergeometric test, or rank-based enrichment score) for each pathway."
- [other] Calculate adjusted p-values using multiple-testing correction (e.g., Benjamini–Hochberg).: "Calculate adjusted p-values using multiple-testing correction (e.g., Benjamini–Hochberg)."
- [intro] Metabolite enrichment analysis and their associated enriched pathways.: "Metabolite enrichment analysis and their associated enriched pathways."
- [readme] Enrichment score of metabolite class, Maps to pathway of the species of choice, Calculate enrichment score of pathways: "Enrichment score of metabolite class, Maps to pathway of the species of choice, Calculate enrichment score of pathways"
