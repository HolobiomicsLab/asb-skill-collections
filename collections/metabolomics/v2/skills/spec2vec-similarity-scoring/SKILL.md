---
name: spec2vec-similarity-scoring
description: Use when after discovering Mass2Motifs via LDA on preprocessed MS/MS spectra, use this skill to assign putative substructure annotations by matching each motif's fragmentation pattern against a pre-indexed spectral library using learned spectral embeddings.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Spec2Vec
  - Python
  - MS2LDA
  - MAG (Mass2Motif Annotation Guidance)
  - MS2LDAViz
  techniques:
  - LC-MS
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spec2vec-similarity-scoring

## Summary

Compute Spec2Vec cosine similarity scores between Mass2Motifs and a spectral library to retrieve top-ranked annotated spectra for each motif. This enables automated annotation of discovered fragmentation motifs by identifying the most similar known spectral references.

## When to use

After discovering Mass2Motifs via LDA on preprocessed MS/MS spectra, use this skill to assign putative substructure annotations by matching each motif's fragmentation pattern against a pre-indexed spectral library using learned spectral embeddings. Apply when you have a trained motifset JSON file and need to generate per-motif annotation records with similarity confidence metrics for visualization and export.

## When NOT to use

- Input motifset has not been validated or contains incomplete Mass2Motif definitions
- Spectral library index is incompatible with the loaded Spec2Vec model version or was built from a different training corpus
- Cosine similarity threshold has not been calibrated for your spectral domain or quality requirements — using arbitrary thresholds risks over-annotation or under-annotation

## Inputs

- Trained motifset JSON file (motifset_optimized.json) containing discovered Mass2Motifs
- Pre-trained Spec2Vec model and embeddings (from Zenodo zenodo.org/records/15688609)
- Spec2Vec-indexed spectral library database

## Outputs

- Per-motif annotation records in JSON format (compatible with MS2LDAViz)
- Motif-to-substructure label mappings with cosine similarity scores
- Confidence metrics for each annotation

## How to apply

Load the pre-trained Spec2Vec model and embeddings from the designated Zenodo repository (zenodo.org/records/15688609), then load the trained motifset JSON file containing all discovered Mass2Motifs. For each Mass2Motif, compute cosine similarity scores between the motif's embedded representation and all entries in the Spec2Vec-indexed spectral library. Retrieve the top-ranked annotated spectra or reference entries for each motif based on a cosine similarity threshold (implementation determines sensitivity/specificity tradeoff). Generate annotation records that map each motif identifier to suggested labels, similarity scores, and confidence metrics, then export the output in JSON format compatible with MS2LDAViz for downstream exploration and curation.

## Related tools

- **Spec2Vec** (Computes learned spectral embeddings and cosine similarity scores between Mass2Motifs and spectral library entries)
- **MAG (Mass2Motif Annotation Guidance)** (Orchestrates automated annotation workflow integrating Spec2Vec similarity lookup with annotation record generation) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDA** (Provides the LDA-based motif discovery framework whose outputs (motifset JSON) serve as input to Spec2Vec annotation) — https://github.com/vdhooftcompmet/MS2LDA
- **MS2LDAViz** (Consumes the JSON annotation output and enables interactive visualization and export of per-motif annotation records) — https://github.com/vdhooftcompmet/MS2LDA

## Evaluation signals

- Annotation JSON output conforms to MS2LDAViz schema and can be loaded without parsing errors
- All discovered Mass2Motifs receive at least one annotation record with a non-null similarity score
- Cosine similarity scores fall within the [0, 1] range and show expected distribution (mean and variance consistent with library diversity and motif specificity)
- Top-ranked annotations are biologically plausible given the motif's fragmentation composition (neutral losses and fragments align with known substructure losses)
- Similarity score ranking is monotonically decreasing; top candidate has higher score than second candidate

## Limitations

- Annotation quality depends critically on the quality and completeness of the spectral library index and the Spec2Vec model's training corpus; poorly-trained or biased embeddings will produce spurious high-similarity matches
- Cosine similarity alone does not capture semantic or chemical validity; a high score does not guarantee the annotation is correct or that the motif truly represents the proposed substructure
- Motifs with fragmentation patterns absent or underrepresented in the training library will receive low-confidence annotations or no match above threshold
- The skill does not perform de novo structure elucidation; it relies on the existence of reference spectra in the indexed library

## Evidence

- [methods] Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec: "Automated Mass2Motif Annotation Guidance (MAG) with Spec2Vec"
- [other] For each Mass2Motif, compute Spec2Vec similarity scores against the Spec2Vec-indexed spectral library using the loaded model. Retrieve the top-ranked annotated spectra or reference entries for each motif based on cosine similarity threshold.: "For each Mass2Motif, compute Spec2Vec similarity scores against the Spec2Vec-indexed spectral library using the loaded model. 4. Retrieve the top-ranked annotated spectra or reference entries for"
- [other] Download and load the pre-trained Spec2Vec model and embeddings from the Zenodo repository (zenodo.org/records/15688609). Load the trained motifset JSON file (motifset_optimized.json) containing all discovered Mass2Motifs.: "Download and load the pre-trained Spec2Vec model and embeddings from the Zenodo repository (zenodo.org/records/15688609). 2. Load the trained motifset JSON file (motifset_optimized.json) containing"
- [other] Generate annotation records mapping each motif identifier to suggested labels, similarity scores, and confidence metrics. Export the per-motif annotation output in JSON format compatible with MS2LDAViz.: "Generate annotation records mapping each motif identifier to suggested labels, similarity scores, and confidence metrics. 6. Export the per-motif annotation output in JSON format compatible with"
- [other] MS2LDA provides automated annotation of Mass2Motifs using MAG with Spec2Vec, which loads a trained motifset together with the Spec2Vec model from a Zenodo repository to output per-motif annotation records.: "MS2LDA provides automated annotation of Mass2Motifs using MAG with Spec2Vec, which loads a trained motifset together with the Spec2Vec model from a Zenodo repository to output per-motif annotation"
