---
name: enrichment-score-computation
description: Use when after you have normalized metabolite abundances across samples
  and mapped metabolites to pathway or ontology identifiers. Use it when your goal
  is to identify statistically significant metabolite pathways or classes rather than
  analyze individual metabolite abundance changes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - Python (pandas, NumPy, SciPy)
  - Statistical analysis libraries (scipy.stats for enrichment tests)
  - MetENP
  - KEGGREST
  - pathview
  - SciPy (scipy.stats)
  license_tier: open
derived_from:
- doi: 10.1101/2020.11.20.391912
  title: MetENP
evidence_spans:
- MetENP
- enrichment statistics
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metenp_cq
    doi: 10.1101/2020.11.20.391912
    title: MetENP
  dedup_kept_from: coll_metenp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.11.20.391912
  all_source_dois:
  - 10.1101/2020.11.20.391912
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# enrichment-score-computation

## Summary

Compute statistical enrichment scores for metabolite pathways or metabolite classes from normalized abundance tables using tests like Fisher's exact, hypergeometric, or rank-based methods, followed by multiple-testing correction. This identifies which metabolite pathways or classes are significantly over- or under-represented in the dataset.

## When to use

Apply this skill after you have normalized metabolite abundances across samples and mapped metabolites to pathway or ontology identifiers. Use it when your goal is to identify statistically significant metabolite pathways or classes rather than analyze individual metabolite abundance changes. Trigger: you have a metabolite-to-pathway mapping and a question about which pathways show coordinated enrichment.

## When NOT to use

- Input metabolites are not yet mapped to pathways or ontologies — perform metabolite mapping first.
- Metabolite abundances have not been normalized — raw counts or non-comparable units across samples will inflate false positives.
- Goal is to identify individual significantly changed metabolites, not pathway-level patterns — use differential abundance testing instead.

## Inputs

- Normalized metabolite abundance table (rows=metabolites, columns=samples) in Metabolomics Workbench format or similar tabular format
- Metabolite-to-pathway cross-reference database or ontology mapping
- Metabolite identifiers (e.g., RefMet IDs, KEGG compound IDs)

## Outputs

- Enrichment results table with pathway identifiers, enrichment scores, p-values, and adjusted p-values (q-values)
- List of significantly enriched pathways (filtered by adjusted p-value threshold, e.g., q < 0.05)

## How to apply

First, normalize metabolite abundances using log-transformation or quantile normalization to account for inter-sample differences. Next, map each metabolite in your table to one or more pathway or class identifiers using a metabolite-to-pathway cross-reference database. Then, select an appropriate statistical test: Fisher's exact test or hypergeometric test for binary presence/absence data, or rank-based enrichment scores for continuous abundance data. Compute the test statistic and raw p-value for each pathway. Finally, apply multiple-testing correction (e.g., Benjamini–Hochberg) to control false discovery rate across all pathways tested. Output should include pathway identifiers, raw enrichment scores, unadjusted p-values, and adjusted p-values (e.g., q-values).

## Related tools

- **MetENP** (R package that implements metabolite enrichment analysis, pathway mapping, and enrichment score computation for metabolomics data) — https://github.com/metabolomicsworkbench/MetENP
- **KEGGREST** (Bioconductor R package for querying KEGG pathway and compound databases to retrieve metabolite-to-pathway mappings)
- **pathview** (Bioconductor R package for visualization of metabolite enrichment scores on KEGG pathway diagrams)
- **SciPy (scipy.stats)** (Python statistical library providing Fisher's exact test, hypergeometric test, and other enrichment test implementations)

## Evaluation signals

- Enrichment scores are computed for every pathway in the cross-reference database without missing values or errors.
- P-values and adjusted p-values (q-values) are monotonically ordered: raw p-values ≤ 1.0 and adjusted p-values ≥ raw p-values for each pathway.
- Multiple-testing correction reduces the number of significant pathways compared to uncorrected p-values (e.g., Benjamini–Hochberg should yield q-values ≥ corresponding raw p-values).
- Pathway rankings by enrichment score are consistent with biological expectations (e.g., pathways involving abundant metabolites rank higher than those with rare metabolites).
- Re-running the same analysis on the same normalized input reproduces identical enrichment scores and p-values (deterministic output).

## Limitations

- Enrichment scores depend critically on the completeness and accuracy of the metabolite-to-pathway database; unmapped metabolites are excluded from analysis.
- Statistical power is low when the number of significantly changed metabolites is small relative to the total metabolite pool.
- Rank-based enrichment methods assume a monotonic relationship between metabolite abundance and pathway relevance, which may not hold for complex regulatory networks.
- Multiple-testing correction becomes conservative when testing many pathways, increasing the risk of false negatives.
- Enrichment scores computed from normalized abundances may not reflect true biological changes if normalization method introduces bias (e.g., log-transformation of near-zero values).

## Evidence

- [other] Compute enrichment statistics (e.g., Fisher's exact test, hypergeometric test, or rank-based enrichment score) for each pathway.: "Compute enrichment statistics (e.g., Fisher's exact test, hypergeometric test, or rank-based enrichment score) for each pathway."
- [other] Calculate adjusted p-values using multiple-testing correction (e.g., Benjamini–Hochberg).: "Calculate adjusted p-values using multiple-testing correction (e.g., Benjamini–Hochberg)."
- [other] Normalize metabolite abundances across samples using appropriate scaling (e.g., log-transformation or quantile normalization).: "Normalize metabolite abundances across samples using appropriate scaling (e.g., log-transformation or quantile normalization)."
- [other] Map metabolites to pathway/ontology identifiers using metabolite-to-pathway cross-reference database.: "Map metabolites to pathway/ontology identifiers using metabolite-to-pathway cross-reference database."
- [readme] Enrichment score of metabolite class, Maps to pathway of the species of choice, Calculate enrichment score of pathways: "Enrichment score of metabolite class, Maps to pathway of the species of choice, Calculate enrichment score of pathways"
