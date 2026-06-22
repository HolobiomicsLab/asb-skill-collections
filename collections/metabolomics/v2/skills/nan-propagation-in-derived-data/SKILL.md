---
name: nan-propagation-in-derived-data
description: Use when when constructing derived elemental ratio images via Calculator formula evaluation in pew², and input element channels contain NaN pixels (from thresholding, signal dropout, or instrumental noise).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0080
  - http://edamontology.org/topic_3372
  tools:
  - Calculator
  - pewpew
  - pewlib
derived_from:
- doi: 10.1021/acs.analchem.1c02138
  title: Pew2
- doi: 10.1529/biophysj.103.038422
  title: ''
evidence_spans:
- The built in `Calculator` can perform simple calculations on image data by entering the desired formula into the `Formula` text box
- The built in `Filtering Tool` removes spikes by comparing pixel values to a locally defined threshold
- '|pewpew| is an open-source LA-ICP-MS data import and processing application'
- based on the python library pewlib_
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pew2_cq
    doi: 10.1021/acs.analchem.1c02138
    title: Pew2
  dedup_kept_from: coll_pew2_cq
schema_version: 0.2.0
---

# NaN Propagation in Derived Data

## Summary

Handle missing or invalid pixel values (NaN) consistently when evaluating per-pixel mathematical expressions across LA-ICP-MS element channels. NaN propagation ensures that pixels below detection limits, failed measurements, or invalid intermediates do not corrupt downstream derived image arrays.

## When to use

When constructing derived elemental ratio images via Calculator formula evaluation in pew², and input element channels contain NaN pixels (from thresholding, signal dropout, or instrumental noise). Use this skill whenever a per-pixel arithmetic or conditional operation must decide whether to propagate NaN forward, mask the result, or apply a fallback value.

## When NOT to use

- If the input element channels are already validated and contain no NaN (unlikely in real LA-ICP-MS data); NaN handling is still best practice but may be overengineering for clean synthetic data.
- If the output format or downstream tool explicitly forbids NaN (e.g., some export formats or legacy software); use `nantonum` conversion as a preprocessing step instead.
- If the analysis goal requires imputation or statistical interpolation of missing pixels rather than explicit masking; consider separate imputation workflows before Calculator evaluation.

## Inputs

- Open LA-ICP-MS element image arrays (in-memory, registered in the pew² image registry)
- Formula string with element references (e.g., P31, Zn66), arithmetic/logical operators, and conditionals
- Pixel arrays with potential NaN values from prior thresholding, masking, or quality filtering

## Outputs

- Derived image array with NaN values propagated through arithmetic and conditional operations
- Registered image in pew² open images with user-supplied or existing name

## How to apply

During element-wise evaluation of the abstract syntax tree (AST), propagate NaN through arithmetic operations (+, −, ×, ÷, ^) following IEEE 754 semantics: any operation involving a NaN operand yields NaN. For conditional branches (if/then/else or ternary ?:), evaluate the condition pixel-by-pixel; if the condition contains NaN, the pixel becomes NaN in the branch result. Use in-place masking or threshold operations (e.g., `threshold(image, value)`) to explicitly convert pixels below a cutoff to NaN before arithmetic, and use `nantonum(array)` to convert remaining NaN values to a user-specified default (typically 0) only when the downstream analysis can tolerate uniform replacement. Register the resulting derived array with NaN propagated through to the output image, or optionally apply `nantonum` as the final step if the output format or visualization does not support NaN.

## Related tools

- **Calculator** (Evaluates per-pixel mathematical expressions and conditionals on element channels, with integrated NaN propagation and handling) — https://github.com/djdt/pewpew
- **pewpew** (GUI host and execution environment for Calculator formulas; maintains the open image registry where NaN-aware derived arrays are stored and visualized) — https://github.com/djdt/pewpew
- **pewlib** (Underlying Python library that implements per-pixel AST evaluation, NaN propagation semantics, and image array operations) — https://github.com/djdt/pewlib

## Evaluation signals

- Output derived image contains NaN pixels exactly where any input operand was NaN (spot-check a few pixels through Calculator formula log or pixel inspector).
- Arithmetic operations involving NaN produce NaN: verify that (NaN + 5) → NaN, (NaN / 0) → NaN, and (NaN * 0) → NaN in the output.
- Conditional expressions branch correctly on NaN: e.g., in a ternary `condition ? a : b`, pixels where condition is NaN should yield NaN in the result (not silently fall through to a or b).
- Histogram or statistical summary of the derived image reports the correct count of NaN pixels (can be viewed in pew² image stats panel).
- When `nantonum` is applied as a final step, all NaN are replaced with the specified default value (e.g., 0 or a fill value), and the output image is exportable in standard formats (CSV, NetCDF, etc.).

## Limitations

- NaN propagation follows IEEE 754 floating-point semantics; non-standard behavior in some edge cases (e.g., 0/0 or ∞ − ∞) depends on the NumPy or underlying math library version.
- Conditional logic (if/then/else) that receives NaN in the condition branch will yield NaN for that pixel; there is no automatic fallback or imputation—users must explicitly handle with `nantonum` if a deterministic result is required.
- Performance may degrade for very large image arrays (e.g., thousands of channels × millions of pixels) due to per-pixel evaluation overhead; optimize by pre-filtering or downsampling if needed.
- NaN propagation is transparent to the user; if formulas are chained across multiple derived images, NaN from early steps will accumulate, potentially leading to sparsity in final outputs; document the expected NaN fraction in the analysis plan.

## Evidence

- [other] Handle NaN propagation and conditionals: pixels failing thresholds become NaN; conditionals branch per-pixel.: "Handle NaN propagation and conditionals: pixels failing thresholds become NaN; conditionals branch per-pixel."
- [other] For supported functions (threshold, mask, segment, kmeans, otsu, mean, median, percentile, normalise, nantonum, abs), apply them to specified arrays in-place within the evaluation context.: "For supported functions (threshold, mask, segment, kmeans, otsu, mean, median, percentile, normalise, nantonum, abs), apply them to specified arrays in-place within the evaluation context."
- [other] Evaluate the AST element-wise (pixel-by-pixel) over all arrays simultaneously, applying arithmetic, comparison, and logical operations in correct precedence.: "Evaluate the AST element-wise (pixel-by-pixel) over all arrays simultaneously, applying arithmetic, comparison, and logical operations in correct precedence."
- [other] Pew² provides a Calculator module that evaluates per-pixel expressions over element channels to produce new derived image arrays, supporting conditional logic and arithmetic operations on elemental data.: "Pew² provides a Calculator module that evaluates per-pixel expressions over element channels to produce new derived image arrays, supporting conditional logic and arithmetic operations on elemental"
