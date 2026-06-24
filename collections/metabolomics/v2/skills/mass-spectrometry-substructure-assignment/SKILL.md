---
name: mass-spectrometry-substructure-assignment
description: Use when after Mass2Motif discovery via LDA on preprocessed MS/MS spectra,
  when you have a set of inferred motifs (fragments and neutral losses with LDA probabilities)
  and need to assign putative substructure identities rather than retain anonymous
  motif labels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0224
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - MS2LDA
  - MAG
  - Python
  - Spec2Vec
  - MotifDB
  - MassQL
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

# mass-spectrometry-substructure-assignment

## Summary

Automated assignment of chemical substructures to discovered Mass2Motifs by embedding their pseudo-spectra into a pretrained Spec2Vec model and querying a reference motif database (MotifDB) for structurally related candidates ranked by similarity. This skill enables rapid annotation of recurring fragmentation patterns discovered through MS2LDA topic modeling, converting unsupervised motifs into interpretable structural classes.

## When to use

After Mass2Motif discovery via LDA on preprocessed MS/MS spectra, when you have a set of inferred motifs (fragments and neutral losses with LDA probabilities) and need to assign putative substructure identities rather than retain anonymous motif labels. Particularly useful in untargeted metabolomics workflows where prior compound identification is unavailable and structural interpretation of fragmentation patterns is desired.

## When NOT to use

- Input motifs have not been validated or filtered for quality (e.g., motifs with very low LDA probability or minimal supporting spectra should be excluded first).
- MS/MS spectra have not been preprocessed (noise filtering, ion mode separation) prior to LDA; MAG assumes clean, reliable pseudo-spectra.
- Reference MotifDB is known to be incomplete or misannotated for your compound class; annotation results will inherit those biases.

## Inputs

- Discovered Mass2Motifs (fragments and neutral losses weighted by LDA probabilities)
- Pretrained Spec2Vec model checkpoint (downloadable from Zenodo 15688609)
- MotifDB reference database (accompanying Spec2Vec model package)

## Outputs

- JSON annotation report mapping Mass2Motif IDs to ranked candidate substructures
- Confidence scores and structural class assignments per motif
- Filtered candidate list adhering to MAG similarity threshold

## How to apply

Load the pretrained Spec2Vec model (from zenodo.org/records/15688609) into the MAG (Mass2Motif Annotation Guidance) module. For each discovered Mass2Motif, construct a pseudo-spectrum by weighting fragment ions and neutral losses by their LDA probabilities. Compute Spec2Vec embeddings for each pseudo-spectrum using the loaded model. Query MotifDB via these embeddings to retrieve ranked candidate motifs and annotations. Apply MAG's default similarity score threshold to filter candidates, and generate a JSON report mapping each Mass2Motif to ranked candidate substructures, confidence scores, and structural classes. The workflow prioritizes high-confidence matches (above threshold) and discards low-scoring candidates to minimize false annotations.

## Related tools

- **MS2LDA** (Performs LDA-based topic modeling on MS/MS spectra to discover Mass2Motifs; MAG integrates as its annotation module) — https://github.com/vdhooftcompmet/MS2LDA
- **Spec2Vec** (Pretrained neural embedding model that encodes pseudo-spectra (fragments + neutral losses) into vector space for similarity-based querying) — https://zenodo.org/records/15688609
- **MotifDB** (Reference database of structurally characterized motifs queried via Spec2Vec embeddings to retrieve candidate annotations)
- **MassQL** (Integration layer enabling structured queries against MotifDB search results)
- **Python** (Runtime environment for MAG module and Spec2Vec inference)

## Evaluation signals

- JSON report contains all discovered Mass2Motifs with at least one ranked candidate annotation (no empty motif entries).
- Confidence scores for top candidates fall within expected range (e.g., 0–1 normalized similarity); candidates below MAG threshold are excluded.
- Pseudo-spectra embeddings are deterministic and reproducible across runs (same motif input → same Spec2Vec vector → same MotifDB ranking).
- Reported structural classes are logically consistent with LDA-inferred fragment composition (e.g., fragments matching known loss patterns for the assigned substructure).
- Candidates ranked by Spec2Vec similarity score show monotone decreasing confidence; no inversions or ties unexplained by tied similarity values.

## Limitations

- Annotation quality depends entirely on Spec2Vec model training data and MotifDB completeness; motifs absent or poorly represented in training will receive low-confidence or spurious assignments.
- MAG heuristics apply a fixed similarity threshold; users cannot easily customize sensitivity vs. specificity trade-off per motif or dataset.
- Pseudo-spectra are synthetic constructs (weighted fragment distributions); they may not capture rare but structurally informative peaks if those peaks have low LDA probability.
- No confidence propagation from LDA model uncertainty (posterior variance) to final annotation scores; MAG treats all motifs equally regardless of LDA fit quality.

## Evidence

- [other] MS2LDA implements an Automated Mass2Motif Annotation Guidance (MAG) mechanism that integrates a downloaded Spec2Vec model to provide annotation guidance for Mass2Motifs discovered through the topic modeling workflow.: "MS2LDA implements an Automated Mass2Motif Annotation Guidance (MAG) mechanism that integrates a downloaded Spec2Vec model to provide annotation guidance for Mass2Motifs discovered through the topic"
- [other] Extract or generate pseudo-spectra representations for each discovered Mass2Motif (fragments and neutral losses weighted by their LDA probabilities).: "Extract or generate pseudo-spectra representations for each discovered Mass2Motif (fragments and neutral losses weighted by their LDA probabilities)."
- [other] Compute Spec2Vec embeddings for each Mass2Motif pseudo-spectrum using the loaded model.: "Compute Spec2Vec embeddings for each Mass2Motif pseudo-spectrum using the loaded model."
- [other] Query MotifDB via the loaded embeddings to retrieve structurally related reference motifs and candidate annotations.: "Query MotifDB via the loaded embeddings to retrieve structurally related reference motifs and candidate annotations."
- [other] Rank and filter candidate annotations by similarity score (default threshold applied by MAG heuristics).: "Rank and filter candidate annotations by similarity score (default threshold applied by MAG heuristics)."
- [other] Generate and return an annotation report mapping each Mass2Motif to candidate substructures, confidence scores, and structural classes in JSON format.: "Generate and return an annotation report mapping each Mass2Motif to candidate substructures, confidence scores, and structural classes in JSON format."
- [readme] MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification: "MS2LDA addresses this by identifying recurring substructures (motifs) across spectral datasets without relying on prior compound identification"
- [readme] providing automated annotation of discovered motifs. This tool significantly enhances the capabilities described in the original MS2LDA paper (2016), offering users an integrated workflow: "providing automated annotation of discovered motifs. This tool significantly enhances the capabilities described in the original MS2LDA paper (2016)"
- [readme] Before running MS2LDA you must download the Spec2Vec model, embeddings, and library DB (See the Zenodo repository): "Before running MS2LDA you must download the Spec2Vec model, embeddings, and library DB (See the Zenodo repository)"
