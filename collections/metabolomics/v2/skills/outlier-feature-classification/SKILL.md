---
name: outlier-feature-classification
description: Use when after peak picking by MS-DIAL and import into R, when the feature table contains m/z values with decimal components that fall within the [4, 8] interval (indicating instrumental artifacts or calibration errors).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - R
  - margheRita
  - MS-DIAL
  - notame
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- The R package margheRita addresses the complete workflow
- The R package margheRita
- The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS)
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# outlier-feature-classification

## Summary

Identify and classify molecular features with anomalous mass-to-charge (m/z) decimal values that fall outside the expected instrumental range, removing them from downstream analysis in untargeted LC-MS/MS metabolomics. This filtering step ensures that only features with physically plausible m/z values are retained for metabolite annotation and statistical testing.

## When to use

After peak picking by MS-DIAL and import into R, when the feature table contains m/z values with decimal components that fall within the [4, 8] interval (indicating instrumental artifacts or calibration errors). Apply this filter during the initial quality-control and filtering phase, before metabolite annotation or statistical analysis, to prevent false-positive identifications and spurious associations.

## When NOT to use

- When the input data has already been filtered for m/z quality by the peak-picking software or a prior preprocessing step.
- When analyzing targeted metabolomics data with a predefined list of m/z values, where all features are known to be biologically relevant.
- When the m/z decimal range [4, 8] is not representative of instrumental artifacts in your specific MS-DIAL configuration or ionization mode.

## Inputs

- MS-DIAL feature table with m/z values (numeric column)
- feature abundance matrix (features × samples)

## Outputs

- filtered feature table (appropriate m/z values only)
- outlier feature table (inappropriate m/z values)
- filtering summary report (count of retained vs. removed features)

## How to apply

Extract the decimal part of each m/z value by computing m/z modulo 1 for all features in the MS-DIAL feature table. Classify features as inappropriate if their decimal part lies within the interval [4, 8]; otherwise mark as appropriate. Separate the feature set into two subsets: one containing features with appropriate m/z values (suitable for downstream analysis) and one containing features with inappropriate m/z values (to be excluded). Return both subsets and a summary report documenting the count and proportion of filtered features. The rationale is that features with m/z decimal values in this range typically reflect instrumental noise or calibration drift rather than true metabolite signals.

## Related tools

- **margheRita** (Implements m/z filtering via the m_z_filtering() function within the complete LC-MS/MS preprocessing workflow) — https://github.com/emosca-cnr/margheRita
- **MS-DIAL** (Generates the initial feature table with m/z values that serves as input to outlier classification) — http://prime.psc.riken.jp/Metabolomics_Software/MS-DIAL/
- **R** (Programming environment for implementing decimal extraction and feature classification logic)
- **notame** (Alternative R package for LC-MS metabolomics preprocessing that includes filtering by wrong m/z values) — https://github.com/hanhineva-lab/notame

## Evaluation signals

- Verify that the sum of retained and removed feature counts equals the total input feature count.
- Confirm that all features in the 'appropriate' subset have m/z decimal values outside [4, 8] (i.e., decimal part < 4 OR decimal part > 8).
- Confirm that all features in the 'inappropriate' subset have m/z decimal values within [4, 8] (i.e., 4 ≤ decimal part ≤ 8).
- Check that the filtered feature table (appropriate subset) yields improved cosine similarity matches or higher confidence metabolite identifications in downstream annotation steps compared to the unfiltered table.
- Ensure the feature abundance matrix dimensions are consistent after subsetting (number of columns unchanged; number of rows equals count of retained features).

## Limitations

- The m/z decimal interval [4, 8] is a default threshold specific to margheRita and MS-DIAL configuration; it may need adjustment for different mass spectrometers, ionization modes (RP-C18, HILIC, RP-C8, pZIC-HILIC), or calibration protocols.
- This filter assumes that features with m/z decimal values in [4, 8] are uniformly artifacts; true signals falling in this range (though rare) will be incorrectly removed.
- The method does not account for m/z shifts caused by adduct formation, isotopologues, or in-source fragmentation; these must be handled by separate preprocessing steps.
- Filtering is applied before consideration of other quality metrics (e.g., coefficient of variation, missing value patterns), so the final dataset may still contain low-quality features after this step.

## Evidence

- [other] The m/z filtering function removes features whose m/z decimal values fall within the interval [4, 8] by default. When applied to the dataset, this filter excluded 56 features with inappropriate m/z values while retaining 548 features with appropriate m/z values.: "The m/z filtering function removes features whose m/z decimal values fall within the interval [4, 8] by default. When applied to the dataset, this filter excluded 56 features with inappropriate m/z"
- [other] Extract the decimal part of each m/z value by computing m/z modulo 1. Classify features as inappropriate if the decimal part lies within [4,8]; otherwise mark as appropriate.: "Extract the decimal part of each m/z value by computing m/z modulo 1. Classify features as inappropriate if the decimal part lies within [4,8]; otherwise mark as appropriate."
- [readme] The package provides a series of pre-processing functions (quality control, filtering and normalization) with a particular focus on methods specifically recommended for metabolomic profiles, such as filtering by mass defects, filtering by coefficient of variation (samples vs QCs) and probabilistic quotient normalization: "a series of pre-processing functions (quality control, filtering and normalization) with a particular focus on methods specifically recommended for metabolomic profiles, such as filtering by mass"
- [intro] runs filters to exclude features/sample with many missing values, features with wrong m/z values: "runs filters to exclude features/sample with many missing values, features with wrong m/z values"
