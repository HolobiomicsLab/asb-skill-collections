---
name: metabolite-genomic-network-mapping
description: Use when you have independent metabolomic GWAS results (metabolite p-values, effect sizes) and separate meta-genome GWAS results (variant p-values, effect sizes) from similar diseases or phenotypes, and you want to identify statistically enriched metabolite–gene co-occurrences without paired.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3559
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3517
  - http://edamontology.org/topic_0602
  tools:
  - R
  - metGWAS 1.0
  - KEGG
  - HMDB
  - GWAS Catalog
derived_from:
- doi: 10.1093/bioinformatics/btad523/7248906
  title: metGWAS 1.0
evidence_spans:
- An R workflow for network-driven over-representation analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metgwas_1_0_cq
    doi: 10.1093/bioinformatics/btad523/7248906
    title: metGWAS 1.0
  dedup_kept_from: coll_metgwas_1_0_cq
schema_version: 0.2.0
---

# metabolite-genomic-network-mapping

## Summary

Map disease-associated metabolites and genomic variants to their respective nodes in a biological interaction network, then perform statistical over-representation analysis to link independent metabolomic and meta-genome GWAS results. This enables discovery of novel metabolite–gene associations when paired studies are unavailable.

## When to use

You have independent metabolomic GWAS results (metabolite p-values, effect sizes) and separate meta-genome GWAS results (variant p-values, effect sizes) from similar diseases or phenotypes, and you want to identify statistically enriched metabolite–gene co-occurrences without paired metabolomics-GWAS data. Use this when standalone studies are available but direct paired analysis is not feasible.

## When NOT to use

- You have paired metabolomics-GWAS data from the same cohort (use direct association analysis instead)
- Metabolites or variants cannot be mapped to known interaction networks due to lack of annotation
- You are working with a single study rather than independent datasets (network-driven integration requires multiple studies)

## Inputs

- metabolomic GWAS summary statistics (p-values, effect sizes, metabolite identifiers)
- meta-genome GWAS summary statistics (p-values, effect sizes, genomic variant identifiers)
- metabolite-protein interaction database (e.g., KEGG, HMDB)
- GWAS network representation (e.g., GWAS Catalog network graph)

## Outputs

- over-representation analysis results table (feature names, enrichment scores, adjusted p-values, network membership)
- ranked list of enriched metabolite–gene associations
- network-mapped metabolite and variant sets

## How to apply

First, load metabolomic GWAS results and meta-genome GWAS results into R, then filter associations by a significance threshold (e.g., p < 0.05 or p < 0.005 depending on stringency). Map filtered metabolites to interacting proteins (genes) using online databases (e.g., KEGG, HMDB), and map genomic variants to their associated genes using the metGWAS 1.0 GWAS network representation. For each metabolic pathway or gene set, perform a hypergeometric test to compute enrichment of co-occurring metabolite–variant associations against the background network structure. Adjust p-values using Benjamini–Hochberg correction and rank results by adjusted significance. Export a results table with feature names, enrichment scores, adjusted p-values, and network membership.

## Related tools

- **metGWAS 1.0** (R workflow for performing network-driven over-representation analysis between metabolomic and meta-genome GWAS results using hypergeometric testing and GWAS Catalog network integration) — https://github.com/saifurbd28/metGWAS-1.0
- **KEGG** (Metabolic pathway and metabolite-protein interaction database for mapping disease-associated metabolites to interacting genes)
- **HMDB** (Human Metabolome Database used to identify discoverable genes for metabolite annotation (discoverableGenes_akaAllGenesInHMDB))
- **GWAS Catalog** (Network representation of GWAS studies used to identify genomic gene sets and variant-gene associations)

## Examples

```
source('metGWAS_1.0_19_April.R'); results <- metGWAS_analysis(metabolomic_gwas_file, genomic_gwas_file, network_database, p_threshold = 0.05)
```

## Evaluation signals

- Adjusted p-values (Benjamini–Hochberg) are computed and fall within the expected range (0–1), with significant results below your chosen threshold (e.g., p < 0.05 or p < 0.10)
- Enriched metabolite–gene associations can be validated against the original paired metabolomics-GWAS literature (e.g., case study 1 matched APOA5 from cardiovascular disease study)
- Network coverage is adequate: most input metabolites and variants map to known database nodes; unmapped features are documented
- Enrichment scores (hypergeometric test statistics) and gene sets are consistent with known biological pathways (e.g., glycerophospholipid metabolism for cardiovascular disease)
- Output results table contains no missing values in key columns (feature names, enrichment scores, adjusted p-values, pathway membership)

## Limitations

- Analysis is limited to genes with known metabolite interactions due to the unpaired nature of the datasets; novel metabolites or variants without database annotation cannot be assessed
- Results depend on the completeness and currency of reference databases (KEGG, HMDB, GWAS Catalog); outdated or sparse annotations reduce power
- Hypergeometric test assumes independence of metabolite–variant associations and may inflate significance if underlying correlation structure is not accounted for
- Discovery power is marginal when pathway-level enrichment is weak (e.g., case study 2 reported P = 0.10–0.13, suggesting borderline significance)

## Evidence

- [intro] metGWAS 1.0 integrates metabolomic and meta-genome GWAS through network-driven over-representation: "An R workflow for network-driven over-representation analysis between independent metabolomic and meta-genome wide association studies"
- [readme] Metabolic gene sets are generated by mapping metabolites to proteins; genomic gene sets from GWAS Catalog network: "Metabolic gene sets are generated by mapping disease-associated metabolites to interacting proteins (genes) via online databases. Genomic gene sets are identified from a network representation of the"
- [readme] Hypergeometric test is the primary statistical method for enrichment: "metGWAS 1.0, that generates and statistically compares metabolic and genomic gene sets using a hypergeometric test"
- [readme] Case study 1 identified nine genes in glycerophospholipid metabolism pathway linked to cardiovascular disease: "we identified nine genes (APOA5, PLA2G5, PLA2G2D, PLA2G2E, PLA2G2F, LRAT, PLA2G2A, PLB1, and PLA2G7) that interact with metabolites in the KEGG glycerophospholipid metabolism pathway"
- [readme] Analysis is constrained by known metabolite-gene interactions: "Although such an analysis is limited to genes with known metabolite interactions due to the unpaired nature of the data sets"
