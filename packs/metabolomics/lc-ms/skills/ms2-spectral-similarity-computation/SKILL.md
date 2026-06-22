---
name: ms2-spectral-similarity-computation
description: Use when you have two or more LC-MS/MS datasets (in mzML, mzXML, or MGF format) and need to quantify their overall spectral content similarity—typical scenarios include data quality control, species identification, molecular phylogenetics, or proteome comparison across samples, cell lines, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3365
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - compareMS2
  - DISMS2
  techniques:
  - LC-MS
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

# ms2-spectral-similarity-computation

## Summary

Compute global similarity between tandem mass spectrometry datasets by extracting spectral features, normalizing intensities, calculating pairwise cosine similarities, and aggregating them into a single similarity metric. This enables direct comparison of LC-MS/MS datasets without relying on sequence databases or spectral libraries.

## When to use

Apply this skill when you have two or more LC-MS/MS datasets (in mzML, mzXML, or MGF format) and need to quantify their overall spectral content similarity—typical scenarios include data quality control, species identification, molecular phylogenetics, or proteome comparison across samples, cell lines, or tissues where you want to measure similarity independently of protein identification.

## When NOT to use

- Input datasets are already assigned to known peptide sequences or proteins—use spectral library matching (e.g., BiblioSpec, SpectraST) or database search tools (Mascot, Comet, Sage) instead.
- You need de novo peptide sequencing from spectra—this skill compares spectral patterns, not sequences; use de novo sequencing tools (LUTEFISK, PepNovo) for sequence inference.
- Input data is single-spectrum or requires comparison to external reference libraries—this skill is designed for dataset-to-dataset comparison, not spectrum-to-library matching.

## Inputs

- tandem mass spectrometry dataset 1 (mzML, mzXML, or MGF format)
- tandem mass spectrometry dataset 2 (mzML, mzXML, or MGF format)

## Outputs

- global spectral similarity score (numeric value between 0 and 1)
- pairwise similarity distribution (histogram or summary statistics)
- number of high-scoring spectrum pairs (count)
- results file (text or tabular format)

## How to apply

Load the two tandem MS datasets and parse each spectrum to extract precursor mass, retention time, and fragment ion peaks. Normalize fragment ion intensities within each spectrum independently to account for instrument and sample variation. Compute pairwise cosine similarity between all spectra across the two datasets using normalized m/z and intensity vectors. Aggregate pairwise similarities using a global metric (mean, median, or percentile-based score) to produce a single global spectral similarity value between 0 (no shared spectra) and 1 (identical spectral content). Output the global similarity score alongside supporting statistics such as the distribution of pairwise similarities and the number of high-scoring spectrum pairs to enable interpretation.

## Related tools

- **compareMS2** (primary tool for calculating global similarity and generating phylogenetic trees, heatmaps, and species identification charts from tandem MS datasets) — https://github.com/524D/compareMS2
- **DISMS2** (alternative direct comparison tool for tandem MS spectra)

## Evaluation signals

- Global similarity score is numeric, bounded between 0 and 1, and symmetric (distance A→B equals B→A).
- Pairwise similarity distribution is non-empty and contains only values in [0, 1]; median/mean aggregates are consistent with reported global score.
- High-scoring pairs count is ≤ total possible pairwise comparisons (n₁ × n₂ for datasets of size n₁ and n₂).
- Output file is present and contains required statistics (global score, distribution summary, pair count); no NaN or infinite values.
- When comparing identical or highly similar datasets, global similarity approaches 1; when comparing unrelated datasets, similarity approaches 0.

## Limitations

- Similarity computation depends on spectral overlap; datasets with completely non-overlapping m/z or precursor mass ranges will yield near-zero similarity regardless of spectral quality.
- Normalization of fragment intensities within each spectrum is independent, so datasets acquired on different instruments with different dynamic ranges or noise floors may not be directly comparable.
- Aggregation method (mean, median, percentile) significantly affects the final global score; the article does not specify which is default or recommend best-practice selection for specific applications.
- The tool does not account for biological redundancy (multiple spectra from the same peptide or protein), so high abundance proteins can dominate the similarity metric.
- No changelog present in the repository—version tracking and reproducibility information for prior releases is absent, limiting verification of results across tool versions.

## Evidence

- [other] Load two tandem mass spectrometry datasets (in a supported format such as mzML or mzXML). 2. Parse and extract precursor mass, retention time, and fragment ion peaks from each spectrum. 3. Normalize fragment ion intensities within each spectrum independently. 4. Compute pairwise cosine similarity between all spectra across the two datasets using normalized m/z and intensity vectors. 5. Aggregate pairwise similarities using a global similarity metric (e.g., mean, median, or percentile-based score) to produce a single global spectral similarity value.: "Load two tandem mass spectrometry datasets (in a supported format such as mzML or mzXML). 2. Parse and extract precursor mass, retention time, and fragment ion peaks from each spectrum. 3. Normalize"
- [readme] compareMS2 is a tool for direct comparison of tandem mass spectrometry datasets, typically from liquid chromatography-tandem mass spectrometry (LC-MS/MS), defining similarity as a function of shared (similar) spectra and distance as the inverse of this similarity.: "compareMS2 is a tool for direct comparison of tandem mass spectrometry datasets, typically from liquid chromatography-tandem mass spectrometry (LC-MS/MS), defining similarity as a function of shared"
- [readme] Data with identical spectral content thus have similarity 1 and distance 0. The similarity of datasets with no similar spectra tend to 0 (distance +∞) as the size of the sets go to infinity.: "Data with identical spectral content thus have similarity 1 and distance 0. The similarity of datasets with no similar spectra tend to 0"
- [readme] compareMS2 can also be used to quantify the similarity of proteomes from different cell lines or tissues from the same species, before and independently of any protein identification by database or spectral library search.: "compareMS2 can also be used to quantify the similarity of proteomes from different cell lines or tissues from the same species, before and independently of any protein identification"
- [discussion] No changelog found — reproducibility and version tracking information is absent: "No changelog found — reproducibility and version tracking information is absent"
