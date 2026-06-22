---
name: masking-augmentation-for-contrastive-learning
description: Use when when training a transformer encoder on tandem mass spectra (MS/MS) and you need to generate positive sample pairs for contrastive learning without access to labeled chemical or spectral analogues.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Python
  - Anaconda
  - Git
  - PyTorch
  - MSBERT
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

# masking-augmentation-for-contrastive-learning

## Summary

Apply stochastic masking to tandem mass spectra to create augmented positive sample pairs for contrastive learning in a transformer encoder. This technique leverages the randomness of masking to construct diverse positive examples that improve the learning signal when paired with a contrastive loss.

## When to use

When training a transformer encoder on tandem mass spectra (MS/MS) and you need to generate positive sample pairs for contrastive learning without access to labeled chemical or spectral analogues. Use this skill when your goal is to embed mass spectra into a chemically rational space and you have a large unlabeled MS/MS corpus (e.g., GNPS dataset) where self-supervised augmentation is more practical than manual pairing.

## When NOT to use

- Input spectra are already strongly labeled with known chemical analogues or curated positive pairs; in such cases, use supervised contrastive learning or label-based hard mining instead.
- Spectrum dimension is very low (< 50 features) or extremely sparse; masking may remove critical structural information and degrade learning.
- Goal is only to compute library matching similarity without improving embeddings; a pre-trained model and direct cosine similarity may suffice.

## Inputs

- Tandem mass spectra (MS/MS) in MSP or tabular format (m/z–intensity pairs or spectral feature vectors)
- Transformer encoder backbone (PyTorch module)
- Training dataset (GNPS or similar large unlabeled MS/MS corpus)
- Contrastive loss function (e.g., NT-Xent, triplet loss)

## Outputs

- Paired augmented spectra (original and masked representations)
- Paired embedding vectors (output from transformer encoder for each augmentation)
- Contrastive loss scalar per batch
- Trained transformer encoder weights

## How to apply

Implement a random masking module that applies stochastic element-wise masking to input tandem mass spectra feature vectors (e.g., m/z–intensity pairs or tokenized spectral representations). For each training batch, generate two augmented views of each spectrum: one with the original features and one with randomly masked features. Pass both views through the same transformer encoder backbone to produce paired embeddings. Compute the contrastive loss (e.g., NT-Xent loss) between these paired embeddings; the randomness of masking ensures sufficient diversity between the two augmented views while preserving the core chemical structure of the spectrum. Validate tensor shape transformations through the forward pass to ensure the encoder and masking module correctly wire into the contrastive loss computation. Hyperparameters include the masking probability (fraction of features masked per augmentation) and contrastive temperature; tune these empirically to balance positive-pair coherence with negative-pair separation.

## Related tools

- **PyTorch** (Deep learning framework for implementing transformer encoder, masking module, and contrastive loss computation) — https://pytorch.org/
- **MSBERT** (Reference implementation of mask learning and contrastive learning for MS/MS embedding; provides transformer backbone, masking strategy, and training pipeline) — https://github.com/zhanghailiangcsu/MSBERT
- **matchms** (Post-training integration framework for computing MSBERT-based similarity scores in spectral matching workflows) — https://github.com/zhanghailiangcsu/MSBERT/tree/main/matchms_workflow

## Examples

```
from model.MSBERTModel import MSBERT
from model.utils import ProcessMSP, ModelEmbed
model = MSBERT(100002, 512, 6, 16, 0, 100, 3)
demo_data, demo_smiles = ProcessMSP('example/demo.msp')
demo_arr = ModelEmbed(model, demo_data, 16)
```

## Evaluation signals

- Verify tensor shape consistency: original and masked spectra embeddings should have identical batch and embedding dimensions (e.g., [batch_size, embedding_dim]); mismatch indicates wiring error.
- Contrastive loss should decrease monotonically over training epochs; sustained increases suggest masking probability or temperature misalignment.
- Downstream library matching performance (top-1, top-5, top-10 accuracy on a held-out test set, e.g., Orbitrap dataset) should exceed baseline methods (Spec2Vec, cosine similarity); MSBERT achieved 0.7871, 0.8950, 0.9080 respectively, demonstrating learned embedding quality.
- Embedding rationality validation: dimensionality-reduced embeddings (PCA/t-SNE) should cluster spectra of structurally similar compounds; calculate structural similarity (e.g., Tanimoto on molecular fingerprints) and verify high correlation with embedding distance.
- Reproducibility check: retrain on identical random seed and dataset split; loss curves and final test metrics should be deterministic.

## Limitations

- Masking hyperparameter (masking fraction, masking strategy) must be tuned empirically; universal defaults do not exist across different MS/MS instrument types (Orbitrap, Q-TOF, etc.) or ionization modes.
- The method assumes spectra can be meaningfully tokenized or featurized as dense vectors; very sparse or noisy spectra may lose discriminative power under masking.
- Training requires a large, clean unlabeled MS/MS corpus (GNPS dataset used in the reference study); small or highly imbalanced instrument-specific datasets may produce poor embeddings.
- Computational cost scales with batch size and embedding dimension; no specific guidance provided on memory/speed tradeoffs for real-time inference or large-scale library matching.
- No changelog or versioning documentation available, making reproducibility and incremental improvement tracking difficult.

## Evidence

- [readme] MSBERT used the transformer encoder as the backbone and take advantage of the randomness of the mask to construct positive samples for contrastive learning.: "MSBERT used the transformer encoder as the backbone and take advantage of the randomness of the mask to construct positive samples for contrastive learning."
- [other] Implement the random masking mechanism that applies stochastic masking to tandem mass spectra features to create augmented positive pairs for contrastive learning.: "Implement the random masking mechanism that applies stochastic masking to tandem mass spectra features to create augmented positive pairs for contrastive learning."
- [other] Verify the encoder and masking module are correctly wired to the contrastive loss computation by validating tensor shape transformations through the forward pass.: "Verify the encoder and masking module are correctly wired to the contrastive loss computation by validating tensor shape transformations through the forward pass."
- [readme] MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset. The results are significantly better than Spec2Vec and cosine similarity.: "MSBERT had a stronger ability in library matching, with top 1, top5, and top 10 were 0.7871, 0.8950, and 0.9080 on Orbitrap test dataset. The results are significantly better than Spec2Vec and cosine"
- [readme] The rationality of embedding was demonstrated by reducing the dimensionality of the embedding vectors, calculating structural similarity, and spectra clustering.: "The rationality of embedding was demonstrated by reducing the dimensionality of the embedding vectors, calculating structural similarity, and spectra clustering."
- [readme] MSBERT was trained and tested on GNPS dataset.: "MSBERT was trained and tested on GNPS dataset."
