---
name: molecular-fingerprint-prediction
description: Use when you have tandem MS/MS spectra paired with known molecular structures (for training) or unknown spectra requiring structure identification, and you want to predict dense molecular fingerprint vectors that encode structural similarity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0338
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0154
  tools:
  - PyTorch
  - MIST
  - MIST-CF
  - SIRIUS decomp
derived_from:
- doi: 10.1038/s42256-023-00708-3
  title: MIST (chemical formula transformer)
evidence_spans:
- github.com/samgoldman97/mist
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mist_chemical_formula_transformer_cq
    doi: 10.1038/s42256-023-00708-3
    title: MIST (chemical formula transformer)
  dedup_kept_from: coll_mist_chemical_formula_transformer_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s42256-023-00708-3
  all_source_dois:
  - 10.1038/s42256-023-00708-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-fingerprint-prediction

## Summary

Predict molecular structural fingerprints directly from tandem mass spectrometry (MS/MS) data by encoding collections of fragment-derived chemical formulae through a transformer neural network architecture. This enables structure annotation and similarity-based retrieval without requiring fragmentation tree construction or spectral database lookup.

## When to use

Apply this skill when you have tandem MS/MS spectra paired with known molecular structures (for training) or unknown spectra requiring structure identification, and you want to predict dense molecular fingerprint vectors that encode structural similarity. Use it when your primary goal is to annotate spectra by ranking candidate structures or embedding spectra into a continuous similarity space, rather than directly predicting a single best-match molecule.

## When NOT to use

- Input spectra lack subformula information and SIRIUS or equivalent decomposition tools are unavailable.
- Target is to predict a single molecular structure directly (e.g., SMILES string) rather than a fingerprint; use structure prediction or dereplication methods instead.
- Spectra are from positive-mode MS/MS only; MIST as described handles [M+H]+ adducts; extension to multiple adduct types (e.g., [M+Na]+) requires model retraining.

## Inputs

- Tandem mass spectrometry spectra (MGF file format)
- Fragment chemical formulae (extracted via SIRIUS decomp or internal subformula labeling)
- Reference molecular structures as SMILES strings (for training and retrieval)
- Target fingerprint vectors (e.g., ECFP, Morgan fingerprints) for ground truth

## Outputs

- Predicted molecular fingerprint vectors (fixed dimension, real-valued)
- Ranked candidate molecule list (when retrieval library is provided)
- Learned spectrum-to-fingerprint transformer model weights and architecture
- Spectrum embeddings in dense continuous space (when contrastive training applied)

## How to apply

Load tandem MS/MS spectra in MGF format. Extract subformulae (fragment chemical formulae) from each spectrum using internal chemical subformula assignment or SIRIUS fragmentation tree decomposition. Tokenize and embed each subformula using a learned chemical formula vocabulary with sinusoidal positional embeddings. Pass the embedded subformula sequences through a multi-head transformer encoder stack to capture inter-fragment relationships. Pool the encoder output (e.g., via mean pooling or CLS token) to obtain a fixed-dimensional representation. Project the pooled vector through a dense layer to produce a molecular fingerprint prediction with dimensions matching your target fingerprint space (e.g., 2048-bit ECFP). During training, minimize the distance between predicted fingerprints and ground-truth fingerprints; optionally train in a contrastive learning framework to enable subsequent retrieval-by-lookup against a reference SMILES library.

## Related tools

- **MIST** (Primary transformer architecture for encoding chemical formula sequences and predicting fingerprints from tandem MS; includes contrastive training framework for retrieval-by-database-lookup) — https://github.com/samgoldman97/mist
- **MIST-CF** (Extended architecture for chemical formula transformer with improved subformula assignment, multi-adduct support, and sinusoidal formula embeddings; provides advances to be backported into fingerprint prediction model) — https://github.com/samgoldman97/mist-cf
- **SIRIUS decomp** (Dynamic programming algorithm to enumerate potential chemical formulae for observed MS1 precursor masses; used to generate subformula candidates for transformer input)
- **PyTorch** (Deep learning framework for implementing transformer encoder, multi-head self-attention, and training loop with contrastive or supervised loss)

## Examples

```
. quickstart/00_download_models.sh && . quickstart/01_run_models.sh
```

## Evaluation signals

- Predicted fingerprint dimensions match target fingerprint space (e.g., 2048 bits for ECFP); confirm via tensor shape inspection.
- When evaluated against held-out test spectra, predicted fingerprints exhibit high Tanimoto similarity to ground-truth fingerprints (typical benchmark: >0.7 for known compounds).
- In retrieval mode, known true molecule ranks in top-k candidates when fingerprints are used to search a reference library; report rank-1 accuracy and mean reciprocal rank.
- Contrastive-trained embeddings cluster spectra from the same molecule and separate isomers in the embedding space; verify via t-SNE visualization or silhouette score on held-out data.
- Model loss converges during training (supervised fingerprint MSE or contrastive triplet loss); monitor validation loss to detect overfitting.

## Limitations

- Requires precomputed subformula assignments (SIRIUS or internal labeling); quality of subformula extraction directly impacts fingerprint prediction accuracy.
- Handles positive-mode [M+H]+ adducts and H+ spectra; extension to neutral loss fragments, multiple adduct types ([M+Na]+, etc.), and negative-mode requires model retraining and architectural updates.
- Performance degrades on spectra from high-resolution instruments (e.g., Orbitrap) not well represented in training data; models trained on public NPLIB1 dataset may underperform vs. those trained on commercial NIST20 (available on request).
- Fingerprint predictions are probabilistic embeddings; direct structure prediction requires post-hoc database lookup or a separate structure decoder module.
- Contrastive learning framework requires construction of isomer-aware retrieval HDF file (>5GB); this preprocessing step is not included in minimal quickstart and must be manually generated.

## Evidence

- [intro] MIST applies a transformer architecture to directly encode and learn to represent collections of chemical formula: "MIST applies a transformer architecture to directly encode and learn to represent collections of chemical formula"
- [other] Tokenize and embed chemical formulae using a learned vocabulary: "Tokenize and embed chemical formulae using a learned vocabulary. 3. Pass embedded formula sequences through a transformer encoder stack with multi-head self-attention."
- [other] Pool the transformer output (e.g., via mean pooling or CLS token) to obtain a fixed-dimensional representation: "Pool the transformer output (e.g., via mean pooling or CLS token) to obtain a fixed-dimensional representation. 5. Project the pooled representation through a dense layer to predict a molecular"
- [intro] when trained in a contrastive learning framework, MIST enables embedding and structure annotation by database lookup: "when trained in a contrastive learning framework, MIST enables embedding and structure annotation by database lookup"
- [readme] To list out all potential formulae for an observed MS1 mass, we utilize the dynamic programming algorithm implemented by SIRIUS, `SIRIUS decomp`: "To list out all potential formulae for an observed MS1 mass, we utilize the dynamic programming algorithm implemented by SIRIUS, `SIRIUS decomp`"
- [readme] Utilizing sinusoidal *formula* embeddings as developed in our previous work [SCARF]: "Utilizing sinusoidal *formula* embeddings as developed in our previous work [SCARF]"
- [readme] This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data).: "This model may be less performant than the model trained on the commercial NIST20 Library (particularly for Orbitrap or higher resolution data)."
