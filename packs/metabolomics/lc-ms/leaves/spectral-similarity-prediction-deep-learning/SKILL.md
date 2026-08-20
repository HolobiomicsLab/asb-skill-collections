---
name: spectral-similarity-prediction-deep-learning
description: Use when when you have paired MS/MS spectra (unknown and known metabolites) with annotated structural similarity labels, and you need to rank candidate structures for metabolite identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  tools:
  - DeepMASS
  - Keras
  - RDKit
  - IsoSpecPy
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.8b05405
  title: Deep MS/MS similarity
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deep_ms_ms_similarity_cq
    doi: 10.1021/acs.analchem.8b05405
    title: Deep MS/MS similarity
  dedup_kept_from: coll_deep_ms_ms_similarity_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.8b05405
  all_source_dois:
  - 10.1021/acs.analchem.8b05405
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-similarity-prediction-deep-learning

## Summary

Train and apply a deep-learning model to predict structural similarity scores between unknown and known metabolites using their MS/MS spectra. This skill extends metabolite identification beyond the limits of direct spectral database matching by learning transformational and structural relationships encoded in fragmentation patterns.

## When to use

When you have paired MS/MS spectra (unknown and known metabolites) with annotated structural similarity labels, and you need to rank candidate structures for metabolite identification. Specifically, apply this skill when the metabolite of interest is absent from your reference database but structurally related metabolites are present, and you want to predict which database entries are most likely to share the unknown's core structure.

## When NOT to use

- Input spectra are not MS/MS fragmentation data (e.g., intact mass or LC–MS chromatograms only).
- You have no annotated ground-truth structural similarity labels for training; the model requires supervised pairs.
- The unknown metabolite is already present in your reference database; direct spectral matching is more efficient.

## Inputs

- paired MS/MS spectra (unknown metabolite spectra, known reference spectra)
- metadata: m/z values, intensity values per spectrum
- structural similarity labels or ground-truth similarity scores for training pairs
- reference spectral database (for ranking candidates)

## Outputs

- trained deep neural network model (weights file)
- predicted structural similarity scores (0–1 or unbounded, per model design)
- ranked list of candidate structures for unknown metabolite (sorted by predicted similarity)
- inference function for scoring new spectrum pairs

## How to apply

Load paired MS/MS spectra datasets with metadata and structural similarity annotations. Preprocess spectra by normalizing intensity values and extracting m/z features. Design a deep neural network architecture (using Keras) that encodes spectral data into learned vector representations. Train the model on annotated spectrum pairs using supervised learning with a regression or ranking loss objective. Evaluate performance on a held-out test set using correlation-based metrics (e.g., Pearson correlation between predicted and reference similarity scores). Export the trained model weights and inference function to score candidate structures from your reference database against the unknown spectrum.

## Related tools

- **DeepMASS** (reference implementation of the deep-learning spectral similarity prediction workflow; includes pre-trained model weights and rank method for candidate structure selection) — https://github.com/hcji/DeepMASS
- **Keras** (deep neural network framework for designing and training the spectral encoding architecture)
- **RDKit** (cheminformatics library for structural similarity computation and chemical representation (used in DeepMASS dependency chain))
- **IsoSpecPy** (isotope pattern computation library used in preprocessing and feature extraction for spectral data)

## Evaluation signals

- Pearson correlation between predicted similarity scores and held-out test set reference similarities should be ≥ 0.7 (or project-specific threshold).
- Ranked candidate list should place true structural analogs in the top-k positions (e.g., top 10% of candidates).
- Model convergence: training loss decreases monotonically; validation loss plateaus without divergence.
- Inference latency per spectrum pair is <1 second (practical throughput for large candidate ranking).
- Spectral preprocessing is consistent: all m/z values normalized to [0, 1] or unit norm; no NaN or missing intensity values in model input.

## Limitations

- Model performance depends critically on quantity and quality of annotated training pairs; sparse or noisy similarity labels degrade predictions.
- Requires pre-trained model weights or sufficient in-house spectral database to train from scratch; public pre-trained weights may not transfer across ionization modes or instrument types.
- Metabolite identification is limited to candidates in the reference database; novel structural scaffolds not represented in training data will not be identified.
- Spectral preprocessing choices (normalization, m/z binning, intensity thresholding) significantly impact model robustness; hyperparameters must be tuned per dataset.
- Dataset availability: the original MetDNA experimental spectra used in DeepMASS publication were removed; users must provide their own annotated spectra or wait for public dataset inclusion (as of 2019/05/13 note in README).

## Evidence

- [readme] DeepMASS is a known-to-unknown metabolite identification workflow, which includes a deep-learning based model to predict structural similarity between the unknown metabolites and the known ones based on their MS/MS spectra: "DeepMASS is a known-to-unknown metabolite identification workflow, which includes a deep-learning based model to predict structural similarity between the unknown metabolites and the known ones based"
- [readme] Using the transformational relationship and structural similarity between metabolites is a promising strategy to extend the number of metabolites can be identified by the existing database.: "Using the transformational relationship and structural similarity between metabolites is a promising strategy to extend the number of metabolites can be identified"
- [other] Load paired MS/MS spectra datasets (unknown and known metabolite spectra) with metadata. Preprocess spectra by normalizing intensity values and extracting relevant m/z features. Design a deep learning architecture to encode spectral data into learned representations. Train the model on annotated spectrum pairs with structural similarity labels using supervised learning. Evaluate model performance on a held-out test set using similarity prediction metrics (e.g., Pearson correlation between predicted and reference similarities).: "Preprocess spectra by normalizing intensity values and extracting relevant m/z features. Design a deep learning architecture to encode spectral data into learned representations. Train the model on"
- [readme] If you want to train a model based on your in-house database, please put your spectra files into data/spectra directory and run test.py.: "If you want to train a model based on your in-house database, please put your spectra files into data/spectra directory and run test.py"
- [readme] the dataset has been removed. If you have already download the dataset, please keep it private, and the dataset can be only used to reproduce the results of DeepMASS paper.: "the dataset has been removed. If you have already download the dataset, please keep it private"
