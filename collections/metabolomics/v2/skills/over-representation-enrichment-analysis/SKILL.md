---
name: over-representation-enrichment-analysis
description: Use when you have p-values and effect sizes from two independent association studies (metabolomic GWAS and meta-genome GWAS) and want to identify whether variants associated with disease phenotypes co-occur with metabolites that share biochemical pathways or protein interactions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_3517
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_0091
  tools:
  - R
  - metGWAS 1.0
  - KEGG database
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btad523/7248906
  all_source_dois:
  - 10.1093/bioinformatics/btad523/7248906
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# over-representation-enrichment-analysis

## Summary

A statistical method that tests whether disease-associated metabolites or genomic variants are non-randomly enriched in known biological pathways or gene sets. This skill bridges independent metabolomic and GWAS studies by mapping their results to shared biological networks and quantifying co-occurrence significance using hypergeometric tests.

## When to use

You have p-values and effect sizes from two independent association studies (metabolomic GWAS and meta-genome GWAS) and want to identify whether variants associated with disease phenotypes co-occur with metabolites that share biochemical pathways or protein interactions. Use this when standalone studies lack paired sample designs but you need to statically evaluate cross-study signal.

## When NOT to use

- Both input datasets are paired (metabolite and variant measurements from the same samples); use direct co-association or correlation analysis instead.
- No known metabolite–gene interaction network exists for your biological domain.
- Input data are already collapsed into pathway or gene-set level summaries; this skill requires raw variant and metabolite association lists.

## Inputs

- metabolomic GWAS results (p-values, effect sizes, metabolite identifiers)
- meta-genome GWAS results (p-values, effect sizes, genomic variant identifiers)
- biological network database mapping metabolites to interacting proteins/genes
- pathway or gene set annotations (e.g., KEGG, HMDB)

## Outputs

- over-representation results table with feature names, enrichment scores, adjusted p-values, and network membership
- ranked list of significantly enriched metabolite–gene pathways
- multiple-testing corrected p-values per gene set

## How to apply

Filter associations from each study by a significance threshold (typically p < 0.05 or user-specified cutoff). Map the resulting metabolite and genomic variant identifiers to their corresponding biological network nodes using reference databases (e.g., KEGG pathways, HMDB protein interactions). Group associations into gene sets based on pathway or protein membership. For each gene set, apply a hypergeometric test to compute enrichment statistics, comparing the observed co-occurrence of metabolite–variant pairs against the background network structure. Adjust p-values for multiple testing using Benjamini–Hochberg correction. Rank enriched features by adjusted significance and report feature names, enrichment scores, adjusted p-values, and network membership.

## Related tools

- **metGWAS 1.0** (R workflow that implements network-driven over-representation analysis via hypergeometric test, mapping of metabolites and variants to network nodes, and multiple-testing correction) — https://github.com/saifurbd28/metGWAS-1.0
- **KEGG database** (Source for pathway and biochemical interaction annotations used to generate metabolic gene sets)
- **HMDB** (Source for metabolite-to-protein interaction mapping)
- **GWAS Catalog** (Network representation of hundreds of GWAS studies from which genomic gene sets are derived)

## Examples

```
source('metGWAS_1.0_19_April.R'); metGWAS_workflow(metabolomics_pvals, gwas_pvals, network_db, p_threshold=0.05, correction_method='BH')
```

## Evaluation signals

- Adjusted p-values from Benjamini–Hochberg correction are monotonically ordered and each adjusted p ≥ original p for the same feature.
- Enriched genes reported in results are confirmed to exist in both the metabolite–protein interaction database (HMDB) and the GWAS Catalog network.
- Hypergeometric test p-values for top-ranked pathways are reproducible by independently computing the cumulative hypergeometric distribution on the same contingency tables.
- Case study validation: genes identified (e.g., APOA5 in cardiovascular disease, glycerophospholipid metabolism) are documented in prior paired metabolomics-GWAS literature or show established metabolic relevance.
- Negative control: permuting metabolite–variant mappings or shuffling network edges should substantially increase (weaken) enrichment p-values.

## Limitations

- Analysis is limited to genes with known metabolite interactions; novel metabolite–gene pairs cannot be discovered by this method due to the unpaired nature of input datasets.
- Results depend critically on the completeness and accuracy of the metabolite–protein interaction database and GWAS Catalog; missing or incorrect mappings will produce false negatives or false positives.
- Marginal significance (e.g., P = 0.10–0.13) may be observed when pathway signals are weak or sample sizes in source studies are small, limiting actionability.
- Hypergeometric test assumes independence of gene set memberships; genes or metabolites present in multiple pathways may inflate or deflate apparent enrichment.

## Evidence

- [other] metGWAS 1.0 is an R workflow designed to perform network-driven over-representation analysis that integrates and links results from independent metabolomic and meta-genome wide association studies.: "metGWAS 1.0 is an R workflow designed to perform network-driven over-representation analysis that integrates and links results from independent metabolomic and meta-genome wide association studies."
- [other] Perform over-representation analysis by computing enrichment statistics for co-occurring metabolite–variant associations against the background network structure.: "Perform over-representation analysis by computing enrichment statistics for co-occurring metabolite–variant associations against the background network structure."
- [readme] We developed a bioinformatics tool, metGWAS 1.0, that generates and statistically compares metabolic and genomic gene sets using a hypergeometric test.: "We developed a bioinformatics tool, metGWAS 1.0, that generates and statistically compares metabolic and genomic gene sets using a hypergeometric test."
- [readme] Metabolic gene sets are generated by mapping disease-associated metabolites to interacting proteins (genes) via online databases.: "Metabolic gene sets are generated by mapping disease-associated metabolites to interacting proteins (genes) via online databases."
- [other] Adjust p-values for multiple testing (e.g., Benjamini–Hochberg correction) and rank enriched features by significance.: "Adjust p-values for multiple testing (e.g., Benjamini–Hochberg correction) and rank enriched features by significance."
- [readme] Although such an analysis is limited to genes with known metabolite interactions due to the unpaired nature of the data sets, any discovered associations may represent biomarkers and druggable targets for treatment and prevention.: "Although such an analysis is limited to genes with known metabolite interactions due to the unpaired nature of the data sets, any discovered associations may represent biomarkers and druggable"
