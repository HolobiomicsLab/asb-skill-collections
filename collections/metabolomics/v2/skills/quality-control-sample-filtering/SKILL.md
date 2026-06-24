---
name: quality-control-sample-filtering
description: Use when after building a SummarizedExperiment from metabolomics measurements
  but before batch correction and internal standard recommendation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3172
  tools:
  - R
  - mzQuality
  - SummarizedExperiment
  license_tier: open
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- library(mzQuality)
- knitr::rmarkdown, library(mzQuality)
- mzQuality requires a specific format for the input data.
- mzQuality requires a specific format for the input data
- The `buildExperiment` function will then take the data and create an experiment
  object that can be used for analysis.
- Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store
  the data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_margherita_cq
    doi: 10.1101/2024.06.20.599545v1
    title: MargheRita
  - build: coll_mzquality_cq
    doi: 10.1021/jasms.5c00073
    title: mzquality
  dedup_kept_from: coll_mzquality_cq
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

# quality-control-sample-filtering

## Summary

Identify and remove outlier pooled quality control (QC) samples and mis-injected study samples based on statistical tests and internal standard areas in metabolomics experiments. This skill ensures only reliable QC samples are retained for batch correction and compound reliability assessment.

## When to use

After building a SummarizedExperiment from metabolomics measurements but before batch correction and internal standard recommendation. Apply this skill when your dataset contains pooled QC samples (type='QC') and you need to detect statistical outliers in compound/internal-standard ratios or mis-injected study samples with anomalous internal standard peak areas.

## When NOT to use

- Input does not contain pooled QC samples or internal standard measurements—filtering requires replicate QC data to establish the distribution against which outliers are detected.
- Study design lacks internal standard spiking—mis-injection detection via internal standard areas cannot be performed.
- All samples are already pre-filtered externally or the experiment is a single-point measurement with no QC replicates.

## Inputs

- SummarizedExperiment object with assays including 'ratio' (compound/internal-standard)
- colData containing 'type' column (values: 'QC', 'Study Sample', etc.)
- colData containing internal standard area measurements

## Outputs

- SummarizedExperiment with updated colData 'use' column (TRUE/FALSE per sample)
- Rosner Test statistics and p-values (in colData or diagnostic output)

## How to apply

The mzQuality package applies the Rosner Test to detect statistical outliers in QC samples based on their compound/internal-standard ratios, and independently tests study samples for mis-injections using their internal standard areas. These thresholds can be configured in the doAnalysis function. Samples flagged as outliers are marked with FALSE in the colData 'use' column. Examine the ratio distribution across QC samples and internal standard areas for study samples to understand which samples were filtered and why. Subset the experiment using exp[rowData(exp)$use, exp$use] to retain only reliable compounds and samples. The rationale is that outlier QC samples skew batch correction models and unreliable study samples inflate false positives in downstream reporting.

## Related tools

- **mzQuality** (Performs Rosner Test on QC sample ratios and internal standard area checks; marks unreliable samples in colData 'use' column via doAnalysis function) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Container object storing sample metadata (colData) and assay measurements (ratio, internal standard areas); filtering updates the 'use' flag in colData) — https://bioconductor.org/packages/release/bioc/html/SummarizedExperiment.html
- **R** (Execution environment for mzQuality Rosner Test implementation and subsetting operations)

## Examples

```
exp <- doAnalysis(exp = exp); exp_filtered <- exp[rowData(exp)$use, exp$use]
```

## Evaluation signals

- Verify colData 'use' column contains only TRUE/FALSE values and no NAs after filtering; count of FALSE entries should match suspected outliers.
- Compare distributions of compound/internal-standard ratios before and after filtering—outlier-removed QC samples should lie outside mean ± 3σ of retained QC distribution.
- Confirm internal standard peak areas for flagged study samples are visibly anomalous (e.g., near detection limit or saturated) compared to the majority of study samples.
- Check that retained QC samples form a tight, unimodal distribution suitable for batch correction—if multimodal or heavily skewed, re-examine filtering thresholds.
- Validate that the number of samples marked FALSE is consistent with the Rosner Test significance threshold (e.g., α=0.05); document how many outliers were removed per sample type.

## Limitations

- Rosner Test assumes approximately normal distribution of ratios within QC samples; heavily skewed or multimodal distributions may cause false positives or negatives.
- The method is sensitive to the choice of significance threshold (α) and the number of outliers expected; no guidance is provided in the article for threshold selection beyond 'can be set in doAnalysis'.
- Filtering relies on having sufficient QC replicates; very small numbers of QC samples (e.g., <3) may be insufficient for robust outlier detection.
- Internal standard mis-injection detection only works when internal standards are present and their peak areas vary systematically with injection quality; detection may fail if internal standard response is extremely robust to injection failure.

## Evidence

- [intro] Rosner Test outlier detection in QC samples: "The package tests samples for outliers, specifically for (Pooled) Quality Control (QC) samples using their Compound / Internal Standard ratio"
- [intro] Study sample mis-injection detection: "Study Samples are tested for mis-injections using their Internal Standard areas"
- [other] Sample reliability flagging and subsetting: "mzQuality adds a column called `use` in both the `rowData` and `colData` slots of the SummarizedExperiment. These contain either a `TRUE` or `FALSE` value, indicating if the compound or sample is"
- [other] Outlier-based filtering rationale: "It bases the decision for compounds on the combination of RSDQC, the background signal percentage, and the presence of the compounds in QC samples. The thresholds for these values can be set in"
- [readme] Subsetting workflow: "To retrieve the compounds and samples recommended by mzQuality, you can use the following code to subset the experiment: exp <- exp[rowData(exp)$use, exp$use]"
