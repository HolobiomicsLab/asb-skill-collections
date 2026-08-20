---
name: motifdb-reference-library-querying
description: Use when after Mass2Motifs have been inferred from tandem MS/MS spectra
  via LDA topic modeling and you need to assign putative substructure annotations
  to those motifs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - MS2LDA
  - MAG
  - MotifDB
  - Python
  - Spec2Vec
  - MAG (Automated Mass2Motif Annotation Guidance)
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- '**MS2LDA** applies *probabilistic topic modeling*, originally developed for natural
  language processing (NLP), to **tandem mass spectrometry (MS/MS)** data.'
- Invoke the main script `ms2lda_runfull.py` with your arguments
- Automated annotation of **M2M** using **MAG**
- Compare motifs to known entries in MotifDB
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

# motifdb-reference-library-querying

## Summary

Query the MotifDB reference library using Spec2Vec embeddings to retrieve structurally related reference motifs and retrieve candidate annotations for discovered Mass2Motifs. This skill bridges unsupervised mass spectrometry fragmentation motif discovery with validated structural knowledge.

## When to use

After Mass2Motifs have been inferred from tandem MS/MS spectra via LDA topic modeling and you need to assign putative substructure annotations to those motifs. Specifically, use this skill when you have pseudo-spectra representations (fragment m/z and neutral loss values weighted by LDA probabilities) for each discovered motif and want to retrieve ranked candidate annotations with confidence scores.

## When NOT to use

- Mass2Motifs have not yet been inferred from MS/MS spectra (LDA modeling step must precede querying).
- No pre-trained Spec2Vec model is available or cannot be downloaded from the specified Zenodo repository.
- Pseudo-spectra cannot be reliably constructed (e.g., LDA probabilities are not available or fragments/neutral losses are unreliable).

## Inputs

- Mass2Motif pseudo-spectra (fragments and neutral losses with LDA probabilities)
- Pre-trained Spec2Vec model (binary file from Zenodo 15688609)
- MotifDB reference library (searchable motif entries with structural annotations)

## Outputs

- Annotated Mass2Motif report (JSON format with candidate substructures per motif)
- Ranked candidate annotations with similarity scores
- Structural class assignments and confidence metrics

## How to apply

First, compute Spec2Vec embeddings for each discovered Mass2Motif pseudo-spectrum using a pre-trained Spec2Vec model (downloaded from Zenodo 15688609). Then query MotifDB via these embeddings to retrieve a ranked set of structurally related reference motifs. Rank and filter candidate annotations by similarity score using MAG module heuristics (typically a default threshold that balances specificity and recall). Generate an annotation report mapping each Mass2Motif to candidate substructures, confidence scores, and structural classes. The rationale is that Spec2Vec embeddings capture semantic similarity in fragmentation patterns learned from large reference spectral corpora, allowing transfer of known structural annotations to newly discovered motifs without requiring manual database curation.

## Related tools

- **MS2LDA** (Orchestrates the full workflow; provides the LDA-inferred Mass2Motif definitions and MAG module that integrates Spec2Vec querying.) — https://github.com/vdhooftcompmet/MS2LDA
- **Spec2Vec** (Pre-trained neural embedding model that computes similarity-preserving representations of pseudo-spectra for MotifDB querying.)
- **MotifDB** (Searchable reference library of known MS2 fragmentation motifs and structural annotations indexed for rapid retrieval via Spec2Vec embeddings.)
- **MAG (Automated Mass2Motif Annotation Guidance)** (MS2LDA module that orchestrates Spec2Vec embedding computation, MotifDB querying, and candidate filtering/ranking to produce final annotation reports.) — https://github.com/vdhooftcompmet/MS2LDA

## Evaluation signals

- All discovered Mass2Motifs receive ≥1 candidate annotation with a similarity score above the MAG default threshold.
- Returned structural classes are valid and consistent with known fragmentation chemistry for the putative substructures.
- Annotation report is valid JSON with expected schema (motif_id, candidates[], confidence_scores[], structural_classes[]).
- Candidate annotations are ranked monotonically by similarity score (highest first).
- Re-running the query with the same Spec2Vec model and MotifDB snapshot yields identical results (determinism check).

## Limitations

- Annotation quality depends on the coverage and accuracy of the MotifDB reference library; rare or novel motifs may receive low-confidence or no matches.
- Spec2Vec model performance is sensitive to the training corpora used to pre-train the model; out-of-domain MS/MS data may yield suboptimal embeddings.
- Default MAG similarity thresholds are heuristic-based and may require tuning for specific analytical contexts (e.g., metabolomics vs. natural products).
- The MAG module does not account for competing structural hypotheses or multi-class substructures; annotations are treated independently.

## Evidence

- [methods] Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec: "Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec"
- [methods] Extract or generate pseudo-spectra representations for each discovered Mass2Motif (fragments and neutral losses weighted by their LDA probabilities). Compute Spec2Vec embeddings for each Mass2Motif pseudo-spectrum using the loaded model. Query MotifDB via the loaded embeddings to retrieve structurally related reference motifs and candidate annotations.: "Extract or generate pseudo-spectra representations for each discovered Mass2Motif (fragments and neutral losses weighted by their LDA probabilities). Compute Spec2Vec embeddings for each Mass2Motif"
- [methods] Rank and filter candidate annotations by similarity score (default threshold applied by MAG heuristics). Generate and return an annotation report mapping each Mass2Motif to candidate substructures, confidence scores, and structural classes in JSON format.: "Rank and filter candidate annotations by similarity score (default threshold applied by MAG heuristics). Generate and return an annotation report mapping each Mass2Motif to candidate substructures,"
- [methods] Before running MS2LDA you must download the Spec2Vec model, embeddings, and library DB (See the Zenodo repository): "Before running MS2LDA you must download the Spec2Vec model, embeddings, and library DB (See the Zenodo repository)"
- [readme] MS2LDA includes a web-based visualization application (MS2LDAViz) for exploring and analyzing results.: "MS2LDA includes a web-based visualization application (MS2LDAViz) for exploring and analyzing results."
