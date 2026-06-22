---
name: metabolomics-data-downstream-analysis
description: Use when you have deposited spatio-molecular matrices (e.g., MORPHnMOL.csv from SpaceM analysis) and need to reproduce or extend the data transformations, feature extractions, and figure generation reported in a metabolomics manuscript.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Google Colab
  - Python 3
  - CellProfiler 3.0.0
  - Fiji
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41592-021-01198-0
  all_source_dois:
  - 10.1038/s41592-021-01198-0
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-data-downstream-analysis

## Summary

Downstream processing of spatio-molecular matrices from single-cell metabolomics to extract features, transform data, and generate publication-quality visualizations that replicate manuscript figures. This skill bridges raw MALDI-imaging mass spectrometry and microscopy outputs into interpretable cell-level metabolic profiles.

## When to use

You have deposited spatio-molecular matrices (e.g., MORPHnMOL.csv from SpaceM analysis) and need to reproduce or extend the data transformations, feature extractions, and figure generation reported in a metabolomics manuscript. Use this skill when you want to validate the reproducibility of published results or apply the same visualization pipeline to new spatio-molecular data.

## When NOT to use

- Input data is raw MALDI-imaging mass spectrometry files (.RAW, .imzML) or microscopy tiles — use SpaceM upstream processing (cell segmentation, ablation mark detection, image stitching) first to generate spatio-molecular matrices.
- Goal is method development or algorithm optimization — this skill applies a fixed, published pipeline; it is not designed for parameter tuning or novel method exploration.
- Data lacks spatial context or cell-level segmentation — the skill requires pre-segmented cell identities linked to both morphological features and molecular measurements.

## Inputs

- Spatio-molecular matrix (CSV format, rows=cells, columns=morphological + metabolite features)
- Deposited dataset from MetaboLights repository (e.g., reviewer ID or DOI)
- Google Colab notebook URL or local Python 3 environment with dependencies installed

## Outputs

- Processed data tables (CSV) with transformed features and aggregated statistics
- Publication-quality figures (PNG, PDF) replicating manuscript plots
- Intermediate feature matrices (e.g., PCA loadings, clustering assignments)

## How to apply

Load the spatio-molecular matrix (CSV format containing morphological and molecular features indexed by cell ID) into a Python 3 environment via Google Colab or local Jupyter notebook. Execute the downstream processing pipeline sequentially: (1) import and validate the matrix structure; (2) apply data transformations (e.g., normalization, scaling, or log transformation as specified in the notebook); (3) perform feature extraction and dimensionality reduction steps (e.g., PCA, clustering); (4) generate publication-quality figures through matplotlib/seaborn visualization routines that map metabolic and morphological features to spatial or statistical plots. The notebook cells are designed to be run in order, with intermediate outputs (processed tables, feature matrices, figures) saved at each step. Verify correctness by comparing generated figures against the published manuscript figures pixel-by-pixel or by checking that output dimensions and summary statistics match expected values.

## Related tools

- **Google Colab** (Interactive notebook environment for running Python 3 downstream processing pipeline with pre-installed dependencies and cloud storage integration) — https://colab.research.google.com/
- **Python 3** (Programming language for data transformation, feature extraction, and visualization routines in the downstream processing pipeline)
- **CellProfiler 3.0.0** (Upstream image segmentation tool (not directly used in this skill but required to generate input spatio-molecular matrices)) — https://cellprofiler.org/previous_releases/
- **Fiji** (Upstream image registration and preprocessing tool (not directly used in this skill but required to generate input spatio-molecular matrices)) — https://imagej.net/Fiji/Downloads

## Examples

```
# In Google Colab: open notebook at https://colab.research.google.com/drive/1CKdHDUkGIpAcBzrSfuCodMF_l2xbVAKT?usp=sharing, download MORPHnMOL.csv from MetaboLights reviewer417760fcbfbb6076b4ce5bd9a7e7c893, upload to Colab, then execute cells sequentially to generate and display figures.
```

## Evaluation signals

- All output figures visually match published manuscript figures in layout, color scheme, and data representation.
- Output CSV files contain expected number of rows (cells) and columns (morphological + metabolite features) with no missing values in key columns.
- Summary statistics (mean, median, standard deviation of key features) fall within documented ranges or match values reported in manuscript tables.
- Notebook executes without errors or warnings when cells are run sequentially, indicating data schema and dependency compatibility.
- Intermediate outputs (e.g., PCA variance explained, clustering silhouette scores) align with values reported in manuscript methods or supplementary materials.

## Limitations

- Pipeline is optimized for the specific SpaceM output format (MORPHnMOL.csv); adaptation required if input matrix structure or column names differ.
- Reproducibility depends on matching Python package versions specified in requirements.txt; environment drift or newer package versions may alter numerical outputs or visualizations slightly.
- Google Colab execution may fail or be slow if the spatio-molecular matrix exceeds available RAM; local installation may be necessary for very large datasets.
- Figure generation relies on exact parameter values (e.g., colormap, marker size, axis limits) hardcoded in the notebook; customization requires manual notebook editing.
- No interactive validation or error recovery built into the pipeline; silent failures in intermediate steps may propagate to final figures without alerting the user.

## Evidence

- [intro] the downstream processing of the spatio-molecular matrices provided by SpaceM: "the downstream processing of the spatio-molecular matrices provided by SpaceM"
- [other] downstream processing pipeline including data transformation, feature extraction, and visualization steps: "Execute all notebook cells sequentially, running the downstream processing pipeline including data transformation, feature extraction, and visualization steps."
- [other] replicates all main figures of the manuscript: "The Google Colab notebook interactively presents downstream processing of spatio-molecular matrices provided by SpaceM and replicates all main figures of the manuscript."
- [other] Download the deposited spatio-molecular matrices: "Access the MetaboLights repository (reviewer417760fcbfbb6076b4ce5bd9a7e7c893) and download the deposited SpaceM spatio-molecular matrices."
- [readme] The final spatio-molecular matrix will be stored as MORPHnMOL.csv: "The final spatio-molecular matrix will be stored as `MORPHnMOL.csv` and can be found inside the `scAnalysis` sub-folder."
- [readme] we present interactively using Google Collab the downstream processing: "we [present interactively using Google Collab](https://colab.research.google.com/drive/1CKdHDUkGIpAcBzrSfuCodMF_l2xbVAKT?usp=sharing) the downstream processing of the spatio-molecular matrices"
