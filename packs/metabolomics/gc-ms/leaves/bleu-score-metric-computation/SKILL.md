---
name: bleu-score-metric-computation
description: Use when you have a trained sequence-to-sequence model (such as GCMSFormer) that predicts mass spectra from overlapped peaks, and you need to evaluate model performance on a held-out test set.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - PyTorch
  - Python 3
  - conda
  - GCMSFormer
  techniques:
  - GC-MS
derived_from:
- doi: 10.1021/acs.analchem.3c05772
  title: GCMSFormer
evidence_spans:
- '[pytorch](https://pytorch.org/)'
- '[python3](https://www.python.org/)'
- We recommend to use [conda](https://conda.io/docs/user-guide/install/download.html)
- We recommend to use [conda](https://conda.io/docs/user-guide/install/download.html).
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gcmsformer_cq
    doi: 10.1021/acs.analchem.3c05772
    title: GCMSFormer
  dedup_kept_from: coll_gcmsformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.3c05772
  all_source_dois:
  - 10.1021/acs.analchem.3c05772
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# bleu-score-metric-computation

## Summary

Compute the BLEU (bilingual evaluation understudy) score to quantify the quality of predicted mass spectra against reference spectra in overlapped peak resolution tasks. This metric measures n-gram precision and is commonly used in sequence-to-sequence models like GCMSFormer to evaluate how well predicted pure mass spectral matrices match ground-truth spectra.

## When to use

Apply this skill when you have a trained sequence-to-sequence model (such as GCMSFormer) that predicts mass spectra from overlapped peaks, and you need to evaluate model performance on a held-out test set. Use BLEU score specifically when you want a standard, reference-based metric for comparing predicted spectral sequences to ground-truth spectra in machine learning benchmarking workflows.

## When NOT to use

- When comparing spectra without reference ground-truth labels (BLEU requires reference sequences); use similarity-based metrics (cosine, spectral angle) instead.
- When the test set is not held out during training and validation; BLEU scores on training/validation data are not reliable performance indicators.
- When predicted outputs are not sequence-structured mass spectra; BLEU is designed for sequence comparison and does not apply to unstructured or tabular outputs.

## Inputs

- Trained GCMSFormer Transformer model checkpoint
- Test set of simulated overlapped peaks (10,000 samples in 8:1:1 split)
- Reference/ground-truth mass spectral matrices for test samples
- Model prediction outputs on test set

## Outputs

- BLEU score (float, 0–1 range)
- Per-sample or aggregate n-gram precision scores
- Evaluation report with reproducibility verification

## How to apply

After training and validating your GCMSFormer model on augmented simulated overlapped peaks data (partitioned into train/validation/test sets in an 8:1:1 ratio), evaluate the trained model on the held-out test set (e.g., 10,000 samples) by running inference to generate predicted mass spectral matrices. Compute the BLEU score metric on the test set predictions against reference spectra using the model evaluation pipeline. The BLEU score ranges from 0 to 1, where higher values (e.g., 0.9988) indicate better alignment between predicted and reference spectral sequences. Verify reproducibility by confirming the reported benchmark score is achieved under identical data splits, hyperparameters, and random seeds.

## Related tools

- **PyTorch** (Deep learning framework for model training, validation, and inference; used to run the trained GCMSFormer model on test data and generate predictions for BLEU computation) — https://pytorch.org/
- **GCMSFormer** (Transformer-based model for predicting pure mass spectra from overlapped peaks; the model whose test-set performance is evaluated by BLEU score) — https://github.com/zxguocsu/GCMSFormer
- **Python 3** (Programming language for scripting the BLEU metric computation and model evaluation pipeline) — https://www.python.org/

## Examples

```
# After training GCMSFormer, evaluate on test set:
from GCMSFormer import train_model, Resolution
model, Loss = train_model(para, TRAIN, VALID, tgt_vacob)
test_predictions = model.predict(TEST)  # Generate predictions
bleu_score = compute_bleu(test_predictions, TEST_references)  # Compute BLEU against reference spectra
print(f'BLEU score: {bleu_score}')
```

## Evaluation signals

- BLEU score on test set should match or exceed the reported benchmark of 0.9988 when using identical data split (8:1:1), model architecture, and training hyperparameters.
- Score should be computed only on the held-out test set (10,000 samples), not on training or validation data.
- BLEU score should be reproducible across multiple runs with fixed random seeds and identical model checkpoints.
- Individual n-gram precisions (1-gram, 2-gram, 3-gram, 4-gram) should all be high (> 0.99) for strong model performance; any significant drop in higher-order n-grams indicates worse sequence quality.
- Score computation should not include samples from the training (80,000) or validation (10,000) sets; data leakage invalidates the metric.

## Limitations

- BLEU score requires reference ground-truth spectra; it cannot be computed for real GC-MS data without prior chemical analysis or literature reference standards.
- BLEU is a reference-based metric and does not directly measure chemical validity or peak resolution accuracy; high BLEU does not guarantee that predicted concentrations or mass spectra are chemically correct.
- Score is sensitive to the choice of n-gram weights and smoothing parameters; results may not be directly comparable across implementations if these parameters differ.
- On small test sets (< 1,000 samples), BLEU scores may have higher variance; the reported benchmark uses 10,000 test samples for stable evaluation.

## Evidence

- [intro] its bilingual evaluation understudy (BLEU) on the test set was 0.9988: "its bilingual evaluation understudy (BLEU) on the test set was 0.9988"
- [intro] The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1: "The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1"
- [other] Evaluate the trained model on the held-out test set and compute BLEU score metric.: "Evaluate the trained model on the held-out test set and compute BLEU score metric."
- [other] Report test-set BLEU score and verify reproducibility against the reported benchmark of 0.9988.: "Report test-set BLEU score and verify reproducibility against the reported benchmark of 0.9988."
