---
name: chromatographic-window-coverage-assessment
description: Use when after extracting retention times from top MS1 features detected
  in an LC-MS run, and when you need to evaluate whether a given gradient time range
  (e.g., 0–30 minutes) is being used efficiently to separate compounds. Apply this
  skill as the objective function in gradient optimization (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - Jupyter Notebook
  - bago
  - pyopenms
  techniques:
  - LC-MS
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-window-coverage-assessment

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Quantifies how effectively a liquid chromatography gradient distributes compounds across the usable retention-time window by converting a series of MS1 retention times into a normalized separation-efficiency score (0–1). This metric encodes omics-scale compound-separation performance for gradient optimization workflows.

## When to use

After extracting retention times from top MS1 features detected in an LC-MS run, and when you need to evaluate whether a given gradient time range (e.g., 0–30 minutes) is being used efficiently to separate compounds. Apply this skill as the objective function in gradient optimization (e.g., Bayesian optimization) to compare candidate gradients within ≤10 iterations.

## When NOT to use

- Input retention times are already binned or aggregated—sepEfficiency requires individual feature retention times, not histograms or pre-computed distributions.
- Gradient window definition is missing or ambiguous—rtRange must clearly delimit the start and end of the gradient phase in minutes.
- You are comparing separation performance across different MS platforms or instruments without instrument-specific calibration—the encoding may not be directly comparable between incompatible detector or ionization configurations.

## Inputs

- rtSeq: list or array of retention times (float, in minutes) from top MS1 features
- rtRange: tuple (start_time, end_time) defining the gradient window in minutes
- MSExperiment object or extracted ms1Spectrum objects from LC-MS raw data

## Outputs

- separation_efficiency: float normalized to [0, 1] representing gradient coverage quality
- qualitative assessment: 'good separation' (>0.7), 'moderate' (0.4–0.7), 'poor' (<0.4)

## How to apply

Extract a series of retention times (rtSeq) from the top detected MS1 features in your raw LC-MS data (typically using readRawData and extractMS1 workflows). Define the gradient time range (rtRange, in minutes) that spans the chromatographic window of interest. Pass both rtSeq and rtRange to the sepEfficiency function, which calculates the distribution and spacing of retention times across the usable gradient window. The function returns a normalized float value between 0 (no separation—all compounds elute at the same time) and 1 (complete separation—compounds are evenly dispersed across the gradient). Validate that the returned value falls within [0, 1] and reflects realistic separation performance for your feature set. Use this metric as the objective to optimize gradient parameters (initial %B, final %B, slope) via Bayesian optimization.

## Related tools

- **bago** (Provides the sepEfficiency function and the full Bayesian optimization framework for iteratively refining gradients based on separation-efficiency scores) — https://github.com/huaxuyu/bago
- **pyopenms** (Parses raw LC-MS data and provides MSExperiment object to extract MS1 features and retention times)
- **Python** (Execution environment for bago workflows and retention-time extraction scripts)
- **Jupyter Notebook** (Interactive environment for running separation-efficiency calculations and visualizing gradient coverage across multiple runs) — https://github.com/Waddlessss/BAGO

## Examples

```
from bago import sepEfficiency; rt_times = [5.2, 8.1, 12.4, 18.7, 24.5]; rt_range = (2.0, 30.0); eff = sepEfficiency(rtSeq=rt_times, rtRange=rt_range); print(f'Separation efficiency: {eff:.3f}')
```

## Evaluation signals

- Returned separation_efficiency value is a float in [0.0, 1.0]; values outside this range indicate an implementation error.
- Retention times in rtSeq are all within rtRange boundaries; any rtSeq value outside [rtRange[0], rtRange[1]] indicates data preparation error.
- Separation efficiency increases monotonically (or at least does not decrease significantly) when retention times become more evenly distributed across the gradient window (test with synthetic uniform vs. clustered rtSeq).
- Visual inspection: plot retention times as a histogram or scatter along the gradient axis; separation efficiency should correlate visually with how well the features 'fill' the window rather than clustering at one end.
- Comparison across gradients: when applied to multiple LC-MS runs with different gradient parameters, separation efficiency should be higher for gradients that visually spread compounds across a broader retention-time range.

## Limitations

- sepEfficiency encodes only the distribution of retention times; it does not account for peak width, resolution, or overlap—two gradients with identical retention-time spacing but different peak capacities will receive the same score.
- The metric assumes that the provided rtRange correctly reflects the usable gradient window; if rtRange is set too narrow or too wide relative to actual gradient execution, the efficiency score may be misleading.
- No changelog is available for the bago package, so version-specific behavior of sepEfficiency (e.g., handling of ties, edge cases with <3 features) is not documented.
- Separation efficiency is optimized for omics-scale discovery (small-molecule MS); applicability to large-molecule (protein, antibody) LC-MS or targeted assays has not been validated in the provided documentation.

## Evidence

- [other] The sepEfficiency function calculates separation efficiency using a series of retention times extracted from LC-MS data, producing a singular metric that encodes compound-separation performance for omics-scale gradient evaluation.: "The sepEfficiency function calculates separation efficiency using a series of retention times extracted from LC-MS data, producing a singular metric that encodes compound-separation performance for"
- [other] Extract or receive a series of retention times (rtSeq) from the top detected MS1 features and the gradient time range (rtRange, in minutes) defining when the gradient begins and ends. Compute separation efficiency by calculating the distribution and spacing of retention times across the usable gradient window using the sepEfficiency function with rtSeq and rtRange parameters.: "Extract or receive a series of retention times (rtSeq) from the top detected MS1 features and the gradient time range (rtRange, in minutes) defining when the gradient begins and ends. Compute"
- [other] Return a normalized float value between 0 (no separation) and 1 (complete separation) that quantifies how effectively the gradient spreads compounds across the chromatographic window.: "Return a normalized float value between 0 (no separation) and 1 (complete separation) that quantifies how effectively the gradient spreads compounds across the chromatographic window."
- [readme] Separation efficiency was defined to evaluate the performance of a gradient.: "Separation efficiency was defined to evaluate the performance of a gradient."
- [readme] Wonder how omics-scale evaluation is achieved? Read more about [encodings].: "Wonder how omics-scale evaluation is achieved? Read more about [encodings]."
