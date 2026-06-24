---
name: metabolomics-batch-effect-correction
description: Use when you have log-transformed, imputed metabolomics data from multiple
  experimental batches (rawImpute assay) that shows visible batch effects in PCA plots
  or signal drift across runs, and your study design includes intra-batch replicates
  (technical replicates within a run) and inter-batch.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - hRUV
  - RUV-III
  - R
  - SummarizedExperiment
  - dplyr
  license_tier: open
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

# metabolomics-batch-effect-correction

## Summary

Apply hierarchical RUV-III normalisation with intra-batch loess smoothing and inter-batch concatenate structure to remove batch effects and signal drift from multi-batch metabolomics data. This skill leverages sample replicates embedded within and across experimental runs to estimate and correct unwanted variation in SummarizedExperiment objects.

## When to use

Apply this skill when you have log-transformed, imputed metabolomics data from multiple experimental batches (rawImpute assay) that shows visible batch effects in PCA plots or signal drift across runs, and your study design includes intra-batch replicates (technical replicates within a run) and inter-batch replicates (quality control or spike-in samples across batches) that can inform RUV-III decomposition.

## When NOT to use

- Input data lacks intra-batch or inter-batch replicate samples; RUV-III requires both types to estimate unwanted variation.
- Metabolite filtering has not been performed; apply threshold filtering (>50% missing per batch) and intersect filtering before calling hRUV.
- Input assay is not log-transformed and imputed; hRUV expects rawImpute (log2-transformed and k-NN imputed) as input, not raw counts or unimputed data.

## Inputs

- SummarizedExperiment object with rawImpute assay (log-transformed and k-NN imputed)
- Batch metadata (batch assignment per sample)
- Replicate metadata (intra-batch replicate identifiers; inter-batch replicate identifiers)

## Outputs

- SummarizedExperiment object with new loessShort_concatenate assay (batch-corrected, normalised metabolite intensities)
- Batch effect correction applied to all metabolites quantified across all batches (intersect set)

## How to apply

Load a SummarizedExperiment object containing the rawImpute assay and batch/replicate metadata. Call the hRUV function with parameters: intra='loessShort' to apply non-linear smoothing within batches using RUV-III with k=5 short replicate neighbors, and inter='concatenate' to apply hierarchical inter-batch normalisation using batch replicate samples with k=5 batch replicate neighbors. Extract the resulting normalised loessShort_concatenate assay from the returned SummarizedExperiment. Evaluate success by verifying that batch structure is no longer visible in PCA plots and that signal drift across experimental runs has been corrected.

## Related tools

- **hRUV** (Core function implementing hierarchical RUV-III normalisation with intra-batch loess smoothing and inter-batch concatenate structure) — https://github.com/SydneyBioX/hRUV
- **RUV-III** (Statistical method underlying hRUV for estimating and removing unwanted variation using intra-batch and inter-batch replicate samples)
- **SummarizedExperiment** (Data container for storing assays, metadata, and batch/replicate annotations)
- **dplyr** (Tidyverse package for data manipulation and preparation of metadata)

## Examples

```
library(hRUV); dat_normalized <- hRUV(dat, intra='loessShort', inter='concatenate', intra_k=5, inter_k=5); assay(dat_normalized, 'loessShort_concatenate')
```

## Evaluation signals

- PCA plot of loessShort_concatenate assay no longer shows clustering by batch; samples cluster by biological grouping instead.
- Signal drift trend across experimental run order (batch sequence) is corrected; loess-smoothed intensity trend is flat in loessShort_concatenate vs. trending in rawImpute.
- Batch-to-batch variance (between-batch sum of squares) is reduced post-correction compared to pre-correction, quantifiable via ANOVA or batch effect variance components.
- Replicate samples (intra-batch or inter-batch) show reduced Euclidean distance in loessShort_concatenate compared to rawImpute assay.
- Metabolite abundance distributions remain stable (median, IQR unchanged); normalisation corrects systematic bias without inflating noise.

## Limitations

- Requires well-designed replicate embedding; if replicates are not strategically distributed within and across batches, RUV-III decomposition may be uninformative.
- loessShort intra-batch smoothing assumes short-range (within-run) signal drift; may not correct long-range or non-monotonic instrumental artifacts.
- Concatenate inter-batch structure assumes hierarchical batch relationships; may be suboptimal if batches are unrelated or non-sequential.
- Skill is specific to metabolomics in SummarizedExperiment format; not applicable to other data types (genomics, proteomics) without adaptation.
- No changelog or version history available; reproducibility depends on hRUV package version stability (current version tested on R 4.0.3).

## Evidence

- [full_text] After applying hruv normalisation with loessShort intra-batch and concatenate inter-batch parameters, the resulting loessShort_concatenate assay eliminates batch effects visible in PCA plots and corrects signal drift across experimental runs.: "After applying hruv normalisation with loessShort intra-batch and concatenate inter-batch parameters, the resulting loessShort_concatenate assay eliminates batch effects visible in PCA plots and"
- [full_text] Call the hRUV function with parameters: intra='loessShort' (intra-batch non-linear smoothing), inter='concatenate' (inter-batch hierarchical structure), intra_k=5 (short replicate neighbors for intra-batch RUV-III), inter_k=5 (batch replicate neighbors for inter-batch RUV-III).: "Call the hRUV function with parameters: intra='loessShort' (intra-batch non-linear smoothing), inter='concatenate' (inter-batch hierarchical structure), intra_k=5 (short replicate neighbors for"
- [readme] hRUV is a package for normalisation of multiple batches of metabolomics data in a hierarchical strategy with use of samples replicates in large-scale studies. The tool utilises 2 types of replicates: intra-batch and inter-batch replicates to estimate the unwanted variation within and between batches with RUV-III.: "hRUV is a package for normalisation of multiple batches of metabolomics data in a hierarchical strategy with use of samples replicates in large-scale studies. The tool utilises 2 types of replicates:"
- [intro] For intra batch normalisation, we perform loess smoothing on samples and RUV-III using short replicates with parameter k set to 5: "For intra batch normalisation, we perform loess smoothing on samples and RUV-III using short replicates with parameter k set to 5"
- [intro] We have filtered metabolites with more than 50% of missing values per batch and selected metabolites that are quantified across all batches (intersect): "We have filtered metabolites with more than 50% of missing values per batch and selected metabolites that are quantified across all batches (intersect)"
