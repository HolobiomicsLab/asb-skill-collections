---
name: differential-metabolite-detection
description: Use when you have normalized and aligned lipidomic and metabolomic spectral
  features from the Multi-ABLE method across multiple biological samples grouped by
  phenotype (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_2269
  tools:
  - R
  - MultiABLER
  - limma
  - ProteoMM
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1016/j.isci.2023.106881
  title: MultiABLER
- doi: 10.1021/acs.analchem.9b01842
  title: ''
evidence_spans:
- MultiABLER is a set of R functions
- MultiABLER is a set of R functions forms a seamless workflow
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_multiabler_cq
    doi: 10.1016/j.isci.2023.106881
    title: MultiABLER
  dedup_kept_from: coll_multiabler_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.isci.2023.106881
  all_source_dois:
  - 10.1016/j.isci.2023.106881
  - 10.1021/acs.analchem.9b01842
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Differential Metabolite Detection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identifies lipids and metabolites that are significantly associated with a disease phenotype (e.g., atherosclerosis) using multivariate analysis of normalized lipidomic and metabolomic spectral data. This skill detects which molecular features differ between sample groups after preprocessing and alignment.

## When to use

You have normalized and aligned lipidomic and metabolomic spectral features from the Multi-ABLE method across multiple biological samples grouped by phenotype (e.g., atherosclerotic vs. control arterial tissue), and need to identify which specific lipids and metabolites are significantly altered between groups.

## When NOT to use

- Input spectral data have not been preprocessed, normalized, or aligned across samples — run preprocessing first.
- You have only a single sample or no biological replication — multivariate statistical methods require multiple independent samples per group.
- Phenotype information is missing or ambiguous — differential detection requires clear grouping or quantitative phenotype labels.

## Inputs

- Preprocessed and normalized lipidomic spectral feature matrix (rows = m/z features, columns = samples)
- Preprocessed and normalized metabolomic spectral feature matrix (rows = m/z features, columns = samples)
- Phenotype annotation table (sample ID, disease status or quantitative trait)
- Sample metadata (e.g., tissue type, treatment group)

## Outputs

- Ranked list of differential lipids with p-values and fold-changes
- Ranked list of differential metabolites with p-values and fold-changes
- Statistical summary tables (coefficients, significance thresholds)
- Multivariate analysis plots (e.g., score plots, loadings, volcano plots)
- Quality control visualizations showing group separation

## How to apply

Load the preprocessed and normalized spectral feature matrix (rows = features, columns = samples) along with phenotype metadata into R. Execute the MultiABLER multivariate analysis functions, which apply statistical and/or machine-learning methods to rank features by association with the disease phenotype. The functions produce ranked lists of differential lipids and metabolites with statistical significance values, along with quality control plots showing feature separation between phenotype groups. Interpretation is grounded in the magnitude of fold-change or model coefficient, statistical significance (typically p < 0.05 after multiple-testing correction), and biological plausibility within the atherosclerosis literature.

## Related tools

- **MultiABLER** (Implements the multivariate analysis functions to identify differential lipids and metabolites from integrated spectral feature matrices) — https://github.com/holab-hku/MultiABLER
- **R** (Execution environment for MultiABLER functions and statistical/visualization workflows)
- **limma** (Linear modeling and multiple-testing correction for differential feature detection) — https://www.bioconductor.org/packages/release/bioc/html/limma.html
- **ProteoMM** (Multivariate statistical methods for omics feature ranking and visualization) — https://www.bioconductor.org/packages/release/bioc/html/ProteoMM.html

## Examples

```
devtools::install_github("holab-hku/MultiABLER", dependencies = TRUE); source('MultiABLER.r'); result <- multivariate_differential_analysis(feature_matrix = normalized_lipids, phenotype = atherosclerosis_status, method = 'limma')
```

## Evaluation signals

- Ranked feature lists contain only m/z features that passed quality thresholds (non-zero intensity across replicates, intensity above background).
- Statistical significance values show expected distribution: majority of features above threshold (e.g., p > 0.05), top differential features show p < 0.05 after multiple-testing correction.
- Multivariate score and loading plots show clear visual separation between phenotype groups along principal axes.
- Fold-change magnitudes are biologically plausible: differential lipids and metabolites known from literature to be perturbed in atherosclerosis appear in top-ranked lists.
- Output plots and tables are reproducible across independent runs with the same input data and parameter settings.

## Limitations

- MultiABLER is designed specifically for the Multi-ABLE method; data from other lipidomic/metabolomic platforms may require input reformatting or separate preprocessing pipelines.
- Small sample sizes (< 5 replicates per group) reduce statistical power; no minimum sample size is specified in the article.
- The method assumes that preprocessed features are already normalized and aligned; batch effects and instrumental drift introduced before running multivariate analysis will propagate to differential detection results.
- Identification of detected lipids and metabolites as specific molecular species requires orthogonal validation (e.g., tandem MS/MS, retention time matching, or synthetic standards), which is outside the scope of MultiABLER.

## Evidence

- [other] Run the multivariate analysis functions to identify differential lipids and metabolites associated with atherosclerosis phenotypes.: "Run the multivariate analysis functions to identify differential lipids and metabolites associated with atherosclerosis phenotypes."
- [other] MultiABLER supports integrative processing and analysis of lipidomic and metabolomic data generated by the Multi-ABLE method.: "MultiABLER supports integrative processing and analysis of lipidomic and metabolomic data generated by the Multi-ABLE method"
- [readme] To run MultiABLER, install the following packges in R and run the funcions in MultiABLER.r. A detailed tutorial on how to run MultiABLER can be found in here.: "To run MultiABLER, install the following packges in R and run the funcions in MultiABLER.r"
- [readme] In case of installation issues, try install the following dependencies: ProteoMM, limma, Tidyverse.: "In case of installation issues, try install the following dependencies and run the above code: ProteoMM, limma, Tidyverse"
