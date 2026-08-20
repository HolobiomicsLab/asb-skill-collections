---
name: sample-prioritization-through-structural-clustering
description: Use when you have 2D NMR spectral data (HSQC, HMBC, COSY) from multiple samples in a natural products screening campaign and need to rank samples by structural novelty or identify which samples share common molecular scaffolds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0080
  tools:
  - MADByTE
  - conda
  - Python
  techniques:
  - NMR
derived_from:
- doi: 10.1021/acs.jnatprod.0c01076
  title: MADByTE
evidence_spans:
- MADByTE stands for **M**etabolomics **A**nd **D**ereplication **By** **T**wo-dimensional **E**xperiments.
- conda env create -f environment.yml
- If you have followed the installation guide and setup the MADByTE Python virtual environment
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_madbyte_cq
    doi: 10.1021/acs.jnatprod.0c01076
    title: MADByTE
  dedup_kept_from: coll_madbyte_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jnatprod.0c01076
  all_source_dois:
  - 10.1021/acs.jnatprod.0c01076
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-prioritization-through-structural-clustering

## Summary

Identify and rank samples in large natural product mixtures by computing shared structural features across heteronuclear (HSQC, HMBC) and homonuclear (COSY) 2D NMR spectra, enabling rapid prioritization based on scaffold commonality and inter-sample relationships. This skill leverages comparative NMR analysis to distinguish structurally novel from redundant samples within a cohort.

## When to use

You have 2D NMR spectral data (HSQC, HMBC, COSY) from multiple samples in a natural products screening campaign and need to rank samples by structural novelty or identify which samples share common molecular scaffolds. Apply this skill when sample size is large enough that manual spectral comparison is impractical, and when you want to guide downstream synthetic or isolation effort toward the most structurally diverse or interesting compounds.

## When NOT to use

- Input is already a curated feature table or pre-filtered scaffold inventory — direct network analysis is more efficient.
- Sample set is very small (< 5 samples) — manual spectral comparison or targeted peak assignment is faster and more transparent.
- NMR spectra are of poor quality, heavily overlapped, or from a single sample — the method requires multi-sample comparative power to derive meaningful scaffolds.

## Inputs

- 2D heteronuclear NMR spectral data (HSQC, HMBC format)
- 2D homonuclear NMR spectral data (COSY format)
- Multi-sample dataset with spectral files for all samples in cohort

## Outputs

- Feature/correlation network representation (graph structure)
- Adjacency matrix or graph file (suitable for network visualization)
- Sample-level connectivity metrics and prioritization ranking
- Shared structural feature annotations across samples

## How to apply

Load heteronuclear and homonuclear 2D NMR spectral datasets for all samples into MADByTE. Run the comparative analysis pipeline, which simultaneously processes all experiments to identify and correlate common peaks across the sample set. The pipeline generates a feature/correlation network that represents shared structural scaffolds as interconnected nodes; samples with fewer or weaker connections to the network represent potential structural outliers and are prioritized for further investigation. Export the resulting network as an adjacency matrix or graph structure to support downstream visualization and interpretation. Prioritization rank is derived from node connectivity: samples with unique or underrepresented structural features appear as peripheral or isolated nodes, making them candidates for prioritization.

## Related tools

- **MADByTE** (Executes comparative 2D NMR analysis pipeline to identify shared structural features and generate feature/correlation networks across large sample sets) — https://github.com/liningtonlab/madbyte
- **conda** (Manages and activates the MADByTE Python virtual environment from environment.yml configuration)
- **Python** (Runtime environment for MADByTE launcher script execution and network export)

## Examples

```
conda activate madbyte && python madbyte_gui.py
```

## Evaluation signals

- Network connectivity distribution shows variance across samples; samples with low degree centrality represent structural outliers and prioritization candidates.
- Shared structural feature nodes are robustly reproducible across multiple 2D experiment types (heteronuclear and homonuclear); spurious peaks do not cluster consistently.
- Sample clusters in the network align with known or expected chemical classes or natural product families when structural context is available.
- Exported adjacency matrix is symmetric and can be imported into standard graph visualization tools (Cytoscape, igraph) without format errors.
- Prioritized samples (peripheral nodes) yield novel or unique peak patterns when their individual spectra are inspected post-hoc; central samples show expected redundancy.

## Limitations

- Method requires sufficient spectral quality and peak resolution across the cohort; heavily overlapped or noisy spectra degrade feature correlation accuracy.
- Prioritization is based on comparative scaffold commonality, not on bioactivity or chemical novelty; structurally unique samples may still be chemically uninteresting.
- Peak alignment and feature correlation sensitivity depend on spectral referencing consistency and acquisition parameters across samples; systematic offsets can inflate false feature dissimilarity.
- Large sample sets (> ~100 samples) may exceed computational memory or runtime constraints; scalability is not explicitly characterized in the published work.

## Evidence

- [readme] MADByTE allows for comparative analysis of NMR spectra from large sample sets, simultaneously, deriving shared structural features from heteronuclear and homonuclear experiments.: "MADByTE allows for comparative analysis of NMR spectra from large sample sets, simultaneously, deriving shared structural features from heteronuclear and homonuclear experiments."
- [readme] Using large sample sets, the common features between each sample can be visualized to aid in sample prioritization and structure characterization of scaffolds present.: "Using large sample sets, the common features between each sample can be visualized to aid in sample prioritization and structure characterization of scaffolds present."
- [intro] Run the MADByTE launcher script to execute the comparative analysis pipeline, which identifies and correlates common peaks across samples.: "Run the MADByTE launcher script to execute the comparative analysis pipeline, which identifies and correlates common peaks across samples."
- [intro] Generate a feature/correlation network representation that visualizes shared structural scaffolds and inter-sample relationships.: "Generate a feature/correlation network representation that visualizes shared structural scaffolds and inter-sample relationships."
- [readme] MADByTE stands for Metabolomics And Dereplication By Two-dimensional Experiments.: "MADByTE stands for **M**etabolomics **A**nd **D**ereplication **By** **T**wo-dimensional **E**xperiments."
