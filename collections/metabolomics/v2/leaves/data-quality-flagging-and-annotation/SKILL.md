---
name: data-quality-flagging-and-annotation
description: Use when after peak integration and feature alignment in metabolomic
  processing, when you have a feature table (rows=features, columns=samples) and need
  to identify which features are corrupted by processing artifacts (faulty peak integration,
  feature misalignment).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - AVIR.R
  - R
  - e1071
  - caret
  license_tier: open
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

# data-quality-flagging-and-annotation

## Summary

Apply AVIR.R to detect and flag computational artifacts in metabolomic feature tables by identifying anomalous variation patterns indicative of peak integration errors or feature misalignment. This skill produces an annotated feature table and diagnostic report stratifying quality problems by type.

## When to use

After peak integration and feature alignment in metabolomic processing, when you have a feature table (rows=features, columns=samples) and need to identify which features are corrupted by processing artifacts (faulty peak integration, feature misalignment). Use this skill before downstream statistical analysis to avoid propagating systematic errors.

## When NOT to use

- Input is already a quality-filtered or pre-curated feature table (flagging would be redundant).
- You lack paired peak height and peak area measurements (AVIR.R requires both metrics).
- Your data are from non-targeted metabolomics workflows where peak integration and alignment artifacts are not the primary concern.

## Inputs

- metabolomics feature table (CSV format, rows=metabolic features, columns=samples)
- peak height data (CSV file, rows=features, columns=samples)
- peak area data (CSV file, rows=features, columns=samples)

## Outputs

- annotated feature table with quality flags
- diagnostic summary report (features, variation scores, problem categories)

## How to apply

Load your metabolomics feature table into R as a matrix with features as rows and samples as columns. Prepare two separate .csv files: one containing peak height and one containing peak area for each feature–sample pair. Execute the AVIR.R script by sourcing it in R Studio (or via `CTRL + SHIFT + ENTER`); the routine computes computational variation metrics across metabolic features and applies flagging logic to identify features exhibiting anomalous variation patterns. The script generates a diagnostic report listing flagged features, their variation scores, and problem categories (peak integration vs. alignment errors). Inspect the flagged feature list and cross-reference with your upstream processing logs to confirm the nature of each anomaly before filtering or reprocessing.

## Related tools

- **AVIR.R** (Computes computational variation metrics across metabolic features and applies flagging logic to identify peak integration and alignment errors) — github.com/HuanLab/AVIR
- **R** (Runtime environment for executing AVIR.R and loading/manipulating metabolomic feature tables)
- **e1071** (R package dependency for AVIR.R statistical computations)
- **caret** (R package dependency for AVIR.R model training and classification)

## Examples

```
# In R Studio: source('AVIR.R'); # then inspect output diagnostic report and annotated_feature_table.csv
```

## Evaluation signals

- Diagnostic report is generated with non-empty flagged feature list; variation scores are numeric and within expected range (typically 0–1 or standardized scale).
- Flagged features map back to known processing issues (e.g., co-eluting peaks, retention time drift) visible in raw chromatograms or peak tables.
- Annotated feature table contains a quality-flag column with binary or categorical labels (e.g., 'pass', 'peak_integration_error', 'misalignment'); all rows are preserved but marked.
- Distribution of flagged vs. unflagged features is consistent with expected contamination rate (typically < 5–10% of features in well-run experiments).
- Removal of flagged features from downstream analysis reduces spurious associations and improves biological reproducibility (e.g., lower false-discovery rate in differential analysis).

## Limitations

- AVIR.R relies on unsupervised variation metrics and may require manual curation or external validation to confirm that flagged features truly represent processing artifacts rather than genuine biological variation.
- The method requires paired peak height and peak area data; workflows that produce only one of these metrics cannot be analyzed.
- Flagging accuracy depends on the quality of upstream peak integration and alignment; severely corrupted data may evade detection or generate false positives.
- AVIR.R is designed for computational variation; it does not address biological confounders (e.g., batch effects, sample preparation artifacts) or chemical noise.

## Evidence

- [readme] AVIR.R is a program developed to recognize computational variation among metabolic features in samples, thereby identifying problems in the data -- such as faulty peak integration or feature misalignment -- caused by metabolomic processing.: "AVIR.R is a program developed to recognize computational variation among metabolic features in samples, thereby identifying problems in the data -- such as faulty peak integration or feature"
- [other] Execute AVIR.R routine to compute computational variation metrics across metabolic features. Apply flagging logic to identify features exhibiting anomalous variation patterns indicative of peak integration or alignment errors.: "Execute AVIR.R routine to compute computational variation metrics across metabolic features. Apply flagging logic to identify features exhibiting anomalous variation patterns indicative of peak"
- [readme] When adding your own datasets to be analyzed using AVIR.R, please split it into two .csv files, one with the height, and the other with the area, of the chromatographic feature peaks.: "split it into two .csv files, one with the height, and the other with the area, of the chromatographic feature peaks"
- [other] Generate a diagnostic report listing flagged features, variation scores, and problem categories. Output the annotated feature table with quality flags and the diagnostic summary.: "Generate a diagnostic report listing flagged features, variation scores, and problem categories. Output the annotated feature table with quality flags and the diagnostic summary"
- [readme] Run the script by clicking the 'Source' button at the top right of the script. Alternatively press CTRL + SHIFT + ENTER.: "Run the script by clicking the 'Source' button at the top right of the script. Alternatively press CTRL + SHIFT + ENTER"
