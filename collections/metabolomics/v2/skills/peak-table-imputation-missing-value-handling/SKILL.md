---
name: peak-table-imputation-missing-value-handling
description: Use when after peak clustering in a GCIMS preprocessing pipeline, when the peak table matrix contains NA values corresponding to peaks detected in some samples but not others, and you have computed cluster statistics that characterize each peak cluster's properties.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  tools:
  - R
  - GCIMS
derived_from:
- doi: 10.1016/j.chemolab.2023.104938
  title: GCIMS
evidence_spans:
- library(ggplot2) library(cowplot) library(GCIMS)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gcims_cq
    doi: 10.1016/j.chemolab.2023.104938
    title: GCIMS
  dedup_kept_from: coll_gcims_cq
schema_version: 0.2.0
---

# peak-table-imputation-missing-value-handling

## Summary

Imputes NA values in GCIMS peak table matrices using cluster statistics to fill missing intensity measurements. This step is essential after peak clustering to ensure a complete, analyzable peak intensity matrix for downstream statistical analysis.

## When to use

After peak clustering in a GCIMS preprocessing pipeline, when the peak table matrix contains NA values corresponding to peaks detected in some samples but not others, and you have computed cluster statistics that characterize each peak cluster's properties.

## When NOT to use

- Input peak table is already complete with no NA values present.
- Cluster statistics have not yet been computed or are unavailable.
- The research question requires preservation of missing-value patterns for dropout analysis or missingness-dependent weighting.

## Inputs

- peak_table_matrix (numeric matrix with samples as rows, peak clusters as columns, containing NA values)
- GCIMSDataset object (the preprocessed GCIMS sample collection with metadata)
- cluster_stats (statistics computed from peak clustering, e.g., cluster centroids and characteristics)

## Outputs

- imputed_peak_table (numeric matrix with all NA values filled, same dimensions as input)
- CSV export of imputed peak table (for downstream analysis or archival)

## How to apply

Load the peak_table_matrix (rows = samples, columns = peak clusters), the GCIMSDataset object, and cluster_stats into the R environment. Call the imputePeakTable function with these three arguments. The function uses cluster statistics (e.g., mean intensity, retention time, drift time properties per cluster) to impute biologically plausible values for missing peaks, replacing NA entries with estimated intensities. Verify that all NA values have been filled in the resulting matrix before exporting. The imputation leverages delayed evaluation where possible to minimize memory usage, consistent with GCIMS design principles.

## Related tools

- **GCIMS** (R package providing the imputePeakTable function and peak clustering infrastructure) — https://github.com/sipss/GCIMS
- **R** (Programming environment for calling imputePeakTable and handling matrix operations)

## Examples

```
imputePeakTable(peak_table_matrix, dataset, cluster_stats)
```

## Evaluation signals

- All NA values in the output peak table are replaced with numeric values; no NA cells remain.
- Output matrix has identical dimensions (samples × clusters) to the input peak table.
- Imputed values fall within plausible intensity ranges observed in non-missing entries of the peak table.
- Summary statistics (mean, median, distribution) of imputed columns are consistent with unimputed columns from the same cluster.
- Exported CSV file is readable and contains no missing values in the intensity columns.

## Limitations

- Imputation quality depends on the accuracy and representativeness of cluster statistics; clusters with few observations may produce less reliable imputations.
- The method assumes that missingness is not informative (i.e., NA values do not encode a distinct biological signal); if peak absence is meaningful, imputation may introduce bias.
- No guidance is provided in the article regarding sensitivity of downstream analyses to imputation method choice or robustness checks.

## Evidence

- [other] Does the imputePeakTable function successfully fill NA values in the peak table matrix when provided with the dataset and cluster statistics?: "Does the imputePeakTable function successfully fill NA values in the peak table matrix when provided with the dataset and cluster statistics?"
- [other] The imputePeakTable function fills NA values in the peak table matrix; the imputed peak table shows that NA values were imputed.: "The imputePeakTable function fills NA values in the peak table matrix; the imputed peak table shows that NA values were imputed."
- [other] Call imputePeakTable function with peak_table_matrix, dataset, and cluster_stats as arguments to impute missing values.: "Call imputePeakTable function with peak_table_matrix, dataset, and cluster_stats as arguments to impute missing values."
- [intro] GCIMS uses delayed evaluations were possible, so dataset modifications can be executed in a more efficient way and without using too much RAM.: "GCIMS uses delayed evaluations were possible, so dataset modifications can be executed in a more efficient way and without using too much RAM."
- [other] Verify that all NA values have been filled and export the resulting imputed peak table as a CSV file.: "Verify that all NA values have been filled and export the resulting imputed peak table as a CSV file."
