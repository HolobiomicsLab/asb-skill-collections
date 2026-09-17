---
name: spectral-similarity-scoring-and-ranking
description: Use when after discovering Mass2Motifs via LDA topic modeling on MS/MS
  data, when you need to assign putative structural annotations to those motifs by
  comparing their fragmentation signatures (weighted fragment and neutral loss distributions)
  to a curated reference database of known motifs and.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_3372
  - http://edamontology.org/topic_0091
  tools:
  - MS2LDA
  - MAG
  - Python
  - Spec2Vec
  - MotifDB
  - MAG (Automated Mass2Motif Annotation Guidance)
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

# spectral-similarity-scoring-and-ranking

## Summary

Score and rank candidate Mass2Motif annotations by computing Spec2Vec embeddings for pseudo-spectra (fragment and neutral loss distributions) and querying a reference motif database to retrieve structurally related motifs, filtered by similarity threshold. This enables automated, confidence-scored structural annotation of discovered Mass2Motifs.

## When to use

After discovering Mass2Motifs via LDA topic modeling on MS/MS data, when you need to assign putative structural annotations to those motifs by comparing their fragmentation signatures (weighted fragment and neutral loss distributions) to a curated reference database of known motifs and their associated substructures.

## When NOT to use

- When no pre-trained Spec2Vec model or reference motif database (MotifDB) is available or accessible in your environment.
- When Mass2Motifs have been derived from ion-mode-specific data (e.g., positive-only) and you need to cross-annotate against mixed-polarity reference databases without harmonization.
- When fragmentation patterns are extremely sparse or low-probability (LDA weight << 0.01), as embeddings may not reliably distinguish signal from noise.

## Inputs

- Discovered Mass2Motifs (LDA topic output with fragment–probability and neutral loss–probability distributions)
- Pre-trained Spec2Vec model (downloadable from Zenodo 15688609)
- MotifDB reference database with embedded motif vectors and structural annotations

## Outputs

- JSON annotation report mapping each Mass2Motif to ranked candidate substructures
- Confidence scores and similarity rankings for each annotation candidate
- Structural class assignments for each Mass2Motif

## How to apply

Extract or generate pseudo-spectra for each discovered Mass2Motif by weighting fragments and neutral losses by their LDA probabilities. Load a pre-trained Spec2Vec model (downloaded from Zenodo) into the MAG module and compute Spec2Vec embeddings for each pseudo-spectrum, converting fragmentation patterns into a vector space representation. Query MotifDB using these embeddings to retrieve candidate reference motifs ranked by cosine or similar distance metric. Apply a similarity score threshold (MAG default heuristics) to filter candidates and retain only high-confidence matches. Generate and export an annotation report in JSON format mapping each Mass2Motif to ranked candidate substructures, confidence scores, and structural classes. The rationale is that Spec2Vec embeddings capture spectral semantics even when fragment exact masses differ, enabling robust cross-dataset motif matching.

## Related tools

- **Spec2Vec** (Embedding model that converts Mass2Motif pseudo-spectra (fragment and neutral loss distributions) into fixed-size vector representations for similarity-based querying against MotifDB) — https://zenodo.org/records/15688609
- **MotifDB** (Reference database of known Mass2Motifs with pre-computed embeddings and structural annotations; queried via Spec2Vec embeddings to retrieve candidate annotations ranked by similarity score)
- **MAG (Automated Mass2Motif Annotation Guidance)** (Orchestrator module that integrates Spec2Vec embeddings, MotifDB queries, and annotation ranking heuristics to produce confidence-scored structural assignments) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA** (Parent workflow tool that discovers Mass2Motifs via LDA and integrates MAG for annotation; provides preprocessing, LDA modeling, and visualization context for this skill) — https://github.com/vdhooftcompmet/MS2LDA

## Examples

```
mag = MAG(spec2vec_model_path='zenodo_15688609/model.pkl', motifdb_path='zenodo_15688609/motifdb.json'); ranked_annotations = mag.annotate_motifs(mass2motifs=discovered_motifs, similarity_threshold=0.7); report = mag.export_json('annotation_report.json')
```

## Evaluation signals

- All Mass2Motifs in the output report have a non-null similarity score and at least one ranked candidate annotation with confidence ≥ MAG threshold (verify JSON schema compliance and no null similarity values).
- Candidate substructures returned for each Mass2Motif are drawn from MotifDB and have corresponding structural class labels; cross-validate a random sample of top-ranked candidates against literature or independent MS/MS databases.
- Similarity score distribution across Mass2Motifs is non-trivial (not all 1.0 or all ≤ 0.5); check histogram/quantile summary to ensure the embedding space and ranking are discriminative.
- Pseudo-spectra weights (LDA probabilities) for each Mass2Motif sum to ~1.0 and include both fragments and neutral losses; verify input data integrity before embedding.
- JSON report is machine-readable and conforms to documented schema; parse and validate field names, data types, and required keys (e.g., 'candidate_substructures', 'confidence_scores', 'structural_class').

## Limitations

- Annotation accuracy is bounded by the completeness and representativeness of MotifDB; novel or rare substructures not in the reference set will receive low or no matches.
- Spec2Vec embeddings may conflate spectrally similar but structurally distinct motifs (false positives) or fail to match motifs with unusual fragmentation behavior not well-represented in the training set.
- The similarity threshold and ranking heuristics are fixed defaults in MAG and may not be optimal for all compound classes or ionization modes; manual threshold tuning and validation are recommended for high-stakes structural elucidation.
- Pseudo-spectra generation is sensitive to LDA convergence and prior hyperparameters; poorly converged or over/under-regularized LDA models will propagate as unreliable fragment–probability weightings into embeddings.

## Evidence

- [other] Extract or generate pseudo-spectra representations for each discovered Mass2Motif (fragments and neutral losses weighted by their LDA probabilities): "Extract or generate pseudo-spectra representations for each discovered Mass2Motif (fragments and neutral losses weighted by their LDA probabilities)."
- [other] Compute Spec2Vec embeddings for each Mass2Motif pseudo-spectrum using the loaded model. Query MotifDB via the loaded embeddings to retrieve structurally related reference motifs and candidate annotations.: "Compute Spec2Vec embeddings for each Mass2Motif pseudo-spectrum using the loaded model. Query MotifDB via the loaded embeddings to retrieve structurally related reference motifs and candidate"
- [other] Rank and filter candidate annotations by similarity score (default threshold applied by MAG heuristics). Generate and return an annotation report mapping each Mass2Motif to candidate substructures, confidence scores, and structural classes in JSON format.: "Rank and filter candidate annotations by similarity score (default threshold applied by MAG heuristics). Generate and return an annotation report mapping each Mass2Motif to candidate substructures,"
- [methods] Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec: "Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec"
- [readme] Before running MS2LDA you must download the Spec2Vec model, embeddings, and library DB: "Before running MS2LDA you must download the Spec2Vec model, embeddings, and library DB (See the Zenodo repository)"
