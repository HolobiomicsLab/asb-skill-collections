---
name: non-targeted-feature-detection-and-screening
description: Use when you have raw LC/MS data in mzML format and your analysis goal
  is to comprehensively detect and annotate all mass spectral features present, rather
  than measuring predefined target analytes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - pymzml
  - pandas
  - numpy
  - scipy
  - joblib
  - tqdm
  - tqdm_joblib
  - matplotlib
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c00060
  all_source_dois:
  - 10.1021/acs.analchem.5c00060
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# non-targeted-feature-detection-and-screening

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

The LAGF algorithm performs non-targeted screening on LC/MS data in mzML format to automatically detect and annotate mass spectral features without prior knowledge of target compounds. This skill is essential when exploring untargeted metabolomics datasets to discover all detectable features and their characteristics.

## When to use

Apply this skill when you have raw LC/MS data in mzML format and your analysis goal is to comprehensively detect and annotate all mass spectral features present, rather than measuring predefined target analytes. Use it in discovery-phase metabolomics studies, environmental screening, or exploratory profiling where you want to extract the full feature space without a priori compound lists.

## When NOT to use

- Input is already a processed feature table or peak list (skip directly to statistical analysis).
- Analysis requires targeted quantitation of predefined compounds with known retention times and m/z values (use targeted screening instead).
- Data is in a non-mzML format that cannot be read by pymzml without prior conversion.

## Inputs

- LC/MS data file in mzML format
- pymzml-compatible mass spectrometry data

## Outputs

- Screening results containing detected features
- Annotated feature table with m/z, retention time, and intensity values
- Feature annotations and metadata

## How to apply

Load your LC/MS data file in mzML format using pymzml, then execute the LAGF algorithm workflow as documented in the example.ipynb notebook. The workflow applies the non-targeted screening pipeline to systematically extract mass spectral features across the retention time and m/z dimensions. The algorithm generates annotated feature detections with associated metadata. Validate the output by confirming that detected features have assigned m/z values, retention times, and intensity measurements; check that the results table is properly formatted and contains no null feature IDs.

## Related tools

- **pymzml** (Parses and loads LC/MS data in mzML format for input to the LAGF algorithm)
- **pandas** (Structures and manipulates the feature annotation and results tables)
- **numpy** (Provides numerical array operations for feature extraction calculations)
- **scipy** (Supplies statistical and signal processing functions for feature detection)
- **joblib** (Enables parallel processing of large LC/MS datasets)
- **matplotlib** (Visualizes detected features and screening results)

## Evaluation signals

- Verify that all output rows have non-null m/z, retention time, and intensity values with no NaN entries.
- Confirm that detected feature m/z values fall within the expected mass range for the instrument and sample (e.g., 100–1200 m/z for typical small-molecule LC/MS).
- Check that retention times are monotonically increasing or clustered within expected chromatographic windows.
- Validate that the feature count is consistent with the sample complexity and instrument sensitivity (e.g., hundreds to thousands of features for typical metabolomics samples).
- Cross-reference a subset of high-intensity features against known background ions (solvent, contaminants) to confirm they are appropriately flagged or retained in context.

## Limitations

- The algorithm's performance depends on input data quality; poor-quality or heavily contaminated LC/MS data may yield spurious or missed features.
- No changelog is available to track algorithm improvements or version-specific changes in feature detection behavior.
- The documented workflow relies on exact reproduction of the example.ipynb notebook environment; deviations in Python dependency versions (especially pymzml, scipy, numpy) may alter feature detection results.

## Evidence

- [other] The LAGF algorithm workflow is demonstrated in the example.inpynb file, which serves as the primary documentation for executing the non-targeted screening tool on LC/MS data.: "The LAGF algorithm workflow is shown in the file "example.inpynb""
- [other] 1. Load the LC/MS data file in mzML format using pymzml. 2. Execute the LAGF algorithm workflow as defined in example.ipynb, applying the non-targeted screening pipeline to extract and annotate features. 3. Generate and save the screening results output containing detected features and their annotations.: "Load the LC/MS data file in mzML format using pymzml. Execute the LAGF algorithm workflow as defined in example.ipynb, applying the non-targeted screening pipeline to extract and annotate features."
- [readme] LAGF is described as an LC/MS data non-targeted screening tool in the README.: "LC/MS data non-targeted screening tools"
- [readme] Python >= 3.8.2 is required; specific versions of dependencies are listed.: "The list below is the version of Python dependencies used when developing the algorithm. Older versions might still work but are untested."
