---
name: metabolite-feature-filtering-by-missingness
description: Use when you have a raw metabolite abundance matrix (e.g., from MSPrep or another LC-MS/MS pipeline) with many features and samples, and you observe that a substantial fraction of metabolites are missing (NA or zero-valued) across replicates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MSPrep
  - Bioconductor
  - marr
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1186/s12859-021-04336-9
  title: marr
- doi: 10.1080/01621459.2017.1397521
  title: ''
evidence_spans:
- 'marr: An R/Bioconductor package for Maximum Rank Reproducibility'
- The R-package **marr** can be installed from GitHub using the R package [devtools]
- The **msprepCOPD** data in the **marr** package was pre-processed using the MSPrep software
- '`marr`: An R/Bioconductor package for Maximum Rank Reproducibility'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_marr_cq
    doi: 10.1186/s12859-021-04336-9
    title: marr
  dedup_kept_from: coll_marr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-021-04336-9
  all_source_dois:
  - 10.1186/s12859-021-04336-9
  - 10.1080/01621459.2017.1397521
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-feature-filtering-by-missingness

## Summary

Remove metabolite features from a high-dimensional abundance matrix that exceed a missingness threshold (typically 80%), reducing noise and improving feature quality for downstream reproducibility and statistical analysis. This filtering step is a standard preprocessing gate in mass spectrometry–based metabolomics workflows.

## When to use

Apply this skill when you have a raw metabolite abundance matrix (e.g., from MSPrep or another LC-MS/MS pipeline) with many features and samples, and you observe that a substantial fraction of metabolites are missing (NA or zero-valued) across replicates. Use it to reduce the feature set before imputation, normalization, or reproducibility assessment—especially when replicate count is small (e.g., 20 replicates) and you want to retain only well-represented metabolites. Typical trigger: raw feature count is much higher than expected (e.g., 662 metabolites) and metabolite detection rates vary widely across the feature set.

## When NOT to use

- Input is already a pre-filtered or curated feature table (e.g., from a published metabolite panel); re-filtering may discard validated signals.
- Missingness is sparse and random (not systematic); aggressive filtering may remove true low-abundance features and bias downstream analysis.
- You have no prior knowledge of appropriate missingness threshold for your assay type or study design; blindly applying 80% may be arbitrary.

## Inputs

- Raw metabolite abundance matrix (SummarizedExperiment assay with metabolites as rows, samples as columns)
- Metabolite identifiers
- Sample annotations and metadata
- Missingness threshold value (e.g., 0.80 for 80%)

## Outputs

- Filtered metabolite abundance matrix with reduced feature count
- Filtered metabolite identifiers
- Log of removed metabolites and their missingness rates
- Summary statistics: original feature count, final feature count, number and percentage of features removed

## How to apply

Load the raw metabolite abundance matrix (rows = metabolites, columns = samples) from a SummarizedExperiment or data frame. Calculate the proportion of missing values (NA, zero, or per-protocol convention) for each metabolite across all samples. Set a missingness threshold—commonly 80%—and identify metabolites that exceed it. Retain only metabolites with ≤80% missingness (equivalently, present in ≥20% of samples; for 20 replicates, ≥4 samples). Remove all metabolites exceeding the threshold and output the filtered abundance matrix with metabolite identifiers and sample annotations preserved. The rationale is to eliminate sparse, poorly-detected features that are unlikely to be reproducible or biologically informative, while retaining a compact set of well-measured metabolites for downstream analysis.

## Related tools

- **MSPrep** (Upstream software for metabolite detection and abundance quantification; produces the raw matrix to be filtered)
- **marr** (R/Bioconductor package for maximum rank reproducibility assessment; filtering is a preprocessing step before marr reproducibility analysis) — https://github.com/Ghoshlab/marr
- **R** (Language and environment for matrix manipulation, NA/zero detection, threshold computation, and filtering logic)
- **Bioconductor** (Framework providing SummarizedExperiment class for structured metabolite data; enables standardized filtering workflows)

## Examples

```
# Load raw msprepCOPD data and filter metabolites with >80% missingness
library(marr)
data(msprepCOPD)
raw_matrix <- assay(msprepCOPD)
miss_prop <- colSums(is.na(raw_matrix)) / nrow(raw_matrix)
retain_idx <- which(miss_prop <= 0.80)
filtered_matrix <- raw_matrix[, retain_idx]
cat(sprintf("Filtered: %d -> %d metabolites\n", ncol(raw_matrix), ncol(filtered_matrix)))
```

## Evaluation signals

- Output feature count is less than input feature count; log shows X metabolites removed.
- All remaining metabolites have ≤80% missingness (or ≥20% detection rate); spot-check a sample of features to verify.
- No metabolites with >80% missingness remain in filtered matrix; missingness histogram or summary shows max ≤80%.
- Filtered matrix dimensions match expected reduction (e.g., 662 → 645 metabolites, 17 removed = 2.6%).
- Sample and metabolite metadata are intact and aligned with filtered feature indices; no off-by-one or index mismatches.

## Limitations

- Threshold of 80% missingness is conventional but not universal; different assay platforms, sample types, or study designs may justify different cutoffs (e.g., 70%, 90%), and the choice is not formally justified in the article.
- Filtering assumes that missingness is random or assay-driven, not biological; if metabolites are genuinely absent in certain sample classes, aggressive filtering may bias phenotypic inference.
- Does not impute or estimate missing values; works only on detection presence/absence. Subsequent imputation (e.g., via BPCA) is a separate step.
- Binary filtering (retain vs. remove) is not adaptive per metabolite or per sample pair; soft-weighting or probabilistic approaches are not considered.
- Small replicate counts (e.g., 20 samples) make missingness estimates noisy; a feature truly present at 15% detection may be stochastically removed or retained.

## Evidence

- [other] The MSPrep filtering step removes metabolites exceeding 80% missingness, reducing the raw metabolite count from 662 to 645 (a loss of 17 metabolites or 2.6% of features).: "The MSPrep filtering step removes metabolites exceeding 80% missingness, reducing the raw metabolite count from 662 to 645 (a loss of 17 metabolites or 2.6% of features)."
- [other] Identify and retain only metabolites with ≤80% missingness (i.e., present in ≥20% of samples, or equivalently ≥4 of 20 samples).: "Identify and retain only metabolites with ≤80% missingness (i.e., present in ≥20% of samples, or equivalently ≥4 of 20 samples)."
- [intro] Filtering: Metabolites are removed if they are missing more than 80% of the samples: "Filtering: Metabolites are removed if they are missing more than 80% of the samples"
- [other] Calculate the proportion of missing values (NA or zero, depending on MSPrep convention) for each metabolite across all 20 samples.: "Calculate the proportion of missing values (NA or zero, depending on MSPrep convention) for each metabolite across all 20 samples."
- [other] Output the filtered abundance matrix with metabolite identifiers and sample annotations preserved.: "Output the filtered abundance matrix with metabolite identifiers and sample annotations preserved."
