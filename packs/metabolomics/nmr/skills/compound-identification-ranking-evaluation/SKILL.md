---
name: compound-identification-ranking-evaluation
description: Use when after training a FlavorFormer model end-to-end with weighted loss on 1H NMR spectra and compound labels, apply this skill to a held-out test set to measure compound identification accuracy and ranking quality.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3382
  - http://edamontology.org/topic_0092
  tools:
  - Python
  - Anaconda
  - PyTorch
  - FlavorFormer
  - Python 3.13.2
  techniques:
  - GC-MS
  - NMR
derived_from:
- doi: 10.1016/j.microc.2025.115372
  title: FlavorFormer
evidence_spans:
- Python 3.13.2 and Pytorch (version 2.7.0+cu118)
- Install [Anaconda](https://www.anaconda.com/).
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_flavorformer_cq
    doi: 10.1016/j.microc.2025.115372
    title: FlavorFormer
  dedup_kept_from: coll_flavorformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.microc.2025.115372
  all_source_dois:
  - 10.1016/j.microc.2025.115372
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Compound Identification Ranking Evaluation

## Summary

Evaluate the performance of a hybrid deep learning model (FlavorFormer) on compound identification tasks by computing accuracy metrics and ranking-based performance indicators on held-out NMR spectral data. This skill assesses whether the bi-encoder/cross-encoder architecture correctly ranks and identifies compounds in flavor mixtures.

## When to use

After training a FlavorFormer model end-to-end with weighted loss on 1H NMR spectra and compound labels, apply this skill to a held-out test set to measure compound identification accuracy and ranking quality. Use it when you need to validate that the fusion pooling and dual-encoder strategy produces reliable compound rankings from new mixture spectra.

## When NOT to use

- Model has not yet been trained end-to-end; use this only after backpropagation with weighted loss is complete.
- Test set is not held-out or is contaminated with training data; ranking metrics will be artificially inflated.
- Compound labels are incomplete or ambiguous; ground truth must be unambiguous to interpret ranking correctness.
- Input spectra are not preprocessed to the same scale and format as training data; preprocessing mismatch will degrade rankings.

## Inputs

- Trained FlavorFormer model checkpoint (PyTorch state_dict)
- Preprocessed 1H NMR spectral data (test set)
- Ground-truth compound labels for test spectra
- Compound reference embeddings or reference library

## Outputs

- Compound identification accuracy metric (percentage or absolute count)
- Ranking performance metrics (e.g., mean reciprocal rank, NDCG, ranking precision)
- Performance report (text or JSON document)
- Per-sample prediction scores and rankings (for error analysis)

## How to apply

Load the trained FlavorFormer model checkpoint and the held-out test set of preprocessed 1H NMR spectra with ground-truth compound labels. Generate predictions by passing spectra through the hybrid CNN-Transformer backbone and both encoder branches (bi-encoder and cross-encoder). Compute compound identification accuracy by comparing predicted compound rankings to ground truth. Calculate ranking metrics (e.g., mean reciprocal rank, normalized discounted cumulative gain, or ranking precision at k) to assess how well the fused logits from both encoders rank true compounds at the top of the candidate list. Document the performance report with both accuracy and ranking metrics as evidence that the weighted loss successfully balanced bi-encoder and cross-encoder contributions.

## Related tools

- **PyTorch** (Deep learning framework for loading trained model, running inference on test spectra, and computing evaluation metrics)
- **FlavorFormer** (Trained hybrid CNN-Transformer model with bi-encoder and cross-encoder branches for compound identification) — https://github.com/yfWang01/FlavorFormer
- **Python 3.13.2** (Runtime environment for executing evaluation scripts and ranking metric calculations)

## Evaluation signals

- Compound identification accuracy on test set is substantially higher than random baseline (> 1 / num_compounds), confirming the model learned meaningful representations.
- Ranking metrics (MRR, NDCG, or ranking precision) show that true compounds are ranked in the top-k positions for a large fraction of test spectra.
- Performance report documents both bi-encoder and cross-encoder contributions, confirming that weighted loss successfully balanced both branches.
- Error analysis: false negatives and false positives are attributed to spectral ambiguity or compound similarity, not model failure.
- Test set performance is consistent with or slightly lower than validation performance, indicating no sign of overfitting or data leakage.

## Limitations

- FlavorFormer was developed for 1H NMR spectra of flavor mixtures; ranking performance may not generalize to other spectral modalities (e.g., 13C NMR, GCMS) or non-flavor compounds without retraining.
- Ranking metrics depend on the quality of ground-truth compound labels in the test set; mislabeled or ambiguous labels will artificially degrade reported metrics.
- The weighted loss function requires tuning of encoder weight coefficients; reported metrics are sensitive to the balance between bi-encoder and cross-encoder contributions.
- Performance on highly similar compounds or overlapping spectral signatures is limited by the spectral resolution and preprocessing pipeline; no ranking metric can overcome fundamental spectral ambiguity.

## Evidence

- [other] 6. Validate on held-out test set, compute compound identification accuracy and ranking metrics, and save trained model checkpoint and performance report.: "Validate on held-out test set, compute compound identification accuracy and ranking metrics, and save trained model checkpoint and performance report"
- [readme] leverages a combination of a bi-encoder and cross-encoder, a fusion pooling strategy, and a weighted loss function to identify compounds correctly: "leverages a combination of a bi-encoder and cross-encoder, a fusion pooling strategy, and a weighted loss function to identify compounds correctly"
- [readme] FlavorFormer enables the accurate and rapid identification of compounds in flavor mixtures, establishing it as a powerful tool for NMR-based mixture studies.: "FlavorFormer enables the accurate and rapid identification of compounds in flavor mixtures, establishing it as a powerful tool for NMR-based mixture studies"
- [other] Combine bi-encoder and cross-encoder logits using the weighted loss function (balancing both encoder contributions) and train end-to-end with backpropagation.: "Combine bi-encoder and cross-encoder logits using the weighted loss function (balancing both encoder contributions) and train end-to-end with backpropagation"
