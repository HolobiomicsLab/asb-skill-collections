---
name: metabolomic-feature-imputation
description: Use when when a preprocessed metabolomic feature table (e.g., MS-Dial
  output) retains features and samples that passed filtering for missingness thresholds
  and m/z validity, but still contain scattered missing values (NA). This skill is
  appropriate after sample-level filtering (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3662
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - margheRita
  - R
  - notame
  - MS-Dial
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- The R package margheRita addresses the complete workflow for metabolomic profiling
  in untargeted studies based on liquid chromatography (LC) coupled with tandem mass
  spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
- The R package margheRita addresses the complete workflow
- The R package margheRita
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

# metabolomic-feature-imputation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Replace missing values in metabolomic feature tables using a minimum-value-based random substitution strategy, after applying upstream feature and sample-level filtering. This skill is applied after excluding features with incorrect m/z values and samples/features with excessive missingness, to recover measurable but undetected metabolite signals without artificially amplifying noise.

## When to use

When a preprocessed metabolomic feature table (e.g., MS-Dial output) retains features and samples that passed filtering for missingness thresholds and m/z validity, but still contain scattered missing values (NA). This skill is appropriate after sample-level filtering (e.g., excluding samples with <100 detected metabolites) and feature-level filtering (e.g., features in <3 samples, or m/z decimal values in [4,8] range removed), and is NOT applied to features or samples that were excluded in those steps.

## When NOT to use

- Input feature table has not yet been filtered for incorrect m/z values or excessive missingness — apply m/z and sample/feature-level filtering first.
- Missing values are non-random (e.g., systematic missingness in a batch or treatment group) — investigate root cause and consider batch correction or selective filtering instead.
- The analysis requires absolute quantification or metabolite concentration inference — minimum-value imputation introduces uncertainty unsuitable for targeted quantitative studies; consider alternative strategies (e.g., limit-of-detection substitution with instrument-validated thresholds).

## Inputs

- Filtered metabolomic feature table (e.g., Urine_RP_NEG_norm.txt, Urine_RP_POS_norm.txt from MS-Dial output)
- Feature abundance matrix with rows=features, columns=samples, with NA entries representing undetected metabolites

## Outputs

- Imputed feature abundance matrix with all NA values replaced by random substitutions in the 10–25% minimum-value range
- Feature count and sample count summary confirming retention after imputation

## How to apply

After filtering, impute remaining NA values by replacing each missing value with a random number drawn uniformly between 10% and 25% of that feature's minimum observed value. This approach assumes the missing values fall below the instrument's detection limit and represent true biological absence, while preserving the feature's concentration range and avoiding artificial signal amplification. The imputation is feature-wise: compute the minimum non-NA abundance for each feature independently, then for each NA entry in that feature, sample a random value from [0.10 × min_abundance, 0.25 × min_abundance]. This method is grounded in the principle that undetected metabolites are more likely to be present at very low (but non-zero) levels than at zero, and the 10–25% range prevents overestimation while maintaining realistic quantitative ranges. Apply this after all upstream filtering steps are complete and verified (e.g., after confirming sample and feature counts match expected totals).

## Related tools

- **margheRita** (R package providing the filtering() function that executes sample/feature-level exclusions and calls the imputation step; implements the complete preprocessing workflow including NA imputation on MS-Dial output) — https://github.com/emosca-cnr/margheRita
- **notame** (R package offering multiple imputation strategies (including random forest and random-value methods); compatible with margheRita via as.metaboset() export for alternative imputation approaches) — https://github.com/hanhineva-lab/notame
- **MS-Dial** (Peak-picking software that generates the raw feature table (with NA entries for undetected metabolites) prior to preprocessing and imputation in margheRita)
- **R** (Programming language runtime for executing margheRita and the filtering/imputation workflow)

## Evaluation signals

- No NA values remain in the output feature matrix; all original NA entries are replaced with numeric values in the range [0.10 × min, 0.25 × min] for each feature.
- Feature and sample counts do not change after imputation; the output retains the same dimensions (243 samples × 548 features for Urine dataset example) as the filtered input.
- Imputed values are strictly positive (>0) and less than the feature's minimum observed value, confirming they fall in the 10–25% range and do not exceed any detected abundance.
- Distribution of imputed values for each feature is uniform within the specified range and does not create artificial clusters or skew the feature's histogram.
- Downstream statistical tests (e.g., differential abundance, PCA) proceed without failure due to missing values and produce interpretable results consistent with the feature's underlying biological range.

## Limitations

- Random imputation introduces stochasticity; repeated runs on the same data will yield slightly different imputed values. Set a random seed before imputation if reproducibility is required.
- The 10–25% minimum-value strategy assumes all missing values are below the instrument's detection limit and does not account for systematic missingness (e.g., post-translational modifications absent in a sample group). Features with very skewed abundance distributions (e.g., one sample with extremely high abundance) may yield implausibly narrow imputation ranges.
- Imputation does not recover true metabolite identity or abundance; it is a mathematical convenience for downstream analysis. Results should be interpreted with the understanding that imputed values are not measured observations.

## Evidence

- [other] The filtering() function applies three sequential steps: (1) excludes samples with fewer than 100 metabolites and features occurring in fewer than 3 samples, (2) removes features with m/z decimal values within the range [4, 8] by default, and (3) imputes remaining NA values by replacing them with a random number calculated between 10%-25% of the feature's minimum value.: "imputes remaining NA values by replacing them with a random number calculated between 10%-25% of the feature's minimum value"
- [other] On the Urine dataset, this retained 243/243 samples, 604/604 features after NA filtering, and 548/604 features after m/z filtering.: "On the Urine dataset, this retained 243/243 samples, 604/604 features after NA filtering, and 548/604 features after m/z filtering."
- [readme] a series of pre-processing functions (quality control, filtering and normalization) with a particular focus on methods specifically recommended for metabolomic profiles: "a series of pre-processing functions (quality control, filtering and normalization) with a particular focus on methods specifically recommended for metabolomic profiles"
- [intro] runs filters to exclude features/sample with many missing values, features with wrong m/z values: "runs filters to exclude features/sample with many missing values, features with wrong m/z values"
