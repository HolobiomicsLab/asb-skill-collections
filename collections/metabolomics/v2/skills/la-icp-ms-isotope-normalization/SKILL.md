---
name: la-icp-ms-isotope-normalization
description: Use when you have multi-isotope LA-ICP-MS data (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
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

# LA-ICP-MS Isotope Normalization

## Summary

Normalize elemental abundance or intensity data in LA-ICP-MS images by ratioing one isotope channel against another (e.g., dividing by a reference isotope or internal standard) to correct for ablation efficiency, plasma conditions, or matrix effects. This skill is essential when deriving quantitative elemental ratios or correcting for instrumental drift across line-by-line, spot-wise, or ablation-time-aligned acquisitions.

## When to use

Apply this skill when you have multi-isotope LA-ICP-MS data (e.g., P31, Zn66, Fe56 from Agilent, Thermo iCap, or PerkinElmer instruments) and need to convert raw intensity counts into normalized ratios—either to correct for matrix-dependent sensitivity differences, to normalize against a known internal standard, or to create derived elemental ratio images for downstream colocalization or quantitative analysis. Typical triggers: (1) intensity values vary across the ablation due to laser power or plasma drift, (2) you need to express results as element-to-element ratios rather than absolute intensities, or (3) you are comparing multiple samples imaged under different conditions.

## When NOT to use

- When the reference (denominator) isotope channel contains no meaningful signal or is saturated across most pixels—the result will be dominated by NaN or noise.
- When only single-isotope data is available (normalization requires at least two isotope channels); use direct intensity export instead.
- When absolute quantification is required and no external calibration curve or certified standard has been measured; normalization alone does not convert ratios to concentration units.

## Inputs

- LA-ICP-MS multi-isotope image arrays (one per isotope channel, e.g., P31, Zn66, Fe56)
- Imported line-by-line, spot-wise, or ablation-time-aligned LA-ICP-MS data from Agilent, Thermo iCap, PerkinElmer, or CSV formats
- Internal standard or reference isotope intensity array (designated by user)

## Outputs

- Derived isotope ratio image array (e.g., Zn66/Fe56 or P31/Fe56 as new named image)
- Pixel-by-pixel normalized elemental abundance or intensity ratios with NaN propagation for invalid pixels
- Registered image in the open image registry (pewpew) ready for visualization, further filtering, or export

## How to apply

Load all desired isotope channels into pewpew as separate image arrays (one per isotope) using the import dialog for your instrument format (Agilent .b, Thermo CSV/LDR, PerkinElmer .xl, or generic CSV). Then use the Calculator module to construct a per-pixel formula that divides the target isotope array by the reference isotope array (e.g., `Zn66 / Fe56` or `(P31 + S34) / Fe56`). The Calculator parses the expression, validates each referenced isotope against the open image registry, builds an abstract syntax tree, and evaluates it element-wise (pixel-by-pixel) across all arrays. Any pixels where the denominator is zero or NaN will automatically become NaN in the output. Register the result as a new named image. For robust normalization, consider applying a threshold, rolling median, or rolling mean filter to the denominator channel before division to suppress noise-driven artifacts. After normalization, export the derived ratio image(s) for quantitative comparison across samples or regions.

## Related tools

- **pewlib** (Core Python library that provides LA-ICP-MS data import, array representation, and per-pixel arithmetic operations required to load multi-isotope channels and compute normalized ratios) — https://github.com/djdt/pewlib
- **pewpew** (GUI application (built on pewlib) for interactive import of multi-format LA-ICP-MS data, visual registration and alignment of multi-isotope images, and Calculator module for constructing and evaluating per-pixel isotope ratio formulas) — https://github.com/djdt/pewpew
- **Calculator** (Submodule within pewpew that parses and evaluates per-pixel mathematical expressions over element channels to produce normalized ratio arrays, supporting arithmetic operations, conditional logic, and built-in filter functions (rolling mean/median, threshold, mask, segment, kmeans, otsu)) — https://github.com/djdt/pewpew

## Evaluation signals

- Derived ratio image array is successfully registered in pewpew's open image registry with the user-supplied name (or overwrites an existing image if name collision occurs).
- Pixel-by-pixel ratio values are computed correctly: spot-check a subset of pixels by manually dividing numerator by denominator intensities; results should match within machine precision.
- NaN propagation is correct: pixels where denominator is zero or NaN should produce NaN in the output ratio; non-NaN outputs should have finite, non-negative values if both numerator and denominator are positive.
- Visualization of the ratio image in pewpew shows spatial structure consistent with the underlying isotope distributions (e.g., high ratios in regions where target isotope is abundant and reference isotope is depleted; smooth gradients absent sudden artifacts).
- Export of the ratio image produces a valid output file (CSV, HDF5, or other format) with dimensions matching the input LA-ICP-MS acquisition grid and values consistent with re-import and re-calculation.

## Limitations

- NaN pixels in the reference (denominator) isotope channel propagate as NaN in the output ratio, potentially reducing the valid pixel count significantly if the reference channel is noisy or has low signal.
- The Calculator does not currently support external calibration curves or physical unit conversion; normalized ratios are unitless and relative, not absolute concentrations. A separate post-processing step (e.g., external standard comparison or matrix-matched calibration) is required for quantitative calibration.
- Normalization by a variable reference isotope does not account for mass fractionation, instrumental mass bias, or laser-induced elemental fractionation differences between the target and reference isotopes; users must validate that the reference isotope behaves as a proxy for the target isotope's acquisition conditions.
- The open-source pewlib/pewpew may not support all proprietary LA-ICP-MS vendor formats; only Agilent, Thermo iCap, PerkinElmer, Nu Instruments, and CSV/ImzML are listed as supported; other formats may require manual conversion.
- Rolling median or mean pre-filtering of the denominator channel may introduce boundary artifacts or suppress genuine spatial heterogeneity; filter parameters should be validated empirically on the target dataset.

## Evidence

- [other] Pew² provides a Calculator module that evaluates per-pixel expressions over element channels to produce new derived image arrays, supporting conditional logic and arithmetic operations on elemental data.: "Pew² provides a Calculator module that evaluates per-pixel expressions over element channels to produce new derived image arrays"
- [other] Parse the formula string using a recursive descent or expression-tree parser to tokenize element references (e.g., P31, Zn66), mathematical operators (+, −, ×, ÷, ^), and control-flow keywords (if/then/else or ternary ?:). Validate each referenced isotope name against the open image registry and load corresponding pixel arrays.: "tokenize element references (e.g., P31, Zn66), mathematical operators (+, −, ×, ÷, ^)"
- [other] Evaluate the AST element-wise (pixel-by-pixel) over all arrays simultaneously, applying arithmetic, comparison, and logical operations in correct precedence.: "Evaluate the AST element-wise (pixel-by-pixel) over all arrays simultaneously, applying arithmetic, comparison, and logical operations"
- [other] Handle NaN propagation and conditionals: pixels failing thresholds become NaN; conditionals branch per-pixel.: "Handle NaN propagation and conditionals: pixels failing thresholds become NaN"
- [readme] Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data using the python library pewlib.: "Pew² is a GUI for importing and processing line-by-line, spot-wise and ablation-time-aligned LA-ICP-MS data"
- [readme] Agilent, Thermo iCap, Perkin Elemer, Nu Intruments, CSV Images and Lines, ImzML, and Iolite Laser Logs are supported formats.: "Agilent, Thermo iCap, Perkin Elemer, Nu Intruments, CSV Images and Lines, ImzML"
- [readme] Pewlib is a library for importing, processing and exporting LA-ICP-MS data. Currently exports from Agilent, Thermo and PerkinElmer software is supported: "Pewlib is a library for importing, processing and exporting LA-ICP-MS data. Currently exports from Agilent, Thermo and PerkinElmer software is supported"
