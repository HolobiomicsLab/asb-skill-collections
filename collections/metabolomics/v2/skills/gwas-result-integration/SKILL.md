---
name: gwas-result-integration
description: Use when you have independent metabolomic GWAS results (metabolite p-values, effect sizes, metabolite IDs) and separate meta-genome GWAS results (variant p-values, effect sizes, genomic variant IDs) from similar diseases or phenotypes, and you want to discover novel metabolite–gene associations and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3375
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btad523/7248906
  all_source_dois:
  - 10.1093/bioinformatics/btad523/7248906
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# gwas-result-integration

## Summary

Integrate independent metabolomic and meta-genome wide association study results through network-driven over-representation analysis, mapping disease-associated metabolites to interacting genes and comparing them against a GWAS-derived gene network using hypergeometric enrichment testing.

## When to use

You have independent metabolomic GWAS results (metabolite p-values, effect sizes, metabolite IDs) and separate meta-genome GWAS results (variant p-values, effect sizes, genomic variant IDs) from similar diseases or phenotypes, and you want to discover novel metabolite–gene associations and potential biomarkers by leveraging existing metabolite–protein interaction databases and GWAS catalogs without paired metabolomics-GWAS data.

## When NOT to use

- You have only a single standalone metabolomics or GWAS study and no independent comparator dataset.
- Your metabolites or variants map to fewer than 5–10 genes in the reference databases; hypergeometric testing requires sufficient overlap to be meaningful.
- You have paired metabolomics-GWAS data from a single cohort; direct association testing is more powerful than network-based over-representation.

## Inputs

- Metabolomic GWAS results table (metabolite identifiers, p-values, effect sizes)
- Meta-genome GWAS results table (genomic variant identifiers, p-values, effect sizes)
- KEGG or equivalent pathway/protein interaction database
- GWAS Catalog network representation (100s of compiled GWAS studies)

## Outputs

- Over-representation results table (gene names, enriched pathways, enrichment p-values, adjusted p-values, network membership)
- List of candidate metabolite–gene associations ranked by statistical significance

## How to apply

Load metabolomic GWAS results and meta-genome GWAS results into R. Filter associations by a significance threshold (typically p < 0.05 or user-specified cutoff). Map metabolites to interacting proteins (genes) using online databases such as KEGG, and map genomic variants to genes using a pre-computed GWAS Catalog network. Generate metabolic gene sets from disease-associated metabolites and genomic gene sets from the GWAS network representation. Perform a hypergeometric test to statistically compare the two gene sets and compute enrichment p-values. Adjust p-values for multiple testing (e.g., Benjamini–Hochberg correction) and rank results by significance. The rationale is that co-occurrence of metabolite–gene and variant–gene associations in pathway-level gene sets provides evidence for shared biological mechanisms even when the original studies are unpaired.

## Related tools

- **metGWAS 1.0** (Primary R workflow implementing network-driven over-representation analysis via hypergeometric testing and p-value adjustment) — https://github.com/saifurbd28/metGWAS-1.0
- **KEGG** (Source database for mapping disease-associated metabolites to interacting proteins/genes)
- **HMDB** (Reference database for discoverable genes associated with known metabolites)
- **GWAS Catalog** (Network representation source comprising 100s of compiled GWAS studies for variant-to-gene mapping)

## Examples

```
source('metGWAS 1.0_19 April.R'); results <- runMetGWAS(metabolomic_gwas_table, metagenome_gwas_table, p_threshold=0.05, correction_method='BH')
```

## Evaluation signals

- Enriched genes appear in both the metabolite-derived gene set (via KEGG/HMDB) and the GWAS-derived gene set (via network), confirming cross-study integration.
- Adjusted p-values (Benjamini–Hochberg corrected) are < 0.05 for top hits, indicating statistical significance after multiple-testing correction.
- Reproduction of known associations from paired metabolomics-GWAS studies (e.g., APOA5 in cardiovascular disease case study).
- Enriched pathway names (e.g., 'glycerophospholipid metabolism', 'kidney disease') are semantically coherent with the input study phenotypes.
- The number of enriched gene–pathway associations is non-zero and exceeds background expectation under the hypergeometric null model.

## Limitations

- Analysis is limited to genes with known metabolite interactions recorded in reference databases; novel or unmapped metabolite–protein pairs will not be detected.
- Relies on the quality and completeness of the GWAS Catalog network and metabolite–protein interaction databases; missing or outdated annotations reduce power.
- Unpaired design cannot directly prove causality; discovered associations may represent indirect or spurious co-enrichment.
- Marginal significance (P = 0.10–0.13) observed in case study 2 suggests modest effect sizes in some contexts; larger or more diverse GWAS datasets may be needed for kidney disease and other phenotypes.

## Evidence

- [other] metGWAS 1.0 is an R workflow designed to perform network-driven over-representation analysis that integrates and links results from independent metabolomic and meta-genome wide association studies.: "metGWAS 1.0 is an R workflow designed to perform network-driven over-representation analysis that integrates and links results from independent metabolomic and meta-genome wide association studies."
- [readme] We developed a bioinformatics tool, metGWAS 1.0, that generates and statistically compares metabolic and genomic gene sets using a hypergeometric test.: "We developed a bioinformatics tool, metGWAS 1.0, that generates and statistically compares metabolic and genomic gene sets using a hypergeometric test."
- [readme] Metabolic gene sets are generated by mapping disease-associated metabolites to interacting proteins (genes) via online databases.: "Metabolic gene sets are generated by mapping disease-associated metabolites to interacting proteins (genes) via online databases."
- [readme] Genomic gene sets are identified from a network representation of the GWAS Catalog comprising 100s of studies.: "Genomic gene sets are identified from a network representation of the GWAS Catalog comprising 100s of studies."
- [other] Filter associations by significance threshold (typically p < 0.05 or user-specified cutoff).: "Filter associations by significance threshold (typically p < 0.05 or user-specified cutoff)."
- [other] Adjust p-values for multiple testing (e.g., Benjamini–Hochberg correction) and rank enriched features by significance.: "Adjust p-values for multiple testing (e.g., Benjamini–Hochberg correction) and rank enriched features by significance."
- [readme] Although such an analysis is limited to genes with known metabolite interactions due to the unpaired nature of the data sets, any discovered associations may represent biomarkers and druggable targets for treatment and prevention.: "Although such an analysis is limited to genes with known metabolite interactions due to the unpaired nature of the data sets, any discovered associations may represent biomarkers and druggable"
