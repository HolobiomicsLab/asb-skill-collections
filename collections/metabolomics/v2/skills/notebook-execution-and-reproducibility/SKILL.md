---
name: notebook-execution-and-reproducibility
description: Use when when you have access to a peer-reviewed manuscript with an accompanying interactive notebook and public data repository, and you need to verify that the published figures can be regenerated from the original data through the documented processing pipeline, or when you want to reuse the.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3934
  tools:
  - Google Colab
  - Python 3
  - MetaboLights
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

# notebook-execution-and-reproducibility

## Summary

Execute an interactive Jupyter/Colab notebook to reproduce published manuscript figures from deposited spatio-molecular matrices and downstream processing pipelines. This skill validates computational reproducibility by running the complete analysis workflow and comparing generated outputs to published results.

## When to use

When you have access to a peer-reviewed manuscript with an accompanying interactive notebook and public data repository, and you need to verify that the published figures can be regenerated from the original data through the documented processing pipeline, or when you want to reuse the exact analytical steps on new but structurally similar data.

## When NOT to use

- The notebook contains proprietary or closed-source code that cannot be executed in your environment.
- The deposited datasets are incomplete, corrupted, or no longer accessible.
- Your input data has a fundamentally different structure or scale than the manuscript examples, requiring custom parameter tuning beyond running the notebook as-is.

## Inputs

- Spatio-molecular matrices in CSV or structured format (e.g., MORPHnMOL.csv from SpaceM)
- Interactive Jupyter or Google Colab notebook with complete downstream processing code
- Manuscript with published figure images and numerical results for comparison

## Outputs

- Replicated manuscript figures (plots, heatmaps, scatter plots in image format)
- Processed data tables and feature matrices produced by the pipeline
- Execution log documenting cell runtimes and any warnings or errors

## How to apply

First, locate and access the deposited datasets via the provided repository link (e.g., MetaboLights for spatio-molecular matrices). Download the data into a local or cloud environment. Open the interactive notebook (hosted on Google Colab or equivalent) and load the downloaded datasets as input structures matching the notebook's expected schema. Execute all notebook cells sequentially without modification, running the full downstream processing pipeline including data transformation, feature extraction, and visualization steps. Monitor execution for errors and verify that generated figures and processed data tables match the published manuscript outputs in both visual appearance and numerical values. Save outputs and document any deviations from expected results.

## Related tools

- **Google Colab** (Cloud-based interactive notebook environment for executing the SpaceM downstream processing pipeline without local installation) — https://colab.research.google.com/
- **Python 3** (Programming language runtime required to execute all notebook cells and data processing functions)
- **MetaboLights** (Public repository for depositing and accessing spatio-molecular matrices and related datasets) — https://www.ebi.ac.uk/metabolights/

## Examples

```
# 1. Access MetaboLights and download spatio-molecular matrices (reviewer417760fcbfbb6076b4ce5bd9a7e7c893)
# 2. Open https://colab.research.google.com/drive/1CKdHDUkGIpAcBzrSfuCodMF_l2xbVAKT?usp=sharing
# 3. Upload downloaded MORPHnMOL.csv
# 4. Run all cells sequentially; output figures appear in notebook and MORPHnMOL.csv is saved to scAnalysis/
```

## Evaluation signals

- All notebook cells execute without exceptions or raise only expected, documented warnings.
- Generated figures are visually identical to published manuscript figures (same layout, color scheme, axis ranges, and data point distributions).
- Processed data tables match published numerical values within expected floating-point precision (typically < 1e-10 relative error for deterministic operations).
- Output file paths and naming conventions match documentation (e.g., final matrix saved as MORPHnMOL.csv in scAnalysis subfolder).
- Execution completes within documented time budget (README states 'installation time is less than one hour').

## Limitations

- Notebook execution assumes the exact software versions specified in requirements.txt are installed; dependency version drift may cause silent numerical differences or runtime errors.
- The notebook is optimized for the specific data structure and file formats produced by SpaceM (spatio-molecular matrices); applying it to differently structured metabolomics data requires manual adaptation.
- Reproducibility is limited to the exact analytical workflow documented in the notebook; downstream analyses or parameter variations are outside the scope of this skill.
- Google Colab execution may be rate-limited or subject to session timeouts for large datasets, requiring the user to checkpoint and restart execution.

## Evidence

- [readme] we [present interactively using Google Collab](https://colab.research.google.com/drive/1CKdHDUkGIpAcBzrSfuCodMF_l2xbVAKT?usp=sharing) the downstream processing of the spatio-molecular matrices provided by SpaceM and replicate all main figures of the manuscript.: "present interactively using Google Collab the downstream processing of the spatio-molecular matrices provided by SpaceM and replicate all main figures of the manuscript"
- [other] Execute all notebook cells sequentially, running the downstream processing pipeline including data transformation, feature extraction, and visualization steps.: "Execute all notebook cells sequentially, running the downstream processing pipeline including data transformation, feature extraction, and visualization steps"
- [readme] The SpaceM datasets presented in the manuscript are available on [MetaboLights](https://www.ebi.ac.uk/metabolights/reviewer417760fcbfbb6076b4ce5bd9a7e7c893).: "The SpaceM datasets presented in the manuscript are available on [MetaboLights]"
- [readme] The final spatio-molecular matrix will be stored as `MORPHnMOL.csv` and can be found inside the `scAnalysis` sub-folder.: "The final spatio-molecular matrix will be stored as `MORPHnMOL.csv` and can be found inside the `scAnalysis` sub-folder"
- [other] The Google Colab notebook interactively presents downstream processing of spatio-molecular matrices provided by SpaceM and replicates all main figures of the manuscript.: "The Google Colab notebook interactively presents downstream processing of spatio-molecular matrices provided by SpaceM and replicates all main figures of the manuscript"
