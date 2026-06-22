---
name: metabolite-database-embedding-lookup
description: Use when when you have paired tandem MS spectra and known molecular structures (SMILES or fingerprints) and want to annotate novel spectra by retrieving similar structures from a reference database without relying on spectral database matching.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
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

# metabolite-database-embedding-lookup

## Summary

Train a spectrum transformer model using contrastive learning to align tandem MS spectrum embeddings with molecular structure fingerprint embeddings, enabling structure annotation through nearest-neighbor lookup in a reference metabolite database. This approach replaces database-dependent fragmentation tree matching with learned joint embedding spaces.

## When to use

When you have paired tandem MS spectra and known molecular structures (SMILES or fingerprints) and want to annotate novel spectra by retrieving similar structures from a reference database without relying on spectral database matching. Use this when you need to generalize beyond existing spectral libraries or when contrastive embedding-based retrieval outperforms traditional cosine/spectral similarity metrics.

## When NOT to use

- Input consists only of MS1 precursor masses without fragmentation spectra; use MIST-CF for chemical formula prediction instead.
- Reference database is very small (< 100 metabolites) or highly specialized; contrastive learning may not yield robust embeddings.
- Negative mode spectra or multiple adduct types are required; original MIST focuses on positive mode [M+H]+ only.

## Inputs

- Tandem MS spectra (MGF format or .ms files with m/z and intensity pairs)
- Molecular structures as SMILES strings or known chemical identifiers
- Reference metabolite database with both spectra and structures

## Outputs

- Joint embedding space (spectrum embeddings and fingerprint embeddings aligned)
- Ranked candidate structures for query spectra with similarity scores
- Structure annotations with relevance scores

## How to apply

Load paired tandem MS spectra and corresponding molecular structures as training data. Preprocess spectra by normalizing intensities and filtering noise; encode structures into molecular fingerprints using a reference fingerprint scheme (e.g., ECFP). Initialize a MIST transformer with separate spectrum encoder and fingerprint encoder modules. Train end-to-end using contrastive loss (with negative sampling from unpaired spectra-structure pairs in each batch) to align spectrum embeddings with fingerprint embeddings in a joint space. After training convergence, encode a reference metabolite database (all spectra and structures) into the learned joint embedding space. For novel query spectra, generate embeddings via the trained spectrum encoder and perform k-nearest-neighbor lookup in the reference database embeddings to retrieve candidate structures, ranked by similarity scores (e.g., cosine distance in embedding space).

## Related tools

- **MIST** (Transformer architecture for encoding spectra and fingerprints; provides the spectrum and fingerprint encoder modules trained via contrastive loss) — https://github.com/samgoldman97/mist
- **MIST-CF** (Extension for chemical formula prediction from MS/MS data; complements structure annotation with formula constraints) — https://github.com/samgoldman97/mist-cf

## Examples

```
. quickstart/00_download_models.sh && . quickstart/01_run_models.sh
```

## Evaluation signals

- Retrieval rank metric: fraction of query spectra for which the correct structure ranks in top-k (e.g., top-1, top-5, top-10)
- Embedding space alignment: verify that paired spectrum-fingerprint embeddings are closer than randomly sampled spectrum-fingerprint pairs; measure via contrastive loss convergence
- Cosine similarity distribution: confirm that true positive pairs have higher cosine similarity in the joint embedding space than false positives from the same batch
- Database lookup precision: for a held-out test set of spectra, verify that nearest-neighbor candidates match known ground-truth structures with acceptable error rates
- Embedding space stability: re-encode the same spectra multiple times and confirm embeddings are reproducible (e.g., correlation > 0.99)

## Limitations

- Method requires paired spectrum-structure training data; performance degrades if training set lacks chemical diversity or is biased toward certain instrument types or ionization modes.
- Contrastive learning depends on quality negative sampling; poor negative sampling (e.g., similar but incorrect structures in a batch) can hurt embedding alignment.
- Original MIST focuses on positive mode MS/MS with [M+H]+ adducts; multiple adduct types and negative mode support require model extension (as noted in MIST-CF README).
- Reference database size and composition affect retrieval performance; small or non-representative databases yield lower annotation accuracy.
- Joint embedding space is specific to the fingerprint encoding scheme used during training; transferability to different fingerprint schemes is limited.

## Evidence

- [intro] When trained in a contrastive learning framework, MIST enables embedding and structure annotation by database lookup.: "when trained in a contrastive learning framework, MIST enables embedding and structure annotation by database lookup"
- [other] Train MIST end-to-end using contrastive loss to align spectrum embeddings with fingerprint embeddings, with negative sampling from unpaired spectra-structure pairs in each batch.: "Train MIST end-to-end using contrastive loss to align spectrum embeddings with fingerprint embeddings, with negative sampling from unpaired spectra-structure pairs in each batch"
- [other] For novel spectra, generate embeddings via the trained spectrum encoder and perform nearest-neighbor lookup in the reference database embeddings to retrieve candidate structures with similarity scores.: "For novel spectra, generate embeddings via the trained spectrum encoder and perform nearest-neighbor lookup in the reference database embeddings to retrieve candidate structures with similarity scores"
- [readme] MIST models can be used to predict molecular fingerprints from tandem mass spectrometry data and, when trained in a contrastive learning framework, enable embedding and structure annotation by database lookup.: "MIST models can be used to predict molecular fingerprints from tandem mass spectrometry data and, when trained in a contrastive learning framework, enable embedding and structure annotation by"
- [other] Preprocess spectra (normalize intensities, filter noise) and encode chemical structures into fingerprints using a reference fingerprint scheme.: "Preprocess spectra (normalize intensities, filter noise) and encode chemical structures into fingerprints using a reference fingerprint scheme"
