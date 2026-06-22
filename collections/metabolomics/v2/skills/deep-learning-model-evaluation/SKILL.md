---
name: deep-learning-model-evaluation
description: Use when after training a Siamese neural network on MS/MS spectrum pairs, use this skill to quantify prediction performance on a disjoint test set (e.g., 3600+ spectra from 500 unseen compounds).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3407
  tools:
  - MS2DeepScore
  - Python
  - RDKit
  - NumPy
  - matchms
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Our MS2DeepScore Python library offers two types of data generators
- To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles
- Our MS2DeepScore Python library offers two types of data generators, one which iterates over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over all spectra and was used for
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- mean squared error (MSE) loss
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore_cq
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore_cq
schema_version: 0.2.0
---

# deep-learning-model-evaluation

## Summary

Evaluate a trained deep learning model's prediction accuracy on a held-out test set of spectrum pairs by computing root mean squared error (RMSE) between predicted and reference structural similarity scores. This skill assesses whether the model generalizes well to unseen data without applying uncertainty filtering.

## When to use

After training a Siamese neural network on MS/MS spectrum pairs, use this skill to quantify prediction performance on a disjoint test set (e.g., 3600+ spectra from 500 unseen compounds). Trigger this when you need a single-number accuracy metric to compare model variants, report generalization performance, or decide whether uncertainty-based filtering is warranted.

## When NOT to use

- Input test set spectra have not undergone the same preprocessing (binning, peak filtering, intensity transformation) as the training set — preprocessing mismatch will invalidate RMSE interpretation.
- Test set is not truly independent from training data (data leakage) — RMSE will be artificially low and not reflect generalization.
- Reference Tanimoto scores are computed from a different molecular fingerprint method (e.g., Morgan fingerprints instead of RDKit Daylight) — the metric measures alignment to the wrong ground truth.

## Inputs

- Pre-trained MS2DeepScore Siamese neural network model (PyTorch state_dict)
- Test set of binned MS/MS spectra (52 m/z bins per spectrum, low-intensity peaks removed)
- Reference structural similarity labels (Tanimoto scores from RDKit Daylight fingerprints, 2048 bits)
- Spectrum metadata (InChIKey for matching reference annotations)

## Outputs

- Root mean squared error (RMSE) metric for predicted vs. reference Tanimoto scores
- Array of predicted Tanimoto scores for all test spectrum pairs
- Array of reference Tanimoto scores
- Performance summary file (RMSE value and dataset size)

## How to apply

Load the pre-trained model and test set of binned spectra (52 bins per spectrum after filtering unused bins). Generate all possible spectrum pairs from the test set and compute 200-dimensional spectral embeddings for each spectrum using the trained base network. Calculate cosine similarity between paired embeddings and convert to predicted Tanimoto scores without applying uncertainty filtering. Retrieve reference Tanimoto scores computed from RDKit Daylight fingerprints (2048 bits) for each pair. Compute root mean squared error (RMSE) using the MSE loss formulation between predicted and reference Tanimoto scores across all test pairs. RMSE of ~0.15 without filtering and ~0.10 with uncertainty restrictions indicates acceptable performance; document both filtered and unfiltered results for transparency.

## Related tools

- **MS2DeepScore** (Pre-trained Siamese network model for generating spectral embeddings and predicting Tanimoto scores) — https://github.com/matchms/ms2deepscore
- **RDKit** (Computes reference Tanimoto scores from Daylight fingerprints (2048 bits) for ground truth labels)
- **NumPy** (Computes cosine similarity between embeddings and RMSE loss metric)
- **matchms** (Spectrum data loading, metadata extraction, and preprocessing pipeline) — https://github.com/matchms/matchms
- **Python** (Scripting language for orchestrating data loading, model inference, and metric computation)

## Examples

```
from ms2deepscore.models import load_model; from ms2deepscore import MS2DeepScore; import numpy as np; model = load_model('ms2deepscore_model.pt'); embeddings = model.get_embedding_array(test_spectra); predicted_scores = np.dot(embeddings, embeddings.T); rmse = np.sqrt(np.mean((predicted_scores - reference_tanimoto_scores)**2)); print(f'RMSE: {rmse:.4f}')
```

## Evaluation signals

- RMSE falls within reported range (0.10–0.15) for benchmark datasets; values >0.20 suggest model failure or preprocessing mismatch.
- Test set size and composition match article specifications (3600+ spectra, 500 unique compounds, no data leakage).
- Predicted Tanimoto scores are bounded in [0, 1] and match reference scores' statistical distribution (mean, median, percentiles).
- RMSE without uncertainty filtering is consistently higher than RMSE with IQR thresholds applied, confirming that filtering reduces error.
- Reference Tanimoto scores are computed from the same RDKit Daylight fingerprint method (2048 bits) documented in methods; fingerprint count and bit depth are invariant across evaluation runs.

## Limitations

- RMSE does not capture performance at extremes (e.g., near-zero or near-unity similarities); distributions of errors across similarity bins should be examined separately.
- Model trained on 109,734 GNPS spectra; performance may degrade on spectra from different sources, ionization modes, or chemical families not well-represented in training data.
- Evaluation assumes test set spectra are of high quality with complete metadata (InChIKey, SMILES, or InChI); incomplete or misannotated spectra will corrupt reference labels and inflate RMSE.
- No comparison to alternative structural similarity measures (e.g., cosine similarity on fingerprints, classical spectral matching); RMSE alone does not establish superiority.
- Computational cost scales quadratically with test set size (~6.5M pairs for 3600 spectra); evaluation on very large test sets (>10,000 spectra) may be intractable without GPU acceleration.

## Evidence

- [full_text] MS2DeepScore achieves a root mean squared error of approximately 0.15 for predicted Tanimoto scores on the test set without uncertainty restrictions.: "MS2DeepScore achieves a root mean squared error of approximately 0.15 for predicted Tanimoto scores on the test set without uncertainty restrictions."
- [full_text] Generate all possible spectrum pairs from the test set (n=6,485,401 unique pairs) and compute 200-dimensional spectral embeddings for each spectrum using the trained base network. Calculate cosine similarity between paired embeddings and convert to predicted Tanimoto scores (no uncertainty filtering applied). Retrieve reference Tanimoto scores computed from RDKit Daylight fingerprints (2048 bits) for each test spectrum pair. Compute root mean squared error (RMSE) between predicted and reference Tanimoto scores across all test pairs using the MSE loss formulation.: "Generate all possible spectrum pairs from the test set (n=6,485,401 unique pairs) and compute 200-dimensional spectral embeddings for each spectrum using the trained base network. Calculate cosine"
- [intro] achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty: "achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty"
- [methods] We use annotated MS/MS spectra from GNPS, which underwent basic metadata cleaning. The dataset was retrieved from GNPS and contains a total of 210,407 MS/MS spectra.: "We use annotated MS/MS spectra from GNPS, which underwent basic metadata cleaning. The dataset was retrieved from GNPS and contains a total of 210,407 MS/MS"
- [methods] Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z: "Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z"
- [results] the neural network was not trained on any spectrum metadata such as parent mass and elemental formula: "the neural network was not trained on any spectrum metadata such as parent mass and elemental formula"
- [readme] To compute the similarities between spectra of your choice you can run the code below. There is a small example dataset available in the folder "./tests/resources/pesticides_processed.mgf".: "To compute the similarities between spectra of your choice you can run the code below. There is a small example dataset available"
