---
name: spectral-molecular-family-linking
description: Use when when you have pre-processed genomic data (GCFs from AntiSMASH/BigScape clustering) and metabolomic data (spectra and molecular families from GNPS molecular networking) and need to systematically score and rank putative relationships between biosynthetic gene clusters and their.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0102
  tools:
  - nplinker
  - Python
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

# spectral-molecular-family-linking

## Summary

Compute weighted links between Genomic Cluster Families (GCFs) and molecular families/spectra using the Metcalf scoring algorithm, producing a directed LinkGraph artifact that represents genotype-phenotype associations in natural product discovery.

## When to use

When you have pre-processed genomic data (GCFs from AntiSMASH/BigScape clustering) and metabolomic data (spectra and molecular families from GNPS molecular networking) and need to systematically score and rank putative relationships between biosynthetic gene clusters and their corresponding metabolite products to prioritize targets for experimental validation.

## When NOT to use

- Genomic data is not organized as GCFs (e.g., raw BGC annotations without clustering); use BigScape clustering first.
- Metabolomic data lacks molecular networking (e.g., only raw spectra without family assignments); preprocessing via GNPS is required.
- Input spectra or GCFs contain missing or corrupted metadata; data must be validated and complete before scoring.

## Inputs

- Genomic Cluster Families (GCFs) from AntiSMASH/BigScape output
- Molecular spectra from GNPS (GNPS1 or GNPS2 workflows)
- Molecular families from GNPS molecular networking
- NPLinker-compatible dataset configuration

## Outputs

- LinkGraph artifact (directed weighted graph)
- Pairwise link scores between GCFs and spectra
- Link metadata (scores, confidence, source)

## How to apply

Initialize NPLinker's DatasetLoader with pre-prepared GCFs, spectral entities, and molecular families from GNPS. Instantiate a MetcalfScoring object passing the loaded genomic and metabolomic entities. Execute NPLinker.get_links() which applies the Metcalf scoring algorithm to compute pairwise link scores between each GCF and spectral entity, encoding the hypothesis that high-scoring links represent genuine BGC–metabolite associations. The returned LinkGraph is a directed weighted graph where nodes are GCFs and spectra, edges carry link scores, and metadata. Validate by confirming links are present and scores fall within the expected numerical range (typically 0–1 or normalized likelihood).

## Related tools

- **nplinker** (Executes Metcalf scoring computation and returns LinkGraph via DatasetLoader and get_links() method) — https://github.com/NPLinker/nplinker
- **BigScape** (Clusters AntiSMASH BGC annotations into Genomic Cluster Families (GCFs) used as linking targets)
- **AntiSMASH** (Detects and annotates biosynthetic gene clusters (BGCs) whose clustering produces GCF input)
- **GNPS** (Generates molecular families and spectral networks consumed as linking sources)
- **Python** (Programming language for NPLinker API invocation)

## Examples

```
from nplinker import NPLinker; npl = NPLinker('config.yaml'); npl.load_data(); links = npl.get_links(scoring_method='metcalf'); print(links.links[:10])
```

## Evaluation signals

- LinkGraph object is non-null and contains ≥1 edges (links present between GCFs and spectra)
- Link scores are numeric, bounded, and distributed within expected range (e.g., [0, 1] or normalized likelihood scores)
- LinkGraph metadata includes link provenance, timestamps, and scoring method identifier ('metcalf')
- Directed graph structure is consistent: edges point from GCFs to spectral entities with no self-loops
- High-scoring links correspond to known or validated BGC–metabolite associations (spot-check against literature or experimental data if available)

## Limitations

- Metcalf scoring relies on complete and accurate GCF and molecular family annotations; garbage-in-garbage-out applies if clustering or networking artifacts are present.
- Scoring does not account for biosynthetic plausibility or metabolite toxicity/stability; filtered links still require expert or experimental validation.
- LinkGraph is a bipartite projection; edges do not represent mechanistic biosynthetic steps, only statistical co-occurrence/homology signals.
- No discussion of reproducibility, failure modes, or sensitivity to parameter tuning is provided in the available documentation.

## Evidence

- [other] The MetcalfScoring computation accepts GCFs and molecular families/spectra as inputs and computes links between them, returning a LinkGraph artifact that represents the scoring results.: "The MetcalfScoring computation accepts GCFs and molecular families/spectra as inputs and computes links between them, returning a LinkGraph artifact that represents the scoring results."
- [other] Load pre-prepared datasets containing GCFs (from AntiSMASH via BigScape clustering), spectra, and molecular families (from GNPS molecular networking) using NPLinker's DatasetLoader.: "Load pre-prepared datasets containing GCFs (from AntiSMASH via BigScape clustering), spectra, and molecular families (from GNPS molecular networking) using NPLinker's DatasetLoader."
- [other] Execute the scoring computation via the NPLinker.get_links() method, which applies the Metcalf scoring algorithm to compute pairwise links between GCFs and spectral entities.: "Execute the scoring computation via the NPLinker.get_links() method, which applies the Metcalf scoring algorithm to compute pairwise links between GCFs and spectral entities."
- [other] Return a LinkGraph object containing the computed links as a directed weighted graph with link scores and metadata.: "Return a LinkGraph object containing the computed links as a directed weighted graph with link scores and metadata."
- [other] Validate the LinkGraph by checking that links are present and scores are in expected range.: "Validate the LinkGraph by checking that links are present and scores are in expected range."
- [readme] NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data.: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data."
