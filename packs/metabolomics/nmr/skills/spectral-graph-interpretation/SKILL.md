---
name: spectral-graph-interpretation
description: Use when after submitting MS/MS data and feature tables to GNPS and receiving a molecular networking job result.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0602
  tools:
  - MZmine2
  - GNPS
  - Cytoscape
  - Jupyter notebook
  - R
  techniques:
  - LC-MS
  - NMR
derived_from:
- doi: 10.1021/acs.jnatprod.7b00737
  title: Bioactivity-Based Molecular Networking
evidence_spans:
- open bioinformatic tools, such [MZmine2](http://mzmine.github.io/)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bioactivity_based_molecular_networking_cq
    doi: 10.1021/acs.jnatprod.7b00737
    title: Bioactivity-Based Molecular Networking
  dedup_kept_from: coll_bioactivity_based_molecular_networking_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jnatprod.7b00737
  all_source_dois:
  - 10.1021/acs.jnatprod.7b00737
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-graph-interpretation

## Summary

Interpret the node and edge tables output by GNPS molecular networking to extract compound annotations, spectral similarity relationships, and bioactive molecular families. This skill bridges the computational graph output to biological interpretation for natural product discovery and bioassay-guided fractionation workflows.

## When to use

After submitting MS/MS data and feature tables to GNPS and receiving a molecular networking job result. Specifically: when you have retrieved the node table (compounds/spectra) and edge table (spectral similarity links) from GNPS output and need to map these back to detected LC-MS features, bioassay activity, or downstream structural elucidation steps.

## When NOT to use

- Input is raw LC-MS/MS data files (mzML, raw) that have not yet been processed through feature detection and GNPS submission — use feature detection and GNPS submission skills first.
- You lack bioassay activity data and are performing untargeted metabolomics without bioassay guidance — spectral graph interpretation is optimized for bioactive molecular networks that integrate activity data; standard molecular networking alone does not require this integration step.
- The GNPS job failed or produced empty node/edge tables due to insufficient spectral library matches or misconfiguration — verify GNPS job status and parameters before attempting interpretation.

## Inputs

- GNPS node table (CSV or TSV containing compound/spectrum identifiers and metadata)
- GNPS edge table (CSV or TSV containing spectral similarity scores and edge weights)
- Feature quantification matrix (features_quantification_matrix.csv with aligned intensities across fractions)
- Bioassay activity data (binary or continuous activity scores aligned to fractions/features)

## Outputs

- Annotated molecular network graph (Cytoscape session file or exported network format)
- Filtered edge list with spectral similarity thresholds applied
- Node table annotated with bioassay activity and putative compound annotations
- Bioactive molecular family clusters (nodes grouped by spectral similarity and activity correlation)

## How to apply

Retrieve the node table (containing compound/spectrum identifiers and putative annotations from MS/MS library matching) and edge table (containing pairwise spectral similarity scores and cosine-derived edge weights) from the GNPS platform output. Load these tables into a visualization tool such as Cytoscape (minimum version 3.4) to construct the molecular network graph. Filter edges using the spectral similarity thresholds configured during GNPS submission (typically cosine similarity > 0.7 and parent mass difference within configured tolerance, e.g. 5 ppm). Map detected bioassay activity (from Step 1 bioassay data) onto nodes using feature intensity quantification tables, allowing identification of bioactive molecular families. Export or annotate nodes with putative compound identifications derived from GNPS MS/MS library matching against available spectral databases. Use the resulting annotated, filtered network for downstream hypothesis generation (e.g., structural families of interest, novel bioactive scaffolds).

## Related tools

- **GNPS** (Generate spectral similarity graphs (node and edge tables) via MS/MS library matching and molecular networking computation) — http://gnps.ucsd.edu
- **Cytoscape** (Visualize and filter the molecular network graph; map bioassay activity and annotations onto nodes; minimum version 3.4) — http://www.cytoscape.org/
- **Jupyter notebook** (Execute reproducible downstream analysis: correlate bioassay activity with node intensities, perform statistical filtering, generate visualizations) — http://jupyter.org/
- **R** (Statistical analysis of bioassay-spectral similarity correlations; network topology analysis; data wrangling) — https://www.r-project.org/

## Evaluation signals

- Node table contains entries for all features with MS/MS data; edge table cosine similarity scores range from 0–1 with majority of retained edges > threshold (0.7 typical)
- Bioassay activity successfully maps onto network nodes; nodes with highest activity form recognizable molecular families (clusters of high spectral similarity)
- Putative annotations (from GNPS MS/MS matching) align with expected natural product chemical classes or known bioactive scaffolds in literature
- Network topology is connected or shows interpretable subclusters; isolated nodes or highly fragmented networks suggest GNPS parameter misconfiguration or insufficient spectral library coverage
- Edge filtering reproducibly removes low-confidence similarity links; final network size and density match those reported in publications using similar thresholds and datasets

## Limitations

- MS/MS validation of putative annotations is not provided in the GNPS output alone; MS/MS library matching assigns annotations only to level 2 (putatively annotated compounds) by Metabolomics Standards Initiative standards; structural confirmation requires additional NMR or authentic standards.
- Spectral similarity does not imply structural similarity or bioactivity relationship; spectral clustering can group chemically distinct compounds with similar fragmentation patterns, and bioactive molecular families must be validated experimentally.
- GNPS molecular networking depends on MS/MS spectral library coverage; features without known library matches appear as unannotated nodes, potentially excluding novel bioactive compounds from initial interpretation.
- Bioassay data quality and alignment are critical; misalignment between feature intensities and bioassay measurements (e.g., incorrect fraction labeling) will produce spurious activity-network correlations.

## Evidence

- [other] Retrieve the resulting node table (compounds/spectra) and edge table (spectral similarity links) from GNPS output.: "Retrieve the resulting node table (compounds/spectra) and edge table (spectral similarity links) from GNPS output."
- [readme] The list of molecules of interest can be directly exported from GNPS as a result of MS/MS matching against spectral libraries available at GNPS.: "The list of molecules of interest can be directly exported from GNPS as a result of MS/MS matching against spectral libraries"
- [readme] This implements a molecular identification at the level putatively annotated compounds, corresponding to the level 2 of the Metabolomics Standards Initiative: "This implements a molecular identification at the level putatively annotated compounds, corresponding to the level 2 of the Metabolomics Standards Initiative"
- [readme] You will need to install Cytoscape (minimum version 3.4).: "You will need to install Cytoscape (minimum version 3.4)."
- [intro] integrates MS/MS molecular networking and bioassay-guided fractionation into the concept of bioactive molecular networking: "integrates MS/MS molecular networking and bioassay-guided fractionation into the concept of bioactive molecular networking"
