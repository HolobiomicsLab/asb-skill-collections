---
name: mass2motif-annotation-guidance-via-spectral-embeddings
description: Use when after discovering Mass2Motifs through LDA topic modeling of MS/MS fragmentation data, when you need to assign chemical meaning (substructure classes, candidate annotations) to motifs by leveraging pre-trained spectral embeddings and a reference motif database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MS2LDA
  - MAG
  - Python
  - Spec2Vec
  - MotifDB
  - MassQL
  - LDA (Latent Dirichlet Allocation)
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
- doi: 10.5281/zenodo.15688609
  title: ''
evidence_spans:
- '**MS2LDA** applies *probabilistic topic modeling*, originally developed for natural language processing (NLP), to **tandem mass spectrometry (MS/MS)** data.'
- Invoke the main script `ms2lda_runfull.py` with your arguments
- Automated annotation of **M2M** using **MAG**
- configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
- Configure the Python environment (set `PYTHONPATH`, activate conda, etc.)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda_cq
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda_cq
schema_version: 0.2.0
---

# mass2motif-annotation-guidance-via-spectral-embeddings

## Summary

Automated annotation of Mass2Motifs discovered through LDA-based topic modeling by computing Spec2Vec spectral embeddings for pseudo-spectra representations and querying a motif database to retrieve structurally related reference annotations ranked by similarity. This skill bridges unsupervised substructure discovery with interpretable chemical structure assignment.

## When to use

Apply this skill after discovering Mass2Motifs through LDA topic modeling of MS/MS fragmentation data, when you need to assign chemical meaning (substructure classes, candidate annotations) to motifs by leveraging pre-trained spectral embeddings and a reference motif database. Use it when the motifs are already extracted and represent fragment/neutral-loss probability distributions rather than intact spectra.

## When NOT to use

- Input data are raw MS/MS spectra that have not yet been converted to a bag-of-fragments format or undergone LDA topic modeling; use preprocessing and LDA modeling steps first.
- The Spec2Vec model checkpoint is unavailable or incompatible with the MAG module version; re-download or verify model provenance.
- Mass2Motifs lack sufficient fragment/neutral-loss diversity (e.g., single-fragment motifs) such that pseudo-spectrum embeddings collapse or become uninformative in the embedding space.

## Inputs

- Discovered Mass2Motif objects (fragment/neutral-loss probability distributions from LDA topic modeling)
- Pre-trained Spec2Vec model checkpoint (downloadable from Zenodo 10.5281/zenodo.15688609)
- MotifDB reference motif library (indexed embeddings)
- LDA output (motif composition and fragment/loss assignments with posterior probabilities)

## Outputs

- JSON annotation report mapping each Mass2Motif to candidate substructures
- Confidence scores (similarity scores from embedding-space ranking)
- Structural class labels (chemical classification of assigned motifs)
- Ranked list of reference motif matches per input Mass2Motif

## How to apply

Load the pre-trained Spec2Vec model from the Zenodo repository (10.5281/zenodo.15688609) into the MAG module environment. For each discovered Mass2Motif, construct a pseudo-spectrum by weighting fragments and neutral losses by their inferred LDA probabilities. Compute Spec2Vec vector embeddings for each pseudo-spectrum using the loaded model. Query MotifDB (via MassQL integration or direct embedding lookup) with the computed embeddings to retrieve reference motifs above a similarity threshold (apply default MAG heuristics for ranking). Rank candidate annotations by cosine similarity or other embedding-space distance metric. Filter results using configurable confidence score thresholds and return a structured JSON annotation report mapping each Mass2Motif to candidate substructures, confidence scores, and structural classes.

## Related tools

- **MS2LDA** (Container framework implementing the LDA topic modeling workflow and MAG annotation module; orchestrates preprocessing, modeling, and annotation stages.) — https://github.com/vdhooftcompmet/MS2LDA
- **Spec2Vec** (Pre-trained spectral embedding model that converts pseudo-spectra (and reference motifs) into vector representations in a shared embedding space for similarity-based retrieval.) — https://zenodo.org/records/15688609
- **MotifDB** (Searchable reference database of known mass spectrometry motifs and their annotations; queried via computed Spec2Vec embeddings to retrieve candidate structural assignments.)
- **MassQL** (Query language and interface for searching and retrieving motifs from MotifDB by embedding similarity and metadata criteria.)
- **LDA (Latent Dirichlet Allocation)** (Probabilistic topic model applied to MS/MS fragmentation data to infer Mass2Motifs and their fragment/neutral-loss probability distributions, which serve as input to pseudo-spectrum construction.)
- **Python** (Execution environment for running MS2LDA, loading Spec2Vec models, and orchestrating the annotation workflow via scripts or Jupyter notebooks.)

## Evaluation signals

- Each Mass2Motif in the output JSON has a non-empty list of candidate annotations ranked by confidence score; check that scores are in the range [0, 1] or a bounded similarity metric.
- All candidate annotations resolve to valid chemical structural classes or known fragment patterns in the reference MotifDB; inspect the 'structural_class' field for recognized taxonomy.
- Pseudo-spectrum representations for each Mass2Motif are reproducibly constructed from the same LDA probability vectors; verify determinism by re-running the annotation step and comparing Spec2Vec embeddings (should be identical).
- Embedding-space similarity scores are monotonically ranked within each motif's candidate list; verify sorting order and absence of ties at similar confidence boundaries.
- JSON schema validation passes (required fields: motif_id, candidates[], candidate[].annotation, candidate[].score, candidate[].structural_class); check for completeness and type consistency.

## Limitations

- Annotation quality depends on the coverage and accuracy of the reference MotifDB; if a discovered motif has no close structural analog in the database, candidate scores may be low or uninformative.
- Spec2Vec embeddings are pre-trained on a fixed MS2LDA reference corpus; novel fragmentation patterns or instrument-specific behaviors not present in training data may not be captured accurately.
- Pseudo-spectra representations (constructed from LDA probability-weighted fragments/losses) are synthetic and may not fully recapitulate the statistical properties of observed spectra; edge cases with sparse or noisy LDA posterior distributions can yield unstable embeddings.
- Similarity threshold defaults (MAG heuristics) are tuned for general MS2LDA workflows; domain-specific or instrument-specific projects may require manual threshold adjustment for optimal precision/recall trade-offs.
- Computational cost scales with the number of discovered Mass2Motifs and the size of the MotifDB reference index; large-scale analyses may benefit from batching or index partitioning strategies not detailed in the baseline workflow.

## Evidence

- [other] MS2LDA implements an Automated Mass2Motif Annotation Guidance (MAG) mechanism that integrates a downloaded Spec2Vec model to provide annotation guidance for Mass2Motifs discovered through the topic modeling workflow.: "MS2LDA implements an Automated Mass2Motif Annotation Guidance (MAG) mechanism that integrates a downloaded Spec2Vec model to provide annotation guidance for Mass2Motifs"
- [other] Extract or generate pseudo-spectra representations for each discovered Mass2Motif (fragments and neutral losses weighted by their LDA probabilities).: "Extract or generate pseudo-spectra representations for each discovered Mass2Motif (fragments and neutral losses weighted by their LDA probabilities)"
- [other] Compute Spec2Vec embeddings for each Mass2Motif pseudo-spectrum using the loaded model. Query MotifDB via the loaded embeddings to retrieve structurally related reference motifs and candidate annotations.: "Compute Spec2Vec embeddings for each Mass2Motif pseudo-spectrum using the loaded model. Query MotifDB via the loaded embeddings to retrieve structurally related reference motifs"
- [other] Rank and filter candidate annotations by similarity score (default threshold applied by MAG heuristics). Generate and return an annotation report mapping each Mass2Motif to candidate substructures, confidence scores, and structural classes in JSON format.: "Rank and filter candidate annotations by similarity score (default threshold applied by MAG heuristics). Generate and return an annotation report mapping each Mass2Motif to candidate substructures,"
- [readme] Before running MS2LDA you must download the Spec2Vec model, embeddings, and library DB: "Before running MS2LDA you must download the Spec2Vec model, embeddings, and library DB (See the Zenodo repository)"
- [readme] MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification, thus accelerating structure elucidation and analysis.: "MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification, thus accelerating structure elucidation"
- [methods] Annotation → assign substructure meaning: "Annotation → assign substructure meaning"
