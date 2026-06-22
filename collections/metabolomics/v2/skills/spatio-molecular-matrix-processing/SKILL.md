---
name: spatio-molecular-matrix-processing
description: Use when you have deposited SpaceM spatio-molecular matrices (MORPHnMOL.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2945
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - Google Colab
  - Python 3
  - MetaboLights repository
  - SpaceM GitHub repository
derived_from:
- doi: 10.1038/s41592-021-01198-0
  title: SpaceM
evidence_spans:
- we [present interactively using Google Collab](https://colab.research.google.com/drive/1CKdHDUkGIpAcBzrSfuCodMF_l2xbVAKT?usp=sharing)
- We support `python3`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spacem_cq
    doi: 10.1038/s41592-021-01198-0
    title: SpaceM
  dedup_kept_from: coll_spacem_cq
schema_version: 0.2.0
---

# spatio-molecular-matrix-processing

## Summary

Downstream processing and analysis of spatio-molecular matrices produced by SpaceM (single-cell metabolomics integrated with MALDI-imaging mass spectrometry) to extract metabolic features, perform dimensionality reduction, and generate publication-ready visualizations. This skill transforms the raw spatio-molecular matrix (MORPHnMOL.csv) into interpretable figures and processed data tables.

## When to use

You have deposited SpaceM spatio-molecular matrices (MORPHnMOL.csv) from single-cell metabolomics experiments and need to replicate or extend the downstream analysis pipeline to generate main figures, perform feature extraction, apply data transformation, and produce comparative visualizations across cell populations or experimental conditions.

## When NOT to use

- Raw MALDI-imaging mass spectrometry files (.RAW, .imzML, .ibd) that have not yet been processed to produce spatio-molecular matrices—use the full SpaceM pipeline (CellProfiler segmentation, METASPACE annotation, matrix assembly) instead.
- Pre-stitched microscopy images without cell segmentation or ablation mark detection—the downstream processing assumes cell-level assignments and spatial coordinates are already resolved.
- If your input lacks both morphological (cell segmentation) and molecular (metabolite intensity) annotations—the spatio-molecular matrix must contain both dimensions.

## Inputs

- SpaceM spatio-molecular matrix (CSV file: MORPHnMOL.csv)
- Cell morphology and molecular annotation metadata
- Spatial coordinate information (x, y pixel or um coordinates per cell)

## Outputs

- Processed and transformed spatio-molecular data table (CSV)
- Publication-ready figures (scatter plots, heatmaps, clustering visualizations)
- Feature-extracted matrices (reduced dimensionality representations)
- Cell segmentation and metabolite assignment results

## How to apply

Load the spatio-molecular matrix CSV file into Python 3 and execute the provided interactive Google Colab notebook sequentially, which implements data transformation (normalization, scaling), feature extraction (metabolite selection, dimensionality reduction), and visualization steps (clustering plots, heatmaps, scatter plots). The notebook accepts the downloaded matrices as input data structures and applies the documented processing logic to replicate all main manuscript figures. Execute all cells in order, verify that intermediate outputs match expected shapes and value ranges at each step, and save the resulting processed data tables and output figures. The pipeline is optimized for the SpaceM output format where rows are single cells and columns are metabolite intensities with spatial coordinates.

## Related tools

- **Google Colab** (Interactive Python execution environment for running the downstream processing notebook and generating figures interactively) — https://colab.research.google.com/drive/1CKdHDUkGIpAcBzrSfuCodMF_l2xbVAKT?usp=sharing
- **Python 3** (Programming language runtime for executing the data transformation, feature extraction, and visualization pipeline)
- **MetaboLights repository** (Public data repository storing deposited spatio-molecular matrices for download and reuse) — https://www.ebi.ac.uk/metabolights/reviewer417760fcbfbb6076b4ce5bd9a7e7c893
- **SpaceM GitHub repository** (Source code repository containing the downstream processing notebook and supporting scripts) — https://github.com/alexandrovteam/SpaceM

## Evaluation signals

- All main figures from the manuscript are successfully regenerated with matching layout, data distributions, and statistical annotations.
- The processed data table preserves the original number of cells (rows) and contains expected metabolite columns with numeric intensities (no NaN or Inf values outside specified missing regions).
- Intermediate outputs at each pipeline step (after normalization, after feature selection, after dimensionality reduction) match the documented expected shapes and value ranges reported in the notebook.
- Spatial coordinate metadata remain intact and correctly linked to metabolite intensities, allowing reproduction of spatial distribution plots.
- Output CSV files are well-formed and can be re-loaded without parsing errors; figure files are generated in standard image formats and display without corruption.

## Limitations

- The downstream processing pipeline is tightly coupled to the SpaceM-specific matrix format (MORPHnMOL.csv); matrices from other single-cell metabolomics platforms or different preprocessing pipelines may require format adaptation.
- The Google Colab notebook is designed for interactive exploration and figure replication; production-scale batch processing of large numbers of matrices may require conversion to a standalone script with explicit error handling.
- The pipeline assumes that cell segmentation and metabolite-to-cell assignment have already been performed correctly upstream (via CellProfiler and METASPACE); poor segmentation or misalignment of ablation marks will propagate to and compromise downstream results.
- No changelog was found in the documentation; version compatibility and reproducibility across different releases of Python, pandas, scikit-learn, and visualization dependencies are not explicitly tracked.

## Evidence

- [readme] the downstream processing of the spatio-molecular matrices provided by SpaceM and replicate all main figures of the manuscript: "we [present interactively using Google Collab](https://colab.research.google.com/drive/1CKdHDUkGIpAcBzrSfuCodMF_l2xbVAKT?usp=sharing) the downstream processing of the spatio-molecular matrices"
- [other] Execute all notebook cells sequentially, running the downstream processing pipeline including data transformation, feature extraction, and visualization steps: "Execute all notebook cells sequentially, running the downstream processing pipeline including data transformation, feature extraction, and visualization steps."
- [readme] The final spatio-molecular matrix will be stored as MORPHnMOL.csv and can be found inside the scAnalysis sub-folder: "The final spatio-molecular matrix will be stored as `MORPHnMOL.csv` and can be found inside the `scAnalysis` sub-folder."
- [readme] We support python3. For the detailed requirements, see the file 'requirements.txt'. To install the dependencies, run: pip install -r requirements.txt: "We support `python3`. For the detailed requirements, see the file 'requirements.txt'. To install the dependencies, run: `pip install -r requirements.txt`"
- [readme] The SpaceM datasets presented in the manuscript are available on MetaboLights: "The SpaceM datasets presented in the manuscript are available on [MetaboLights](https://www.ebi.ac.uk/metabolights/reviewer417760fcbfbb6076b4ce5bd9a7e7c893)."
