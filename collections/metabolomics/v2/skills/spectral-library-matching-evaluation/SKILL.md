---
name: spectral-library-matching-evaluation
description: Use when you have a trained spectral embedding model (e.g., MSBERT, Spec2Vec) and need to benchmark its library matching accuracy against reference spectra on a test dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - Anaconda
  - Git
  - MSBERT
  - Spec2Vec
  - PyTorch
  - Python (scipy.stats, numpy)
  - matchms
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

# spectral-library-matching-evaluation

## Summary

Quantifies the accuracy of tandem mass spectrum library matching by computing rank-based hit rates (top-1, top-5, top-10) and performing statistical significance testing to compare embedding-based methods (MSBERT, Spec2Vec) against baselines. This skill validates whether a trained spectral embedding model achieves reported library matching performance on a held-out test set.

## When to use

Apply this skill when you have a trained spectral embedding model (e.g., MSBERT, Spec2Vec) and need to benchmark its library matching accuracy against reference spectra on a test dataset. Use it specifically when: (1) you want to reproduce published accuracy claims, (2) you are comparing two or more matching strategies (embedding vs. cosine-similarity vs. baseline), or (3) you need to report rank-based metrics (top-k hit rates) that are standard in mass spectrometry library matching literature.

## When NOT to use

- The test dataset is not labeled with ground-truth library identifiers — ranking cannot be evaluated without known correct matches.
- You are evaluating a model on the same training or validation set it was trained on — use only held-out test data to avoid overfitting bias.
- The reference library and test spectra are from different mass spectrometry instruments or acquisition protocols with incomparable m/z or intensity distributions — embedding spaces may not transfer meaningfully.

## Inputs

- Pre-trained spectral embedding model (PyTorch checkpoint, e.g., MSBERT.pkl)
- Test spectrum dataset in .msp or compatible format with ground-truth library identifiers
- Reference library spectrum dataset (same format, e.g., GNPS MSMS spectra)
- Baseline embedding model(s) for comparison (e.g., Spec2Vec model checkpoint)

## Outputs

- Top-1, top-5, top-10 hit-rate accuracy scores (range [0, 1]) for each method
- p-values from statistical significance tests
- Summary table comparing accuracy metrics across MSBERT and baselines
- Ranked match lists (true library identifier rank per test spectrum)

## How to apply

Load the pre-trained embedding model (e.g., MSBERT) and the test spectrum dataset (e.g., GNPS Orbitrap subset). Generate embeddings for all test spectra and all reference library spectra using the model encoder. Compute cosine-similarity scores between each test spectrum and all library spectra, then rank matches and record the rank of the true library identifier. Calculate top-1, top-5, and top-10 hit rates as the fraction of test spectra whose true library match appears in the top-k ranked results. Repeat this computation for each baseline method (Spec2Vec, raw cosine-similarity without embedding). Perform paired statistical significance testing (e.g., paired t-test or chi-squared test) to confirm that MSBERT outperforms baselines. Report accuracy scores, p-values, and confidence intervals in a summary table.

## Related tools

- **MSBERT** (Pre-trained transformer-based spectral embedding model used to generate embeddings for test and library spectra; performs the core matching and ranking computation.) — https://github.com/zhanghailiangcsu/MSBERT
- **Spec2Vec** (Baseline spectral embedding method trained on the same GNPS dataset; used for comparative accuracy evaluation.) — https://github.com/zhanghailiangcsu/MSBERT/tree/main/Spec2VecModel
- **PyTorch** (Deep learning framework used to load model checkpoints and compute cosine-similarity scores between embeddings.) — https://pytorch.org/
- **Python (scipy.stats, numpy)** (Statistical libraries for paired t-tests, chi-squared tests, and ranking/sorting operations on match results.)
- **matchms** (Workflow framework for spectral data processing and similarity calculation; can integrate MSBERT similarity scoring.) — https://github.com/zhanghailiangcsu/MSBERT/tree/main/matchms_workflow

## Examples

```
import torch
from model.MSBERTModel import MSBERT
from model.utils import ModelEmbed, ProcessMSP, MSBERTSimilarity
import numpy as np

model = MSBERT(100002, 512, 6, 16, 0, 100, 3)
model.load_state_dict(torch.load('model/MSBERT.pkl'))
test_data, test_smiles = ProcessMSP('example/test.msp')
lib_data, lib_smiles = ProcessMSP('example/library.msp')
test_embed = ModelEmbed(model, test_data, 16)
lib_embed = ModelEmbed(model, lib_data, 16)
cos_scores = MSBERTSimilarity(test_embed, lib_embed)
top1_hits = np.sum(np.argmax(cos_scores, axis=1) == np.arange(len(test_data))) / len(test_data)
```

## Evaluation signals

- Top-1 accuracy should match or exceed the reported benchmark (≥0.7871 for MSBERT on Orbitrap test set); top-5 and top-10 should be monotonically increasing and ≥0.8950 and ≥0.9080 respectively.
- Statistical significance testing (p-value < 0.05) confirms MSBERT outperforms Spec2Vec and cosine-similarity baselines.
- All test spectra receive exactly one ground-truth rank per method; no missing or duplicate ranks.
- Hit rates for baseline methods (Spec2Vec, cosine-similarity) should be substantially lower than MSBERT, demonstrating clear performance differentiation.
- Accuracy metrics are consistent when evaluated on stratified subsets of the test set (e.g., by precursor m/z range or collision energy), indicating stable generalization.

## Limitations

- Accuracy metrics are dataset-specific: MSBERT performance (top-1=0.7871, top-5=0.8950, top-10=0.9080) was measured only on the Orbitrap test subset of GNPS; performance may differ on other instruments, collision energies, or spectral libraries.
- The evaluation requires clean, filtered spectra with ground-truth library identifiers; noisy or mislabeled spectra will degrade observed accuracy and may not reflect true model capability.
- Cosine-similarity baseline results depend critically on the embedding quality; raw cosine-similarity without any embedding (used as a control) will almost always underperform learned embeddings, limiting its diagnostic value.

## Evidence

- [intro] MSBERT achieved top-1, top-5, and top-10 library matching scores of 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset, outperforming Spec2Vec and cosine similarity baselines.: "MSBERT achieved top-1, top-5, and top-10 library matching scores of 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset"
- [intro] Calculate rank-based accuracy metrics (top-1, top-5, top-10 hit rates) for all three methods. Perform statistical significance testing (e.g., paired t-test or chi-squared) to confirm MSBERT outperforms both baselines.: "Calculate rank-based accuracy metrics (top-1, top-5, top-10 hit rates) for all three methods. Perform statistical significance testing (e.g., paired t-test or chi-squared) to confirm MSBERT"
- [intro] Generate embeddings for all test spectra and reference library spectra using the MSBERT encoder. Compute cosine-similarity matching scores between test and library embeddings, retrieving top-1, top-5, and top-10 ranked matches.: "Generate embeddings for all test spectra and reference library spectra using the MSBERT encoder. Compute cosine-similarity matching scores between test and library embeddings, retrieving top-1,"
- [intro] Load the pre-trained MSBERT model and the GNPS-derived Orbitrap test dataset. Run the model on the test spectra to generate embeddings and perform library matching.: "Load the pre-trained MSBERT model and the GNPS-derived Orbitrap test dataset. Run the model on the test spectra to generate embeddings and perform library matching."
- [readme] The results are significantly better than Spec2Vec and cosine similarity.: "The results are significantly better than Spec2Vec and cosine similarity."
- [readme] MSBERT was trained and tested on GNPS dataset.: "MSBERT was trained and tested on GNPS dataset."
