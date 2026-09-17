---
name: heteronuclear-homonuclear-correlation-extraction
description: Use when you have 2D NMR spectral data from multiple samples (a large
  sample set) including both heteronuclear experiments (HSQC, HMBC) and homonuclear
  experiments (COSY), and your goal is to identify which structural features are conserved
  across samples, prioritize samples by scaffold similarity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3628
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0153
  tools:
  - MADByTE
  - conda
  - Python
  techniques:
  - NMR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.jnatprod.0c01076
  title: MADByTE
evidence_spans:
- MADByTE stands for **M**etabolomics **A**nd **D**ereplication **By** **T**wo-dimensional
  **E**xperiments.
- conda env create -f environment.yml
- If you have followed the installation guide and setup the MADByTE Python virtual
  environment
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

# Heteronuclear-Homonuclear Correlation Extraction

## Summary

Extract and correlate shared structural features across multiple NMR samples by simultaneously processing heteronuclear (HSQC, HMBC) and homonuclear (COSY) 2D experiments. This skill enables rapid dereplication and scaffold identification in natural product mixtures by identifying common peaks and inter-sample relationships.

## When to use

Apply this skill when you have 2D NMR spectral data from multiple samples (a large sample set) including both heteronuclear experiments (HSQC, HMBC) and homonuclear experiments (COSY), and your goal is to identify which structural features are conserved across samples, prioritize samples by scaffold similarity, or characterize the dominant scaffold structures present in a natural product mixture.

## When NOT to use

- Input is already a curated feature table or pre-extracted peak list — use this skill only on raw or minimally processed 2D NMR spectral data.
- Single sample or very small cohorts (< 3–5 samples) — the skill is designed for comparative analysis of large sample sets where shared feature patterns emerge.
- Only 1D NMR data is available — MADByTE requires both heteronuclear and homonuclear 2D experiments to derive reliable structural correlations.

## Inputs

- Heteronuclear 2D NMR spectra (HSQC, HMBC format) for multiple samples
- Homonuclear 2D NMR spectra (COSY format) for multiple samples
- MADByTE Python virtual environment configuration (environment.yml)
- Sample metadata or sample list identifying all spectra to be analyzed

## Outputs

- Feature/correlation network (graph or adjacency matrix format)
- Shared structural feature map across samples
- Inter-sample relationship visualization
- Sample prioritization ranking by structural similarity
- Scaffold structure characterization output

## How to apply

Activate the MADByTE Python virtual environment using conda with the provided environment.yml configuration. Load all heteronuclear and homonuclear 2D NMR spectral data for the entire sample set into MADByTE. Execute the comparative analysis pipeline via the launcher script, which simultaneously processes all experiments to identify and correlate common peaks across samples. The pipeline generates a feature/correlation network that maps shared structural scaffolds and inter-sample relationships. Export the resulting network in graph or adjacency matrix format, which can then be visualized and interpreted to rank samples by structural similarity and characterize dominant scaffold structures. The simultaneous processing of multiple experiment types (rather than sequential analysis) is critical to the workflow's ability to leverage complementary structural information.

## Related tools

- **MADByTE** (Core platform for simultaneous heteronuclear/homonuclear 2D NMR comparative analysis and shared feature identification) — https://github.com/liningtonlab/madbyte
- **conda** (Environment manager for activating and maintaining the MADByTE Python virtual environment)
- **Python** (Runtime language for MADByTE launcher scripts and pipeline execution)

## Examples

```
conda activate madbyte && python madbyte_gui.py
```

## Evaluation signals

- Feature/correlation network contains nodes for each sample and edges representing shared structural features, with inter-sample connectivity proportional to scaffold similarity.
- Network export file is valid in declared graph/adjacency format (e.g., valid JSON, edge list, or matrix) and can be ingested by standard visualization tools without parsing errors.
- Common peaks identified in heteronuclear and homonuclear experiments are consistent (e.g., a peak in HSQC that correlates to a COSY cross-peak is represented as a single shared feature node, not duplicates).
- Sample prioritization ranking reflects expected chemical similarity (e.g., samples known to contain the same natural product scaffold rank higher than structurally unrelated samples).
- Network size and edge density are consistent with the input sample set size and structural diversity (sparse networks for highly diverse samples, denser networks for closely related samples).

## Limitations

- Installation must be performed manually via conda command-line or included .bat script; Anaconda Navigator installation will fail.
- Requires high-quality 2D NMR spectral data; poor spectral resolution or missing experiments (heteronuclear or homonuclear) will reduce the reliability of feature correlation.
- The method is most effective for large sample sets; small sample cohorts may not yield statistically robust or biologically meaningful scaffold clustering.
- Peak correlation is dependent on NMR spectral processing parameters; inconsistent preprocessing across samples may introduce spurious correlations or miss true shared features.

## Evidence

- [readme] MADByTE allows for comparative analysis of NMR spectra from large sample sets, simultaneously, deriving shared structural features from heteronuclear and homonuclear experiments.: "MADByTE allows for comparative analysis of NMR spectra from large sample sets, simultaneously, deriving shared structural features from heteronuclear and homonuclear experiments."
- [readme] Using large sample sets, the common features between each sample can be visualized to aid in sample prioritization and structure characterization of scaffolds present.: "Using large sample sets, the common features between each sample can be visualized to aid in sample prioritization and structure characterization of scaffolds present."
- [other] Load heteronuclear (e.g., HSQC, HMBC) and homonuclear (e.g., COSY) 2D NMR spectral data for all samples in the dataset.: "Load heteronuclear (e.g., HSQC, HMBC) and homonuclear (e.g., COSY) 2D NMR spectral data for all samples in the dataset."
- [other] Generate a feature/correlation network representation that visualizes shared structural scaffolds and inter-sample relationships.: "Generate a feature/correlation network representation that visualizes shared structural scaffolds and inter-sample relationships."
- [readme] We Highly recommend installing through the included .bat script or installing manually with conda env create -f environment.yml.: "We Highly recommend installing through the included .bat script or installing manually with `conda env create -f environment.yml`."
- [readme] DO NOT INSTALL MADBYTE USING ANACONDA NAVIGATOR - IT WILL FAIL INSTALLATION.: "DO NOT INSTALL MADBYTE USING ANACONDA NAVIGATOR - IT WILL FAIL INSTALLATION."
