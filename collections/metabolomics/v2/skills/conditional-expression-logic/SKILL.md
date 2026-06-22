---
name: conditional-expression-logic
description: 'Use when you need to create a derived image array where the output value at each pixel depends conditionally on the values of one or more element channels at that pixel. Common triggers include: (1) you want to mask or zero out pixels where an element concentration falls below a detection limit;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3070
  - http://edamontology.org/topic_3382
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

# Conditional Expression Logic in Per-Pixel Elemental Calculations

## Summary

This skill enables users to embed conditional branching (if/then/else or ternary operators) directly into per-pixel mathematical expressions over LA-ICP-MS elemental channels, allowing dynamic filtering and selective computation based on pixel-level thresholds. It is essential when deriving new image arrays that depend on element ratios, abundance thresholds, or logical gates applied element-wise across hyperspectral data.

## When to use

Apply this skill when you need to create a derived image array where the output value at each pixel depends conditionally on the values of one or more element channels at that pixel. Common triggers include: (1) you want to mask or zero out pixels where an element concentration falls below a detection limit; (2) you need to select pixels based on a ratio threshold (e.g., Zn/Cu > 2); (3) you want to assign different computed values depending on which element dominates; (4) you are implementing a multi-channel classification where pixel assignment depends on logical conditions (e.g., 'if P31 > threshold AND Zn66 < limit, then assign group A'). Do NOT use this skill for non-conditional arithmetic or when the expression can be fully evaluated without branching logic.

## When NOT to use

- Input expression is purely arithmetic with no conditional branches — use simple per-pixel arithmetic instead.
- All pixels are expected to satisfy the condition identically (i.e., no branching is needed) — simplify to deterministic computation.
- The desired behavior is row-wise or image-wise filtering rather than per-pixel selection — use Region selection or global Threshold tools instead.

## Inputs

- Formula string containing element references, conditional operators (if/then/else or ternary ?:), arithmetic operators (+, −, ×, ÷, ^), and comparison operators (>, <, ==, !=, >=, <=)
- Open LA-ICP-MS image registry containing elemental channel arrays (one array per isotope, e.g., P31, Zn66)
- Per-pixel values (float arrays with potential NaN entries)

## Outputs

- New derived image array with per-pixel conditional results registered in the open images registry
- Array name (user-supplied or overwritten if it already exists)

## How to apply

Within the Calculator module of pewpew, parse the user-supplied formula string containing element references (e.g., P31, Zn66), conditional operators (if/then/else or ternary ?:), and arithmetic/comparison operators. Validate all referenced isotope names against the open image registry and load the corresponding pixel arrays. Construct an abstract syntax tree (AST) that separates arithmetic expressions, comparisons, and conditional branches, ensuring correct operator precedence. Evaluate the AST element-wise across all pixels simultaneously: for each pixel, resolve all comparisons (e.g., P31 > 100), follow conditional branches per-pixel (pixels meeting the condition take the 'then' branch; others take the 'else' branch), and compute the result. Handle NaN propagation: pixels that fail thresholds or comparisons within conditionals become NaN. Register the resulting array in the open images registry under the user-supplied name, or overwrite an existing image if the name is already in use. Correctness depends on verifying that pixel values follow the expected branching pattern when sampled across regions known to satisfy or fail the condition.

## Related tools

- **pewpew** (GUI environment providing the Calculator module that parses, validates, and evaluates conditional expressions over multi-channel LA-ICP-MS images) — https://github.com/djdt/pewpew
- **pewlib** (Python library underlying pewpew; implements the expression parser, AST construction, per-pixel evaluation logic, and image array registration) — https://github.com/djdt/pewlib

## Examples

```
Within pewpew Calculator: `if (Zn66 > 100) then (P31 / Zn66) else NaN` evaluates the ratio P31/Zn66 only for pixels where Zn66 exceeds 100 counts, setting all other pixels to NaN in the derived image.
```

## Evaluation signals

- Spot-check a subset of pixels known to satisfy the condition; verify their output matches the 'then' branch value.
- Spot-check a subset of pixels known to fail the condition; verify their output matches the 'else' branch value or is NaN.
- Verify that NaN values propagate correctly: pixels with NaN inputs or that fail thresholds within the condition yield NaN output.
- Confirm the new image is registered in the open images list with the expected name and correct pixel dimensions matching the input channels.
- Overlay the derived image against original channels to visually confirm spatial patterns align with expected conditional logic (e.g., derived values are concentrated in regions where the condition is met).

## Limitations

- Expression parser uses recursive descent or expression-tree parsing; complex nested conditionals with many branches may suffer performance degradation at scale (millions of pixels).
- NaN propagation follows pixel-wise rules; if any input to a comparison or arithmetic operation is NaN, the result becomes NaN — no fallback or imputation is applied automatically.
- Supported functions (threshold, mask, segment, kmeans, otsu, mean, median, percentile, normalise, nantonum, abs) can be called within conditionals but are applied in-place; order of operations matters and may not be transparent if nested deeply.
- No explicit support for user-defined functions or macros; all operations must be expressible in the formula string using built-in operators and keywords.

## Evidence

- [other] Pew² provides a Calculator module that evaluates per-pixel expressions over element channels to produce new derived image arrays, supporting conditional logic and arithmetic operations on elemental data.: "Pew² provides a Calculator module that evaluates per-pixel expressions over element channels to produce new derived image arrays, supporting conditional logic and arithmetic operations on elemental"
- [other] Parse the formula string using a recursive descent or expression-tree parser to tokenize element references (e.g., P31, Zn66), mathematical operators (+, −, ×, ÷, ^), and control-flow keywords (if/then/else or ternary ?:).: "Parse the formula string using a recursive descent or expression-tree parser to tokenize element references (e.g., P31, Zn66), mathematical operators (+, −, ×, ÷, ^), and control-flow keywords"
- [other] Evaluate the AST element-wise (pixel-by-pixel) over all arrays simultaneously, applying arithmetic, comparison, and logical operations in correct precedence.: "Evaluate the AST element-wise (pixel-by-pixel) over all arrays simultaneously, applying arithmetic, comparison, and logical operations in correct precedence."
- [other] Handle NaN propagation and conditionals: pixels failing thresholds become NaN; conditionals branch per-pixel.: "Handle NaN propagation and conditionals: pixels failing thresholds become NaN; conditionals branch per-pixel."
- [other] Create a new image array from the result and register it in the open images with the user-supplied name, or if the name already exists, overwrite the existing image data.: "Create a new image array from the result and register it in the open images with the user-supplied name, or if the name already exists, overwrite the existing image data."
- [readme] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library [pewlib](https://github.com/djdt/pewlib).: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library [pewlib]"
