---
name: omics-data-quality-assessment-normalization-context
description: Use when after loading peptide or protein-level quantification matrices with sample metadata into pmartR, and before proceeding to statistical analysis (ANOVA, G-test).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# omics-data-quality-assessment-normalization-context

## Summary

Assessment of proteomics data quality and selection of appropriate normalization centering measures before statistical analysis. This skill uses the SPANS procedure to automatically evaluate and select optimal centering methods (mean, median, geometric mean, robust normalization) rather than requiring manual selection, ensuring that normalization choices are data-driven and reproducible.

## When to use

After loading peptide or protein-level quantification matrices with sample metadata into pmartR, and before proceeding to statistical analysis (ANOVA, G-test). Use when you have proteomics expression data and need to determine which centering method is most appropriate for your specific dataset, particularly when manual method selection introduces subjectivity or when comparing datasets across different experiments.

## When NOT to use

- When data has already been normalized by upstream processing (e.g., vendor-supplied normalized abundance values) — applying SPANS to pre-normalized data risks double-normalization artifacts.
- When a specific centering method is required by downstream statistical or regulatory protocols — SPANS automaticity may conflict with mandated standardization.
- For non-proteomics omics data types (metabolomics, transcriptomics, genomics) where SPANS is explicitly designed for proteomics — applicability to other omics types is not documented.

## Inputs

- peptide-level quantification matrix (expression data)
- protein-level quantification matrix (expression data)
- sample metadata (phenotypes, groups, covariates)
- biomolecule metadata (peptide/protein annotations)

## Outputs

- normalized expression matrix (centered using SPANS-selected method)
- metadata documenting selected centering approach
- quality assessment report indicating normalization method applied

## How to apply

Load the proteomics expression data (peptide or protein-level quantification matrix) and sample metadata into the pmartR Shiny GUI. Navigate to the Normalization step in the analysis workflow. Instead of manually selecting a centering method, invoke the SPANS procedure, which automatically evaluates available centering options (mean, median, geometric mean, robust normalization) and selects the optimal approach based on data characteristics. Apply the SPANS-selected centering method to normalize the expression matrix. The procedure reduces bias by removing subjective method selection and provides reproducible centering that accounts for the distributional properties of your specific proteomics dataset.

## Related tools

- **pmartR** (R package providing SPANS procedure and normalization algorithms; backend for all normalization and centering computations) — https://github.com/pmartR/pmartR
- **PMart Shiny GUI** (Web interface wrapping pmartR that exposes SPANS normalization workflow without requiring R coding; primary user-facing tool for this skill) — https://github.com/pmartR/PMart_ShinyApp
- **R** (Computation environment executing pmartR and SPANS logic)

## Examples

```
After uploading proteomics data and sample metadata into the PMart Shiny GUI, navigate to the Normalization tab and select 'SPANS procedure' from the centering method dropdown, then click 'Apply Normalization' to automatically evaluate and apply the optimal centering method.
```

## Evaluation signals

- Metadata output explicitly documents which centering method (mean, median, geometric mean, or robust normalization) was selected by SPANS for the dataset.
- Normalized expression matrix shows reduced systematic bias compared to raw data, detectable through exploratory data analysis (PCA, correlation heatmaps) available in the GUI.
- SPANS selection is reproducible across repeated runs on the same dataset, confirming the procedure is deterministic.
- Post-normalization sample distributions (visualized via PCA or missing-variable plots in the GUI) show improved homogeneity across experimental groups compared to pre-normalization data.
- Statistical analysis downstream (ANOVA, G-test) produces consistent effect sizes and p-values, indicating stable and appropriate normalization.

## Limitations

- SPANS is documented only for proteomics data; applicability to other omics modalities (metabolomics, transcriptomics) is not established in the pmartR documentation.
- No explicit performance benchmarks, validation protocols, or comparison metrics are provided in the source material; the procedure is presented as a capability without quantitative validation data.
- The README and article do not enumerate the exact criteria or thresholds SPANS uses to evaluate and rank centering methods, making the decision-making logic a black box to users.
- SPANS is available only through the pmartR ecosystem; no standalone or language-agnostic implementation is mentioned.

## Evidence

- [other] The normalization step in the GUI centers proteomics data using a variety of methods, with the SPANS procedure available to automatically determine the appropriate centering measure rather than requiring manual selection.: "The normalization step in the GUI centers proteomics data using a variety of methods, with the SPANS procedure available to automatically determine the appropriate centering measure rather than"
- [readme] Normalization. Center data using a variety of methods. Determine appropriate measures automatically using the SPANS procedure for proteomics.: "Normalization.  Center data using a variety of methods.  Determine appropriate measures automatically using the SPANS procedure for proteomics."
- [other] Apply the SPANS procedure to automatically evaluate and select the optimal centering method from available options (e.g., mean, median, geometric mean, robust normalization).: "Apply the SPANS procedure to automatically evaluate and select the optimal centering method from available options (e.g., mean, median, geometric mean, robust normalization)."
- [other] Load proteomics expression data (peptide or protein-level quantification matrix) and sample metadata into pmartR.: "Load proteomics expression data (peptide or protein-level quantification matrix) and sample metadata into pmartR."
- [other] Return the normalized expression matrix with metadata documenting which centering approach was selected and applied.: "Return the normalized expression matrix with metadata documenting which centering approach was selected and applied."
