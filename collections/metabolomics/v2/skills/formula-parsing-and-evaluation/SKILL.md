---
name: formula-parsing-and-evaluation
description: 'Use when you have multiple open elemental images (e.g., P31, Zn66) from LA-ICP-MS and need to create a new derived image by evaluating a per-pixel mathematical expression. Typical triggers include: combining isotope ratios (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3050
  - http://edamontology.org/topic_3382
  tools:
  - Calculator
  - pewpew
  - pewlib
  - pewpew (Pew²)
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

# formula-parsing-and-evaluation

## Summary

Parse and evaluate mathematical expressions over per-pixel elemental channel data in LA-ICP-MS images to derive new image arrays. This skill enables users to combine multiple isotope channels via arithmetic, logical, and conditional operators, producing new derived images with support for built-in functions like threshold, mask, segment, and statistical measures.

## When to use

Apply this skill when you have multiple open elemental images (e.g., P31, Zn66) from LA-ICP-MS and need to create a new derived image by evaluating a per-pixel mathematical expression. Typical triggers include: combining isotope ratios (e.g., 'Zn66 / Cu65'), applying conditional logic to mask regions based on elemental thresholds (e.g., 'if P31 > 1000 then Ca42 else nan'), or applying in-place statistical transformations (e.g., 'threshold(Fe56, 500)', 'kmeans(Ni60, 3)').

## When NOT to use

- Input images are not LA-ICP-MS elemental data or are not yet loaded into the pewpew open image registry.
- Formula references isotope names that are not registered as open images or contain syntax errors that the parser cannot tokenize.
- Desired operation is purely statistical (e.g., computing channel means without per-pixel derivation); use built-in statistical functions instead.

## Inputs

- Multiple open elemental image arrays (registered in pewpew image registry, e.g., P31, Zn66, Ca42)
- Formula string containing isotope references, operators, and optional function calls

## Outputs

- New derived image array registered in open images with user-supplied name
- Pixel-wise results of formula evaluation; NaN for pixels failing thresholds or conditions

## How to apply

First, construct a formula string referencing registered open images by isotope name (e.g., P31, Zn66) and combining them with arithmetic operators (+, −, ×, ÷, ^), comparison operators, and optional conditional branches (if/then/else or ternary ?:). Use a recursive descent or expression-tree parser to tokenize the formula into an abstract syntax tree (AST), validating each isotope reference against the open image registry and loading corresponding pixel arrays. Build an intermediate representation separating arithmetic expressions, comparisons, and conditional branches. Evaluate the AST element-wise (pixel-by-pixel) over all registered arrays simultaneously, applying arithmetic and logical operations in correct operator precedence; pixels that fail thresholds or conditions become NaN. For supported in-place functions (threshold, mask, segment, kmeans, otsu, mean, median, percentile, normalise, nantonum, abs), apply them to specified arrays within the evaluation context. Finally, register the resulting image array in the open images with a user-supplied name, overwriting any existing image of that name.

## Related tools

- **pewpew (Pew²)** (GUI application for importing, registering, and managing LA-ICP-MS elemental images; provides the Calculator module that executes formula parsing and evaluation) — https://github.com/djdt/pewpew
- **pewlib** (Python library underlying pewpew; handles LA-ICP-MS data import and image array representation) — https://github.com/djdt/pewlib

## Evaluation signals

- Resulting image array is registered in open images with the user-supplied name and is accessible for export or further processing.
- Pixel-wise results match expected formula evaluation: arithmetic operations preserve numeric precision, conditionals branch correctly per-pixel, and NaN propagation follows IEEE rules.
- Built-in function results (threshold, mask, segment, kmeans, otsu, mean, median, percentile, normalise, nantonum, abs) are applied correctly to specified input arrays and do not affect other open images.
- Formula parser correctly tokenizes and validates all isotope references; references to non-existent images or malformed syntax are rejected with informative error messages.
- Output image dimensions and coordinate alignment match the input arrays; pixels are aligned 1:1 with the input element channels.

## Limitations

- Formula must reference only isotope names that are already loaded and registered as open images in pewpew; dynamic image loading is not supported within the formula string.
- Supported functions are limited to: threshold, mask, segment, kmeans, otsu, mean, median, percentile, normalise, nantonum, abs. User-defined functions or external library calls are not supported.
- NaN propagation is strict: any arithmetic operation involving NaN produces NaN; users must explicitly use nantonum() to replace NaN values before operations.
- Performance scales with image dimensions and formula complexity; very large images or deeply nested conditional branches may be slow.
- Conditional branching (if/then/else) is evaluated per-pixel independently; vectorized short-circuit evaluation is not optimized.

## Evidence

- [other] Pew² provides a Calculator module that evaluates per-pixel expressions over element channels to produce new derived image arrays: "Pew² provides a Calculator module that evaluates per-pixel expressions over element channels to produce new derived image arrays, supporting conditional logic and arithmetic operations on elemental"
- [other] Parse formula string using recursive descent or expression-tree parser to tokenize element references, operators, and control-flow keywords: "Parse the formula string using a recursive descent or expression-tree parser to tokenize element references (e.g., P31, Zn66), mathematical operators (+, −, ×, ÷, ^), and control-flow keywords"
- [other] Validate each referenced isotope name against the open image registry and load corresponding pixel arrays: "Validate each referenced isotope name against the open image registry and load corresponding pixel arrays."
- [other] Evaluate the AST element-wise (pixel-by-pixel) over all arrays simultaneously, applying arithmetic, comparison, and logical operations in correct precedence: "Evaluate the AST element-wise (pixel-by-pixel) over all arrays simultaneously, applying arithmetic, comparison, and logical operations in correct precedence."
- [other] Handle NaN propagation and conditionals: pixels failing thresholds become NaN; conditionals branch per-pixel: "Handle NaN propagation and conditionals: pixels failing thresholds become NaN; conditionals branch per-pixel."
- [other] Supported functions (threshold, mask, segment, kmeans, otsu, mean, median, percentile, normalise, nantonum, abs) are applied to specified arrays in-place within the evaluation context: "For supported functions (threshold, mask, segment, kmeans, otsu, mean, median, percentile, normalise, nantonum, abs), apply them to specified arrays in-place within the evaluation context."
- [readme] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib"
