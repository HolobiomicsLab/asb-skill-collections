---
name: replicate-based-unwanted-variation-estimation
description: Use when when you have metabolomics data organised across multiple experimental
  batches with deliberately embedded sample replicates within batches (short replicates)
  and across batches (batch replicates), and you observe batch effects or signal drift
  in PCA plots that obscure biological patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - hRUV
  - RUV-III
  - R
  - SummarizedExperiment
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1101/2020.12.21.423723
  title: hRUV
evidence_spans:
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data'
- '`hRUV` is a package for normalisation of multiple batches of metabolomics data
  in a hierarchical strategy'
- 'utilises 2 types of replicates: intra-batch and inter-batch replicates to estimate
  the unwanted variation within and between batches with RUV-III'
- Install the R package from GitHub using the `devtools` package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hruv_cq
    doi: 10.1101/2020.12.21.423723
    title: hRUV
  dedup_kept_from: coll_hruv_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.12.21.423723
  all_source_dois:
  - 10.1101/2020.12.21.423723
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# replicate-based-unwanted-variation-estimation

## Summary

Estimate unwanted variation (batch effects and signal drift) in multi-batch metabolomics data by leveraging intra-batch and inter-batch sample replicates with RUV-III, enabling hierarchical normalisation that removes technical noise while preserving biological signal.

## When to use

When you have metabolomics data organised across multiple experimental batches with deliberately embedded sample replicates within batches (short replicates) and across batches (batch replicates), and you observe batch effects or signal drift in PCA plots that obscure biological patterns. This skill applies specifically when replicates are available and systematically arranged to characterise both intra-batch and inter-batch unwanted variation.

## When NOT to use

- Input data lacks structured replicate samples embedded within and across batches; RUV-III requires replicate information to estimate unwanted variation.
- Data is already batch-corrected or normalised by another method; applying hRUV post-hoc may introduce artefacts or over-normalisation.
- Sample size or replicate density is insufficient (e.g., fewer than 2–3 replicates per batch or very few batches); RUV-III estimates become unstable with sparse replicate information.

## Inputs

- SummarizedExperiment object with cleaned, imputed assay (e.g., rawImpute)
- Batch metadata (assignment of samples to experimental runs)
- Replicate metadata (intra-batch and inter-batch replicate designations)
- Log-transformed and quality-filtered metabolite abundance matrix

## Outputs

- Normalised assay (loessShort_concatenate) within the SummarizedExperiment object
- Unwanted variation estimates (RUV-III factors) for intra-batch and inter-batch components
- Signal drift-corrected metabolite abundance matrix

## How to apply

Load the SummarizedExperiment object containing the log-transformed, cleaned assay (e.g., rawImpute after filtering metabolites with >50% missing values per batch and k-nearest neighbour imputation) along with batch and replicate metadata. Call the hRUV function with: intra='loessShort' (applies non-linear loess smoothing for intra-batch signal drift correction), inter='concatenate' (hierarchical structure for inter-batch variation), intra_k=5 (uses 5 nearest replicate neighbours within batches for RUV-III estimation), and inter_k=5 (uses 5 nearest replicate neighbours across batches for RUV-III estimation). The function decomposes unwanted variation into within-batch and between-batch components, estimates the unwanted variation matrix using replicate information, and returns a normalised assay. Validate success by confirming that batch effects are eliminated in PCA plots of the resulting loessShort_concatenate assay and that biological variance structure is preserved.

## Related tools

- **hRUV** (Primary normalisation package that implements hierarchical RUV-III strategy with intra-batch and inter-batch replicate decomposition and loess smoothing for metabolomics batch correction) — https://github.com/SydneyBioX/hRUV
- **RUV-III** (Underlying statistical method for estimating unwanted variation using sample replicates; utilised separately for intra-batch and inter-batch unwanted variation estimation)
- **SummarizedExperiment** (Data container for storing metabolite abundance matrices, assays, and metadata (batch, replicate designations) required as input and output) — https://bioconductor.org/packages/SummarizedExperiment/
- **R** (Execution environment for hRUV package and downstream analysis)

## Examples

```
library(hRUV); dat <- hRUV(dat, intra='loessShort', inter='concatenate', intra_k=5, inter_k=5); loessShort_concatenate_assay <- assay(dat, 'loessShort_concatenate')
```

## Evaluation signals

- PCA plots of the normalised assay show no clustering by batch; batch effects visible in raw or imputed assay are eliminated.
- Biological sample groupings (e.g., patient phenotypes or treatment groups) remain distinct and are not obscured by technical batch variation in the normalised assay.
- Signal drift across experimental run order is corrected; metabolite intensities no longer show systematic trends correlated with batch sequence.
- Replicate samples (intra-batch and inter-batch) cluster tightly together in PCA space after normalisation, validating removal of replicate-specific technical noise.
- Metabolite abundance distributions within the normalised assay show expected ranges without extreme compression or inflation compared to the original assay.

## Limitations

- Requires deliberate experimental design with embedded replicates; cannot be applied retroactively to data lacking replicate samples.
- Performance depends on replicate quality and representation across batches; sparse or unbalanced replicate distributions may lead to unstable RUV-III estimates.
- The method assumes linearity (loessShort smoothing) and hierarchical batch structure; may not fully capture complex, non-monotonic drift patterns or unusual batch interactions.
- Normalisation is specific to the replicate structure and batch arrangement of the study; results may not transfer directly to new batches or studies with different replicate designs.
- No changelog currently available; version stability and backwards compatibility across hRUV package updates are not documented in the article.

## Evidence

- [readme] intra-batch and inter-batch replicates to estimate the unwanted variation within and between batches with RUV-III: "The tool utilises 2 types of replicates: intra-batch and inter-batch replicates to estimate the unwatned variation within and between batches with RUV-III."
- [intro] loessShort intra-batch normalisation with RUV-III and concatenate inter-batch structure: "For intra batch normalisation, we perform loess smoothing on samples and RUV-III using short replicates with parameter k set to 5... For inter batch normalisation, we perform concatenating"
- [readme] hierarchical approach to removing unwanted variation by harnessing information from sample replicates embedded in the sequence of experimental runs/batches: "Our novel tool is a novel hierarchical approach to removing unwanted variation by harnessing information from sample replicates embedded in the seequence of experimental runs/batches and applying"
- [intro] metabolites filtered with >50% missing values per batch and intersect method applied: "We have filtered metabolites with more than 50% of missing values per batch and selected metabolites that are quantified across all batches (intersect)"
- [intro] batch effects eliminated in PCA plots after normalisation: "the resulting loessShort_concatenate assay eliminates batch effects visible in PCA plots and corrects signal drift across experimental runs."
