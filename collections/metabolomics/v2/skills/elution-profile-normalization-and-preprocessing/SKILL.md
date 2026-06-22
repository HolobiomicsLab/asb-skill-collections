---
name: elution-profile-normalization-and-preprocessing
description: Use when when you have raw co-fractionation/mass-spectrometry elution intensity profiles and plan to train a CNN or semi-supervised learning model (Label Spreading) directly on unengineered elution data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3474
  tools:
  - SPIFFED
  - EPIC
derived_from:
- doi: 10.1093/bib/bbad229/7199559
  title: SPIFFED
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spiffed_cq
    doi: 10.1093/bib/bbad229/7199559
    title: SPIFFED
  dedup_kept_from: coll_spiffed_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bib/bbad229/7199559
  all_source_dois:
  - 10.1093/bib/bbad229/7199559
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# elution-profile-normalization-and-preprocessing

## Summary

Preprocessing of co-fractionation/mass-spectrometry (CF-MS) elution profiles by normalizing intensity values and handling missing data points, preparing raw elution data for direct input to end-to-end deep learning models without manual feature extraction. This step is critical for eliminating feature engineering bottlenecks and enabling convolutional neural networks to learn directly from raw co-elution patterns.

## When to use

When you have raw co-fractionation/mass-spectrometry elution intensity profiles and plan to train a CNN or semi-supervised learning model (Label Spreading) directly on unengineered elution data. Specifically, use this when: (1) you intend to set feature_selection parameter to '000000001' (raw elution profile mode), (2) your input contains intensity measurements across multiple chromatographic fractions with potential missing or zero values, and (3) you want to avoid manual correlation score computation and instead let the neural network learn co-elution patterns end-to-end.

## When NOT to use

- Input is already a pre-computed feature table (e.g., correlation scores, PCCN, Pearson coefficients) — in that case, set feature_selection to the appropriate bitmask (e.g., '11101001') and use Random Forest or EPPC, not CNN.
- You are using training_method RF (Random Forest), which requires manually selected correlation scores (feature_selection parameter must NOT be '000000001').
- Elution data is already aggregated into summary statistics (e.g., peak position, area under curve) — this skill is for raw, profile-level intensity preservation.

## Inputs

- Raw co-fractionation/mass-spectrometry elution intensity files (tab-separated or CSV matrices with proteins × fractions)
- Elution profile data with potential missing values, zero intensities, or below-detection noise
- Gold standard file defining positive (interacting) and negative (non-interacting) protein pairs for training labels

## Outputs

- Normalized and preprocessed elution profile matrices ready for CNN input
- Validated protein pair feature tensors (shape: NUM_EP × NUM_FRC or flattened equivalent)
- Summary statistics of normalization (mean, std, min, max intensities post-processing)

## How to apply

Load co-fractionation mass-spectrometry elution profiles from input files (typically intensity matrices with proteins as rows and fractions as columns). Normalize intensity values across fractions to place all profiles on a comparable scale—this may involve z-score normalization, min-max scaling, or quantile normalization depending on the distribution of intensities. Identify and handle missing data points (NaN, zero, or below-detection-threshold values) through imputation, masking, or exclusion strategies. Ensure all elution profiles conform to the expected dimensionality (NUM_EP elution profiles per protein pair, NUM_FRC fractions per profile, default 2 profiles × 27 fractions). Validate that the preprocessed data is in a format compatible with the neural network input layer (typically a 3D tensor or flattened matrix). Store the preprocessed profiles in the input directory specified by the `-s 000000001` parameter before invoking the CNN or Label Spreading training pipeline.

## Related tools

- **SPIFFED** (End-to-end deep learning framework that consumes preprocessed raw elution profiles and trains CNN or Label Spreading models for protein-protein interaction prediction) — https://github.com/bio-it-station/SPIFFED
- **EPIC** (Original protein interaction predictor that SPIFFED extends; provides reference architecture for elution profile handling and PPI inference) — https://github.com/BaderLab/EPIC

## Examples

```
python ./src/main.py -s 000000001 /path/to/input/elution_profiles -c /path/to/gold_standard.txt /path/to/output -o preprocessed -M CNN --LEARNING_SELECTION sl --NUM_EP 2 --NUM_FRC 27
```

## Evaluation signals

- All elution intensity values fall within expected range after normalization (e.g., [0, 1] for min-max or mean ≈ 0, std ≈ 1 for z-score); histograms of pre- and post-normalization should show compression into comparable scales.
- Preprocessed profiles conform to exact tensor shape (NUM_EP × NUM_FRC, default 2 × 27); mismatch indicates incomplete or malformed preprocessing.
- Missing data handling is documented and consistent: verify that all NaN/zero values are either imputed, masked, or removed with reproducible criteria; check that the count of removed/imputed entries does not exceed an acceptable threshold (e.g., <10% of total entries).
- Validation and test set split is applied after preprocessing, not before, to avoid data leakage; confirm that train/test ratio matches --TRAIN_TEST_RATIO parameter (default 0.3).
- CNN training converges within expected number of epochs without divergence or NaN loss values, indicating that input normalization prevents gradient explosion/vanishing.

## Limitations

- SPIFFED uses Python 2.7, which is end-of-life; modern CF-MS preprocessing may require porting to Python 3.x.
- Default NUM_FRC=27 and NUM_EP=2 are tailored to the EPIC benchmark datasets; different experimental protocols (e.g., higher-resolution fractionation, replicate profiling) may require retuning these parameters.
- The README does not specify the exact normalization method (z-score vs. min-max vs. quantile); practitioners must either infer from SPIFFED source code or validate empirically that the chosen method preserves biological co-elution signal.
- Handling of missing data is not explicitly documented; imputation strategy (mean-filling, forward-fill, exclusion) could bias downstream PPI predictions if systematic missingness correlates with protein abundance or interaction likelihood.
- Ensemble mode (--CNN_ENSEMBLE 1) doubles input dimensionality; preprocessing must be scaled or validated to ensure memory and gradient stability.

## Evidence

- [methods] Preprocess elution data by normalizing intensity values and handling missing data points.: "Preprocess elution data by normalizing intensity values and handling missing data points."
- [readme] SPIFFED differs from EPIC in that it uses a convolutional neural network to analyze raw co-elution data, thereby eliminating the need for manual feature engineering.: "SPIFFED differs from EPIC in that it uses a convolutional neural network to analyze raw co-elution data, thereby eliminating the need for manual feature engineering."
- [readme] If you want to run Convolutional Neural Network (CNN) or Label Spreading (LS), you must set this parameter to "-s 000000001".: "If you want to run Convolutional Neural Network (CNN) or Label Spreading (LS), you must set this parameter to "-s 000000001"."
- [readme] --NUM_FRC `number_of_fractions`: This parameter stores the number of fractions in the elution profile file. (default: `27`): "--NUM_FRC `number_of_fractions`: This parameter stores the number of fractions in the elution profile file. (default: `27`)"
