---
name: global-similarity-aggregation
description: Use when after computing pairwise cosine similarities between all spectra across two LC-MS/MS datasets when you need a single scalar summary of dataset-level resemblance rather than individual spectrum matches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - compareMS2
derived_from:
- doi: 10.1021/acs.jproteome.2c00457
  title: compareMS2 2.0
evidence_spans:
- compareMS2 calculates the global similarity between tandem mass spectrometry datasets
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_comparems2_2_0_cq
    doi: 10.1021/acs.jproteome.2c00457
    title: compareMS2 2.0
  dedup_kept_from: coll_comparems2_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00457
  all_source_dois:
  - 10.1021/acs.jproteome.2c00457
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Global Similarity Aggregation

## Summary

Aggregate pairwise spectral similarity scores across two tandem mass spectrometry datasets into a single global metric that quantifies overall dataset resemblance. This skill enables rapid, reference-independent comparison of LC-MS/MS proteomes for phylogenetics, quality control, and species identification.

## When to use

Apply this skill after computing pairwise cosine similarities between all spectra across two LC-MS/MS datasets when you need a single scalar summary of dataset-level resemblance rather than individual spectrum matches. Use it when comparing proteomes from different organisms, tissues, or experimental conditions and you want to avoid database or spectral library dependencies.

## When NOT to use

- When you require individual spectrum-to-spectrum matches or identifications rather than a dataset-level summary.
- When comparing a single spectrum to a library or database; use spectrum–library matching instead.
- When input spectra are not yet normalized or when retention time and m/z calibration are unreliable across datasets; normalize and validate first.

## Inputs

- two tandem mass spectrometry datasets in mzML or mzXML format
- precursor mass, retention time, and fragment ion peak data extracted and parsed from each spectrum
- normalized fragment ion intensity vectors (normalized independently per spectrum)
- pairwise cosine similarity matrix computed across all spectra between the two datasets

## Outputs

- global spectral similarity score (single scalar value)
- pairwise similarity distribution statistics (e.g., mean, median, standard deviation)
- count of high-scoring spectrum pairs (above a similarity threshold)
- results file containing global score and supporting statistics

## How to apply

After normalizing fragment ion intensities within each spectrum and computing pairwise cosine similarities using normalized m/z and intensity vectors across all spectra in two datasets, select an aggregation function—mean, median, or percentile-based score—to reduce the distribution of pairwise similarities to a single value. The choice of aggregation depends on robustness requirements: mean is simple but sensitive to outliers; median is more robust; percentile-based (e.g., 90th percentile) emphasizes high-confidence matches. Record supporting statistics alongside the global score, including the pairwise similarity distribution shape and count of high-scoring pairs (e.g., cosine > 0.7), to enable diagnostic interpretation and reproducibility.

## Related tools

- **compareMS2** (Implements pairwise spectral cosine similarity computation and global aggregation for LC-MS/MS dataset comparison) — https://github.com/524D/compareMS2

## Evaluation signals

- Global similarity score is a scalar in the valid range [0, 1] (or normalized equivalent) reflecting the proportion of similar spectra between datasets.
- Pairwise similarity distribution statistics are computed and reported; median and mean should be interpretable and differ as expected given the spectrum population.
- Count of high-scoring pairs (similarity above threshold) is positive when datasets share proteomes and near-zero when datasets are dissimilar; trend aligns with biological expectation.
- Results file contains all supporting statistics alongside global score; reproducibility is enabled by recording preprocessing parameters (normalization method, cosine threshold used for counting).
- When applied to replicate samples or identical datasets, global similarity approaches 1.0; distance (inverse) approaches 0.

## Limitations

- Aggregation choices (mean vs. median vs. percentile) can yield different global scores from the same pairwise distribution; method must be pre-specified and justified.
- Global similarity is sensitive to differences in spectral coverage and abundance (protein quantity), not just amino acid sequence; datasets with identical proteomes but different protein expression will have lower similarity than expected.
- No changelog or version tracking information is available in the compareMS2 repository, limiting reproducibility across software updates.
- Similarity is symmetric by default (distance from A to B equals distance from B to A); this assumes equal dataset size and quality, which may not hold for unbalanced comparisons.
- Threshold parameters for defining 'high-scoring pairs' (e.g., cosine > 0.7) are user-specified; results are sensitive to this choice and must be documented.

## Evidence

- [other] Aggregate pairwise similarities using a global similarity metric (e.g., mean, median, or percentile-based score) to produce a single global spectral similarity value.: "Aggregate pairwise similarities using a global similarity metric (e.g., mean, median, or percentile-based score) to produce a single global spectral similarity value."
- [other] Write the global similarity score and supporting statistics (e.g., pairwise similarity distribution, number of high-scoring pairs) to a results file.: "Write the global similarity score and supporting statistics (e.g., pairwise similarity distribution, number of high-scoring pairs) to a results file."
- [other] compareMS2 calculates the global similarity between tandem mass spectrometry datasets, taking two such datasets as input and producing a similarity score as output.: "compareMS2 calculates the global similarity between tandem mass spectrometry datasets, taking two such datasets as input and producing a similarity score as output."
- [readme] Data with identical spectral content thus have similarity 1 and distance 0. The similarity of datasets with no similar spectra tend to 0.: "Data with identical spectral content thus have similarity 1 and distance 0. The similarity of datasets with no similar spectra tend to 0."
- [readme] not only the amino acid sequences of the peptides affect the distance metric in compareMS2, but also the abundance (or coverage) of the proteins.: "not only the amino acid sequences of the peptides affect the distance metric in compareMS2, but also the abundance (or coverage) of the proteins."
