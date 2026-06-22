---
name: structure-annotation-via-similarity-ranking
description: Use when you have an unknown tandem MS spectrum and seek to assign a chemical structure by matching against a curated reference database (e.g., NIST, GNPS, or custom metabolite libraries) without requiring an exact spectral match.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3173
  tools:
  - MIST
  - MIST-CF
  techniques:
  - LC-MS
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

# structure-annotation-via-similarity-ranking

## Summary

Annotate unknown metabolite structures by embedding tandem MS spectra into a learned joint chemical space and ranking nearest-neighbor candidates from a reference database. This skill leverages contrastive learning to align spectrum embeddings with molecular fingerprint or chemical formula embeddings, enabling structure retrieval without direct database spectrum matching.

## When to use

Apply this skill when you have an unknown tandem MS spectrum and seek to assign a chemical structure by matching against a curated reference database (e.g., NIST, GNPS, or custom metabolite libraries) without requiring an exact spectral match. Use this when a pre-trained spectrum-to-embedding model is available or can be trained on paired spectra-structure data, and when the reference database has been encoded into the same joint embedding space.

## When NOT to use

- Input spectra are from instruments or ionization modes not represented in the training data; model generalization may be poor.
- Reference database is very small (<100 unique structures) or lacks diversity similar to the query spectrum's molecular class.
- Query spectrum has low signal-to-noise ratio or sparse fragmentation pattern; embeddings may be unreliable.
- No pre-trained or trainable contrastive model is available; standard database search methods (e.g., spectral cosine matching) are more appropriate.

## Inputs

- tandem mass spectrometry spectrum (MGF format or .ms file with m/z and intensity peak pairs)
- reference metabolite database with paired spectra and molecular structures (SMILES or structural fingerprints)
- pre-trained spectrum encoder model (MIST or equivalent transformer architecture)
- pre-trained chemical structure encoder model (fingerprint or formula transformer)

## Outputs

- ranked list of candidate structures with embedding similarity scores
- spectrum embedding vector in joint chemical space
- structure annotations with confidence metrics based on nearest-neighbor distance

## How to apply

Load tandem MS spectra and encode them using a pre-trained spectrum encoder (e.g., MIST transformer trained with contrastive loss). For each query spectrum, generate a continuous embedding in the joint chemical space. Encode a reference metabolite database (containing spectra and corresponding molecular structures or fingerprints) into the same embedding space using matched fingerprint or formula encoders. Perform nearest-neighbor similarity search in the embedding space using distance metrics (e.g., cosine, Euclidean) to retrieve the top-k candidate structures ranked by embedding proximity. The ranking score reflects the learned alignment between spectrum and structure representation; higher similarity indicates stronger agreement between the spectral fragmentation pattern and the candidate molecular structure.

## Related tools

- **MIST** (Transformer-based spectrum encoder trained with contrastive loss to generate spectrum embeddings aligned with fingerprint embeddings; used to encode query spectra and reference spectra into joint embedding space) — https://github.com/samgoldman97/mist
- **MIST-CF** (Extension of MIST for encoding chemical formulas and ranking formula-adduct candidates; can be combined with fingerprint ranking in multi-modal structure annotation) — https://github.com/samgoldman97/mist-cf

## Examples

```
. quickstart/00_download_models.sh && . quickstart/01_run_models.sh && ls quickstart/model_predictions/retrieval/
```

## Evaluation signals

- Retrieve-rank evaluation: measure if true structure appears in top-k (k=1, 5, 10) retrieved candidates; report accuracy or mean reciprocal rank (MRR).
- Embedding space coherence: verify that spectra from the same molecular structure cluster together and are separated from spectra of different structures by larger distances.
- Similarity score distribution: confirm that true structure matches have higher embedding similarity scores (e.g., cosine > 0.7) than decoy or false-positive candidates.
- Consistency across isomers: for molecules with multiple isomers in the reference database, confirm that the method ranks isomers by structural similarity to the query spectrum, not random ties.
- Database coverage: confirm reference database has been fully encoded and is searchable; spot-check that random reference database entries retrieve their own spectra with top-1 rank (sanity check).

## Limitations

- Contrastive model performance depends heavily on training data diversity and size; performance may degrade on spectra from underrepresented instruments (Orbitrap, quadrupole) or ionization modes.
- Similarity ranking assumes the true structure is present in the reference database; performance baseline is limited by database completeness and curation.
- Joint embedding space alignment quality depends on balanced training data; if training pairs are biased toward certain molecular classes (e.g., natural products), retrieval may fail for synthetic or rare metabolites.
- Nearest-neighbor ranking is sensitive to the choice of distance metric and normalization scheme; no consensus on optimal embedding space geometry for metabolite structures is documented.
- False-positive retrievals can occur if the query spectrum is highly similar (by embedding) to multiple non-isomeric structures; additional orthogonal evidence (e.g., retention time, chemical formula validation) is recommended for confirmation.

## Evidence

- [intro] when trained in a contrastive learning framework, MIST enables embedding and structure annotation by database lookup: "when trained in a contrastive learning framework, MIST enables embedding and structure annotation by database lookup"
- [other] Train MIST end-to-end using contrastive loss to align spectrum embeddings with fingerprint embeddings, with negative sampling from unpaired spectra-structure pairs in each batch: "Train MIST end-to-end using contrastive loss to align spectrum embeddings with fingerprint embeddings, with negative sampling from unpaired spectra-structure pairs"
- [other] For novel spectra, generate embeddings via the trained spectrum encoder and perform nearest-neighbor lookup in the reference database embeddings to retrieve candidate structures with similarity scores: "For novel spectra, generate embeddings via the trained spectrum encoder and perform nearest-neighbor lookup in the reference database embeddings to retrieve candidate structures with similarity scores"
- [other] After training convergence, encode a reference metabolite database (spectra and structures) into joint embedding space: "After training convergence, encode a reference metabolite database (spectra and structures) into joint embedding space"
- [other] Preprocess spectra (normalize intensities, filter noise) and encode chemical structures into fingerprints using a reference fingerprint scheme: "Preprocess spectra (normalize intensities, filter noise) and encode chemical structures into fingerprints using a reference fingerprint scheme"
- [readme] annotate spectra by ranking candidates in a reference smiles list: "annotate spectra by ranking candidates in a reference smiles list"
