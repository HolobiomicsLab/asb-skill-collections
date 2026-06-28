---
name: pathway-functional-analysis-workflow
description: 'Use when you have an LC-MS metabolomics feature list (m/z, optionally
  p-values/fold changes) and want biological interpretation without prior identification
  — feature preparation, mummichog functional analysis from m/z, pathway/enrichment
  analysis, and pathway-level interpretation.

  '
license: CC-BY-4.0
metadata:
  kind: composite-workflow
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  techniques:
  - LC-MS
  stage_count: 4
  member_skills:
  - untargeted-metabolomics-feature-analysis
  - metabolomics-data-quality-assessment
  - metabolite-feature-column-mapping
  - metabolomic-feature-table-assembly
  - metabolic-network-mapping
  - pathway-activity-propagation-inference
  - functional-module-inference-from-networks
  - network-based-functional-prediction
  - mass-feature-to-node-mapping
  - metabolite-set-enrichment-analysis
  - pathway-metabolite-mapping-integration
  - metabolic-pathway-database-querying
  - metabolite-set-analysis
  - metabolite-kegg-pathway-enrichment
  - pathway-enrichment-visualization
  - enrichment-score-computation
  - metabolomic-biomarker-pathway-association
  member_tools:
  - Mummichog 3
  - metDataModel
  - JMS
  - mass2chem
  - MetaboAnalystR
  - R
  - metabCombiner
  - JPA
  - XCMS
  - MS-Convert
  - Python
  - mummichog (v3)
  - mummichog
  - fgsea
  - readr
  - readxl
  - KEGG
  - enrichmet
  - KEGGREST
  - igraph
  - clusterProfiler
  - margheRita
  - ComplexHeatmap
  - PALS (Pathway Activity Level Scoring)
  - PALS Viewer
  - ORA (Over-Representation Analysis)
  - GSEA (Gene Set Enrichment Analysis)
  - GNPS (Global Natural Products Social Molecular Networking)
  - MS2LDA
  - ggplot2
  - KEGG_Enrich_PlotPanel
  - Enrichment
  - KEGG_Enrich_Plot
  - Python (pandas, NumPy, SciPy)
  - Statistical analysis libraries (scipy.stats for enrichment tests)
  - MetENP
  - pathview
  - SciPy (scipy.stats)
  derived_from_workflows: []
  bound_by: perspicacite-semantic
schema_version: 0.3.0
attribution:
  generator: AgenticScienceBuilder
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
  zenodo_doi: 10.5281/zenodo.20794027
---

# Pathway & Functional Analysis (m/z to Biology)

## Summary

End-to-end functional analysis: turn a ranked m/z feature list into predicted pathway activity and enriched metabolite sets, even without confident structure annotations.


## When to use

Use when you have an LC-MS metabolomics feature list (m/z, optionally p-values/fold changes) and want biological interpretation without prior identification — feature preparation, mummichog functional analysis from m/z, pathway/enrichment analysis, and pathway-level interpretation.


## When NOT to use

- The data is not LC-MS.
- You need a single atomic step, not the full pipeline (use the leaf skill directly via the router).

## Stages

### Stage 1 — feature_prep

**Goal:** prepare a ranked m/z feature list for functional analysis

**EDAM operation:** operation_3435

**Inputs:** feature-table · **Outputs:** tsv

**Candidate leaf skills:** `untargeted-metabolomics-feature-analysis` (primary), `metabolomics-data-quality-assessment`, `metabolite-feature-column-mapping`, `metabolomic-feature-table-assembly`

**Tools:** Mummichog 3, metDataModel, JMS, mass2chem, MetaboAnalystR, R, metabCombiner, JPA, XCMS, MS-Convert

**Grounding:** 4 KB(s); DOIs: 10.1021/acs.analchem.0c03693, 10.1038/s41467-024-48009-6, 10.1371/journal.pcbi.1003123, 10.3390/metabo12030212

### Stage 2 — mummichog

**Goal:** functional analysis directly from m/z (mummichog)

**EDAM operation:** operation_3928

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `metabolic-network-mapping` (primary), `pathway-activity-propagation-inference`, `functional-module-inference-from-networks`, `network-based-functional-prediction`, `mass-feature-to-node-mapping`

**Tools:** Mummichog 3, metDataModel, JMS, mass2chem, Python, mummichog (v3), mummichog

**Grounding:** 1 KB(s); DOIs: 10.1371/journal.pcbi.1003123

### Stage 3 — pathway_enrichment

**Goal:** pathway + metabolite-set enrichment

**EDAM operation:** operation_3928

**Inputs:** tsv · **Outputs:** tsv

**Candidate leaf skills:** `metabolite-set-enrichment-analysis` (primary), `pathway-metabolite-mapping-integration`, `metabolic-pathway-database-querying`, `metabolite-set-analysis`, `metabolite-kegg-pathway-enrichment`

**Tools:** R, fgsea, readr, readxl, KEGG, enrichmet, KEGGREST, igraph, clusterProfiler, margheRita, ComplexHeatmap, PALS (Pathway Activity Level Scoring), PALS Viewer, ORA (Over-Representation Analysis), GSEA (Gene Set Enrichment Analysis), GNPS (Global Natural Products Social Molecular Networking), MS2LDA, ggplot2, KEGG_Enrich_PlotPanel, Enrichment, KEGG_Enrich_Plot

**Grounding:** 6 KB(s); DOIs: 10.1093/bib/bbac455, 10.1101/2024.06.20.599545, 10.1101/2024.06.20.599545v1, 10.1101/2025.08.28.672951v2 …

### Stage 4 — interpretation

**Goal:** interpret + visualize enriched pathways

**EDAM operation:** operation_3659

**Inputs:** tsv, tsv · **Outputs:** tsv

**Candidate leaf skills:** `pathway-enrichment-visualization` (primary), `enrichment-score-computation`, `metabolomic-biomarker-pathway-association`

**Tools:** clusterProfiler, margheRita, R, ComplexHeatmap, Python (pandas, NumPy, SciPy), Statistical analysis libraries (scipy.stats for enrichment tests), MetENP, KEGGREST, pathview, SciPy (scipy.stats), ggplot2, igraph, KEGG_Enrich_PlotPanel, Enrichment, KEGG_Enrich_Plot

**Grounding:** 4 KB(s); DOIs: 10.1093/bib/bbac455, 10.1101/2020.11.20.391912, 10.1101/2024.06.20.599545, 10.1101/2024.06.20.599545v1

## Grounding

Each stage carries the `kb_slugs`/`dois` of the leaves it draws on. Ground any stage against its source paper with the collection's `/ground` command or `bin/perspicacite_kb_bind.py` (Perspicacité KB; serverless local-clone fallback).

## Verification contract

`workflow.yaml` is gradable by `asb solve-workflow` (checkpoint mode). Each stage declares typed outputs; the final stage emits the master deliverable.

## Provenance

Generated by `compose_workflows.py` (semantic binding). `derived_from_workflows` lists ASB per-paper workflows whose structure corroborated this pipeline — these are the eval-ablation set (SPEC §8). Staging only; promote via `release_gate.py`.
