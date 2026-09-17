---
name: spec2vec-model-loading-and-inference
description: Use when you have discovered Mass2Motifs or other fragmentation pattern
  representations via LDA and need to generate vector embeddings to query a reference
  motif database (MotifDB) for structural annotation candidates.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2939
  edam_topics:
  - http://edamontology.org/topic_0943
  - http://edamontology.org/topic_3371
  - http://edamontology.org/topic_0602
  tools:
  - MS2LDA
  - Spec2Vec
  - MAG
  - Python
  - MotifDB
  - MAG (Mass2Motif Annotation Guidance)
  - Latent Dirichlet Allocation (LDA)
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- '**MS2LDA** applies *probabilistic topic modeling*, originally developed for natural
  language processing (NLP), to **tandem mass spectrometry (MS/MS)** data.'
- Invoke the main script `ms2lda_runfull.py` with your arguments
- Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1073/pnas.1608041113
  all_source_dois:
  - 10.1073/pnas.1608041113
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spec2vec-model-loading-and-inference

## Summary

Load a pre-trained Spec2Vec model and compute spectral embeddings for mass spectrometry data or pseudo-spectra (e.g., Mass2Motifs) to enable similarity-based retrieval and annotation. This is a core computational step within MS2LDA's Automated Mass2Motif Annotation Guidance (MAG) pipeline.

## When to use

Apply this skill when you have discovered Mass2Motifs or other fragmentation pattern representations via LDA and need to generate vector embeddings to query a reference motif database (MotifDB) for structural annotation candidates. Specifically, use it after LDA-based topic modeling has produced Mass2Motif pseudo-spectra (fragments and neutral losses weighted by their LDA probabilities) and you require similarity-based ranking of candidate annotations.

## When NOT to use

- Input spectra have not been processed through LDA topic modeling; raw fragmentation patterns without probabilistic motif assignment cannot be meaningfully represented as weighted pseudo-spectra.
- The pre-trained Spec2Vec model is unavailable or incompatible with your spectral data format or MS/MS acquisition mode (e.g., model was trained on positive-mode spectra but your data is negative-mode only).
- MotifDB is absent or the reference library does not contain relevant structural motifs for your compound class; queries will return low-confidence or irrelevant candidates.

## Inputs

- Pre-trained Spec2Vec model (from Zenodo 15688609)
- Discovered Mass2Motifs (fragments and neutral losses with LDA probability weights)
- Reference motif database (MotifDB)
- MS/MS pseudo-spectra or synthetic spectra representing motif compositions

## Outputs

- Spec2Vec embeddings (vector representations of Mass2Motifs)
- Ranked candidate annotations with similarity scores
- Annotation report (JSON format) mapping Mass2Motifs to substructures and confidence scores
- Structural class assignments for each motif

## How to apply

First, download the pre-trained Spec2Vec model, embeddings, and library database from the designated Zenodo repository (zenodo.org/records/15688609) into your MS2LDA environment. Load the model artifact into memory within the MAG module. For each discovered Mass2Motif, construct or extract its pseudo-spectrum representation by combining fragments and neutral losses weighted by their inferred LDA probabilities. Pass each pseudo-spectrum through the loaded Spec2Vec model to compute a vector embedding. Use these embeddings to query MotifDB, retrieving structurally related reference motifs ranked by cosine similarity or equivalent distance metric. Apply the MAG heuristic threshold (default parameters) to filter candidate annotations. Return a JSON-formatted annotation report mapping each Mass2Motif to ranked candidate substructures, confidence scores, and structural classes.

## Related tools

- **MS2LDA** (Parent workflow framework that integrates Spec2Vec model loading and inference within the MAG (Automated Mass2Motif Annotation Guidance) module for automated motif annotation) — https://github.com/vdhooftcompmet/MS2LDA
- **Spec2Vec** (Pre-trained embedding model used to encode pseudo-spectra into fixed-dimensional vectors for similarity-based motif retrieval and ranking)
- **MotifDB** (Reference motif database queried via Spec2Vec embeddings to retrieve and rank candidate structural annotations for discovered Mass2Motifs)
- **MAG (Mass2Motif Annotation Guidance)** (MS2LDA submodule that orchestrates Spec2Vec model loading, embedding computation, and heuristic filtering to generate annotation reports)
- **Latent Dirichlet Allocation (LDA)** (Upstream probabilistic topic modeling step that produces Mass2Motifs (fragments and neutral losses with LDA probabilities) fed to Spec2Vec for embedding)

## Evaluation signals

- Spec2Vec embeddings are successfully computed for all discovered Mass2Motifs without shape mismatches or NaN values; dimensionality matches the model's output layer.
- MotifDB queries return candidate annotations ranked by similarity score; top-ranked candidates have similarity scores above the applied MAG threshold and correspond to structurally plausible substructures.
- JSON annotation report is well-formed, contains all Mass2Motifs with non-empty candidate lists (or justified empty lists), and confidence scores are numeric and bounded (e.g., 0–1 or percentile rank).
- Annotation quality can be spot-checked against known reference compounds in the dataset (where structure is independently confirmed); annotation candidates should include true substructural features with high confidence scores.
- Spec2Vec embedding vectors and MotifDB query results are reproducible across runs (same input motifs produce identical or near-identical embeddings and candidate rankings).

## Limitations

- Spec2Vec model performance depends on the quality and coverage of the training corpus; structural motifs absent from the training data or MotifDB will not be reliably retrieved or ranked.
- MAG heuristic thresholds are fixed by default; threshold tuning may be required for different spectral datasets or compound classes, and no automated threshold selection mechanism is provided.
- Pseudo-spectrum generation (weighting fragments by LDA probabilities) assumes that high-probability fragments are more structurally informative; outlier or noisy fragments can degrade embedding quality.
- MotifDB completeness and relevance to the target compound class (e.g., natural products vs. pharmaceuticals) directly constrain annotation utility; incomplete or biased reference libraries will limit candidate recall.
- Model and database versions must be kept in sync; using outdated or mismatched Spec2Vec/MotifDB versions may produce inconsistent or incorrect rankings.

## Evidence

- [methods] Before running MS2LDA you must download the Spec2Vec model, embeddings, and library DB: "Before running MS2LDA you must download the Spec2Vec model, embeddings, and library DB (See the Zenodo repository)"
- [other] Extract or generate pseudo-spectra representations for each discovered Mass2Motif (fragments and neutral losses weighted by their LDA probabilities): "Extract or generate pseudo-spectra representations for each discovered Mass2Motif (fragments and neutral losses weighted by their LDA probabilities)."
- [other] Compute Spec2Vec embeddings for each Mass2Motif pseudo-spectrum using the loaded model: "Compute Spec2Vec embeddings for each Mass2Motif pseudo-spectrum using the loaded model."
- [other] Query MotifDB via the loaded embeddings to retrieve structurally related reference motifs and candidate annotations: "Query MotifDB via the loaded embeddings to retrieve structurally related reference motifs and candidate annotations."
- [other] Rank and filter candidate annotations by similarity score (default threshold applied by MAG heuristics): "Rank and filter candidate annotations by similarity score (default threshold applied by MAG heuristics)."
- [other] Generate and return an annotation report mapping each Mass2Motif to candidate substructures, confidence scores, and structural classes in JSON format: "Generate and return an annotation report mapping each Mass2Motif to candidate substructures, confidence scores, and structural classes in JSON format."
- [other] MS2LDA implements an Automated Mass2Motif Annotation Guidance (MAG) mechanism that integrates a downloaded Spec2Vec model: "MS2LDA implements an Automated Mass2Motif Annotation Guidance (MAG) mechanism that integrates a downloaded Spec2Vec model to provide annotation guidance for Mass2Motifs discovered through the topic"
