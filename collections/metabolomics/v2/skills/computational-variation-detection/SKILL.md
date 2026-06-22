---
name: computational-variation-detection
description: Use when after peak detection and feature alignment in a metabolomic LC–MS/MS or GC–MS workflow, when you have a feature table (rows=metabolic features, columns=samples) split into separate .csv files for peak height and peak area.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - AVIR.R
  - R
  - e1071
  - caret
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c04046
  all_source_dois:
  - 10.1021/acs.analchem.3c04046
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# computational-variation-detection

## Summary

AVIR.R detects computational artifacts in metabolomic data by identifying anomalous variation patterns among features across samples, flagging quality problems such as faulty peak integration or feature misalignment. This skill is essential for validating metabolomic feature tables before downstream analysis.

## When to use

Apply this skill after peak detection and feature alignment in a metabolomic LC–MS/MS or GC–MS workflow, when you have a feature table (rows=metabolic features, columns=samples) split into separate .csv files for peak height and peak area. Use it when you suspect data quality issues introduced during chromatographic processing, or as a routine QC step before statistical or biological interpretation.

## When NOT to use

- Do not use if your feature table has already undergone manual curation or post-hoc filtering for quality — the skill is designed for raw or minimally processed peak tables.
- Do not apply if peak height and area data are not separately available or cannot be formatted into the required two-file structure.
- Do not use for non-metabolomic LC–MS or GC–MS data where peak integration semantics differ substantially.

## Inputs

- PeakHeight_Demo.csv (peak height values; rows=features, columns=samples)
- PeakArea_Demo.csv (peak area values; rows=features, columns=samples)

## Outputs

- Annotated feature table with quality flags
- Diagnostic report listing flagged features, variation scores, and problem categories

## How to apply

Load metabolomic feature tables (height and area .csv files) into R, ensuring rows represent metabolic features and columns represent samples. Install required packages (e1071, caret). Execute the AVIR.R script by sourcing it in R Studio (Source button or CTRL+SHIFT+ENTER). The routine computes computational variation metrics across features to detect anomalous variation patterns indicative of peak integration errors or feature misalignment. The algorithm applies flagging logic to classify features by problem category. Output includes an annotated feature table with quality flags and a diagnostic summary report listing flagged features, their variation scores, and assigned problem categories.

## Related tools

- **AVIR.R** (Primary executable that computes computational variation metrics and applies flagging logic to detect peak integration and alignment errors) — github.com/HuanLab/AVIR
- **R** (Runtime environment for executing AVIR.R script and loading/processing .csv feature tables)
- **e1071** (R package dependency for statistical computations in variation metric calculation)
- **caret** (R package dependency for machine learning and feature flagging logic)

## Examples

```
# In R Studio: set working directory, install dependencies, source AVIR.R
setwd('/path/to/AVIR.R'); install.packages(c('e1071','caret')); source('AVIR.R')
```

## Evaluation signals

- Diagnostic report is generated and contains non-empty lists of flagged features with assigned problem categories (peak integration vs. feature misalignment)
- All rows in the output annotated feature table carry a quality flag (present or absent); no rows are missing flags
- Variation scores for flagged features fall into expected ranges documented in the method; extreme or NaN values indicate computation failure
- Features flagged as problematic show visually distinguishable or statistically significant variation patterns compared to non-flagged features when plotted
- Output files (annotated table + diagnostic summary) are non-empty, properly formatted .csv files with correct row/column cardinality matching the input

## Limitations

- AVIR.R requires metabolomic data split into exactly two .csv files (peak height and peak area); other formats or combined files must be pre-processed.
- The skill is tuned for metabolomic LC–MS/MS and GC–MS workflows and may not generalize to other mass spectrometry modalities or non-MS platforms.
- No explicit discussion of how the method handles missing data, zero values, or sparse features in the feature table.
- The README references a user guide and video tutorial (with placeholder link) but does not document parameter tuning, sensitivity settings, or thresholds for flagging logic.

## Evidence

- [other] AVIR.R operates by recognizing computational variation among metabolic features in samples to identify problems in metabolomic data caused by processing, including faulty peak integration and feature misalignment.: "AVIR.R is a program developed to recognize computational variation among metabolic features in samples, thereby identifying problems in the data -- such as faulty peak integration or feature"
- [other] The workflow loads a metabolomics feature table, computes computational variation metrics, applies flagging logic, and generates a diagnostic report with quality flags.: "Load the metabolomics feature table (rows=features, columns=samples) into R. Execute AVIR.R routine to compute computational variation metrics across metabolic features. Apply flagging logic to"
- [readme] Input data must be formatted as two separate .csv files, one for peak height and one for peak area, with rows as features and columns as samples.: "When adding your own datasets to be analyzed using AVIR.R, please split it into two .csv files, one with the height, and the other with the area, of the chromatographic feature peaks."
- [readme] R Studio execution: source the script using the Source button or CTRL+SHIFT+ENTER keyboard shortcut after installing required packages.: "Run the script by clicking the "Source" button at the top right of the script. Alternatively press CTRL + SHIFT + ENTER."
- [readme] Required R package dependencies are e1071 and caret, installed via install.packages().: "Simply run the following code in R Studio: `install.packages('e1071')` `install.packages('caret')`"
