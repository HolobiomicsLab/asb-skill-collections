---
name: genome-cluster-family-scoring-computation
description: Use when you have pre-processed AntiSMASH BGC annotations (optionally clustered via BigScape into GCFs), GNPS molecular networking spectra and molecular families, and you seek to computationally link biosynthetic gene clusters to observed metabolites without manual curation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0621
  tools:
  - nplinker
  - Python
  - AntiSMASH
  - BigScape
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
---

# genome-cluster-family-scoring-computation

## Summary

Compute scoring-based links between Genomic Cluster Families (GCFs) and spectral/molecular families using the MetcalfScoring algorithm within NPLinker, producing a directed weighted LinkGraph artifact. This skill integrates AntiSMASH-derived BGC clusters with GNPS molecular networking data to infer genotype–phenotype associations.

## When to use

Apply this skill when you have pre-processed AntiSMASH BGC annotations (optionally clustered via BigScape into GCFs), GNPS molecular networking spectra and molecular families, and you seek to computationally link biosynthetic gene clusters to observed metabolites without manual curation. Trigger conditions: presence of antismash/ directory, gnps/ molecular networking archive, and spectra/molecular family definitions.

## When NOT to use

- Input spectral data lack GNPS molecular family annotations or metadata.
- BGC data are not clustered into GCFs or lack sufficient genomic context for inter-cluster comparison.
- You seek manual curation or have prior knowledge of specific genotype–phenotype pairs that should be validated rather than discovered de novo.

## Inputs

- AntiSMASH BGC annotations (antismash/ directory)
- BigScape-clustered GCFs or raw BGCs
- GNPS molecular networking archive (from GNPS1 or GNPS2 workflows)
- Spectral data objects
- Molecular family definitions

## Outputs

- LinkGraph artifact (directed weighted graph of GCF-to-spectrum links)
- Link scores and metadata

## How to apply

Load pre-prepared genomic and metabolomic datasets using NPLinker's DatasetLoader (AntiSMASH BGCs via BigScape clustering into GCFs, and GNPS spectra with molecular families). Initialize a MetcalfScoring instance with the loaded entities. Execute the scoring computation via NPLinker.get_links() method, which applies pairwise Metcalf scoring between GCFs and spectral entities. The algorithm returns a LinkGraph object—a directed weighted graph encoding computed links, their scores, and metadata. Validate by checking for non-empty link sets and verifying link scores fall within the expected range (typically 0 to 1 or algorithm-defined bounds). The scoring rationale weights chemical similarity, genomic proximity, and other features defined by the Metcalf method.

## Related tools

- **nplinker** (Core framework for executing MetcalfScoring and returning LinkGraph; wraps scoring computation and manages dataset loading.) — https://github.com/NPLinker/nplinker
- **AntiSMASH** (Generates BGC annotations that are input to NPLinker; BGCs are clustered into GCFs for scoring.)
- **BigScape** (Clusters AntiSMASH BGCs into GCFs; NPLinker can run BigScape automatically if the bigscape directory does not exist.)
- **GNPS** (Provides molecular networking data (spectra, molecular families) required as input to NPLinker for computing links.) — https://gnps.ucsd.edu
- **Python** (Programming environment for NPLinker execution; Python version ≥3.11 required.)

## Examples

```
from nplinker import NPLinker; npl = NPLinker(); npl.load_data(); links = npl.get_links(method='metcalf'); print(links)
```

## Evaluation signals

- LinkGraph object is non-empty: check that len(links) > 0 after computation.
- Link scores are within expected range: verify all scores satisfy 0 ≤ score ≤ 1 or align with Metcalf algorithm bounds.
- Graph structure is valid: confirm that LinkGraph contains directed edges with metadata (source GCF, target spectrum/family, score).
- Link count scales appropriately: for N GCFs and M spectra, verify computed link count is plausible (typically sparse, << N × M).
- Reproducibility check: re-run computation on identical inputs and confirm identical LinkGraph output.

## Limitations

- MetcalfScoring performance depends on quality and completeness of input AntiSMASH annotations and GNPS molecular networking; poor or missing metadata reduces link confidence.
- Scoring is computational (not experimental validation); links are predictions and require downstream biochemical or genomic evidence.
- BigScape clustering threshold and parameters influence GCF composition; different clustering parameters may yield different link sets.
- No discussion of edge cases or failure modes is provided in the article or README; robustness to incomplete or malformed input data is unclear.

## Evidence

- [other] The MetcalfScoring computation accepts GCFs and molecular families/spectra as inputs and computes links between them, returning a LinkGraph artifact that represents the scoring results.: "The MetcalfScoring computation accepts GCFs and molecular families/spectra as inputs and computes links between them, returning a LinkGraph artifact that represents the scoring results."
- [other] Load pre-prepared datasets containing GCFs (from AntiSMASH via BigScape clustering), spectra, and molecular families (from GNPS molecular networking) using NPLinker's DatasetLoader.: "Load pre-prepared datasets containing GCFs (from AntiSMASH via BigScape clustering), spectra, and molecular families (from GNPS molecular networking) using NPLinker's DatasetLoader."
- [other] Execute the scoring computation via the NPLinker.get_links() method, which applies the Metcalf scoring algorithm to compute pairwise links between GCFs and spectral entities.: "Execute the scoring computation via the NPLinker.get_links() method, which applies the Metcalf scoring algorithm to compute pairwise links between GCFs and spectral entities."
- [other] Return a LinkGraph object containing the computed links as a directed weighted graph with link scores and metadata.: "Return a LinkGraph object containing the computed links as a directed weighted graph with link scores and metadata."
- [readme] NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data.: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data."
