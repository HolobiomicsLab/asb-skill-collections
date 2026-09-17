---
name: class-imbalance-mitigation-via-normalization
description: Use when preparing training batches for a neural network classifier on
  LCMS peak data where class counts are unequal (e.g., more high-quality peaks than
  low-quality peaks).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - NeatMS
  - Python
  - Keras
  - TensorFlow
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.1c02220
  title: neatms
evidence_spans:
- NeatMS provides the necessary functions to do that, all we will have to do is create
  a `Neural network handler` object
- Calling the method `get_threshold()` will compute and return the optimal threshold
- After installation, you should be able to import NeatMS
- Import the required libraries first
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_neatms
    doi: 10.1021/acs.analchem.1c02220
    title: neatms
  dedup_kept_from: coll_neatms
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02220
  all_source_dois:
  - 10.1021/acs.analchem.1c02220
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# class-imbalance-mitigation-via-normalization

## Summary

Balance class representation in neural network training batches by enforcing equal peak counts across all classes, set to the smallest class size. This mitigates training bias toward overrepresented classes in imbalanced LCMS labeling datasets.

## When to use

Apply this skill when preparing training batches for a neural network classifier on LCMS peak data where class counts are unequal (e.g., more high-quality peaks than low-quality peaks). Use it to prevent the model from preferentially learning the overrepresented class at the expense of classification accuracy on minority classes.

## When NOT to use

- Input dataset already has equal class sizes or balanced representation—normalization will discard data unnecessarily.
- You require maximum data retention for a very small dataset; normalization will downsample to the smallest class, reducing total training size.
- The analytical goal is to preserve and study class imbalance patterns or rare-event detection; normalization obscures the true population distribution.

## Inputs

- NN_handler object (instantiated with experiment, matrice_size, margin, min_scan_num)
- labeled LCMS peak dataset with multiple classes (e.g., high-quality, low-quality, artifact)
- validation_split parameter (float, e.g., 0.1)

## Outputs

- training batch (80% of balanced peaks)
- validation batch (e.g., 10% of balanced peaks)
- test batch (e.g., 10% of balanced peaks)
- batch metadata with equal peak counts per class per batch

## How to apply

After instantiating an NN_handler object with your experiment data and specifying matrix size (e.g., 120), margin (e.g., 1), and minimum scan filtering (e.g., min_scan_num=5), invoke nn_handler.create_batches() with the parameter normalise_class=True. This will automatically downsample all classes to match the peak count of the smallest class, ensuring that training, validation, and test batches each contain equal representations of every class. Set validation_split (e.g., 0.1 for 10%) to define the validation fraction. Inspect the resulting batch metadata to verify that peak counts per class are identical across all batches and equal to the smallest class size. Compare this to a baseline run with normalise_class=False to confirm class balancing has been applied.

## Related tools

- **NeatMS** (Provides NN_handler object and create_batches() method with normalise_class parameter for enforcing equal class representation in training batches) — https://github.com/bihealth/NeatMS
- **Keras** (Neural network training framework used downstream after batch creation for model optimization)
- **TensorFlow** (Backend for Keras-based neural network training on balanced batches)

## Examples

```
nn_handler.create_batches(validation_split=0.1, normalise_class=True)
```

## Evaluation signals

- Verify that the peak count per class in each batch equals min(class_counts) from the original dataset.
- Confirm that all classes have identical peak counts within training, validation, and test batches.
- Compare batch class distributions with normalise_class=False to ensure True reduces imbalance variance to zero.
- Check that total peaks per batch equals (number_of_classes × smallest_class_count).
- Validate that no class is represented with fewer peaks than originally present in the smallest class.

## Limitations

- Normalization reduces total training data by discarding peaks from overrepresented classes; datasets with very small minority classes will have significantly fewer total training examples.
- The method assumes all classes are equally important for the downstream task; if rare-event classes should be underweighted or overweighted based on domain knowledge, uniform balancing is inappropriate.
- No in-built mechanism to handle newly imbalanced or drifting class distributions during transfer learning or model fine-tuning on new datasets.

## Evidence

- [other] when normalise_class is set to True, the create_batches() method ensures that every class has an equal number of peaks in the resulting training batches, with the total number of peaks per class equal to the smallest class count: "When normalise_class is set to True, the create_batches() method ensures that every class has an equal number of peaks in the resulting training batches, with the total number of peaks per class"
- [methods] normalise_class argument allows you to make sure every class has the same number of peaks for the training, when set to True, the number of peaks for each class will be equal to the smallest: "The `normalise_class` argument allows you to make sure every class has the same number of peaks for the training, when set to `True`, the number of peaks for each class will be equal to the smallest"
- [methods] NeatMS provides the necessary functions to do that, all we will have to do is create a Neural network handler object and call the batch creation method: "NeatMS provides the necessary functions to do that, all we will have to do is create a `Neural network handler` object and call the batch creation method."
- [other] when set to False, class counts remain unequal, reflecting the original distribution in the dataset: "when set to False, class counts remain unequal, reflecting the original distribution in the dataset"
