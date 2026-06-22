---
name: molecular-fingerprint-generation-and-encoding
description: Use when when you have paired tandem MS spectra and corresponding molecular structures (as SMILES strings or InChI keys) and need to train a model that jointly embeds spectra and structures for structure annotation by database lookup.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0310
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3407
  tools:
  - MIST
  - MIST-CF
derived_from:
- doi: 10.1038/s42256-023-00708-3
  title: MIST (chemical formula transformer)
evidence_spans:
- and, when trained in a contrastive learning framework, enable embedding and structure annotation by database lookup.
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
---

# molecular-fingerprint-generation-and-encoding

## Summary

Encode chemical structures into fixed-dimensional fingerprint representations that can be aligned with mass spectrometry embeddings in a joint latent space. This skill is essential for training contrastive learning models that map tandem MS spectra to molecular structures via shared embedding representations.

## When to use

When you have paired tandem MS spectra and corresponding molecular structures (as SMILES strings or InChI keys) and need to train a model that jointly embeds spectra and structures for structure annotation by database lookup. The skill applies when you want to enable nearest-neighbor retrieval of candidate structures from a reference metabolite database given a novel spectrum.

## When NOT to use

- When structures are not available or are highly incomplete (missing major functional groups), as fingerprints depend on accurate structural representation.
- When the reference database contains very few (<100) unique structures, limiting the ability to learn a discriminative embedding space.
- When only molecular formula or simple metadata is available instead of full chemical structures—use formula-based encoders instead.

## Inputs

- SMILES strings or molecular structure representations
- Reference fingerprint scheme specification (e.g., Morgan fingerprints, ECFP)
- Paired tandem MS spectra and corresponding molecular structures
- Preprocessed spectrum intensity arrays (normalized, noise-filtered)

## Outputs

- Fingerprint embeddings in joint latent space
- Reference metabolite database encoded as embedding vectors
- Structure encoder module weights after contrastive training
- Similarity score matrix between query spectra and reference structures

## How to apply

Preprocess the molecular structure data by converting SMILES strings or structural notation into standardized fingerprint encodings using a reference fingerprint scheme (e.g., Morgan fingerprints, ECFP). Initialize a dedicated chemical structure encoder module within the transformer architecture alongside the spectrum encoder. During contrastive training, feed normalized fingerprints through this encoder to produce fingerprint embeddings that align with spectrum embeddings via contrastive loss with negative sampling from unpaired spectra-structure pairs in each batch. After training convergence, encode the entire reference metabolite database (structures and spectra) into the joint embedding space. Verify alignment by checking that spectra and their true paired structures project to nearby regions in the embedding space with high cosine similarity.

## Related tools

- **MIST** (Transformer architecture that jointly encodes spectra and molecular fingerprints into aligned embeddings for structure annotation by database lookup) — https://github.com/samgoldman97/mist
- **MIST-CF** (Extended MIST variant using similar fingerprint encoding principles but specialized for predicting precursor chemical formulae from MS/MS data) — https://github.com/samgoldman97/mist-cf

## Evaluation signals

- Fingerprint embeddings of paired spectra-structure pairs have cosine similarity > 0.7 after training convergence.
- Top-1 and top-10 recall of true structure annotations when performing nearest-neighbor lookup in reference database embeddings on held-out test spectra.
- Distribution of embedding distances: true paired structures cluster significantly closer than random negative pairs (effect size > 2 standard deviations).
- Consistency of fingerprint encoding: identical structures encoded from different SMILES representations (canonical vs. non-canonical) produce identical or near-identical fingerprint embeddings.
- No mode collapse: embedding space contains diverse regions corresponding to different chemical scaffolds rather than collapsing structures into a narrow region.

## Limitations

- Fingerprint quality and dimensionality depend strongly on the choice of reference scheme; different schemes (Morgan vs. ECFP vs. Daylight) may yield different embedding geometries and retrieval performance.
- Contrastive learning requires careful negative sampling; if the reference database contains structurally similar isomers or diastereomers, false negatives in the training objective can degrade structure annotation accuracy.
- Performance degrades on structures outside the chemical space of the training database (e.g., novel scaffolds or rare natural products not represented in GNPS/NIST).
- The skill assumes availability of high-quality paired spectra-structure labels; errors or ambiguities in structure assignment in the training data propagate directly into learned embeddings.
- Joint embedding space is instrument-dependent; models trained on Orbitrap high-resolution data may perform poorly on lower-resolution time-of-flight or quadrupole instruments without instrument-type covariate conditioning.

## Evidence

- [other] Preprocess spectra (normalize intensities, filter noise) and encode chemical structures into fingerprints using a reference fingerprint scheme.: "Preprocess spectra (normalize intensities, filter noise) and encode chemical structures into fingerprints using a reference fingerprint scheme."
- [other] Train MIST end-to-end using contrastive loss to align spectrum embeddings with fingerprint embeddings, with negative sampling from unpaired spectra-structure pairs in each batch.: "Train MIST end-to-end using contrastive loss to align spectrum embeddings with fingerprint embeddings, with negative sampling from unpaired spectra-structure pairs in each batch."
- [readme] MIST models can be used to predict molecular fingerprints from tandem mass spectrometry data and, when trained in a contrastive learning framework, enable embedding and structure annotation by database lookup.: "MIST models can be used to predict molecular fingerprints from tandem mass spectrometry data and, when trained in a contrastive learning framework, enable embedding and structure annotation by"
- [other] After training convergence, encode a reference metabolite database (spectra and structures) into joint embedding space. For novel spectra, generate embeddings via the trained spectrum encoder and perform nearest-neighbor lookup in the reference database embeddings to retrieve candidate structures with similarity scores.: "After training convergence, encode a reference metabolite database (spectra and structures) into joint embedding space. For novel spectra, generate embeddings via the trained spectrum encoder and"
- [readme] MIST applies a transformer architecture to directly encode and learn to represent collections of chemical formula.: "MIST applies a transformer architecture to directly encode and learn to represent collections of chemical formula."
