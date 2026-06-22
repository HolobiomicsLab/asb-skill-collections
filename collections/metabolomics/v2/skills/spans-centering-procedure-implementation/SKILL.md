---
name: spans-centering-procedure-implementation
description: Use when normalizing peptide or protein-level quantification matrices in proteomics workflows and you need to center the data but lack domain knowledge to manually select among mean, median, geometric mean, or robust centering methods.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3577
  tools:
  - pmartR
  - R
  - PMart Shiny GUI
derived_from:
- doi: 10.1021/acs.jproteome.3c00512
  title: PMart
evidence_spans:
- Shiny GUI implementation of the pmartR R package.
- Shiny GUI implementation of the pmartR R package
- the bulk of the functionality of the package to be available to the user without the need for familiarity with R or the package itself
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pmart_cq
    doi: 10.1021/acs.jproteome.3c00512
    title: PMart
  dedup_kept_from: coll_pmart_cq
schema_version: 0.2.0
---

# SPANS-centering-procedure-implementation

## Summary

The SPANS (Spanning Proteomics Analysis with Normalization Selection) procedure automatically selects the optimal centering method (mean, median, geometric mean, or robust normalization) for proteomics expression data normalization, eliminating manual method selection in the pmartR pipeline. This data-driven approach ensures proteomics datasets are normalized using statistically appropriate centering measures tailored to their distributional characteristics.

## When to use

Apply this skill when normalizing peptide or protein-level quantification matrices in proteomics workflows and you need to center the data but lack domain knowledge to manually select among mean, median, geometric mean, or robust centering methods. SPANS is particularly valuable when analyzing diverse proteomics cohorts where distributional assumptions may vary across datasets or when a reproducible, non-subjective normalization approach is required for biomarker discovery pipelines.

## When NOT to use

- Data have already been normalized using an alternative method and re-normalization is not intended.
- Analysis requires a specific centering method mandated by external protocol or prior publication; SPANS selection is automatic and not user-overrideable in the default workflow.
- Input is not proteomics quantification data (e.g., metabolomics or genomics expression formats may have different distributional assumptions not addressed by SPANS).

## Inputs

- Peptide-level or protein-level quantification matrix (expression data)
- Sample metadata and experimental design information
- Optionally, previously defined group assignments and filtering criteria

## Outputs

- Centered/normalized expression matrix
- Metadata field documenting which centering method was selected and applied by SPANS

## How to apply

Load the proteomics expression matrix (peptide or protein-level quantification data) and corresponding sample metadata into the pmartR Shiny GUI or R environment. Invoke the SPANS procedure during the normalization workflow step, which evaluates candidate centering methods against the empirical distribution of the expression data and automatically selects the most appropriate measure. The procedure applies the selected centering method to produce a normalized matrix documented with the centering method identifier. The rationale is that SPANS reduces analyst bias by using data-driven criteria rather than prior assumptions about normalization approach, and ensures consistency across multi-study analyses by applying the same algorithmic selection logic.

## Related tools

- **pmartR** (R package providing the computational backend for SPANS procedure implementation and normalization method evaluation) — https://github.com/pmartR/pmartR
- **PMart Shiny GUI** (Web application exposing SPANS normalization workflow and automated centering method selection without requiring R code) — https://github.com/pmartR/PMart_ShinyApp
- **R** (Programming language runtime for executing pmartR normalization functions)

## Evaluation signals

- Normalized expression matrix contains no missing values in the centering step (values were centered, not removed).
- Metadata documentation clearly identifies which centering method (mean, median, geometric mean, or robust) was selected by SPANS.
- Downstream statistical analyses (e.g., ANOVA, G-test for biomarker discovery) produce consistent results when applied to SPANS-normalized data versus manually-selected normalization, or show improvement in biomarker recovery on validation cohorts.
- Comparison of centering method selection across datasets processed through SPANS shows systematic, reproducible choices rather than arbitrary or analyst-dependent variation.
- Principal component analysis or exploratory visualizations on normalized data show reduced technical artifact clustering and improved separation of biological groups relative to alternative centering methods.

## Limitations

- SPANS procedure selection is automatic and the chosen centering method cannot be manually overridden in the default GUI workflow if the selected method is deemed inappropriate for a given use case.
- The article does not provide explicit documentation of the algorithmic criteria SPANS uses to evaluate and rank candidate centering methods, limiting transparency and reproducibility of the selection logic.
- SPANS is designed specifically for proteomics data; applicability to other omics modalities (metabolomics, transcriptomics, lipidomics) with different distributional characteristics is not discussed.
- No performance benchmarks, comparative validation results, or sensitivity analyses are provided in the article to quantify SPANS' improvement over manual method selection or alternative automated approaches.

## Evidence

- [other] The normalization step in the GUI centers proteomics data using a variety of methods, with the SPANS procedure available to automatically determine the appropriate centering measure: "Normalization.  Center data using a variety of methods.  Determine appropriate measures automatically using the SPANS procedure for proteomics."
- [other] SPANS evaluates and selects the optimal centering method from available options for normalization: "Apply the SPANS procedure to automatically evaluate and select the optimal centering method from available options (e.g., mean, median, geometric mean, robust normalization)."
- [other] The result of applying SPANS is a normalized expression matrix documented with centering method metadata: "Return the normalized expression matrix with metadata documenting which centering approach was selected and applied."
- [readme] pmartR Shiny GUI implementation enables proteomics normalization workflows without R familiarity: "Shiny GUI implementation of the pmartR R package... the bulk of the functionality of the package to be available to the user without the need for familiarity with R"
