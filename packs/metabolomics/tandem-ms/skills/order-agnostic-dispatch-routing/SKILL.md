---
name: order-agnostic-dispatch-routing
description: Use when when your untargeted LC-MS pipeline must support multiple peak-picking backends and you need to let users specify which algorithm to use (via configuration file or parameter) without hard-coding algorithm dependencies.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0769
  tools:
  - Centwave
  - FeatureFinderMetabo
  - ADAP
  - ProteoWizard
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

# Order-Agnostic Dispatch Routing

## Summary

Route untargeted LC-MS data to a user-selected peak-picking algorithm (Centwave, FeatureFinderMetabo, or ADAP) via configuration, execute it, and standardize output to a common feature matrix format. This skill decouples algorithm selection from workflow execution, enabling transparent algorithm swapping without changing calling code.

## When to use

When your untargeted LC-MS pipeline must support multiple peak-picking backends and you need to let users specify which algorithm to use (via configuration file or parameter) without hard-coding algorithm dependencies. Triggered by the presence of a peak-picking algorithm selection parameter in your parameters.txt or configuration object, and centroided mzML or netCDF input data.

## When NOT to use

- Input data is already a feature table or peak table; skip to alignment/grouping stages instead.
- Raw LC-MS data is in profile (non-centroided) format; centroid first using ProteoWizard before routing.
- Data contains mixed polarity scans; split by polarity and route each separately, as SLAW requires uniform polarity.

## Inputs

- Configuration specification naming the peak-picking algorithm (Centwave, FeatureFinderMetabo, or ADAP)
- Raw LC-MS data in centroided mzML or netCDF format
- Algorithm-specific parameters (e.g., ppm tolerance, minimum intensity, peak width thresholds)

## Outputs

- Standardized peak table with m/z, retention time, and intensity columns (feature matrix)
- Algorithm metadata (algorithm name, parameters, execution statistics)
- Peak table in common internal format for downstream SLAW stages

## How to apply

Accept a configuration specification (e.g., from parameters.txt) naming the target peak-picking algorithm (Centwave, FeatureFinderMetabo, or ADAP) and the raw LC-MS data in mzML or netCDF format. Route the data and algorithm-specific parameters to the corresponding wrapper module based on the configuration key. Execute the selected peak-picking algorithm on the input data with its specified parameters (e.g., ppm tolerance, minimum intensity, minimum peak width). Standardize the output peak table to a common internal format containing at minimum m/z, retention time, and intensity columns (a feature matrix). Return both the standardized peak table and algorithm metadata (e.g., algorithm name, parameters used) to the caller for downstream stages (alignment, grouping, gap-filling). The routing decision is made once at workflow initialization, not per-sample.

## Related tools

- **Centwave** (Peak-picking algorithm option; detects peaks in centroided LC-MS data; routed to via configuration selection)
- **FeatureFinderMetabo** (Peak-picking algorithm option; alternative to Centwave for metabolite feature detection; routed to via configuration selection)
- **ADAP** (Peak-picking algorithm option; adaptive peak picking method; routed to via configuration selection)
- **ProteoWizard** (Preprocessing tool to convert vendor raw files to centroided mzML format; required input preparation before routing)

## Evaluation signals

- Configuration key correctly maps to the intended algorithm wrapper module; verify by logging which algorithm module is instantiated.
- Output peak table contains exactly three mandatory columns (m/z, retention time, intensity) and matches the expected internal schema; validate via schema check on output feature matrix.
- Algorithm metadata is correctly attached to output; verify algorithm name, parameters used, and execution timestamp are present and non-empty.
- Peak table is generated without errors for all three supported algorithms when each is selected in turn; test routing to Centwave, FeatureFinderMetabo, and ADAP independently.
- Downstream workflow stages (alignment, grouping) accept the standardized output without reformatting; verify no intermediate conversion step is needed.

## Limitations

- Only three peak-picking algorithms are wrapped (Centwave, FeatureFinderMetabo, ADAP); other algorithms require new wrapper code.
- Input LC-MS data must be centroided and of uniform polarity; profile mode or mixed-polarity data will cause routing to fail.
- Routing decision is static per workflow run; algorithm selection cannot be changed mid-pipeline without re-invoking the workflow.
- Output standardization assumes all three algorithms can produce m/z, retention time, and intensity estimates; if an algorithm's native output format lacks one of these, standardization must include imputation or the algorithm becomes incompatible.
- DIA-MS (data-independent acquisition) is not supported; routing only works for DDA-MS data as stated in SLAW README.

## Evidence

- [other] Route the data to the corresponding algorithm wrapper module based on the configuration key.: "Route the data to the corresponding algorithm wrapper module based on the configuration key."
- [other] SLAW wraps three independent peak picking algorithms—Centwave, FeatureFinderMetabo, and ADAP—enabling configurable selection among them for the peak-picking stage: "SLAW wraps three independent peak picking algorithms—Centwave, FeatureFinderMetabo, and ADAP—enabling configurable selection among them for the peak-picking stage"
- [other] Standardize the output peak table to a common internal format (e.g., feature matrix with m/z, retention time, intensity columns).: "Standardize the output peak table to a common internal format (e.g., feature matrix with m/z, retention time, intensity columns)."
- [readme] All data must be centroided and of unique polarity.: "All data must be centroided and of unique polarity."
- [readme] Wrapping of three main peak picking algorithms: Centwave, FeatureFinderMetabo, ADAP: "Wrapping of three main peak picking algorithms: Centwave, FeatureFinderMetabo, ADAP"
- [readme] DDA only: "SLAW is a scalable, containerized workflow for untargeted LC-MS processing (DDA only)."
