---
name: random-matrix-theory-application
description: Use when when analyzing normalized DNA methylation beta matrices (450K or EPIC arrays) and you need to identify the true number of latent batch or technical factors present in the data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3935
  edam_topics:
  - http://edamontology.org/topic_3295
  - http://edamontology.org/topic_0634
  tools:
  - ChAMP
  - ChAMPdata
  - minfi
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

# random-matrix-theory-application

## Summary

Apply Random Matrix Theory (RMT) within champ.SVD() to detect and cap the number of latent components in methylation data, limiting reported principal components to a maximum of 20 when RMT identifies more than 20 underlying factors. This skill enables robust batch effect detection by distinguishing true signal structure from noise in high-dimensional methylation arrays.

## When to use

When analyzing normalized DNA methylation beta matrices (450K or EPIC arrays) and you need to identify the true number of latent batch or technical factors present in the data. Use this skill when the sample size or biological complexity suggests potential batch structure but the exact dimensionality is unknown; RMT will automatically detect signal rank while preventing overfitting to noise.

## When NOT to use

- Input data is already a feature table or dimensionality-reduced representation (e.g., already run through PCA or t-SNE); apply RMT-based SVD to raw or normalized abundance matrices, not derived features.
- Sample size is extremely small (< 5–8 samples) or data contains no clear batch structure; RMT requires sufficient signal-to-noise ratio to reliably detect latent components.
- You require reporting all detected components without capping; if your downstream analysis depends on components >20, this skill's hard maximum of 20 is inappropriate.

## Inputs

- normalized beta matrix (numerical matrix of methylation M-values or beta-values)
- HumanMethylation450 or EPIC array data (loaded from .idat files or pre-processed beta-valued matrix)

## Outputs

- singular value decomposition (SVD) results with latent component count (maximum 20)
- principal components ranked by variance explained
- component loadings for visualization of batch effects

## How to apply

Load a normalized beta matrix (from .idat files or a beta-valued matrix) into R and call champ.SVD() on the data. The function internally applies Random Matrix Theory to estimate the number of true latent components by analyzing the singular value spectrum. When RMT detects more than 20 latent components, champ.SVD() automatically caps the output to the top 20 principal components. Inspect the returned component count to confirm the capping behavior; this threshold of 20 represents a practical limit beyond which components are likely noise or statistical artifacts. Use the resulting component list to visualize and interpret batch structure (e.g., clustering samples by experimental batches or technical factors).

## Related tools

- **ChAMP** (primary tool implementing champ.SVD() function with built-in Random Matrix Theory component detection and capping) — https://github.com/YuanTian1991/ChAMP
- **ChAMPdata** (data package providing methylation array annotations and test datasets (HumanMethylation450, EPICSimData) required for SVD analysis) — https://github.com/YuanTian1991/ChAMPdata
- **minfi** (alternative or complementary tool providing Functional Normalization preprocessing before SVD application)

## Examples

```
library(ChAMP); data(EPICSimData); champ.SVD(beta = myBeta)
```

## Evaluation signals

- Returned component count equals exactly 20 when Random Matrix Theory detects >20 latent components; component count is ≤20 in all cases.
- Scree plot or variance explained shows a clear elbow or inflection point at or near the detected/capped component rank, indicating RMT correctly identified signal dimensionality.
- Samples cluster by known batch, experimental condition, or technical factor along principal components 1–20, confirming components capture true structure rather than noise.
- SVD component loadings are interpretable and align with metadata (e.g., PC1 separates case vs. control, PC2 separates sequencing batch); components beyond rank 20 show no such structure.

## Limitations

- RMT component detection is sensitive to the degree of normalization and quality control applied before SVD; poor data preprocessing (e.g., uncorrected Type-2 probes, low-quality samples) may confound RMT estimates.
- The hard cap at 20 components may obscure detection of weak but genuine structure beyond rank 20; if downstream analysis depends on >20 components, results may be incomplete.
- RMT assumes a specific noise model (typically Wishart or Marchenko–Pastur distribution); violations (e.g., non-Gaussian noise, heavy-tailed distributions in methylation arrays) may reduce accuracy.
- No changelog or versioning information provided; the capping behavior and RMT implementation may differ across ChAMP versions, potentially affecting reproducibility.

## Evidence

- [other] champ.SVD() implements a component capping mechanism that selects only the top 20 components when Random Matrix Theory detects more than 20 latent variables in the methylation dataset.: "champ.SVD() implements a component capping mechanism that selects only the top 20 components when Random Matrix Theory detects more than 20 latent components in the methylation dataset."
- [other] Does champ.SVD() correctly limit the number of reported principal components to a maximum of 20 when Random Matrix Theory detects more than 20 latent components in the data?: "Does champ.SVD() correctly limit the number of reported principal components to a maximum of 20 when Random Matrix Theory detects more than 20 latent components in the data?"
- [intro] The singular value decomposition (SVD) method allows an in-depth look at batch effects: "The singular value decomposition (SVD) method allows an in-depth look at batch effects"
- [readme] ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis: "ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis"
- [intro] a variety of different data import methods (e.g. from .idat files or a beta-valued matrix): "a variety of different data import methods (e.g. from .idat files or a beta-valued matrix)"
