---
name: metabolomic-feature-table-processing
description: Use when you have a metabolomics feature table (rows=features, columns=samples) generated from LC-MS or GC-MS preprocessing and need to identify which features contain systematic errors from peak integration or alignment.
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

# metabolomic-feature-table-processing

## Summary

AVIR.R detects computational variation among metabolic features in samples to identify data quality problems caused by metabolomic processing, such as faulty peak integration or feature misalignment. This skill enables automated quality control of untargeted metabolomics datasets by flagging anomalous features before downstream analysis.

## When to use

Apply this skill when you have a metabolomics feature table (rows=features, columns=samples) generated from LC-MS or GC-MS preprocessing and need to identify which features contain systematic errors from peak integration or alignment. Use it as a quality-control checkpoint after feature detection but before statistical or multivariate analysis, especially when processing large batches of samples where manual inspection is infeasible.

## When NOT to use

- Input data has already been manually curated or pre-filtered for quality — AVIR.R is redundant after expert review.
- You do not have both peak height and peak area data available — the routine requires paired chromatographic measurements.
- Your data are already at the level of metabolite identifications or aggregated across samples — AVIR.R requires the raw feature-level table.

## Inputs

- metabolomics feature table (CSV or R data frame, rows=features, columns=samples)
- peak height data (CSV format: features × samples)
- peak area data (CSV format: features × samples)

## Outputs

- annotated feature table with quality flags per feature
- diagnostic summary report (features, variation scores, problem categories)
- flagged feature list with anomaly classifications

## How to apply

Load your metabolomics feature table into R and execute the AVIR.R routine to compute computational variation metrics across metabolic features. The routine applies flagging logic to identify features exhibiting anomalous variation patterns indicative of peak integration errors or misalignment. Features are scored by their deviation from expected variation behavior; those exceeding anomaly thresholds are flagged and categorized by problem type. Generate a diagnostic report listing flagged features, their variation scores, and problem categories, then output the annotated feature table with quality flags appended. The rationale is that true metabolic features should exhibit systematic variation correlated with biological or experimental conditions, whereas processing errors produce spurious or uncorrelated variation signatures.

## Related tools

- **AVIR.R** (executes computational variation detection and anomaly flagging on the feature table) — https://github.com/HuanLab/AVIR
- **R** (runtime environment; required packages: e1071, caret)

## Examples

```
# In R Studio: load peak height and area CSVs, source AVIR.R script
setwd('path/to/AVIR.R'); source('AVIR.R')
```

## Evaluation signals

- Diagnostic report is generated with non-empty flagged feature list; at least one feature exhibits anomalous variation pattern.
- All flagged features have assigned problem categories (peak integration error, feature misalignment, or other) with numerical variation scores.
- Annotated feature table has a quality-flag column appended with binary or categorical values matching the diagnostic summary.
- Variation metrics are reproducible across multiple runs on the same input; scores remain stable.
- Flagged features cluster in 2D/3D variation space as visual outliers; unflagged features form coherent cloud.

## Limitations

- AVIR.R assumes feature variation is primarily driven by biological/experimental factors; datasets with extreme batch effects or instrumental drift may produce false positives.
- The routine requires paired peak height and peak area CSV files; missing or misaligned data will cause errors.
- Anomaly threshold and flagging logic are not explicitly parameterized in the README; users cannot easily adjust sensitivity without modifying the source code.
- No guidance provided on handling features with zero or near-zero intensity across samples, which may artificially inflate variation metrics.

## Evidence

- [readme] AVIR.R is a program developed to recognize computational variation among metabolic features in samples, thereby identifying problems in the data -- such as faulty peak integration or feature misalignment -- caused by metabolomic processing.: "AVIR.R is a program developed to recognize computational variation among metabolic features in samples, thereby identifying problems in the data -- such as faulty peak integration or feature"
- [other] Load the metabolomics feature table (rows=features, columns=samples) into R. Execute AVIR.R routine to compute computational variation metrics across metabolic features. Apply flagging logic to identify features exhibiting anomalous variation patterns indicative of peak integration or alignment errors.: "Load the metabolomics feature table (rows=features, columns=samples) into R. Execute AVIR.R routine to compute computational variation metrics across metabolic features. Apply flagging logic to"
- [other] Generate a diagnostic report listing flagged features, variation scores, and problem categories. Output the annotated feature table with quality flags and the diagnostic summary.: "Generate a diagnostic report listing flagged features, variation scores, and problem categories. Output the annotated feature table with quality flags and the diagnostic summary."
- [readme] When adding your own datasets to be analyzed using AVIR.R, please split it into two .csv files, one with the height, and the other with the area, of the chromatographic feature peaks.: "When adding your own datasets to be analyzed using AVIR.R, please split it into two .csv files, one with the height, and the other with the area, of the chromatographic feature peaks."
- [readme] install.packages('e1071')
install.packages('caret'): "install.packages('e1071')
install.packages('caret')"
