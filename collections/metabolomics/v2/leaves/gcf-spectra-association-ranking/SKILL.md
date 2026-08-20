---
name: gcf-spectra-association-ranking
description: Use when when you have integrated genomic data (GCFs from AntiSMASH via
  BigScape clustering) and metabolomic data (spectra and molecular families from GNPS
  molecular networking) and need to identify and rank which secondary metabolites
  detected in spectra are likely produced by which biosynthetic.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0204
  tools:
  - nplinker
  - Python
  - AntiSMASH
  - BigScape
  - GNPS
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1186/s40168-022-01444-3
  title: NPClassScore
evidence_spans:
- It provides the tools [`GNPSDownloader`][nplinker.metabolomics.gnps.GNPSDownloader]
  and [`GNPSExtractor`][nplinker.metabolomics.gnps.GNPSExtractor]
- '[![github repo badge](https://img.shields.io/badge/github-nplinker-000.svg?color=blue)](https://github.com/NPLinker/nplinker)'
- Python version ≥3.11
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_npclassscore_cq
    doi: 10.1186/s40168-022-01444-3
    title: NPClassScore
  dedup_kept_from: coll_npclassscore_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-022-01444-3
  all_source_dois:
  - 10.1186/s40168-022-01444-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# gcf-spectra-association-ranking

## Summary

Compute ranked associations between Genomic Cluster Families (GCFs) and molecular spectra using the Metcalf scoring algorithm, producing a weighted LinkGraph artifact that represents putative biosynthetic-metabolomic links with quantified confidence scores.

## When to use

When you have integrated genomic data (GCFs from AntiSMASH via BigScape clustering) and metabolomic data (spectra and molecular families from GNPS molecular networking) and need to identify and rank which secondary metabolites detected in spectra are likely produced by which biosynthetic gene clusters, quantifying the strength of each putative association.

## When NOT to use

- Input genomic or metabolomic data has not been pre-processed through AntiSMASH, BigScape, and GNPS respectively—Metcalf scoring assumes upstream clustering and networking are complete.
- You require probabilistic uncertainty quantification or Bayesian credible intervals around link scores—MetcalfScoring produces point estimates only.
- Spectral or GCF data is incomplete, misaligned, or missing key metadata (e.g., molecular weights, fragmentation patterns, or cluster boundary annotations).

## Inputs

- GCFs (Genomic Cluster Families) from AntiSMASH/BigScape clustering
- Molecular spectra from mass spectrometry
- Molecular families from GNPS molecular networking
- Loaded NPLinker Dataset object

## Outputs

- LinkGraph object containing weighted directed edges between GCFs and spectral entities
- Link score annotations (numeric weights on edges)
- Ranked associations (implicit via edge scores)

## How to apply

Load pre-prepared genomic and metabolomic datasets (GCFs, spectra, and molecular families) using NPLinker's DatasetLoader. Initialize a MetcalfScoring instance with the loaded entities. Execute the scoring computation via NPLinker.get_links(), which applies the Metcalf algorithm to compute pairwise links between GCFs and spectral entities. The algorithm returns a LinkGraph object—a directed weighted graph where each edge represents a GCF-to-spectrum association labeled with a numeric link score. Validate the LinkGraph by confirming that links are present and scores fall within expected ranges (typically [0, 1] or similar normalized interval). The ranking is implicit in the link scores; higher scores indicate stronger predicted associations.

## Related tools

- **nplinker** (Core framework providing DatasetLoader, MetcalfScoring class, and LinkGraph data structure for computing and managing GCF-spectra associations) — https://github.com/NPLinker/nplinker
- **AntiSMASH** (Upstream tool for detecting and annotating biosynthetic gene clusters (input to BigScape clustering))
- **BigScape** (Clustering tool that groups AntiSMASH BGCs into GCFs, which serve as genomic entities for Metcalf scoring)
- **GNPS** (Metabolomic networking platform providing molecular families and spectra that are scored against GCFs) — https://gnps.ucsd.edu
- **Python** (Programming environment for executing NPLinker DatasetLoader and MetcalfScoring methods)

## Examples

```
from nplinker import NPLinker; npl = NPLinker.load(config_file='config.yaml'); npl.load_data(); links = npl.get_links(scoring_method='metcalf'); print(links.edges())
```

## Evaluation signals

- LinkGraph is non-empty: at least one GCF-to-spectrum link is present in the output.
- Link scores are numeric and within expected normalized range (e.g., [0.0, 1.0] or equivalent quantile).
- All GCF and spectrum identifiers in LinkGraph edges correspond to entities in the input Dataset.
- LinkGraph is a directed graph with GCFs and spectral entities as node sets and weighted edges representing associations.
- Rerunning the same computation with identical inputs produces identical link scores (deterministic output).

## Limitations

- MetcalfScoring requires upstream AntiSMASH, BigScape, and GNPS preprocessing; garbage input data produces garbage output.
- Link scores are deterministic point estimates; no confidence intervals or uncertainty bounds are returned.
- The Metcalf algorithm's specificity and sensitivity depend on the quality and completeness of the input genomic and metabolomic datasets; sparse or noisy data may yield false positives or false negatives.
- No discussion section or methodological limitations are documented in the provided source material; algorithm rationale and failure modes are not explicitly described.

## Evidence

- [other] The MetcalfScoring computation accepts GCFs and molecular families/spectra as inputs and computes links between them, returning a LinkGraph artifact that represents the scoring results.: "The MetcalfScoring computation accepts GCFs and molecular families/spectra as inputs and computes links between them, returning a LinkGraph artifact that represents the scoring results."
- [other] Load pre-prepared datasets containing GCFs (from AntiSMASH via BigScape clustering), spectra, and molecular families (from GNPS molecular networking) using NPLinker's DatasetLoader.: "Load pre-prepared datasets containing GCFs (from AntiSMASH via BigScape clustering), spectra, and molecular families (from GNPS molecular networking)"
- [other] Execute the scoring computation via the NPLinker.get_links() method, which applies the Metcalf scoring algorithm to compute pairwise links between GCFs and spectral entities.: "Execute the scoring computation via the NPLinker.get_links() method, which applies the Metcalf scoring algorithm to compute pairwise links between GCFs and spectral entities."
- [other] Return a LinkGraph object containing the computed links as a directed weighted graph with link scores and metadata.: "Return a LinkGraph object containing the computed links as a directed weighted graph with link scores and metadata."
- [other] Validate the LinkGraph by checking that links are present and scores are in expected range.: "Validate the LinkGraph by checking that links are present and scores are in expected range."
- [readme] NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data.: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data."
