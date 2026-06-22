---
name: taxonomy-classification-evaluation
description: Use when you have a pre-trained model (or candidate models) and need to assess whether it generalizes better than existing synthetic-molecule baselines on natural product taxonomy classification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3928
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0602
  tools:
  - NaFM
  - train.py
  - inference.py
  - scikit-learn
derived_from:
- doi: 10.1002/anie.202507483
  title: NA
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_nafm_cq
    doi: 10.1002/anie.202507483
    title: NA
  dedup_kept_from: coll_nafm_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/anie.202507483
  all_source_dois:
  - 10.1002/anie.202507483
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# taxonomy-classification-evaluation

## Summary

Benchmarking a foundation model's taxonomy classification performance against synthetic-molecule pre-trained baselines on natural product datasets using standardized metrics. This skill validates whether a model captures natural synthesis patterns through quantitative comparison of accuracy, precision, recall, and F1-score across taxonomy classes.

## When to use

You have a pre-trained model (or candidate models) and need to assess whether it generalizes better than existing synthetic-molecule baselines on natural product taxonomy classification. This is the right skill when your goal is to demonstrate superiority or inadequacy of a model's ability to capture evolutionary and biosynthetic patterns reflected in hierarchical taxonomy (Class, Superclass, Pathway levels).

## When NOT to use

- Input dataset is not a natural product collection—if molecules are synthetic or from standard chemical libraries, synthetic-baseline comparison loses interpretive power.
- No held-out test set is available or test set was used during model selection—evaluation must use truly unseen data to avoid overfitting bias.
- Baseline models are not publicly available or reproducible—comparison requires equivalent computational setups and hyperparameters to ensure fair benchmarking.

## Inputs

- Pre-trained foundation model checkpoint (e.g., NaFM.ckpt)
- Baseline model checkpoints (synthetic-molecule pre-trained, e.g., ChemBERTa)
- Taxonomy classification dataset with SMILES and class labels (CSV format with molecule identifiers, SMILES strings, and hierarchical taxonomy annotations)
- Train/validation/test set splits or instructions for stratified splitting

## Outputs

- Per-class accuracy, precision, recall, F1-score metrics for each model
- Summary comparison table (models × metrics) showing absolute values and differences
- Statistical significance test results (p-values, confidence intervals)
- Qualitative interpretation of whether synthetic pre-training is inadequate for natural synthesis patterns

## How to apply

Load the pre-trained foundation model weights and one or more baseline models pre-trained on synthetic molecules (e.g., ChemBERTa, MolBERT). Obtain a labeled natural product taxonomy dataset (e.g., Ontology classification data) and split into train/validation/test sets. Evaluate each model on the held-out test set, computing accuracy, precision, recall, and F1-score for each taxonomy class. Generate a summary comparison table showing metric differences between the foundation model and baselines. Statistical significance testing (e.g., paired t-tests or McNemar's test) can strengthen the comparison. The evaluation targets whether synthetic pre-training inadequately captures natural synthesis patterns—if foundation model metrics substantially exceed baselines, this validates the claim.

## Related tools

- **NaFM** (Pre-trained foundation model checkpoint to be evaluated on taxonomy classification) — https://github.com/TomAIDD/NaFM-Official
- **train.py** (Script to load and evaluate models on downstream classification tasks with configurable hyperparameters) — https://github.com/TomAIDD/NaFM-Official
- **inference.py** (Script to run inference on new molecules for classification predictions) — https://github.com/TomAIDD/NaFM-Official
- **scikit-learn** (Compute accuracy, precision, recall, F1-score, and statistical significance metrics)

## Examples

```
python train.py --task finetune --dataset Ontology --dataset-root downstream_data/Ontology --pretrained-path NaFM.ckpt --num-epochs 300 --batch-size 256 --dataset-arg Class --seed 0
```

## Evaluation signals

- Foundation model F1-score exceeds all baseline models by a statistically significant margin (p < 0.05 on paired tests) for at least the majority of taxonomy classes.
- Per-class precision and recall are balanced (difference < 0.05 between the two) indicating the model is not biased toward false positives or false negatives on natural products.
- Baseline models (synthetic pre-trained) show lower performance on natural product taxonomy compared to their reported performance on synthetic datasets, validating the inadequacy claim.
- Test set size is ≥ 100 molecules per class to ensure sufficient statistical power; macro-averaged F1 is reported alongside per-class metrics.
- Confusion matrix for foundation model shows fewer misclassifications between hierarchically related classes (e.g., different pathways within the same superclass) compared to baselines.

## Limitations

- Evaluation scripts (test.py) in the repository are described as lightweight demonstration templates, not production pipelines; minor hyperparameter adjustments (learning rate, epochs, early stopping patience) may be necessary depending on dataset and training environment.
- The benchmark is specific to the Ontology dataset and hierarchical taxonomy levels (Class, Superclass, Pathway); generalization to other natural product classification schemes is not guaranteed.
- Statistical significance depends on test set size and class imbalance; imbalanced datasets may require weighted metrics or stratified sampling to ensure fair comparison.

## Evidence

- [intro] We first benchmark NaFM on taxonomy classification against models pre-trained on synthetic molecules, demonstrating their inadequacy for capturing natural synthesis patterns: "We first benchmark NaFM on taxonomy classification against models pre-trained on synthetic molecules, demonstrating their inadequacy for capturing natural synthesis patterns"
- [other] Evaluate NaFM on the held-out test set, computing accuracy, precision, recall, and F1-score for each taxonomy class. Load baseline models pre-trained on synthetic molecules (e.g., ChemBERTa, MolBERT, or other standard molecular pre-training frameworks). Evaluate each baseline model on the same test set using identical metrics. Compare NaFM performance against baselines and generate a summary table showing metric differences and statistical significance.: "Evaluate NaFM on the held-out test set, computing accuracy, precision, recall, and F1-score for each taxonomy class"
- [readme] Supports hierarchical classification at **Class**, **Superclass**, and **Pathway** levels.: "Supports hierarchical classification at **Class**, **Superclass**, and **Pathway** levels"
- [readme] The configs under ```examples/``` are example settings used for running the provided tasks. Some downstream tasks may require minor adjustment of parameters such as learning rate, training epochs, or early stopping patience depending on the dataset and training environment.: "Some downstream tasks may require minor adjustment of parameters such as learning rate, training epochs, or early stopping patience depending on the dataset and training environment"
- [readme] The repository includes lightweight demonstration scripts intended to illustrate the basic inference workflow and input/output usage of NaFM. In particular, ```test.py``` should be regarded as a minimal demonstration template rather than the exact production evaluation pipeline used to generate the benchmark results reported in the paper.: "```test.py``` should be regarded as a minimal demonstration template rather than the exact production evaluation pipeline"
