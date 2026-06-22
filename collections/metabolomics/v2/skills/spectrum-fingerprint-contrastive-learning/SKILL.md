---
name: spectrum-fingerprint-contrastive-learning
description: Use when when you have paired tandem MS spectra and corresponding molecular structures (SMILES or fingerprints), and you want to build a retrieval system for metabolite structure annotation that can rank candidate structures for novel spectra by embedding similarity rather than spectral matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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

# spectrum-fingerprint-contrastive-learning

## Summary

Train a transformer-based model using contrastive learning to align tandem MS spectra embeddings with molecular fingerprint embeddings, enabling structure annotation via nearest-neighbor lookup in a reference database. This approach learns joint spectrum-structure representations without requiring direct fragmentation tree computation.

## When to use

When you have paired tandem MS spectra and corresponding molecular structures (SMILES or fingerprints), and you want to build a retrieval system for metabolite structure annotation that can rank candidate structures for novel spectra by embedding similarity rather than spectral matching scores alone.

## When NOT to use

- Input spectra lack corresponding structure annotations; contrastive learning requires paired training data.
- Goal is de novo formula annotation without a reference structure database; use MIST-CF instead.
- Spectra are from a single, highly specialized instrument class; cross-instrument generalization may suffer without instrument type embedding as a model covariate.

## Inputs

- Tandem MS spectra (MGF or .ms format with m/z and intensity pairs)
- SMILES strings or molecular structures paired with spectra
- Reference molecular fingerprint encoding scheme
- Unpaired molecular structure library for negative sampling

## Outputs

- Trained MIST transformer checkpoint (spectrum and fingerprint encoders)
- Joint embedding space with reference database encoded
- Ranked candidate structures for query spectra with embedding similarity scores

## How to apply

Load paired training data of tandem MS spectra and SMILES/structures. Preprocess spectra by normalizing intensities and filtering noise, and encode structures into molecular fingerprints using a reference scheme. Initialize a MIST transformer with dual encoders: one for spectra (peak m/z and intensity) and one for fingerprints. Train end-to-end using contrastive loss with negative sampling from unpaired spectra-structure pairs within each batch to align the two embedding spaces. After convergence, encode a reference metabolite database (both spectra and structures) into the learned joint embedding space. For novel spectra, generate embeddings via the spectrum encoder and perform nearest-neighbor lookup to retrieve ranked candidate structures with similarity scores.

## Related tools

- **MIST** (Core transformer architecture for dual spectrum and fingerprint encoding and contrastive training) — https://github.com/samgoldman97/mist
- **MIST-CF** (Related extension for chemical formula prediction; shares transformer advances applicable back to MIST fingerprint encoder) — https://github.com/samgoldman97/mist-cf

## Examples

```
. quickstart/00_download_models.sh && . quickstart/01_run_models.sh
```

## Evaluation signals

- Embedding space alignment: spectrum and fingerprint embeddings for the same molecule cluster together; embeddings for different molecules separate by cosine distance.
- Retrieval ranking accuracy: top-k recall and mean reciprocal rank of the true structure candidate in nearest-neighbor lookups on held-out test spectra.
- Loss convergence: contrastive loss plateaus during training and validation loss does not increase, indicating stable joint embedding.
- Database lookup coverage: percentage of query spectra for which the reference database returns candidate structures within a minimum similarity threshold (e.g., cosine > 0.7).

## Limitations

- Contrastive learning relies on balanced negative sampling; skewed or imbalanced pairing of spectra and structures may bias embeddings toward abundant molecular families.
- Fingerprint choice (e.g., Morgan, ECFP) affects embedding quality; the skill is sensitive to the reference fingerprint encoding scheme used.
- Performance degrades on spectra from instruments or ionization modes underrepresented in training data; MIST-CF demonstrates that embedding instrument type as a covariate helps, suggesting this should be incorporated.
- Spectral preprocessing (noise filtering, normalization method) impacts learned representations; preprocessing parameters are not deeply explored in the primary MIST paper but are listed as critical steps.

## Evidence

- [intro] When trained in a contrastive learning framework, MIST enables embedding and structure annotation by database lookup.: "when trained in a contrastive learning framework, MIST enables embedding and structure annotation by database lookup"
- [other] 1. Load tandem MS spectra and corresponding molecular structures or SMILES strings as paired training data. 2. Preprocess spectra (normalize intensities, filter noise) and encode chemical structures into fingerprints using a reference fingerprint scheme. 3. Initialize MIST transformer architecture with spectrum encoder and chemical formula/fingerprint encoder modules. 4. Train MIST end-to-end using contrastive loss to align spectrum embeddings with fingerprint embeddings, with negative sampling from unpaired spectra-structure pairs in each batch.: "Train MIST end-to-end using contrastive loss to align spectrum embeddings with fingerprint embeddings, with negative sampling from unpaired spectra-structure pairs"
- [other] For novel spectra, generate embeddings via the trained spectrum encoder and perform nearest-neighbor lookup in the reference database embeddings to retrieve candidate structures with similarity scores.: "generate embeddings via the trained spectrum encoder and perform nearest-neighbor lookup in the reference database embeddings to retrieve candidate structures"
- [intro] MIST applies a transformer architecture to directly encode and learn to represent collections of chemical formula.: "MIST applies a transformer architecture to directly encode and learn to represent collections of chemical formula"
- [readme] We provide an additional notebook notebooks/mist_demo.ipynb that shows these calls programmatically, rather than in the command line.: "pretrained models can be used to: 1. Predict fingerprints from spectra 2. Annotate spectra by ranking candidates in a reference smiles list 3. Embed spectra into a dense continuous space"
