---
name: pathway-metabolite-mapping-integration
description: Use when when you have metabolite-level summary statistics (p-values, log2 fold changes) from differential analysis and need to test whether specific metabolic pathways are significantly enriched in your dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0199
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - R
  - fgsea
  - readr
  - readxl
  - enrichmet
  - KEGGREST
  - readxl / readr
  - igraph
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.08.28.672951v2
  all_source_dois:
  - 10.1101/2025.08.28.672951v2
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# pathway-metabolite-mapping-integration

## Summary

Integration of curated pathway-to-metabolite reference mappings with differential analysis results to establish the metabolic background context for enrichment testing. This skill enables Fisher's exact test and GSEA by defining which metabolites belong to which pathways, serving as the reference gene set for statistical significance assessment.

## When to use

When you have metabolite-level summary statistics (p-values, log2 fold changes) from differential analysis and need to test whether specific metabolic pathways are significantly enriched in your dataset. The skill is necessary whenever you plan to run pathway enrichment analysis, metabolite set enrichment analysis (MetSEA), or topology-based centrality calculations on metabolomic data.

## When NOT to use

- Your input metabolites are already aggregated at the pathway level; use this skill only with individual metabolite-level data.
- You have protein-centric pathway annotations (e.g., KEGG Orthology gene sets) instead of metabolite-specific mappings; metabolite-pathway databases (KEGG, LION lipid ontology) are required.
- Your reference mapping is incomplete or organism-specific (e.g., only bacteria metabolites) but your data is from a different organism; validate taxonomic consistency before integration.

## Inputs

- Differential analysis results table (metabolite ID, p-value, adjusted p-value, log2 fold change)
- PathwayVsMetabolites reference file (TSV/CSV with Pathway and Metabolites columns, metabolites comma-separated KEGG IDs)
- Input metabolite list (character vector of KEGG IDs or metabolite identifiers)
- Optional: KEGG lookup table (kegg_id → metabolite name) for annotation

## Outputs

- Validated pathway-metabolite mapping matrix (pathways × metabolites binary or count matrix)
- GMT-formatted gene set definitions (for fgsea input)
- Filtered pathway set passing occurrence thresholds (min_pathway_occurrence, min_metabolite_occurrence)
- Mapping diagnostic report (% metabolites matched, coverage statistics, pathway size distribution)

## How to apply

Load a curated PathwayVsMetabolites reference file that maps metabolic pathway names to their constituent metabolite KEGG IDs (using the format: Pathway | comma-separated KEGG IDs). Validate that all metabolites in your input data (from differential analysis results) have corresponding entries in the reference mapping. Apply filtering thresholds: retain pathways with min_pathway_occurrence ≥ 2 and metabolites with min_metabolite_occurrence ≥ 1 to avoid sparse gene sets in subsequent fgsea testing. For GSEA integration, prepare a ranked metabolite list sorted by a combined test statistic (e.g., signed p-value or log2 fold change × -log10(p-value)), then use the pathway-metabolite mappings as GMT-formatted gene set definitions. Validate mapping completeness by confirming that >90% of input metabolites match KEGG IDs in the reference file; metabolites without matches should be flagged for manual curation or excluded with justification.

## Related tools

- **enrichmet** (Integrates pathway-metabolite mapping with fgsea and Fisher's exact test to execute complete enrichment workflow; PathwayVsMetabolites is a required input parameter) — https://github.com/biodatalab/enrichmet
- **fgsea** (Performs fast Metabolite Set Enrichment Analysis using mapped gene set definitions (GMT) prepared from pathway-metabolite integration; computes Normalized Enrichment Scores)
- **KEGGREST** (Retrieves pathway-to-metabolite mappings from KEGG database; used to obtain or validate reference mappings)
- **readxl / readr** (Loads curated PathwayVsMetabolites reference files and KEGG lookup tables from Excel or CSV formats)
- **igraph** (Builds metabolite-pathway network from validated mapping for topology-based centrality metrics)

## Examples

```
```r
PathwayVsMetabolites <- read.csv('human_pathway.csv')
kegg_lookup <- read.xlsx('kegg_lookup.xlsx')
results <- enrichmet(inputMetabolites = inputMetabolites, PathwayVsMetabolites = PathwayVsMetabolites, da_results = da_out, kegg_lookup = kegg_lookup, min_pathway_occurrence = 2, min_metabolite_occurrence = 1, p_value_cutoff = 0.05)
```
```

## Evaluation signals

- Mapping coverage: ≥90% of input metabolites successfully matched to at least one pathway in the reference file; documented metadata report for unmatched IDs.
- Pathway size distribution inspection: median pathway size 5–15 metabolites (minimum 5 after filtering); no single pathway contains >80% of metabolites (indicates overgeneralization).
- Filtered pathway and metabolite counts meet thresholds: min_pathway_occurrence ≥ 2 and min_metabolite_occurrence ≥ 1; before/after filtering statistics reported.
- GMT format validity: each pathway produces ≥5 metabolites after mapping (fgsea minimum); no duplicate pathway-metabolite pairs; all KEGG IDs are properly formatted (C##### or split-handled).
- Downstream test stability: fgsea runs without errors on the mapped gene set definitions; Fisher's exact test contingency tables for top pathways are interpretable (counts non-negative, totals consistent).

## Limitations

- Reference mapping quality depends on curation source (KEGG, LION, or custom); outdated or organism-specific mappings may omit newly discovered metabolites or miss species-level pathway variants.
- Metabolite identification ambiguity: multiple KEGG IDs may represent the same compound under different ionization or derivatization states; the integration step assumes exact KEGG ID matching and does not perform fuzzy matching.
- Pathway granularity mismatch: KEGG pathways are sometimes hierarchical (parent/child) or overlapping; standard mapping treats each pathway independently, potentially inflating the size of parent pathways and reducing statistical power for child pathways.
- Sparse pathways after filtering: if min_pathway_occurrence or min_metabolite_occurrence thresholds are too stringent, valid but rare metabolite-pathway associations are excluded, reducing biological insight.
- Missing data handling: metabolites without corresponding p-values or fold changes in the differential analysis results cannot be ranked for GSEA; they are excluded without imputation, potentially biasing pathway scores if the missing data are not Missing Completely At Random.

## Evidence

- [readme] This file defines the mapping between metabolic pathways and their associated metabolites and serves as the background reference for the Fisher exact test used during enrichment: "Provide PathwayVsMetabolites input file defining mapping between metabolic pathways and their associated metabolites and serves as the background reference for the Fisher exact test"
- [intro] pathway to metabolite mappings are obtained from the KEGG resource using the KEGGREST package: "pathway to metabolite mappings are obtained from the KEGG resource using the KEGGREST package"
- [intro] curated KEGG data for enrichment using Fisher's Exact Test: "enrichmet integrates fgsea for fast MetSEA, igraph for topology-based metrics, and curated KEGG data for enrichment using Fisher's Exact Test"
- [intro] curated human specific pathway to metabolite mappings are periodically updated and made available on Zenodo: "curated human specific pathway to metabolite mappings are periodically updated and made available on Zenodo"
- [other] Prepare ranked metabolite list sorted by test statistic (e.g., log2 fold change or -log10(p-value)) for input to fgsea: "Prepare ranked metabolite list sorted by test statistic (e.g., log2 fold change or -log10(p-value)) for input to fgsea"
- [intro] Filter pathways using min_pathway_occurrence parameter and metabolites using min_metabolite_occurrence parameter: "Filter pathways using min_pathway_occurrence parameter and Filter metabolites using min_metabolite_occurrence parameter"
- [intro] lipid ontology mapping file was generated in the same format as the PathwayVsMetabolites dataset created using data from the LION lipid ontology database: "lipid ontology mapping file was generated in the same format as the PathwayVsMetabolites dataset created using data from the LION lipid ontology database"
