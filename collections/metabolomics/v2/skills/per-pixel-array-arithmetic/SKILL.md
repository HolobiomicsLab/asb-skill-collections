---
name: per-pixel-array-arithmetic
description: Use when you have multiple registered LA-ICP-MS elemental images (e.g.,
  P31, Zn66 intensity maps) and need to compute a new derived image by applying per-pixel
  operations—such as elemental ratios, thresholding, masking, or conditional logic—across
  channels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3673
  - http://edamontology.org/topic_0769
  tools:
  - Calculator
  - pewpew
  - pewlib
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c02138
  title: Pew2
- doi: 10.1529/biophysj.103.038422
  title: ''
evidence_spans:
- The built in `Calculator` can perform simple calculations on image data by entering
  the desired formula into the `Formula` text box
- The built in `Filtering Tool` removes spikes by comparing pixel values to a locally
  defined threshold
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02138
  all_source_dois:
  - 10.1021/acs.analchem.1c02138
  - 10.1529/biophysj.103.038422
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# per-pixel-array-arithmetic

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Evaluate mathematical expressions element-wise across multiple LA-ICP-MS elemental image arrays to produce derived quantitative images. This skill enables users to create new imaging layers by applying arithmetic, comparison, and conditional logic to pixel values from different isotope channels simultaneously.

## When to use

You have multiple registered LA-ICP-MS elemental images (e.g., P31, Zn66 intensity maps) and need to compute a new derived image by applying per-pixel operations—such as elemental ratios, thresholding, masking, or conditional logic—across channels. Use this when exploratory analysis or protocol design requires on-the-fly computation of ratios, differences, or segmented subsets without pre-computing or exporting intermediate arrays.

## When NOT to use

- The input images are not aligned or have mismatched pixel dimensions—per-pixel arithmetic requires spatial correspondence.
- You need to compute aggregate statistics (e.g., mean, median) across the entire image rather than per-pixel values; use summary statistics tools instead.
- Formula references isotopes or image names not present in the open registry; validation will fail before evaluation.

## Inputs

- open LA-ICP-MS elemental image array (e.g., P31, Zn66 pixel intensity maps)
- formula string with element references, operators, and optional conditionals
- optional: mask or threshold images for conditional evaluation

## Outputs

- derived image array (new or overwritten) with per-pixel computed values
- registered image in the open image registry with user-supplied name

## How to apply

Parse the user-supplied formula string (e.g., 'P31 / Zn66', 'if(Fe > 100, Fe - Mn, NaN)') using a recursive descent parser to tokenize element references, operators (+, −, ×, ÷, ^), and control-flow keywords (if/then/else or ternary ?:). Validate each isotope name against the open image registry and load the corresponding pixel arrays. Build an abstract syntax tree separating arithmetic expressions, comparisons, and conditional branches. Evaluate the AST element-wise (pixel-by-pixel) over all arrays simultaneously, applying operations in correct precedence. Apply supported in-place functions (threshold, mask, segment, kmeans, otsu, mean, median, percentile, normalise, nantonum, abs) to specified arrays within the evaluation context. Handle NaN propagation: pixels failing thresholds become NaN; conditionals branch per-pixel. Register the result as a new image with the user-supplied name, overwriting if the name already exists.

## Related tools

- **pewpew** (GUI application that provides the Calculator module and image registration context for per-pixel formula evaluation over LA-ICP-MS elemental layers) — https://github.com/djdt/pewpew
- **pewlib** (Python library underlying pewpew; provides array I/O, image data structures, and image registry for formula evaluation) — https://github.com/djdt/pewlib

## Evaluation signals

- Formula parses without syntax error and all referenced element names are present in the open image registry.
- Output array has identical pixel dimensions (shape) as input images and contains numeric or NaN values only.
- Spot-checks of output pixels match hand-calculated results for representative input values (e.g., verify P31/Zn66 ratio at a known pixel location).
- NaN propagation is correct: pixels that fail conditionals or thresholds are NaN; valid pixels contain expected arithmetic results.
- New image is registered and visible in the image list; existing images with the same name are overwritten without error.

## Limitations

- All input images must have identical pixel dimensions and spatial alignment; mismatched shapes will cause evaluation failure.
- NaN handling is propagating: any NaN in an operand propagates through arithmetic, so input images with excessive missing data may yield mostly NaN output.
- Supported functions (threshold, mask, segment, kmeans, otsu, mean, median, percentile, normalise, nantonum, abs) are limited to those explicitly implemented in the Calculator; custom functions are not supported.
- Performance scales linearly with image size and formula complexity; very large images (>1 GB) or deeply nested conditionals may be slow.

## Evidence

- [other] Pew² provides a Calculator module that evaluates per-pixel expressions over element channels to produce new derived image arrays, supporting conditional logic and arithmetic operations on elemental data.: "Pew² provides a Calculator module that evaluates per-pixel expressions over element channels to produce new derived image arrays, supporting conditional logic and arithmetic operations on elemental"
- [other] Parse the formula string using a recursive descent or expression-tree parser to tokenize element references (e.g., P31, Zn66), mathematical operators (+, −, ×, ÷, ^), and control-flow keywords (if/then/else or ternary ?:).: "Parse the formula string using a recursive descent or expression-tree parser to tokenize element references (e.g., P31, Zn66), mathematical operators (+, −, ×, ÷, ^), and control-flow keywords"
- [other] Evaluate the AST element-wise (pixel-by-pixel) over all arrays simultaneously, applying arithmetic, comparison, and logical operations in correct precedence.: "Evaluate the AST element-wise (pixel-by-pixel) over all arrays simultaneously, applying arithmetic, comparison, and logical operations in correct precedence."
- [other] Handle NaN propagation and conditionals: pixels failing thresholds become NaN; conditionals branch per-pixel.: "Handle NaN propagation and conditionals: pixels failing thresholds become NaN; conditionals branch per-pixel."
- [readme] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data"
