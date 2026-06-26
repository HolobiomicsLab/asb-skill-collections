---
name: cluster-statistics-integration
description: Use when after peak clustering has been performed on aligned GCIMS samples
  and a peak table matrix has been constructed, but the matrix contains NA values
  because some samples did not yield detected peaks at certain cluster positions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0593
  tools:
  - R
  - GCIMS
  techniques:
  - GC-MS
  - ion-mobility-MS
  license_tier: restricted
  provenance_tier: literature
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.chemolab.2023.104938
  all_source_dois:
  - 10.1016/j.chemolab.2023.104938
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cluster-statistics-integration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Integrate peak cluster statistics (centroids, sizes, member assignments) into a peak table matrix to impute missing or NA values that arise from incomplete peak detection or alignment across GCIMS samples. This step bridges peak clustering output and downstream quantitative analysis by filling gaps in the peak intensity matrix using cluster-level summary statistics.

## When to use

After peak clustering has been performed on aligned GCIMS samples and a peak table matrix has been constructed, but the matrix contains NA values because some samples did not yield detected peaks at certain cluster positions. Use this skill when you need a complete, non-sparse peak table for statistical or machine-learning downstream analysis and cluster statistics (e.g., mean drift time, retention time, and intensity across cluster members) are available to guide imputation.

## When NOT to use

- Peak table is already complete (no NA values present).
- Cluster statistics are unavailable or unreliable (e.g., clusters contain only single members).
- The analysis requires explicit missing-value coding for downstream statistical testing (e.g., missing-completely-at-random analysis); imputation may violate assumptions.

## Inputs

- peak_table_matrix (numeric matrix with rows=samples, columns=clusters, containing NA values)
- GCIMSDataset object (preprocessed GCIMS dataset with aligned samples)
- cluster_stats object (cluster centroid positions and membership statistics)

## Outputs

- imputed_peak_table (numeric matrix, same dimensions as input, with all NA values filled)

## How to apply

Load the peak_table_matrix (rows = samples, columns = clusters), the GCIMSDataset object, and the cluster_stats object (containing centroid positions and cluster membership) into the R environment. Call the imputePeakTable function, passing these three objects as arguments. The function uses cluster centroids and member statistics to estimate missing peak intensities at cluster positions where a sample did not yield a direct detection. Verify post-imputation that all NA values have been replaced with numeric estimates and that the resulting matrix is dense (no remaining NAs). Export the imputed peak table as a CSV file for downstream analysis.

## Related tools

- **GCIMS** (R package providing the imputePeakTable function and data structures (GCIMSDataset, cluster_stats)) — https://github.com/sipss/GCIMS
- **R** (Runtime environment for executing imputePeakTable and matrix operations)

## Examples

```
imputed_peak_table <- imputePeakTable(peak_table_matrix, dataset, cluster_stats); write.csv(imputed_peak_table, 'imputed_peaks.csv', row.names=TRUE)
```

## Evaluation signals

- All NA values in the imputed peak table are replaced with numeric values (no remaining NAs).
- Imputed values are within the observed range of intensities in the peak table (no negative or unreasonably extreme values).
- Sample-wise and cluster-wise sums/means of imputed intensities are consistent with biological expectations (e.g., no sample shows zero total intensity after imputation).
- Comparison of pre- and post-imputation matrices shows changes only at NA positions; non-NA values are unchanged.
- Output matrix can be successfully exported to CSV without errors and retains correct dimensions (nsamples × nclusters).

## Limitations

- Imputation assumes cluster statistics are representative and stable across samples; poor cluster quality (e.g., loose or heterogeneous clusters) may yield biased estimates.
- The imputePeakTable function's algorithm is not detailed in the article; sensitivity to cluster size, centroid confidence, and distance thresholds is unknown.
- Missing values may be missing-not-at-random (e.g., systematic failures in low-intensity samples); imputation does not address this mechanism and may inflate false positives in downstream analysis.
- No changelog or versioning information is available for the GCIMS package, limiting reproducibility and traceability of changes to the imputation logic.

## Evidence

- [other] The imputePeakTable function fills NA values in the peak table matrix; the imputed peak table shows that NA values were imputed.: "The imputePeakTable function fills NA values in the peak table matrix; the imputed peak table shows that NA values were imputed."
- [other] Call imputePeakTable function with peak_table_matrix, dataset, and cluster_stats as arguments to impute missing values.: "Call imputePeakTable function with peak_table_matrix, dataset, and cluster_stats as arguments to impute missing values."
- [other] Verify that all NA values have been filled and export the resulting imputed peak table as a CSV file.: "Verify that all NA values have been filled and export the resulting imputed peak table as a CSV file."
- [readme] GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples.: "GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples."
