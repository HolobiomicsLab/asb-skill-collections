# SciTask Card: Reproduce the AUC ROC Score Exceeding 0.9 Under Full Training Condition

- Task ID: `task_005`
- Schema version: `0.18.0`
- Created at: `2026-06-16T07:11:40.529655+00:00`
- Source package: `/Users/nothiasl/git/AgenticScienceBuilder/outputs/asbb_pilot/coll_neatms/synthesized_package`
- Domain: `mass-spectrometry / metabolomics`
- Subtask categories: `model-training`, `data-processing`, `benchmark-evaluation`
- GitHub: `bihealth/NeatMS`
- Input from: `task_004`
- Quality: Score 2/5 — Coherent: false, placeholder, 3 grounding failures

## Classification

- Task kind: `reproduction`
- Article type: `software-tool`
- Primary domain: `metabolomics`
- Subdomains: `computational-metabolomics`, `artificial-intelligence`, `untargeted-metabolomics`
- Techniques: `machine-learning`, `deep-learning`, `feature-detection`, `metabolite-identification`, `dimensionality-reduction`
- Keywords: `untargeted lcms` · `signal labelling` · `peak filtering` · `false positive detection` · `neural network classification` · `ms1 peaks` · `metabolomics data processing`

## Research Question
Does training the NeatMS CNN model from scratch on the provided example dataset under full training conditions produce an AUC ROC score exceeding 0.9 without evidence of overfitting?

## Connected Finding
NeatMS relies on neural network based classification to enable automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.

## Task Description
Train a NeatMS convolutional neural network from scratch on an example LC-MS dataset using the default architecture (convolutional base + dense classifier with dropout and kernel regularization) and report the Area Under the ROC Curve (AUC) score, verifying it exceeds 0.95 and confirming absence of overfitting.

## Inputs
- task_004.expected_outputs[0]: Training batch artifact (80% of peaks, class-imbalanced distribution)
- Raw LC-MS data in mzML format
- Feature table in CSV format (mzMine or XCMS aligned/unaligned peaks)
- NeatMS example dataset (raw_data_folder_path and feature_table_path)

## Expected Outputs
- Trained neural network model file (HDF5 format)
- AUC ROC score (numeric value ≥ 0.95)
- ROC curve plot (PNG or similar)
- Training and validation accuracy curves (matplotlib figure)

## Expected Output File

- `trained_model.h5`

## Landmark Outputs

- `batches_metadata.json (or equivalent; records training/test/validation split counts)`
- `training_log.csv (epoch-wise loss and accuracy; output from TensorFlow history)`
- `auc_roc_table.csv (Probability_threshold vs True/False Positive Rate from get_true_vs_false_positive_df)`
- `roc_curve.png`

## Tools
- NeatMS
- Python
- TensorFlow
- Keras
- scikit-learn
- pandas
- NumPy
- Jupyter Notebook

## Skills
- neural-network-architecture-design
- deep-learning-training-convergence-monitoring
- overfitting-detection-and-prevention
- roc-curve-auc-metric-evaluation
- hyperparameter-tuning-learning-rate-optimizer-selection
- batch-preparation-class-imbalance-handling
- mass-spectrometry-peak-classification

## Workflow Description
1. Load raw mzML files and feature table (CSV format from mzMine or XCMS) into a NeatMS Experiment object specifying input type (mzmine or xcms). 2. Create a Neural Network Handler with default parameters (matrice_size=120, margin=1, min_scan_num=5) and call create_batches(validation_split=0.1, normalise_class=False) to generate training, test, and validation batches (80:10:10 split). 3. Initialize a fresh CNN model using create_model(lr=0.00001, optimizer='Adam') with default hyperparameters and train via train_model(1000) for an initial epoch count. 4. Monitor training and validation accuracy on the returned Keras/TensorFlow logs; if no plateau is observed, resume training by calling train_model() again with additional epochs. 5. Compute ROC curve and AUC using get_true_vs_false_positive_df() data with scikit-learn's auc() function on False Positive Rate vs. True Positive Rate. 6. Inspect training and validation accuracy curves to confirm no overfitting (training accuracy ≈ validation accuracy); if training reaches ~100% while validation lags significantly, halt training.

## Available Artifacts
| Path | Role | Indexable |
|---|---|---|
| `figures/ADAP_threshold_all_vs_recall_training_500.png` | figure | False |
| `figures/ROC_recall_High_vs_all.png` | figure | False |
| `figures/Screenshot 2020-04-28 at 16.43.33.png` | figure | False |
| `figures/annotation_tool.png` | figure | False |
| `figures/recall_table.png` | figure | False |
| `paper.md` | main_article | True |

## Missing Information
- No changelog found

## Domain Knowledge
- The default NeatMS architecture uses dropout and kernel regularization layers specifically designed to prevent overfitting; if these are present and training/validation curves diverge significantly, data quality or labeling consistency should be reviewed rather than assuming architecture failure.
- The softmax output layer produces three mutually exclusive probability distributions (one per class: High_quality, Low_quality, Noise), so AUC must be computed as a one-vs-rest macro or binary classification against a designated positive class (typically High_quality for metabolomics filtering).
- Training can be resumed by calling train_model() multiple times with different epoch counts; users must manually monitor logs to avoid severe overfitting, as NeatMS lacks built-in early stopping callbacks.
- The recommended minimum dataset size for full model training is 500 peaks per class; smaller datasets should use transfer learning instead to avoid underfitting.
- Matrix size (default 120 points) and margin (default 1, meaning margin width = peak width on each side) determine input shape; changing these parameters requires retraining from scratch and breaks compatibility with pre-trained models.

## Uncertainty Notes
- This card was generated by the LLM-assisted pipeline and needs scientific expert review.
- Each TracedClaim's evidence_span has been substring-checked against its source section; see logs/llm_calls.jsonl and capsules/<task_id>/quality_report.json for groundedness results.

## Evidence Snippets
- `ev_001` from `agent2_synthesis` (agent2_traced): [methods] Does training the NeatMS CNN model from scratch on the provided example dataset under full training conditions produce an AUC ROC score exceeding 0.9 without evidence of overfitting?: 'When choosing this option, we recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class).'
- `ev_002` from `agent2_synthesis` (agent2_traced): [intro] NeatMS relies on neural network based classification to enable automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines.: '**NeatMS** relies on neural network based classification.'
- `ev_003` from `agent2_synthesis` (agent2_traced): [other] Raw LC-MS data in mzML format: 'Raw data files in mzML format.'
- `ev_004` from `agent2_synthesis` (agent2_traced): [other] Feature table in CSV format (mzMine or XCMS aligned/unaligned peaks): 'One feature table file in .csv format (multiple if peaks are not aligned).'
- `ev_005` from `agent2_synthesis` (agent2_traced): [other] NeatMS example dataset (raw_data_folder_path and feature_table_path): 'Now that you feel confident with neural network training, let's dive in and prepare our batches.'
- `ev_006` from `agent2_synthesis` (agent2_traced): [other] Trained neural network model file (HDF5 format): 'nn_handler.class_model.save('my_own_model_020.h5')'
- `ev_007` from `agent2_synthesis` (agent2_traced): [other] AUC ROC score (numeric value ≥ 0.95): 'If correctly trained, you should obtain an AUC higher than 95.0.'
- `ev_008` from `agent2_synthesis` (agent2_traced): [other] ROC curve plot (PNG or similar): 'prob_df_roc.plot(x='False', y='True', figsize=(10,10), grid=True)'
- `ev_009` from `agent2_synthesis` (agent2_traced): [other] Training and validation accuracy curves (matplotlib figure): 'when you see no increase in the accuracy of the training and test set, you can stop the training.'
- `ev_010` from `agent2_synthesis` (agent2_traced): [other] NeatMS: 'NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object'
- `ev_011` from `agent2_synthesis` (agent2_traced): [methods] Python: 'open source python package'
- `ev_012` from `agent2_synthesis` (agent2_traced): [other] TensorFlow: 'calling the training method (1000 by default). NeatMS does not currently provides callback functions to automatically stop the training. Calling the training method will simply resume the training'
- `ev_013` from `agent2_synthesis` (agent2_traced): [methods] Keras: 'from keras.optimizers import SGD, Adam'
- `ev_014` from `agent2_synthesis` (agent2_traced): [other] scikit-learn: 'from sklearn.metrics import auc'
- `ev_015` from `agent2_synthesis` (agent2_traced): [other] pandas: 'import pandas as pd'
- `ev_016` from `agent2_synthesis` (agent2_traced): [other] NumPy: 'import numpy as np'
- `ev_017` from `agent2_synthesis` (agent2_traced): [other] Jupyter Notebook: 'You can install them through the pip command

`pip install notebook dash jupyter-dash`'
- `ev_018` from `agent2_synthesis` (agent2_traced): [discussion] No changelog found: 'No changelog found.'

## Evaluation Strategy
### Direct Checks
- verify file exists at github:bihealth__NeatMS containing example dataset referenced in cond_full_training configuration
- script_runs: execute NeatMS full model training pipeline on example dataset using default CNN architecture (convolutional base + dense classifier)
- value_in_range: AUC ROC score from trained model is >= 0.9 (metric_auc_threshold)
- output_matches_reference: training and validation loss curves show no divergence indicative of overfitting (consistent with result_no_overfitting_observed); parameter-sensitive to epoch-by-epoch loss trajectory interpretation

### Expert Review
- confirm that reported AUC ROC value of ≥0.9 represents appropriate evaluation on held-out test set (not training set)
- assess whether loss curve stability and metric consistency across epochs substantiate the claim of no overfitting observed
- verify that default CNN architecture (convolutional base + dense classifier) was applied without undocumented modifications

## Review Questions
- Is the research question correctly identified and scoped?
- Does the connected finding have enough supporting evidence?
- Which artifacts are required before this can become an executable benchmark task?
- What direct, visual, textual, or expert-review checks should be used for evaluation?

## Execution Profile
- **Compute tier:** medium

## Methodology Summary
1. Load raw mzML files and feature table (mzMine or XCMS CSV) into NeatMS Experiment object.
2. Create NN_handler and partition data into training (80%), test (10%), and validation (10%) batches using create_batches(validation_split=0.1) with default normalization (normalise_class=False).
3. Initialize untrained CNN using create_model(lr=0.00001, optimizer='Adam') with default architecture (convolutional base + dense classifier + dropout + kernel regularization).
4. Train model via iterative train_model(epoch_count) calls, monitoring training and validation accuracy logs to detect convergence and absence of overfitting.
5. Compute True Positive Rate and False Positive Rate at multiple probability thresholds using get_true_vs_false_positive_df().
6. Calculate AUC ROC using scikit-learn auc() function on threshold-swept TPR/FPR curve.
7. Validation: AUC ROC score ≥ 0.95; training accuracy and validation accuracy curves remain closely aligned (no significant divergence indicating overfitting).

## Workflow Ports

**Inputs:**

- `raw_mzml_files` — Raw LC-MS data in mzML format
- `feature_table_csv` — Feature table in CSV format

**Outputs:**

- `trained_model_h5` — Trained neural network model (HDF5)
- `auc_roc_score` — AUC ROC score (numeric)
- `roc_curve_plot` — ROC curve visualization (PNG)
- `training_history` — Training and validation accuracy curves

## Provenance

- **Source kind:** github
- **Synthesized from:** `github:bihealth__NeatMS`
- **Synthesized at:** 2026-06-16T07:21:58+00:00

## Extraction Quality
- Score: 2/5
- Coherent: false
- Placeholder detected: true
- Groundedness failures (3):
  - tools[1]: evidence_span 'open source python package' not found in section 'methods' for value='Python'
  - research_question: evidence_span about '500 peaks for each class' does not address the specific question about AUC ROC ≥0.9 or overfitting detection—it only describes dataset size recommendations, creating a semantic gap
  - finding: evidence_span is truncated ('**NeatMS** relies on neural network based classification.') and omits the complete claim about 'automated filtering of false positive MS1 peaks', creating incomplete grounding
- Notes: This card suffers from multiple alignment and grounding issues. The research_question (model performance on example dataset) and finding (NeatMS uses neural networks for filtering) are conceptually unrelated and should not be paired. The AUC threshold varies (0.9 vs 0.95) without reconciliation. Key evidence spans are either truncated, generic, or semantically distant from their claims. The evidence_span for the research_question addresses dataset size, not model performance metrics. Overfitting detection is mentioned but lacks quantitative criteria. Recommend: (1) align research_question with finding or create separate cards, (2) unify AUC threshold across all sections, (3) provide complete and article-specific evidence spans, (4) define overfitting quantitatively (e.g., max 5% gap between training/validation accuracy), (5) clarify which class label is used for one-vs-rest AUC computation.

---

*Card produced by **AgenticScienceBuilder (ASB)** — heuristic + LLM-assisted extraction from a research artifact. See the `ro-crate-metadata.json` in this capsule for full provenance.*
