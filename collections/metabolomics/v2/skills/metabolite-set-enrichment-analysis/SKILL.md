---
name: metabolite-set-enrichment-analysis
description: Use when you have differential metabolomics results (p-values and log2 fold changes) for a set of metabolites and want to identify which known metabolic pathways or metabolite sets show concerted enrichment in your condition of interest.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - R
  - fgsea
  - readr
  - readxl
  - KEGG
  - enrichmet
  - KEGGREST
  - igraph
derived_from:
- doi: 10.1101/2025.08.28.672951v2
  title: EnrichMET
evidence_spans:
- simplifies pathway enrichment analysis by allowing the complete workflow to be executed through a single R function call
- enrichmet integrates fgsea for fast MetSEA
- library(readr)
- library(readxl)
- curated KEGG data for enrichment using Fisher's Exact Test
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_enrichmet_cq
    doi: 10.1101/2025.08.28.672951v2
    title: EnrichMET
  dedup_kept_from: coll_enrichmet_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.08.28.672951v2
  all_source_dois:
  - 10.1101/2025.08.28.672951v2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-set-enrichment-analysis

## Summary

Metabolite Set Enrichment Analysis (MetSEA) identifies statistically significant metabolic pathways and gene sets associated with ranked metabolite lists by computing Normalized Enrichment Scores (NES) via fast set-enrichment algorithms like fgsea. Use this skill to detect coordinated shifts in metabolite abundance across curated pathway definitions, complementing univariate pathway enrichment when you have ranked metabolite statistics (p-values, fold changes, or test statistics).

## When to use

You have differential metabolomics results (p-values and log2 fold changes) for a set of metabolites and want to identify which known metabolic pathways or metabolite sets show concerted enrichment in your condition of interest. MetSEA is particularly valuable when individual metabolite signals are weak but pathway-level coordination is suspected, or when you wish to rank pathways by their overall effect size (NES) rather than by count-based Fisher tests alone.

## When NOT to use

- Your input is an unranked set of metabolites with no associated test statistics (log2 fold change, p-value, or effect size ranking). MetSEA requires a continuous ranking; use Fisher's exact test or overlap-based enrichment if only metabolite membership is available.
- Pathway definitions are not available or are poorly curated for your organism/context. MetSEA is sensitive to pathway composition; sparse or misaligned pathway-metabolite mappings will yield unreliable NES and p-values.
- Your sample size or statistical power is very low (e.g., <3 replicates per condition or >50% metabolites with padj > 0.5). MetSEA may detect spurious pathway signals or fail to converge if ranking statistics are uninformative.

## Inputs

- Ranked metabolite list (KEGG IDs or metabolite identifiers sorted by test statistic: log2 fold change, −log10(p-value), or signed combination thereof)
- PathwayVsMetabolites reference file (data.frame or CSV mapping pathway names to comma-separated metabolite identifiers)
- Summary statistics table (p-values, log2 fold changes, optional adjusted p-values) with metabolite identifiers as rows

## Outputs

- MetSEA results table (data.frame with columns: Pathway name, Normalized Enrichment Score (NES), nominal p-value, adjusted p-value (padj), pathway size, leading-edge subset of metabolites)
- Significant pathway subset filtered by padj < 0.05 or user-specified threshold
- MetSEA plot (enrichment plot showing running sum of pathway enrichment statistic)

## How to apply

Load your ranked metabolite list sorted by a signed test statistic (e.g., sign(log2 fold change) × −log10(p-value) or similar), along with a PathwayVsMetabolites reference file defining metabolite membership in each pathway. Execute fgsea with the ranked metabolites and pathway definitions to compute Normalized Enrichment Scores (NES), nominal p-values, and adjusted p-values (FDR or padj) for each pathway. Filter results by a significance threshold (typically padj < 0.05 or nominal p < 0.05) and extract the MetSEA results table. The enrichmet() function encapsulates this workflow via its integration of fgsea, accepting precomputed summary statistics (p-values, log2 fold changes) or raw metabolomics data from which it will compute differential analysis internally using run_de(). Key parameters include ranking method (e.g., 'signed_pval' for p-value-based scores), pathway size filters (min/max metabolites per pathway), and multiple-testing correction strategy (typically Benjamini-Hochberg for padj).

## Related tools

- **fgsea** (Core algorithm for fast Metabolite Set Enrichment Analysis; computes Normalized Enrichment Scores (NES), p-values, and padj for ranked metabolite lists against pathway definitions.)
- **enrichmet** (Wrapper function integrating fgsea for MetSEA alongside Fisher's exact test pathway enrichment, centrality analysis, and multi-plot generation; encapsulates the full workflow from raw metabolomics data or precomputed statistics to MetSEA results and visualization.) — https://github.com/biodatalab/enrichmet
- **KEGGREST** (Package for retrieving pathway-to-metabolite mappings from the KEGG resource; used to construct or validate PathwayVsMetabolites reference files.)
- **igraph** (Graph library for computing topology-based metrics (e.g., betweenness centrality) on metabolite-pathway networks; complements MetSEA results with node-level centrality scores.)

## Examples

```
results <- enrichmet(inputMetabolites = inputMetabolites, PathwayVsMetabolites = PathwayVsMetabolites, example_data = example_data, kegg_lookup = kegg_lookup, analysis_type = c("gsea"), p_value_cutoff = 0.05, min_pathway_occurrence = 2)
```

## Evaluation signals

- MetSEA results table contains only pathways with Normalized Enrichment Scores (NES) and p-values; check that NES ranges from −1 to +1 and p-values are between 0 and 1.
- After filtering by padj < 0.05 (or chosen cutoff), the number of significant pathways is reasonable relative to total pathway count tested (typically <50% for exploratory studies). Extreme proportions (0% or >90%) warrant review of ranking method or pathway definitions.
- Leading-edge metabolites for top pathways (highest |NES|) overlap meaningfully with metabolites showing largest individual fold changes or lowest individual p-values, indicating consistency between pathway-level and metabolite-level signals.
- MetSEA and Fisher's exact test pathway enrichment rank pathways similarly for top hits (Spearman correlation of −log10(p) or p-values > 0.5), suggesting robustness across enrichment methods.
- No pathway in the results has NES = 0 or NES = 1.0 exactly for all entries; exact duplicates indicate possible ties in ranking or pathway-metabolite overlap that may warrant filtering by pathway size.

## Limitations

- MetSEA results depend critically on the quality and completeness of the PathwayVsMetabolites reference. Outdated, sparse, or organism-specific pathway definitions may yield pathways with low specificity or mechanistic relevance (e.g., pathway membership defined by co-expression rather than true biochemical relationships).
- Ranking method (e.g., log2 fold change vs. −log10(p-value) vs. signed p-value) significantly affects NES and pathway rankings. No single ranking is universally optimal; choice should be justified by the biological question and effect-size distribution.
- Small pathway sizes (e.g., <5 metabolites) or highly overlapping pathway definitions can inflate p-values or lead to collinearity in results. The enrichmet() function offers min_pathway_occurrence and pathway size filtering to mitigate this.
- Multiple-testing correction (e.g., Benjamini-Hochberg FDR) becomes conservative when the number of pathways tested is very large (>1000), potentially missing weakly significant but biologically relevant pathways.
- MetSEA assumes that test statistics are approximately independent across metabolites. Highly correlated metabolites (e.g., from the same lipid class or isotope label) may artificially inflate pathway NES if many correlated metabolites belong to the same pathway.

## Evidence

- [intro] enrichmet() function integrates fgsea for fast MetSEA and produces a MetSEA results table as one of three output data.frame objects, alongside metabolite centrality and pathway enrichment results.: "The enrichmet() function integrates fgsea for fast MetSEA and produces a MetSEA results table as one of three output data.frame objects, alongside metabolite centrality and pathway enrichment results."
- [intro] fgsea with ranked metabolite list computes Normalized Enrichment Scores (NES) for each metabolite set, with pathway names, NES values, p-values, and adjusted p-values.: "Execute fgsea with the ranked metabolite list and pathway-to-metabolite gene set definitions, computing Normalized Enrichment Scores (NES) for each metabolite set."
- [intro] MetSEA input is ranked metabolites sorted by test statistic (log2 fold change or −log10(p-value)).: "Prepare ranked metabolite list sorted by test statistic (e.g., log2 fold change or -log10(p-value)) for input to fgsea."
- [intro] Significance filtering is applied at padj < 0.05 to extract significant MetSEA results.: "Apply significance filtering (e.g., padj < 0.05) and extract the MetSEA results table containing pathway names, NES values, p-values, and adjusted p-values."
- [readme] enrichmet workflow can accept either precomputed summary statistics or raw metabolomics data for differential analysis.: "These results can be supplied in one of two formats: 1. Precomputed summary statistics 2. Raw metabolomics data, from which the workflow will compute differential analysis results internally"
