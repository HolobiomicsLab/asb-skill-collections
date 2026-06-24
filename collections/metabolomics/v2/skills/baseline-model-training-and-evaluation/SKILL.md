---
name: baseline-model-training-and-evaluation
description: 'Use when when you need to establish comparable performance baselines
  for a novel spectrum prediction model and require fair comparison across multiple
  baseline architectures. Trigger this skill when: (1) you have a new spectrum prediction
  approach (e.g., ICEBERG, SCARF) to benchmark;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - PyTorch
  - TensorFlow
  - PubChem
  - ms-pred
  - MAGMa
  techniques:
  - GC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s42256-024-00816-8
  title: ICEBERG
evidence_spans:
- _No usage/docs found._
- By inputting the chemical formula and your experimental spectrum, the WebUI will
  rank it against all candidates from PubChem.
- the WebUI will rank it against all candidates from PubChem
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_iceberg_cq
    doi: 10.1038/s42256-024-00816-8
    title: ICEBERG
  dedup_kept_from: coll_iceberg_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42256-024-00816-8
  all_source_dois:
  - 10.1038/s42256-024-00816-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# baseline-model-training-and-evaluation

## Summary

Train and evaluate baseline spectrum prediction models (NEIMS FFN/GNN, MassFormer, 3DMolMS, GrAFF-MS, CFM-ID) under equivalent hyperparameter and covariate settings to enable fair comparison with novel spectrum prediction approaches. This skill ensures reproducible, controlled benchmarking across multiple model architectures on mass spectrometry tasks.

## When to use

When you need to establish comparable performance baselines for a novel spectrum prediction model and require fair comparison across multiple baseline architectures. Trigger this skill when: (1) you have a new spectrum prediction approach (e.g., ICEBERG, SCARF) to benchmark; (2) you possess a labeled spectrum dataset with molecular structures (NIST'20, MassSpecGym) and collision energy annotations; (3) you aim to isolate the contribution of your model's architecture rather than differences in training data, preprocessing, or hyperparameter tuning.

## When NOT to use

- Dataset lacks collision energy annotations — baselines like NEIMS require collision-specific covariates and equivalence assumptions break down.
- You are comparing models across fundamentally different prediction tasks (e.g., electron ionization vs. electrospray ionization) — covariates and dataset splits must be task-specific, not forced into a single unified framework.
- Computational budget is extremely limited (< 24 GB GPU RAM) — ICEBERG and other multi-stage pipelines require substantial resources; CPU-only training will be prohibitively slow for fair hyperparameter sweeps.

## Inputs

- Labeled mass spectra dataset with collision energy annotations (NIST'20 .SDF format or equivalent HDF5 structure)
- Molecular structures as SMILES strings or chemical formulas
- Preprocessed subformula or fragment annotations (from SCARF or MAGMa pipeline)
- Train/validation/test splits (e.g., random or scaffold-based)

## Outputs

- Trained baseline model checkpoints (PyTorch .pt or equivalent)
- Spectrum predictions on test/benchmark compounds (m/z and intensity arrays)
- Evaluation metrics per baseline (cosine similarity, spectral match score, retrieval ranks)
- Comparison table or plot showing baseline vs. novel model performance
- Log files documenting hyperparameter sweeps and training curves

## How to apply

Implement multiple baseline models (NEIMS with FFN and GNN encoders, MassFormer, 3DMolMS, GrAFF-MS) using a unified framework (ms-pred) that enforces identical preprocessing pipelines, input covariates, and hyperparameter search spaces across all models. For each baseline: (1) preprocess molecular structures into fixed-length feature vectors or graph representations suitable for each encoder type; (2) train on the same labeled spectrum dataset using the same loss function (e.g., mean squared error) and optimizer (e.g., Adam) with matched batch sizes and learning rate schedules; (3) evaluate on a held-out test set using equivalent metrics (cosine similarity, spectral match score, top-1/top-10 retrieval accuracy); (4) save model checkpoints and generate predictions on benchmark compounds. The rationale is that controlling these confounding factors isolates architectural differences and prevents hyperparameter tuning bias from favoring any single baseline.

## Related tools

- **ms-pred** (Unified framework implementing NEIMS (FFN/GNN encoders), MassFormer, 3DMolMS, GrAFF-MS baselines with equivalent preprocessing, covariates, and hyperparameter sweeps for fair spectrum prediction model comparison) — https://github.com/coleygroup/ms-pred
- **PyTorch** (Deep learning backend for implementing FFN and GNN baseline encoders with standard loss functions and optimization algorithms)
- **TensorFlow** (Alternative deep learning backend for baseline model training and inference)
- **MAGMa** (Algorithm for annotating substructures and fragment breakage patterns required for ICEBERG training set construction during baseline experiments)

## Evaluation signals

- Baseline models converge during training (training loss decreases monotonically over epochs, no divergence or NaN values in loss logs).
- Test set evaluation metrics fall within expected ranges for each baseline relative to published results (e.g., NEIMS cosine similarity ~0.7–0.8 on comparable datasets).
- Hyperparameter sweep results are reproducible across runs with the same random seed (e.g., best learning rate and batch size identical across two training runs).
- All baselines use identical input features and preprocessing (verified by checksum or log inspection of covariate tensors before model input).
- Model checkpoint files are non-empty and contain trainable parameters (verified by loading and inspecting weight tensors in PyTorch/TensorFlow).

## Limitations

- NIST'20 is a commercial dataset requiring purchase; results are difficult to reproduce without access. MassSpecGym is publicly available but has undergone less manual curation and quality control than NIST, leading to different prediction accuracy expectations.
- Fair comparison assumes all baselines benefit equally from hyperparameter tuning; some architectures (e.g., GNNs vs. FFNs) may have inherent sensitivity to learning rate or batch size not captured by a uniform sweep.
- Training ICEBERG and other multi-stage baselines requires two GPUs with ≥24 GB RAM each; smaller GPU or CPU-only inference significantly extends training time and may compromise convergence.
- Baseline implementations may require dataset-specific preprocessing (e.g., SCARF requires subformula assignment via magma_subform_50 or no_subform variants); missing or inconsistent preprocessing breaks equivalence assumptions.
- CFM-ID is not retrained within the ms-pred framework (only inference instructions provided); its comparison results may not reflect identical training conditions as other baselines.

## Evidence

- [readme] In order to fairly compare various spectra models, we implement a number of baselines and alternative models using equivalent settings across models (i.e., same covariates, hyperparameter sweeps for each, etc.): "equivalent settings across models (i.e., same covariates, hyperparameter sweeps for each, etc.)"
- [other] Preprocess molecular structures into fixed-length feature vectors suitable for FFN input. 3. Construct a feedforward neural network encoder with standard hidden layers and ReLU activations. 4. Train the FFN encoder on the spectrum prediction task using mean squared error loss and an optimization algorithm (e.g. Adam).: "Preprocess molecular structures into fixed-length feature vectors suitable for FFN input... Construct a feedforward neural network encoder... Train the FFN encoder on the spectrum prediction task"
- [other] Evaluate the model on a held-out test set, computing prediction accuracy metrics (e.g. cosine similarity, spectral match score). 6. Save the trained model checkpoint and generate predictions on benchmark compounds for comparison with ms-pred results.: "Evaluate the model on a held-out test set, computing prediction accuracy metrics (e.g. cosine similarity, spectral match score). Save the trained model checkpoint and generate predictions on"
- [readme] You need two GPUs with at least 24GB RAM to train ICEBERG (we used NVIDIA A5000 for development). If you are trying to train the model on a smaller GPU, try cutting down the batch size and skipping the contrastive finetuning step.: "You need two GPUs with at least 24GB RAM to train ICEBERG... If you are trying to train the model on a smaller GPU, try cutting down the batch size"
- [readme] We are retiring the support of the NPLIB1 dataset... nist20 is a commercial dataset available for purchase... Given the scale of effort required to purchase samples, run experiments, and collect such a large amount of spectra, and that NIST'20 is the only database where all spectra have collision energy annotations, this dataset is a reasonable investment: "nist20 is a commercial dataset available for purchase... NIST'20 is the only database where all spectra have collision energy annotations"
- [readme] CFM-ID from [CFM-ID 4.0: More Accurate ESI-MS/MS Spectral Prediction and Compound Identification] (not retrained; instructions for running are provided): "CFM-ID 4.0... (not retrained; instructions for running are provided)"
- [readme] The archived version released with [Goldman et al. (2024)] is at the iceberg_analychem_2024 branch. The internal pipeline used to conduct experiments can be followed below: 1. Train dag model... 2. Sweep over the number of fragments to generate... 3. Use model 1 to predict model 2 training set: "The internal pipeline used to conduct experiments can be followed... Sweep over the number of fragments to generate"
