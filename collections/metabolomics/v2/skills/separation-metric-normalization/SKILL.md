---
name: separation-metric-normalization
description: Use when you have extracted retention times from top MS1 features across an LC-MS run and need a single, comparable metric to evaluate how effectively a gradient spreads compounds across the chromatographic window.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - Python
  - Jupyter Notebook
  - bago
  - pyopenms
  - scikit-learn
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
---

# separation-metric-normalization

## Summary

Converts a series of retention times from LC-MS data into a normalized quantitative separation efficiency score (0–1) that encodes compound-separation performance at omics scale. This skill enables standardized comparison of gradient performance across different experiments and chemical spaces.

## When to use

Apply this skill when you have extracted retention times from top MS1 features across an LC-MS run and need a single, comparable metric to evaluate how effectively a gradient spreads compounds across the chromatographic window. Use it to benchmark gradient performance before, during, or after Bayesian optimization of LC-MS methods, or to compare gradient performance across multiple runs or conditions.

## When NOT to use

- Input retention time sequence is empty or contains fewer than 2 features — the metric cannot meaningfully encode separation.
- Gradient time range (rtRange) is zero or negative — the function requires a positive window to normalize against.
- Raw MS data has not yet been processed to extract MS1 features; pass processed ms1Spectrum objects or retention time arrays, not raw mzML/netCDF files.

## Inputs

- rtSeq: ordered sequence of retention times (float array, in minutes) from top MS1 features
- rtRange: tuple or list of (gradient_start, gradient_end) in minutes
- ms1Spectrum objects or extracted m/z and intensity pairs from LC-MS data

## Outputs

- separation_efficiency: float scalar in [0, 1] representing normalized separation performance
- validation_status: boolean or string indicating whether output is valid and realistic

## How to apply

Extract a series of retention times (rtSeq) from the top detected MS1 features and record the gradient time range (rtRange, in minutes) defining when the gradient begins and ends. Pass both rtSeq and rtRange to the sepEfficiency function, which calculates the distribution and spacing of retention times across the usable gradient window. The function returns a normalized float value between 0 (no separation) and 1 (complete separation). Validate that the output falls within [0, 1] and reflects realistic separation performance for the input feature set by spot-checking against visual inspection of the base peak chromatogram and the number of resolved features.

## Related tools

- **bago** (Python package providing sepEfficiency function to compute normalized separation efficiency from retention times) — https://github.com/huaxuyu/bago
- **pyopenms** (Read raw LC-MS data and extract MS1 scans for retention time extraction)
- **scikit-learn** (Optional preprocessing (e.g., StandardScaler) for retention time normalization before sepEfficiency calculation)

## Examples

```
from bago import sepEfficiency; rt_seq = [2.3, 5.1, 8.7, 12.4, 15.9]; rt_range = (1.0, 20.0); sep_eff = sepEfficiency(rt_seq, rt_range); print(f'Separation efficiency: {sep_eff:.3f}')
```

## Evaluation signals

- Output value is a float strictly within [0.0, 1.0]; values outside this range indicate a function error.
- For a known well-separated gradient (e.g., many features evenly distributed across rtRange), sepEfficiency should be > 0.6; for co-eluting compounds, < 0.3.
- Retention times in rtSeq are monotonically increasing and all fall within rtRange boundaries.
- Recomputing sepEfficiency on the same rtSeq and rtRange produces identical output (deterministic).
- Separation efficiency increases when rtSeq becomes more evenly distributed across rtRange (e.g., adding separated features increases the metric).

## Limitations

- The metric assumes that higher spacing of retention times across the gradient window reflects better separation; it does not measure mass spectral quality, identity confidence, or quantification accuracy.
- Omics-scale evaluation depends on complete and unbiased detection of MS1 features; missing features or instrument dropout will underestimate true separation efficiency.
- The normalized [0, 1] scale is relative to the input rtRange; changing the gradient time window will change the same compound set's efficiency score, making cross-experiment comparisons valid only if rtRange is held constant.
- No changelog provided; exact implementation details of the sepEfficiency encoding function are not documented in the article.

## Evidence

- [methods] sepEfficiency function definition and inputs: "The sepEfficiency function calculates separation efficiency using a series of retention times extracted from LC-MS data, producing a singular metric that encodes compound-separation performance for"
- [other] Workflow steps for applying sepEfficiency: "Extract or receive a series of retention times (rtSeq) from the top detected MS1 features and the gradient time range (rtRange, in minutes) defining when the gradient begins and ends. Compute"
- [other] Output normalization and validation: "Return a normalized float value between 0 (no separation) and 1 (complete separation) that quantifies how effectively the gradient spreads compounds across the chromatographic window. Validate the"
- [readme] Omics-scale separation evaluation: "Separation efficiency was defined to evaluate the performance of a gradient."
- [readme] Purpose of separation encoding in BAGO: "Wonder how omics-scale evaluation is achieved? Read more about [encodings]."
