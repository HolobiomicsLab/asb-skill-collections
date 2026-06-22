---
name: molecular-networking-construction
description: Use when you have LC-MS/MS DDA data from one or more samples and need to organize fragmentation spectra by similarity relationships to support compound annotation, enable cross-sample comparisons, and identify known and unknown metabolites sharing structural features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_2258
  tools:
  - ENPKG
  - MZmine
  - ENPKG MN/ISDB/Taxo module
  - MEMO
derived_from:
- doi: 10.1021/acscentsci.3c00800
  title: enpkg
evidence_spans:
- Welcome to the ENPKG Full Workflow!
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_enpkg
    doi: 10.1021/acscentsci.3c00800
    title: enpkg
  dedup_kept_from: coll_enpkg
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acscentsci.3c00800
  all_source_dois:
  - 10.1021/acscentsci.3c00800
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-networking-construction

## Summary

Generate a Molecular Network (MN) from LC-MS/MS DDA fragmentation spectra to group related compounds and enable spectral similarity-based annotation and structural relationships across a metabolomics dataset.

## When to use

You have LC-MS/MS DDA data from one or more samples and need to organize fragmentation spectra by similarity relationships to support compound annotation, enable cross-sample comparisons, and identify known and unknown metabolites sharing structural features.

## When NOT to use

- Input data is already a curated spectral library (use direct matching instead)
- Only targeted/SRM data are available without fragmentation spectra (MN requires DDA MS/MS)
- Sample size is very small (single scan) or fragmentation data are missing/poor quality

## Inputs

- LC-MS/MS DDA spectra in mzML or mzXML format (positive and/or negative ionization modes)
- MZmine-processed feature detection output
- Sample metadata with taxon information

## Outputs

- Molecular Network graph structure (nodes=MS2 spectra, edges=cosine similarity ≥ threshold)
- Network-annotated feature table with cluster assignments
- Spectral adjacency matrix or GraphML format compatible with MEMO analysis

## How to apply

After MZmine processing of raw LC-MS/MS DDA data (positive and/or negative ionization modes), invoke the molecular networking module within the ENPKG workflow. The workflow automatically generates the MN from fragmentation spectra and integrates it with downstream spectral matching and taxonomical reweighting. The MN construction uses cosine similarity metrics to cluster related fragmentation patterns, creating a graph where nodes represent MS2 spectra and edges represent similarity above a defined threshold. Validate the resulting network structure for connected components, edge weight distributions, and consistency with known compound clusters. The output MN is then compatible with MEMO analysis for cross-sample spectral fingerprint comparison and serves as input for subsequent annotation steps.

## Related tools

- **MZmine** (Pre-processes raw LC-MS/MS DDA data, detects features, and exports spectra for MN construction) — http://mzmine.github.io/
- **ENPKG MN/ISDB/Taxo module** (Orchestrates MN generation, spectral matching, and taxonomical reweighting on processed samples) — https://github.com/enpkg/enpkg_mn_isdb_taxo
- **MEMO** (Generates MEMO matrix from samples' spectral data for comparative analysis of spectral fingerprints) — https://github.com/mandelbrot-project/memo

## Examples

```
bash src/install_sirius.sh /opt/sirius && sh workflow/00_workflow_all.sh
```

## Evaluation signals

- Network contains expected number of connected components relative to sample complexity and MS/MS quality
- Edge weights (cosine similarity scores) cluster known compound pairs above threshold; absence of false-positive edges between structurally unrelated spectra
- Degree distribution and clustering coefficient are consistent with expected metabolite diversity (not all nodes isolated; not fully connected)
- Feature annotations align with network neighbor identities—high-confidence matches co-localize in network neighborhoods
- Output is compatible with downstream MEMO analysis and produces valid GraphML/adjacency matrices

## Limitations

- MN quality depends critically on MS/MS spectrum quality; low-abundance or noisy spectra may produce spurious or missing edges
- Cosine similarity threshold is data-dependent; suboptimal thresholds can over-cluster or fragment true compound families
- MN alone does not provide compound identities; must be coupled with spectral matching and taxonomical reweighting for actionable annotations
- Network construction is computationally intensive for very large datasets (>10,000 spectra); scalability depends on available hardware

## Evidence

- [readme] For each sample, the workflow automatically resolves the species taxonomy against Open Tree of Life (ottID), generates a Molecular Network from fragmentation spectra (MN) and annotates features using two different methods (spectral matching to in silico DB coupled to taxonomical reweighting and Sirius/CSI:FingerID).: "generates a Molecular Network from fragmentation spectra (MN) and annotates features using two different methods (spectral matching to *in silico* DB coupled to taxonomical reweighting and"
- [readme] The different steps are described below, with the link to the corresponding repository to perform the analysis: MN, ISDB annotation and taxonomical/chemical consistency reweighting. Aim: MN generation, ISDB and MS1 annotation coupled to taxonomical and chemical consistency reweighting on each sample.: "MN generation, ISDB and MS1 annotation coupled to taxonomical and chemical consistency reweighting on each sample"
- [readme] The generated data structure is compatible with a MEMO analysis. Finally, all of the data previously generated is integrated into a sample-specific RDF knowledge graph.: "The generated data structure is compatible with a [MEMO](https://github.com/mandelbrot-project/memo) analysis."
- [readme] These sample-specific KG from multiple specific can be combined to effectively compare samples based on their metadata and their spectral and structural data.: "These sample-specific KG from multiple specific can be combined to effectively compare samples based on their metadata and their spectral and structural data."
