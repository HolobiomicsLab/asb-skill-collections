---
name: nmr-spectral-comparative-analysis
description: Use when you have 2D NMR spectral data (heteronuclear and/or homonuclear experiments) from multiple samples in a natural products library or mixture, and you need to identify common structural scaffolds, correlate features across samples, or prioritize samples for further structural annotation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3370
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
---

# NMR spectral comparative analysis

## Summary

Comparative analysis of 2D NMR spectra across large sample sets to identify and visualize shared structural features from both heteronuclear (HSQC, HMBC) and homonuclear (COSY) experiments. This skill enables rapid scaffold characterization and sample prioritization in complex natural product mixtures.

## When to use

You have 2D NMR spectral data (heteronuclear and/or homonuclear experiments) from multiple samples in a natural products library or mixture, and you need to identify common structural scaffolds, correlate features across samples, or prioritize samples for further structural annotation without running individual peak assignments.

## When NOT to use

- Input spectra are from only a single sample (comparative analysis requires multiple samples)
- Spectra lack both heteronuclear and homonuclear experiment types (the method relies on simultaneous analysis of both)
- Goal is de novo full structural elucidation of individual compounds (this skill identifies shared scaffolds, not complete structures)

## Inputs

- 2D NMR spectral data in MADByTE-compatible format (heteronuclear experiments: HSQC, HMBC)
- 2D NMR spectral data (homonuclear experiments: COSY)
- Multiple sample spectra (large sample sets)
- MADByTE environment configuration (environment.yml)

## Outputs

- Feature/correlation network representation (graph format)
- Adjacency matrix or network file
- Shared structural feature annotations
- Inter-sample relationship visualization
- Sample prioritization list based on scaffold similarity

## How to apply

Load heteronuclear (HSQC, HMBC) and homonuclear (COSY) 2D NMR spectral data for all samples simultaneously into the MADByTE workflow. The pipeline correlates common peaks across the sample set and derives shared structural features by analyzing patterns consistent across both experiment types. Execute the comparative analysis to generate a feature/correlation network that visualizes inter-sample relationships and scaffold structures. Export the resulting network in graph or adjacency matrix format to enable downstream visualization and interpretation. Success depends on uniform spectral acquisition and sufficient sample set size (multiple samples) to yield meaningful inter-sample correlation patterns.

## Related tools

- **MADByTE** (Core platform for executing comparative 2D NMR spectral analysis and feature/correlation network generation across sample sets) — https://github.com/liningtonlab/madbyte
- **conda** (Environment manager for installing and activating the MADByTE Python virtual environment)
- **Python** (Runtime environment for MADByTE launcher scripts and spectral processing pipeline)

## Examples

```
conda activate madbyte
python madbyte_gui.py
```

## Evaluation signals

- Network output contains ≥2 connected components representing shared features across samples
- Exported adjacency matrix is symmetric and square (nodes = samples or features; edges = correlations)
- Visualized correlation network highlights clustered samples (grouping by structural similarity), indicating discriminative power
- Common peaks identified in network are verifiable by overlay of raw 2D spectra from multiple samples
- Output file format matches expected graph/adjacency format suitable for downstream visualization tools

## Limitations

- Requires simultaneous acquisition of heteronuclear AND homonuclear experiments; missing experiment type reduces feature correlation confidence
- Performance and feature quality scale with sample set size; very small sample sets (<3–5 samples) may not yield robust inter-sample patterns
- Spectral preprocessing (phase correction, baseline correction) must be uniform across all samples to avoid artifactual feature misalignment
- Does not automatically assign chemical structures to identified shared features; network identifies scaffolds but requires manual annotation or external database matching
- Installation via Anaconda Navigator is explicitly not supported; must use conda command-line or provided .bat script

## Evidence

- [readme] MADByTE allows for comparative analysis of NMR spectra from large sample sets, simultaneously, deriving shared structural features from heteronuclear and homonuclear experiments.: "MADByTE allows for comparative analysis of NMR spectra from large sample sets, simultaneously, deriving shared structural features from heteronuclear and homonuclear experiments."
- [readme] Using large sample sets, the common features between each sample can be visualized to aid in sample prioritization and structure characterization of scaffolds present.: "Using large sample sets, the common features between each sample can be visualized to aid in sample prioritization and structure characterization of scaffolds present."
- [other] Load heteronuclear (e.g., HSQC, HMBC) and homonuclear (e.g., COSY) 2D NMR spectral data for all samples in the dataset.: "Load heteronuclear (e.g., HSQC, HMBC) and homonuclear (e.g., COSY) 2D NMR spectral data for all samples in the dataset."
- [other] Generate a feature/correlation network representation that visualizes shared structural scaffolds and inter-sample relationships.: "Generate a feature/correlation network representation that visualizes shared structural scaffolds and inter-sample relationships."
- [other] Export the network as a structured output file (graph or adjacency format) suitable for downstream visualization and interpretation.: "Export the network as a structured output file (graph or adjacency format) suitable for downstream visualization and interpretation."
- [readme] DO NOT INSTALL MADBYTE USING ANACONDA NAVIGATOR - IT WILL FAIL INSTALLATION.: "DO NOT INSTALL MADBYTE USING ANACONDA NAVIGATOR - IT WILL FAIL INSTALLATION."
- [readme] Ensure your virtual environment is activated and run the launcher script.: "Ensure your virtual environment is activated and run the launcher script."
