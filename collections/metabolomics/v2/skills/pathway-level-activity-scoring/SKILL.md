---
name: pathway-level-activity-scoring
description: Use when you have a metabolite intensity matrix (samples × metabolites) with assigned annotations (peak IDs mapped to KEGG or ChEBI compound IDs), a metabolic pathway database, and need to rank pathways by activity level within experimental groups or comparisons.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0203
  tools:
  - PALS (Pathway Activity Level Scoring)
  - PALS
  - PALS Viewer
  - GNPS
  - MS2LDA
derived_from:
- doi: 10.3390/metabo11020103
  title: pals
- doi: 10.1186/1471-2105-6-225
  title: ''
evidence_spans:
- we introduce **PALS (Pathway Activity Level Scoring)**, a complete tool that performs database queries of pathways, decomposes activity levels in pathways
- we introduce PALS (Pathway Activity Level Scoring), a complete tool that performs database queries of pathways, decomposes activity levels in pathways
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pals
    doi: 10.3390/metabo11020103
    title: pals
  dedup_kept_from: coll_pals
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo11020103
  all_source_dois:
  - 10.3390/metabo11020103
  - 10.1186/1471-2105-6-225
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Pathway-Level Activity Scoring via PLAGE Decomposition

## Summary

Decompose a metabolite intensity matrix into quantitative pathway activity scores using singular value decomposition (SVD), enabling robust ranking of metabolic pathways without losing information through dichotomous thresholding. This approach is more resilient to noise and missing peaks than over-representation analysis (ORA) or gene set enrichment analysis (GSEA).

## When to use

You have a metabolite intensity matrix (samples × metabolites) with assigned annotations (peak IDs mapped to KEGG or ChEBI compound IDs), a metabolic pathway database, and need to rank pathways by activity level within experimental groups or comparisons. Use this when peaks exhibit high noise or sparse coverage, as PLAGE preserves quantitative intensity information rather than binarizing presence/absence.

## When NOT to use

- Input data is already a pre-computed feature or pathway activity table, not raw peak intensities.
- Pathway database is unavailable or metabolites cannot be reliably mapped to compound identifiers.
- Analysis goal is to identify significantly perturbed individual metabolites rather than pathway-level trends.

## Inputs

- Metabolite intensity matrix (CSV: rows=peak IDs, columns=sample names, values=peak intensities; optional second row with group assignments)
- Annotation matrix (CSV: peak ID → KEGG/ChEBI compound ID mappings, supporting many-to-many relationships)
- Pathway database (pathway definitions as metabolite sets; e.g., KEGG pathways from PiMP, Reactome COMPOUND/ChEBI/UniProt/ENSEMBL)
- Experimental design specification (sample grouping and case/control comparisons)

## Outputs

- Pathway ranking table (pathway ID, activity score per comparison, p-value, coverage metrics)
- Unique formulae count per pathway (unq_pw_F), dataset formula hits (tot_ds_F), coverage fraction (F_coverage)

## How to apply

For each pathway in the database, extract the subset of metabolites assigned to that pathway from your intensity matrix. Apply singular value decomposition (SVD) to this subset and extract the first principal component (singular vector) as the pathway activity score. Log₂-transform intensities and standardize to zero mean and unit variance across samples before decomposition. Compute statistical significance (p-values) for each pathway activity score and rank pathways by magnitude. The method handles multiple peak-to-metabolite mappings and performs data imputation: if all samples in a factor have zero intensity, replace with user-specified minimum (default 5000); if some samples are zero, replace with factor mean. Results are more robust when applied to metabolomics data with prevalent noise and missing peaks.

## Related tools

- **PALS** (Command-line tool and Python library implementing PLAGE decomposition, ORA, and GSEA for pathway activity scoring; performs database queries, data imputation, preprocessing, and result ranking) — https://github.com/glasgowcompbio/PALS
- **PALS Viewer** (Web-based graphical interface (Streamlit) for running PALS, visualizing pathway rankings, and inspecting significantly changing pathways) — https://pals.glasgowcompbio.org/app/
- **GNPS** (Provides molecular family (MF) annotations that can be grouped and analyzed alongside metabolic pathways in PALS) — http://gnps.ucsd.edu/
- **MS2LDA** (Provides mass-to-motif annotations that can be grouped and analyzed alongside metabolic pathways in PALS) — http://ms2lda.org/

## Examples

```
python pals/run.py PLAGE notebooks/test_data/HAT/int_df.csv notebooks/test_data/HAT/annotation_df.csv test_output.csv --db PiMP_KEGG --comparisons Stage_1/Control Stage_2/Control
```

## Evaluation signals

- Pathway activity scores are continuous (not binary) and span a range consistent with the normalized intensity distribution.
- P-values are reported for each pathway and adjust for multiple comparisons; pathways with low coverage (F_coverage near 0) are distinguishable.
- Results are reproducible: same input data and parameters produce identical rankings across runs.
- Robustness check: rerun with increased noise or synthetic missing peaks; rankings remain stable and more consistent than ORA/GSEA results.
- Output coverage metrics (unq_pw_F, tot_ds_F, F_coverage) indicate data-pathway overlap; pathways with <2 matched metabolites are flagged or filtered.

## Limitations

- Method requires reliable metabolite-to-compound mappings; ambiguous or missing annotations reduce pathway coverage and power.
- SVD-based scoring assumes linear principal component structure; nonlinear pathway interactions are not captured.
- Data imputation strategy (minimum or mean replacement) is crude and may introduce bias if missingness is non-random.
- Pathway database selection (KEGG vs. Reactome, metabolic-only vs. all pathways, species-specific) significantly affects results; online (Neo4j) vs. offline mode affects pathway freshness.
- Method is designed for metabolomics; extension to proteomics/transcriptomics requires compound ID replacement (UniProt, ENSEMBL) and has not been validated in the cited work.

## Evidence

- [other] For each pathway, apply PLAGE (Pathway Level Analysis of Gene Expression) decomposition via singular value decomposition (SVD) on the subset of metabolites assigned to that pathway. Extract the first principal component (singular vector) from each pathway's SVD as the pathway activity score.: "For each pathway, apply PLAGE (Pathway Level Analysis of Gene Expression) decomposition via singular value decomposition (SVD) on the subset of metabolites assigned to that pathway. Extract the first"
- [readme] The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA). This is particularly important for metabolomics peak data, where noise and missing peaks are prevalent.: "The results are found to be more robust to noise and missing peaks compared to the alternatives (ORA, GSEA)"
- [readme] Data imputation is performed to the intensity matrix when it is loaded: if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value (which can be set by the user); and if only some of the sample values in a factor are zero then these are replaced by the mean value of the non-zero samples in that factor.: "if all of the samples in a single experimental factor have intensities of zero these are replaced by the minimum intensity value"
- [readme] The data is subsequently transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance across the samples.: "transformed to log-2 base and standardised using the preprocessing module in Scipy such that the intensity matrix has a zero mean and unit variance"
- [readme] the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways: "the decomposition approach in PALS is amenable to the analysis of any group of metabolite sets, not just pathways"
- [readme] Pathways are identified by their id and can be sorted by the `p-value` columns. The column `unq_pw_F` lists the unique formulae found in that pathway, `tot_ds_F` lists the formula hits found in the dataset, and `F_coverage` is the proportion of `tot_ds_F` to `unq_pw_F`.: "The column `unq_pw_F` lists the unique formulae found in that pathway, `tot_ds_F` lists the formula hits found in the dataset, and `F_coverage` is the proportion"
