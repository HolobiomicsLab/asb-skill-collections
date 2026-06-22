---
name: precision-recall-curve-generation-and-interpretation
description: Use when you have computed spectral similarity scores from multiple methods (e.g., MS2DeepScore, Spec2Vec, modified cosine) on the same set of spectrum pairs, have assigned ground-truth structural similarity labels (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - MS2DeepScore
  - Spec2Vec
  - RDKit
  - Python
  - scikit-learn
  - matchms
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Our MS2DeepScore Python library offers two types of data generators
- To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles
- recently introduced unsupervised Spec2V
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- Our MS2DeepScore Python library offers two types of data generators, one which iterates over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over all spectra and was used for
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

# precision-recall-curve-generation-and-interpretation

## Summary

Construct precision-recall curves by varying a similarity threshold across a full range (0 to 1.0) and computing precision (true positives / total predicted positives) and recall (true positives / all true positives) at each threshold, then compare curves to assess the trade-offs between different spectral similarity measures in retrieving structurally related compound pairs. This skill is essential for comparing multiple similarity algorithms' ability to retrieve high-similarity pairs (e.g., Tanimoto > 0.6) across the full decision boundary.

## When to use

You have computed spectral similarity scores from multiple methods (e.g., MS2DeepScore, Spec2Vec, modified cosine) on the same set of spectrum pairs, have assigned ground-truth structural similarity labels (e.g., Tanimoto fingerprint scores), and need to evaluate and visually compare which method best balances the precision-recall trade-off for retrieving structurally related compounds at a given similarity threshold.

## When NOT to use

- Ground-truth labels (structural similarity scores) are not available or are unreliable.
- You only have a single similarity method and no baseline for comparison; a precision-recall curve requires multiple methods to justify the comparison cost.
- Your use case requires a single optimality criterion (e.g., F1-score) rather than exploration of the full precision-recall frontier.

## Inputs

- All computed spectrum pairs (6,485,401 unique pairs in the MS2DeepScore study)
- Spectral similarity scores for each pair from method 1 (e.g., MS2DeepScore cosine similarities)
- Spectral similarity scores for each pair from method 2 (e.g., Spec2Vec scores)
- Spectral similarity scores for each pair from method 3 (e.g., modified cosine scores)
- Ground-truth structural similarity labels (Tanimoto fingerprint scores computed from RDKit Daylight fingerprints)
- High-similarity threshold (e.g., Tanimoto > 0.6)

## Outputs

- Precision-recall curve coordinates (threshold, precision, recall) for each method
- Comparative precision-recall plot with overlaid curves for all methods
- Quantitative comparison showing precision-recall trade-offs across methods
- Visual evidence of which method achieves superior precision/recall combinations

## How to apply

For each spectral similarity method and each threshold value from 0 to 1.0 in small increments: (1) select all spectrum pairs whose predicted similarity exceeds the threshold; (2) compute precision as the fraction of selected pairs with Tanimoto > 0.6 (the high-similarity label threshold); (3) compute recall as the fraction of all true high-similarity pairs (Tanimoto > 0.6) that were correctly selected; (4) plot threshold on the x-axis against precision on the y-axis, with recall indicated by marker position or color; (5) overlay precision-recall curves from all methods to visually inspect which methods achieve better precision at comparable recall levels (or vice versa). The rationale is that different applications may prioritize precision (few false positives) or recall (few false negatives), so the curve reveals the full landscape of trade-offs rather than a single point metric.

## Related tools

- **scikit-learn** (Used for precision-recall computation and visualization; provides utilities for threshold iteration and metric calculation)
- **RDKit** (Computes ground-truth Tanimoto structural similarity labels from Daylight fingerprints (2048 bits) for all spectrum pairs)
- **matchms** (Provides spectrum data structures and preprocessing utilities to organize spectrum pairs and metadata before similarity computation) — https://github.com/matchms/matchms
- **MS2DeepScore** (One of the spectral similarity methods whose precision-recall curve is computed and compared) — https://github.com/matchms/ms2deepscore
- **Spec2Vec** (One of the baseline spectral similarity methods whose precision-recall curve is computed and compared)
- **Python** (Programming environment for threshold iteration, precision/recall calculation, and curve plotting)

## Examples

```
from sklearn.metrics import precision_recall_curve; import numpy as np; thresholds = np.arange(0, 1.01, 0.01); for method, scores in {'MS2DeepScore': ms2_scores, 'Spec2Vec': spec2vec_scores}.items(): precision, recall, _ = precision_recall_curve(high_sim_labels, scores); plt.plot(recall, precision, label=method); plt.xlabel('Recall'); plt.ylabel('Precision'); plt.legend(); plt.show()
```

## Evaluation signals

- Precision-recall curves are monotonically decreasing in threshold space (higher threshold → fewer positives → lower recall), confirming correct threshold sweep logic.
- Recall reaches 1.0 at threshold = 0 (all pairs selected, so all true positives are found) and precision = 1.0 at high thresholds (only highest-confidence pairs selected).
- The area under each precision-recall curve (AUPRC) is computed and compared; a method with higher AUPRC is superior across the threshold range.
- Visual inspection confirms that curves do not cross erratically; smooth, monotonic descent indicates correct computation.
- At the chosen operating point (e.g., precision ≥ 0.9), recall values differ meaningfully across methods, confirming that the comparison surface distinctions in precision-recall trade-offs.

## Limitations

- The choice of high-similarity threshold (Tanimoto > 0.6) is dataset- and application-dependent; a different threshold may yield different curve rankings.
- Ground-truth structural similarity labels depend entirely on the choice of molecular fingerprint (RDKit Daylight fingerprints in this study); alternative fingerprints may produce different labels and curves.
- Precision-recall curves assume that the test set of spectrum pairs is representative of the deployment use case; distributional shift may alter real-world precision-recall.
- The granularity of threshold sweeps (e.g., 0.01 increments) affects computational cost and curve smoothness; very fine sweeps may be slow on large datasets (>6M pairs).
- Curves provide no information about computational cost, scalability, or inference time; a method with lower precision-recall may be preferred if it is orders of magnitude faster.

## Evidence

- [methods] For each spectral similarity measure, vary the similarity threshold from 0 to 1.0 and compute precision (high-similarity pairs retrieved / total pairs selected) and recall (high-similarity pairs retrieved / all high-similarity pairs) at each threshold.: "For each spectral similarity measure, vary the similarity threshold from 0 to 1.0 and compute precision (high-similarity pairs retrieved / total pairs selected) and recall (high-similarity pairs"
- [methods] Define high structural similarity pairs as those with Tanimoto > 0.6.: "Define high structural similarity pairs as those with Tanimoto > 0.6."
- [methods] MS2DeepScore outperforms both modified Cosine and Spec2Vec across the full precision-recall range for identifying structurally related compounds, achieving notably better precision/recall combinations for retrieving high Tanimoto pairs (Tanimoto > 0.6).: "MS2DeepScore outperforms both modified Cosine and Spec2Vec across the full precision-recall range for identifying structurally related compounds, achieving notably better precision/recall"
- [methods] Generate precision-recall curves for all three methods and compare the trade-offs reported in Figure 4.: "Generate precision-recall curves for all three methods and compare the trade-offs reported in Figure 4."
- [methods] Calculate Tanimoto structural similarity labels for all pairs using RDKit Daylight fingerprints (2048 bits).: "Calculate Tanimoto structural similarity labels for all pairs using RDKit Daylight fingerprints (2048 bits)."
