---
name: deep-learning-feature-extraction
description: Use when you have preprocessed and normalized LC-MS metabolomics data from multiple disease groups (e.g., healthy, disease-A, disease-B) and need to identify which m/z features or their patterns discriminate between phenotypes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3674
  tools:
  - DeepMSProfiler
  - TensorFlow
  - Keras
  - Python
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-024-51433-3
  title: DeepMSProfiler
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepmsprofiler_cq
    doi: 10.1038/s41467-024-51433-3
    title: DeepMSProfiler
  dedup_kept_from: coll_deepmsprofiler_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-51433-3
  all_source_dois:
  - 10.1038/s41467-024-51433-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# deep-learning-feature-extraction

## Summary

Apply deep learning models (e.g., DenseNet121) to extract disease-specific metabolic features from preprocessed LC-MS metabolomics data, producing interpretable heatmaps and feature importance maps that link individual m/z signals to disease phenotypes. This skill bridges raw spectra and actionable biomarker discovery.

## When to use

You have preprocessed and normalized LC-MS metabolomics data from multiple disease groups (e.g., healthy, disease-A, disease-B) and need to identify which m/z features or their patterns discriminate between phenotypes. Use this skill when classification accuracy alone is insufficient and you require interpretable per-metabolite or per-region contribution maps to guide downstream biomarker validation or mechanistic studies.

## When NOT to use

- Input data is already a feature table derived from domain expert knowledge or targeted metabolite panels; deep learning feature extraction is most valuable when raw LC-MS spectra or unsupervised feature lists are available.
- Sample size is very small (<20 samples per class) or severely imbalanced; deep ensemble models require sufficient labeled training data to avoid overfitting.
- Computational resources are extremely limited; DenseNet121 with CUDA and 10 ensemble runs typically requires GPU memory (≥5 GB) and hours of training time.

## Inputs

- Normalized LC-MS metabolomics feature matrix (samples × m/z features, typically .npy format or array-like)
- Sample-to-disease-label mapping (e.g., label.txt with disease-type assignments)
- Train/test split specification (e.g., datalist.txt with FilePath, Label, and Dataset columns)

## Outputs

- Trained deep learning model checkpoint (one per ensemble run)
- Per-sample disease-type classification predictions and confidence scores
- Saliency heatmaps (samples × m/z × m/z or samples × m/z, .npy format) showing feature attribution
- Ensemble consensus heatmap (aggregated across 10 runs)
- AUC curves and confusion matrix plots (optional, .svg format)

## How to apply

Train a deep learning classifier (DenseNet121 with Adam optimizer, learning rate 1e-4, batch size 8, typically 2–10 epochs per run over 10 ensemble runs) on the normalized LC-MS feature matrix using labeled disease-group assignments. After training, apply RISE (or equivalent gradient-based) saliency mapping to generate per-sample and per-class heatmaps showing which m/z signals most strongly influence predictions. Aggregate heatmaps across the ensemble to produce a consensus feature importance map. Validate by confirming that high-importance regions correspond to known disease biomarkers or biological hypotheses, and by checking that AUC and confusion matrix metrics meet domain expectations (typically >0.85 AUC for three-class disease classification in metabolomics).

## Related tools

- **DeepMSProfiler** (End-to-end LC-MS deep learning pipeline; orchestrates training, prediction, and feature extraction via mainRun.py; provides pre-trained models and RISE saliency visualization) — https://github.com/yjdeng9/DeepMSProfiler
- **TensorFlow** (Deep learning framework for building and training DenseNet121 classifier)
- **Keras** (High-level neural network API for model definition and training (integrated with TensorFlow 2.2.0))
- **Python** (Primary scripting language for data loading, preprocessing, and orchestration (PEP8 compliant))

## Examples

```
python mainRun.py -data ../example/data/ -label ../example/label.txt -out ../jobs -run_train -run_pred -run_feature -arch DenseNet121 -lr 1e-4 -batch 8 -epoch 2 -run 10
```

## Evaluation signals

- Classification metrics: AUC ≥ 0.85 on held-out test set for three-class disease discrimination (e.g., healthy vs. nodule vs. cancer)
- Confusion matrix shows low off-diagonal misclassification; disease-specific true positive rate >80%
- Saliency heatmaps reveal spatially coherent, biologically interpretable regions (not noise or artifact); high-importance m/z signals align with known disease metabolite signatures or HMDB/lipid database entries
- Ensemble consensus heatmaps are stable across 10 runs (low variance in feature importance rankings)
- Feature heatmap shapes and dimensions match input (samples × m/z × m/z for 2D saliency, or samples × m/z for 1D); .npy files save and load without corruption

## Limitations

- Requires GPU or CUDA environment (CUDA 10.1 tested; CPU-only training is possible but much slower) and substantial RAM for in-memory operations on high-resolution LC-MS matrices
- Deep learning models are sensitive to class imbalance and train/test split; stratified random splits and data balancing are not explicitly discussed but are assumed necessary
- RISE saliency maps highlight regions that influence predictions but do not establish causality; high-importance m/z features may be biomarkers or confounders; downstream validation (e.g., targeted MS/MS, pathway analysis, independent cohorts) is required
- Pre-trained model (859 serum samples: 210 healthy, 323 lung nodules, 326 lung cancer) is restricted to academic use and must be obtained from the authors; transfer learning and domain adaptation are not documented
- Input data format flexibility is limited; .npy or .mzML formats are supported; auto-conversion from .mzML may introduce preprocessing artifacts if not validated
- No explicit handling of batch effects, instrument drift, or systematic technical variation described in the README or article

## Evidence

- [readme] It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels. 2. Heatmaps depicting the correlation of different metabolite: "It takes raw metabolomics data from different disease groups as input and provides three main outputs: 1. Sample disease type labels. 2. Heatmaps depicting the correlation of different metabolite"
- [other] Apply a deep learning model to extract disease-specific features from the normalized data.: "Apply a deep learning model to extract disease-specific features from the normalized data."
- [readme] It harnesses the potential of deep learning to process complex data from different diseases and generate unique disease features.: "It harnesses the potential of deep learning to process complex data from different diseases and generate unique disease features."
- [readme] -arch: Specifies the model architecture, e.g., 'DenseNet121'. -pretrain: Specifies the path to the pre-trained model, default is None. -lr: Sets the learning rate, default is 1e-4. -opt: Specifies the optimizer, e.g., 'adam'. -batch: Sets the batch size, default is 8. -epoch: Sets the number of training epochs, default is 2. -run: Specifies the number of runs, default is 10.: "-arch: Specifies the model architecture, e.g., 'DenseNet121'. -pretrain: Specifies the path to the pre-trained model, default is None. -lr: Sets the learning rate, default is 1e-4. -opt: Specifies"
- [readme] After run_feature, the heatmaps were saved in ../jobs/jobs007/feature_results/ensemble_RISE.npy, so we can then show the feature heatmaps for different classes.: "After run_feature, the heatmaps were saved in ../jobs/jobs007/feature_results/ensemble_RISE.npy, so we can then show the feature heatmaps for different classes."
- [readme] Python Version: Python >= 3.6. TensorFlow Version: TensorFlow == 2.2.0. Keras Version: Keras == 2.3.1.: "Python Version: Python >= 3.6. TensorFlow Version: TensorFlow == 2.2.0. Keras Version: Keras == 2.3.1."
