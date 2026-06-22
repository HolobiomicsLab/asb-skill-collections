---
name: baseline-comparative-analysis
description: Use when your research proposes a new spectral embedding, matching algorithm, or retrieval method and you need to quantify its improvement over known baselines. Specifically, when you have a test dataset (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - Anaconda
  - Git
  - PyTorch
  - MSBERT
  - Spec2Vec
  - scipy.stats
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

# baseline-comparative-analysis

## Summary

Systematically compare a novel embedding or matching method against established baselines (e.g., Spec2Vec, cosine similarity) using rank-based accuracy metrics (top-1, top-5, top-10 hit rates) and statistical significance testing on a standardized test dataset. This skill validates whether the proposed method genuinely outperforms existing approaches rather than claiming superiority by anecdote.

## When to use

Your research proposes a new spectral embedding, matching algorithm, or retrieval method and you need to quantify its improvement over known baselines. Specifically, when you have a test dataset (e.g., Orbitrap MS/MS spectra), reference library spectra, and predictions or rankings from both your method and at least two baseline methods, and you want to compute rank-based hit rates and statistical p-values to support a claim of superior performance.

## When NOT to use

- Your dataset is too small (< 100 test samples) to reliably estimate hit rates and p-values; use cross-validation or bootstrap resampling instead.
- You have only one baseline or no baseline; comparative analysis requires at least two established methods to measure against.
- Your method is not yet deployable or trainable (e.g., still in design phase); implement and validate end-to-end on test data first.

## Inputs

- pre-trained neural embedding model (PyTorch state_dict or equivalent)
- test MS/MS spectra dataset (MSP format or array)
- reference library spectra (MSP format or array)
- baseline method implementations (Spec2Vec model, raw spectrum vectors)

## Outputs

- rank-based accuracy metrics table (top-1, top-5, top-10 hit rates for each method)
- statistical significance test results (p-values, t-statistics or chi-squared values)
- comparative performance summary (mean ± SD accuracy per method per cutoff)

## How to apply

Load the pre-trained model (e.g., MSBERT) and generate embeddings for all test spectra and reference library spectra using a consistent encoder (e.g., PyTorch transformer). Compute cosine-similarity matching scores between test and library embeddings, retrieving top-1, top-5, and top-10 ranked matches for your method. Repeat the same ranking procedure for at least two baseline methods (e.g., Spec2Vec embeddings and raw cosine similarity without embedding). Calculate rank-based accuracy metrics (hit rates) for all three methods at each cutoff (top-k). Perform paired statistical significance testing (e.g., paired t-test or chi-squared test) to confirm statistical significance of differences. Report accuracy scores, p-values, and effect sizes in a summary table; the rationale is that ranking accuracy at multiple cutoffs (top-1, top-5, top-10) better captures partial credit for near-misses than binary correctness, and significance testing guards against overfitting to a specific test fold.

## Related tools

- **PyTorch** (load pre-trained model and compute embeddings for test and reference spectra) — https://pytorch.org/
- **MSBERT** (pre-trained transformer encoder for MS/MS spectra; generates embeddings for matching) — https://github.com/zhanghailiangcsu/MSBERT
- **Spec2Vec** (baseline embedding method trained on filtered GNPS dataset for comparative ranking) — https://zenodo.org/records/13722644
- **Python** (scripting language for data loading, similarity computation, and statistical testing)
- **scipy.stats** (paired t-test and chi-squared significance testing)

## Examples

```
import torch
from model.MSBERTModel import MSBERT
from model.utils import ModelEmbed, MSBERTSimilarity

model = MSBERT(100002, 512, 6, 16, 0, 100, 3)
model.load_state_dict(torch.load('model/MSBERT.pkl'))
test_emb = ModelEmbed(model, test_spectra, 16)
lib_emb = ModelEmbed(model, library_spectra, 16)
sim_scores = MSBERTSimilarity(test_emb, lib_emb)
top_k_hits = {1: (sim_scores.argsort(axis=1)[:, :1] < true_idx).mean(),
              5: (sim_scores.argsort(axis=1)[:, :5] < true_idx).mean(),
              10: (sim_scores.argsort(axis=1)[:, :10] < true_idx).mean()}
```

## Evaluation signals

- Top-1, top-5, and top-10 hit rates are monotonically non-decreasing (top-10 ≥ top-5 ≥ top-1) for all methods.
- Significance test p-values are ≤ 0.05 or other pre-specified α-level, indicating the proposed method's improvement is not due to chance.
- Effect sizes (e.g., Cohen's d or Cramér's V) are reported alongside p-values and show practical magnitude of improvement (not just statistical significance).
- Baseline methods are applied identically to the same test and reference spectra, ruling out data leakage or train/test contamination.
- Hit-rate values lie in [0, 1] interval and are consistent with the sample size (e.g., top-1 accuracy on 1000 spectra should yield counts divisible by 1000 when multiplied by sample size).

## Limitations

- Comparison is restricted to the Orbitrap instrument subset of GNPS; generalization to other MS/MS instruments (Q-TOF, Quadrupole, etc.) is not validated by this analysis alone.
- Baseline methods (Spec2Vec, cosine similarity) may not represent the state-of-the-art; other deep learning or physics-informed baselines could shift conclusions.
- Statistical significance does not imply practical significance; small p-values with tiny effect sizes may not justify deployment overhead.
- Hit-rate metrics do not capture ranking confidence, tie-breaking behavior, or spectral quality heterogeneity; additional analyses (e.g., calibration curves, per-instrument or per-compound stratification) are recommended.

## Evidence

- [intro] MSBERT achieved top-1, top-5, and top-10 library matching scores of 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset: "MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset."
- [intro] Comparison includes Spec2Vec and cosine similarity baselines: "The results are significantly better than Spec2Vec and cosine similarity."
- [other] Workflow includes generating embeddings, computing similarity scores, retrieving top-k matches, and calculating rank-based accuracy metrics: "Generate embeddings for all test spectra and reference library spectra using the MSBERT encoder. 3. Compute cosine-similarity matching scores between test and library embeddings, retrieving top-1,"
- [other] Statistical significance testing validates improvement over baselines: "Perform statistical significance testing (e.g., paired t-test or chi-squared) to confirm MSBERT outperforms both baselines."
- [readme] Example code loading model and computing similarity on demo spectra: "# Load model
model_file = 'model/MSBERT.pkl'
model = MSBERT(100002, 512, 6, 16, 0,100,3)
model.load_state_dict(torch.load(model_file))"
