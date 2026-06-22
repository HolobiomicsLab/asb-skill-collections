---
name: metabolomic-biomarker-pathway-association
description: Use when after marker identification (via fold-change, PLS-DA, t-test, or other feature selection methods) has produced a ranked list of metabolic features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - ggplot2
  - igraph
  - KEGG_Enrich_PlotPanel
  - Enrichment
  - KEGG_Enrich_Plot
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
---

# metabolomic-biomarker-pathway-association

## Summary

This skill links identified metabolomic biomarkers to biological pathways through enrichment analysis, enabling interpretation of marker compounds in the context of KEGG or custom databases. It transforms a list of compound identifiers and their fold-change values into pathway statistics and visualizations.

## When to use

After marker identification (via fold-change, PLS-DA, t-test, or other feature selection methods) has produced a ranked list of metabolic features. Use this skill when you need to assign biological relevance to detected biomarkers by testing whether they are overrepresented in known metabolic pathways, with statistical filtering (p-value cutoff, typically 0.05) to focus on significant associations.

## When NOT to use

- Input compound list is empty or contains <3 compounds; enrichment analysis requires sufficient sample size to detect meaningful pathway associations.
- Compound identifiers do not match the selected database schema (e.g., using HMDB IDs when IDtype=1 expects KEGG compound IDs); incorrect ID mapping will result in zero or very low enrichment hits.
- No prior biomarker selection or filtering has been performed; enrichment on an unfiltered feature list dilutes signal and inflates multiple-testing burden.

## Inputs

- Compound list (data frame or vector with compound IDs; e.g., sampleDatakegg)
- Fold-change values (numeric vector aligned to compound IDs)
- Enrichment parameter object (EnrichParam) configured via KEGG_Enrich_PlotPanel()
- Target enrichment database ('kegg' or custom; specified via enrichDB parameter)

## Outputs

- EnrichResultList (table of KEGG/database pathway enrichment results with p-values, enrichment counts, and pathway identifiers)
- Enrichment statistics table (pathway name, compound count, p-value, fold-change summary)
- Pathway visualization (ggplot2 plot or igraph network diagram showing enriched pathways and compound associations)

## How to apply

Begin with a compound list (sampleDatakegg) containing identifiers and fold-change values. Configure enrichment parameters using KEGG_Enrich_PlotPanel() with enrichDB='kegg' (or custom database), pvalcutoff=0.05, IDtype=1 (for KEGG compound IDs), and cateIdx=1 to specify pathway category. Pass the configured EnrichParam to Enrichment(), which returns EnrichResultList—a table of pathway-level statistics (p-values, enrichment counts, pathway names). Filter results by p-value threshold (0.05) to retain only significant pathways. Finally, invoke KEGG_Enrich_Plot() with EnrichResultList, compound IDs, and fold-change vector (e.g., seq(from=-2, to=2, length.out=24)) to produce pathway network or bar-plot visualizations. The rationale is that compounds clustering in the same pathway suggest coordinated metabolic perturbation and strengthen biological interpretation.

## Related tools

- **KEGG_Enrich_PlotPanel** (Configures enrichment parameters (database, p-value cutoff, ID type, category index) before enrichment computation) — https://github.com/LargeMetabo/LargeMetabo
- **Enrichment** (Executes enrichment statistical test and returns pathway-level results table filtered by p-value threshold) — https://github.com/LargeMetabo/LargeMetabo
- **KEGG_Enrich_Plot** (Visualizes enrichment results as network or bar plots using ggplot2 and igraph, integrating fold-change values) — https://github.com/LargeMetabo/LargeMetabo
- **ggplot2** (Graphics backend for pathway enrichment visualization)
- **igraph** (Network graph construction for pathway-compound association visualization)

## Examples

```
sampleDatakegg <- EnrichData$sampleDatakegg; EnrichParam <- KEGG_Enrich_PlotPanel(sampleDatakegg, enrichDB = "kegg", pvalcutoff = 0.05, IDtype = 1, cateIdx = 1); EnrichResultList <- Enrichment(EnrichParam); EnrichFC <- seq(from = -2, to = 2, length.out = 24); KEGG_Enrich_Plot(EnrichResultList = EnrichResultList, cpdID = sampleDatakegg, cpdFC = EnrichFC)
```

## Evaluation signals

- EnrichResultList contains non-empty table with columns for pathway ID, compound count, p-value, and pathway name; all p-values ≤ pvalcutoff (0.05).
- Number of enriched pathways is ≥1 and <total pathway count in database; extreme values (0 or >50% of database) suggest ID mismatch or overly permissive threshold.
- Visualization renders without errors and displays only pathways with p < pvalcutoff; fold-change color scale or node size reflects magnitude and direction of biomarker perturbation.
- Enriched pathways are biologically interpretable relative to study design (e.g., disease-relevant pathways if comparing disease vs. control biomarkers).
- Results are reproducible: same compound list and parameters produce identical EnrichResultList and visualization across independent runs.

## Limitations

- Enrichment analysis depends critically on ID type and database version; mismatched IDs result in zero enrichment hits or spurious associations.
- P-value threshold (0.05) is arbitrary; multiple-testing correction (e.g., Benjamini–Hochberg FDR) is not explicitly discussed in the README and should be considered for large biomarker lists.
- Pathway annotation is static and reflects the chosen database snapshot (KEGG, MetLin, or custom); novel or understudied pathways will not be detected.
- Enrichment does not infer causality or regulatory hierarchy; compounds in the same pathway may reflect independent or downstream responses rather than coordinated metabolic control.

## Evidence

- [other] enrichDB='kegg', pvalcutoff=0.05, IDtype=1, and cateIdx=1: "The Enrichment() function takes enrichment parameters (EnrichParam) configured via KEGG_Enrich_PlotPanel() with enrichDB='kegg', pvalcutoff=0.05, IDtype=1, and cateIdx=1, and returns"
- [other] KEGG enrichment visualization panels and result export: "Call KEGG_Enrich_PlotPanel() to generate preliminary KEGG enrichment visualization panels. 3. Execute Enrichment() function with parameters enrichDB='kegg', IDtype=1, and pvalcutoff=0.05 to compute"
- [readme] Compound list input for KEGG enrichment: "When performing enrichment analysis for KEGG pathways, a compound list should be properly provided. An example input for enrichment analysis for the KEGG pathways is provided in the LargeMetabo"
- [readme] EnrichResultList passed to KEGG_Enrich_Plot with fold-change values: "EnrichResultList <- Enrichment(EnrichParam); EnrichFC <- seq(from = -2,to = 2, length.out = 24); KEGG_Enrich_Plot(EnrichResultList = EnrichResultList, cpdID = sampleDatakegg, cpdFC = EnrichFC)"
- [other] Tools supporting enrichment visualization: "several R packages are utilized in the background processes, including ggplot2, igraph"
