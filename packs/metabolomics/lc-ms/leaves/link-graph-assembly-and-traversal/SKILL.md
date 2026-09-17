---
name: link-graph-assembly-and-traversal
description: Use when after running a scoring algorithm (e.g., MetcalfScoring) on
  paired genomic and metabolomic datasets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3439
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3697
  tools:
  - nplinker
  - Python
  - BigScape
  - AntiSMASH
  - GNPS
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# link-graph-assembly-and-traversal

## Summary

Assemble and traverse LinkGraph artifacts representing weighted, directed links between Genomic Cluster Families (GCFs) and molecular families/spectra produced by scoring algorithms like Metcalf. This skill enables systematic exploration of genotype–phenotype associations in natural product discovery workflows.

## When to use

Apply this skill after running a scoring algorithm (e.g., MetcalfScoring) on paired genomic and metabolomic datasets. Use it when you need to extract, validate, and traverse the resulting LinkGraph to identify high-confidence GCF–spectrum associations, filter by score thresholds, or prepare links for downstream visualization or annotation.

## When NOT to use

- Input genomic or metabolomic data is missing or incomplete; LinkGraph assembly requires both paired omics inputs.
- Scoring algorithm has not been executed or LinkGraph artifact has not been produced; this skill operates on the output of a prior scoring step, not on raw data.
- You need to modify link scores post-hoc; LinkGraph is an immutable artifact of the scoring computation.

## Inputs

- Genomic Cluster Families (GCFs) from AntiSMASH/BigScape
- Molecular families and spectra from GNPS molecular networking
- Paired genomic and metabolomic datasets loaded via NPLinker DatasetLoader

## Outputs

- LinkGraph object (directed weighted graph with GCF–spectrum links)
- Link scores and metadata for each GCF–spectrum association
- Filtered or subgraph LinkGraph for downstream visualization or annotation

## How to apply

Initialize a MetcalfScoring instance with loaded GCFs (from AntiSMASH via BigScape clustering) and spectral entities (from GNPS molecular networking) via NPLinker's DatasetLoader. Execute the scoring computation using NPLinker.get_links() to compute pairwise links between GCFs and spectral entities, returning a LinkGraph object as a directed weighted graph with link scores and metadata. Validate the LinkGraph by checking that links are present and scores fall within expected ranges (e.g., 0–1 for normalized scores). Traverse the graph by iterating over nodes and edges to extract high-confidence associations, apply score-based filtering, or prepare subgraphs for downstream analysis.

## Related tools

- **nplinker** (Core framework for assembling LinkGraph from MetcalfScoring output via DatasetLoader and get_links() API) — https://github.com/NPLinker/nplinker
- **BigScape** (Generates GCF clustering from AntiSMASH output, input for LinkGraph assembly)
- **AntiSMASH** (Produces Biosynthetic Gene Cluster (BGC) predictions, raw input for GCF clustering)
- **GNPS** (Provides molecular networking data including spectral families and metadata, input for LinkGraph assembly)

## Examples

```
from nplinker import NPLinker; npl = NPLinker(); npl.load_data(); links = npl.get_links(scoring_method='metcalf'); link_graph = links; print(f'Assembled LinkGraph with {len(link_graph.edges())} links')
```

## Evaluation signals

- LinkGraph object is successfully instantiated with no missing or null node/edge attributes.
- Link scores are present and fall within expected numerical range (e.g., 0–1 for normalized Metcalf scores).
- Number of links in the graph matches the number of valid GCF–spectrum pairs after scoring computation.
- Graph traversal (iteration over nodes and edges) completes without errors and returns consistent topology.
- Subgraph filtering by score threshold reduces link count monotonically and produces valid sub-LinkGraph.

## Limitations

- LinkGraph assembly depends on quality and completeness of upstream AntiSMASH/BigScape GCF clustering and GNPS molecular networking; garbage-in, garbage-out behavior inherited from input data.
- Metcalf scoring may produce low or zero scores for genuine GCF–spectrum associations if the genomic and metabolomic signals are weak or misaligned in time/space.
- LinkGraph traversal and filtering are read-only operations; the underlying scored edges cannot be recomputed or adjusted post-assembly without re-running the scoring step.

## Evidence

- [other] The MetcalfScoring computation accepts GCFs and molecular families/spectra as inputs and computes links between them, returning a LinkGraph artifact that represents the scoring results.: "Execute the scoring computation via the NPLinker.get_links() method, which applies the Metcalf scoring algorithm to compute pairwise links between GCFs and spectral entities. 4. Return a LinkGraph"
- [other] NPLinker requires paired genomic and metabolomic data to assemble the LinkGraph.: "Load pre-prepared datasets containing GCFs (from AntiSMASH via BigScape clustering), spectra, and molecular families (from GNPS molecular networking) using NPLinker's DatasetLoader."
- [other] Validation of LinkGraph involves checking link presence and score ranges.: "Validate the LinkGraph by checking that links are present and scores are in expected range."
- [readme] NPLinker is the core framework for implementing link-graph assembly in natural product discovery.: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data."
