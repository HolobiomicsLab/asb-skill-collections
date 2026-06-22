---
name: internal-standard-area-aberrancy-flagging
description: Use when after building a SummarizedExperiment from metabolomics data but before quantitative analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - mzQuality
  - R
  - SummarizedExperiment
derived_from:
- doi: 10.1021/jasms.5c00073
  title: mzquality
evidence_spans:
- mzQuality requires a specific format for the input data.
- mzQuality requires a specific format for the input data
- library(mzQuality)
- knitr::rmarkdown, library(mzQuality)
- The `buildExperiment` function will then take the data and create an experiment object that can be used for analysis.
- Internally, mzQuality uses Bioconductors' *SummarizedExperiment* object to store the data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# internal-standard-area-aberrancy-flagging

## Summary

Detection and flagging of mis-injected or otherwise compromised study samples by identifying anomalies in internal standard peak areas within a metabolomics SummarizedExperiment object. This skill isolates samples with aberrant internal standard signals that indicate technical failure and should be excluded from downstream analysis.

## When to use

After building a SummarizedExperiment from metabolomics data but before quantitative analysis. Apply this skill when you need to identify study samples with internal standard areas that deviate significantly from the population mean—a sign of mis-injection, instrument drift, or ionization failure—to prevent unreliable samples from biasing compound quantification or batch correction.

## When NOT to use

- Internal standards have not been assigned or spiked into samples.
- Study design intentionally varies internal standard amounts across samples.
- Input data is already filtered and QC flags have been manually validated by a domain expert.

## Inputs

- SummarizedExperiment object with assays containing internal standard peak areas
- colData with sample metadata (type, batch, injection information)
- Explicit internal standard identifiers in rowData

## Outputs

- SummarizedExperiment with use=FALSE flag in colData for aberrant samples
- Tabulated list of flagged study samples with internal standard areas and metadata
- Diagnostic plots showing internal standard area distribution and outlier positions

## How to apply

Call doAnalysis on the SummarizedExperiment with removeOutliers=TRUE to activate outlier detection. The function calculates internal standard peak areas across all samples and applies statistical tests (Rosner Test) to identify study samples with aberrant internal standard areas. Samples flagged as outliers are marked with use=FALSE in the colData slot. Extract flagged samples by subsetting the experiment with exp[, !exp$use] and tabulate their internal standard values alongside batch, type, and injection metadata to confirm technical failure rather than biological signal. The rationale is that internal standards are spiked at constant amounts; large deviations indicate instrumental or injection error, not sample variation.

## Related tools

- **mzQuality** (R package that implements doAnalysis function with removeOutliers=TRUE; performs Rosner Test on internal standard areas and flags aberrant study samples) — https://github.com/hankemeierlab/mzQuality
- **SummarizedExperiment** (Bioconductor container object storing assay matrices (peak areas), rowData (compound/standard annotations), and colData (sample metadata and QC flags))
- **R** (Runtime environment for executing mzQuality workflows and extracting flagged samples)

## Examples

```
exp <- doAnalysis(exp = exp, removeOutliers = TRUE); flagged_samples <- exp[, !exp$use]; write.table(as.data.frame(colData(flagged_samples)), file = 'flagged_outliers.tsv', sep = '\t', row.names = TRUE)
```

## Evaluation signals

- Flagged samples have internal standard areas >2–3 standard deviations from the batch median, confirmed by boxplot or violin plot of internal standard assay stratified by batch and type.
- use column in colData contains FALSE for all flagged samples; TRUE for retained samples; no NA values.
- Tabulated outlier report shows internal standard area values alongside batch and type; visual inspection confirms deviations are technical (e.g., all flagged samples from a single injection day or instrument state) rather than random.
- Subsetting exp[, exp$use] reduces sample count and removes the identified outliers; downstream PCA or batch correction plots show tighter clustering without flagged samples.
- No reportable compounds are removed solely due to internal standard flagging; the filtering affects only colData, not rowData.

## Limitations

- Rosner Test assumes approximately normal distribution of internal standard areas within each batch; highly skewed or multi-modal distributions may yield false positives or false negatives.
- Flagging threshold is controlled by removeOutliers=TRUE/FALSE and applies globally; no per-batch or per-compound-class tuning of sensitivity in the standard doAnalysis call.
- Internal standards must be correctly identified in rowData; mislabeled or absent internal standard annotations will prevent the skill from detecting aberrancy.
- Study samples with genuinely low internal standard signal (e.g., very low concentration, high matrix suppression in a specific aliquot type) may be incorrectly flagged as mis-injected rather than biologically real.

## Evidence

- [intro] Study Samples are tested for mis-injections using their Internal Standard areas: "Study Samples are tested for mis-injections using their Internal Standard areas"
- [other] doAnalysis flags QC outliers by Compound/Internal Standard ratio, detects mis-injected Study Samples via Internal Standard areas, and removes bad compounds when called with removeOutliers=TRUE: "detects mis-injected Study Samples via Internal Standard areas, and removes bad compounds when called with removeOutliers=TRUE"
- [other] Extract and tabulate flagged outlier samples (QC and study samples with aberrant Compound/Internal Standard ratios or internal standard areas): "Extract and tabulate flagged outlier samples (QC and study samples with aberrant Compound/Internal Standard ratios or internal standard areas)"
- [readme] For samples, this is based on the outcome of the Rosner Test, which tests for statistical outliers in QC samples: "For samples, this is based on the outcome of the Rosner Test, which tests for statistical outliers in QC samples"
- [readme] mzQuality adds a column called `use` in both the `rowData` and `colData` slots of the SummarizedExperiment. These contain either a `TRUE` or `FALSE` value, indicating if the compound or sample is reliable for reporting: "mzQuality adds a column called `use` in both the `rowData` and `colData` slots of the SummarizedExperiment. These contain either a `TRUE` or `FALSE` value, indicating if the compound or sample is"
