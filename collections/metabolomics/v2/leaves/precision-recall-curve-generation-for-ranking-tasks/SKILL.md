---
name: precision-recall-curve-generation-for-ranking-tasks
description: Use when when you have computed similarity scores (e.g., MS2DeepScore,
  Spec2Vec, modified Cosine) between pairs of spectra or compounds and want to compare
  their ability to retrieve chemically related pairs. Apply this skill if you have
  ground-truth structural similarity labels (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
  tools:
  - matchms
  - MS2DeepScore
  - RDKit
  - Python
  - scikit-learn
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

# precision-recall-curve-generation-for-ranking-tasks

## Summary

Generate precision-recall curves to evaluate and visually compare the ranking performance of multiple similarity scoring methods across a range of decision thresholds. This skill is essential for assessing retrieval quality when the goal is to identify high-confidence pairs (e.g., structurally similar compounds) from scored candidate sets.

## When to use

When you have computed similarity scores (e.g., MS2DeepScore, Spec2Vec, modified Cosine) between pairs of spectra or compounds and want to compare their ability to retrieve chemically related pairs. Apply this skill if you have ground-truth structural similarity labels (e.g., Tanimoto scores ≥ a threshold) and need to evaluate how many true positives each method captures versus false positives across varying decision thresholds.

## When NOT to use

- Input data lacks ground-truth labels or structural similarity annotations needed to define 'high similarity' pairs.
- The task is single-threshold classification (e.g., pass/fail at a fixed cutoff); use a confusion matrix or ROC curve instead.
- Similarity scores are already pre-filtered or thresholded; precision-recall assumes access to the full, unfiltered score distribution.

## Inputs

- Computed similarity scores for all spectrum pairs (numerical matrix or list)
- Ground-truth structural similarity labels (e.g., Tanimoto scores from RDKit Daylight fingerprints)
- Definition of 'high structural similarity' (e.g., Tanimoto ≥ threshold value)
- Multiple scoring method outputs to compare (e.g., MS2DeepScore, Spec2Vec, modified Cosine)

## Outputs

- Precision-recall curve plot (PNG or equivalent image format)
- Precision and recall values at each threshold for each method
- Visual comparison of method performance across the full range of thresholds

## How to apply

For each scoring method, iterate over a range of similarity thresholds (typically 0 to 1). At each threshold, partition all spectrum pairs into two groups: selected (score ≥ threshold) and unselected. For the selected group, compute precision as (count of high Tanimoto pairs in selection) / (total pairs selected) and recall as (count of high Tanimoto pairs in selection) / (total high Tanimoto pairs in the full dataset). Plot precision on the y-axis versus recall on the x-axis for all methods on a single figure. The resulting curve shows the precision-recall trade-off: methods with curves closer to the upper-right corner dominate across thresholds. Compare curves visually and compute area-under-curve (AUC) metrics if quantitative ranking is required.

## Related tools

- **scikit-learn** (Compute precision, recall, and AUC metrics from predictions and ground-truth labels)
- **matchms** (Load, clean, and manage spectrum metadata and InChIKey labels used to retrieve ground-truth structural similarity) — https://github.com/matchms/matchms
- **RDKit** (Generate molecular fingerprints and compute Tanimoto scores as ground-truth structural similarity labels)
- **MS2DeepScore** (Produce spectral embedding-based similarity scores to be evaluated on the precision-recall curve) — https://github.com/matchms/ms2deepscore

## Examples

```
from sklearn.metrics import precision_recall_curve; precision, recall, thresholds = precision_recall_curve(y_true=(tanimoto_scores >= 0.6), probas_pred=ms2deepscore_scores); plt.plot(recall, precision); plt.xlabel('Recall'); plt.ylabel('Precision'); plt.savefig('precision_recall_curve.png')
```

## Evaluation signals

- Precision-recall curve is monotonically decreasing or non-increasing as recall increases (precision should not unexpectedly rise at higher recall thresholds).
- Area under the precision-recall curve is between 0 and 1, and higher AUC indicates better method performance.
- All three methods (or more) appear as distinct curves on the same plot; visual separation confirms differences in ranking quality.
- At low thresholds (high recall), all methods show reduced precision; at high thresholds (low recall), precision approaches 1 for good methods.
- Ground-truth Tanimoto scores are correctly retrieved for all test pairs using InChIKey labels and fingerprint computation is consistent across pairs.

## Limitations

- Precision-recall curves are sensitive to the definition of 'high structural similarity' threshold; results may differ substantially if the Tanimoto cutoff is changed.
- The curve assumes a fixed dataset size; results are not generalizable if test set composition or size varies significantly.
- Class imbalance (i.e., if most pairs have low Tanimoto) can make recall difficult to interpret; precision may remain high even at low absolute true-positive counts.
- The method requires complete ground-truth labels for all pairs; missing or noisy Tanimoto annotations will distort the curve.
- Computational cost scales quadratically with the number of spectra; comparing 3,601 spectra generates 6,485,401 unique pairs and may be memory-intensive.

## Evidence

- [other] For each scoring method (MS2DeepScore, Spec2Vec, classical similarity), iterate threshold values from 0 to 1 and for each threshold measure precision (high Tanimoto pairs in selection / all selected pairs) and recall (high Tanimoto pairs in selection / all high Tanimoto pairs), where 'high Tanimoto' is defined as Tanimoto ≥ threshold.: "For each scoring method (MS2DeepScore, Spec2Vec, classical similarity), iterate threshold values from 0 to 1 and for each threshold measure precision (high Tanimoto pairs in selection / all selected"
- [other] Plot precision versus recall for all three methods on a single figure and save as precision_recall_curve.png.: "Plot precision versus recall for all three methods on a single figure and save as precision_recall_curve.png."
- [methods] The precision/recall plot in Fig. 4 was created by measuring how many pairs with Tanimoto scores above a set threshold ("high structural similarity pair") were among a subset of all pairs for which: "The precision/recall plot in Fig. 4 was created by measuring how many pairs with Tanimoto scores above a set threshold ("high structural similarity pair") were among a subset of all pairs"
- [other] MS2DeepScore demonstrates superior precision and recall across the full range of similarity thresholds compared to modified Cosine and Spec2Vec when identifying structurally related compounds (Tanimoto > 0.6) from the test set of 3601 spectra.: "MS2DeepScore demonstrates superior precision and recall across the full range of similarity thresholds compared to modified Cosine and Spec2Vec when identifying structurally related compounds"
- [methods] we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities: "we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities"
