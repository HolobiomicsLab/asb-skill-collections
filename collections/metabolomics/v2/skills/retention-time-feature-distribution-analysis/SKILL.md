---
name: retention-time-feature-distribution-analysis
description: Use when you have extracted retention times from top MS1 features in an LC-MS/MS experiment and need to assess whether the gradient configuration (start and end time in minutes) achieves adequate compound separation across the full chemical space.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Jupyter Notebook
  - bago
  - pyopenms
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.1101/2023.09.08.556930
  title: BAGO
- doi: 10.1002/9780470508183
  title: ''
evidence_spans:
- Download and install Python 3.8 or later from `python.org`
- model.computeNextGradient()
- A Jupyter Notebook is provided to help you get started with the LC gradient optimization
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-feature-distribution-analysis

## Summary

Quantify LC-MS chromatographic gradient performance by encoding the spatial distribution of detected compound retention times into a normalized separation-efficiency metric (0–1). This skill bridges raw retention-time sequences to omics-scale gradient evaluation by computing how effectively a gradient spreads compounds across the usable chromatographic window.

## When to use

Apply this skill when you have extracted retention times from top MS1 features in an LC-MS/MS experiment and need to assess whether the gradient configuration (start and end time in minutes) achieves adequate compound separation across the full chemical space. Use it as the feedback signal during Bayesian optimization of gradient parameters, or to compare two gradient protocols on the same sample.

## When NOT to use

- Input is already a pre-computed feature table or quantification matrix; this skill operates on raw retention-time sequences, not aggregated abundance data.
- Gradient window (rtRange) is not defined or spans less than 1 minute; the metric requires sufficient chromatographic space to detect separation.
- MS1 feature detection has not been performed; the skill requires a ranked list of detected compounds, not raw spectral data.

## Inputs

- rtSeq (list or array of float): retention times in minutes extracted from top MS1 features
- rtRange (tuple of float): [gradient_start_time_min, gradient_end_time_min]
- MS1 feature intensity list (implicit): used to rank and select top detected compounds

## Outputs

- separation_efficiency_score (float): normalized metric in [0, 1] encoding gradient separation performance
- separation_efficiency_interpretation (string, implicit): qualitative assessment (e.g., 'poor', 'adequate', 'optimal')

## How to apply

Extract retention times (rtSeq) from the highest-intensity MS1 features detected across the chromatographic run, along with the gradient time window bounds (rtRange, in minutes, e.g., [0.5, 20.0]). Pass these to the sepEfficiency function, which calculates the distribution and spacing of retention times within the usable gradient window. The function normalizes the result to [0, 1], where 0 indicates no separation (all features clustered at one point) and 1 indicates ideal separation (features uniformly distributed). Validate that the output is a float strictly within [0, 1] and that it reflects realistic gradient performance for the input feature count. Use this score as the objective function in Bayesian optimization to iteratively refine gradient parameters (e.g., organic solvent ramp rate, column temperature) across subsequent LC-MS/MS runs.

## Related tools

- **bago** (Implements the sepEfficiency function for retention-time encoding and houses the Bayesian optimization loop that uses separation-efficiency scores to guide gradient refinement) — https://github.com/huaxuyu/bago
- **pyopenms** (Provides MSExperiment and ms1Spectrum objects for parsing and organizing LC-MS/MS raw data before retention-time extraction)
- **Python** (Language and runtime environment for executing sepEfficiency and Bayesian optimization workflows)
- **Jupyter Notebook** (Interactive notebook environment for prototyping and visualizing retention-time distributions and separation-efficiency scores) — https://github.com/Waddlessss/bago

## Examples

```
from bago import sepEfficiency; rt_times = [2.3, 5.1, 7.8, 12.4, 15.9]; gradient_window = (0.5, 20.0); sep_score = sepEfficiency(rtSeq=rt_times, rtRange=gradient_window); print(f'Separation efficiency: {sep_score:.3f}')
```

## Evaluation signals

- Output separation_efficiency_score is a float and lies strictly within [0.0, 1.0].
- Higher separation_efficiency scores correlate with improved peak-picking accuracy and wider m/z feature coverage in downstream untargeted metabolomics analysis (validate by counting distinct MS/MS annotations or feature identification rate).
- Retention times in rtSeq are monotonically increasing or clustered in biologically plausible regions (e.g., polar compounds early, lipids late).
- Separation efficiency increases monotonically or plateaus as the gradient window (rtRange) expands; efficiency should not improve when a shorter gradient is used on the same sample.
- Repeated measurements of the same gradient produce consistent (±0.02) separation-efficiency scores, confirming robustness to minor instrumental drift.

## Limitations

- Separation efficiency encodes only the geometric spacing of detected features, not their chemical diversity or mass resolution; two gradients with identical retention-time distributions will score equally even if compound identifiability differs.
- The metric depends on MS1 feature detection quality; missing or mis-detected features will produce artificially low or high scores.
- No explicit penalty for co-elution or mass overlap; separation efficiency reflects retention-time spread alone, not chromatographic resolution or mass accuracy.
- Designed for omics-scale (untargeted) analyses; not applicable to targeted quantification where compound retention times are fixed by reference standards.
- Gradient optimization via this metric assumes linear interpolation within the gradient window; non-linear or multi-segment gradients may not be accurately modeled.

## Evidence

- [other] The sepEfficiency function calculates separation efficiency using a series of retention times extracted from LC-MS data, producing a singular metric that encodes compound-separation performance for omics-scale gradient evaluation.: "The sepEfficiency function calculates separation efficiency using a series of retention times extracted from LC-MS data, producing a singular metric that encodes compound-separation performance for"
- [other] Extract or receive a series of retention times (rtSeq) from the top detected MS1 features and the gradient time range (rtRange, in minutes) defining when the gradient begins and ends. Compute separation efficiency by calculating the distribution and spacing of retention times across the usable gradient window using the sepEfficiency function with rtSeq and rtRange parameters. Return a normalized float value between 0 (no separation) and 1 (complete separation) that quantifies how effectively the gradient spreads compounds across the chromatographic window.: "Extract or receive a series of retention times (rtSeq) from the top detected MS1 features and the gradient time range (rtRange, in minutes) defining when the gradient begins and ends. Compute"
- [methods] Separation efficiency was defined to evaluate the performance of a gradient.: "Separation efficiency was defined to evaluate the performance of a gradient."
- [readme] Separation efficiency was defined to evaluate the performance of a gradient. Wonder how omics-scale evaluation is achieved? Read more about [encodings].: "Separation efficiency was defined to evaluate the performance of a gradient. Wonder how omics-scale evaluation is achieved? Read more about [encodings]."
- [readme] Find an optimal gradient for your LC-MS/MS analysis within 10 runs.: "Find an optimal gradient for your LC-MS/MS analysis within 10 runs."
