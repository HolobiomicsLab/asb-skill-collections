---
name: metabolite-kegg-pathway-enrichment
description: Use when you have an annotated list of metabolite compounds (with associated
  m/z features or compound IDs) and want to determine which KEGG metabolic pathways
  are significantly enriched or depleted in your experimental samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - ggplot2
  - igraph
  - KEGG_Enrich_PlotPanel
  - Enrichment
  - KEGG_Enrich_Plot
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1093/bib/bbac455
  title: LargeMetabo
evidence_spans:
- several R packages are utilized in the background processes, including ggfortify,
  ggplot2, igraph
- several R packages are utilized in the background processes, including ggplot2,
  igraph, MASS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_largemetabo_cq
    doi: 10.1093/bib/bbac455
    title: LargeMetabo
  dedup_kept_from: coll_largemetabo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bib/bbac455
  all_source_dois:
  - 10.1093/bib/bbac455
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-kegg-pathway-enrichment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

This skill performs statistical enrichment analysis of metabolite compound lists against KEGG pathway databases to identify significantly over-represented metabolic pathways. It quantifies pathway associations using p-value filtering and fold-change values to support functional interpretation of metabolomic datasets.

## When to use

Apply this skill when you have an annotated list of metabolite compounds (with associated m/z features or compound IDs) and want to determine which KEGG metabolic pathways are significantly enriched or depleted in your experimental samples. Use it after marker identification or filtering steps have produced a candidate compound list, and you need to move from individual metabolite significance to pathway-level biological interpretation.

## When NOT to use

- Input compound list is unannotated (raw m/z values without KEGG/database mapping); annotate first using Metabo_Annotation().
- Sample size is very small (<3 replicates per group) or compound list contains <5 features; statistical power and multiple-testing correction may be unreliable.
- You need to enrich against custom or non-standard databases; use Enrich_Plot() with custom enrichDB parameter instead.

## Inputs

- compound list with KEGG IDs or standardized metabolite identifiers
- fold-change or intensity vector aligned to compound IDs
- EnrichParam configuration object from KEGG_Enrich_PlotPanel()

## Outputs

- EnrichResultList: enrichment result table with pathway names, p-values, and statistics
- KEGG pathway enrichment visualization (heatmap or network plot)

## How to apply

Prepare a compound list with metabolite identifiers (IDtype=1 for KEGG IDs or IDtype=2 for other databases) and associated fold-change or intensity values. Call KEGG_Enrich_PlotPanel() with the compound list, setting enrichDB='kegg', pvalcutoff=0.05, and appropriate cateIdx to configure enrichment parameters. Execute Enrichment() on the resulting EnrichParam object to compute enrichment statistics and filter pathways by the specified p-value threshold (default 0.05). The function returns EnrichResultList, a table of significant pathways with their statistics. Pass this result table along with the original fold-change values to KEGG_Enrich_Plot() for visualization. The rationale is that statistical filtering isolates biologically credible pathway associations while fold-change annotation reveals the direction and magnitude of pathway member dysregulation.

## Related tools

- **KEGG_Enrich_PlotPanel** (Configures enrichment analysis parameters (enrichDB, p-value cutoff, ID type, category index) and generates preliminary visualization panels) — https://github.com/LargeMetabo/LargeMetabo
- **Enrichment** (Core function that executes KEGG enrichment calculation, computes p-values, and filters results by specified p-value threshold) — https://github.com/LargeMetabo/LargeMetabo
- **KEGG_Enrich_Plot** (Visualizes EnrichResultList as heatmaps or network plots, integrating pathway statistics with compound fold-change values) — https://github.com/LargeMetabo/LargeMetabo
- **ggplot2** (Underlying graphics package used for rendering enrichment plots)
- **igraph** (Network visualization support for pathway topology and compound-pathway associations)

## Examples

```
EnrichParam <- KEGG_Enrich_PlotPanel(sampleDatakegg, enrichDB = "kegg", pvalcutoff = 0.05, IDtype = 1, cateIdx = 1); EnrichResultList <- Enrichment(EnrichParam); EnrichFC <- seq(from = -2, to = 2, length.out = 24); KEGG_Enrich_Plot(EnrichResultList = EnrichResultList, cpdID = sampleDatakegg, cpdFC = EnrichFC)
```

## Evaluation signals

- Returned p-values are all ≤ pvalcutoff (default 0.05); no pathways with p > 0.05 should be in final result table.
- EnrichResultList columns include at minimum: pathway name/ID, p-value, enrichment statistic, and count of significant compounds in pathway.
- KEGG_Enrich_Plot output displays consistent color/intensity mapping between fold-change values and heatmap visualization (e.g., red for upregulated, blue for downregulated compounds).
- Number of enriched pathways is biologically plausible (typically 5–200 for well-powered metabolomic studies); extreme values (0 or >1000) suggest misconfigured ID mapping or threshold.
- Compounds in result table match input compound list by ID; no spurious or off-target pathways from ID mismatches.

## Limitations

- Enrichment analysis accuracy depends on quality of metabolite annotation; unannotated or incorrectly mapped compounds will bias pathway statistics.
- KEGG database coverage is incomplete for many specialized or novel metabolites; absent compounds are not tested and may lead to false negatives.
- p-value cutoff (0.05) does not account for multiple-testing correction across all tested pathways; user should consider applying Bonferroni or FDR correction for stricter significance.
- Fold-change or intensity values must be properly aligned to compound IDs; misalignment between cpdID and cpdFC vectors in KEGG_Enrich_Plot() will produce misleading visualizations.

## Evidence

- [readme] KEGG enrichment configuration and execution: "EnrichParam <- KEGG_Enrich_PlotPanel(sampleDatakegg, enrichDB = "kegg", pvalcutoff = 0.05, IDtype = 1, cateIdx = 1); EnrichResultList <- Enrichment(EnrichParam)"
- [other] Output structure and content of enrichment results: "The Enrichment() function takes enrichment parameters (EnrichParam) configured via KEGG_Enrich_PlotPanel() with enrichDB='kegg', pvalcutoff=0.05, IDtype=1, and cateIdx=1, and returns"
- [readme] Integration of fold-change with enrichment visualization: "KEGG_Enrich_Plot(EnrichResultList = EnrichResultList, cpdID = sampleDatakegg, cpdFC = EnrichFC)"
- [readme] Input requirements for KEGG enrichment: "When performing enrichment analysis for KEGG pathways, a compound list should be properly provided"
- [other] Enrichment result table usage: "can be passed to KEGG_Enrich_Plot() for visualization alongside compound IDs and fold-change values"
