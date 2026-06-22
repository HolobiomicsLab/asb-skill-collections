---
name: python-workflow-execution-and-orchestration
description: Use when you have raw LC/MS data in mzML format and need to execute a complete non-targeted screening workflow to extract and annotate chemical features.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - Python >= 3.8.2
  - Python
  - pymzml
  - pandas
  - numpy
  - scipy
  - joblib
  - tqdm
  - tqdm_joblib
  - matplotlib
  - tqdm / tqdm_joblib
  - numpy / scipy
  - LAGF
derived_from:
- doi: 10.1021/acs.analchem.5c00060
  title: LAGF
evidence_spans:
- Python >= 3.8.2
- pymzml==2.5.2
- pandas==2.0.3
- numpy==1.22.4
- scipy==1.4.1
- joblib==0.15.1
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00060
  all_source_dois:
  - 10.1021/acs.analchem.5c00060
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# python-workflow-execution-and-orchestration

## Summary

Execute a multi-stage LC/MS non-targeted screening workflow implemented in Python, coordinating data loading, feature extraction, algorithmic processing, and result serialization. This skill orchestrates the LAGF algorithm pipeline on mzML-formatted mass spectrometry data using task parallelization and progress tracking.

## When to use

You have raw LC/MS data in mzML format and need to execute a complete non-targeted screening workflow to extract and annotate chemical features. Use this skill when you want to apply the LAGF algorithm as documented in the project's example notebook, with reproducible orchestration across multiple computational stages.

## When NOT to use

- Input data is not in mzML format or is already a processed feature table
- Raw LC/MS data has missing or corrupted mzML structure that pymzml cannot parse
- Workflow execution environment lacks Python >= 3.8.2 or required dependency versions

## Inputs

- LC/MS raw data file in mzML format
- LAGF algorithm configuration (as defined in example.ipynb)
- Python environment with dependencies installed (Python >= 3.8.2)

## Outputs

- Screening results output containing detected features
- Feature annotations and metadata
- Pandas DataFrame with extracted chemical features

## How to apply

Load the raw LC/MS data file in mzML format using pymzml. Execute the LAGF algorithm workflow as defined in the example.ipynb file, which applies the non-targeted screening pipeline to extract and annotate features from the mass spectrometry data. Use joblib for parallel task execution and tqdm/tqdm_joblib to monitor progress across batches. Collect detected features and their annotations into a structured output table (pandas DataFrame) and save results to disk. Verify workflow completion by checking that output feature table contains expected columns and row counts match algorithmic expectations.

## Related tools

- **pymzml** (Load and parse LC/MS data in mzML format for pipeline input)
- **joblib** (Manage parallel task execution across feature extraction batches)
- **tqdm / tqdm_joblib** (Display progress bars during workflow execution and parallelized screening)
- **pandas** (Construct and manipulate feature annotation tables; serialize results)
- **numpy / scipy** (Numerical computation and statistical operations within LAGF algorithm)
- **matplotlib** (Visualize screening results and intermediate feature distributions)
- **LAGF** (Core non-targeted screening algorithm for LC/MS feature extraction and annotation) — github.com/zsspython/LAGF

## Evaluation signals

- Output feature table is a valid pandas DataFrame with rows for each detected feature and columns for m/z, retention time, and annotations
- Total number of extracted features is consistent with expected algorithm behavior on the input dataset
- All mzML records processed without parsing errors reported by pymzml
- Workflow completion time is reasonable given input file size and available CPU cores (joblib parallelization verified)
- Output file is successfully written to disk and can be read back without data loss or schema violations

## Limitations

- Algorithm performance and feature detection quality depend on LC/MS data quality and instrument calibration; low-quality spectra may yield sparse or unreliable annotations
- Requires sufficient system memory to hold the complete mzML file in RAM during processing (no streaming mode documented)
- Parallelization overhead via joblib may not yield speedup for very small input files
- No changelog or version history provided; dependency versions are pinned to development environment (joblib==0.15.1, scipy==1.4.1, etc.), and older/newer versions are untested

## Evidence

- [other] Load LC/MS data file in mzML format; execute LAGF algorithm; generate output with detected features and annotations: "1. Load the LC/MS data file in mzML format using pymzml. 2. Execute the LAGF algorithm workflow as defined in example.ipynb, applying the non-targeted screening pipeline to extract and annotate"
- [readme] LAGF is described as a non-targeted screening tool for LC/MS data: "LAGF
LC/MS data non-targeted screening tools"
- [readme] Workflow is documented in the example.ipynb notebook: "The LAGF algorithm workflow is shown in the file "example.inpynb""
- [readme] Python >= 3.8.2 is required; specific dependency versions are listed: "Python >= 3.8.2
-joblib==0.15.1
-matplotlib==3.1.3
-numpy==1.22.4
-pandas==2.0.3
-pymzml==2.5.2
-scipy==1.4.1
-tqdm==4.45.0
-tqdm_joblib==0.0.3"
