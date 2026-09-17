---
name: ms-spectra-extraction-and-preprocessing
description: 'Use when you have raw LC-MS/MS data in mzML or mzXML format and need
  to: (1) identify the top-abundance MS1 signals in an LC run, (2) compute a single
  scalar metric (separation efficiency) that summarizes how well compounds are resolved
  across the chromatogram, and (3) feed that metric into a.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - BAGO
  - pyopenms
  - scikit-learn
  - Python
  - bago
  techniques:
  - LC-MS
  - CE-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2023.09.08.556930
  title: BAGO
- doi: 10.1002/9780470508183
  title: ''
evidence_spans:
- BAGO is a Bayesian optimization strategy for LC gradient optimization for MS-based
  small molecule analysis
- A :class:`ms1Spectrum` object (supported by :mod:`bago`)
- A :class:`MSExperiment` object (supported by :mod:`pyopenms`)
- a :class:`sklearn.preprocessing.StandardScaler` object used to scale the data
- a :class:`sklearn.gaussian_process.GaussianProcessRegressor` object
- Download and install Python 3.8 or later from `python.org`
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bago_cq
    doi: 10.1101/2023.09.08.556930
    title: BAGO
  dedup_kept_from: coll_bago_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2023.09.08.556930
  all_source_dois:
  - 10.1101/2023.09.08.556930
  - 10.1002/9780470508183
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS spectra extraction and preprocessing

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and convert MS1 and MS2 spectra from raw LC-MS data files (mzML/mzXML) into standardized spectrum objects, then compute retention-time-based separation efficiency metrics to enable iterative gradient optimization. This preprocessing step transforms unstructured mass spectrometry data into quantifiable features for Bayesian optimization of LC gradients.

## When to use

You have raw LC-MS/MS data in mzML or mzXML format and need to: (1) identify the top-abundance MS1 signals in an LC run, (2) compute a single scalar metric (separation efficiency) that summarizes how well compounds are resolved across the chromatogram, and (3) feed that metric into a Bayesian optimization loop to iteratively refine gradient conditions. Use this skill as the first step in each iteration of the BAGO optimization workflow.

## When NOT to use

- Input data is already in processed feature table or peak list format (e.g., CSV with m/z, RT, intensity columns) — skip directly to Gaussian process fitting.
- MS data are from targeted or MRM workflows where only a small set of predetermined transitions are monitored — the omics-scale separation efficiency metric assumes broad untargeted MS1 coverage.
- Retention time reproducibility across gradient trials is poor or unmeasurable (e.g., instrumental drift or gradient hold-up volume not controlled) — separation efficiency will not correlate meaningfully with optimization.

## Inputs

- mzML or mzXML raw LC-MS data file
- Top signal abundance threshold (integer, e.g., top 50–100 signals)
- Retention time window or mass tolerance (optional, for signal alignment)

## Outputs

- MSExperiment object (pyopenms)
- ms1Spectrum objects (list of MS1 scans)
- ms2Spectrum objects (list of MS2 scans)
- Top signals (m/z values with intensities)
- Separation efficiency scalar (0–1 or normalized range per gradient trial)
- Retention time series per signal (for post-hoc verification)

## How to apply

Load the raw LC-MS data file using pyopenms (readRawData function) to populate an MSExperiment object. Extract all MS1 scans into ms1Spectrum objects and MS2 scans into ms2Spectrum objects using the extractMS1 and extractMS2 functions respectively. Call findTopSignals on the MS1 data to identify the most abundant m/z features. For each top signal, extract its retention times across the run and compute separation efficiency using the sepEfficiency function, which measures retention-time spacing between peaks as a proxy for chromatographic resolution. This scalar metric (typically 0–1 or normalized range) becomes the ground-truth output for the Gaussian process model in the next optimization step. Document the m/z values, retention times, and efficiency score for comparison across gradient trials.

## Related tools

- **pyopenms** (Read raw LC-MS data files (mzML/mzXML) into MSExperiment objects; extract MS1 and MS2 spectra into standardized spectrum objects.) — https://github.com/OpenMS/OpenMS
- **bago** (Provides high-level functions (readRawData, extractMS1, extractMS2, findTopSignals, sepEfficiency) for preprocessing and computing separation efficiency metrics from MS data.) — https://github.com/huaxuyu/bago
- **scikit-learn** (StandardScaler for normalizing gradient encodings and spectrum intensity values prior to Gaussian process fitting.) — https://github.com/scikit-learn/scikit-learn

## Examples

```
from bago import readRawData, extractMS1, extractMS2, findTopSignals, sepEfficiency; ms_exp = readRawData('sample.mzML'); ms1_scans = extractMS1(ms_exp); ms2_scans = extractMS2(ms_exp); top_mz = findTopSignals(ms1_scans, n=50); sep_eff = sepEfficiency(ms1_scans, top_mz)
```

## Evaluation signals

- MSExperiment object is non-empty and contains at least N MS1 scans and M MS2 scans matching the expected run time and scan count from the instrument method.
- Top signals list contains m/z values with non-zero intensities; m/z values fall within the expected detection range (e.g., 50–1500 m/z for small molecules).
- Separation efficiency scalar is a normalized number (0–1 or bounded range) and shows consistent reproducibility when the same gradient is run twice.
- Retention time series per signal is monotonically increasing (or constant within instrumental jitter) and spans the expected chromatographic window (e.g., 0–30 min).
- Separation efficiency improves (or worsens predictably) when gradients are manually varied in a known direction (e.g., longer initial hold → later elution → different efficiency), confirming the metric is sensitive to gradient changes.

## Limitations

- Separation efficiency is a single scalar metric and may mask multi-modal compound distributions or bimodal resolution (early-eluting vs. late-eluting compound pairs resolved differently). Use with caution if the chemical space of interest is heterogeneous in hydrophobicity.
- Preprocessing assumes robust peak detection in MS1 data. Noisy spectra, baseline drift, or instrument artifacts can skew the top signals and reduce metric reliability.
- No changelog or versioning information is available for the bago package, so reproducibility across different package versions is not formally documented.
- The method is designed for untargeted LC-MS/MS of small molecules; applicability to large-molecule (protein, peptide) or targeted MRM workflows is not discussed.

## Evidence

- [methods] Load raw LC-MS data extraction: "Load raw LC-MS data from mzML or mzXML file using pyopenms and extract MS1 and MS2 spectra into ms1Spectrum and ms2Spectrum objects."
- [methods] Top signal and separation efficiency computation: "Find top signals in MS1 data and compute separation efficiency (retention time spacing metric) for the initial gradient run."
- [methods] Function definitions for preprocessing workflow: "Function to extract all MS1 scans and convert them to :class:`ms1Spectrum` objects"
- [methods] Separation efficiency metric definition: "Calculate the separation efficiency using a series of retention times"
- [intro] Omics-scale evaluation design: "Separation efficiency was defined to evaluate the performance of a gradient."
- [readme] Efficiency goal and iteration count: "Find an optimal gradient for your LC-MS/MS analysis within 10 runs."
