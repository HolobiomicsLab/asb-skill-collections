---
name: cross-omics-strain-mapping
description: Use when when you have paired genomics (AntiSMASH BGC annotations) and metabolomics (GNPS spectra and molecular families) data from the same microbial strains and need to identify which biosynthetic pathways produce which observed natural products.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0102
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3697
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

# cross-omics-strain-mapping

## Summary

Map genomic and metabolomic data from the same microbial strains by loading AntiSMASH biosynthetic gene clusters (BGCs), GNPS molecular families (MFs), and strain annotations into NPLinker, then computing scored links between GCFs and spectra to associate natural product biosynthesis with genomic origin.

## When to use

When you have paired genomics (AntiSMASH BGC annotations) and metabolomics (GNPS spectra and molecular families) data from the same microbial strains and need to identify which biosynthetic pathways produce which observed natural products. Use this skill when strain-level metadata connects both data modalities and you want to compute similarity-scored associations (e.g., metcalf, cosine) between GCFs and mass spectra.

## When NOT to use

- Input is missing consistent strain identifiers across genomics and metabolomics datasets — cross-omics mapping requires shared sample metadata.
- AntiSMASH or GNPS data is already preprocessed into a single integrated table — use this skill on raw or modality-specific outputs, not post-merged features.
- Genomics or metabolomics data alone is available without paired strain samples — the skill requires both modalities linked by strain.

## Inputs

- AntiSMASH BGC predictions (antismash/ directory)
- GNPS molecular families and spectra data (gnps/ directory)
- Strain metadata or shared identifiers across datasets
- nplinker.toml configuration file specifying root_dir, mode, and scoring methods

## Outputs

- LinkGraph object with scored associations between GCFs and spectra
- Link tuples (GCF, spectrum, score) via link_graph.links
- Strain-indexed mappings: npl.gcfs, npl.spectra, npl.mfs, npl.strains properties

## How to apply

First, organize AntiSMASH BGC predictions and GNPS molecular networking results (spectra, molecular families, and annotations) into separate subdirectories (antismash/ and gnps/) within a working directory, ensuring strain identifiers are consistent across datasets. Create an nplinker.toml configuration file specifying root_dir, mode='local' (for local execution), and scoring.methods=['metcalf'] or other supported scoring method. Instantiate NPLinker with the config file path and call npl.load_data() to ingest all entities from the subdirectories. Then call npl.get_links(npl.gcfs[:N], 'metcalf') on a subset of gene cluster families (GCFs) to compute metcalf-scored links; this returns a LinkGraph object containing scored tuples associating GCFs with spectra. Export results by iterating over link_graph.links and accessing the paired npl.gcfs, npl.spectra, and npl.strains properties to map genomic clusters to metabolomic observations at the strain level.

## Related tools

- **nplinker** (Core framework for loading, linking, and exporting cross-omics strain associations; computes similarity-scored links between GCFs and spectra using configurable scoring methods (metcalf, cosine, etc.)) — https://github.com/NPLinker/nplinker
- **AntiSMASH** (Provides BGC predictions and annotations that populate the antismash/ input directory; NPLinker ingests and indexes these as GCFs for linking to metabolomic data)
- **GNPS** (Produces molecular families, mass spectra, and spectral annotations ingested from the gnps/ directory; spectra are linked to GCFs via NPLinker scoring) — https://gnps.ucsd.edu
- **Python** (Runtime environment (≥3.11) for executing NPLinker API calls (npl.load_data(), npl.get_links()) and iterating over LinkGraph outputs)
- **BigScape** (Optional clustering tool; NPLinker can automatically invoke BigScape to compute GCF groupings if bigscape/ directory is absent)

## Examples

```
from nplinker import NPLinker; npl = NPLinker('nplinker.toml'); npl.load_data(); links = npl.get_links(npl.gcfs[:3], 'metcalf'); print([(g.id, s.spectrum_id, score) for g, s, score in links.links])
```

## Evaluation signals

- LinkGraph object returned by npl.get_links() is non-empty (contains ≥1 scored link tuple)
- All returned links have valid GCF and spectrum references resolvable via npl.gcfs and npl.spectra properties
- Metcalf scores (or chosen scoring method) fall within expected range (e.g., 0–1 for normalized similarity) and show variation across links (not all identical)
- Strain identifiers are consistent between GCF and spectrum in each link tuple, confirming cross-omics mapping at strain level
- Link counts and score distributions match expectations from input dataset size (e.g., N GCFs × M spectra ≤ total possible links)

## Limitations

- Requires consistent strain identifiers or metadata keys across AntiSMASH and GNPS datasets; missing or mismatched identifiers will result in incomplete or spurious strain mappings.
- Scoring method (metcalf, cosine, etc.) is fixed at configuration time; scoring method must be chosen a priori and cannot be changed without re-instantiation.
- Local mode (mode='local') processes data in memory; very large datasets (many strains, thousands of spectra/BGCs) may exceed available RAM.
- The skill relies on external data quality: incomplete or incorrectly annotated BGC predictions or poor GNPS spectral clustering will propagate errors into links.

## Evidence

- [other] NPLinker can compute links for the first GCFs using metcalf scoring method, producing a LinkGraph output.: "NPLinker can compute links for the first GCFs using metcalf scoring method, producing a LinkGraph output."
- [other] Create a configuration file nplinker.toml specifying root_dir as the working directory, mode='local', and scoring.methods=['metcalf'].: "Create a configuration file nplinker.toml specifying root_dir as the working directory, mode='local', and scoring.methods=['metcalf']."
- [other] Instantiate NPLinker with the configuration file path and call npl.load_data() to load GNPS spectra, molecular families, annotations, and AntiSMASH BGC data: "Instantiate NPLinker with the configuration file path and call npl.load_data() to load GNPS spectra, molecular families, annotations, and AntiSMASH BGC data from the gnps and antismash subdirectories."
- [other] Call npl.get_links(npl.gcfs[:3], 'metcalf') to compute metcalf-scored links between the first three GCFs and other entities, returning a LinkGraph object.: "Call npl.get_links(npl.gcfs[:3], 'metcalf') to compute metcalf-scored links between the first three GCFs and other entities, returning a LinkGraph object."
- [readme] NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data.: "NPLinker is a python framework for data mining microbial natural products by integrating genomics and metabolomics data."
- [other] Export the LinkGraph by accessing npl.gcfs, npl.spectra, npl.mfs, and npl.strains properties, and serialize link results via link_graph.links: "Export the LinkGraph by accessing npl.gcfs, npl.spectra, npl.mfs, and npl.strains properties, and serialize link results via link_graph.links to obtain scored link tuples."
