---
name: metabolite-abundance-normalization
description: Use when after loading a raw metabolite abundance table (rows=metabolites, columns=samples) from Metabolomics Workbench format and before mapping metabolites to pathway identifiers or computing enrichment statistics.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - Python (pandas, NumPy, SciPy)
  - pandas
  - NumPy
  - SciPy
  - MetENP
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1101/2020.11.20.391912
  title: MetENP
evidence_spans:
- MetENP
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-abundance-normalization

## Summary

Normalize metabolite abundances across samples using scaling methods (log-transformation or quantile normalization) to prepare a Metabolomics Workbench format abundance table for downstream enrichment analysis. Normalization removes systematic technical variation and ensures fair comparison of metabolite signals across samples.

## When to use

After loading a raw metabolite abundance table (rows=metabolites, columns=samples) from Metabolomics Workbench format and before mapping metabolites to pathway identifiers or computing enrichment statistics. Use this skill when metabolite signals exhibit wide dynamic range, sample-level batch effects, or skewed abundance distributions that could bias pathway enrichment.

## When NOT to use

- Input is already a pre-normalized feature table or abundance matrix from another preprocessing pipeline (e.g., from XCMS or MZmine output that already includes normalization).
- Abundance data are already on a log-scale or have been rarefied (relative abundance) and further transformation would distort compositional structure.
- Analysis requires preservation of absolute metabolite concentrations (e.g., for external validation against mass spectrometry calibration curves); normalization may obscure absolute quantification.

## Inputs

- raw metabolite abundance table (rows=metabolites, columns=samples) in Metabolomics Workbench format
- metadata indicating sample groupings or batch labels (optional, for identifying systematic effects)

## Outputs

- normalized metabolite abundance matrix (same dimensions, scaled abundances)
- normalization parameters/factors (for reproducibility and downstream visualization)
- diagnostic plots (e.g., boxplot of log-abundances per sample, quantile-quantile plots)

## How to apply

Load the raw metabolite abundance matrix from Metabolomics Workbench format into a data structure (e.g., pandas DataFrame). Apply one of two normalization strategies: (1) log-transformation (e.g., log2 or natural log after pseudocount addition) to stabilize variance and compress dynamic range, or (2) quantile normalization to align the empirical distribution of metabolite abundances across all samples. The choice depends on data characteristics—log-transformation is recommended for skewed, right-tailed distributions; quantile normalization works well when systematic sample-level shifts dominate. After normalization, verify that metabolite abundances are on a comparable scale across samples (e.g., check that median and variance are similar per sample) before proceeding to metabolite-to-pathway mapping and enrichment scoring.

## Related tools

- **pandas** (In-memory data frame manipulation and transformation (load, subset, apply row/column-wise scaling operations))
- **NumPy** (Vectorized numerical operations for log-transformation, normalization scaling, and statistical summaries)
- **SciPy** (Statistical functions including quantile normalization and rank-based transformations via scipy.stats)
- **MetENP** (R package implementing the full enrichment pipeline including metabolite loading, normalization, and pathway mapping) — https://github.com/metabolomicsworkbench/MetENP

## Evaluation signals

- Post-normalization abundance distributions are approximately symmetric or have reduced right-skew compared to raw data (inspect via histogram or Q-Q plot per metabolite class).
- Sample-level median abundances and variance are visually similar across samples after normalization (boxplot of normalized abundances shows comparable interquartile ranges).
- No metabolites become zero or negative after normalization; all values remain in valid abundance space for downstream enrichment tests.
- Downstream enrichment scores and p-values are reproducible when the same normalization method is reapplied to the same input table.
- Metabolite rank-ordering (most to least abundant) within each sample is consistent before and after normalization (Spearman correlation of raw vs. normalized ranks ≥ 0.95 per sample).

## Limitations

- Log-transformation requires a pseudocount (e.g., 1 or the minimum non-zero abundance) to handle zero abundances; choice of pseudocount can subtly affect results for very low-abundance metabolites.
- Quantile normalization assumes that the majority of metabolites are not truly differentially abundant; if a large proportion of metabolites are genuinely changed between groups, quantile normalization may overcorrect and mask real biological signal.
- Normalization does not account for metabolite-specific batch effects (e.g., ion suppression in mass spectrometry); if such effects are strong and systematically associated with sample groups, enrichment results may be confounded.
- The README notes that MetENP requires installation of multiple Bioconductor dependencies (KEGGREST, KEGGgraph, pathview) and optional R packages (plyr, dplyr, tidyr, ggplot2, etc.); environment setup can be error-prone.

## Evidence

- [other] Normalize metabolite abundances across samples using appropriate scaling (e.g., log-transformation or quantile normalization).: "Normalize metabolite abundances across samples using appropriate scaling (e.g., log-transformation or quantile normalization)."
- [other] Load metabolite abundance table from Metabolomics Workbench format (rows=metabolites, columns=samples).: "Load metabolite abundance table from Metabolomics Workbench format (rows=metabolites, columns=samples)."
- [other] MetENP performs metabolite enrichment analysis to identify enriched pathways from metabolomics data.: "MetENP performs metabolite enrichment analysis to identify enriched pathways from metabolomics data."
- [other] Python (pandas, NumPy, SciPy), Statistical analysis libraries (scipy.stats for enrichment tests): "Python (pandas, NumPy, SciPy), Statistical analysis libraries (scipy.stats for enrichment tests)"
