---
name: deep-learning-model-inference-on-test-sets
description: 'Use when you have a pretrained deep learning model, a reserved test set with ground-truth annotations, and need to evaluate prediction quality or generate embeddings for downstream analysis. Typical triggers: benchmarking a new model against classical baselines (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3703
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_3520
  tools:
  - matchms
  - MS2DeepScore
  - RDKit
  - Python
  - scikit-learn
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names
- MS2DeepScore to predict structural similarity scores for spe
- we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set
- we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- Our MS2DeepScore Python library offers two types of data generators
- Our MS2DeepScore Python library
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-021-00558-4
  all_source_dois:
  - 10.1186/s13321-021-00558-4
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# deep-learning-model-inference-on-test-sets

## Summary

Apply a pretrained deep learning model to generate predictions (embeddings, similarity scores, or structural labels) on a held-out test set, then compute performance metrics by comparing predictions against ground-truth labels. This skill is essential for validating model generalization and comparing against baseline methods on structurally independent data.

## When to use

You have a pretrained deep learning model, a reserved test set with ground-truth annotations, and need to evaluate prediction quality or generate embeddings for downstream analysis. Typical triggers: benchmarking a new model against classical baselines (e.g., modified Cosine, Spec2Vec), computing precision-recall curves across similarity thresholds, or assessing whether predictions correlate with structural similarity labels (Tanimoto scores from molecular fingerprints).

## When NOT to use

- Test set overlaps with training set or shares the same InChIKeys — this violates independence and inflates apparent performance.
- Ground-truth labels are missing or unreliable (e.g., InChIKeys not validated, RDKit fingerprints not computed consistently).
- Model was trained end-to-end on the same spectra or molecular structures in your test set — use a truly held-out validation set instead.

## Inputs

- Pretrained deep learning model weights (e.g., Siamese neural network checkpoint)
- Reserved test set: mass spectra with metadata (InChIKey, m/z, intensity peaks)
- Ground-truth structural similarity annotations (RDKit Tanimoto scores or equivalent)
- Spectrum file in standard format (mgf, msp, mzML, mzXML, json)

## Outputs

- Low-dimensional spectral embeddings for all test spectra (e.g., 200-dim vectors)
- Pairwise similarity scores for all spectrum pairs (e.g., cosine distances)
- Precision-recall curves (threshold vs. precision, threshold vs. recall)
- Performance comparison table (MS2DeepScore vs. Spec2Vec vs. modified Cosine)
- Precision-recall plot (PNG/PDF)

## How to apply

Load the pretrained model weights and the reserved test set (e.g., 3,601 spectra with InChIKey structural labels). Batch-process all test spectra through the model's base network to generate low-dimensional embeddings (e.g., 200-dimensional vectors). For each pair or specimen, compute predictions using the model's similarity function (e.g., cosine distance between embeddings). Retrieve ground-truth labels for each prediction (e.g., RDKit Tanimoto scores computed from Daylight fingerprints with 2048 bits) by matching InChIKeys. Iterate over a range of prediction thresholds (0–1) and for each threshold compute precision (fraction of high ground-truth pairs in predictions above threshold) and recall (fraction of all high ground-truth pairs retrieved). Compare your model's precision-recall curve against baseline methods on the same test set to quantify relative performance.

## Related tools

- **MS2DeepScore** (Pretrained Siamese neural network model that computes structural similarity predictions from pairs of MS/MS spectra embeddings) — https://github.com/matchms/ms2deepscore
- **matchms** (Loads, cleans, and filters mass spectra; provides data pipeline and spectrum pair generation) — https://github.com/matchms/matchms
- **RDKit** (Computes ground-truth Tanimoto structural similarity scores from molecular fingerprints (Daylight, 2048 bits) derived from InChI/SMILES)
- **scikit-learn** (Provides utilities for dimensionality reduction (t-SNE) and can compute performance metrics)
- **Python** (Language for implementing the inference pipeline, threshold iteration, and metric computation)

## Examples

```
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore
import matchms

model = load_model('ms2deepscore_model.pt')
ms2ds = MS2DeepScore(model)
spectra = matchms.importing.load_from_mgf('test_set.mgf')
embeddings = ms2ds.get_embedding_array(spectra)
similarities = ms2ds.pair_prediction(spectra, spectra)
```

## Evaluation signals

- Embeddings have correct shape (all test spectra mapped to same dimensionality, e.g., 200-dim) and no NaN or Inf values.
- Precision-recall curves are monotonic or semi-monotonic: precision should not increase with recall, and both should be in [0, 1].
- MS2DeepScore precision-recall dominates (lies above) both modified Cosine and Spec2Vec across most of the threshold range, confirming reported superiority.
- Prediction RMSE on Tanimoto scores falls within reported range (0.13–0.2 for Tanimoto in range 0.1–0.9) when computed against ground-truth labels.
- Test set statistics match reported dimensions: 3,601 spectra, 500 unique InChIKeys, no overlap with training set's 14,062 InChIKeys.

## Limitations

- Model performance degrades on spectra with very high or very low structural similarity (Tanimoto < 0.1 or > 0.9); RMSE predictions are unreliable outside the 0.1–0.9 range.
- Predictions are sensitive to spectrum metadata quality and peak filtering (e.g., peaks < 0.1% intensity must be removed, max 1,000 peaks); inconsistent preprocessing inflates prediction uncertainty.
- Monte-Carlo Dropout uncertainty estimates can filter out valid predictions if thresholds are too stringent (using interquartile range > set values); trade-off between confidence and coverage.
- Cross-ionization-mode predictions (positive vs. negative) may have degraded accuracy if the test set does not match the training ionization distribution.
- Computational cost scales quadratically with test set size (all pairwise comparisons: 6.5M pairs for 3,601 spectra); very large test sets require batching or approximation.

## Evidence

- [other] Load the reserved test set (3,601 spectra) and the pretrained MS2DeepScore base network from the Zenodo deposit. 2. Compute 200-dimensional spectral embeddings for all test spectra using the MS2DeepScore base network.: "Load the reserved test set (3,601 spectra) and the pretrained MS2DeepScore base network from the Zenodo deposit. 2. Compute 200-dimensional spectral embeddings for all test spectra using the"
- [other] Generate all possible spectrum pairs from the test set (6,485,401 unique pairs) and compute MS2DeepScore structural similarity predictions using cosine distance between embeddings.: "Generate all possible spectrum pairs from the test set (6,485,401 unique pairs) and compute MS2DeepScore structural similarity predictions using cosine distance between embeddings."
- [other] Retrieve ground-truth Tanimoto scores (computed from RDKit Daylight fingerprints with 2048 bits) for each test pair using the 14-character InChIKey structural labels.: "Retrieve ground-truth Tanimoto scores (computed from RDKit Daylight fingerprints with 2048 bits) for each test pair using the 14-character InChIKey structural labels."
- [other] For each scoring method (MS2DeepScore, Spec2Vec, classical similarity), iterate threshold values from 0 to 1 and for each threshold measure precision (high Tanimoto pairs in selection / all selected pairs) and recall (high Tanimoto pairs in selection / all high Tanimoto pairs): "For each scoring method (MS2DeepScore, Spec2Vec, classical similarity), iterate threshold values from 0 to 1 and for each threshold measure precision (high Tanimoto pairs in selection / all selected"
- [other] MS2DeepScore demonstrates superior precision and recall across the full range of similarity thresholds compared to modified Cosine and Spec2Vec when identifying structurally related compounds (Tanimoto > 0.6) from the test set of 3601 spectra.: "MS2DeepScore demonstrates superior precision and recall across the full range of similarity thresholds compared to modified Cosine and Spec2Vec when identifying structurally related compounds"
- [intro] we achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty: "we achieve a root mean squared error for predicted Tanimoto scores of about 0.15 when run without uncertainty restrictions, and down to 0.1 with stronger restrictions on model uncertainty"
- [methods] To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles [17]. At inference time, dropout was applied to all but the first layer of the base network. N = 10 embeddings were: "To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles. At inference time, dropout was applied to all but the first layer of the base network. N = 10 embeddings were"
- [results] validation set (3597 spectra of 500 unique InChIKeys)... test set (3601 spectra of 500 unique InChIKeys): "validation set (3597 spectra of 500 unique InChIKeys)... test set (3601 spectra of 500 unique InChIKeys)"
- [readme] To compute the similarities between spectra of your choice you can run the code below. There is a small example dataset available in the folder "./tests/resources/pesticides_processed.mgf".: "To compute the similarities between spectra of your choice you can run the code below. There is a small example dataset available in the folder "./tests/resources/pesticides_processed.mgf"."
- [readme] The resulting similarity matrix, is a numpy array containing all the MS2DeepScore predictions between all spectra.: "The resulting similarity matrix, is a numpy array containing all the MS2DeepScore predictions between all spectra."
