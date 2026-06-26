---
name: reference-database-screening
description: Use when after a CNN model has generated predicted molecular embeddings
  from mass spectrometry data, use this skill to match those predictions against a
  curated reference database of known molecular embeddings.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Convolutional Neural Network (CNN)
  - ChemEmbed
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2025.02.07.637102v1
  title: ChemEmbed
evidence_spans:
- perform predictions using a trained Convolutional Neural Network (CNN) model
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemembed_cq
    doi: 10.1101/2025.02.07.637102v1
    title: ChemEmbed
  dedup_kept_from: coll_chemembed_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.02.07.637102v1
  all_source_dois:
  - 10.1101/2025.02.07.637102v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# reference-database-screening

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Screen predicted molecular embeddings against a reference database to identify and rank candidate molecules by similarity. This skill bridges CNN predictions and molecular identification by computing pairwise similarity scores and filtering high-confidence matches.

## When to use

After a CNN model has generated predicted molecular embeddings from mass spectrometry data, use this skill to match those predictions against a curated reference database of known molecular embeddings. Specifically, apply it when you need to convert abstract embeddings into a ranked list of candidate molecules with confidence scores for metabolite identification or compound annotation tasks.

## When NOT to use

- Query or reference embeddings are not from the same trained CNN model or are incompatible dimensionally
- Reference database is empty, unindexed, or embeddings are not pre-computed
- Input embeddings are already discrete molecular annotations rather than continuous vectors

## Inputs

- CNN-predicted embeddings for query molecules (vector format from trained model)
- Reference database embeddings (pre-computed vectors from reference molecules)
- Similarity threshold parameter (float, e.g., cosine similarity cutoff)
- Top N candidates parameter (integer, e.g., 5)

## Outputs

- Ranked candidate list with match scores and reference molecule identifiers
- Pairwise similarity score matrix (queries × reference database)
- Filtered candidate matches exceeding the similarity threshold

## How to apply

Load the CNN-predicted embeddings for query molecules and reference database embeddings from the trained model output. Compute pairwise similarity scores between query embeddings and all reference database embeddings using a distance metric such as cosine similarity or Euclidean distance. Rank reference molecules by similarity score in descending order for each query compound. Apply a similarity threshold to retain only high-confidence matches and filter candidate matches accordingly. Generate a ranked candidate list with match scores and reference molecule identifiers for each query compound, optionally including the top N candidates as configured.

## Related tools

- **Convolutional Neural Network (CNN)** (Generates predicted molecular embeddings from mass spectrometry spectra data that serve as query vectors for database screening)
- **ChemEmbed** (End-to-end framework that orchestrates data preprocessing, CNN prediction, and reference database screening for metabolite identification) — https://github.com/massspecdl/ChemEmbed

## Examples

```
python main.py --config config.yaml
# where config.yaml specifies reference_database, model_path, top_n_candidates: 5, and prediction_results output file
```

## Evaluation signals

- Similarity scores are within the valid range [0, 1] for cosine similarity or are non-negative for Euclidean distance
- Ranked candidate list is non-empty when similarity threshold is appropriate; empty results may indicate threshold is too stringent or embeddings are poorly calibrated
- Top-ranked candidate has the highest similarity score; scores decrease monotonically down the ranked list
- Number of returned candidates does not exceed the specified top_n_candidates parameter
- Retrieved reference molecules can be traced back to identifiers in the reference database pickle file or flat file

## Limitations

- Screening quality depends critically on the trained CNN model's embedding space; poor model calibration yields unreliable matches
- Reference database completeness and representation bias affect coverage; absent or underrepresented compound classes will yield no or low-quality matches
- Cosine similarity or Euclidean distance may not capture all relevant molecular features; Tanimoto similarity based on SMILES can complement embedding-based scoring if available
- Computational cost scales with reference database size; very large databases (millions of compounds) may require approximate nearest-neighbor methods or database indexing
- Threshold selection is empirically driven and dataset-dependent; no universal threshold guarantees optimal precision–recall trade-off across all compound classes

## Evidence

- [other] The framework is designed to match predictions from a trained CNN model against a reference database to identify potential candidate molecules for metabolite identification.: "match predictions from a trained CNN model against a reference database to identify potential candidate molecules"
- [other] Compute pairwise similarity scores between query embeddings and all reference database embeddings using a distance metric (e.g., cosine similarity or Euclidean distance).: "Compute pairwise similarity scores between query embeddings and all reference database embeddings using a distance metric (e.g., cosine similarity or Euclidean distance)"
- [other] Filter candidate matches by applying a similarity threshold to retain only high-confidence matches.: "Filter candidate matches by applying a similarity threshold to retain only high-confidence matches"
- [readme] Matches predicted embeddings with a reference database to find top candidate molecules based on cosine similarity.: "Matches predicted embeddings with a reference database to find top candidate molecules based on cosine similarity"
- [readme] top_n_candidates: Number of top candidate molecules to retrieve from the reference database.: "top_n_candidates: Number of top candidate molecules to retrieve from the reference database"
