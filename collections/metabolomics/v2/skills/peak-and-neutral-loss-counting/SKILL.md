---
name: peak-and-neutral-loss-counting
description: Use when when you have matchms-processed MS2 spectra from multiple samples and need to create comparable sample-level signatures for cross-sample analysis, particularly when samples are chemodiverse, have poor feature overlap, or exhibit strong retention time shifts across LC methods or MS.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0625
  tools:
  - matchms
  - spec2vec
  - numpy
  - Python
  - MEMO
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra and converting them into documents.
- pip install numpy
- conda create --name memo python=3.8
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_memo_cq
    doi: 10.3389/fbinf.2022.842964
    title: memo
  dedup_kept_from: coll_memo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fbinf.2022.842964
  all_source_dois:
  - 10.3389/fbinf.2022.842964
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-and-neutral-loss-counting

## Summary

Counts occurrences of MS2 peaks and neutral losses (to precursor) within individual samples to generate sample-level MS2 fingerprints. This quantitative summarization enables retention-time-agnostic sample comparison and alignment in metabolomics workflows.

## When to use

When you have matchms-processed MS2 spectra from multiple samples and need to create comparable sample-level signatures for cross-sample analysis, particularly when samples are chemodiverse, have poor feature overlap, or exhibit strong retention time shifts across LC methods or MS technologies.

## When NOT to use

- Input spectra have not been preprocessed through matchms (data quality and metadata standardization cannot be assumed).
- Retention-time information is critical for your analysis; MEMO is explicitly RT-agnostic and discards RT.
- You require feature-by-sample matrices with exact m/z alignment; MEMO fingerprints are sample-level aggregate counts, not individual spectral features.

## Inputs

- Per-sample MS2 spectra (matchms Spectrum objects)
- Precursor m/z values for each spectrum
- spec2vec document representations

## Outputs

- Per-sample MS2 fingerprint vectors (occurrence counts)
- MemoMatrix: unified fingerprint alignment matrix (numpy array)

## How to apply

Load per-sample MS2 spectra processed through matchms and extract spec2vec document representations. For each sample, systematically count the frequency of each unique MS2 fragment peak m/z value and neutral loss mass (calculated relative to precursor m/z). Aggregate these counts into a fingerprint vector where each element represents the occurrence frequency of a specific m/z or loss. The counting is performed independently per sample before aggregation; no cross-sample normalization occurs at this stage. Fingerprints are then assembled into a unified matrix via numpy array operations to enable downstream alignment and filtering.

## Related tools

- **matchms** (Processes and standardizes MS2 spectra; provides metadata cleaning and peak filtering for input to fingerprinting) — https://github.com/matchms/matchms
- **spec2vec** (Generates spectral embeddings and document representations from MS2 fragmentation relationships for fingerprint construction) — https://github.com/iomega/spec2vec
- **numpy** (Aggregates per-sample fingerprint vectors into unified MemoMatrix alignment arrays)
- **MEMO** (Complete framework implementing peak/neutral-loss counting and sample vectorization for metabolomics) — https://github.com/mandelbrot-project/memo

## Evaluation signals

- Fingerprint vector length matches the total number of unique MS2 m/z values and neutral losses observed across all samples.
- All occurrence counts are non-negative integers; no negative or fractional counts are present.
- MemoMatrix dimensions are (n_samples, n_features) where n_features is constant across all rows, confirming feature alignment consistency.
- Sum of counts per sample correlates with the total number of MS2 spectra in that sample, validating exhaustive counting.
- Fingerprints from blank/control samples show predictably low or sparse counts compared to active samples before filtering.

## Limitations

- Fingerprints discard spectral intensity and fragmentation fragmentation pathway information; only presence/absence frequency is retained.
- MS2 peak clustering or tolerance-based grouping is not applied; each distinct m/z is counted separately, potentially inflating feature dimensionality in high-resolution instruments.
- Neutral loss calculation depends on accurate precursor m/z assignment; errors propagate into incorrect loss counts.
- Very small samples or samples with few MS2 spectra may produce sparse, uninformative fingerprints with high noise-to-signal ratio.

## Evidence

- [intro] MS2 fingerprints are generated by counting occurrences of MS2 peaks and neutral losses in each sample: "The occurence of MS2 peaks and neutral losses (to the precursor) in each sample is counted and used to generate an *MS2 fingerprint*"
- [intro] Fingerprints are aligned in a second stage to enable cross-sample comparison: "These fingerprints can in a second stage be aligned to compare different samples"
- [readme] MEMO is built on matchms and spec2vec for MS2 handling: "MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra"
- [other] Fingerprint aggregation uses numpy array operations to ensure consistent feature alignment: "Aggregate fingerprint vectors across all samples into a unified matrix using numpy array operations, ensuring consistent feature alignment"
- [readme] MEMO suits chemodiverse samples with poor feature overlap or strong RT shift: "MEMO suits particularly well to compare chemodiverse samples, ie with a poor features overlap, or to compare samples with a strong RT shift"
