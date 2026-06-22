---
name: structural-similarity-ground-truth-validation
description: Use when you have a spectral library with structural ground truth (InChIKey or SMILES annotations for ≥50% of spectra) and want to benchmark whether a new or existing spectral similarity scorer ranks structurally related compounds higher than unrelated ones.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0593
  tools:
  - matchms
  - gensim
  - Numba
  - Pandas
  - scipy
  - Spec2Vec
  - Word2Vec (gensim)
  - scikit-learn
  - Pandas / NumPy
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1008724
  all_source_dois:
  - 10.1371/journal.pcbi.1008724
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# structural-similarity-ground-truth-validation

## Summary

Validate spectral similarity scoring methods by comparing their rankings against ground-truth structural annotations (InChIKeys) and computing receiver-operator-characteristic curves to measure true-positive and false-positive rates. This skill establishes whether a similarity metric (cosine, modified cosine, Spec2Vec, etc.) correlates with actual chemical structure similarity.

## When to use

You have a spectral library with structural ground truth (InChIKey or SMILES annotations for ≥50% of spectra) and want to benchmark whether a new or existing spectral similarity scorer ranks structurally related compounds higher than unrelated ones. Apply this skill to measure if high spectral similarity actually predicts structural similarity and to quantify false-positive contamination in library matching.

## When NOT to use

- Library lacks structural ground truth (InChIKey/SMILES) or has <30% annotation coverage; ROC curves will be unreliable.
- Spectra are already deduplicated to one per unique InChIKey; you cannot compute rank-based metrics without structural diversity.
- Your goal is to optimize peak filtering parameters or instrument settings, not to validate a similarity scorer; use orthogonal quality metrics (mass accuracy, resolution) instead.

## Inputs

- MS/MS spectral library (mzML, mzXML, msp, MGF, or JSON format)
- Precursor mass annotations (required for pre-filtering)
- Structural annotations: InChIKey, SMILES, or other canonical form (required for ≥50% of spectra)
- Pairwise or all-vs-all similarity score matrix (computed separately using cosine, Spec2Vec, etc.)

## Outputs

- Receiver-operator-characteristic curve (TPR vs. FPR at multiple thresholds)
- Area-under-curve (AUC) score
- Precision–recall curve
- True-positive rate, false-positive rate, and accuracy at optimal or user-specified thresholds
- Confusion matrix or classification report per scorer

## How to apply

First, filter the spectral library to remove spectra lacking InChIKey annotation and those with <10 fragment peaks. Canonicalize structural ground truth using the first 14 characters of InChIKey (planar structure). Compute pairwise similarity scores between all spectra (or a representative subset via leave-one-out cross-validation) using your scorer of choice. For each query spectrum, rank the library by descending similarity score and classify each match as a true positive (matching InChIKey planar structure) or false positive (non-matching structure). Construct a receiver-operator-characteristic curve by varying the similarity threshold and recording the true-positive rate (TP / [TP + FN]) and false-positive rate (FP / [FP + TN]) at each threshold. Report area-under-curve, precision–recall curves, and the achieved accuracy or F1 score. Rationale: InChIKey ground truth is objective and reproducible; ROC curves reveal both discriminative power and the trade-off between sensitivity and specificity across all decision thresholds.

## Related tools

- **matchms** (Import, filter, and clean MS/MS spectra; compute cosine and modified cosine similarity scores; interface with InChIKey and peak metadata) — https://github.com/matchms/matchms
- **Spec2Vec** (Compute spectral similarity scores based on learned fragment embeddings (Word2Vec) to compare against cosine-based baselines) — https://github.com/iomega/spec2vec
- **Word2Vec (gensim)** (Train embedding model on spectral peaks and neutral losses to power Spec2Vec similarity calculations)
- **scikit-learn** (Compute ROC curves, AUC scores, precision–recall curves, and confusion matrices)
- **Pandas / NumPy** (Manage spectral metadata tables, classify matches as TP/FP based on InChIKey comparison, aggregate metrics)

## Examples

```
from matchms import Spectrum; from matchms.similarity import CosineGreedy; import pandas as pd; query_results = []; for query in query_spectra: matches = [(lib_spec, CosineGreedy().pair(query, lib_spec)) for lib_spec in library_spectra]; matches.sort(key=lambda x: x[1], reverse=True); query_results.append({"query_inchikey": query.get("inchikey")[:14], "matches": [(m[0].get("inchikey")[:14], m[1]) for m in matches]}); tp = sum(1 for m in matches if m[0].get("inchikey")[:14] == query.get("inchikey")[:14]); fp = len(matches) - tp; print(f"TP: {tp}, FP: {fp}")
```

## Evaluation signals

- ROC curve is strictly above the diagonal (AUC > 0.5), indicating discrimination better than random chance.
- True-positive rate at a specified similarity threshold matches or exceeds the reported literature baseline (e.g., Spec2Vec achieves 88% accuracy as stated in the source task).
- For each threshold, TP + FN = total positives (i.e., all same-structure spectra in library) and FP + TN = total negatives; matrix sums are consistent across thresholds.
- The method with higher AUC shows lower false-positive rate at matched true-positive rates, confirming improved selectivity.
- Accuracy plateau or cross-validation score is reproducible within ±2% when the analysis is re-run with the same random seed and hyperparameters.

## Limitations

- InChIKey annotation is incomplete in many public libraries (e.g., GNPS, MassBank); validation is biased toward annotated spectra and may not reflect performance on unknowns.
- Structural ground truth at the planar level (first 14 InChIKey characters) does not distinguish stereoisomers; two spectra of opposite enantiomers will be marked as true positives despite chemical difference.
- ROC curves assume a single similarity threshold tuning; in practice, different classes of molecules (e.g., peptides vs. small molecules) may require different optimal thresholds—report stratified metrics if possible.
- Spec2Vec and other learned-embedding methods require retraining on new experimental data (e.g., GC-MS or novel fragmentation modes) not well represented in the original training set; pre-trained models may show inflated AUC on in-domain data.
- Evaluation on leave-one-out or small cross-validation splits can inflate reported metrics due to overfitting; use a held-out test set for unbiased estimates.

## Evidence

- [methods] For each similarity method, rank query spectra against library and classify hits as true positives (matching InChIKey within first 14 characters / planar structure) or false positives (non-matching structure) to construct receiver-operator-characteristic curves.: "For each similarity method, rank query spectra against library and classify hits as true positives (matching InChIKey within first 14 characters / planar structure) or false positives (non-matching"
- [other] Spec2Vec resulted in a notably better true/false positive ratio at all thresholds compared to cosine and modified cosine scores during library matching, achieving up to 88% accuracy and higher retrieval rates.: "Spec2Vec resulted in a notably better true/false positive ratio at all thresholds compared to cosine and modified cosine scores during library matching, achieving up to 88% accuracy and higher"
- [results] high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores: "high Spec2Vec spectrum similarity score correlates stronger with structural similarity than the cosine or modified cosine scores"
- [results] The poorer correlation between cosine and modified cosine similarity and structural similarity can largely be explained by high false positive rates: "The poorer correlation between cosine and modified cosine similarity and structural similarity can largely be explained by high false positive rates"
- [results] removing all spectra with fewer than 10 fragment peaks: "removing all spectra with fewer than 10 fragment peaks"
- [results] we also removed all spectra without InChIKey annotation: "we also removed all spectra without InChIKey annotation"
