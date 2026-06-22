---
name: link-scoring-metcalf-algorithm
description: Use when you have loaded GCFs (from AntiSMASH via BigScape clustering), GNPS spectra, and molecular families (from GNPS molecular networking), and need to compute pairwise scoring between genomic and metabolomic entities to identify putative gene cluster–metabolite associations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_0154
  tools:
  - nplinker
  - Python
  - conda
  - pip
  - BigScape
  - AntiSMASH
  - GNPS
derived_from:
- doi: 10.1186/s40168-022-01444-3
  title: NPClassScore
evidence_spans:
- It provides the tools [`GNPSDownloader`][nplinker.metabolomics.gnps.GNPSDownloader] and [`GNPSExtractor`][nplinker.metabolomics.gnps.GNPSExtractor]
- '[![github repo badge](https://img.shields.io/badge/github-nplinker-000.svg?color=blue)](https://github.com/NPLinker/nplinker)'
- Python version ≥3.11
- conda create -n npl-3.11 python=3.11
- pip install nplinker
- NPLinker can run BigScape automatically if the `bigscape` directory does not exist in the working directory.
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# link-scoring-metcalf-algorithm

## Summary

The Metcalf scoring method computes weighted links between Genomic Cluster Families (GCFs) and molecular families/spectra by integrating genomic and metabolomic data, producing a LinkGraph artifact with scored link tuples. This skill is essential for correlating biosynthetic gene clusters with their predicted metabolite products in natural product discovery workflows.

## When to use

Apply this skill when you have loaded GCFs (from AntiSMASH via BigScape clustering), GNPS spectra, and molecular families (from GNPS molecular networking), and need to compute pairwise scoring between genomic and metabolomic entities to identify putative gene cluster–metabolite associations.

## When NOT to use

- Input genomic or metabolomic data has not been preprocessed through AntiSMASH/BigScape or GNPS workflows respectively—Metcalf scoring depends on these standardized clustering and networking annotations.
- You require deterministic or rule-based linking without probabilistic scoring—Metcalf is a computational scoring method and produces weighted, not binary, associations.
- GCFs or spectral entities are incomplete or missing required metadata fields—scoring requires complete entity annotations from both domains.

## Inputs

- GCFs (Genomic Cluster Families) from AntiSMASH/BigScape clustering
- Spectra and molecular families from GNPS molecular networking
- NPLinker DatasetLoader-prepared genomic and metabolomic entities

## Outputs

- LinkGraph object containing directed weighted graph of GCF–spectrum/molecular family links
- Scored link tuples with metadata (accessible via link_graph.links)

## How to apply

Initialize a MetcalfScoring instance with pre-loaded genomic entities (GCFs) and metabolomic entities (spectra and molecular families). Execute the scoring computation via NPLinker's get_links() method, which applies the Metcalf algorithm to compute pairwise links between GCFs and spectral entities. The method returns a LinkGraph object containing directed weighted edges with numeric link scores and associated metadata. Validate the LinkGraph by confirming that links are present and scores fall within the expected range (typically 0–1 for normalized scoring). Export results by accessing the LinkGraph's links property to obtain scored link tuples suitable for downstream filtering, visualization, or prioritization.

## Related tools

- **nplinker** (Framework for loading data, instantiating MetcalfScoring, and executing get_links() to compute scored links and return LinkGraph objects) — https://github.com/NPLinker/nplinker
- **AntiSMASH** (Upstream tool for predicting and annotating biosynthetic gene clusters (BGCs); output used to define GCFs)
- **BigScape** (Clustering tool that groups AntiSMASH BGCs into Genomic Cluster Families (GCFs) for input to Metcalf scoring)
- **GNPS** (Source of molecular networking data (spectra and molecular families) that serve as metabolomic input to Metcalf scoring) — https://gnps.ucsd.edu
- **Python** (Programming language required for instantiating NPLinker, MetcalfScoring, and scripting get_links() invocations)

## Examples

```
from nplinker import NPLinker; npl = NPLinker('nplinker.toml'); npl.load_data(); link_graph = npl.get_links(npl.gcfs[:3], 'metcalf'); scored_links = list(link_graph.links)
```

## Evaluation signals

- LinkGraph object is returned and is non-empty (contains at least one scored link)
- All link scores in the LinkGraph fall within an expected numeric range (typically [0, 1] for normalized metrics)
- Link tuples are accessible and serializable via link_graph.links property
- Both GCF and spectral/molecular family entities are represented in the returned LinkGraph with corresponding metadata
- Scoring computation completes without raising exceptions when valid, pre-loaded genomic and metabolomic data are provided

## Limitations

- Metcalf scoring quality depends on the completeness and accuracy of upstream AntiSMASH/BigScape BGC annotations and GNPS molecular family clustering—garbage inputs produce unreliable links.
- The method produces weighted associations, not causal links; high scores indicate putative correlations but do not confirm true gene cluster–metabolite relationships without orthogonal validation.
- No discussion section is present in the source documentation to address methodological limitations, reproducibility caveats, or failure modes of the scoring algorithm itself.

## Evidence

- [other] The MetcalfScoring computation accepts GCFs and molecular families/spectra as inputs and computes links between them, returning a LinkGraph artifact that represents the scoring results.: "Initialize a MetcalfScoring instance with the loaded genomic and metabolomic entities. Execute the scoring computation via the NPLinker.get_links() method, which applies the Metcalf scoring algorithm"
- [other] The workflow demonstrates data loading, entity preparation, and link computation using Metcalf scoring.: "Load pre-prepared datasets containing GCFs (from AntiSMASH via BigScape clustering), spectra, and molecular families (from GNPS molecular networking) using NPLinker's DatasetLoader."
- [other] Validation confirms that the LinkGraph contains links with scores in expected ranges.: "Validate the LinkGraph by checking that links are present and scores are in expected range."
- [readme] The README confirms NPLinker's role as the primary framework for this workflow.: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data."
