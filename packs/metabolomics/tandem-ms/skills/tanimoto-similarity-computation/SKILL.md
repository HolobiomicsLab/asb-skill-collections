---
name: tanimoto-similarity-computation
description: Use when you have a trained MS2DeepScore neural network and a set of MS/MS spectra (52 binned peaks per spectrum after preprocessing) for which you need to compute pairwise structural similarity predictions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - MS2DeepScore
  - Python
  - RDKit
  - NumPy
  - matchms
  techniques:
  - tandem-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-021-00558-4
  all_source_dois:
  - 10.1186/s13321-021-00558-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tanimoto-similarity-computation

## Summary

Compute Tanimoto structural similarity scores between pairs of mass spectra by converting predicted cosine similarities of learned 200-dimensional spectral embeddings into Tanimoto scores, benchmarked against reference RDKit Daylight fingerprint (2048 bits) similarities. This skill quantifies how well predicted structural similarities match ground-truth fingerprint-based chemical similarity.

## When to use

You have a trained MS2DeepScore neural network and a set of MS/MS spectra (52 binned peaks per spectrum after preprocessing) for which you need to compute pairwise structural similarity predictions. Use this skill when you want to validate model predictions against a reference set of Tanimoto scores computed from RDKit Daylight fingerprints, or when you need to report prediction error (RMSE) on a held-out test set without applying uncertainty filtering.

## When NOT to use

- Input spectra are not binned in the training format (52 bins per spectrum with filtered unused bins) — preprocessing is required first
- You lack chemical structure annotations (InChI or SMILES) for ground-truth Tanimoto reference computation
- Your model was trained with uncertainty quantification (Monte-Carlo Dropout) and you need to apply uncertainty filtering (IQR-based thresholding) — use the uncertainty-restricted variant instead for RMSE ~0.10

## Inputs

- Trained MS2DeepScore Siamese neural network model (base network with 200-dimensional embedding layer)
- Test set of MS/MS spectra (binned format: 52 bins per spectrum, filtered unused bins from training)
- Chemical structure annotations (InChI, SMILES, or InChIKey) for test spectra

## Outputs

- Predicted Tanimoto scores for all test spectrum pairs (floating-point similarity values in [0, 1] range)
- Root mean squared error (RMSE) metric between predicted and reference Tanimoto scores
- Prediction uncertainty estimates (optional, via Monte-Carlo Dropout if model trained with dropout)

## How to apply

Load the pre-trained MS2DeepScore base network and generate 200-dimensional spectral embeddings for each spectrum in your test set using the trained network. For all possible spectrum pairs (n unique pairs for n spectra), compute cosine similarity between paired embeddings. Convert cosine similarities to predicted Tanimoto scores using the network's learned transformation (no uncertainty filtering applied). Retrieve reference Tanimoto scores for each test pair by computing RDKit Daylight fingerprints (2048 bits) from the spectra's chemical structures and calculating their Tanimoto coefficients. Compute root mean squared error (RMSE) between predicted and reference Tanimoto scores across all test pairs using MSE loss formulation. Document the RMSE metric (typically ~0.15 without uncertainty restrictions; ~0.10 with stricter interquartile range filtering) as the accuracy indicator for your predictions.

## Related tools

- **MS2DeepScore** (Pre-trained Siamese neural network that generates spectral embeddings and predicts Tanimoto scores from MS/MS spectrum pairs) — https://github.com/matchms/ms2deepscore
- **RDKit** (Computes reference Tanimoto scores from molecular structures using 2048-bit Daylight fingerprints for ground-truth validation)
- **NumPy** (Vectorized computation of cosine similarities between embeddings and RMSE calculation across all spectrum pairs)
- **matchms** (Handles spectrum metadata cleaning and provides data I/O for MS/MS spectral datasets) — https://github.com/matchms/matchms

## Examples

```
from ms2deepscore.models import load_model; from ms2deepscore import MS2DeepScore; model = load_model('ms2deepscore_model.pt'); ms2ds = MS2DeepScore(model); embeddings = ms2ds.get_embedding_array(test_spectra); from numpy import dot, linalg; similarities = dot(embeddings, embeddings.T) / (linalg.norm(embeddings, axis=1, keepdims=True) * linalg.norm(embeddings, axis=1, keepdims=True).T); rmse = ((predicted_tanimoto - reference_tanimoto) ** 2).mean() ** 0.5
```

## Evaluation signals

- RMSE between predicted and reference Tanimoto scores falls in expected range: ~0.15 without uncertainty filtering, ~0.10 with strict IQR-based filtering
- All predicted Tanimoto scores are bounded in [0, 1] range with no NaN or infinite values
- Prediction distribution across structural similarity bins (low, medium, high) shows no systematic bias toward any bin
- Cosine similarities before Tanimoto conversion are bounded in [-1, 1] range (or [0, 1] for normalized embeddings)
- Number of predicted scores equals the number of unique spectrum pairs: (n × (n − 1)) / 2 for n test spectra

## Limitations

- Spectrum metadata (parent mass, elemental formula) were not used during model training, so predictions reflect only MS/MS peak patterns and ignore precursor-level information
- RMSE of ~0.15 indicates substantial prediction error; structural matches requiring high confidence should apply uncertainty-based filtering (Monte-Carlo Dropout IQR thresholds) to improve accuracy to ~0.10, at the cost of discarding uncertain predictions
- Model trained on GNPS/public library spectra; prediction accuracy may degrade on spectra from novel ionization modes, instruments, or chemical space not represented in training data
- Reference Tanimoto scores depend on RDKit fingerprint quality and chemical structure annotation accuracy; errors or missing InChI/SMILES data propagate into ground-truth labels
- Computational cost scales as O(n²) for n spectra due to all-pairs embedding comparison; large test sets (>10,000 spectra) require memory-efficient batching

## Evidence

- [other] MS2DeepScore achieves a root mean squared error of approximately 0.15 for predicted Tanimoto scores on the test set without uncertainty restrictions.: "MS2DeepScore achieves a root mean squared error of approximately 0.15 for predicted Tanimoto scores on the test set without uncertainty restrictions."
- [other] Generate all possible spectrum pairs from the test set (n=6,485,401 unique pairs) and compute 200-dimensional spectral embeddings for each spectrum using the trained base network. Calculate cosine similarity between paired embeddings and convert to predicted Tanimoto scores (no uncertainty filtering applied).: "generate 200-dimensional spectral embeddings for each spectrum using the trained base network. Calculate cosine similarity between paired embeddings and convert to predicted Tanimoto scores"
- [other] Retrieve reference Tanimoto scores computed from RDKit Daylight fingerprints (2048 bits) for each test spectrum pair. Compute root mean squared error (RMSE) between predicted and reference Tanimoto scores across all test pairs using the MSE loss formulation.: "Retrieve reference Tanimoto scores computed from RDKit Daylight fingerprints (2048 bits) for each test spectrum pair. Compute root mean squared error (RMSE) between predicted and reference Tanimoto"
- [methods] Unless noted otherwise, we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities: "Unless noted otherwise, we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities"
- [intro] achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty: "achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty"
- [methods] Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z: "Spectrum peaks were binned in 10,000 equally-sized bins ranging from 10 to 1000 m/z"
- [results] the neural network was not trained on any spectrum metadata such as parent mass and elemental formula: "the neural network was not trained on any spectrum metadata such as parent mass and elemental formula"
- [methods] To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network: "To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network"
- [readme] To compute the similarities between spectra of your choice you can run the code below. There is a small example dataset available in the folder "./tests/resources/pesticides_processed.mgf". Alternatively you can of course use your own spectra, most common formats are supported, e.g. msp, mzml, mgf, mzxml, json, usi.: "To compute the similarities between spectra of your choice you can run the code below. There is a small example dataset available in the folder "./tests/resources/pesticides_processed.mgf"."
