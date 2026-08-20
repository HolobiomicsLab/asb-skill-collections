---
name: tanimoto-score-threshold-optimization
description: Use when when you have a set of MS/MS spectra with ground-truth structural
  similarity labels (Tanimoto scores computed from molecular fingerprints) and need
  to choose a decision threshold for classifying spectrum pairs as 'chemically related'
  or 'unrelated'.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - matchms
  - MS2DeepScore
  - RDKit
  - Python
  - scikit-learn
  - Spec2Vec
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# Tanimoto-Score Threshold Optimization

## Summary

A method to systematically evaluate and select optimal structural similarity thresholds (Tanimoto scores) for compound retrieval tasks by measuring precision and recall across a range of decision boundaries. This skill determines which threshold value best balances the trade-off between selectivity and sensitivity when retrieving chemically related compounds from mass spectral datasets.

## When to use

When you have a set of MS/MS spectra with ground-truth structural similarity labels (Tanimoto scores computed from molecular fingerprints) and need to choose a decision threshold for classifying spectrum pairs as 'chemically related' or 'unrelated'. Apply this skill when your goal is to optimize retrieval performance for a specific use case (e.g., matching unknowns to a spectral library) where the cost of false positives vs. false negatives differs.

## When NOT to use

- Input lacks ground-truth structural similarity labels (Tanimoto or Dice scores); threshold optimization requires labeled pairs.
- Spectrum pairs have not been preprocessed or filtered (e.g., peaks binned to 10,000 m/z bins, intensities square-root transformed); raw, unprocessed spectra will bias similarity predictions.
- Only a single scoring method is available; threshold optimization is most valuable when comparing multiple methods to select the best one.

## Inputs

- Test set of MS/MS spectra with structural annotations (InChIKey or SMILES)
- Precomputed structural similarity scores (Tanimoto scores from RDKit Daylight fingerprints, 2048 bits)
- Similarity predictions from the scoring method under evaluation (e.g., MS2DeepScore cosine distances, Spec2Vec scores, or classical similarity measures)
- Spectrum pair list or all-pairs similarity matrix

## Outputs

- Precision-recall curve (plot with precision on y-axis, recall on x-axis)
- Optimal threshold value for the use case
- Precision and recall values at each threshold
- Comparative analysis across multiple scoring methods

## How to apply

For each candidate threshold value from 0 to 1 (in suitable increments), count how many spectrum pairs with ground-truth Tanimoto scores at or above that threshold are correctly retrieved by your scoring method, and how many are incorrectly selected. Precision is calculated as (high Tanimoto pairs in selection) / (all selected pairs), and recall as (high Tanimoto pairs in selection) / (all high Tanimoto pairs in the full set). Plot precision versus recall for all scoring methods being compared to visualize the trade-off curve. Select the threshold that achieves the desired balance for your application: choose higher thresholds for high-precision retrieval (fewer false positives) or lower thresholds for high-recall retrieval (fewer false negatives). The definition of 'high Tanimoto' (e.g., ≥0.6 for structurally related compounds) should be set based on domain knowledge about what chemical similarity level is meaningful in your context.

## Related tools

- **RDKit** (Compute ground-truth Tanimoto scores from Daylight fingerprints (2048 bits) for structural similarity labels)
- **MS2DeepScore** (Generate structural similarity predictions (via 200-dimensional spectral embeddings and cosine distance) to evaluate against ground truth) — https://github.com/matchms/ms2deepscore
- **Spec2Vec** (Unsupervised baseline scoring method to compare precision-recall against supervised MS2DeepScore)
- **matchms** (Load, preprocess, and manage MS/MS spectrum metadata and peak data for threshold evaluation) — https://github.com/matchms/matchms
- **scikit-learn** (Optional: compute or visualize precision-recall metrics and handle threshold iteration)
- **Python** (Implementation language for threshold iteration loop, precision/recall calculation, and plotting)

## Examples

```
```python
from ms2deepscore.models import load_model
from ms2deepscore import MS2DeepScore
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

model = load_model('ms2deepscore_model.pt')
ms2ds = MS2DeepScore(model)

# Compute embeddings and similarities
embeddings = ms2ds.get_embedding_array(test_spectra)  # 3601 x 200
similarity_matrix = np.dot(embeddings, embeddings.T)  # cosine similarity

# Compute ground-truth Tanimoto from fingerprints
ground_truth = np.array([Chem.DataStructs.TanimotoSimilarity(fp[i], fp[j]) 
                         for i in range(len(fp)) for j in range(i+1, len(fp))])

# Sweep thresholds and compute precision-recall
thresholds = np.linspace(0, 1, 101)
precision, recall = [], []
for t in thresholds:
    selected = similarity_matrix >= t
    high_sim = ground_truth >= 0.6
    precision.append(np.sum(selected & high_sim) / np.sum(selected + 1e-8))
    recall.append(np.sum(selected & high_sim) / np.sum(high_sim + 1e-8))

# Plot precision-recall curve
import matplotlib.pyplot as plt
plt.plot(recall, precision)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.savefig('precision_recall_curve.png')
```
```

## Evaluation signals

- Precision-recall curve is monotonic or exhibits expected trade-off pattern (precision decreases as recall increases, or vice versa)
- At threshold T=0, recall equals 1.0 (all pairs are selected); at T=1, recall equals 0.0 (no pairs selected)
- For a fixed scoring method, precision and recall values are consistent across multiple runs on the same test set (reproducibility)
- The selected threshold produces precision and recall values in the ranges reported in comparable studies (e.g., MS2DeepScore achieves >0.7 precision and >0.7 recall at optimal thresholds for Tanimoto ≥0.6)
- Comparative curves rank methods correctly: the best-performing method (e.g., MS2DeepScore) occupies the upper-right region of the precision-recall space relative to baselines (modified Cosine, Spec2Vec)

## Limitations

- Threshold optimization is specific to the test set and ground-truth label distribution used; thresholds optimized on one library may not transfer to spectra from different sources or ionization modes.
- Precision and recall depend critically on the definition of 'high Tanimoto' (e.g., ≥0.6 vs. ≥0.5); changing the structural similarity threshold changes the optimal decision boundary for spectrum pair classification.
- The method assumes ground-truth Tanimoto scores are accurate and complete; missing or mislabeled InChIKeys and SMILES will distort the true precision-recall relationship.
- Threshold optimization assumes the cost of false positives equals the cost of false negatives; if your application requires different costs (e.g., clinical diagnostics requiring high specificity), the optimal threshold may differ from the point of maximum harmonic mean (F1 score).

## Evidence

- [other] For each scoring method (MS2DeepScore, Spec2Vec, classical similarity), iterate threshold values from 0 to 1 and for each threshold measure precision (high Tanimoto pairs in selection / all selected pairs) and recall (high Tanimoto pairs in selection / all high Tanimoto pairs), where 'high Tanimoto' is defined as Tanimoto ≥ threshold.: "For each scoring method (MS2DeepScore, Spec2Vec, classical similarity), iterate threshold values from 0 to 1 and for each threshold measure precision (high Tanimoto pairs in selection / all selected"
- [other] MS2DeepScore demonstrates superior precision and recall across the full range of similarity thresholds compared to modified Cosine and Spec2Vec when identifying structurally related compounds (Tanimoto > 0.6) from the test set of 3601 spectra.: "MS2DeepScore demonstrates superior precision and recall across the full range of similarity thresholds compared to modified Cosine and Spec2Vec when identifying structurally related compounds"
- [methods] we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities: "we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities"
- [methods] The precision/recall plot in Fig. 4 was created by measuring how many pairs with Tanimoto scores above a set threshold ('high structural similarity pair') were among a subset of all pairs: "The precision/recall plot in Fig. 4 was created by measuring how many pairs with Tanimoto scores above a set threshold"
- [other] Plot precision versus recall for all three methods on a single figure and save as precision_recall_curve.png.: "Plot precision versus recall for all three methods on a single figure"
