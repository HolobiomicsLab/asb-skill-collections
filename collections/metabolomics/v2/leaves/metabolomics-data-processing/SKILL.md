---
name: metabolomics-data-processing
description: Use when when you have raw or partially processed metabolomics data (feature
  tables with sample metadata) and need to apply quality-control metrics, normalization,
  statistical inference, or advanced classification/variable selection without relying
  on a Galaxy instance.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3813
  tools:
  - Galaxy Genomics Framework
  - SECIMTools
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1186/s12859-018-2134-1
  title: SECIMTools
evidence_spans:
- can be run in a standalone mode or via Galaxy Genomics Framework
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_secimtools_cq
    doi: 10.1186/s12859-018-2134-1
    title: SECIMTools
  dedup_kept_from: coll_secimtools_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-018-2134-1
  all_source_dois:
  - 10.1186/s12859-018-2134-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-data-processing

## Summary

Execute SECIMTools metabolomics processing workflows in standalone mode to perform quality control, statistical analysis, and feature selection on mass spectrometry metabolomics data. This skill bridges standalone command-line invocation and Galaxy Genomics Framework integration for reproducible metabolomics pipelines.

## When to use

When you have raw or partially processed metabolomics data (feature tables with sample metadata) and need to apply quality-control metrics, normalization, statistical inference, or advanced classification/variable selection without relying on a Galaxy instance. Use this skill when reproducibility and portability across computational environments is required.

## When NOT to use

- Input data is already fully quality-controlled and normalized from another pipeline—apply only the specific downstream analysis tools you need.
- You require real-time interactive parameter tuning and visual feedback—Galaxy Genomics Framework or a Jupyter-based workflow may be more suitable.
- Your metabolomics data format is not compatible with SECIMTools input specifications (e.g., non-standard matrix layout, unsupported metadata encoding).

## Inputs

- metabolomics feature abundance table (CSV/TSV matrix: features × samples)
- sample metadata file (CSV/TSV: samples × covariates)
- raw mass spectrometry data (optional, depending on tool)
- tool-specific parameters and thresholds (via command-line arguments)

## Outputs

- processed feature table (normalized or filtered)
- quality-control metrics and diagnostic plots
- statistical results (p-values, effect sizes, model coefficients)
- variable selection results (ranked feature importance or sparse model)
- visualization artifacts (heatmaps, PCA plots, LDA plots, clustering dendrograms)

## How to apply

Obtain the SECIMTools repository and select a specific tool matching your analysis goal (e.g., retention time window evaluation, peak quality filtering, normalization, PCA, PLSDA, random forest, or LASSO variable selection). Prepare input metabolomics data in the format required by the chosen tool (typically a feature abundance matrix and sample metadata file). Invoke the tool via command-line with required arguments and parameters as documented in the tool's help text. Monitor output files for expected format and schema compliance. Validate that produced artifacts (e.g., normalized tables, model coefficients, visualizations) match the documented output specification and are suitable for downstream interpretation or publication.

## Related tools

- **SECIMTools** (Suite of quality-control, normalization, statistical analysis, classification, and variable selection tools for metabolomics data processing in standalone mode) — https://github.com/secimTools/SECIMTools
- **Galaxy Genomics Framework** (Alternative execution environment for SECIMTools workflows via graphical interface)

## Evaluation signals

- Output file exists at the expected location and path specified by the tool invocation.
- Output matrix has correct dimensions (features × samples or samples × features) and preserves sample/feature identifiers from input.
- Quality-control metrics (e.g., retention time window evaluation results, peak evaluation summaries) are present and contain non-empty results.
- Statistical results (p-values, coefficients) fall within expected numeric ranges (e.g., p ∈ [0, 1], coefficients finite and non-NaN).
- Visualization files (heatmaps, PCA/LDA plots, dendrograms) render without errors and display feature/sample labels correctly.

## Limitations

- SECIMTools requires pre-formatted input; data must be prepared into a feature table and metadata matrix before invocation.
- No changelog is available in the repository, limiting traceability of tool behavior changes between versions.
- Standalone mode may require manual dependency management (Python, libraries) on diverse computing environments; the pypi/bioconda packages may simplify this.
- Advanced features (e.g., custom scoring metrics, parallel execution) may be constrained compared to integrated Galaxy workflows.

## Evidence

- [readme] SECIMTools project aims to develop a suite of tools for processing of metabolomics data, which can be run in a standalone mode or via Galaxy Genomics Framework.: "SECIMTools project aims to develop a suite of tools for processing of metabolomics data, which can be run in a standalone mode or via Galaxy Genomics Framework."
- [readme] The suite includes a comprehensive set of quality control metrics (retention time window evaluation and various peak evaluation tools), visualization techniques (hierarchical cluster heatmap, principal component analysis, linear discriminant analysis, modular modularity clustering), basic statistical analysis methods (partial least squares - discriminant analysis, analysis of variance), advanced classification methods (random forest, support vector machines), and advanced variable selection tools (least absolute shrinkage and selection operator LASSO and Elastic Net).: "suite includes a comprehensive set of quality control metrics (retention time window evaluation and various peak evaluation tools), visualization techniques (hierarchical cluster heatmap, principal"
- [readme] SECIMTools are available as a secimtools pypi package. Project has also been packaged for bioconda and Galaxy Genomics Framework.: "SECIMTools are available as a secimtools pypi package. Project has also been packaged for bioconda and Galaxy Genomics Framework."
- [other] Prepare input metabolomics data in the format required by the chosen tool (e.g., feature table, sample metadata).: "Prepare input metabolomics data in the format required by the chosen tool (e.g., feature table, sample metadata)."
- [other] Execute the tool via command-line invocation in standalone mode, passing required arguments and parameters as documented.: "Execute the tool via command-line invocation in standalone mode, passing required arguments and parameters as documented."
