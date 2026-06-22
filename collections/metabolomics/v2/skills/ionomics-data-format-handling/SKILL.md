---
name: ionomics-data-format-handling
description: Use when you have raw ICP-MS ion concentration measurements (e.g., Ca44, Cd111, Fe56, Zn66 in ppm) organized as a data frame with multiple replicates per sample and batch identifiers, and you need to prepare this for ionomics analysis in Galaxy or the IonFlow R package.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3071
  tools:
  - R
  - ionflow
  - IonFlow R package
  - Galaxy
  - R (base, stats)
derived_from:
- doi: 10.1007/s11306-021-01841-z
  title: IonFlow
evidence_spans:
- based on the modification of R package
- github.com__wanchanglin__ionflow
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ionflow_cq
    doi: 10.1007/s11306-021-01841-z
    title: IonFlow
  dedup_kept_from: coll_ionflow_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-021-01841-z
  all_source_dois:
  - 10.1007/s11306-021-01841-z
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ionomics-data-format-handling

## Summary

Convert raw ICP-MS ionomics datasets (ion concentration tables with replicates and batch identifiers) into standardized tabular formats suitable for Galaxy tool ingestion and downstream statistical analysis. This skill ensures data integrity through outlier detection, batch effect correction, and format validation before exploratory and clustering workflows.

## When to use

You have raw ICP-MS ion concentration measurements (e.g., Ca44, Cd111, Fe56, Zn66 in ppm) organized as a data frame with multiple replicates per sample and batch identifiers, and you need to prepare this for ionomics analysis in Galaxy or the IonFlow R package. Triggers include: data contains extreme outliers (values > Q3 + 3*IQ or < Q1 - 3*IQ), batch effects are present across measurement runs, or you are transitioning from raw instrument output to reproducible workflow input.

## When NOT to use

- Data is already normalized or log-transformed by instrument software — applying preprocessing again risks double-transformation and loss of biological signal.
- Input lacks batch identifiers or control strain replicates — median batch correction requires batch-level structure; apply with caution if batches are unknown.
- Analysis goal requires preservation of rare extreme values (e.g., phenotypic extremes in mutant screens) — outlier flagging may discard biologically meaningful variants.

## Inputs

- Raw ICP-MS data frame: numeric ion concentration table (ions as columns, samples as rows, values in ppm)
- Sample metadata: batch identifiers, replicate counts, optional pre-defined standard deviations for ions

## Outputs

- Cleaned ionomics dataset: log-transformed, batch-corrected, outlier-flagged tabular data (TSV/CSV)
- Summary statistics: outlier counts per ion, raw vs. corrected data distributions, batch correction factors
- QC report: outlier list, batch effect magnitude, variance reduction metrics

## How to apply

Begin by inspecting raw data frame structure (ion columns, sample rows, replicate and batch metadata) using `data(IonData)` or equivalent load. Run the PreProcessing function from IonFlow, which applies three sequential steps: (1) outlier detection using interquartile range fencing (outer fences at Q1 - 3*IQ and Q3 + 3*IQ) to flag extreme values per ion, (2) logarithmic transformation of concentration values to stabilize variance across the wide dynamic range typical of ionomics (e.g., Ca 0.449–902.568 ppm vs Co 0.007–0.702 ppm), and (3) median batch correction by scaling log-transformed ion concentrations to the median within each batch to remove systematic instrument drift. Validate output by confirming that corrected data show median = 0 and reduced variance relative to raw data (e.g., variance drops from 829.525 to 0.084 for Ca). Export the cleaned dataset as a tabular file (TSV or CSV) with ions as columns, samples as rows, and metadata columns retained for downstream Galaxy tool ingestion.

## Related tools

- **IonFlow R package** (Executes PreProcessing function for outlier detection, log transformation, and median batch correction of raw ionomics data) — https://github.com/AlinaPeluso/MetaboFlow
- **Galaxy** (Ingests preprocessed tabular ionomics data and exposes downstream analysis workflows (clustering, network analysis, GO enrichment)) — https://github.com/wanchanglin/ionflow
- **R (base, stats)** (Provides data frame manipulation, quantile computation for outlier fencing (Q1, Q3, IQR), and log/scale transformations)

## Examples

```
devtools::install_github("AlinaPeluso/MetaboFlow", subdir="IonFlow"); library(IonFlow); data(IonData); pre_proc <- PreProcessing(data=IonData, stdev=pre_defined_sd); write.csv(pre_proc$median_batch_corrected_data, file="ionflow_cleaned.csv")
```

## Evaluation signals

- Cleaned dataset median = 0 for all ions after batch correction; raw data median ≠ 0 confirms correction was applied.
- Variance of corrected data is substantially lower than raw data (e.g., Ca variance decreases from 829.525 to 0.084); confirms stabilization across batch and ion range.
- Outlier report shows < 1–2% of values flagged per ion; anomalously high outlier rates (> 5%) suggest data quality issues or misspecified fencing parameters.
- Log-transformed values span a comparable range across ions (e.g., all centered near 0 ± 2 after correction) despite raw dynamic range differences; confirms normalization success.
- No missing values introduced during preprocessing; verify row and column counts match input.

## Limitations

- Outlier fencing (Q1 - 3*IQ, Q3 + 3*IQ) is sensitive to data distribution; highly skewed ion measurements may require distribution-specific thresholds (e.g., robust MAD or Huber loss) not documented in article.
- Median batch correction assumes batches are balanced (similar sample counts per batch); extreme batch imbalance may bias correction factors.
- Log transformation undefined for zero or negative concentrations; if raw data contain non-detects or negative values, prior imputation or pseudo-count addition is required.
- Preprocessing output is deterministic given a single raw dataset; reproducibility across instruments or labs requires unified calibration and control strain handling.
- No changelog available in repository; version compatibility between IonFlow R package and Galaxy wrapper versions not explicitly tracked.

## Evidence

- [readme] Outlier detection approach: "We define a lower outer fence: `Q1 - 3*IQ` and a upper outer fence: `Q3 + 3*IQ` where `Q1` and `Q3` are the first and the third quantile of the distribution, respectively."
- [readme] Log transformation and batch correction: "First we take the logarithmm of the concentration value. Then, the data are scaled to the median taken for each ion within each batch."
- [readme] Data format and ion types: "We illustrate the Ionomics workflow with ICP-MS data of yeast intracellular ion concentrations measured for 1454 single-gene haploid knockouts. Ions measured include Ca44, Cd111, Co59, Cu65, Fe56,"
- [readme] PreProcessing function input/output: "This section requires as input the raw data frame, e.g. ion's concentrations. It is also possible to define a set of ion's standard deviation, as these are possibly computed accounting for some"
- [other] Galaxy wrapper implementation: "Galaxy tool for processing and analysis of ionomics data , based on the modification of R package IonFlow"
