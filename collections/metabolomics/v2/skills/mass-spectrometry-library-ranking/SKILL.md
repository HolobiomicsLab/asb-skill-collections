---
name: mass-spectrometry-library-ranking
description: Use when you have a set of unidentified tandem mass spectra (queries) and need to identify them by matching against a curated reference library (e.g., GNPS Orbitrap dataset).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Anaconda
  - Git
  - MSBERT
  - PyTorch
  - matchms
  - Spec2Vec
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

# mass-spectrometry-library-ranking

## Summary

Rank tandem mass spectra (MS/MS) against a reference spectral library using learned embeddings to retrieve top-k spectral matches. This skill evaluates library matching accuracy by computing cosine-similarity scores between query and reference spectrum embeddings, returning ranked hit lists and top-k accuracy metrics.

## When to use

You have a set of unidentified tandem mass spectra (queries) and need to identify them by matching against a curated reference library (e.g., GNPS Orbitrap dataset). Use this skill when you want to move beyond raw cosine-similarity or Spec2Vec baselines and assess whether a learned embedding model (such as MSBERT) improves top-1, top-5, and top-10 hit rates on holdout test spectra.

## When NOT to use

- Reference library is unlabeled or does not contain ground-truth compound identities — rank metrics cannot be computed.
- Query spectra are from a different instrument type (e.g., Orbitrap-trained model applied to QTOF spectra without retraining) — embedding space may not generalize, degrading accuracy.
- You only need to retrieve spectral neighbors without ranking quality metrics — use raw cosine-similarity or embedding lookup instead.

## Inputs

- Test MS/MS spectra (MSP file format with m/z and intensity pairs)
- Reference spectral library (MSP file format)
- Pre-trained MSBERT model checkpoint (PyTorch .pkl file)
- Query-to-reference ground-truth labels (compound identifiers)

## Outputs

- Top-k ranked matches per query spectrum (list of reference spectrum IDs, scores)
- Top-1, top-5, top-10 hit-rate accuracy metrics (float, range [0, 1])
- P-values from statistical significance tests
- Summary comparison table (method × accuracy metric)

## How to apply

Load a pre-trained MSBERT encoder and generate fixed-size embeddings (e.g., 512 dimensions) for all test query spectra and reference library spectra from MSP or pickle format. Compute pairwise cosine-similarity scores between each query embedding and all reference embeddings. Rank reference spectra by descending similarity and extract top-k (k=1, 5, 10) matches for each query. Calculate hit-rate accuracy as the fraction of queries whose true label appears in the top-k ranked list. Report top-1, top-5, and top-10 accuracy scores alongside p-values from paired statistical tests (e.g., paired t-test or chi-squared) to confirm improvement over baseline methods (cosine-similarity on raw spectra or Spec2Vec embeddings).

## Related tools

- **MSBERT** (Pre-trained transformer encoder for generating chemically rational MS/MS embeddings) — https://github.com/zhanghailiangcsu/MSBERT
- **PyTorch** (Deep learning framework for loading and running the MSBERT encoder) — https://pytorch.org/
- **matchms** (Library for MS/MS spectrum processing, filtering, and similarity workflow integration) — https://github.com/zhanghailiangcsu/MSBERT/tree/main/matchms_workflow
- **Spec2Vec** (Baseline embedding method for comparative evaluation) — https://github.com/zhanghailiangcsu/MSBERT/tree/main/Spec2VecModel

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

- Top-1, top-5, top-10 accuracy scores fall within expected ranges (0.0–1.0) and improve monotonically (top-1 ≤ top-5 ≤ top-10).
- P-value from paired significance test is <0.05, confirming MSBERT outperforms cosine-similarity and Spec2Vec baselines.
- Embedding vectors have expected shape (query_count, 512) and are normalized or comparable via cosine metric.
- Ground-truth label appears in retrieved top-k list for ≥70% of test queries (baseline expectation for Orbitrap dataset).
- Ranking is reproducible: same query–reference pair yields identical cosine-similarity score and rank position across runs.

## Limitations

- Model performance is dataset- and instrument-specific; MSBERT trained on GNPS Orbitrap may not generalize to other MS/MS platforms or fragmentation conditions without retraining.
- Accuracy depends on reference library completeness and quality; missing or mislabeled reference spectra degrade ranking correctness.
- Computational cost scales with library size (O(n) embeddings, O(n²) pairwise similarities for n reference spectra); large libraries (>100k spectra) may require GPU acceleration.
- Ground-truth labels must be available to compute hit-rate metrics; method is unsuitable for fully unsupervised or open-search scenarios.

## Evidence

- [intro] MSBERT achieved top-1, top-5, and top-10 library matching scores of 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset: "MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset."
- [intro] Results are significantly better than Spec2Vec and cosine similarity: "The results are significantly better than Spec2Vec and cosine similarity."
- [other] Generate embeddings for all test spectra and reference library spectra using the MSBERT encoder, then compute cosine-similarity matching scores: "Generate embeddings for all test spectra and reference library spectra using the MSBERT encoder. Compute cosine-similarity matching scores between test and library embeddings, retrieving top-1,"
- [other] Calculate rank-based accuracy metrics (top-1, top-5, top-10 hit rates) and perform statistical significance testing: "Calculate rank-based accuracy metrics (top-1, top-5, top-10 hit rates) for all three methods. Perform statistical significance testing (e.g., paired t-test or chi-squared) to confirm MSBERT"
- [readme] Load demo file in MSP format and compute MSBERT embeddings and similarity within matchms workflow: "# Load demo file
demofile = 'matchms_workflow/demo_msms.msp'
spectra = list(load_from_msp(demofile))
# Calculate MSBERT similarity scores between all spectra in matchms workflow
MSBERT_Similarity ="
