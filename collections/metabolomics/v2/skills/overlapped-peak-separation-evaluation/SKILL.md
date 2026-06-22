---
name: overlapped-peak-separation-evaluation
description: Use when you have trained a GCMSFormer Transformer model on augmented simulated overlapped peaks and need to measure its generalization performance on unseen test data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - PyTorch
  - Python 3
  - conda
  - GCMSFormer
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# overlapped-peak-separation-evaluation

## Summary

Evaluate the performance of a Transformer-based model (GCMSFormer) for resolving overlapped peaks in GC-MS data by computing BLEU score on a held-out test set of simulated overlapped peaks. This skill assesses whether the model can accurately predict pure mass spectra and concentration distributions for complex mixtures.

## When to use

You have trained a GCMSFormer Transformer model on augmented simulated overlapped peaks and need to measure its generalization performance on unseen test data. Apply this skill when you have a partitioned dataset (8:1:1 train/validation/test split) and want to validate that the model achieves the reported BLEU score benchmark (0.9988) or compare against a target threshold for mass spectral prediction accuracy.

## When NOT to use

- Test set is not held-out or overlaps with training/validation data (violates independence assumption for BLEU score validity).
- Input peaks are not simulated overlapped peaks or do not follow the 100,000 augmented dataset distribution and augmentation protocol used for model training.
- Model has not completed training and checkpoint selection on the validation set; premature evaluation will not reflect true generalization.

## Inputs

- trained GCMSFormer Transformer model (PyTorch checkpoint)
- test set partition: 10,000 augmented simulated overlapped peaks (8:1:1 split)
- target vocabulary (tgt_vacob) mapping mass spectral tokens
- ground-truth pure mass spectra for test samples

## Outputs

- BLEU score (scalar, range 0–1; reported benchmark 0.9988)
- predicted mass spectral matrix S for all test samples
- predicted concentration distribution matrix C for all test samples
- per-sample evaluation metrics and error analysis

## How to apply

Load the trained GCMSFormer model checkpoint and the held-out test set (10,000 augmented simulated overlapped peaks in a standard 8:1:1 split). Run inference on the test set to generate predicted mass spectral matrices (S) and concentration distributions (C) using the model's Transformer encoder–decoder architecture. Compute the BLEU (Bilingual Evaluation Understudy) score metric comparing predicted mass spectra sequences against ground-truth pure component spectra. Report the test-set BLEU score and verify reproducibility against the reported benchmark of 0.9988. BLEU score directly measures the fidelity of predicted mass spectral peak sequences, serving as a proxy for the quality of overlapped peak deconvolution.

## Related tools

- **PyTorch** (Deep learning framework for loading the trained Transformer model and running inference on test set samples) — https://pytorch.org/
- **Python 3** (Programming language for implementing model evaluation loop and BLEU metric computation) — https://www.python.org/
- **GCMSFormer** (The Transformer model repository providing the trained checkpoint, inference functions, and BLEU evaluation interface) — https://github.com/zxguocsu/GCMSFormer
- **conda** (Environment manager for installing PyTorch, Python 3, and all dependencies required for model evaluation) — https://conda.io/docs/user-guide/install/download.html

## Examples

```
model, Loss = train_model(para, TRAIN, VALID, tgt_vacob); from GCMSFormer.GCMSformer import evaluate; bleu_score = evaluate(model, TEST, tgt_vacob, device='cuda')
```

## Evaluation signals

- Computed BLEU score on test set matches or exceeds the reported benchmark of 0.9988, indicating reproducible model performance.
- BLEU score is computed only on the held-out test partition (10,000 samples) with no data leakage from train or validation sets.
- Predicted mass spectral sequences (output of Transformer decoder) tokenize correctly and are comparable in length and structure to ground-truth spectra.
- Predicted concentration distribution matrix C is non-negative and sums to a physically valid total (e.g., per-sample mass balance check).
- Per-sample BLEU scores show low variance across the test set, indicating stable and generalizable model behavior across diverse overlapped peak configurations.

## Limitations

- BLEU score measures sequence-level token overlap and may not fully capture the chemical accuracy of predicted mass spectra or concentration recovery (chemical validation required separately).
- Evaluation is restricted to simulated overlapped peaks with known ground truth; performance on real GC-MS data with measurement noise and unknown peak composition may differ substantially.
- BLEU score assumes a fixed vocabulary (tgt_vacob) and tokenization scheme; changes to augmentation parameters or token definitions will affect reproducibility.
- The 8:1:1 train/validation/test split is fixed; results are not generalizable to different data partitioning or external datasets with different peak distributions or augmentation strategies.

## Evidence

- [intro] GCMSFormer achieved a BLEU score of 0.9988 on the test set when trained, validated, and tested with 100,000 augmented simulated overlapped peaks in an 8:1:1 ratio.: "its bilingual evaluation understudy (BLEU) on the test set was 0.9988"
- [intro] The evaluation process involves partitioning the augmented dataset, training the model with validation checkpointing, and then computing BLEU on the held-out test set.: "The GCMSFormer model was trained, validated, and tested with 100,000 augmented simulated overlapped peaks in a ratio of 8:1:1"
- [readme] BLEU score serves as the primary metric for assessing the quality of predicted mass spectral sequences in the deconvolution task.: "its bilingual evaluation understudy (BLEU) on the test set was 0.9988. With the aid of the orthogonal projection resolution method (OPR), GCMSFormer can predict the pure mass spectra"
- [intro] The model outputs both mass spectral predictions and concentration distributions, which together constitute the complete deconvolution result.: "GCMSFormer can predict the pure mass spectra of all components in overlapped peaks (mass spectral matrix S), and then use the least squares method to find the concentration distribution matrix C"
- [readme] PyTorch and Python 3 are required dependencies for running model inference and evaluation.: "- [python3](https://www.python.org/) - [pytorch](https://pytorch.org/)"
