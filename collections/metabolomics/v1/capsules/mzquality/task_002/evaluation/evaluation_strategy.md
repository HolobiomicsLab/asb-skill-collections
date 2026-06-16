# Evaluation Strategy

## Direct Checks

- verify that the input SummarizedExperiment object exists and is loadable from task_NNN.expected_outputs (from prior buildExperiment step)
- verify that doAnalysis function is callable from the mzQuality package (script_runs with documented default parameters: removeOutliers=TRUE, useWithinBatch=TRUE, removeBadCompounds=TRUE, qcPercentage=80, backgroundPercentage=40, nonReportableRSD=30)
- verify that the output SummarizedExperiment object contains an assay named 'ratio_corrected' (field_present)
- verify that the output SummarizedExperiment object contains column metadata with outlier annotations for QC samples (field_present)
- verify that the output SummarizedExperiment object contains column metadata with mis-injection annotations for study samples (field_present)
- verify that row count and column count of output assays are consistent with input (robust to parameter choices)

## Expert Review

- assess whether batch-correction using pooled SQC samples has been correctly applied in the 'ratio_corrected' assay by inspecting a subset of QC sample ratios before and after correction
- assess whether outlier detection thresholds (including qcPercentage=80, backgroundPercentage=40, nonReportableRSD=30) have been appropriately applied to flag QC sample outliers
- assess whether compound filtering (removeBadCompounds=TRUE) has removed only truly unreliable compounds based on the quality metrics applied
