---
name: batch-effect-correction-workflow
description: Use when you have a feature table generated from LC-MS/MS non-targeted metabolomics data that spans multiple sample preparation batches, instrumental runs, or experimental conditions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Jupyter Notebook
  - FBMN-STATS
  techniques:
  - LC-MS
derived_from:
- doi: 10.1038/s41596-024-01046-3
  title: FBMN-STATS
evidence_spans:
- To easily install and run Jupyter Notebook in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fbmn_stats_cq
    doi: 10.1038/s41596-024-01046-3
    title: FBMN-STATS
  dedup_kept_from: coll_fbmn_stats_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41596-024-01046-3
  all_source_dois:
  - 10.1038/s41596-024-01046-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# batch-effect-correction-workflow

## Summary

Batch effect correction is a preprocessing step applied to non-targeted LC-MS/MS metabolomics feature tables to remove systematic variation introduced by instrumental or experimental batch conditions before multivariate statistical analysis. Correcting batch effects ensures that observed patterns in downstream analyses reflect true biological differences rather than technical artifacts.

## When to use

Apply this skill when you have a feature table generated from LC-MS/MS non-targeted metabolomics data that spans multiple sample preparation batches, instrumental runs, or experimental conditions. Use it after data merging, data cleanup, and blank removal, and before univariate or multivariate statistical analysis. Batch correction is particularly critical when comparing samples across multiple MassIVE datasets or when instrumental drift or batch-specific systematic noise is suspected.

## When NOT to use

- If your data derives from a single instrumental batch or experimental run with no known batch effects, batch correction may introduce artifacts rather than remove them.
- If batch structure is confounded with treatment/phenotype (e.g., all treatment samples in batch 1, all controls in batch 2), batch correction risks removing true biological signal.
- If input data have not yet undergone data cleanup, blank removal, or merging—apply those preprocessing steps first.

## Inputs

- Feature table (intensity matrix with features as rows, samples as columns)
- Sample metadata file with batch assignment information
- Blank-removed and cleaned feature abundance matrix

## Outputs

- Batch-corrected feature table (same dimensions as input, with batch effects removed)
- Batch effect diagnostics and visualization (e.g., PCA before/after correction)
- Correction parameters and model metadata for reproducibility

## How to apply

Load the merged, cleaned, and blank-removed feature table into the FBMN-STATS Jupyter Notebook environment (R or Python). Apply batch correction algorithms available in the notebook—typically combat or similar variance-stabilizing methods—which model and remove batch-specific effects while preserving biological signal. The notebook parameterizes the batch variable based on sample metadata (e.g., run date, instrument ID, or explicit batch assignment). After correction, verify that principal component analysis (PCA) plots no longer show clustering by batch, and that the corrected feature abundance distributions are statistically comparable across batches before proceeding to univariate and multivariate statistical analyses.

## Related tools

- **Jupyter Notebook** (Interactive environment for executing the batch correction notebook and visualizing before/after batch effects) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **R** (Statistical programming language in which batch correction algorithms are implemented in the FBMN-STATS notebooks) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **FBMN-STATS** (Repository containing validated Jupyter Notebooks with batch correction workflow integrated into the full preprocessing pipeline) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS

## Evaluation signals

- PCA plots before and after correction show no clear clustering by batch variable; biological/phenotypic clustering is preserved or enhanced.
- Feature abundance distributions are comparable across batches post-correction; variance is not driven by batch membership.
- Output feature table has identical dimensions to input; all features and samples are retained (no rows or columns dropped).
- Batch correction parameters (e.g., batch means, shrinkage estimates) are saved and reproducible when re-running the notebook.
- Downstream multivariate statistical results (e.g., principal component loadings, discriminant analysis scores) are not dominated by batch artifacts.

## Limitations

- Batch correction assumes that batch effects are additive or multiplicative across features; non-linear batch patterns may not be fully corrected.
- If batch structure is strongly confounded with true biological treatment, correction may inadvertently remove treatment signal.
- Colab environment automatically disconnects after 90 minutes of idleness or 12 continuous hours of use, requiring re-running the entire batch correction workflow.
- Disk space in Google Colab is limited to 77 GB; correction of very large metabolomics datasets (multiple GB feature tables) may exhaust storage.
- Batch metadata must be accurately recorded and provided; missing or mislabeled batch information will compromise correction quality.

## Evidence

- [readme] perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data"
- [other] Statistical analysis methods can be applied to feature-based molecular networks from non-targeted LC-MS/MS metabolomics data: "Statistical analysis methods can be applied to feature-based molecular networks from non-targeted LC-MS/MS metabolomics data"
- [other] The notebooks provided here enable multivariate statistical analysis of non-targeted LC-MS/MS data: "The FBMN-STATS repository contains Jupyter notebooks that enable multivariate statistical analysis"
