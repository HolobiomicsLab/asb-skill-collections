---
name: peak-integration-quality-assessment
description: Use when you have a metabolomic feature table (rows=features, columns=samples) with peak height and peak area measurements from chromatographic processing, and you suspect data quality issues such as misaligned features or erratic peak integration across your sample cohort.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - AVIR.R
  - R
derived_from:
- doi: 10.1021/acs.analchem.3c04046
  title: AVIR
evidence_spans:
- AVIR.R is a program developed to recognize computational variation among metabolic features in samples
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
---

# peak-integration-quality-assessment

## Summary

AVIR.R is a computational method that detects anomalous variation patterns in metabolomic feature tables to identify data quality problems caused by faulty peak integration or feature misalignment during metabolomic processing. It flags problematic features by computing variation metrics across samples and applying diagnostic logic to isolate integration errors.

## When to use

Apply this skill when you have a metabolomic feature table (rows=features, columns=samples) with peak height and peak area measurements from chromatographic processing, and you suspect data quality issues such as misaligned features or erratic peak integration across your sample cohort. Use it as a post-processing diagnostic before downstream statistical or metabolic analysis.

## When NOT to use

- Input data are already manually curated or quality-filtered for peak integration artifacts.
- Feature table is from non-chromatographic platforms (e.g., direct infusion MS) where peak height/area integration errors are not relevant.
- Raw, unprocessed chromatographic data (mzML, netCDF) rather than extracted feature tables.

## Inputs

- peak_height_matrix (.csv, features × samples)
- peak_area_matrix (.csv, features × samples)

## Outputs

- annotated_feature_table (feature matrix with quality flags)
- diagnostic_report (flagged features, variation scores, problem categories)

## How to apply

Load two .csv files into R—one containing chromatographic peak heights and one containing peak areas, both formatted with features as rows and samples as columns. Execute the AVIR.R routine to compute computational variation metrics across each metabolic feature. The algorithm applies flagging logic to identify features exhibiting anomalous variation patterns indicative of peak integration or alignment errors. Generate a diagnostic report listing flagged features, their variation scores, and categorized problem types. Output an annotated feature table with quality flags appended and a summary report of detected issues.

## Related tools

- **AVIR.R** (Computes computational variation metrics on feature tables and applies flagging logic to detect peak integration and alignment errors) — github.com/HuanLab/AVIR
- **R** (Execution environment for running AVIR.R and supporting package dependencies (e1071, caret))

## Examples

```
install.packages('e1071'); install.packages('caret'); setwd('/path/to/AVIR'); source('AVIR.R')
```

## Evaluation signals

- Diagnostic report is non-empty and contains at least one flagged feature with assigned problem category (peak integration vs. alignment error).
- Variation scores for flagged features fall outside expected statistical bounds defined by the algorithm's anomaly detection threshold.
- Annotated feature table has a quality flag column populated for all features; flagged features are a small minority (< 5–10%) in a high-quality dataset.
- Manual inspection of flagged features' chromatographic traces or alignment plots confirms integration or alignment problems predicted by the report.
- Output files (annotated table and diagnostic summary) are parseable and contain expected row/column structure.

## Limitations

- Requires data formatted as two separate .csv files (peak height and peak area); non-standard formats require pre-processing conversion.
- Performance and sensitivity of flagging logic depend on the underlying statistical variation model; extreme or biologically-driven variation patterns may generate false positives.
- Does not perform peak re-integration; flagged features must be manually re-processed or excluded by downstream workflows.
- No explicit threshold parameters are documented in the README; users cannot adjust sensitivity without modifying source code.

## Evidence

- [other] AVIR.R operates by recognizing computational variation among metabolic features in samples to identify problems in metabolomic data caused by processing, including faulty peak integration and feature misalignment.: "recognize computational variation among metabolic features in samples, thereby identifying problems in the data -- such as faulty peak integration or feature misalignment -- caused by metabolomic"
- [other] Workflow step 1 requires loading a metabolomic feature table with rows as features and columns as samples into R.: "Load the metabolomics feature table (rows=features, columns=samples) into R"
- [other] Workflow steps 2–3 involve executing AVIR.R to compute variation metrics and apply flagging logic.: "Execute AVIR.R routine to compute computational variation metrics across metabolic features. 3. Apply flagging logic to identify features exhibiting anomalous variation patterns"
- [other] Workflow steps 4–5 produce diagnostic and annotated outputs.: "Generate a diagnostic report listing flagged features, variation scores, and problem categories. 5. Output the annotated feature table with quality flags and the diagnostic summary"
- [readme] Input file format requirement specifies two .csv files, one with peak height and one with peak area.: "split it into two .csv files, one with the height, and the other with the area, of the chromatographic feature peaks"
