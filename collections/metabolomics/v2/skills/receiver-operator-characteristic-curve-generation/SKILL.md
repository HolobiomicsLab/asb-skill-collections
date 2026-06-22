---
name: receiver-operator-characteristic-curve-generation
description: Use when when you have computed similarity scores (cosine, modified cosine, Spec2Vec, or other metrics) between a set of query spectra and a reference library with known structural annotations (InChIKey), and you need to evaluate how well each scoring method distinguishes true structural matches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - matchms
  - gensim
  - Numba
  - Pandas
  - scipy
  - Spec2Vec
  - Word2Vec (gensim)
  - scikit-learn or scipy.metrics
derived_from:
- doi: 10.1371/journal.pcbi.1008724
  title: Spec2Vec
evidence_spans:
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms
- the implementations for the cosine score and the modified cosine score used can be found in the Python package matchms [31] (https://github.com/matchms/matchms)
- A Word2Vec [22] model is trained on all documents of a chosen dataset using gensim [37]
- making extensive use of Numpy [24] and Numba [25]
- by making extensive use of Numpy [24] and Numba [25], the library
- Spec2Vec was optimised by making extensive use of Numpy [24] and Numba [25], the library matching was implemented using Pandas [40]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: spec2vec_grounded
    doi: 10.1371/journal.pcbi.1008724
    title: Spec2Vec
  dedup_kept_from: spec2vec_grounded
schema_version: 0.2.0
---

# receiver-operator-characteristic-curve-generation

## Summary

Construct ROC curves by ranking query spectra against a reference library and classifying hits as true or false positives based on structural identity (InChIKey), then computing and plotting true-positive rate versus false-positive rate across similarity score thresholds. This enables quantitative comparison of spectral similarity methods' discriminative power.

## When to use

When you have computed similarity scores (cosine, modified cosine, Spec2Vec, or other metrics) between a set of query spectra and a reference library with known structural annotations (InChIKey), and you need to evaluate how well each scoring method distinguishes true structural matches from non-matches across a range of decision thresholds.

## When NOT to use

- Input library spectra lack validated structural annotations (InChIKey). ROC curves require ground truth labels; without them, TP/FP classification is impossible.
- Similarity scores are not yet computed or pre-filtered. ROC generation requires a complete score matrix; pre-selection steps (e.g., precursor m/z matching) must occur first.
- Your goal is ranking or visualizing spectra in a network without classifier evaluation. If you only need to group similar spectra or draw molecular networks, direct similarity thresholding is sufficient; ROC curves add unnecessary overhead.

## Inputs

- Query spectra (MS/MS data with precursor m/z, fragment peaks, and InChIKey annotation)
- Reference library spectra (MS/MS data with InChIKey annotation)
- Similarity score matrix (one row per query, one column per library spectrum; computed using cosine, modified cosine, Spec2Vec, or equivalent metric)

## Outputs

- Receiver-operator-characteristic curve (plot with FPR on x-axis, TPR on y-axis)
- Area-under-curve (AUC) scalar per method
- True-positive rate and false-positive rate values at each threshold
- Ranked hit list with TP/FP classifications for each query–library pair

## How to apply

For each similarity scoring method, rank query spectra by their computed similarity to each library spectrum. Classify each ranked hit as a true positive if the matched spectrum has an InChIKey within the first 14 characters (planar structure) that matches the query, or a false positive if the structure differs. Vary the classification threshold systematically across the observed similarity score range. At each threshold, calculate the true-positive rate (TP / (TP + FN)) and false-positive rate (FP / (FP + TN)). Plot FPR on the x-axis and TPR on the y-axis, then compute the area under the resulting curve (AUC) as a scalar summary metric. This allows direct comparison of method sensitivity and specificity trade-offs.

## Related tools

- **matchms** (Computes cosine and modified cosine similarity scores; filters and preprocesses spectra before scoring) — https://github.com/matchms/matchms
- **Spec2Vec** (Computes Word2Vec-based spectral similarity embeddings for ROC comparison against cosine methods) — https://github.com/iomega/spec2vec
- **Word2Vec (gensim)** (Underlying embedding model trained on spectrum fragmentation patterns; used by Spec2Vec to generate similarity scores)
- **scikit-learn or scipy.metrics** (Computes ROC curve, AUC, and related metrics from binary classification labels and scores)

## Examples

```
from sklearn.metrics import roc_curve, auc; fpr, tpr, thresholds = roc_curve(true_positive_labels, similarity_scores); roc_auc = auc(fpr, tpr); import matplotlib.pyplot as plt; plt.plot(fpr, tpr, label=f'ROC (AUC={roc_auc:.3f})'); plt.xlabel('False Positive Rate'); plt.ylabel('True Positive Rate'); plt.legend(); plt.show()
```

## Evaluation signals

- ROC curve is monotonically increasing (TPR ≥ previous TPR for each FPR increase), and AUC is between 0 and 1.
- The number of true positives + false positives + true negatives + false negatives equals the total number of query–library pairs evaluated.
- AUC values for Spec2Vec are higher (>0.80) than for cosine and modified cosine methods, consistent with the paper's finding of better true/false-positive ratio.
- The curve passes through (0, 0) at the highest threshold (no hits classified as positive) and (1, 1) at the lowest threshold (all hits classified as positive).
- InChIKey matching is consistent: the same query–library pair always receives the same TP/FP label across repeated curve construction runs.

## Limitations

- ROC curves require complete InChIKey annotations in both query and library spectra. Missing or incomplete annotations will bias TP/FP counts and lower apparent method performance.
- The choice of 'planar structure' (first 14 InChIKey characters) as ground truth is a proxy for structural similarity; some isomers may be incorrectly classified as non-matches if they differ only in stereochemistry.
- ROC construction assumes independence between query–library comparisons; in reality, spectra from the same compound will be more similar, violating this assumption and potentially inflating AUC.
- Spectral quality, pre-processing parameters (peak filtering, m/z tolerance, minimum matching peaks), and library composition directly affect ROC curves; comparisons across studies with different parameters may not be valid.

## Evidence

- [other] For each similarity method, rank query spectra against library and classify hits as true positives (matching InChIKey within first 14 characters / planar structure) or false positives (non-matching structure) to construct receiver-operator-characteristic curves.: "rank query spectra against library and classify hits as true positives (matching InChIKey within first 14 characters / planar structure) or false positives (non-matching structure) to construct"
- [other] Calculate and report true-positive rate, false-positive rate, and area-under-curve for each method and compare against reported paper results.: "Calculate and report true-positive rate, false-positive rate, and area-under-curve for each method and compare against reported paper results"
- [other] Spec2Vec resulted in a notably better true/false positive ratio at all thresholds compared to cosine and modified cosine scores during library matching, achieving up to 88% accuracy and higher retrieval rates.: "Spec2Vec resulted in a notably better true/false positive ratio at all thresholds compared to cosine and modified cosine scores"
- [results] high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores: "high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores"
- [results] The poorer correlation between cosine and modified cosine similarity and structural similarity can largely be explained by high false positive rates: "The poorer correlation between cosine and modified cosine similarity and structural similarity can largely be explained by high false positive rates"
