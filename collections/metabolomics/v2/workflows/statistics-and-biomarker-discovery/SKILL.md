---
name: statistics-biomarker-discovery-workflow
description: 'Use when you have a metabolomics feature/quant table and want a statistically
  rigorous comparison and candidate biomarkers — cleaning and normalization, multivariate
  analysis, differential features, enrichment/pathway analysis, and biomarker selection
  with ROC.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - LC-MS
  stage_count: 5
  member_skills:
  - metabolite-feature-normalization-across-batches
  - metabolite-feature-intensity-normalization
  - metabolomics-feature-transformation
  - metabolomics-data-normalization
  - metabolite-feature-matrix-manipulation
  - multivariate-statistical-analysis-metabolomics
  - multivariate-ordination-analysis
  - metabolomics-feature-selection-significance-filtering
  - multivariate-ordination-analysis-nmds-pca
  - principal-component-analysis-for-metabolomics
  - metabolite-feature-anova-analysis
  - fold-change-calculation
  - multiple-testing-correction-and-p-value-adjustment
  - fold-change-calculation-metabolomics
  - fold-change-calculation-across-groups
  - metabolite-set-enrichment-analysis
  - metabolite-kegg-pathway-enrichment
  - untargeted-metabolomics-feature-analysis
  - metabolic-network-mapping
  - pathway-metabolite-mapping-integration
  - feature-importance-ranking
  - model-performance-evaluation-roc-curves
  - variable-importance-ranking-and-interpretation
  - random-forest-classification-for-metabolite-prediction
  - metabolomic-biomarker-pathway-association
  member_tools:
  - R
  - Jupyter Notebook
  - Google Colab
  - FBMN-STATS web app
  - MZmine3
  - margheRita
  - MS-DIAL
  - fgsea
  - readr
  - readxl
  - KEGG
  - enrichmet
  - KEGGREST
  - igraph
  - MeTEor
  coverage_gaps: []
  derived_from_workflows: []
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# Metabolomics Statistics and Biomarker Discovery

## Summary

End-to-end metabolomics statistics: from a raw feature table to normalized data, multivariate structure, differential features, pathway context, and ranked biomarkers.


## When to use

Use when you have a metabolomics feature/quant table and want a statistically rigorous comparison and candidate biomarkers — cleaning and normalization, multivariate analysis, differential features, enrichment/pathway analysis, and biomarker selection with ROC.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — clean_normalize

**Goal:** clean + normalize the feature table

**EDAM operation:** operation_3435

**Inputs:** feature-table · **Outputs:** feature-table

**Candidate leaf skills:** `metabolite-feature-normalization-across-batches` (primary), `metabolite-feature-intensity-normalization`, `metabolomics-feature-transformation`, `metabolomics-data-normalization`, `metabolite-feature-matrix-manipulation`

**Tools (primary):** R, Jupyter Notebook, Google Colab, FBMN-STATS web app

**Other candidate tools:** R ≥4.1.2, OUKS (Omics Untargeted Key Script), MAI package, MetCorR, GetFeatistics, ggplot2, XCMS, MS-Dial, dbnorm, sva, ber, pcaMethods, limma, impute, BiocParallel, Biobase, mixOmics, statTarget, MInfer, MetaboAnalyst, NormalizeMets, RStudio, NormQcmets, LogTransform, MissingValues, RlaPlots, PcaPlots

**Grounding:** 7 KB(s); DOIs: 10.1007/s11306-018-1347-7, 10.1007/s12561-013-9081-1, 10.1016/j.cmpb.2025.108672, 10.1021/acs.jproteome.1c00392 …

### Stage 2 — multivariate

**Goal:** multivariate analysis (PCA / PLS-DA / OPLS-DA, VIP)

**EDAM operation:** operation_3659

**Inputs:** feature-table · **Outputs:** tsv

**Candidate leaf skills:** `multivariate-statistical-analysis-metabolomics` (primary), `multivariate-ordination-analysis`, `metabolomics-feature-selection-significance-filtering`, `multivariate-ordination-analysis-nmds-pca`, `principal-component-analysis-for-metabolomics`

**Tools (primary):** R, Jupyter Notebook, Google Colab, MZmine3

**Other candidate tools:** vegan, MetaboDirect, R prcomp, ggplot2 (R), Python, mbpls, pandas, numpy, scikit-learn, matplotlib, MAMSI, MamsiStructSearch, Python 3.8, R 4.0.2, seaborn, SYNCSA, ggpubr, factoextra, ggplot2, metaboprep

**Grounding:** 5 KB(s); DOIs: 10.1021/acs.analchem.5c01327, 10.1038/s41596-024-01046-3, 10.1093/bioinformatics/btac059/6522114, 10.1186/s40168-023-01476-3 …

### Stage 3 — differential

**Goal:** differential feature analysis (univariate, volcano, FDR)

**EDAM operation:** operation_3659

**Inputs:** feature-table · **Outputs:** tsv

**Candidate leaf skills:** `metabolite-feature-anova-analysis` (primary), `fold-change-calculation`, `multiple-testing-correction-and-p-value-adjustment`, `fold-change-calculation-metabolomics`, `fold-change-calculation-across-groups`

**Tools (primary):** margheRita, R, MS-DIAL

**Other candidate tools:** Python (pandas, NumPy, SciPy), R (base stats, tidyverse, or similar), pandas, NumPy, SciPy, edgeR.R, DESeq2, RankProd, ggplot2, ComplexHeatmap, edgeR, RankProduct, LargeMetabo, pytest, fermo_core

**Grounding:** 6 KB(s); DOIs: 10.1021/acs.analchem.4c05039, 10.1038/s41467-024-50111-8, 10.1093/bib/bbac455, 10.1093/bioadv/vbae175 …

### Stage 4 — enrichment_pathway

**Goal:** enrichment + pathway / functional analysis

**EDAM operation:** operation_3928

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `metabolite-set-enrichment-analysis` (primary), `metabolite-kegg-pathway-enrichment`, `untargeted-metabolomics-feature-analysis`, `metabolic-network-mapping`, `pathway-metabolite-mapping-integration`

**Tools (primary):** R, fgsea, readr, readxl, KEGG, enrichmet, KEGGREST, igraph

**Other candidate tools:** ggplot2, KEGG_Enrich_PlotPanel, Enrichment, KEGG_Enrich_Plot, Mummichog 3, metDataModel, JMS, mass2chem

**Grounding:** 3 KB(s); DOIs: 10.1093/bib/bbac455, 10.1101/2025.08.28.672951v2, 10.1371/journal.pcbi.1003123

### Stage 5 — biomarker

**Goal:** biomarker selection + ROC / importance

**EDAM operation:** operation_3659

**Inputs:** tsv, tsv · **Outputs:** tsv

**Candidate leaf skills:** `feature-importance-ranking` (primary), `model-performance-evaluation-roc-curves`, `variable-importance-ranking-and-interpretation`, `random-forest-classification-for-metabolite-prediction`, `metabolomic-biomarker-pathway-association`

**Tools (primary):** MeTEor, R

**Other candidate tools:** randomForest, ggplot2, Omu, read.metabo, igraph, KEGG_Enrich_PlotPanel, Enrichment, KEGG_Enrich_Plot

**Grounding:** 4 KB(s); DOIs: 10.1007/978-3-319-47656-8_6, 10.1093/bib/bbac455, 10.1093/bioadv/vbae178, 10.1128/mra.00129-19

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding + EDAM-aware primary selection). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
