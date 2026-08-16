---
name: pathway-enrichment-visualization
description: Use when after running ORA on a set of significant metabolite PubChemCIDs
  (e.g., features with q-value < 1e-9 from ANOVA) against a metabolic pathway database,
  and you need to identify and communicate which pathways are robustly enriched in
  your case.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - clusterProfiler
  - margheRita
  - R
  - ComplexHeatmap
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- margheRita implements both Over Representation Analysis (ORA) and Metabolite Set
  Enrichment Analysis (MSEA), based on clusterProfiler
- The R package margheRita addresses the complete workflow for metabolomic profiling
  in untargeted studies based on liquid chromatography (LC) coupled with tandem mass
  spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
- The R package margheRita addresses the complete workflow
- The R package margheRita
- The function `h_map()` provides heatmaps based on package ComplexHeatmap
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_margherita_cq
    doi: 10.1101/2024.06.20.599545v1
    title: MargheRita
  dedup_kept_from: coll_margherita_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.06.20.599545v1
  all_source_dois:
  - 10.1101/2024.06.20.599545v1
  - 10.1101/2024.06.20.599545
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pathway-enrichment-visualization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate and visualize metabolic pathway enrichment results from Over Representation Analysis (ORA) of significant metabolites, ranked by statistical significance and filtered by robust effect size. This skill transforms ORA output into publication-ready barplots and tabular summaries for biological interpretation.

## When to use

After running ORA on a set of significant metabolite PubChemCIDs (e.g., features with q-value < 1e-9 from ANOVA) against a metabolic pathway database, and you need to identify and communicate which pathways are robustly enriched in your case. Use this skill when you have pathway-level test statistics (adjusted p-values, enrichment ratios) and want to highlight the most significant biological signals for downstream interpretation or publication.

## When NOT to use

- Input metabolites do not have robust PubChemCID mappings or annotation confidence is low (level < 1)
- The metabolic universe (background set) is not well-defined or does not represent all detected metabolites
- Pathway database lacks coverage for the metabolite class of interest (e.g., lipids, xenobiotics)

## Inputs

- PubChemCIDs of significant metabolite features (from ANOVA or other statistical test with q-value threshold)
- Complete set of identified metabolites (metabolic universe) detected across the full dataset
- Pathway database mapping (e.g., KEGG, Reactome)
- ORA results object from clusterProfiler (containing pathway-level statistics)

## Outputs

- Barplot visualization of enriched pathways ranked by -log10(adjusted p-value)
- Enriched pathways table with pathway descriptions, adjusted p-values, enrichment ratios, and pathway sizes
- Filtered pathway list meeting significance and size thresholds

## How to apply

Execute ORA using clusterProfiler with significant PubChemCIDs queried against standard metabolic pathway databases (e.g., KEGG, Reactome), then filter enriched pathways by adjusted p-value threshold (e.g., q < 0.05) and minimum pathway size to ensure robustness. Compute -log10(adjusted p-value) for each pathway as the ranking metric. Generate a barplot with pathways ranked along the x-axis and -log10(adjusted p-value) on the y-axis, color-coded by effect direction or pathway class. Simultaneously export a table containing pathway descriptions, adjusted p-values, enrichment counts, and pathway sizes to support the visualization and enable cross-reference with biological databases.

## Related tools

- **clusterProfiler** (Executes over-representation analysis (ORA) on significant PubChemCIDs against metabolic pathway databases and computes adjusted p-values)
- **ComplexHeatmap** (Generates publication-ready barplot and heatmap visualizations of enriched pathways and their associated statistics)
- **margheRita** (Integrates ORA and MSEA pathway analysis over various metabolic databases; handles end-to-end workflow from feature annotation to pathway visualization) — https://github.com/emosca-cnr/margheRita
- **R** (Programming environment for executing clusterProfiler ORA functions and generating visualizations)

## Evaluation signals

- Barplot displays only pathways with adjusted p-value below the specified threshold (e.g., q < 0.05); no pathways violating this criterion appear
- Pathway ranking on the barplot is monotonically decreasing by -log10(adjusted p-value); highest enrichment significance on the left
- Exported enriched pathways table contains valid PubChemCID-to-pathway mappings and non-zero enrichment counts for all listed pathways
- Pathway size filtering is consistently applied: minimum and maximum pathway member counts are documented and enforced across all results
- Visualization legend or color scheme distinguishes pathway categories or enrichment direction (if applicable) and is consistent with table annotations

## Limitations

- ORA performance depends on the quality and completeness of the pathway database; sparse or outdated KEGG/Reactome mappings may miss true enrichments
- Results are sensitive to the significance threshold chosen for the input feature set (e.g., q-value cutoff); overly stringent thresholds reduce statistical power
- Pathway size thresholds must be tuned to balance statistical robustness against loss of biologically relevant small pathways
- PubChemCID annotation gaps or ambiguities in metabolite identification (level < 1) reduce the number of metabolites successfully queried against pathway databases

## Evidence

- [other] Extract PubChemCIDs corresponding to metabolite features meeting the most stringent ANOVA significance threshold from the Urine dataset (both RP_NEG and RP_POS polarities). Define the metabolic universe as all metabolites detected across the full Urine dataset. Execute over-representation analysis (ORA) using clusterProfiler with the significant PubChemCIDs queried against standard metabolic pathway databases (e.g., KEGG, Reactome).: "Execute over-representation analysis (ORA) using clusterProfiler with the significant PubChemCIDs queried against standard metabolic pathway databases (e.g., KEGG, Reactome)."
- [other] Filter enriched pathways by adjusted p-value and pathway size thresholds to identify robust enrichments. Generate a barplot visualization of top enriched pathways ranked by -log10(adjusted p-value) and export the results table.: "Filter enriched pathways by adjusted p-value and pathway size thresholds to identify robust enrichments. Generate a barplot visualization of top enriched pathways ranked by -log10(adjusted p-value)"
- [readme] margheRita implements both Over Representation Analysis (ORA) and Metabolite Set Enrichment Analysis (MSEA), based on clusterProfiler: "margheRita implements both Over Representation Analysis (ORA) and Metabolite Set Enrichment Analysis (MSEA), based on clusterProfiler"
- [readme] pathway analysis based on ORA and MSEA over various databases: "pathway analysis based on ORA and MSEA over various databases"
- [other] The function `h_map()` provides heatmaps based on package ComplexHeatmap: "The function `h_map()` provides heatmaps based on package ComplexHeatmap"
