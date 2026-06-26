---
name: mz-decimal-extraction
description: Use when after loading a feature table with m/z values from MS-Dial output
  when you need to identify and remove features with anomalous decimal m/z values.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - R
  - margheRita
  - MS-Dial
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- The R package margheRita addresses the complete workflow
- The R package margheRita
- The R package margheRita addresses the complete workflow for metabolomic profiling
  in untargeted studies based on liquid chromatography (LC) coupled with tandem mass
  spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_margherita_cq
    doi: 10.1101/2024.06.20.599545v1
    title: MargheRita
  dedup_kept_from: coll_margherita_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.06.20.599545v1
  all_source_dois:
  - 10.1101/2024.06.20.599545v1
  - 10.1101/2024.06.20.599545
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mz-decimal-extraction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and classify the decimal portion of mass-to-charge (m/z) values from MS-Dial feature tables to identify and filter features with inappropriate m/z ratios. This skill enables quality control by removing features whose decimal m/z values fall outside acceptable ranges, a common preprocessing step in untargeted LC-MS/MS metabolomics.

## When to use

Apply this skill after loading a feature table with m/z values from MS-Dial output when you need to identify and remove features with anomalous decimal m/z values. This is particularly relevant in untargeted metabolomics workflows where incorrect mass assignments can arise from instrument artifacts, noise, or calibration drift. Use it as part of the initial quality control and filtering phase before statistical analysis or metabolite annotation.

## When NOT to use

- Input feature table is already pre-filtered or does not contain m/z decimal values.
- Analysis requires retention of all detected features regardless of m/z quality (e.g., exploratory untargeted discovery where mass accuracy is not yet validated).
- M/z values are known to follow a non-standard decimal distribution due to specialized acquisition modes or calibration strategies.

## Inputs

- MS-Dial feature table (with m/z values column)
- Feature abundance matrix with m/z annotations

## Outputs

- Subset of features with appropriate m/z decimal values
- Subset of features with inappropriate m/z decimal values
- Filtering summary report (counts, thresholds, rationale)

## How to apply

Load the MS-Dial feature table containing m/z values into R. Extract the decimal part of each m/z value by computing m/z modulo 1 (m/z %% 1). Define a threshold interval (default [4, 8] in the source article) and classify each feature as inappropriate if its decimal value falls within that range, otherwise mark as appropriate. Separate the feature set into two subsets: retained features with appropriate decimal m/z values and excluded features with inappropriate values. Return both subsets and a summary report documenting the number of features retained versus excluded, along with the filtering threshold used.

## Related tools

- **margheRita** (R package providing m_z_filtering() function to extract decimal m/z values and classify features by decimal value ranges) — https://github.com/emosca-cnr/margheRita
- **MS-Dial** (Peak-picking software that generates the feature table with m/z annotations as input to this skill)
- **R** (Programming language in which m/z decimal extraction and modulo arithmetic are implemented)

## Examples

```
m_z_filtering(feature_table = feature_data, decimal_range = c(4, 8))
```

## Evaluation signals

- Feature count totals: sum of retained + excluded features equals initial feature count (e.g., 548 + 56 = 604 total features).
- Decimal value distribution: verify that excluded features have decimal m/z values within [4, 8] and retained features fall outside this range.
- No NaN or infinite m/z values remain after extraction; modulo operation produces valid numeric decimal portions.
- Filtering summary report documents filtering threshold, number of features removed, and number retained with explicit counts and percentages.
- Downstream feature abundance matrix dimensions are consistent: retained feature count matches rows in filtered abundance table.

## Limitations

- The threshold interval [4, 8] is dataset-dependent and may require adjustment based on instrument calibration, acquisition mode, or metabolite class expectations; universal defaults may not apply to all LC-MS methods.
- Mass defects and natural m/z distributions vary by chemical class (e.g., organic metabolites vs. xenobiotics), so a single decimal filter may incorrectly exclude legitimate features from minority classes.
- High-resolution MS data and low-resolution MS data may require different decimal threshold strategies; this skill assumes sufficient mass accuracy for meaningful decimal-value classification.
- The skill does not account for systematic m/z drift across a batch or run; if calibration drift is present, the decimal filter may inconsistently classify features measured at different times.

## Evidence

- [other] Extract the decimal part of each m/z value by computing m/z modulo 1.: "Extract the decimal part of each m/z value by computing m/z modulo 1."
- [other] The m/z filtering function removes features whose m/z decimal values fall within the interval [4, 8] by default.: "The m/z filtering function removes features whose m/z decimal values fall within the interval [4, 8] by default."
- [other] When applied to the dataset, this filter excluded 56 features with inappropriate m/z values while retaining 548 features with appropriate m/z values.: "When applied to the dataset, this filter excluded 56 features with inappropriate m/z values while retaining 548 features with appropriate m/z values."
- [intro] runs filters to exclude features/sample with many missing values, features with wrong m/z values: "runs filters to exclude features/sample with many missing values, features with wrong m/z values"
- [readme] margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS): "margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS)"
