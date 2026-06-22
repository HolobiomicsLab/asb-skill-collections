---
name: metabolomics-dataset-handling-massive
description: Use when you are beginning a non-targeted metabolomics analysis and need to source raw LC-MS/MS data files (in mzML or NetCDF format) that have been vetted for quality and are known to support FBMN and statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3500
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - R
  - MassIVE
  - MZmine3
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1038/s41596-024-01046-3
  title: FBMN-STATS
evidence_spans:
- To easily install and run Jupyter Notebook in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fbmn_stats_cq
    doi: 10.1038/s41596-024-01046-3
    title: FBMN-STATS
  dedup_kept_from: coll_fbmn_stats_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41596-024-01046-3
  all_source_dois:
  - 10.1038/s41596-024-01046-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomics-dataset-handling-massive

## Summary

Retrieve, organize, and validate non-targeted LC-MS/MS metabolomics datasets from the MassIVE repository for use in feature-based molecular network and multivariate statistical analysis workflows. This skill ensures data integrity and reproducibility by following standardized dataset selection and download protocols.

## When to use

You are beginning a non-targeted metabolomics analysis and need to source raw LC-MS/MS data files (in mzML or NetCDF format) that have been vetted for quality and are known to support FBMN and statistical analysis. Specifically, when you want to reproduce published results or validate a multivariate statistical analysis pipeline against reference datasets with known expected outputs.

## When NOT to use

- You already have processed feature tables or pre-aligned data in hand — dataset retrieval is not needed.
- Your analysis requires targeted MS/MS data or ion chromatography formats not available in the MassIVE public repository.
- You are working with proprietary or restricted-access datasets that are not published in MassIVE.

## Inputs

- MassIVE dataset identifier (e.g., MSV000082312)
- Raw LC-MS/MS data files (mzML or NetCDF format)
- Sample metadata file (if provided in MassIVE repository)

## Outputs

- Organized local dataset directory with raw LC-MS/MS files
- Sample-to-file mapping document
- Batch and blank sample annotations
- Verification report confirming dataset completeness

## How to apply

Navigate to the MassIVE repository and identify publicly archived non-targeted LC-MS/MS datasets that match your analysis scope (e.g., MSV000082312 or MSV000085786 for FBMN-STATS validation). Download the raw data files and any associated metadata (sample annotations, batch information, blank sample designations). Organize the files in a local directory structure that preserves sample-to-file mappings and batch groupings. Before proceeding to feature detection, verify that the dataset contains the expected number of samples, includes blank/quality control samples for quality assessment, and that file formats are compatible with your downstream processing tool (e.g., MZmine3). Cross-reference your downloaded dataset against published result files or a reference Google Drive folder to confirm completeness.

## Related tools

- **MassIVE** (Public repository for archiving and retrieving non-targeted LC-MS/MS metabolomics datasets with DOI and standardized metadata) — https://massive.ucsd.edu/
- **MZmine3** (Subsequent feature detection and alignment tool; expects raw data files downloaded from MassIVE as input)

## Evaluation signals

- Downloaded files are present in the local directory and match the dataset size reported in MassIVE metadata.
- File format check: all raw data files are in mzML or NetCDF format and open without errors in MZmine3.
- Sample count matches expected number (e.g., test datasets typically contain 10–30 samples including blanks).
- Blank and quality control samples are correctly labeled and segregated in the sample metadata.
- When reproduced against reference outputs, the complete dataset produces the same number of features and statistical results as published reference files in the associated Google Drive.

## Limitations

- MassIVE datasets are public and may be updated or archived; confirm dataset availability and versioning before publishing results.
- Not all metabolomics datasets in MassIVE are formatted or annotated consistently; datasets from GNPS Quickstart versions prior to GNPS 2 may generate incorrect feature tables and require reformatting.
- Large datasets (>100 samples or >100 GB) may require significant local storage and bandwidth; cloud-based execution (e.g., Google Colab) has a 77 GB disk limit per user session.
- Raw data files do not include pre-computed metadata such as retention time or mass calibration; these must be inferred during feature detection.

## Evidence

- [readme] MASSIVE Datasets from which all the files were selected for MZmine3: MSV000082312 and MSV000085786: "MASSIVE Datasets from which all the files were selected for MZmine3: [MSV000082312](https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?task=8a8139d9248b43e0b0fda17495387756) and [MSV000085786]"
- [other] Download the test dataset (MSV000082312 or MSV000085786) from MassIVE.: "Download the test dataset (MSV000082312 or MSV000085786) from MassIVE."
- [readme] The result files of the notebook can be found in the Google Drive: [Google Drive Link for the files]: "The result files of the notebook can be found in the Google Drive: [Google Drive Link for the files]"
- [readme] For GNPS Quickstart Users: Quickstart GNPS 2 Recommendation: We advise Quickstart GNPS users to switch to the latest GNPS 2 for FBMN-STATS and accessing the Notebooks. The previous version of Quickstart GNPS does not generate the reformatted output needed for Notebook/Web app integration, leading to incorrect feature tables.: "The previous version of Quickstart GNPS does not generate the reformatted output needed for Notebook/Web app integration, leading to incorrect feature tables."
- [readme] Although Colab is easier to use and is all Cloud-based, the main problem with the Colab environment is when you leave the Colab notebook idle for 90 mins or continuously used it for 12 hours, the runtime will automatically disconnect.: "the main problem with the Colab environment is when you leave the Colab notebook idle for 90 mins or continuously used it for 12 hours, the runtime will automatically disconnect."
