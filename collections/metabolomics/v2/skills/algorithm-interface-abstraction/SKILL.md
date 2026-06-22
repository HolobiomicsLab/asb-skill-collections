---
name: algorithm-interface-abstraction
description: Use when you have multiple independent peak-picking algorithms available and need to allow end-users to select among them for the same analytical task (peak detection in untargeted LC-MS data) without coupling the rest of your pipeline to each algorithm's API.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3214
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Centwave
  - FeatureFinderMetabo
  - ADAP
  - SLAW
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.1c02687
  title: slaw
evidence_spans:
- 'Wrapping of three main peak picking algorithms: Centwave, FeatureFinderMetabo, ADAP'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_slaw_cq
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_slaw_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02687
  all_source_dois:
  - 10.1021/acs.analchem.1c02687
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# algorithm-interface-abstraction

## Summary

Design a unified interface that wraps multiple interchangeable peak-picking algorithms (Centwave, FeatureFinderMetabo, ADAP) and routes raw LC-MS data to the selected algorithm via configuration-driven dispatch, standardizing outputs to a common feature table format. This abstraction isolates algorithm-specific details and allows users to swap peak-picking methods without rewriting downstream processing logic.

## When to use

You have multiple independent peak-picking algorithms available and need to allow end-users to select among them for the same analytical task (peak detection in untargeted LC-MS data) without coupling the rest of your pipeline to each algorithm's API. Typical trigger: a configuration file specifying algorithm choice ('Centwave' vs 'FeatureFinderMetabo' vs 'ADAP') and raw mzML or netCDF input data.

## When NOT to use

- Input data is already a feature table or alignment matrix (data has already been peak-picked); use this skill only at the raw data → peak table boundary.
- All downstream code is tightly coupled to a single algorithm's output schema and cannot tolerate differences in column names or precision; refactoring to accept a standardized format is a prerequisite.
- The analysis requires simultaneous use of multiple peak-picking algorithms on the same data and explicit comparison of their results (consider running each separately and comparing outputs post-hoc instead).

## Inputs

- Configuration specification (text or JSON) naming the peak-picking algorithm (Centwave, FeatureFinderMetabo, or ADAP)
- Centroided raw LC-MS data in mzML or netCDF format
- Algorithm-specific parameters (e.g., ppm tolerance, peak width range)

## Outputs

- Standardized feature matrix (rows=features/ions, columns=m/z, retention time, intensity)
- Algorithm metadata (algorithm name, version, parameters applied)
- Feature quality indicators (e.g., signal-to-noise ratio, peak shape metrics)

## How to apply

Implement a routing layer that accepts a configuration key naming the target peak-picking algorithm and centroided LC-MS data (mzML or netCDF format). Route the data to the corresponding algorithm-specific wrapper module based on the configuration value. Execute the selected algorithm with user-supplied parameters. Standardize the algorithm's output (which may differ in column names, units, or structure) into a common internal format—typically a feature matrix with columns for m/z, retention time, and intensity. Return both the standardized feature table and algorithm metadata (e.g., algorithm name, version, parameters used) so downstream stages (alignment, grouping, gap-filling) operate uniformly. This decouples downstream code from algorithm-specific output schemas and allows parameter swapping via configuration without code changes.

## Related tools

- **Centwave** (One of three selectable peak-picking algorithms; detects peaks using continuous wavelet transform)
- **FeatureFinderMetabo** (One of three selectable peak-picking algorithms; feature detection optimized for metabolomics)
- **ADAP** (One of three selectable peak-picking algorithms; adaptive peak detection)
- **SLAW** (Reference implementation of algorithm-interface abstraction for untargeted LC-MS processing) — https://github.com/zamboni-lab/SLAW

## Examples

```
docker run --rm -v /path/to/input:/input -v /path/to/output:/output zambonilab/slaw:latest
```

## Evaluation signals

- Verify that selecting different algorithm names in the configuration file routes data to the correct wrapper and executes the intended algorithm (e.g., check log output or algorithm metadata in output).
- Confirm that output from each algorithm, despite differences in native format, produces a standardized feature matrix with identical column names and types (m/z, retention time, intensity).
- Validate that downstream stages (alignment, grouping, gap-filling) accept the standardized output from any algorithm without modification, confirming decoupling.
- Check that feature counts and m/z/RT ranges are consistent with the selected algorithm's known sensitivity and specificity on positive control samples.
- Ensure algorithm metadata is correctly captured and propagated through the output for reproducibility and audit trails.

## Limitations

- SLAW wrapping is specific to three peak-picking algorithms (Centwave, FeatureFinderMetabo, ADAP); adding new algorithms requires implementing a new wrapper module.
- Output standardization assumes all wrapped algorithms report at least m/z, retention time, and intensity; algorithms lacking one of these metrics cannot be integrated without lossy transformation.
- Parameter optimization (automated tuning for alignment and gap-filling) is decoupled from algorithm selection; users must manually manage parameter ranges for each algorithm choice.
- DIA-MS and profile-mode (non-centroided) data are not supported; all input must be centroided DDA mzML or netCDF.
- Polarity detection is performed once at initialization; mixed-polarity datasets require pre-splitting and separate SLAW runs.

## Evidence

- [other] SLAW wraps three independent peak picking algorithms—Centwave, FeatureFinderMetabo, and ADAP—enabling configurable selection among them for the peak-picking stage of untargeted LC-MS processing.: "SLAW wraps three independent peak picking algorithms—Centwave, FeatureFinderMetabo, and ADAP—enabling configurable selection among them for the peak-picking stage"
- [other] Route the data to the corresponding algorithm wrapper module based on the configuration key.: "Route the data to the corresponding algorithm wrapper module based on the configuration key."
- [other] Standardize the output peak table to a common internal format (e.g., feature matrix with m/z, retention time, intensity columns).: "Standardize the output peak table to a common internal format (e.g., feature matrix with m/z, retention time, intensity columns)."
- [readme] Wrapping of three main peak picking algorithms: Centwave, FeatureFinderMetabo, ADAP: "Wrapping of three main peak picking algorithms: Centwave, FeatureFinderMetabo, ADAP"
- [readme] Raw MS data in mzML format. Files can include MS1 and DDA-MS2 scans. All data must be centroided and of unique polarity.: "Raw MS data in mzML format. Files can include MS1 and DDA-MS2 scans. All data must be centroided and of unique polarity."
