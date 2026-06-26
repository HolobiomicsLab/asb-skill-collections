---
name: pathway-over-representation-analysis-ora
description: Use when apply ORA after conducting statistical tests (e.
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
  - KEGG / Reactome
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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

# Pathway Over-Representation Analysis (ORA)

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

ORA identifies metabolic pathways that are significantly enriched among a set of significant metabolites (e.g., those meeting stringent ANOVA q-value thresholds) when tested against the complete set of detected metabolites in an untargeted LC-MS/MS study. This provides biological interpretation of which canonical metabolic processes are disrupted or altered in the experimental condition.

## When to use

Apply ORA after conducting statistical tests (e.g., ANOVA) on normalized metabolite abundance data when you have identified a subset of significant features (metabolites with low adjusted p-values or q-values, typically q < 1e-9 for stringent filtering) and wish to determine which known metabolic pathways are over-represented in that subset relative to the universe of all detected metabolites.

## When NOT to use

- Input metabolite set is not derived from a rigorous statistical test (e.g., arbitrary cutoff on fold-change alone without p-value adjustment).
- Metabolic universe definition is incomplete or biased (e.g., only includes a subset of detected metabolites or uses a different detection method).
- Metabolite-to-pathway annotations are unavailable or severely incomplete for the organism/database combination.

## Inputs

- Metabolite feature table (normalized abundance matrix, e.g., Urine_RP_NEG_norm.txt, Urine_RP_POS_norm.txt from MS-DIAL output)
- ANOVA or statistical test results with q-values or adjusted p-values per metabolite feature
- PubChemCID or metabolite identifier mapping for significant features
- List of all detected metabolites (metabolic universe definition)

## Outputs

- Table of enriched pathways with pathway name, description, adjusted p-value, and pathway size
- Barplot visualization of top enriched pathways ranked by -log10(adjusted p-value)
- ORA results object (clusterProfiler enrichResult) with full statistics for downstream filtering or export

## How to apply

Extract the PubChemCIDs or other metabolite identifiers corresponding to metabolites meeting your statistical significance threshold (e.g., q-value < 1e-9 from ANOVA). Define the metabolic universe as all metabolites detected across the full dataset, irrespective of polarity or ionization mode. Execute ORA using clusterProfiler by querying the significant metabolite set against standard metabolic pathway databases (KEGG, Reactome, or similar). Filter enriched pathways by adjusted p-value threshold and pathway size (e.g., requiring minimum pathway membership) to retain robust, biologically meaningful enrichments. Rank results by -log10(adjusted p-value) and visualize the top enriched pathways as a barplot with accompanying results table.

## Related tools

- **clusterProfiler** (Executes over-representation analysis (ORA) on significant PubChemCIDs queried against metabolic pathway databases; implements both ORA and MSEA enrichment testing.) — https://bioconductor.org/packages/clusterProfiler
- **margheRita** (R package that wraps clusterProfiler for pathway analysis over various metabolic databases; provides complete workflow from MS-DIAL output to ORA/MSEA results including data normalization and statistical testing.) — https://github.com/emosca-cnr/margheRita
- **ComplexHeatmap** (Provides heatmap visualization of results and data exploration; used alongside barplot visualization of enriched pathways.) — https://bioconductor.org/packages/ComplexHeatmap
- **KEGG / Reactome** (Standard metabolic pathway databases queried during ORA to define pathway membership and calculate enrichment statistics.)

## Examples

```
# After computing ANOVA on normalized metabolite abundances and extracting significant PubChemCIDs (q < 1e-9):
# In R using margheRita:
enriched_pathways <- mR_enrichment(sig_pubchemcids, background_universe, database="KEGG", pvalue_cutoff=0.05)
```

## Evaluation signals

- Enriched pathways have adjusted p-value below threshold (typically padj < 0.05) and contain >2 metabolites from the significant set.
- Identified pathways are biologically plausible given the experimental context (e.g., urine metabolomics should recover renal/urinary metabolic processes).
- Barplot ranks pathways by -log10(adjusted p-value) in descending order with clear separation between highly enriched and marginal pathways.
- Results table includes pathway name, description, adjusted p-value, pathway size, and count of significant metabolites per pathway.
- PubChemCID mapping is bidirectional and complete: all significant metabolites in the input set map to at least one pathway database record, and no orphan or unmapped identifiers remain in results.

## Limitations

- ORA assumes that all metabolites in the universe have equal probability of being detected and reported; systematic bias in MS-DIAL peak picking or metabolite annotation can inflate or deflate enrichment scores.
- Pathway annotations depend on metabolic database currency and coverage; novel or poorly annotated metabolites will not contribute to any pathway and may reduce statistical power.
- ORA does not account for quantitative abundance differences (fold-change magnitudes) among significant metabolites; all members of the significant set are treated equally. Consider Metabolite Set Enrichment Analysis (MSEA) if ranked quantitative data are available.
- Cross-pathway dependencies and pathway overlap are not modeled; if two pathways share many metabolites, their enrichment statistics may be correlated and lead to redundant interpretations.
- Statistical significance of enrichment does not imply biological relevance; pathway size, metabolite measurement precision, and experimental design confound interpretation.

## Evidence

- [other] Extract PubChemCIDs corresponding to metabolite features meeting the most stringent ANOVA significance threshold from the Urine dataset (both RP_NEG and RP_POS polarities). Define the metabolic universe as all metabolites detected across the full Urine dataset. Execute over-representation analysis (ORA) using clusterProfiler with the significant PubChemCIDs queried against standard metabolic pathway databases (e.g., KEGG, Reactome).: "Extract PubChemCIDs corresponding to metabolite features meeting the most stringent ANOVA significance threshold from the Urine dataset (both RP_NEG and RP_POS polarities). Define the metabolic"
- [other] Filter enriched pathways by adjusted p-value and pathway size thresholds to identify robust enrichments. Generate a barplot visualization of top enriched pathways ranked by -log10(adjusted p-value) and export the results table.: "Filter enriched pathways by adjusted p-value and pathway size thresholds to identify robust enrichments. Generate a barplot visualization of top enriched pathways ranked by -log10(adjusted p-value)"
- [intro] margheRita implements both Over Representation Analysis (ORA) and Metabolite Set Enrichment Analysis (MSEA), based on clusterProfiler: "margheRita implements both Over Representation Analysis (ORA) and Metabolite Set Enrichment Analysis (MSEA), based on clusterProfiler"
- [other] Over Representation Analysis (ORA) of the most significant ANOVA features (q-value < 1e-9) from the Urine dataset identified enriched pathways represented in a table with pathway descriptions and visualization as a barplot.: "Over Representation Analysis (ORA) of the most significant ANOVA features (q-value < 1e-9) from the Urine dataset identified enriched pathways represented in a table with pathway descriptions and"
- [intro] pathway analysis based on ORA and MSEA over various databases: "pathway analysis based on ORA and MSEA over various databases"
