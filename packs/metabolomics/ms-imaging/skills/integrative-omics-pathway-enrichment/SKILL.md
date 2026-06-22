---
name: integrative-omics-pathway-enrichment
description: Use when you have a preprocessed peak table with statistically significant or differentially abundant metabolites (e.g., from ANCOVA or PLS/PLS-DA), and you want to move beyond individual peak-level interpretation to understand which biological pathways or metabolic networks are perturbed.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3501
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - R
  - SMART
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1021/acs.analchem.5c03225
  title: SMART 2.0
evidence_spans:
- SMART written in R and R GUI has been developed as user-friendly software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_smart_2_0_cq
    doi: 10.1021/acs.analchem.5c03225
    title: SMART 2.0
  dedup_kept_from: coll_smart_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03225
  all_source_dois:
  - 10.1021/acs.analchem.5c03225
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# integrative-omics-pathway-enrichment

## Summary

Integrative Omics Pathway Analysis (IOPA) maps detected metabolomic peaks to metabolite identities and associates them with known biological pathways, then computes pathway enrichment scores and statistical significance to identify which metabolic pathways are most altered or dysregulated in the studied samples or phenotypes.

## When to use

Apply this skill when you have a preprocessed peak table with statistically significant or differentially abundant metabolites (e.g., from ANCOVA or PLS/PLS-DA), and you want to move beyond individual peak-level interpretation to understand which biological pathways or metabolic networks are perturbed. Use IOPA when the research question is: 'Which metabolic pathways are enriched or dysregulated in my samples?' rather than 'Which individual metabolites differ?'

## When NOT to use

- Input is already a pre-computed pathway enrichment result or gene/protein-level pathway analysis; do not re-run IOPA on pathway-level data.
- Peak identities are unknown or below metabolomics standards (MSI Level 3 or lower); IOPA requires confident metabolite assignment to map to pathways.
- No metabolite-to-pathway annotation resource is available for your organism, tissue, or metabolic context; enrichment will be uninformative or biased by database incompleteness.

## Inputs

- preprocessed peak table (feature matrix: samples × peaks with normalized intensities)
- peak metadata (m/z, retention time, peak identifiers)
- metabolite annotation table (peak-to-metabolite mappings, e.g., from database matching or MSI level 2 identifications)
- metabolite-pathway association database (KEGG IDs, pathway names, metabolite–pathway incidence matrix)
- sample phenotype or grouping information
- per-peak statistical results (p-values, effect sizes, or importance scores from prior ANCOVA/PLS-DA analysis)

## Outputs

- pathway enrichment results table (pathway identifiers, enrichment scores, p-values, adjusted p-values/FDR, number of significant metabolites per pathway)
- pathway ranking (sorted by significance or effect magnitude)
- pathway annotation summary (pathway name, description, member metabolites, their individual statistics)

## How to apply

First, map each significant peak (identified by m/z, retention time, or spectral database matching) to a metabolite identity using a reference library or in silico annotation tool. Second, obtain or construct a metabolite-to-pathway annotation database (e.g., KEGG, BioCyC, or similar) that associates each identified metabolite with one or more canonical or custom metabolic pathways. Third, for each pathway, aggregate the statistical evidence (e.g., effect sizes, p-values, or importance scores) from all metabolites assigned to that pathway. Fourth, compute pathway enrichment statistics—such as the proportion of pathway members that are significant, the mean effect size within the pathway, or a Fisher's exact test / hypergeometric test comparing observed vs. expected pathway hits—to yield a pathway-level p-value or enrichment score. Finally, apply multiple-testing correction (e.g., Benjamini-Hochberg FDR) across all tested pathways to control false discovery rate and rank pathways by statistical significance.

## Related tools

- **SMART** (R-based metabolomics analysis platform that implements the IOPA module; orchestrates peak annotation, metabolite mapping, and pathway enrichment computation within the integrated workflow) — github.com/YuJenL/SMART
- **R** (Programming environment in which IOPA is implemented; used to load peak tables, parse metabolite-pathway associations, compute enrichment statistics, and aggregate results)

## Evaluation signals

- Pathway results table contains no missing or NaN values in required columns (pathway identifier, enrichment score, p-value, adjusted p-value).
- All adjusted p-values are ≥ raw p-values; FDR correction is monotonically non-decreasing when pathways are sorted by raw p-value.
- Number of significant metabolites per pathway is consistent with the metabolite-pathway incidence matrix; spot-check a few pathways by manual counting.
- Pathways with more member metabolites in the annotation database and more significant hits rank higher (or lower, depending on the enrichment statistic), demonstrating sensitivity to effect magnitude and pathway size.
- Top-ranked pathways are biologically plausible given the study design and phenotype (e.g., lipid metabolism dysregulation in obesity studies, amino acid metabolism in liver disease).

## Limitations

- Pathway enrichment depends critically on the completeness and accuracy of the metabolite-pathway annotation database; missing metabolites or incorrect assignments will bias results.
- IOPA is sensitive to metabolite identification confidence; peaks annotated at MSI Level 3 or lower may introduce noise into pathway statistics.
- Overlapping pathway definitions (shared metabolites between pathways) can confound interpretation; no explicit deconvolution of metabolite pleiotropy is performed.
- Pathway-level p-values may be conservative or liberal depending on the enrichment method (e.g., Fisher's exact vs. hypergeometric vs. set-based methods); the choice of test is not always documented in the README.

## Evidence

- [other] IOPA maps peaks to metabolite identities, constructs metabolite-pathway associations, and computes pathway enrichment scores and significance: "For IOPA: map peaks to metabolite identities, construct metabolite-pathway associations, and compute pathway enrichment scores and significance."
- [readme] IOPA is one of three statistical analysis methods offered by SMART: "Statistical Analysis: Perform association analysis (ANCOVA), classification analysis (PLS/PLS-DA), and integrative omics pathway analysis (IOPA)"
- [readme] SMART streamlines the complete analysis flow from preprocessing to advanced downstream analysis, including IOPA as a post-statistical module: "SMART streamlines the complete analysis flow from initial data preprocessing to advanced downstream data analysis"
- [other] Results are aggregated into a single table with peak identifiers and test-specific metrics: "Aggregate results (p-values, effect sizes, importance scores, or pathway statistics) into a single results table with peak identifiers and test-specific metrics."
