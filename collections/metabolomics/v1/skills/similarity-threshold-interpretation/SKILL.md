---
name: similarity-threshold-interpretation
description: Use when when you have computed Spec2Vec similarity scores (typically cosine similarity in [0, 1] range) between discovered Mass2Motifs and a spectral library, and need to decide which matches are sufficiently confident to include in per-motif annotation output.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0154
  tools:
  - Python
  - MS2LDA
  - Spec2Vec
  - MAG (Mass2Motif Annotation Guidance)
  - MS2LDAViz
  - MotifDB
derived_from:
- doi: 10.1093/bioinformatics/btx582
  title: ms2lda
evidence_spans:
- Configure the Python environment (set PYTHONPATH, activate conda, etc.)
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda
    doi: 10.1093/bioinformatics/btx582
    title: ms2lda
  dedup_kept_from: coll_ms2lda
schema_version: 0.2.0
---

# similarity-threshold-interpretation

## Summary

Interpret and apply cosine similarity thresholds to rank and filter Spec2Vec-annotated spectral matches, converting continuous similarity scores into actionable confidence-ranked annotation records for Mass2Motifs. This skill bridges continuous metric output to discrete annotation decisions in the context of automated substructure discovery.

## When to use

When you have computed Spec2Vec similarity scores (typically cosine similarity in [0, 1] range) between discovered Mass2Motifs and a spectral library, and need to decide which matches are sufficiently confident to include in per-motif annotation output. Apply this skill if your downstream visualization (MS2LDAViz) or downstream structural inference requires ranked, filtered annotation records rather than raw similarity matrices.

## When NOT to use

- If you have not yet computed Spec2Vec embeddings or similarity scores—apply Spec2Vec embedding and cosine similarity computation first.
- If your motif discovery step has not yet completed (LDA modeling phase); annotation is a downstream post-processing step after Mass2Motifs are learned.
- If you are working with unannotated or non-indexed spectral libraries where Spec2Vec reference embeddings do not exist; MAG requires pre-computed Spec2Vec embeddings.

## Inputs

- trained motifset JSON file (motifset_optimized.json) containing discovered Mass2Motifs
- pre-trained Spec2Vec model and embeddings (from Zenodo repository zenodo.org/records/15688609)
- Spec2Vec-indexed spectral library (MotifDB or equivalent reference database)
- list of Mass2Motif identifiers to annotate

## Outputs

- per-motif annotation records in JSON format (motif ID, suggested labels, similarity scores, confidence metrics)
- ranked list of top-matched reference spectra or annotations per motif
- JSON output compatible with MS2LDAViz visualization application

## How to apply

Load the trained motifset JSON and Spec2Vec model embeddings from the Zenodo repository. For each Mass2Motif, compute Spec2Vec cosine similarity scores against all entries in the indexed spectral library using the loaded model. Apply a similarity threshold (the article does not specify an exact cutoff value, but the workflow indicates a threshold parameter controls retrieval) to select top-ranked annotated spectra or reference entries. For matches above the threshold, generate annotation records that map each motif identifier to suggested labels, similarity scores, and confidence metrics. Export these records in JSON format compatible with MS2LDAViz. The threshold acts as a precision–recall tradeoff: higher thresholds reduce false positives but may miss valid annotations; lower thresholds increase sensitivity but risk spurious matches.

## Related tools

- **Spec2Vec** (computes cosine similarity scores between Mass2Motifs and spectral library entries; loads pre-trained embeddings to enable threshold-based ranking) — https://zenodo.org/records/15688609
- **MAG (Mass2Motif Annotation Guidance)** (orchestrates the automated annotation workflow that applies similarity thresholds to generate per-motif annotation records) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDAViz** (consumes JSON annotation records (with similarity scores and confidence metrics) to visualize and explore threshold-filtered motif annotations) — https://github.com/vdhooftcompmet/MS2LDA
- **MotifDB** (indexed reference database against which Spec2Vec similarities are computed; threshold selects which MotifDB entries become motif annotations)

## Evaluation signals

- Verify that all returned annotation records contain numeric similarity scores in [0, 1] range and that scores are monotonically ranked (highest first) for each motif.
- Check that the count of returned annotations per motif varies inversely with threshold stringency: higher threshold → fewer matches per motif.
- Confirm JSON output schema matches MS2LDAViz compatibility requirements: each annotation record includes motif_id, label/reference, similarity_score, and confidence metric fields.
- Cross-validate a sample of threshold-filtered matches by manual inspection: do top-ranked reference spectra visually/structurally resemble the discovered motif fragmentation patterns?
- Ensure no duplicate or conflicting annotations appear in the output (one reference entry per unique motif–label pair).

## Limitations

- The optimal similarity threshold is not specified in the documentation; practitioners must tune it empirically or use domain knowledge, and threshold choice directly impacts annotation precision and recall.
- Spec2Vec similarity is computed against a fixed, pre-indexed spectral library; annotations cannot reference spectra or substructures outside that library, limiting discovery to known chemical space.
- High-throughput similarity computation over large motifsets and libraries may be computationally expensive; performance scales with library size and motif count.
- Confidence metrics depend on the quality and coverage of the underlying Spec2Vec model and reference library; poor embeddings or incomplete library indexing will produce low-confidence or missing annotations.

## Evidence

- [other] Retrieve the top-ranked annotated spectra or reference entries for each motif based on cosine similarity threshold.: "Retrieve the top-ranked annotated spectra or reference entries for each motif based on cosine similarity threshold."
- [other] Generate annotation records mapping each motif identifier to suggested labels, similarity scores, and confidence metrics.: "Generate annotation records mapping each motif identifier to suggested labels, similarity scores, and confidence metrics."
- [other] For each Mass2Motif, compute Spec2Vec similarity scores against the Spec2Vec-indexed spectral library using the loaded model.: "For each Mass2Motif, compute Spec2Vec similarity scores against the Spec2Vec-indexed spectral library using the loaded model."
- [readme] MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework that brings the concept of topic modeling to the world of tandem mass spectrometry: "MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework that brings the concept of topic modeling to the world of tandem mass spectrometry"
- [methods] Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec: "Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec"
