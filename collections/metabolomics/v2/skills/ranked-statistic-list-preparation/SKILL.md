---
name: ranked-statistic-list-preparation
description: Use when after completing differential analysis (e.g., via run_de()) to generate p-values and log2 fold changes, and before executing fgsea-based MetSEA enrichment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0885
  tools:
  - R
  - fgsea
  - readr
  - readxl
  - enrichmet
  - run_de
derived_from:
- doi: 10.1101/2025.08.28.672951v2
  title: EnrichMET
evidence_spans:
- simplifies pathway enrichment analysis by allowing the complete workflow to be executed through a single R function call
- enrichmet integrates fgsea for fast MetSEA
- library(readr)
- library(readxl)
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
---

# ranked-statistic-list-preparation

## Summary

Prepare a ranked metabolite list sorted by test statistic (log2 fold change or -log10(p-value)) for input to fast set enrichment analysis (fgsea). This intermediate step converts differential analysis results into the ordered format required by GSEA algorithms.

## When to use

After completing differential analysis (e.g., via run_de()) to generate p-values and log2 fold changes, and before executing fgsea-based MetSEA enrichment. Use this skill when you have summary statistics for metabolites and need to prepare them for pathway set enrichment testing with ranked statistics.

## When NOT to use

- Input is already a ranked list or pre-computed fgsea result object
- Metabolite identifiers cannot be mapped to standard KEGG IDs or pathway reference
- Summary statistics contain missing or infinite values; rank metric cannot be computed

## Inputs

- Differential analysis results table (data.frame with metabolite identifiers, p-values, adjusted p-values, log2 fold changes)
- Metabolite KEGG IDs or other standardized identifiers
- PathwayVsMetabolites reference mapping (defines pathway-to-metabolite associations)

## Outputs

- Ranked metabolite list (numeric vector named by KEGG IDs, sorted by test statistic)
- fgsea-compatible input object ready for pathway enrichment testing

## How to apply

Extract metabolite identifiers (KEGG IDs), p-values, and log2 fold changes from the differential analysis output. Create a ranking metric by selecting either log2 fold change directly or computing -log10(p-value) and optionally applying a sign correction based on directionality (e.g., 'signed_pval' method: sign(log2fc) × -log10(p-value)). Sort the metabolites by this ranking metric in descending order to prioritize metabolites with largest absolute effect sizes or lowest p-values. The ranked list serves as input to fgsea(), which tests whether metabolite sets (pathways) are enriched toward the top or bottom of the ranked list, computing Normalized Enrichment Scores (NES) and adjusted p-values for significance filtering (typically padj < 0.05).

## Related tools

- **fgsea** (Performs fast set enrichment analysis on the ranked metabolite list, computing Normalized Enrichment Scores and adjusted p-values for pathway significance testing)
- **enrichmet** (Integrates fgsea and pathway enrichment pipeline; consumes the ranked metabolite list as input to execute MetSEA with curated KEGG pathway-to-metabolite mappings) — https://github.com/biodatalab/enrichmet
- **run_de** (Generates the upstream differential analysis results (p-values, log2 fold changes) that are reformatted into the ranked list) — https://github.com/biodatalab/enrichmet
- **R** (Implements ranking, sorting, and data transformation operations on differential analysis output)

## Examples

```
# Load DE results, extract KEGG IDs and compute signed p-value ranking
ranked_list <- sign(da_results$log2fc) * (-log10(da_results$pval))
names(ranked_list) <- da_results$met_id
ranked_list <- sort(ranked_list, decreasing = TRUE)
# Pass to fgsea via enrichmet
results <- enrichmet(inputMetabolites = NULL, PathwayVsMetabolites = PathwayVsMetabolites, da_results = da_results, analysis_type = 'gsea')
```

## Evaluation signals

- Ranked list contains all metabolites present in the input differential analysis table with no duplicates or loss of identifiers
- Numeric ranking values are strictly monotonic (either all ascending or all descending) with no ties or missing values
- KEGG IDs or metabolite identifiers in the ranked list match those in the PathwayVsMetabolites reference; unmapped metabolites are logged or excluded
- fgsea execution on the ranked list completes successfully and returns NES and adjusted p-value columns with no errors or NaN values
- Top-ranked metabolites correspond to smallest p-values or largest absolute log2 fold changes relative to input differential analysis results

## Limitations

- Ranking metric selection (log2fc vs. -log10(p-value) vs. signed variant) affects downstream GSEA results and pathway interpretation; choice should align with study hypothesis
- Metabolite identifiers not found in the PathwayVsMetabolites reference are excluded from fgsea, reducing statistical power; verification of identifier format (KEGG ID extraction from complex IDs) is required
- Tied ranking values (e.g., identical p-values or fold changes) may lead to arbitrary ordering; application of random tie-breaking or secondary sorting by secondary statistic is recommended
- Missing or infinite values in p-values or log2 fold changes prevent rank computation; preprocessing and imputation/filtering are prerequisites

## Evidence

- [other] Prepare ranked metabolite list sorted by test statistic (e.g., log2 fold change or -log10(p-value)) for input to fgsea.: "Prepare ranked metabolite list sorted by test statistic (e.g., log2 fold change or -log10(p-value)) for input to fgsea."
- [readme] Created rankings for 23 KEGG metabolites using 'signed_pval' method. Ranking range: -3.523 to 4: "Created rankings for 23 KEGG metabolites using 'signed_pval' method
> Ranking range: -3.523 to 4"
- [readme] Testing 54 pathways with GSEA: "Testing 54 pathways with GSEA"
- [other] Execute fgsea with the ranked metabolite list and pathway-to-metabolite gene set definitions, computing Normalized Enrichment Scores (NES) for each metabolite set.: "Execute fgsea with the ranked metabolite list and pathway-to-metabolite gene set definitions, computing Normalized Enrichment Scores (NES) for each metabolite set."
- [readme] enrichment analysis using DE results results1 <- enrichmet(inputMetabolites = NULL, PathwayVsMetabolites = PathwayVsMetabolites, da_results = da_out: "enrichment analysis using DE results results1 <- enrichmet(inputMetabolites = NULL, PathwayVsMetabolites = PathwayVsMetabolites, da_results = da_out"
