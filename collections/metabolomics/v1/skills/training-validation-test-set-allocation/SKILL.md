---
name: training-validation-test-set-allocation
description: Use when after labeling a representative subset of peaks (typically 10–20 pooled samples with corresponding feature tables) and before neural network training, when you need to split labeled data into independent subsets for model training, hyperparameter tuning, and unbiased performance evaluation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0634
  tools:
  - NeatMS
  - Python
  - NumPy
derived_from:
- doi: 10.1021/acs.analchem.1c02220
  title: neatms
evidence_spans:
- NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object
- Calling the method `get_threshold()` will compute and return the optimal threshold
- After installation, you should be able to import NeatMS
- Import the required libraries first
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_neatms
    doi: 10.1021/acs.analchem.1c02220
    title: neatms
  dedup_kept_from: coll_neatms
schema_version: 0.2.0
---

# training-validation-test-set-allocation

## Summary

Partition labeled LCMS peak data into training, validation, and test sets with optional class balancing to ensure neural network models are trained on representative data without leakage and evaluated fairly. In NeatMS, this is performed via the nn_handler.create_batches() method, which supports both class-normalized (equal peaks per class) and unnormalized (original distribution) allocation strategies.

## When to use

After labeling a representative subset of peaks (typically 10–20 pooled samples with corresponding feature tables) and before neural network training, when you need to split labeled data into independent subsets for model training, hyperparameter tuning, and unbiased performance evaluation. Use this skill when class imbalance in your labeled peaks would bias training (normalise_class=True) or when you want to preserve the original class distribution for realistic model evaluation (normalise_class=False).

## When NOT to use

- Input data is already a pre-split or pre-allocated training/validation/test set (avoid double-splitting or conflicting allocation schemes).
- Labeled peak count is less than ~100 peaks total per class for full model training (small datasets may benefit from transfer learning instead of train/val/test splitting; NeatMS recommends ≥500 peaks per class minimum).
- Peak labels are not yet assigned or Experiment object is not fully annotated; complete the annotation phase first.

## Inputs

- Labeled Experiment object (ntms.Experiment with raw LCMS data folder, feature table(s), and manually annotated peak classes)
- NN_handler instance configured with matrix size, margin, and min_scan_num filter
- Integer validation_split parameter (e.g., 0.1 for 10%)
- Boolean normalise_class parameter (True or False)

## Outputs

- Training batch artifact (80% of labeled peaks, class-normalized or original distribution)
- Validation batch artifact (10% of labeled peaks)
- Test batch artifact (10% of labeled peaks)
- Batch metadata (peak counts per class per batch, class distribution statistics)

## How to apply

Instantiate an NN_handler object from a loaded Experiment with ntms.NN_handler(experiment, matrice_size=120, margin=1, min_scan_num=5), then invoke nn_handler.create_batches(validation_split=0.1, normalise_class=True_or_False) to partition the labeled peaks. When normalise_class=True, the method subsamples all classes to match the smallest class count, ensuring balanced representation in each batch (training 80%, validation 10%, test 10% by default). When normalise_class=False, the original class distribution is preserved across batches. Inspect the resulting batch metadata (peak counts per class per batch) to verify that normalized batches satisfy the constraint that every class has equal peak counts, while unnormalized batches reflect the original imbalance. The choice between normalization strategies depends on whether class imbalance in your labeled data is representative of the real sample population or an artifact of labeling effort.

## Related tools

- **NeatMS** (Primary tool providing NN_handler.create_batches() method for reproducible batch allocation with optional class normalization.) — https://github.com/bihealth/NeatMS
- **Python** (Runtime environment for calling NeatMS NN_handler API and scripting batch allocation workflows.)
- **NumPy** (Underlying numerical library used by NeatMS for batch array operations and class subsampling.)

## Examples

```
nn_handler.create_batches(validation_split=0.1, normalise_class=True)
```

## Evaluation signals

- Training, validation, and test batches sum to 100% of input labeled peaks (minus any dropped by min_scan_num or other filters).
- When normalise_class=True: all classes have identical peak counts within each batch, equal to the minimum class count from the input; when normalise_class=False: class counts in batches reflect the original distribution.
- No peak appears in more than one batch (no leakage); each batch is a disjoint subset.
- Batch sizes (peak counts per batch) and class distributions are logged or exportable via batch metadata inspection.
- Validation and test set sizes match the specified validation_split ratio (e.g., 0.1 → ~10% of total peaks per batch type).

## Limitations

- Class normalization (normalise_class=True) discards peaks from overrepresented classes to match the smallest class; this reduces effective training set size and may lose information about class diversity if the smallest class is very small.
- The method does not automatically stratify batches by other metadata (e.g., sample or replicate origin); users must verify that validation/test sets contain independent samples, not replicates of training samples.
- Recommended minimum of ~500 peaks per class is not automatically enforced; users must manually verify adequate labeled data before allocation.
- No explicit support for multi-label or hierarchical class structures; all peaks are assumed to have a single class label.

## Evidence

- [other] When normalise_class is set to True, the create_batches() method ensures that every class has an equal number of peaks in the resulting training batches, with the total number of peaks per class equal to the smallest class count: "When normalise_class is set to True, the create_batches() method ensures that every class has an equal number of peaks in the resulting training batches, with the total number of peaks per class"
- [methods] The `normalise_class` argument allows you to make sure every class has the same number of peaks for the training, when set to `True`, the number of peaks for each class will be equal to the smallest: "The `normalise_class` argument allows you to make sure every class has the same number of peaks for the training, when set to `True`, the number of peaks for each class will be equal to the smallest"
- [other] Load a labeled experiment object into NeatMS using ntms.Experiment(raw_data_folder_path, feature_table_path, input_data) with 10–20 pooled representative samples and their corresponding feature tables. 2. Instantiate an NN_handler object with ntms.NN_handler(experiment, matrice_size=120, margin=1, min_scan_num=5): "Load a labeled experiment object into NeatMS using ntms.Experiment(raw_data_folder_path, feature_table_path, input_data) with 10–20 pooled representative samples and their corresponding feature"
- [methods] NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object and call the batch creation method.: "NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object and call the batch creation method."
- [methods] When choosing this option, we recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class).: "When choosing this option, we recommend that you have at the very least 500 peaks for each class (or 500 peaks in the smallest class)."
