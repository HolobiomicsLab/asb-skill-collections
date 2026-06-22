---
name: metabolite-similarity-scoring
description: Use when you have an unknown compound's mass spectrum (m/z peaks and intensities) in .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0157
  tools:
  - DeepMASS2
derived_from:
- doi: 10.1101/2024.05.30.596727v2
  title: DeepMASS
evidence_spans:
- DeepMASS2 is a cross-platform GUI software tool, which enables deep-learning based metabolite annotation
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_deepmass_cq
    doi: 10.1101/2024.05.30.596727v2
    title: DeepMASS
  dedup_kept_from: coll_deepmass_cq
schema_version: 0.2.0
---

# metabolite-similarity-scoring

## Summary

Score and rank candidate metabolites by computing semantic similarity between an unknown compound's mass spectrum and a reference database of known metabolite spectra using deep-learned mass spectral language encodings. This enables prediction of structurally related metabolites and assists in ranking molecular structure database candidates.

## When to use

You have an unknown compound's mass spectrum (m/z peaks and intensities) in .mgf or equivalent format with mandatory PRECURSOR_MZ and IONMODE tags, and you need to identify structurally related metabolites from a reference database to constrain chemical space and rank candidates for structure elucidation.

## When NOT to use

- Input mass spectrum lacks mandatory PRECURSOR_MZ or IONMODE metadata tags — DeepMASS2 requires these for filtering and model selection.
- Ion mode is unknown or mixed — the tool requires a single consistent polarity to select the correct deep-learning model.
- Reference database is unavailable or incompatible — the pre-indexed pickle and binary index files must be downloaded and placed in the correct data and model directories.

## Inputs

- Unknown compound mass spectrum (.mgf file with PRECURSOR_MZ and IONMODE tags)
- Mass spectral peak list (m/z and intensity pairs)
- Ion mode (positive or negative)
- Precursor m/z value
- Optional: molecular formula

## Outputs

- Ranked list of candidate metabolites with semantic similarity scores
- CSV file mapping unknown spectrum to top-ranked structurally related metabolites
- Semantic similarity scores (cosine similarity metric)

## How to apply

First, validate input mass spectral data contains required metadata: precursor m/z value and ion mode polarity (positive or negative). Load the unknown spectrum and encode it into a semantic vector representation using the DeepMASS2 deep-learning model (Ms2Vec) trained on the appropriate ion mode. Compute cosine similarity or equivalent distance metric between the encoded spectrum and a pre-indexed reference database of known metabolite spectra (references_spectrums_positive.pickle or references_spectrums_negative.pickle). Rank candidate metabolites by similarity score in descending order. Optionally, constrain the chemical space by filtering candidates using molecular formula if available, which significantly improves ranking accuracy. Return the top-ranked structurally related metabolites with their corresponding similarity scores.

## Related tools

- **DeepMASS2** (Deep-learning encoder and semantic similarity search engine; encodes mass spectra into learned language vectors and computes cosine similarity against indexed reference spectra) — https://github.com/hcji/DeepMASS2_GUI

## Evaluation signals

- Returned similarity scores range from 0 to 1 (or appropriate metric bounds) and are sorted in descending order.
- Top-ranked candidates match known structurally related metabolites when available (manual validation against literature or ground truth).
- Output CSV file is successfully generated with COMPOUND_NAME and contains ranked metabolite identifiers and similarity scores.
- Semantic similarity scores are reproducible across multiple runs with identical inputs and model weights.
- Filtering by molecular formula (when provided) reduces candidate list while preserving correct metabolite in top ranks, indicating chemical space constraint is effective.

## Limitations

- Accuracy depends on quality and completeness of the reference database; structurally related metabolites outside the database cannot be retrieved.
- Deep-learning model performance is ion-mode specific; incorrect IONMODE assignment will use wrong model and reference spectra, degrading results.
- Similarity scoring is agnostic to retention time or other orthogonal metadata; mass spectral language alone may not distinguish isomers or closely related structures.
- The tool requires manual download and placement of large model and reference files (≥1 GB); missing or corrupted files will cause runtime failures.
- No changelog documented; version history is sparse (only v0.99.0 and v0.99.1 released), limiting visibility into bug fixes and feature improvements.

## Evidence

- [other] Encode → Compute → Rank workflow: "1. Load the unknown compound's mass spectral data (m/z peaks and intensities). 2. Encode the mass spectrum into a semantic representation using the DeepMASS2 deep-learning model trained on mass"
- [intro] Purpose of structurally related metabolites: "By considering the chemical space, these structurally related metabolites provide valuable information about the potential location of the unknown metabolites and assist in ranking candidates"
- [readme] Required metadata tags: "Precursor m/z - **Required** This tag specifies the precursor ion mass-to-charge ratio (m/z). This is a fundamental requirement for the search engine to filter candidates within the structural"
- [readme] Ion mode requirement: "Ion Mode - **Required** This specifies the polarity of the data, ensuring DeepMASS2 utilizes the correct deep-learning model (Positive vs. Negative) and reference libraries."
- [readme] Optional molecular formula constraint: "Adding the molecular formula helps the semantic similarity engine constrain potential chemical space, significantly improving the ranking accuracy of structurally related metabolites."
- [readme] Reference data requirements: "put the following files into data folder: DeepMassStructureDB-v1.1.csv, references_index_negative_spec2vec.bin, references_index_positive_spec2vec.bin, references_spectrums_negative.pickle,"
