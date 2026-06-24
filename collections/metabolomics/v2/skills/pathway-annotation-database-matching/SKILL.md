---
name: pathway-annotation-database-matching
description: Use when after marker identification or metabolite annotation has produced
  a curated list of compound IDs (e.g., KEGG IDs or CAS numbers) and you need to determine
  which metabolic pathways are statistically overrepresented in your dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
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

# pathway-annotation-database-matching

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Match metabolite compound lists to KEGG pathway databases and compute enrichment statistics to identify which biological pathways are significantly represented in a metabolomic dataset. This skill transforms a compound identifier list into a ranked table of enriched pathways with p-values and gene set membership.

## When to use

Apply this skill after marker identification or metabolite annotation has produced a curated list of compound IDs (e.g., KEGG IDs or CAS numbers) and you need to determine which metabolic pathways are statistically overrepresented in your dataset. Use it when the analysis goal is to move from individual metabolite hits to biological pathway interpretation.

## When NOT to use

- Compound list contains only unannotated m/z values with no database identifier mapping — pathway matching requires resolved metabolite IDs (KEGG or CAS)
- Analysis goal is to annotate individual metabolites rather than interpret pathway enrichment — use metabolite annotation functions (Metabo_Annotation, Annota_Tandem) instead
- Dataset is from a non-model organism or metabolite panel not covered by KEGG — consider alternative enrichment databases via the enrichDB parameter

## Inputs

- compound_list (vector or data frame with metabolite identifiers and optional fold-change values)
- enrichment_parameters (EnrichParam object configured via KEGG_Enrich_PlotPanel)
- identifier_type_code (numeric: 1 for KEGG ID, 2 for CAS number)

## Outputs

- EnrichResultList (data frame/table of enriched pathways with columns: pathway name, p-value, adjusted p-value, gene set size, overlap count)
- pathway_visualization (ggplot object or PNG when KEGG_Enrich_Plot() is called)

## How to apply

First, prepare a compound list (sampleDatakegg) with metabolite identifiers and optional fold-change values. Call KEGG_Enrich_PlotPanel() to configure enrichment parameters: set enrichDB='kegg' to query KEGG pathway database, pvalcutoff=0.05 to filter results by significance threshold, IDtype to specify identifier format (1=KEGG ID, 2=CAS number), and cateIdx to select pathway category. Pass the resulting EnrichParam object to Enrichment() to compute pathway membership overlap and hypergeometric p-values, returning EnrichResultList—a table of pathways ranked by statistical significance. Optionally call KEGG_Enrich_Plot() with compound fold-changes (cpdFC) to visualize enriched pathways alongside metabolite-level effect sizes.

## Related tools

- **KEGG_Enrich_PlotPanel** (Configures enrichment parameters (database, p-value threshold, identifier type, pathway category) before computation) — https://github.com/LargeMetabo/LargeMetabo
- **Enrichment** (Core function that computes pathway membership statistics and p-values from configured parameters) — https://github.com/LargeMetabo/LargeMetabo
- **KEGG_Enrich_Plot** (Visualizes enriched pathways and overlays compound fold-change values for interpretation) — https://github.com/LargeMetabo/LargeMetabo
- **ggplot2** (Graphics rendering backend for pathway enrichment visualization)
- **igraph** (Network graph support for pathway topology visualization)

## Examples

```
EnrichParam <- KEGG_Enrich_PlotPanel(sampleDatakegg, enrichDB = "kegg", pvalcutoff = 0.05, IDtype = 1, cateIdx = 1); EnrichResultList <- Enrichment(EnrichParam); KEGG_Enrich_Plot(EnrichResultList = EnrichResultList, cpdID = sampleDatakegg, cpdFC = EnrichFC)
```

## Evaluation signals

- EnrichResultList contains pathways with p-values all ≤ pvalcutoff (0.05 by default); verify filtering was applied correctly
- Number of enriched pathways is reasonable for dataset size and compound list length (typically 5–50 pathways for metabolomic studies); extreme values suggest parameter miscalibration
- Pathway overlap sizes and p-value ranks are consistent with biological expectation (e.g., lipid metabolism should rank high if lipids dominate markers)
- Fold-change visualization (if generated) shows expected direction of metabolite regulation within top pathways; unexpected patterns suggest compound list quality issue
- Result table contains no missing or NA values in required columns (pathway ID, p-value, overlap count); completeness indicates successful database matching

## Limitations

- KEGG pathway coverage is incomplete for non-model organisms and emerging metabolites; some annotated compounds may not match any pathway
- Hypergeometric test assumes independence of pathways, but true pathway networks contain overlapping and nested relationships
- p-value cutoff (0.05) is a fixed threshold and does not account for multiple-testing correction across many pathways; consider Benjamini–Hochberg adjustment for exploratory work
- Identifier type must be specified correctly (IDtype=1 for KEGG, IDtype=2 for CAS); mismatch silently reduces pathway matches and inflates false negatives
- Pathway enrichment results depend critically on upstream compound annotation quality; errors or missing identifiers in the compound list propagate directly to enrichment output

## Evidence

- [readme] compound_list_requirement: "When performing enrichment analysis for KEGG pathways, a compound list should be properly provided."
- [readme] enrichment_parameters_config: "EnrichParam <- KEGG_Enrich_PlotPanel(sampleDatakegg, enrichDB = "kegg", pvalcutoff = 0.05, IDtype = 1, cateIdx = 1)"
- [readme] enrichment_computation: "EnrichResultList <- Enrichment(EnrichParam)"
- [other] enrichment_result_output: "returns EnrichResultList—a table of KEGG enrichment results that can be passed to KEGG_Enrich_Plot() for visualization alongside compound IDs and fold-change values"
- [readme] visualization_integration: "KEGG_Enrich_Plot(EnrichResultList = EnrichResultList, cpdID = sampleDatakegg, cpdFC = EnrichFC)"
