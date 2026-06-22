---
name: spectral-feature-extraction-and-annotation
description: Use when you have raw LC/MS data in mzML format and need to perform non-targeted screening to discover unknown chemical features without a predefined list of target compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - pymzml
  - pandas
  - numpy
  - scipy
  - joblib
  - tqdm
  - tqdm_joblib
  - matplotlib
  - tqdm and tqdm_joblib
  - pandas, numpy, scipy
derived_from:
- doi: 10.1021/acs.analchem.5c00060
  title: LAGF
evidence_spans:
- pymzml==2.5.2
- pandas==2.0.3
- numpy==1.22.4
- scipy==1.4.1
- joblib==0.15.1
- tqdm==4.45.0
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lagf_cq
    doi: 10.1021/acs.analchem.5c00060
    title: LAGF
  dedup_kept_from: coll_lagf_cq
schema_version: 0.2.0
---

# spectral-feature-extraction-and-annotation

## Summary

Extract and annotate chemical features from untargeted LC/MS data using the LAGF algorithm, which identifies ion signals and associates them with potential molecular identities for screening and discovery workflows.

## When to use

You have raw LC/MS data in mzML format and need to perform non-targeted screening to discover unknown chemical features without a predefined list of target compounds. Apply this skill when you want to detect all significant ion signals across retention time and m/z dimensions and annotate them with chemical information.

## When NOT to use

- Input is already a processed feature table or peak list — LAGF is designed for raw mzML data, not pre-extracted features
- Targeted analysis with a predefined compound list is required — LAGF performs non-targeted screening and may not prioritize known compounds efficiently

## Inputs

- LC/MS data in mzML format
- Raw mass spectrometry file

## Outputs

- Feature table with detected m/z and retention time pairs
- Annotated features with chemical metadata
- Screening results output containing detected features and annotations

## How to apply

Load the LC/MS data file in mzML format using pymzml, then execute the LAGF algorithm workflow as documented in example.ipynb. The workflow applies a non-targeted screening pipeline that extracts feature signals across the full mass spectrometry dataset, associates detected m/z and retention time pairs with feature metadata, and generates annotations for each feature. The process uses parallel processing (joblib) with progress tracking (tqdm) to handle large datasets efficiently. Verify success by confirming the output contains a feature table with detected m/z values, retention times, and associated annotations.

## Related tools

- **pymzml** (Parse and load LC/MS data in mzML format for downstream LAGF processing)
- **joblib** (Enable parallel execution of feature extraction across large LC/MS datasets)
- **tqdm and tqdm_joblib** (Provide progress tracking and monitoring during algorithm execution)
- **pandas, numpy, scipy** (Perform numerical computations, array operations, and statistical analysis on spectral data)
- **matplotlib** (Visualize extracted features and screening results)

## Evaluation signals

- Output feature table is non-empty and contains columns for m/z, retention time, and feature annotations
- All detected features have valid m/z values (positive numbers) and retention times within the LC/MS run duration
- No missing or NaN values in core feature annotation fields
- Feature count is consistent with the complexity of the input LC/MS data (e.g., presence of multiple compounds produces proportionally more features)
- Annotations are populated for detected features, indicating successful linking to chemical metadata

## Limitations

- Workflow documentation relies on example.ipynb; no formal changelog or version history is provided in the repository
- Dependency versions are pinned to specific releases (e.g., numpy==1.22.4, pandas==2.0.3) and compatibility with substantially different versions is untested
- Algorithm performance and feature annotation accuracy are dependent on input data quality and LC/MS instrument calibration

## Evidence

- [readme] LC/MS data non-targeted screening tool performing feature extraction and annotation: "LC/MS data non-targeted screening tools"
- [other] mzML format is the required input file format for the workflow: "Load the LC/MS data file in mzML format using pymzml"
- [readme] The LAGF algorithm workflow is documented in the example.ipynb notebook: "The LAGF algorithm workflow is shown in the file "example.inpynb""
- [other] The workflow generates detected features and their annotations as primary outputs: "Generate and save the screening results output containing detected features and their annotations"
- [readme] Specific Python versions and pinned dependencies are required for reproducibility: "The list below is the version of Python dependencies used when developing the algorithm. Older versions might still work but are untested."
