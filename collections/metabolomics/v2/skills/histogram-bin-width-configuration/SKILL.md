---
name: histogram-bin-width-configuration
description: Use when you have uploaded a numeric column (e.g., H/C ratio, O/C ratio, or other derived properties from high-resolution mass spectrometry) and you are generating a histogram in Punc'data's Canvas tab.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Punc'data
derived_from:
- doi: 10.1021/jasms.5c00151
  title: Punc’data
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_punc_data_cq
    doi: 10.1021/jasms.5c00151
    title: Punc’data
  dedup_kept_from: coll_punc_data_cq
schema_version: 0.2.0
---

# histogram-bin-width-configuration

## Summary

Dynamically adjust histogram bin width in Punc'data based on the numeric range (max – min) of a column to optimize visualization granularity for mass spectrometry data. This skill applies an adaptive rule that switches bin spacing from coarse (1.0) to fine (0.1) when the column span is small, improving readability of narrowly distributed variables like H/C or O/C ratios.

## When to use

Apply this skill when you have uploaded a numeric column (e.g., H/C ratio, O/C ratio, or other derived properties from high-resolution mass spectrometry) and you are generating a histogram in Punc'data's Canvas tab. The skill is triggered when the visual distribution of the column appears too coarse or too fine, indicating that the default bin width does not match the scale of the data.

## When NOT to use

- The column is categorical or non-numeric (e.g., formula strings, sample IDs).
- The histogram bin width has already been manually specified by the user and requires no automatic adjustment.
- The span calculation is undefined or the column contains missing or invalid numeric values.

## Inputs

- Numeric column from CSV file (e.g., H/C ratio, O/C ratio, or derived mass spectrometry property)
- Column metadata (max value, min value, span calculation)

## Outputs

- Interactive histogram visualization in Punc'data Canvas tab
- Histogram with adaptive bin width (0.1 or 1.0) appropriate to data range

## How to apply

First, load a numeric column into Punc'data's column recognition system by uploading a CSV file with appropriate delimiters and column headers. Punc'data will auto-recognize columns via keywords (e.g., 'm/z value', 'intensity', 'formula'). Next, calculate or inspect the range span (max – min) of the column. Apply the adaptive bin-width rule: if span ≤ 3.0, set the histogram bin width to 0.1 for finer resolution; otherwise, use bin width 1.0. Generate and render the histogram in the Canvas A or B tab with the selected bin width. Validate the result by inspecting the rendered bar boundaries and verifying that they align with the threshold-driven choice—bars should be visibly tighter and more granular when span ≤ 3.0, and coarser when span > 3.0.

## Related tools

- **Punc'data** (Interactive visualization and histogram rendering engine; applies column recognition and Canvas-based chart generation with configurable bin widths.) — https://github.com/WTVoe/puncdata

## Evaluation signals

- Bin width matches the expected rule: verify that span ≤ 3.0 produces bins of width 0.1 and span > 3.0 produces bins of width 1.0.
- Histogram bar boundaries align exactly with the configured bin width; inspect the tick labels and bin edges on the Canvas.
- Visual distribution of bars reflects the narrowness or breadth of the data range; narrow ranges should show fine granularity, wide ranges should show coarse grouping.
- No visual artifacts or rendering errors appear when switching between bin widths; the canvas updates smoothly and interactively.
- The rule is applied consistently across multiple numeric columns in the same session.

## Limitations

- The threshold of 3.0 for switching bin width is fixed and not user-configurable in the documented interface; generalization to other domains or column types is not specified.
- No evidence in the provided documentation describes validation of the bin-width rule against standard datasets or statistical benchmarks.
- The rule assumes that all numeric columns follow a similar distribution pattern; highly skewed or multimodal distributions may not render optimally even with adaptive binning.
- The article and README provide no discussion of how the threshold (3.0) was derived or validated; replicability and scientific rationale are not provided.

## Evidence

- [other] Calculate the max and min values of the column to determine the span (max – min). Compare the span against the threshold of 3.0: if span ≤ 3.0, set histogram bin width to 0.1; otherwise, set bin width to 1.0.: "Calculate the max and min values of the column to determine the span (max – min). Compare the span against the threshold of 3.0: if span ≤ 3.0, set histogram bin width to 0.1; otherwise, set bin"
- [readme] Punc'data recognizes which column corresponds to which information based on keywords.: "Punc'data recognizes which column corresponds to which information based on keywords."
- [readme] "Table", "Stats", "Canvas A/B" and "Network" allow different types of tables and charts to be produced. On Canvas A,B and Stats, charts are interactive.: ""Table", "Stats", "Canvas A/B" and "Network" allow different types of tables and charts to be produced. On Canvas A,B and Stats, charts are interactive."
- [readme] To vizualise data, you need to upload a file with separation (; , ...) between the columns.: "To vizualise data, you need to upload a file with separation (; , ...) between the columns."
