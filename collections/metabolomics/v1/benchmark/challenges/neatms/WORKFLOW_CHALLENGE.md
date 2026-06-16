# Workflow Challenge: `coll_neatms_workflow`


> NeatMS is an open source Python package for automated filtering of false positive MS₁ peaks in untargeted LCMS data using neural network-based classification. The package enables users to label peaks, train or fine-tune neural network models, optimize classification thresholds, and export filtered results.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

NeatMS provides an end-to-end workflow for untargeted LCMS signal labeling and false positive peak filtering. The software implements neural network-based classification to distinguish true from false positive peaks reported by standard LCMS data processing pipelines such as mzMine and XCMS. Key functionalities include: (1) a Jupyter-based interactive annotation tool for manual peak labeling across three classes (High quality, Low quality, Noise); (2) methods to construct training, test, and validation batches with configurable parameters (matrix size of 120 points, retention time margin of 1, minimum 5 scans per peak); (3) support for full model training from scratch (requiring ≥500 peaks per class) or transfer learning with frozen convolutional layers; (4) hyperparameter optimization via threshold selection that computes true and false positive rates across probability thresholds to maximize classification accuracy; (5) data export functionality with flexible filtering by peak class, sample presence, and quality criteria. When trained on representative sample subsets using default network architecture, the model achieves AUC scores exceeding 0.95. The software is distributed under the MIT License with tutorials, example data, and pre-trained models available on GitHub.

## Research questions

- Does applying NeatMS default preprocessing to example mzML and feature-table inputs produce a peak matrix with the documented result_matrix_shape dimensions?
- What is the optimal classification threshold value returned by the get_threshold() method when applied to a labelled peak dataset using the default NeatMS neural network model?
- What are the True Positive Rate and False Positive Rate values at threshold 0.01 when applying the default NeatMS model under full training conditions?
- How does the nn_handler.create_batches() method operate when invoked with normalise_class=True versus normalise_class=False, and what are the structural differences in the resulting batch artifacts?
- Does training the NeatMS CNN model from scratch on the provided example dataset under full training conditions produce an AUC ROC score exceeding 0.9 without evidence of overfitting?

## Methods overview

Load raw mzML and feature table files into a NeatMS Experiment object using the standard import interface. Create a NN_handler with default parameters (matrix_size=120, margin=1, min_scan_num=5) to instantiate the peak matrix construction pipeline. Generate batch arrays by calling create_batches() with default 80:10:10 split ratios and no class normalization. Extract and inspect the shape and binary encoding of the peak matrices to confirm (2, 120) dimensionality and margin/peak signal partitioning. Validation: Confirm that peak matrices have shape (2, 120), binary dimension correctly encodes margin (0) and peak (1) regions with first/last 40 points and middle 40 points respectively, and batch counts match documented 80:10:10 split. Load trained NeatMS model and validation dataset containing labelled peaks across three classes (High_quality, Low_quality, Noise). Invoke get_true_vs_false_positive_df(label='High_quality') to compute true and false positive rates across a range of probability thresholds (0.0–1.0). Select the threshold value that maximizes (True positive rate − False positive rate) as the optimal decision boundary. Return the scalar threshold and the underlying metrics dataframe for downstream use in peak classification. Validation: Verify the returned threshold scalar is within expected range (0.22 ± tolerance for default model) and that the metrics dataframe contains complete probability-threshold rows with valid rate values between 0.0 and 1.0. Load the trained NeatMS model and attach it to an NN_handler instance with validation dataset. Invoke get_true_vs_false_positive_df(label='High_quality') to compute the threshold-dependent recall table across probability thresholds [0.00–0.99]. Extract the row at Probability_threshold=0.01 and read columns True, False, False_low, False_noise. Validate that True=1.0, False=0.440, False_low=0.803, and False_noise≈0.206, confirming 100% High_quality retention and 44% false positive rate composition. Validation: output metrics must exactly match the reference values reported in the methods text (True=1.0, False=0.44, Low_quality proportion=80%, Noise proportion≈20%). Load labeled experiment object containing raw LC-MS data (mzML) and feature table (CSV) from 10–20 representative samples with manual peak annotations across High_quality, Low_quality, and Noise classes. Instantiate NN_handler with default parameters (matrice_size=120, margin=1, min_scan_num=5) to configure peak matrix extraction and filtering thresholds. Invoke create_batches(validation_split=0.1, normalise_class=False) to generate training (80%), test (10%), and validation (10%) splits preserving original class-frequency distributions. Invoke create_batches(validation_split=0.1, normalise_class=True) to regenerate the same splits with class balancing, reducing all classes to the minority-class size. Extract and compare per-class peak counts across all six batches (three splits × two normalization modes) to verify that normalized batches enforce equal class cardinality and unnormalized batches preserve imbalance. Validation: Confirm that for each normalized batch, the count of High_quality peaks equals the count of Low_quality peaks equals the count of Noise peaks; and that unnormalized batches retain the original imbalanced distribution without modification. Load raw mzML files and feature table (mzMine or XCMS CSV) into NeatMS Experiment object. Create NN_handler and partition data into training (80%), test (10%), and validation (10%) batches using create_batches(validation_split=0.1) with default normalization (normalise_class=False). Initialize untrained CNN using create_model(lr=0.00001, optimizer='Adam') with default architecture (convolutional base + dense classifier + dropout + kernel regularization). Train model via iterative train_model(epoch_count) calls, monitoring training and validation accuracy logs to detect convergence and absence of overfitting. Compute True Positive Rate and False Positive Rate at multiple probability thresholds using get_true_vs_false_positive_df(). Calculate AUC ROC using scikit-learn auc() function on threshold-swept TPR/FPR curve. Validation: AUC ROC score ≥ 0.95; training accuracy and validation accuracy curves remain closely aligned (no significant divergence indicating overfitting).

**Domain:** metabolomics

**Techniques:** machine-learning, deep-learning, feature-detection, metabolite-identification, dimensionality-reduction

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** NeatMS is an open source python package for untargeted LCMS signal labelling and filtering. _[grounded: neatms_system]_
- **(finding)** NeatMS enables automated filtering of false positive MS1 peaks reported by commonly used LCMS data processing pipelines. _[grounded: neatms_system]_
- **(finding)** NeatMS relies on neural network based classification. _[grounded: neatms_system]_
- **(finding)** NeatMS is distributed as an open source software under the MIT License. _[grounded: neatms_system]_
- **(finding)** The neural network output uses a softmax activation function that produces a probability distribution of 3 probabilities between 0 and 1.
- **(finding)** The 3 probabilities in the neural network output add up to 1, with one probability per class.
- **(finding)** At a 0.01 probability threshold, 100% of High_quality peaks would be correctly predicted but 44% would be false positives. _[grounded: comp_label_high_quality]_
- **(finding)** At a 0.01 threshold, 80% of Low_quality peaks would be predicted as High_quality. _[grounded: comp_label_high_quality]_
- **(finding)** At a 0.01 threshold, 20% of Noise peaks would be predicted as High_quality. _[grounded: comp_label_high_quality]_
- **(finding)** If correctly trained, a model should obtain an AUC higher than 95.0.
- **(finding)** The matrix size argument represents the number of points used to represent a peak.
- **(finding)** The margin argument represents the size of the surrounding signal that should be kept on the retention time dimension.
- **(finding)** A margin of 1 means that the margin size on both sides of the peak will be the same size as the peak width.
- **(finding)** For a peak with a retention time width of 3 seconds and margin of 1, the extracted signal will be 9 seconds.
- **(finding)** With default argument values, the first and last 40 values of the peak represent the margins, and the middle 40 values represent the peak itself.
- **(finding)** A second dimension is added to represent the margin portion of the signal (0) or the peak signal (1).
- **(finding)** The resulting matrix size for one peak is (2, 120) with default arguments.
- **(finding)** Changing the matrix size or margin argument will automatically adapt the neural network architecture.
- **(finding)** When using transfer learning on a preexisting model, one should not change the matrix size or margin arguments if intending to use the default model. _[grounded: neatms_system]_
- **(finding)** The min_scan_number argument filters out peaks with fewer points than the specified value.
- **(finding)** The default min_scan_number value is 5 because it is difficult to judge if a signal is a peak when it has less than 5 points.
- **(finding)** The min_scan_number argument has no impact on the model architecture.
- **(finding)** When using an existing model, lowering the min_scan_number parameter is strongly advised against.
- **(finding)** Increasing the min_scan_number parameter when using an existing model is not a problem.
- **(finding)** Three batches of data are required for neural network training: one for training, one for testing, and one for validation.
- **(finding)** The training and test sets are used during the training process while the validation set remains untouched for hyperparameter tuning.
- **(finding)** The default split between training:test:validation batches is 80:10:10.
- **(finding)** The validation_split argument allows definition of the size of test and validation sets.
- **(finding)** The validation_split argument should not exceed 0.2 to ensure at least 60% of data is left for training.
- **(finding)** The normalise_class argument ensures every class has the same number of peaks for training.
- **(finding)** When normalise_class is set to True, the number of peaks for each class equals the smallest class.
- **(finding)** Full model training is recommended when there are at least 500 peaks for each class.
- **(finding)** Transfer learning should be considered if there are fewer than 500 peaks in the smallest class. _[grounded: cond_transfer_learning]_
- **(finding)** NeatMS allows changing the learning rate and optimizer for model training. _[grounded: neatms_system]_
- **(finding)** The choice of optimizers includes Adam (default) and SGD.
- **(finding)** During development and testing, the best performances were achieved using the Adam optimizer and a learning rate of 0.00001.
- **(finding)** The Adam optimizer with learning rate 0.00001 are set as default values.
- **(finding)** The model argument should be set to None for full model training from scratch. _[grounded: cond_full_training]_
- **(finding)** The number of epochs can be set when calling the training method with a default of 1000.
- **(finding)** NeatMS does not currently provide callback functions to automatically stop training. _[grounded: neatms_system]_
- **(finding)** Calling the training method will resume training for another specified number of epochs.
- **(finding)** The network architecture uses dropout and kernel regularizer to specifically prevent overfitting.
- **(finding)** Training should be stopped when there is no increase in the accuracy of the training and test set.
- **(finding)** If training set accuracy reaches close to 100% while test accuracy lags far behind, this indicates overfitting. _[grounded: tool_tensorflow]_
- **(finding)** Using the default architecture and parameters, overfitting has never happened during development.
- **(finding)** Transfer learning is appropriate when hundreds of peaks have been labelled from the dataset. _[grounded: cond_transfer_learning]_
- **(finding)** The neural network is made of a convolutional base and a classifier. _[grounded: layer_conv_base]_
- **(finding)** The convolutional base performs feature extraction while the classifier performs classification. _[grounded: layer_conv_base]_
- **(finding)** Fine tuning the convolutional base requires a bigger dataset than fine tuning only the classifier. _[grounded: layer_conv_base]_
- **(finding)** The optimal value for the default model's threshold is 0.22.
- **(finding)** A higher threshold would return more accurate but less sensitive results.
- **(finding)** A lower threshold would have the opposite effect of a higher threshold.
- **(finding)** The prediction is performed by batches of peaks, with one batch corresponding to all peaks in one sample.
- **(finding)** Running the prediction takes approximately 15 to 30 seconds per sample depending on file number and size.
- **(finding)** Every peak in the dataset is labeled with one of 3 default classes: High_quality, Low_quality, or Noise. _[grounded: comp_label_high_quality]_
- **(finding)** For optimal training, a representative subset of the dataset being analyzed should be used.
- **(finding)** Using the same sample type, sample preparation, and instrumentation results in a more specific and accurate model.
- **(finding)** Pooled samples should be selected for training as they contain a wide variety of peaks.
- **(finding)** A selection of 10 to 20 samples is enough for creating a training dataset.

**Speculative claims (excluded from scoring):**
- **(finding)** A model and the person who trained it will likely underperform for peaks with fewer than 5 points.

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- SGD optimizer
- Adam optimizer
- Use annotation labels instead of predictions

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Do not change matrix_size or margin arguments if using transfer learning on existing model
- Do not lower min_scan_number when using existing model
- Annotation tool requires Jupyter Notebook

## Steps

### Step `task_001`
- Title: Reproduce the Peak Matrix Shape from NeatMS Default Preprocessing Parameters
- Task kind: `reproduction`
- Task: Preprocess example mzML raw data and feature table using NeatMS default parameters to construct the peak matrix representation, verifying that the output matrix shape matches the documented architecture (2 dimensions × 120 points, with first/last 40 values representing signal margins and middle 40 values representing peak signal).
- Inputs:
  - Raw LC-MS data in mzML format from NeatMS example data (github.com/bihealth/NeatMS/data folder)
  - Feature table in CSV format exported from mzMine or XCMS (github.com/bihealth/NeatMS/data/test_data folder)
- Expected outputs:
  - Peak matrix arrays with shape (2, 120) per peak, where dimension 0 encodes signal intensity and dimension 1 encodes binary margin/peak classification
  - Verification report confirming first and last 40 values represent signal margins (value 0) and middle 40 values represent peak signal (value 1)
  - Batch split statistics (training, test, validation sample counts) matching 80:10:10 default split
- Tools: NeatMS, Python, NumPy, pandas
- Landmark output files: experiment_object.pkl, batch_training_arrays.npy, batch_test_arrays.npy, batch_validation_arrays.npy, matrix_shape_validation.csv
- Primary expected artifact: `peak_matrix_verification_report.txt`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce the Default Model Optimal Threshold Value via get_threshold()
- Task kind: `reproduction`
- Task: Invoke the get_threshold() method on a trained NeatMS neural network model against a validation dataset to compute the optimal probability threshold for peak classification, returning the scalar threshold value (expected ~0.22 for the default model).
- Inputs:
  - Trained NeatMS neural network model file (default model or user-trained .h5 file)
  - Labelled validation dataset with peak annotations (High_quality, Low_quality, Noise classes)
- Expected outputs:
  - Scalar threshold value (float between 0.0 and 1.0)
  - True vs. False positive rate dataframe (Probability_threshold, True, False, False_low, False_noise columns)
- Tools: NeatMS, Python, pandas, scikit-learn, NumPy
- Landmark output files: true_vs_false_positive_rates.csv, threshold_metrics_report.txt
- Primary expected artifact: `optimal_threshold_value.txt`

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce the True/False Positive Rates at Threshold 0.01 from the ROC Analysis
- Task kind: `reproduction`
- Task: Call get_true_vs_false_positive_df() on a trained NeatMS neural network model to retrieve the threshold-dependent recall table, then extract and validate True Positive Rate and False Positive Rate metrics at the 0.01 probability threshold, verifying that 100% of High_quality peaks are retained and false positives comprise 44% overall (80% Low_quality, 20% Noise).
- Inputs:
  - Trained NeatMS neural network model file (default model or custom .h5 file)
  - Validation dataset attached to the NN_handler instance (peaks remain untouched from training/test split)
- Expected outputs:
  - Recall table (DataFrame) with columns Probability_threshold, True, False, False_low, False_noise, indexed by probability threshold from 0.00 to 0.99
  - Extracted metrics at threshold 0.01: True Positive Rate = 1.0, False Positive Rate = 0.440, False_low = 0.803, False_noise = 0.206
- Tools: NeatMS, Python, pandas, NumPy, scikit-learn
- Landmark output files: recall_table_full.csv, metrics_threshold_0_01.txt
- Primary expected artifact: `recall_table_threshold_0_01.csv`

### Step `task_004`
- Depends on: `task_001`
- Title: Reconstruct the Class-Normalized Batch Creation Step for Neural Network Training
- Task kind: `component_reconstruction`
- Task: Create training/validation/test batches from a labeled LC-MS peak dataset using NeatMS.NN_handler.create_batches() with both class-normalization modes (normalise_class=True and False) at the default 80:10:10 split, producing batch artifacts and validating that class-normalized batches enforce equal peak counts across all classes.
- Inputs:
  - task_001.expected_outputs[0]: Peak matrix arrays with shape (2, 120) per peak, where dimension 0 encodes signal intensity and dimension 1 encodes binary margin/peak classification
  - Labeled LC-MS experiment object with raw mzML files and feature table (CSV format from mzMine or XCMS) containing 10–20 representative pooled samples and manually annotated peak labels (High_quality, Low_quality, Noise)
- Expected outputs:
  - Training batch artifact (80% of peaks, class-imbalanced distribution)
  - Test batch artifact (10% of peaks, class-imbalanced distribution)
  - Validation batch artifact (10% of peaks, class-imbalanced distribution)
  - Training batch artifact with equal class counts (80% of normalized peaks, all classes equal to smallest class size)
  - Test batch artifact with equal class counts (10% of normalized peaks, all classes equal to smallest class size)
  - Validation batch artifact with equal class counts (10% of normalized peaks, all classes equal to smallest class size)
  - Verification report documenting per-class peak counts in each batch condition (normalise_class=False vs True)
- Tools: NeatMS, Python
- Landmark output files: train_batch_unnormalized.pkl, test_batch_unnormalized.pkl, val_batch_unnormalized.pkl, train_batch_normalized.pkl, test_batch_normalized.pkl, val_batch_normalized.pkl
- Primary expected artifact: `batch_verification_report.txt`

### Step `task_005`
- Depends on: `task_004`
- Title: Reproduce the AUC ROC Score Exceeding 0.9 Under Full Training Condition
- Task kind: `reproduction`
- Task: Train a NeatMS convolutional neural network from scratch on an example LC-MS dataset using the default architecture (convolutional base + dense classifier with dropout and kernel regularization) and report the Area Under the ROC Curve (AUC) score, verifying it exceeds 0.95 and confirming absence of overfitting.
- Inputs:
  - task_004.expected_outputs[0]: Training batch artifact (80% of peaks, class-imbalanced distribution)
  - Raw LC-MS data in mzML format
  - Feature table in CSV format (mzMine or XCMS aligned/unaligned peaks)
  - NeatMS example dataset (raw_data_folder_path and feature_table_path)
- Expected outputs:
  - Trained neural network model file (HDF5 format)
  - AUC ROC score (numeric value ≥ 0.95)
  - ROC curve plot (PNG or similar)
  - Training and validation accuracy curves (matplotlib figure)
- Tools: NeatMS, Python, TensorFlow, Keras, scikit-learn, pandas, NumPy, Jupyter Notebook
- Landmark output files: batches_metadata.json (or equivalent; records training/test/validation split counts), training_log.csv (epoch-wise loss and accuracy; output from TensorFlow history), auc_roc_table.csv (Probability_threshold vs True/False Positive Rate from get_true_vs_false_positive_df), roc_curve.png
- Primary expected artifact: `trained_model.h5`

## Final expected outputs

- `Scalar threshold value (float between 0.0 and 1.0)` (type: file, tolerance: hash)
- `True vs. False positive rate dataframe (Probability_threshold, True, False, False_low, False_noise columns)` (type: file, tolerance: hash)
- `Recall table (DataFrame) with columns Probability_threshold, True, False, False_low, False_noise, indexed by probability threshold from 0.00 to 0.99` (type: file, tolerance: hash)
- `Extracted metrics at threshold 0.01: True Positive Rate = 1.0, False Positive Rate = 0.440, False_low = 0.803, False_noise = 0.206` (type: file, tolerance: hash)
- `Trained neural network model file (HDF5 format)` (type: file, tolerance: hash)
- `AUC ROC score (numeric value ≥ 0.95)` (type: file, tolerance: hash)
- `ROC curve plot (PNG or similar)` (type: file, tolerance: hash)
- `Training and validation accuracy curves (matplotlib figure)` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** flat

- **Abstraction level:** intermediate

- **Orchestration planning:** static

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_neatms_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Scalar threshold value (float between 0.0 and 1.0)": "<locator>",
    "True vs. False positive rate dataframe (Probability_threshold, True, False, False_low, False_noise columns)": "<locator>",
    "Recall table (DataFrame) with columns Probability_threshold, True, False, False_low, False_noise, indexed by probability threshold from 0.00 to 0.99": "<locator>",
    "Extracted metrics at threshold 0.01: True Positive Rate = 1.0, False Positive Rate = 0.440, False_low = 0.803, False_noise = 0.206": "<locator>",
    "Trained neural network model file (HDF5 format)": "<locator>",
    "AUC ROC score (numeric value \u2265 0.95)": "<locator>",
    "ROC curve plot (PNG or similar)": "<locator>",
    "Training and validation accuracy curves (matplotlib figure)": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
