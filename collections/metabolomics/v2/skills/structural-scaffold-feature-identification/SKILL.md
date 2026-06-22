---
name: structural-scaffold-feature-identification
description: Use when you have 2D NMR spectral data (HSQC, HMBC, COSY) from multiple samples in a library or mixture and need to identify which structural scaffolds are shared across samples, prioritize samples for further analysis based on scaffold novelty or frequency, or characterize the core structural.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3680
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - MADByTE
  - conda
  - Python
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Structural-Scaffold Feature Identification from 2D NMR Spectra

## Summary

Identify and visualize shared structural scaffolds across large sample sets by simultaneously analyzing heteronuclear (HSQC, HMBC) and homonuclear (COSY) 2D NMR experiments to derive comparative features and enable sample prioritization. This skill uses MADByTE's correlation network approach to extract common structural motifs from complex natural product mixtures without requiring full structure elucidation.

## When to use

Apply this skill when you have 2D NMR spectral data (HSQC, HMBC, COSY) from multiple samples in a library or mixture and need to identify which structural scaffolds are shared across samples, prioritize samples for further analysis based on scaffold novelty or frequency, or characterize the core structural frameworks present in a complex extract without individual compound isolation.

## When NOT to use

- Your data includes only 1D NMR spectra (e.g., 1H or 13C alone); MADByTE requires 2D heteronuclear and homonuclear experiments for comparative scaffold analysis.
- You have already fully characterized individual compound structures and seek only to verify known compounds; MADByTE is designed for de novo scaffold discovery and dereplication, not validation of known structures.
- Your samples are pure compounds rather than complex mixtures; the comparative advantage of simultaneous multi-sample analysis is lost on isolated structures.

## Inputs

- Heteronuclear 2D NMR spectra (HSQC, HMBC) for multiple samples in a library
- Homonuclear 2D NMR spectra (COSY) for the same sample set
- NMR spectral data in format compatible with MADByTE (typically Bruker or converted formats)
- Sample metadata or sample identifiers for the dataset

## Outputs

- Feature/correlation network representation mapping shared structural scaffolds across samples
- Network graph file (graph or adjacency matrix format) for visualization and downstream analysis
- Structured output identifying which samples share common structural features
- Network connectivity metrics enabling sample prioritization by scaffold rarity or frequency

## How to apply

Activate the MADByTE Python environment using conda from the provided environment.yml configuration file. Load heteronuclear (HSQC, HMBC) and homonuclear (COSY) 2D NMR spectral data for all samples in your dataset into MADByTE. Execute the MADByTE launcher script to run the comparative analysis pipeline, which correlates common peaks across the full sample set. The algorithm simultaneously processes both experiment types to identify structural features that recur across samples. Inspect the generated feature/correlation network visualization to assess scaffold distribution: samples with high node connectivity share more structural features, while isolated or sparsely connected samples may represent novel scaffolds. Export the network as a graph or adjacency matrix for downstream interpretation or filtering by scaffold frequency thresholds.

## Related tools

- **MADByTE** (Primary tool for comparative 2D NMR analysis and automated shared structural feature extraction across large sample sets) — https://github.com/liningtonlab/madbyte
- **conda** (Environment manager for installing and activating the MADByTE Python virtual environment with specified dependencies)
- **Python** (Runtime environment for MADByTE launcher script execution (madbyte_gui.py))

## Examples

```
conda activate madbyte && python madbyte_gui.py
```

## Evaluation signals

- Network generated contains nodes for each sample and edges weighted by shared feature frequency; samples with high scaffold similarity show high edge weights or clustering.
- Feature/correlation network is parseable as a valid graph or adjacency matrix with consistent node naming and numeric edge weights or connectivity counts.
- Exported network file contains all samples from input dataset with no missing or corrupted entries.
- Visual inspection of network shows expected clustering patterns: known structurally related samples appear proximal in the network, while structurally distinct samples are isolated or sparsely connected.
- Peak correlation counts between sample pairs are consistent when re-run with identical inputs (deterministic reproducibility).

## Limitations

- MADByTE requires high-quality 2D NMR spectra with clear, well-resolved peaks; noisy, overlapped, or poorly shimmed spectra will produce unreliable peak correlations and scaffold assignments.
- The method identifies common structural features but does not automatically assign absolute stereochemistry, full connectivity, or functional group identity without additional orthogonal data (MS, 1D multiplicities, chemical shifts).
- Comparative analysis scales with sample set size; very large libraries (>1000 samples) may require computational optimization or subsampling strategies not detailed in the core workflow.
- Do NOT install MADByTE using Anaconda Navigator; manual conda installation via included .bat script or environment.yml is mandatory to avoid installation failure.

## Evidence

- [readme] MADByTE allows for comparative analysis of NMR spectra from large sample sets, simultaneously, deriving shared structural features from heteronuclear and homonuclear experiments.: "MADByTE allows for comparative analysis of NMR spectra from large sample sets, simultaneously, deriving shared structural features from heteronuclear and homonuclear experiments."
- [readme] Using large sample sets, the common features between each sample can be visualized to aid in sample prioritization and structure characterization of scaffolds present.: "Using large sample sets, the common features between each sample can be visualized to aid in sample prioritization and structure characterization of scaffolds present."
- [other] Load heteronuclear (e.g., HSQC, HMBC) and homonuclear (e.g., COSY) 2D NMR spectral data for all samples in the dataset.: "Load heteronuclear (e.g., HSQC, HMBC) and homonuclear (e.g., COSY) 2D NMR spectral data for all samples in the dataset."
- [other] Generate a feature/correlation network representation that visualizes shared structural scaffolds and inter-sample relationships.: "Generate a feature/correlation network representation that visualizes shared structural scaffolds and inter-sample relationships."
- [readme] We **Highly** recommend installing through the included .bat script or installing manually with `conda env create -f environment.yml`.: "We **Highly** recommend installing through the included .bat script or installing manually with `conda env create -f environment.yml`."
- [readme] If you have followed the installation guide and setup the MADByTE Python virtual environment, then navigate to the root directory of the code using your console/terminal (the directory this `README` is located in). Ensure your virtual environment is activated and run the launcher script.: "Ensure your virtual environment is activated and run the launcher script."
