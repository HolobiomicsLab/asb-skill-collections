---
name: mass2motif-annotation-mapping
description: Use when after LDA-based Mass2Motif discovery has generated a set of recurring fragmentation patterns (motifset_optimized.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - MAG (Mass2Motif Annotation Guidance)
  - Python
  - MS2LDA
  - Spec2Vec
  - MS2LDAViz
  - MotifDB
derived_from:
- doi: 10.1093/bioinformatics/btx582
  title: ms2lda
evidence_spans:
- Automated annotation of M2M using MAG
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

# mass2motif-annotation-mapping

## Summary

Automated annotation of discovered Mass2Motifs by mapping them to known substructures via Spec2Vec similarity scoring against a spectral library. This skill bridges unsupervised motif discovery with interpretable structural labels and confidence metrics.

## When to use

After LDA-based Mass2Motif discovery has generated a set of recurring fragmentation patterns (motifset_optimized.json), use this skill to assign biological or chemical meaning to each motif by computing Spec2Vec cosine similarities against indexed reference spectra and retrieving top-ranked annotated candidates above a similarity threshold.

## When NOT to use

- Input motifset has not yet been validated for stability and interpretability—run diagnostic checks (e.g., coherence, diversity) before annotation.
- No pre-trained Spec2Vec model or spectral library is available for your ionization mode, organism, or chemical class—annotation will be uninformative.
- Spectra in your reference library are poorly annotated or lack structural metadata—annotation confidence will be unreliable.

## Inputs

- motifset_optimized.json (trained Mass2Motifs with mass/loss fragments and occurrence probabilities)
- pre-trained Spec2Vec model (embeddings and weights from Zenodo repository)
- Spec2Vec-indexed spectral library database (reference spectra with known annotations)
- cosine similarity threshold parameter (task-dependent; typical range 0.6–0.9)

## Outputs

- per-motif annotation records (JSON format with motif_id, suggested_label, similarity_score, confidence_metric)
- MS2LDAViz-compatible annotation JSON (structured for web-based visualization)
- annotation summary statistics (e.g., % annotated motifs, mean/median similarity scores per motif)

## How to apply

Load the pre-trained Spec2Vec model and embeddings from Zenodo (zenodo.org/records/15688609) alongside the trained motifset JSON file containing all discovered Mass2Motifs. For each motif, compute Spec2Vec similarity scores against the Spec2Vec-indexed spectral library using cosine similarity as the distance metric. Retrieve the top-ranked annotated spectra or reference entries for each motif based on a cosine similarity threshold (exact threshold depends on specificity/sensitivity trade-off for your compound class). Generate per-motif annotation records mapping each motif identifier to suggested substructure labels, their similarity scores, and confidence metrics derived from ranking and score distribution. Export results in JSON format compatible with MS2LDAViz for downstream visualization and validation.

## Related tools

- **Spec2Vec** (Spectral similarity metric and embedding model used to compute cosine similarities between Mass2Motifs and reference spectra for annotation lookup) — https://zenodo.org/records/15688609
- **MAG (Mass2Motif Annotation Guidance)** (Orchestration framework that automates the Spec2Vec-based annotation lookup process to generate per-motif records) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA** (Parent workflow tool that performs LDA-based motif discovery prior to annotation; provides motifset input and defines integration standards) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDAViz** (Visualization application that renders per-motif annotation records interactively and enables manual curation and export) — https://github.com/vdhooftcompmet/MS2LDA
- **MotifDB** (Searchable motif database of known substructures and their reference spectra used as the annotation lookup target)
- **Python** (Execution environment for loading models, computing similarities, and serializing annotation records)

## Evaluation signals

- All motifs in the input motifset receive at least one annotation record (100% coverage or justified exclusion log).
- Similarity scores for annotated motifs fall within the specified threshold range and show expected distribution (e.g., mean > 0.7, no outlier cliffs).
- Top-ranked annotations for each motif are chemically or biologically plausible given the observed mass and neutral loss patterns in the motif.
- Output JSON validates against MS2LDAViz schema (required fields present, no missing motif_ids, valid numeric ranges for scores).
- Spot-check 10–20 high-confidence motif annotations by manual review of the corresponding reference spectra to confirm semantic correctness.

## Limitations

- Annotation quality depends entirely on coverage and quality of the indexed reference library—rare or unannotated compounds will not be matched.
- Cosine similarity threshold is a user-tunable parameter; no universal optimal value exists—domain knowledge and validation data are required to set it appropriately.
- Spec2Vec embeddings are trained on specific spectral datasets and ionization modes; transferability to novel compound classes or instruments is uncertain.
- Ambiguous motifs (high-confidence matches to multiple structurally distinct substructures) will be annotated with the top match only; full ranking is available in the output but not highlighted.

## Evidence

- [other] MS2LDA provides automated annotation of Mass2Motifs using MAG with Spec2Vec, which loads a trained motifset together with the Spec2Vec model from a Zenodo repository to output per-motif annotation records.: "MS2LDA provides automated annotation of Mass2Motifs using MAG with Spec2Vec, which loads a trained motifset together with the Spec2Vec model from a Zenodo repository to output per-motif annotation"
- [other] For each Mass2Motif, compute Spec2Vec similarity scores against the Spec2Vec-indexed spectral library using the loaded model.: "For each Mass2Motif, compute Spec2Vec similarity scores against the Spec2Vec-indexed spectral library using the loaded model."
- [other] Retrieve the top-ranked annotated spectra or reference entries for each motif based on cosine similarity threshold.: "Retrieve the top-ranked annotated spectra or reference entries for each motif based on cosine similarity threshold."
- [other] Generate annotation records mapping each motif identifier to suggested labels, similarity scores, and confidence metrics.: "Generate annotation records mapping each motif identifier to suggested labels, similarity scores, and confidence metrics."
- [other] Export the per-motif annotation output in JSON format compatible with MS2LDAViz.: "Export the per-motif annotation output in JSON format compatible with MS2LDAViz."
- [methods] Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec: "Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec"
- [readme] MS2LDA includes a web-based visualization application (MS2LDAViz) for exploring and analyzing results.: "MS2LDA includes a web-based visualization application (MS2LDAViz) for exploring and analyzing results."
