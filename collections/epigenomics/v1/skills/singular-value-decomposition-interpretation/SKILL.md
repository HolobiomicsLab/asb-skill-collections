---
name: singular-value-decomposition-interpretation
description: Use when after loading and normalizing a beta-valued methylation matrix (450K or EPIC array), apply SVD interpretation when you need to assess whether observed variation is driven by batch effects rather than biological signal, or when you want to determine the true dimensionality of latent.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0654
  tools:
  - ChAMP
  - ChAMPdata
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

# singular-value-decomposition-interpretation

## Summary

Interprets SVD output from DNA methylation data to detect and characterize batch effects and latent components using Random Matrix Theory thresholding. This skill identifies when principal components exceed the theoretical maximum and correctly applies component capping to avoid over-interpretation of technical artifacts.

## When to use

After loading and normalizing a beta-valued methylation matrix (450K or EPIC array), apply SVD interpretation when you need to assess whether observed variation is driven by batch effects rather than biological signal, or when you want to determine the true dimensionality of latent technical confounders in the data.

## When NOT to use

- Input beta matrix has not been quality-controlled or normalized; apply QC filtering first.
- You expect true biological dimensionality >20 in your data; the 20-component cap is a hard ceiling for reporting, not a recommendation to truncate analysis before batch correction.

## Inputs

- normalized beta-valued matrix (rows: CpG probes; columns: samples)
- sample metadata table (optional, for correlating components with batch variables)

## Outputs

- component count (maximum 20 when Random Matrix Theory detects >20)
- singular values and corresponding loadings
- scree plot showing variance explained per component
- component correlation summary with batch variables

## How to apply

Call champ.SVD() on the normalized beta matrix to perform singular value decomposition analysis. The function automatically applies Random Matrix Theory to detect the number of latent components present in the methylation dataset. If Random Matrix Theory identifies more than 20 latent components, ChAMP implements a component capping mechanism that reports exactly 20 components as the maximum—this is by design to prevent spurious inflation of component count. Inspect the returned component count and visualize the scree plot to assess the proportion of variance explained by each component. Use the component structure to identify batch variables (e.g., processing date, array position, technician) that correlate with the principal components, indicating batch contamination.

## Related tools

- **ChAMP** (primary tool for executing champ.SVD() and interpreting component structure in methylation data) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (provides CpG annotation and test datasets (e.g., 450K lung tumor data, EPICSimData) for validation) — https://github.com/YuanTian1991/ChAMPdata
- **ComBat** (downstream batch correction method applied after SVD identifies batch effects)

## Examples

```
champ.SVD(beta = normalized_beta_matrix, pd = sample_metadata)
```

## Evaluation signals

- Verify that component count returned is ≤20; if Random Matrix Theory detects >20 latent components, confirm the output reports exactly 20.
- Scree plot shows monotonically decreasing variance explained; components beyond the elbow should represent noise or random variation.
- Top components correlate significantly (Pearson r or Spearman ρ) with known batch variables (e.g., array position, processing date); biological covariates should not dominate early components.
- After applying ComBat correction using identified batch variables, re-run SVD and confirm that component count decreases and remaining components do not correlate with batch metadata.

## Limitations

- Component cap of 20 is a hard limit; datasets with genuine biological dimensionality >20 will not reveal all latent structure through this function.
- Random Matrix Theory thresholding assumes the correlation matrix follows null model assumptions; severe batch imbalance or extreme outlier samples may violate these assumptions.
- SVD detects linear combinations of probes; non-linear batch effects or probe-level spatial confounding may not be captured.
- The 450K lung tumor test dataset contains only 8 samples (4 tumor, 4 control), limiting statistical power to detect weak batch effects; larger datasets are recommended for robust interpretation.

## Evidence

- [other] champ.SVD() implements a component capping mechanism that selects only the top 20 components when Random Matrix Theory detects more than 20 latent variables: "champ.SVD() implements a component capping mechanism that selects only the top 20 components when Random Matrix Theory detects more than 20 latent variables in the methylation dataset."
- [intro] SVD method allows in-depth assessment of batch effects in methylation data: "The singular value decomposition (SVD) method allows an in-depth look at batch effects"
- [intro] ChAMP provides workflow for loading and analyzing methylation array data: "ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis"
- [intro] 450K test dataset characteristics for validation: "The 450k lung tumor data set contains only 8 samples, 4 lung tumor samples (T) and 4 control samples (C)"
