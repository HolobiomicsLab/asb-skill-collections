---
name: graph-based-link-representation-visualization
description: Use when after NPLinker computes scored links between genomic and metabolomic entities using a scoring method (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3083
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3520
  tools:
  - nplinker
  - Python
  - conda
  - pip
  - BigScape
  - GNPS
  - AntiSMASH
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

# graph-based-link-representation-visualization

## Summary

Represent and visualize molecular links discovered between genomic and metabolomic entities (GCFs, spectra, molecular families, strains) as a LinkGraph object, enabling structured access to scored link relationships for downstream analysis and interpretation.

## When to use

After NPLinker computes scored links between genomic and metabolomic entities using a scoring method (e.g., metcalf), use this skill to construct and inspect the resulting LinkGraph to examine which GCFs are linked to spectra/molecular families, access link scores, and prepare linked data for export or visualization.

## When NOT to use

- Input data is not yet loaded into NPLinker (i.e., npl.load_data() has not been called)
- No links have been computed yet (npl.get_links() has not been invoked)
- Link computation has failed or returned an empty LinkGraph due to incompatible input data or scoring method

## Inputs

- NPLinker instance with loaded GNPS spectra, molecular families, and AntiSMASH BGC data
- Computed links from npl.get_links() call with a specified scoring method (e.g., metcalf)
- LinkGraph object returned from link computation

## Outputs

- LinkGraph object containing scored link relationships
- Enumerated GCF, spectrum, molecular family, and strain entities accessible via properties
- Scored link tuples (link_graph.links) representing relationships between entities with associated scores

## How to apply

After calling npl.get_links() with a scoring method, the returned LinkGraph object provides structured access to NPLinker's four core entity types: GCFs (from AntiSMASH), spectra (from GNPS), molecular families (from GNPS), and strains. Access the LinkGraph via properties such as npl.gcfs, npl.spectra, npl.mfs, and npl.strains to enumerate entities, then retrieve scored link tuples from link_graph.links to examine link strength and relationships. The LinkGraph acts as the primary data structure for representing integration results, making it essential for understanding which genomic regions correlate with detected metabolites and for filtering or ranking links by score before export.

## Related tools

- **nplinker** (Framework that instantiates, loads data into, and returns LinkGraph objects representing computed genomic-metabolomic links) — https://github.com/NPLinker/nplinker
- **GNPS** (Source of spectra and molecular family data that populate the LinkGraph as metabolomic entities)
- **AntiSMASH** (Source of BGC data that populate the LinkGraph as GCF (genomic cluster family) entities)

## Examples

```
npl.get_links(npl.gcfs[:3], 'metcalf'); print([(link.gcf.id, link.spectrum.spectrum_id, link.score) for link in npl.link_graph.links])
```

## Evaluation signals

- LinkGraph object is non-empty and contains at least one link (link_graph.links is populated)
- All four entity types (GCFs, spectra, molecular families, strains) are accessible and enumerable via LinkGraph properties
- Link tuples in link_graph.links contain valid score values corresponding to the scoring method used (e.g., metcalf scores are numeric and within expected range)
- Entity counts match the input GNPS and AntiSMASH data (e.g., npl.gcfs count ≤ total BGCs in antismash directory)
- Link relationships are bidirectional: each link can be traced back to source entities (GCF, spectrum, MF, strain)

## Limitations

- LinkGraph representation is specific to the scoring method and parameters used; different scoring methods (e.g., metcalf vs. other scorers) produce different link topologies
- LinkGraph does not persist relationships if not explicitly exported; it exists only in memory during the NPLinker session
- Large datasets may result in LinkGraphs with high cardinality, requiring filtering or post-processing to identify high-confidence links
- The document provided contains only changelog entries and dependency history, lacking discussion of LinkGraph serialization formats or visualization limitations

## Evidence

- [other] Call npl.get_links(npl.gcfs[:3], 'metcalf') to compute metcalf-scored links between the first three GCFs and other entities, returning a LinkGraph object.: "Call npl.get_links(npl.gcfs[:3], 'metcalf') to compute metcalf-scored links between the first three GCFs and other entities, returning a LinkGraph object."
- [other] Export the LinkGraph by accessing npl.gcfs, npl.spectra, npl.mfs, and npl.strains properties, and serialize link results via link_graph.links to obtain scored link tuples.: "Export the LinkGraph by accessing npl.gcfs, npl.spectra, npl.mfs, and npl.strains properties, and serialize link results via link_graph.links to obtain scored link tuples."
- [readme] NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data.: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data."
