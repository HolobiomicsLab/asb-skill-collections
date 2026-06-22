---
name: spectral-library-matching-and-ranking
description: Use when when you have discovered Mass2Motifs from MS2LDA topic modeling and need to automatically annotate them by finding the most structurally similar known spectra in a reference library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - MS2LDA
  - Spec2Vec
  - MAG (Mass2Motif Annotation Guidance)
  - MotifDB
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- Configure the Python environment (set PYTHONPATH, activate conda, etc.)
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1073/pnas.1608041113
  all_source_dois:
  - 10.1073/pnas.1608041113
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-library-matching-and-ranking

## Summary

This skill applies Spec2Vec embeddings to compute cosine similarity between Mass2Motifs and a spectral library, retrieving and ranking top-matched annotated spectra or reference entries to generate per-motif annotation records with confidence metrics.

## When to use

When you have discovered Mass2Motifs from MS2LDA topic modeling and need to automatically annotate them by finding the most structurally similar known spectra in a reference library. Use this skill when manual annotation is infeasible at scale and you want reproducible, quantified similarity-based substructure suggestions.

## When NOT to use

- The motifset has not yet been trained or does not exist in JSON format — first complete MS2LDA LDA modeling.
- You are working with private, unpublished spectra not represented in the Spec2Vec-indexed library — library coverage bias will degrade annotation quality.
- You require manual expert curation rather than automated ranking — use this skill to accelerate triage, not to replace human validation.

## Inputs

- trained motifset JSON file (motifset_optimized.json)
- pre-trained Spec2Vec model from Zenodo
- Spec2Vec embeddings from Zenodo
- Spec2Vec-indexed spectral library database

## Outputs

- per-motif annotation records in JSON format
- motif-to-label mappings with similarity scores
- confidence metrics per annotation
- MS2LDAViz-compatible annotation output

## How to apply

Load the pre-trained Spec2Vec model and embeddings from the designated Zenodo repository (zenodo.org/records/15688609), then load the trained motifset JSON file (motifset_optimized.json) containing all discovered Mass2Motifs. For each Mass2Motif, compute Spec2Vec similarity scores against the Spec2Vec-indexed spectral library using the loaded model. Retrieve the top-ranked annotated spectra or reference entries for each motif based on a cosine similarity threshold. Generate annotation records mapping each motif identifier to suggested labels, similarity scores, and confidence metrics. Export the per-motif annotation output in JSON format compatible with MS2LDAViz for downstream visualization and validation.

## Related tools

- **Spec2Vec** (computes cosine similarity scores between Mass2Motifs and reference spectra embeddings)
- **MAG (Mass2Motif Annotation Guidance)** (orchestrates automated annotation of Mass2Motifs using Spec2Vec similarity ranking) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA** (generates the trained motifset that serves as input to this annotation skill) — https://github.com/vdhooftcompmet/MS2LDA
- **MotifDB** (searchable database of reference motifs and annotations used for lookup and comparison)
- **Python** (host language for loading models, computing similarities, and exporting JSON annotations)

## Evaluation signals

- Verify that output JSON contains all motif IDs from the input motifset with no missing records.
- Check that each annotation record includes a similarity score field with numeric values in the range [0, 1] (cosine similarity bounds).
- Confirm that top-ranked matches correspond to known substructures consistent with typical fragmentation patterns for the compound class.
- Validate that JSON output conforms to MS2LDAViz schema and loads without parsing errors in the visualization interface.
- Cross-reference a sample of high-confidence matches (e.g., similarity > 0.8) against the MotifDB or literature to assess biological plausibility.

## Limitations

- Annotation quality depends entirely on the coverage and accuracy of the pre-trained Spec2Vec model and indexed library — novel substructures absent from the training set will receive poor or incorrect matches.
- Cosine similarity thresholds are not automatically optimized and must be tuned empirically; no principled default is stated in the article.
- The skill assumes the motifset JSON structure and field names match the expected format; incompatible or corrupted input files will cause silent failures or malformed output.

## Evidence

- [other] For each Mass2Motif, compute Spec2Vec similarity scores against the Spec2Vec-indexed spectral library using the loaded model.: "For each Mass2Motif, compute Spec2Vec similarity scores against the Spec2Vec-indexed spectral library using the loaded model."
- [other] Download and load the pre-trained Spec2Vec model and embeddings from the Zenodo repository (zenodo.org/records/15688609).: "Download and load the pre-trained Spec2Vec model and embeddings from the Zenodo repository (zenodo.org/records/15688609)."
- [other] Load the trained motifset JSON file (motifset_optimized.json) containing all discovered Mass2Motifs.: "Load the trained motifset JSON file (motifset_optimized.json) containing all discovered Mass2Motifs."
- [other] Retrieve the top-ranked annotated spectra or reference entries for each motif based on cosine similarity threshold.: "Retrieve the top-ranked annotated spectra or reference entries for each motif based on cosine similarity threshold."
- [other] Generate annotation records mapping each motif identifier to suggested labels, similarity scores, and confidence metrics.: "Generate annotation records mapping each motif identifier to suggested labels, similarity scores, and confidence metrics."
- [methods] Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec: "Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec"
- [other] MS2LDA provides automated annotation of Mass2Motifs using MAG with Spec2Vec, which loads a trained motifset together with the Spec2Vec model from a Zenodo repository to output per-motif annotation records.: "MS2LDA provides automated annotation of Mass2Motifs using MAG with Spec2Vec, which loads a trained motifset together with the Spec2Vec model from a Zenodo repository to output per-motif annotation"
