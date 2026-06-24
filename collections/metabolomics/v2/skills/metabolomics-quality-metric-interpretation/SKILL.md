---
name: metabolomics-quality-metric-interpretation
description: Use when after batch correction of metabolomics data using pooled study
  quality control (SQC) samples and calculation of compound/internal standard ratios,
  when you need to decide which compounds are reliable for reporting and which internal
  standard minimizes technical variation (RSDQC) for each.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzQuality
  - mzQualityDashboard
  - SummarizedExperiment
  license_tier: restricted
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- mzQuality is a user-friendly R package
- mzQuality requires a specific format for the input data.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzquality
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00073
  all_source_dois:
  - 10.1021/jasms.5c00073
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-quality-metric-interpretation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Interpret and apply quality control metrics (RSDQC, background signal percentage, matrix effect, presence in QC samples) to identify reliable compounds and internal standards in batch-corrected metabolomics data. This skill enables filtering of unreliable compounds and selection of optimal internal standards based on quantitative thresholds.

## When to use

After batch correction of metabolomics data using pooled study quality control (SQC) samples and calculation of compound/internal standard ratios, when you need to decide which compounds are reliable for reporting and which internal standard minimizes technical variation (RSDQC) for each compound.

## When NOT to use

- When batch correction has not yet been performed on QC samples—apply batch correction first using pooled SQC samples.
- When no internal standard candidates have been assigned to compounds—assign internal standards before calculating RSDQC.
- When working with non-QC sample types only (e.g., study samples alone)—RSDQC interpretation requires QC replicates to assess technical variation.

## Inputs

- Batch-corrected SummarizedExperiment object with assays containing compound/internal standard ratios
- QC sample metadata in colData slot
- Calculated quality metrics in rowData and assays (RSDQC, background signal %, matrix effect, presence counts)

## Outputs

- Internal standard recommendation table (compound × recommended IS × minimum RSDQC)
- Updated SummarizedExperiment with use column in rowData (TRUE/FALSE for each compound)
- Filtered compound set meeting quality thresholds

## How to apply

Load the batch-corrected SummarizedExperiment object containing QC sample ratios and calculated quality metrics (RSDQC, background signal percentage, matrix effect, presence). For each compound, examine the RSDQC values across all internal standard candidates and identify the internal standard yielding the minimum RSDQC as the recommended choice. Simultaneously apply compound-level filters: mark compounds as reliable (use = TRUE) if they meet configurable thresholds for RSDQC (default typically < 30%), background signal percentage, and presence in QC samples. Conversely, set use = FALSE for compounds failing these criteria. These thresholds are user-configurable in the doAnalysis function and should be tuned based on your analytical goals and data characteristics. Export a recommendation table listing each compound, its recommended internal standard, and corresponding minimum RSDQC value.

## Related tools

- **mzQuality** (Primary R package that exhaustively calculates RSDQC values across all internal standard candidates and flags compounds as reliable or unreliable based on quality thresholds) — https://github.com/hankemeierlab/mzQuality
- **mzQualityDashboard** (Interactive Shiny application providing visual interface for interpreting quality metrics and manually overriding compound/sample selection without requiring R programming) — https://github.com/hankemeierlab/mzQualityDashboard
- **SummarizedExperiment** (Bioconductor data structure storing batch-corrected assays, rowData (compound metadata including quality flags), and colData (sample metadata including outlier flags)) — https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html
- **R** (Runtime environment for executing mzQuality analyses and custom quality metric filtering workflows)

## Examples

```
exp <- doAnalysis(exp = exp); filtered_exp <- exp[rowData(exp)$use, exp$use]; recommendation_table <- data.frame(Compound = rownames(filtered_exp), RecommendedIS = rowData(filtered_exp)$internal_standard, MinRSDQC = rowData(filtered_exp)$RSDQC)
```

## Evaluation signals

- RSDQC values are monotonically non-negative and bounded; for each compound, exactly one internal standard is flagged as recommended (minimum RSDQC across candidates).
- The use column in rowData contains only TRUE/FALSE values; compounds marked FALSE fail at least one of the three quality thresholds (RSDQC, background %, presence).
- Recommended internal standards are present in the input internal standard candidate list for each compound; no NAs or out-of-scope internal standards appear.
- Subsetting the experiment using exp[rowData(exp)$use, exp$use] produces a filtered dataset with higher median RSDQC values than the original, confirming that removed compounds had worse technical variation.
- For manual overrides, the use column matches user-specified TRUE/FALSE assignments, and export tables reflect the selected compound set.

## Limitations

- In the current version of mzQuality, only one sample type can be used for calculating concentrations; multiple sample types require sequential runs or external merging.
- RSDQC thresholds are heuristic defaults (typically RSD < 30%, background signal < threshold, presence in QC samples); thresholds must be manually tuned per study and may not generalize across different metabolomics platforms or matrices.
- Interpretation assumes QC samples are truly representative and that batch correction using SQC samples has been performed correctly; biased QC selection or incomplete batch correction will compromise internal standard recommendations.
- The Rosner Test for sample outlier detection in QC samples may be sensitive to sample size and distributional assumptions; outlier flagging should be visually inspected in diagnostic plots.

## Evidence

- [other] mzQuality exhaustively calculates RSDQC values of batch-corrected ratios across all internal standard candidates for each compound and identifies the internal standard yielding the lowest RSDQC as the recommended choice.: "mzQuality exhaustively calculates RSDQC values of batch-corrected ratios across all internal standard candidates for each compound and identifies the internal standard yielding the lowest RSDQC as"
- [readme] It bases the decision for compounds on the combination of RSDQC, the background signal percentage, and the presence of the compounds in QC samples. The thresholds for these values can be set in doAnalysis.: "It bases the decision for compounds on the combination of RSDQC, the background signal percentage, and the presence of the compounds in QC samples. The thresholds for these values can be set in"
- [readme] mzQuality adds a column called use in both the rowData and colData slots of the SummarizedExperiment. These contain either a TRUE or FALSE value, indicating if the compound or sample is reliable for reporting based on the set thresholds.: "mzQuality adds a column called use in both the rowData and colData slots of the SummarizedExperiment. These contain either a TRUE or FALSE value, indicating if the compound or sample is reliable for"
- [intro] mzQuality is capable of recommending different internal standards by exhaustively calculating the Relative Standard Deviation of QC samples (RSDQC) of batch-corrected ratio's.: "mzQuality is capable of recommending different internal standards by exhaustively calculating the Relative Standard Deviation of QC samples (RSDQC) of batch-corrected ratio's."
- [readme] The doAnalysis function will perform the following steps: 1. Calculate the ratio between the compounds and assigned internal standards, 2. Perform batch correction using the pooled study quality control samples (SQC), 3. Calculate the percentage of background signal compared to the study samples, 4. Calculate the matrix effect, 5. Calculate the ratio of the QC sample, 6. Calculate the presence of the compounds in the samples, 7. Calculate the median area of the compounds in the samples, 8. Suggest Internal Standards based on the calculated values.: "The doAnalysis function will perform the following steps: 1. Calculate the ratio between the compounds and assigned internal standards, 2. Perform batch correction using the pooled study quality"
