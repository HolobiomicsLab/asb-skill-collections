---
name: protein-interaction-score-prediction
description: Use when you have co-fractionation/mass-spectrometry (CF-MS) elution profiles (raw intensity vectors across fractions) paired with a gold standard of known positive and negative protein–protein interactions, and your goal is to predict interaction scores for all protein pairs without hand-crafted.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0315
  edam_topics:
  - http://edamontology.org/topic_0128
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3452
  tools:
  - SPIFFED
  - EPIC
  - TensorFlow / Keras
  - scikit-learn
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# protein-interaction-score-prediction

## Summary

Train a balanced end-to-end convolutional neural network to predict protein–protein interaction (PPI) scores directly from raw co-fractionation/mass-spectrometry elution profiles, eliminating manual feature engineering. Apply this skill when you have CF-MS elution intensity data and labeled PPI ground truth, and you want to leverage deep learning to handle class imbalance and nonlinear co-elution patterns.

## When to use

You have co-fractionation/mass-spectrometry (CF-MS) elution profiles (raw intensity vectors across fractions) paired with a gold standard of known positive and negative protein–protein interactions, and your goal is to predict interaction scores for all protein pairs without hand-crafted correlation features. This skill is appropriate when training data is imbalanced (more negative than positive PPIs) and you want to avoid manual feature engineering that traditional methods like EPIC require.

## When NOT to use

- Your input is already a pre-computed feature matrix (e.g., Pearson correlations, mutual information scores) — SPIFFED's strength is eliminating the feature engineering step; use traditional classifiers (RF, SVM) on pre-computed features instead.
- You lack labeled gold standard data — SPIFFED requires supervised or semi-supervised training with positive and negative examples; unsupervised co-complex inference alone is not sufficient.
- Your elution profiles are not aligned or have highly variable numbers of fractions — SPIFFED expects consistent dimensionality (e.g., fixed 27 fractions); preprocessing to uniform length is required first.

## Inputs

- Raw co-fractionation/mass-spectrometry elution profiles (normalized intensity vectors per protein, typically 27 fractions)
- Gold standard file with labeled positive and negative protein–protein interactions (reference complexes or benchmark dataset)
- Input directory containing elution profile files in structured format

## Outputs

- Trained CNN model weights and architecture
- Predicted PPI scores for all protein pairs (typically in output file with filename prefix specified)
- Performance metrics (if validation/test splits are used)

## How to apply

Load raw elution intensity profiles and preprocess by normalizing values and handling missing data points. Set the feature selection parameter to raw elution profile mode (e.g., `-s 000000001`) and choose CNN as the training method (`-M CNN`). Configure class-balancing strategy by setting the negative-to-positive PPI ratio (e.g., `--POS_NEG_RATIO 5`) to address label imbalance; this controls how many negative examples are sampled during training. Specify the number of elution profiles per PPI pair (`--NUM_EP`), number of fractions per profile (`--NUM_FRC`, typically 27), and whether to use ensemble mode (`--CNN_ENSEMBLE`). Choose supervised learning (`--LEARNING_SELECTION sl`) or semi-supervised learning (`--LEARNING_SELECTION ssl`), then train via direct training (`--K_D_TRAIN d`) or k-fold cross-validation (`--K_D_TRAIN k`). The model learns convolutional filters to detect co-elution patterns directly, producing interaction scores for all protein pairs on the test set.

## Related tools

- **SPIFFED** (End-to-end CNN model for PPI prediction from raw CF-MS elution profiles; main implementation tool for this skill) — https://github.com/bio-it-station/SPIFFED
- **EPIC** (Predecessor tool for protein complex inference using handcrafted correlation features; SPIFFED improves upon EPIC by replacing feature engineering with convolutional layers) — https://github.com/BaderLab/EPIC
- **TensorFlow / Keras** (Deep learning framework underlying the CNN model (TensorFlow 1.13.1, Keras 2.2.4 specified in SPIFFED requirements))
- **scikit-learn** (Used for train–test splitting, cross-validation folds, and baseline classifier comparison (RF option))

## Examples

```
python ./main.py -s 000000001 /path/to/input/elution_profiles -c /path/to/gold_standard.tsv /path/to/output -o result -M CNN -n 10 -m EXP -f STRING --LEARNING_SELECTION sl --K_D_TRAIN d --TRAIN_TEST_RATIO 0.3 --POS_NEG_RATIO 5 --NUM_EP 2 --NUM_FRC 27 --CNN_ENSEMBLE 0
```

## Evaluation signals

- Model converges during training: loss decreases monotonically over epochs and validation loss stabilizes without diverging.
- Predicted interaction scores span a reasonable range (e.g., [0, 1] for sigmoid output) and show a bimodal distribution (clear separation between high scores for known interactions and low scores for negatives).
- Cross-validation or test-set metrics (AUROC, AUPRC, precision–recall) meet or exceed the performance of feature-engineered baselines (EPIC with Pearson/mutual information), validating that end-to-end learning captures co-elution patterns.
- Class balance is maintained in training mini-batches: proportions of positive and negative samples match the specified `--POS_NEG_RATIO` throughout epochs.
- Output files are generated with expected filenames and contain predictions for all protein pairs in the input dataset; no crashes or NaN predictions.

## Limitations

- Requires Python 2.7 and specific legacy dependency versions (TensorFlow 1.13.1, Keras 2.2.4); may not be compatible with modern Python 3.x environments without refactoring.
- Assumes fixed, pre-aligned elution profile dimensionality (default 27 fractions); variable-length or ragged profiles require padding or interpolation before input.
- Performance depends critically on the quality and size of the gold standard dataset; sparse or noisy labels may lead to poor generalization.
- No built-in handling of missing fractions or zero-intensity proteins; preprocessors must impute or filter beforehand.
- Ensemble mode (`--CNN_ENSEMBLE 1`) requires multiple replicate elution profiles per protein pair, which may not always be available in all CF-MS experiments.

## Evidence

- [readme] SPIFFED uses a convolutional neural network to analyze raw co-elution data, thereby eliminating the need for manual feature engineering.: "it uses a convolutional neural network to analyze raw co-elution data, thereby eliminating the need for manual feature engineering"
- [readme] A balanced end-to-end deep learning model for interactome prediction from co-fractionation/mass-spectrometry (CF-MS) data: "A balanced end-to-end deep learning model for interactome prediction from co-fractionation/mass-spectrometry (CF-MS) data"
- [readme] CNN and LS must come with raw elution profile ('-s 000000001'). If you want to run with supervised learning, then set '--LEARNING_SELECTION sl': "CNN and LS must come with raw elution profile ('-s 000000001')"
- [readme] This parameter stores the ratio of negative PPIs to positive PPIs.: "This parameter stores the ratio of negative PPIs to positive PPIs"
- [other] Implement class-balancing strategy during training to handle imbalanced positive/negative PPI labels.: "Implement class-balancing strategy during training to handle imbalanced positive/negative PPI labels"
- [other] Train the model on labeled protein pairs using an appropriate loss function (e.g., weighted cross-entropy or focal loss) and optimization algorithm.: "Train the model on labeled protein pairs using an appropriate loss function (e.g., weighted cross-entropy or focal loss)"
