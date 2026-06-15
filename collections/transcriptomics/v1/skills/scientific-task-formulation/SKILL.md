---
name: scientific-task-formulation
description: Use when you encounter a published scientific article or software paper that makes claims about data processing, analysis, or results, but the reproducibility context is unclear, artifacts are scattered, or the connection between claims and outputs is not immediately evident.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0597
  tools:
  - GitHub
  - Seurat
  - WGCNA
derived_from:
- doi: 10.1186/s13059-019-1874-1
  title: sctransform
- doi: 10.1186/1471-2105-9-559
  title: ''
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_sctransform
    doi: 10.1186/s13059-019-1874-1
    title: sctransform
  - build: coll_wgcna
    doi: 10.1186/1471-2105-9-559
    title: wgcna
  dedup_kept_from: coll_sctransform
schema_version: 0.2.0
---

# scientific_task_formulation

## Summary

Formulate a well-scoped scientific task by identifying the research question, assessing reproducibility context, and connecting published claims to their computational and data artifacts. This skill ensures clarity of what is being studied, why, and what evidence supports the findings.

## When to use

Apply this skill when you encounter a published scientific article or software paper that makes claims about data processing, analysis, or results, but the reproducibility context is unclear, artifacts are scattered, or the connection between claims and outputs is not immediately evident. Use it as a front-end step before attempting to implement or validate a method.

## When NOT to use

- The article is purely theoretical and makes no computational or empirical claims.
- Source code or data repositories are explicitly unavailable (e.g., proprietary, withdrawn) and the article states this.
- The task has already been fully validated by expert implementation; use this skill only for initial scoping, not re-validation.

## Inputs

- article text (abstract, methods, discussion sections)
- repository README and documentation
- linked publications and supplementary materials
- GitHub repository structure and release history

## Outputs

- formalized research question
- inventory of reproducibility artifacts (present and missing)
- mapping of claims to computational outputs
- list of unresolved reproducibility gaps

## How to apply

Review the article abstract, methods, and discussion to extract the explicit research question and primary claim. Cross-reference the article with its source code repository (e.g., GitHub) to identify available computational artifacts (scripts, vignettes, examples). Inspect the README and linked publications for version history, installation instructions, and usage examples. Record what materials are present (e.g., code, vignettes, test data) and what are missing (e.g., changelog, raw input files, validation datasets). Use this inventory to assess whether the task is reproducible as stated and to identify gaps that future implementations must address.

## Related tools

- **GitHub** (Version control and artifact hosting for retrieving source code, vignettes, and release history) — https://github.com
- **Seurat** (Single-cell RNA-seq analysis framework that integrates sctransform functionality and demonstrates integration of methods into broader pipelines) — https://satijalab.org/seurat/

## Evaluation signals

- Research question is explicitly stated and falsifiable (not vague or rhetorical).
- All major claims in the article map to at least one computational output, vignette, or example in the repository.
- A checklist of reproducibility artifacts is complete: README, installation instructions, usage examples, linked publications, and version tags are identified.
- Missing signals (e.g., no changelog, no raw input data, no test data) are explicitly documented.
- Expert review confirms that the formulated task matches the article's intent and that reproducibility gaps are accurately identified.

## Limitations

- Heuristic detection of claims and findings may miss implicit or weakly stated hypotheses; expert review is needed to confirm findings.
- Absence of a changelog or formal version history does not necessarily mean the code is unreproducible; it may indicate incomplete documentation.
- Some articles link to supplementary materials on external sites that may become unavailable or change without warning.
- Integration of a method into a larger package (e.g., sctransform into Seurat) may obscure the original method's inputs and outputs if not carefully traced.

## Evidence

- [other] research_question: "Assess the scientific task and reproducibility context described by this article package."
- [other] workflow_steps: "Review indexed article artifacts, connect claims to outputs, inspect available materials, and record missing information."
- [readme] primary_method_reference: "Normalization and variance stabilization of single-cell RNA-seq data using regularized negative binomial regression"
- [readme] core_integration_claim: "Core functionality of this package has been integrated into Seurat, an R package designed for QC, analysis, and exploration of single cell RNA-seq data."
- [readme] usage_example: "Running sctransform on a UMI matrix: normalized_data <- sctransform::vst(umi_count_matrix)$y"
