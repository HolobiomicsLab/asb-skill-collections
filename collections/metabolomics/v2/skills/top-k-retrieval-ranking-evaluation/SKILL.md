---
name: top-k-retrieval-ranking-evaluation
description: Use when when you have deployed a trained embedding or similarity model on a test set of tandem mass spectra and need to measure its ability to rank correct library compounds near the top of retrieved candidates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - Anaconda
  - Git
  - MSBERT
  - PyTorch
  - ProcessMSP utility
  - MSBERTSimilarity
derived_from:
- doi: 10.1021/acs.analchem.4c02426
  title: MSBERT
evidence_spans:
- '[Anaconda](https://www.anaconda.com) for Python 3.12'
- Install [Git](https://git-scm.com/downloads)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_msbert_cq
    doi: 10.1021/acs.analchem.4c02426
    title: MSBERT
  dedup_kept_from: coll_msbert_cq
schema_version: 0.2.0
---

# top-k-retrieval-ranking-evaluation

## Summary

Evaluate the ranking performance of a mass spectra retrieval model by computing top-1, top-5, and top-10 library matching accuracy against ground-truth identifications. This skill measures whether the model's ranked candidate list includes the correct compound in the top k positions.

## When to use

When you have deployed a trained embedding or similarity model on a test set of tandem mass spectra and need to measure its ability to rank correct library compounds near the top of retrieved candidates. This is essential for validating library matching workflows where mass spectral data must be matched to known compound reference spectra.

## When NOT to use

- Input test set lacks ground-truth compound identifiers or reference library annotations.
- Model has not been trained or fine-tuned; only pre-computed embeddings are available without a trained similarity metric.
- Test spectra are from a different instrument type or ionization method than the model was trained on, without validation of domain transfer first.

## Inputs

- trained embedding model (e.g., MSBERT checkpoint)
- test dataset of tandem mass spectra with ground-truth compound identifiers
- reference library of mass spectra with known annotations
- embedding or similarity computation function

## Outputs

- top-1 accuracy (float in [0, 1])
- top-5 accuracy (float in [0, 1])
- top-10 accuracy (float in [0, 1])
- ranked candidate lists per query (optional)

## How to apply

Load the pre-trained model (in this case, MSBERT) and the test dataset (e.g., Orbitrap subset of GNPS). Generate embeddings for all test spectra and perform library matching by computing similarity scores between query spectra and a reference library. For each query spectrum, rank all library candidates by descending similarity score. For each query, check whether the ground-truth compound identifier appears in the top 1, top 5, and top 10 ranked positions. Compute accuracy as the fraction of queries for which the correct match was found within each k threshold. Report the three metrics as proportions (e.g., 0.7871 for top-1 means 78.71% of queries had correct match ranked first).

## Related tools

- **MSBERT** (Pre-trained transformer encoder model for embedding tandem mass spectra; loads state from .pkl checkpoint and generates query/reference embeddings for ranking.) — https://github.com/zhanghailiangcsu/MSBERT
- **PyTorch** (Framework for loading the model checkpoint, computing embeddings, and managing tensor operations during ranking.) — https://pytorch.org/
- **ProcessMSP utility** (Parses .msp files to extract demo spectra and SMILES strings from the test dataset.) — https://github.com/zhanghailiangcsu/MSBERT
- **MSBERTSimilarity** (Computes cosine similarity scores between embedded query and reference spectra to produce ranked candidate lists.) — https://github.com/zhanghailiangcsu/MSBERT

## Examples

```
from model.MSBERTModel import MSBERT
from model.utils import ModelEmbed, ProcessMSP, MSBERTSimilarity
import torch

model = MSBERT(100002, 512, 6, 16, 0, 100, 3)
model.load_state_dict(torch.load('model/MSBERT.pkl'))
demo_data, demo_smiles = ProcessMSP('example/demo.msp')
demo_arr = ModelEmbed(model, demo_data, 16)
cos = MSBERTSimilarity(demo_arr, demo_arr)
```

## Evaluation signals

- Top-1 accuracy falls in expected range (e.g., 0.7871 reported for MSBERT on Orbitrap); compare against baseline methods (e.g., Spec2Vec, cosine similarity on raw spectra) to confirm improvement.
- Top-5 and top-10 accuracies show monotonic increase (top-5 ≥ top-1, top-10 ≥ top-5), confirming correct ranking logic.
- Accuracy metrics are reproducible across multiple runs with the same model checkpoint, test set, and random seed.
- Ground-truth compound is present in the reference library for ≥95% of test queries; queries with missing references are excluded from evaluation.
- Ranked candidate lists are sorted by descending similarity score; manual spot-check confirms top-ranked candidates are chemically/spectrally similar to query.

## Limitations

- Accuracy depends critically on test set composition (e.g., Orbitrap instrument type, MS/MS collision energy) and may not transfer to other instrument types without retraining.
- Library matching accuracy is bounded by the size and diversity of the reference library; small or biased libraries will produce artificially high accuracies.
- Method assumes one-to-one mapping between test spectrum and ground-truth compound; may not handle isomers, adducts, or novel compounds outside the reference library.
- Top-k metrics do not reveal ranking quality beyond the cutoff (e.g., whether correct match is ranked 6th vs. 1000th when k=5); average rank and reciprocal rank metrics provide finer granularity.

## Evidence

- [readme] MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset.: "MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset."
- [other] Compute top-1, top-5, and top-10 matching accuracies by comparing predicted library identifications against ground truth labels.: "Compute top-1, top-5, and top-10 matching accuracies by comparing predicted library identifications against ground truth labels."
- [other] Run the model on the test spectra to generate embeddings and perform library matching.: "Run the model on the test spectra to generate embeddings and perform library matching."
- [readme] The results are significantly better than Spec2Vec and cosine similarity.: "The results are significantly better than Spec2Vec and cosine similarity."
- [other] Load the pre-trained MSBERT model and the GNPS-derived Orbitrap test dataset.: "Load the pre-trained MSBERT model and the GNPS-derived Orbitrap test dataset."
