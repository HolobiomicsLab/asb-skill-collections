---
name: comparative-performance-evaluation-across-methods
description: 'Use when when you have developed a new spectral similarity scoring method
  and need to quantify its retrieval performance relative to established methods (e.g.,
  modified cosine, Spec2Vec). Use this skill if you have: (1) a test set of spectra
  with ground-truth structural similarity labels (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0154
  tools:
  - MS2DeepScore
  - Spec2Vec
  - RDKit
  - Python
  - scikit-learn
  - matchms
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Our MS2DeepScore Python library offers two types of data generators
- To estimate the uncertainty of a prediction we used Monte-Carlo Dropout ensembles
- recently introduced unsupervised Spec2V
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints
  (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints
  (2048 bits) to compute structural similarities
- Our MS2DeepScore Python library offers two types of data generators, one which iterates
  over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over
  all spectra and was used for
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# comparative-performance-evaluation-across-methods

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Systematically benchmark a novel spectral similarity method against established baselines by computing precision-recall curves across a shared test set and structural similarity ground truth. This skill establishes whether a new method achieves superior retrieval performance for compounds of high structural similarity (Tanimoto > 0.6).

## When to use

When you have developed a new spectral similarity scoring method and need to quantify its retrieval performance relative to established methods (e.g., modified cosine, Spec2Vec). Use this skill if you have: (1) a test set of spectra with ground-truth structural similarity labels (e.g., Tanimoto scores from RDKit fingerprints), (2) implementations of competing methods, and (3) a research question about precision-recall trade-offs or ranking performance on a specific structural similarity threshold (e.g., Tanimoto > 0.6).

## When NOT to use

- You lack ground-truth structural similarity annotations (e.g., RDKit Tanimoto scores) for your test spectra — this skill requires a reliable gold standard.
- Your test set is too small or lacks structural diversity (fewer than ~500 unique compounds) — precision-recall curves will be unreliable.
- You are comparing methods on different datasets or using different structural similarity definitions (e.g., one method labeled with Tanimoto, another with Dice) — results will not be commensurable.

## Inputs

- test set of MS/MS spectra (minimum ~3,600 spectra recommended)
- compound structure annotations (InChI, SMILES, or InChIKey for ground truth)
- implementations of novel and baseline spectral similarity methods

## Outputs

- precision-recall curves (one per method)
- structured performance metrics (precision, recall values at each threshold)
- comparison table of method performance at key thresholds (e.g., at high-precision regions)
- visual plots showing precision-recall trade-offs across methods

## How to apply

Load all test spectra and compute similarity scores using the novel method and baseline methods on the same set of unique spectrum pairs (e.g., all 6,485,401 pairs from 3,601 spectra). Generate structural similarity labels for all pairs by computing Tanimoto scores on RDKit Daylight fingerprints (2048 bits). For each spectral similarity measure, vary the threshold from 0 to 1.0, then at each threshold compute precision (high-similarity pairs retrieved / total pairs selected) and recall (high-similarity pairs retrieved / all true high-similarity pairs). Plot precision-recall curves for all methods and visually compare the trade-offs. Ground truth is typically defined as pairs exceeding a Tanimoto threshold (e.g., > 0.6). Use this approach to identify which method achieves better precision-recall combinations across the full range, especially in the high-precision region relevant to structural matching.

## Related tools

- **MS2DeepScore** (novel spectral similarity method to be evaluated) — https://github.com/matchms/ms2deepscore
- **Spec2Vec** (baseline unsupervised spectral similarity method for comparison)
- **RDKit** (compute Tanimoto structural similarity labels using Daylight fingerprints (2048 bits) as ground truth)
- **scikit-learn** (helper library for precision-recall computation and curve generation)
- **matchms** (spectrum data handling and preprocessing (metadata cleaning, spectral binning)) — https://github.com/matchms/matchms
- **Python** (implementation environment for orchestrating similarity computations and plotting)

## Examples

```
from ms2deepscore.models import load_model; from ms2deepscore import MS2DeepScore; from matchms.filtering.default_pipelines import DEFAULT_FILTERS; model = load_model('ms2deepscore_model.pt'); ms2ds = MS2DeepScore(model); scores_novel = ms2ds.pair_iterator(spectrum_pairs); scores_baseline = [modified_cosine(pair) for pair in spectrum_pairs]; tanimoto_labels = [compute_tanimoto(pair) for pair in spectrum_pairs]; precision, recall = precision_recall_curve(tanimoto_labels > 0.6, scores_novel); plt.plot(recall, precision, label='MS2DeepScore')
```

## Evaluation signals

- Precision-recall curves are monotonically decreasing or smooth (increasing recall should not cause precision to spike unpredictably).
- Ground-truth labels (Tanimoto scores) are computed consistently across all spectrum pairs using the same RDKit fingerprint settings (2048 bits, Daylight, no variation in InChIKey selection).
- The high-precision region (>0.7 precision) is well-populated with retrieved pairs; if sparse, the test set may be too small or the structural similarity threshold too stringent.
- All three methods are evaluated on identical spectrum pairs and identical ground-truth labels; no method should have more or fewer pairs scored.
- Reported metrics (precision, recall, area under curve) are reproducible when thresholds are re-applied to the same similarity scores.

## Limitations

- Performance depends critically on ground-truth quality: Tanimoto scores on RDKit Daylight fingerprints (2048 bits) may not perfectly reflect biological or chemical relevance of structural similarity; results are valid only for the selected structural similarity definition.
- The test set should contain spectra of sufficient structural diversity and annotation quality (InChIKey, InChI, SMILES); spectra with missing or incorrect annotations will skew ground truth and inflate error metrics.
- Precision-recall curves are most informative for imbalanced retrieval tasks; if structural similarity pairs comprise a very small fraction of the test set, recall will be low even for good methods.
- The choice of Tanimoto threshold (e.g., > 0.6 for 'high similarity') is arbitrary and may not align with practical chemical relevance; results should be reported across multiple thresholds or thresholds should be justified by domain knowledge.
- Monte-Carlo Dropout-based uncertainty estimates are available but not required for this skill; however, filtering out predictions with high uncertainty (high interquartile range) can improve accuracy at the cost of reducing coverage.

## Evidence

- [other] MS2DeepScore outperforms both modified Cosine and Spec2Vec across the full precision-recall range for identifying structurally related compounds, achieving notably better precision/recall combinations for retrieving high Tanimoto pairs (Tanimoto > 0.6).: "MS2DeepScore outperforms both modified Cosine and Spec2Vec across the full precision-recall range for identifying structurally related compounds"
- [other] For each spectral similarity measure, vary the similarity threshold from 0 to 1.0 and compute precision (high-similarity pairs retrieved / total pairs selected) and recall (high-similarity pairs retrieved / all high-similarity pairs) at each threshold.: "vary the similarity threshold from 0 to 1.0 and compute precision and recall at each threshold"
- [methods] Unless noted otherwise, we used Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities: "Tanimoto scores on RDKit Daylight fingerprints (2048 bits) to compute structural similarities"
- [other] Define high structural similarity pairs as those with Tanimoto > 0.6.: "Define high structural similarity pairs as those with Tanimoto > 0.6"
- [other] Generate precision-recall curves for all three methods and compare the trade-offs reported in Figure 4.: "Generate precision-recall curves for all three methods and compare the trade-offs"
- [methods] Spectrum data preparation: Metadata was cleaned and checked using matchms version 0.8.2: "Metadata was cleaned and checked using matchms [18] version 0.8.2"
- [readme] To compute the similarities between spectra of your choice you can run the code below. There is a small example dataset available in the folder "./tests/resources/pesticides_processed.mgf".: "compute the similarities between spectra of your choice; example dataset available in ./tests/resources/pesticides_processed.mgf"
