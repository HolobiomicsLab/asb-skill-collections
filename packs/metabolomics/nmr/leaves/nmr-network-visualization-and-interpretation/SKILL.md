---
name: nmr-network-visualization-and-interpretation
description: 'Use when you have 2D NMR spectra (heteronuclear: HSQC, HMBC;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3520
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

# NMR Network Visualization and Interpretation

## Summary

This skill uses MADByTE to generate feature/correlation network representations from comparative 2D NMR analysis, enabling visualization of shared structural scaffolds and inter-sample relationships across large heterogeneous natural product mixtures. The resulting network supports rapid sample prioritization and structural annotation of complex mixtures.

## When to use

You have 2D NMR spectra (heteronuclear: HSQC, HMBC; homonuclear: COSY) from multiple samples in a natural products library or mixture series, and you need to identify and visualize common structural features across samples to prioritize samples for detailed structure elucidation or to characterize common scaffold structures present in the collection.

## When NOT to use

- You have only 1D NMR spectra or a single 2D experiment per sample; the comparative network requires multiple samples with multiple orthogonal 2D experiments to derive meaningful correlation structure.
- Your samples are already well-characterized with known structures; network-based structural discovery is most valuable for uncharacterized or structurally diverse natural product mixtures.
- You need absolute peak-by-peak chemical shift assignments rather than relative feature correlation; MADByTE prioritizes inter-sample feature matching over chemical shift calibration.

## Inputs

- Heteronuclear 2D NMR spectra (HSQC, HMBC) in standard spectral format
- Homonuclear 2D NMR spectra (COSY) in standard spectral format
- Sample metadata or identifiers for cohort association

## Outputs

- Feature/correlation network graph (node-edge representation)
- Network adjacency matrix or graph serialization format
- Network visualization file suitable for downstream graph analysis tools
- Sample prioritization ranking based on network connectivity

## How to apply

After running MADByTE's comparative analysis pipeline on loaded heteronuclear and homonuclear 2D NMR spectral data, the pipeline identifies and correlates common peaks across all samples. The workflow then generates a feature/correlation network representation—a graph where nodes represent structural features and edges represent inter-sample correlations—which is exported in a structured format (graph or adjacency representation). This network visualization directly maps shared spectroscopic signatures to sample relationships, allowing practitioners to inspect node degree and clustering patterns to identify frequently occurring structural motifs and to rank samples by their connectivity to prioritize those with novel or hub-like structural features.

## Related tools

- **MADByTE** (Core platform that executes comparative 2D NMR analysis, identifies common peaks across samples, and generates the feature/correlation network representation) — https://github.com/liningtonlab/madbyte
- **conda** (Environment and dependency manager; required to activate the MADByTE Python virtual environment before executing the launcher script)
- **Python** (Runtime language in which MADByTE is implemented; user runs the launcher script (madbyte_gui.py) under the activated conda environment)

## Examples

```
conda activate madbyte && python madbyte_gui.py
```

## Evaluation signals

- Network graph has non-trivial connected component structure (multiple nodes with degree > 1); isolated nodes suggest insufficient spectral overlap or data quality issues.
- Exported adjacency matrix is symmetric (undirected graph) and contains only entries in the range [0, 1] if similarity-weighted, or binary {0, 1} if presence/absence; check for malformed or out-of-range values.
- Sample clustering in the network aligns with known phylogenetic or chemical classification of the natural products library; if major taxonomic groups are randomly scattered, re-examine peak correlation thresholds.
- High-degree hub nodes correspond to abundant or common structural scaffolds (e.g., ubiquitous core ring systems); interpret isolated or low-degree nodes as unique or rare structural variants.
- Network visualization renders without overlapping node labels and maintains interpretable edge density (neither fully connected nor disconnected); degree distribution should be right-skewed rather than uniform.

## Limitations

- MADByTE's peak correlation relies on spectral quality and preprocessing; poor-quality spectra, severe baseline distortion, or mis-phased 2D experiments will degrade feature matching and network topology.
- The network is relative and qualitative: it reflects inter-sample similarity patterns but does not quantify absolute structural confidence or provide chemical shift calibration; validation requires independent NMR or MS-based structure confirmation.
- Large sample sets may generate dense networks that are difficult to interpret visually; clustering or community detection post-processing (not part of MADByTE's default output) may be necessary.
- Heteronuclear experiments (HSQC, HMBC) are sensitive to solvent and salt composition; samples prepared under different conditions may show spurious correlations or missing features unrelated to structure.

## Evidence

- [readme] MADByTE allows for comparative analysis of NMR spectra from large sample sets, simultaneously, deriving shared structural features from heteronuclear and homonuclear experiments.: "MADByTE allows for comparative analysis of NMR spectra from large sample sets, simultaneously, deriving shared structural features from heteronuclear and homonuclear experiments."
- [readme] Using large sample sets, the common features between each sample can be visualized to aid in sample prioritization and structure characterization of scaffolds present.: "Using large sample sets, the common features between each sample can be visualized to aid in sample prioritization and structure characterization of scaffolds present."
- [other] Generate a feature/correlation network representation that visualizes shared structural scaffolds and inter-sample relationships.: "Generate a feature/correlation network representation that visualizes shared structural scaffolds and inter-sample relationships."
- [other] Run the MADByTE launcher script to execute the comparative analysis pipeline, which identifies and correlates common peaks across samples.: "Run the MADByTE launcher script to execute the comparative analysis pipeline, which identifies and correlates common peaks across samples."
- [other] Export the network as a structured output file (graph or adjacency format) suitable for downstream visualization and interpretation.: "Export the network as a structured output file (graph or adjacency format) suitable for downstream visualization and interpretation."
