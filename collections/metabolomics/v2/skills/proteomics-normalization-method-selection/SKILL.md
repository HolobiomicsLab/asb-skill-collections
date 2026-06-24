---
name: proteomics-normalization-method-selection
description: Use when after loading peptide or protein-level quantification matrices
  with sample metadata into pmartR, and before downstream statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - pmartR
  - R
  - Shiny
  license_tier: open
derived_from:
- doi: 10.1021/acs.jproteome.3c00512
  title: PMart
evidence_spans:
- Shiny GUI implementation of the pmartR R package.
- Shiny GUI implementation of the pmartR R package
- the bulk of the functionality of the package to be available to the user without
  the need for familiarity with R or the package itself
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.3c00512
  all_source_dois:
  - 10.1021/acs.jproteome.3c00512
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# proteomics-normalization-method-selection

## Summary

Automatic selection of optimal data centering methods for proteomics expression matrices using the SPANS procedure, eliminating manual trial-and-error in normalization. This skill applies statistical criteria to choose from mean, median, geometric mean, and robust normalization approaches before centering the data.

## When to use

After loading peptide or protein-level quantification matrices with sample metadata into pmartR, and before downstream statistical analysis. Use this skill when you have proteomics expression data that requires normalization but lack prior knowledge about which centering method (mean, median, geometric mean, robust) best suits your data distribution and batch structure.

## When NOT to use

- Data has already been normalized or centered using a predetermined method (SPANS is for automatic selection, not re-normalization)
- Proteomics data is missing group assignment or batch metadata required for SPANS evaluation
- Analysis requires a specific centering method mandated by prior protocol or publication; use manual method selection instead

## Inputs

- peptide or protein-level quantification matrix (expression data)
- sample metadata (sample information including batch, group assignment)
- biomolecule metadata (peptide or protein annotations)

## Outputs

- normalized expression matrix (centered using SPANS-selected method)
- normalization metadata (documenting which centering method was selected and applied)

## How to apply

The SPANS procedure automatically evaluates available centering methods against the loaded proteomics data using statistical criteria to identify the most appropriate normalization approach. Load expression data (peptide or protein quantification matrix) and sample metadata into the pmartR GUI. Invoke the SPANS procedure via the Normalization tab, which evaluates each candidate centering method and selects the one that produces the most appropriate normalized distribution. Apply the SPANS-selected centering method to the expression matrix. Document the chosen centering measure in the output metadata for reproducibility and downstream interpretation.

## Related tools

- **pmartR** (R package providing SPANS procedure and normalization functions; backend for method evaluation and data centering) — https://github.com/pmartR/pmartR
- **Shiny** (GUI framework exposing pmartR normalization and SPANS procedure to users without R familiarity) — https://github.com/pmartR/PMart_ShinyApp
- **R** (Language runtime for pmartR package execution and SPANS statistical computations)

## Evaluation signals

- SPANS procedure completes without error and returns a single selected centering method (mean, median, geometric mean, or robust) from the candidate set
- Output metadata documents the name of the centering method selected by SPANS and matches one of the available methods implemented in pmartR
- Normalized expression matrix has identical dimensions to input matrix; no rows or columns are dropped during centering
- Distribution of normalized values is consistent with the expected behavior of the selected centering method (e.g., median-centered data should have symmetric residuals around zero for symmetric distributions)
- Downstream statistical analyses (ANOVA, G-test) produce stable and reproducible results when run on SPANS-normalized data

## Limitations

- SPANS evaluation depends on quality and completeness of sample metadata and group assignments; incomplete or mislabeled metadata may lead to suboptimal method selection
- The procedure selects from a fixed set of centering methods available in pmartR (mean, median, geometric mean, robust); if none of these methods is appropriate for the specific proteomics data distribution, SPANS cannot recommend alternatives
- SPANS is implemented for proteomics data in pmartR; applicability to other omics data types (metabolomics, genomics) is not addressed in the source material

## Evidence

- [other] The normalization step in the GUI centers proteomics data using a variety of methods, with the SPANS procedure available to automatically determine the appropriate centering measure rather than requiring manual selection.: "with the SPANS procedure available to automatically determine the appropriate centering measure rather than requiring manual selection"
- [other] Apply the SPANS procedure to automatically evaluate and select the optimal centering method from available options (e.g., mean, median, geometric mean, robust normalization).: "Apply the SPANS procedure to automatically evaluate and select the optimal centering method from available options (e.g., mean, median, geometric mean, robust normalization)"
- [readme] Normalization. Center data using a variety of methods. Determine appropriate measures automatically using the SPANS procedure for proteomics.: "Determine appropriate measures automatically using the SPANS procedure for proteomics"
- [other] Load proteomics expression data (peptide or protein-level quantification matrix) and sample metadata into pmartR.: "Load proteomics expression data (peptide or protein-level quantification matrix) and sample metadata into pmartR"
- [other] Center the data using the SPANS-determined method. Return the normalized expression matrix with metadata documenting which centering approach was selected and applied.: "Return the normalized expression matrix with metadata documenting which centering approach was selected and applied"
