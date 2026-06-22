---
name: enrichment-statistical-thresholding
description: Use when after running Enrichment() on a configured EnrichParam object (via KEGG_Enrich_PlotPanel or similar), when you have a full enrichment result table and need to reduce it to pathway hits meeting a specific significance threshold before visualization or export.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - ggplot2
  - igraph
  - KEGG_Enrich_PlotPanel
  - Enrichment
  - KEGG_Enrich_Plot
  - Enrich_Plot
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1093/bib/bbac455
  title: LargeMetabo
evidence_spans:
- several R packages are utilized in the background processes, including ggfortify, ggplot2, igraph
- several R packages are utilized in the background processes, including ggplot2, igraph, MASS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# enrichment-statistical-thresholding

## Summary

Apply p-value cutoffs to filter pathway enrichment results and retain only statistically significant associations between metabolites and biological pathways. This skill ensures that downstream pathway visualization and interpretation focus on robust, reproducible enrichment signals rather than noise.

## When to use

After running Enrichment() on a configured EnrichParam object (via KEGG_Enrich_PlotPanel or similar), when you have a full enrichment result table and need to reduce it to pathway hits meeting a specific significance threshold before visualization or export. Use this when you have a compound list with fold-change values and want to identify which KEGG pathways (or other databases) are statistically overrepresented at a defined p-value stringency.

## When NOT to use

- Input is already a pre-filtered enrichment table (p-values already applied)—re-filtering risks over-stringent or inconsistent thresholds.
- You have no biological justification for the p-value cutoff and want exploratory, unfiltered results—use the full EnrichResultList and filter in post-hoc visualization.
- Compound list lacks sufficient annotation or mass calibration; enrichment will be unreliable regardless of thresholding.

## Inputs

- EnrichParam object (configured via KEGG_Enrich_PlotPanel or similar with enrichDB, IDtype, cateIdx parameters)
- compound list (sampleDatakegg or sampleDatacas format)
- fold-change vector (optional, for visualization post-filtering)

## Outputs

- EnrichResultList (filtered enrichment result table with pathways meeting p-value threshold)
- CSV export of enrichment table (optional)

## How to apply

Configure the enrichment parameters via KEGG_Enrich_PlotPanel() by setting pvalcutoff to your desired threshold (typically 0.05). Pass this EnrichParam object to the Enrichment() function, which computes enrichment statistics and automatically filters the result table to retain only pathways with adjusted p-values ≤ pvalcutoff. The pvalcutoff parameter acts as a hard filter during enrichment computation; results below the threshold are excluded from EnrichResultList. Verify filtering by inspecting the row count and p-value distribution of the returned table before passing it to downstream visualization (KEGG_Enrich_Plot or Enrich_Plot). If too many or too few pathways remain, adjust pvalcutoff accordingly and re-run Enrichment().

## Related tools

- **KEGG_Enrich_PlotPanel** (Configures enrichment parameters (enrichDB, pvalcutoff, IDtype, cateIdx) prior to statistical thresholding) — https://github.com/LargeMetabo/LargeMetabo
- **Enrichment** (Executes enrichment computation and applies pvalcutoff filter to generate EnrichResultList) — https://github.com/LargeMetabo/LargeMetabo
- **KEGG_Enrich_Plot** (Visualizes filtered EnrichResultList alongside compound fold-change values) — https://github.com/LargeMetabo/LargeMetabo
- **Enrich_Plot** (Visualizes filtered enrichment results for non-KEGG databases) — https://github.com/LargeMetabo/LargeMetabo

## Examples

```
EnrichParam <- KEGG_Enrich_PlotPanel(sampleDatakegg, enrichDB = "kegg", pvalcutoff = 0.05, IDtype = 1, cateIdx = 1); EnrichResultList <- Enrichment(EnrichParam)
```

## Evaluation signals

- EnrichResultList row count decreases (or stays constant if all p-values already ≤ cutoff) compared to pre-filtering table; no rows with p-value > pvalcutoff remain.
- All p-values in EnrichResultList are ≤ pvalcutoff; spot-check the maximum p-value in the filtered table.
- Pathway count and composition are consistent and reproducible when re-running Enrichment() with the same pvalcutoff.
- CSV export of filtered table contains only pathways meeting threshold; manual inspection of a few rows confirms p-value filtering was applied.
- Downstream visualization (KEGG_Enrich_Plot or Enrich_Plot) displays only the filtered pathways without errors or missing labels.

## Limitations

- pvalcutoff is a global threshold; it does not account for multiple-hypothesis correction beyond what Enrichment() applies internally—verify that the function uses appropriate FDR or Bonferroni adjustment.
- Very stringent pvalcutoff (e.g., 0.001) may exclude all or most pathways in small compound lists, resulting in empty EnrichResultList.
- Enrichment quality depends on upstream annotation accuracy (MS1 or MS/MS metabolite identification); incorrect compound IDs will propagate through thresholding and yield false negatives.
- pvalcutoff applies uniformly across all pathways; it does not weight by effect size, pathway size, or biological relevance—results may include marginal but statistically significant hits.

## Evidence

- [readme] pvalcutoff parameter in KEGG_Enrich_PlotPanel configuration: "EnrichParam <- KEGG_Enrich_PlotPanel(sampleDatakegg, enrichDB = "kegg", pvalcutoff = 0.05, IDtype = 1, cateIdx = 1)"
- [other] Enrichment function filters by p-value and returns result table: "The Enrichment() function takes enrichment parameters (EnrichParam) configured via KEGG_Enrich_PlotPanel() with enrichDB='kegg', pvalcutoff=0.05, IDtype=1, and cateIdx=1, and returns"
- [other] p-value threshold as filtering criterion in workflow: "Execute Enrichment() function with parameters enrichDB='kegg', IDtype=1, and pvalcutoff=0.05 to compute enrichment statistics and filter results by p-value threshold."
- [readme] Enrichment result table passed to visualization: "EnrichResultList <- Enrichment(EnrichParam); KEGG_Enrich_Plot(EnrichResultList = EnrichResultList, cpdID = sampleDatakegg, cpdFC = EnrichFC)"
