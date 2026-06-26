---
name: feature-alignment-error-identification
description: Use when you have completed peak detection and feature alignment in metabolomic
  LC-MS processing and suspect systematic errors in peak integration or feature misalignment
  across your sample cohort.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - AVIR.R
  - R
  - e1071
  - caret
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.3c04046
  title: AVIR
evidence_spans:
- AVIR.R is a program developed to recognize computational variation among metabolic
  features in samples
- AVIR.R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_avir_cq
    doi: 10.1021/acs.analchem.3c04046
    title: AVIR
  dedup_kept_from: coll_avir_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c04046
  all_source_dois:
  - 10.1021/acs.analchem.3c04046
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-alignment-error-identification

## Summary

AVIR.R identifies data quality problems in metabolomic feature tables by recognizing computational variation patterns across metabolic features that indicate faulty peak integration or feature misalignment errors. This skill flags anomalous features and generates diagnostic reports to guide quality control of metabolomic processing pipelines.

## When to use

Apply this skill when you have completed peak detection and feature alignment in metabolomic LC-MS processing and suspect systematic errors in peak integration or feature misalignment across your sample cohort. Specifically, use it when you observe unexplained variation patterns in feature intensities that may stem from processing artifacts rather than biological variation.

## When NOT to use

- Your data is already filtered and you have validated that peak integration and alignment are correct — re-running AVIR.R will only add computational overhead without improving data quality.
- Your metabolomic data are from a single sample or a very small cohort where computational variation metrics cannot be reliably estimated across replicates.
- You have raw spectral data (mzML, netCDF) instead of a processed feature table — you must first complete peak detection and alignment steps.

## Inputs

- Peak height .csv file (rows=features, columns=samples)
- Peak area .csv file (rows=features, columns=samples)
- Metabolomics feature table in tabular format

## Outputs

- Annotated feature table with quality flags per feature
- Diagnostic report listing flagged features, variation scores, and problem categories
- Feature-level variation metrics

## How to apply

Load your metabolomics feature table (rows=features, columns=samples) into R as two separate .csv files: one containing peak heights and another containing peak areas. Install required dependencies (e1071, caret packages). Execute the AVIR.R routine to compute computational variation metrics across all metabolic features. The algorithm applies flagging logic to identify features exhibiting anomalous variation patterns that deviate from expected biological noise. Output includes quality flags assigned to each feature and a diagnostic summary categorizing problems as peak integration errors or alignment errors. Use the flagged features list to decide whether to exclude problematic features or re-process specific samples.

## Related tools

- **AVIR.R** (Core program that computes computational variation metrics and applies flagging logic to identify peak integration and alignment errors in metabolomic feature tables) — github.com/HuanLab/AVIR
- **R** (Execution environment for AVIR.R; required to run the source script via RStudio)
- **e1071** (R package dependency for statistical and machine learning functions used by AVIR.R)
- **caret** (R package dependency for classification and regression training used by AVIR.R)

## Examples

```
source('AVIR.R'); # After setting working directory to unzipped AVIR.R folder, load peak height and area CSV files and execute via Source button or CTRL+SHIFT+ENTER in RStudio
```

## Evaluation signals

- Verify that all features in the input table receive a quality flag (pass or fail) and that no features are silently dropped.
- Check that the diagnostic report contains at least one flagged feature with an assigned variation score and problem category (peak integration error or alignment error) — absence suggests the algorithm did not detect any anomalies.
- Confirm that flagged features exhibit higher computational variation across samples relative to non-flagged features, and that this variation is consistent with known processing artifacts rather than biological signal.
- Validate that re-processing or excluding flagged features results in reduced technical variation and improved reproducibility in downstream analysis (e.g., metabolite clustering, biomarker detection).
- Ensure the annotated output table matches the schema and row/column structure of the input feature table, with additional quality flag columns appended.

## Limitations

- AVIR.R relies on cross-sample variation patterns and therefore requires sufficient sample replication to estimate robust variation metrics; small cohorts or single-sample experiments will yield unreliable flagging.
- The method identifies computational variation proxies for errors but does not directly validate whether flagged features are truly erroneous without independent confirmation (e.g., manual inspection of chromatograms or orthogonal validation).
- Performance and accuracy depend on proper formatting of input .csv files (separate peak height and peak area files with consistent feature and sample naming); malformed inputs will cause execution errors or silent failures.
- The README does not specify which variation metrics (e.g., coefficient of variation, interquartile range, or machine-learning scores) are computed or how thresholds for anomaly detection are set, limiting reproducibility and tuning options.

## Evidence

- [readme] AVIR.R is a program developed to recognize computational variation among metabolic features in samples, thereby identifying problems in the data -- such as faulty peak integration or feature misalignment: "AVIR.R is a program developed to recognize computational variation among metabolic features in samples, thereby identifying problems in the data -- such as faulty peak integration or feature"
- [other] Workflow involves loading feature table, executing AVIR.R routine to compute variation metrics, applying flagging logic, generating diagnostic report, and outputting annotated feature table: "1. Load the metabolomics feature table (rows=features, columns=samples) into R. 2. Execute AVIR.R routine to compute computational variation metrics across metabolic features. 3. Apply flagging logic"
- [readme] Input file formatting requires two separate .csv files for peak height and peak area: "When adding your own datasets to be analyzed using AVIR.R, please split it into two .csv files, one with the height, and the other with the area, of the chromatographic feature peaks."
- [readme] Required R packages for AVIR.R execution: "Simply run the following code in R Studio: `install.packages('e1071')` `install.packages('caret')`"
- [intro] AVIR.R identifies problems in metabolomic data caused by metabolomic processing including faulty peak integration and feature misalignment: "AVIR.R operates by recognizing computational variation among metabolic features in samples to identify problems in metabolomic data caused by processing, including faulty peak integration and feature"
