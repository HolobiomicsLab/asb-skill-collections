---
name: methylation-batch-effect-detection
description: Use when you have loaded a normalized beta-valued methylation matrix (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0654
  tools:
  - ChAMP
  - ChAMPdata
  - minfi
  - ComBat
derived_from:
- doi: 10.1093/bioinformatics/btx513
  title: champ
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_champ
    doi: 10.1093/bioinformatics/btx513
    title: champ
  dedup_kept_from: coll_champ
schema_version: 0.2.0
---

# methylation-batch-effect-detection

## Summary

Detect and visualize batch effects in DNA methylation array data (450K and EPIC) using singular value decomposition (SVD) with Random Matrix Theory component capping. This skill identifies latent batch-related variability before normalization or correction.

## When to use

Apply this skill when you have loaded a normalized beta-valued methylation matrix (e.g., from HumanMethylation450 or EPIC arrays) and need to assess whether technical batch effects or unknown latent variables are confounding your sample groups prior to downstream analysis (DMR detection, differential methylation testing).

## When NOT to use

- Input is raw (non-normalized) .idat intensity files — use champ.load() and normalization steps first
- You have already corrected batch effects with ComBat or similar and now seek to validate correction success — use post-correction QC plots instead
- Your data contains fewer samples than components to extract — SVD will be uninformative

## Inputs

- normalized beta-valued matrix from HumanMethylation450 or EPIC array data
- optional: sample metadata table with batch, treatment, and technical covariates

## Outputs

- SVD component loadings matrix (samples × up to 20 components)
- explained variance per component
- scree plot and heatmap visualizations
- batch effect assessment summary

## How to apply

Load a normalized beta matrix into R and call champ.SVD() to perform singular value decomposition analysis. The function automatically applies Random Matrix Theory to detect the number of latent components in the data. When Random Matrix Theory identifies more than 20 latent components, ChAMP's implementation caps the output to the top 20 principal components for interpretability. Inspect the returned component loadings and variance explained to identify which experimental variables (batch, sample type, technical replicate) correlate with the principal components. Components with strong correlation to known technical factors (batch ID, array position, processing date) indicate batch effects requiring correction via ComBat or similar methods before proceeding to differential analysis.

## Related tools

- **ChAMP** (primary tool implementing champ.SVD() function for batch effect detection with Random Matrix Theory capping) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (data package providing methylation array annotations and example datasets (HumanMethylation450, EPICSimData)) — https://github.com/YuanTian1991/ChAMPdata
- **minfi** (alternative normalization and quality control for methylation arrays, used alongside ChAMP)
- **ComBat** (downstream batch effect correction method applied after SVD identifies batch-correlated components)

## Examples

```
champ.SVD(beta=myBetaMatrix, pd=mySampleMetadata)
```

## Evaluation signals

- champ.SVD() returns exactly 20 components when Random Matrix Theory detects >20 latent variables (not more, not fewer)
- Scree plot shows monotonically decreasing variance explained across the 20 components
- Batch variable (e.g., array ID, processing date) has significant Pearson or Spearman correlation (|r| > 0.6) with at least one of the top 3 principal components
- Sample type or phenotype of interest shows weak or no correlation with early principal components (r < 0.4), indicating batch, not biology, dominates variance structure
- Post-ComBat correction: re-run champ.SVD() and verify batch variable correlation drops below |r| < 0.4 and biological variable correlation remains strong

## Limitations

- The 20-component cap is fixed and may obscure additional latent structure if >20 true components exist; this is a design choice for interpretability, not a statistical threshold
- SVD assumes linear batch effects; non-linear or interaction-based batch confounders may not be detected
- Requires already-normalized beta matrix; raw intensity data will yield misleading component structure
- Random Matrix Theory component detection is automatic and cannot be tuned; if detection fails, users must manually inspect scree plot and choose components
- SVD alone does not correct batch effects — only identifies them; downstream correction (e.g., ComBat) is required before analysis

## Evidence

- [other] champ.SVD() implements a component capping mechanism that selects only the top 20 components when Random Matrix Theory detects more than 20 latent variables in the methylation dataset.: "champ.SVD() implements a component capping mechanism that selects only the top 20 components when Random Matrix Theory detects more than 20 latent variables"
- [intro] The singular value decomposition (SVD) method allows an in-depth look at batch effects: "The singular value decomposition (SVD) method allows an in-depth look at batch effects"
- [intro] For correction of multiple batch effects the ComBat method has been implemented: "for correction of multiple batch effects the ComBat method has been implemented"
- [intro] ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis: "ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis"
- [intro] a variety of different data import methods (e.g. from .idat files or a beta-valued matrix): "a variety of different data import methods (e.g. from .idat files or a beta-valued matrix)"
