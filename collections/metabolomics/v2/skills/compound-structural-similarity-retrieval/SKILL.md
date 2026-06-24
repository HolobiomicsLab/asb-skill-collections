---
name: compound-structural-similarity-retrieval
description: Use when you have a collection of preprocessed MS/MS spectra with structural
  annotations (InChIKey, SMILES, or InChI) and need to identify pairs of compounds
  that are structurally related above a specified similarity threshold.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3375
  tools:
  - matchms
  - MS2DeepScore
  - RDKit
  - Python
  - scikit-learn
  - Spec2Vec
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included
  cleaning compound names
- MS2DeepScore to predict structural similarity scores for spe
- we used the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral
  embeddings for all 3601 spectra in the test set
- we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute
  structural similarities
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

# compound-structural-similarity-retrieval

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Retrieve chemically related compound pairs from tandem mass spectral datasets by computing structural similarity scores using deep learning embeddings or classical spectral similarity measures, then filtering by precision–recall thresholds. This skill is applied after spectral preprocessing and is used to identify structurally related compounds (Tanimoto > threshold) at scale across thousands of spectra.

## When to use

You have a collection of preprocessed MS/MS spectra with structural annotations (InChIKey, SMILES, or InChI) and need to identify pairs of compounds that are structurally related above a specified similarity threshold. Use this skill when you want to evaluate whether a given similarity scoring method (e.g., MS2DeepScore, Spec2Vec, modified Cosine) effectively retrieves high-Tanimoto pairs, or when you need to rank and filter spectrum pairs by predicted structural similarity for downstream analysis such as spectral clustering or chemical space visualization.

## When NOT to use

- Spectra lack chemical structure annotations (InChIKey or SMILES); ground-truth structural similarity cannot be computed.
- Input spectra have not undergone preprocessing (peak filtering, intensity normalization, metadata cleaning); raw spectra will degrade embedding quality.
- You need to retrieve spectra by *spectral* similarity alone (not structural); use unmodified MS/MS cosine similarity or Spec2Vec without Tanimoto comparison.

## Inputs

- Preprocessed MS/MS spectra (matchms Spectrum objects or .mgf/.msp files)
- Pretrained deep learning model (MS2DeepScore .pt checkpoint) or reference library
- InChIKey structural annotations linked to each spectrum
- RDKit Daylight fingerprints (2048 bits) or precomputed Tanimoto ground truth

## Outputs

- Spectral embeddings (200-dimensional vectors per spectrum)
- Pairwise similarity scores (MS2DeepScore predictions or classical spectral similarity)
- Precision–recall curves for each similarity scoring method
- Ranked list of spectrum pairs sorted by predicted structural similarity
- Filtered set of high-confidence structurally related pairs (above threshold)

## How to apply

Load preprocessed spectra and compute 200-dimensional spectral embeddings using a pretrained deep learning model (MS2DeepScore base network) or classical similarity scores (Spec2Vec, modified Cosine). Generate all possible spectrum pairs and compute pairwise similarity scores (cosine distance between embeddings or spectral vector similarity). Retrieve ground-truth structural similarity labels (Tanimoto scores computed from RDKit Daylight fingerprints with 2048 bits) by matching InChIKey annotations. For each candidate similarity score method, vary a threshold from 0 to 1 and at each threshold compute precision (fraction of selected pairs with Tanimoto ≥ threshold) and recall (fraction of all high-Tanimoto pairs that were selected). Plot precision versus recall curves to compare methods and select the threshold that balances retrieval specificity and sensitivity for your downstream application.

## Related tools

- **MS2DeepScore** (Siamese neural network that predicts structural similarity (Tanimoto) scores directly from pairs of MS/MS spectra embeddings without computing fingerprints) — https://github.com/matchms/ms2deepscore
- **matchms** (Data structure and pipeline for spectrum preprocessing, metadata cleaning, and computation of spectral similarity scores) — https://github.com/matchms/matchms
- **RDKit** (Generates Daylight fingerprints (2048 bits) from molecular structures and computes Tanimoto ground-truth structural similarity scores)
- **Spec2Vec** (Unsupervised spectral similarity baseline method for comparison)
- **scikit-learn** (Dimensionality reduction (t-SNE) for visualization of spectral embeddings in chemical space)

## Examples

```
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore
from matchms.importing import load_from_mgf
import numpy as np

model = load_model("ms2deepscore_model.pt")
spectra = list(load_from_mgf("test_spectra.mgf"))
ms2ds = MS2DeepScore(model)
embeddings = ms2ds.get_embedding_array(spectra)
similarities = np.dot(embeddings, embeddings.T)  # cosine similarity matrix
threshold = 0.7
high_sim_pairs = np.argwhere(similarities >= threshold)
```

## Evaluation signals

- Precision–recall curve shows monotonic decrease in precision as recall increases, with MS2DeepScore achieving higher precision at all recall points compared to modified Cosine and Spec2Vec baselines.
- Computed Tanimoto scores for test pairs (3601 spectra, 6,485,401 unique pairs) show RMSE between 0.13 and 0.20 for predicted scores in the 0.1–0.9 range, consistent with reported model performance.
- Ground-truth Tanimoto labels derived from RDKit Daylight fingerprints match the distribution of InChIKey structural groups (500 unique InChIKeys in validation/test sets).
- At Tanimoto threshold ≥ 0.6, precision and recall values for MS2DeepScore are measurably higher than for classical similarity measures, confirming superior retrieval of structurally related compounds.
- Ranked list of pairs is sortable by similarity score without NaN or out-of-bounds values; embedding vectors have expected dimensionality (200-D) and numerical stability.

## Limitations

- Method requires a large training dataset (> 100,000 annotated spectra) to train a new model; transferability across ionization modes or compound classes not thoroughly benchmarked in original paper.
- Performance depends on quality of structural annotations (InChIKey); spectra with missing or incorrect chemical labels will have unreliable ground-truth Tanimoto scores.
- Computational cost scales quadratically with number of spectra when computing all pairwise similarities; filtering or approximate nearest-neighbor methods needed for very large libraries (> 1 million spectra).
- Model uncertainty estimates via Monte-Carlo Dropout are available but not always reliable at extreme similarity ranges (very low or very high Tanimoto); outlier filtering (IQR thresholds) may be necessary.
- Precision–recall curves are threshold-dependent and sensitive to class imbalance in the test set (e.g., if most pairs have low Tanimoto, recall will be artificially high).

## Evidence

- [other] MS2DeepScore demonstrates superior precision and recall across the full range of similarity thresholds compared to modified Cosine and Spec2Vec when identifying structurally related compounds (Tanimoto > 0.6) from the test set of 3601 spectra.: "MS2DeepScore demonstrates superior precision and recall across the full range of similarity thresholds compared to modified Cosine and Spec2Vec when identifying structurally related compounds"
- [other] Compute 200-dimensional spectral embeddings for all test spectra using the MS2DeepScore base network. Generate all possible spectrum pairs from the test set (6,485,401 unique pairs) and compute MS2DeepScore structural similarity predictions using cosine distance between embeddings.: "Compute 200-dimensional spectral embeddings for all test spectra using the MS2DeepScore base network. Generate all possible spectrum pairs from the test set (6,485,401 unique pairs) and compute"
- [other] Retrieve ground-truth Tanimoto scores (computed from RDKit Daylight fingerprints with 2048 bits) for each test pair using the 14-character InChIKey structural labels.: "Retrieve ground-truth Tanimoto scores (computed from RDKit Daylight fingerprints with 2048 bits) for each test pair using the 14-character InChIKey structural labels"
- [other] For each scoring method (MS2DeepScore, Spec2Vec, classical similarity), iterate threshold values from 0 to 1 and for each threshold measure precision (high Tanimoto pairs in selection / all selected pairs) and recall (high Tanimoto pairs in selection / all high Tanimoto pairs), where 'high Tanimoto' is defined as Tanimoto ≥ threshold.: "For each scoring method (MS2DeepScore, Spec2Vec, classical similarity), iterate threshold values from 0 to 1 and for each threshold measure precision (high Tanimoto pairs in selection / all selected"
- [methods] we use the MS2DeepScore base network (Fig. 1) to compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set. Using the t-SNE [28] implementation from scikit-learn [29] we: "we compute the 200-dimensional spectral embeddings for all 3601 spectra in the test set"
- [readme] This model can be downloaded from [from zenodo here](https://zenodo.org/records/17826815). Only the ms2deepscore_model.pt is needed. The model works for spectra in both positive and negative ionization modes and even predictions across ionization modes can be made by this model.: "This model can be downloaded from [from zenodo here](https://zenodo.org/records/17826815). Only the ms2deepscore_model.pt is needed."
- [readme] To compute the similarities between spectra of your choice you can run the code below. There is a small example dataset available in the folder "./tests/resources/pesticides_processed.mgf". Alternatively you can of course use your own spectra, most common formats are supported, e.g. msp, mzml, mgf, mzxml, json, usi.: "To compute the similarities between spectra of your choice you can run the code below. There is a small example dataset available in the folder "./tests/resources/pesticides_processed.mgf"."
