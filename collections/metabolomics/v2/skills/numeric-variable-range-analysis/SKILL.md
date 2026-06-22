---
name: numeric-variable-range-analysis
description: Use when you have loaded a numeric column (e.g., H/C ratio, O/C ratio, m/z value, or intensity) from a CSV file into Punc'data and need to render a histogram with appropriate bar spacing. The skill is triggered when the range of the column is small enough that default bin widths (1.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - Punc'data
  - puncdata (GitHub repository)
  techniques:
  - mass-spectrometry
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00151
  all_source_dois:
  - 10.1021/jasms.5c00151
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# numeric-variable-range-analysis

## Summary

Analyze the span (max–min) of a numeric variable column to determine an adaptive visualization parameter (histogram bin width) in mass spectrometry data. This skill bridges data profiling and interactive rendering by applying a threshold rule that switches bin spacing based on the spread of the data.

## When to use

Apply this skill when you have loaded a numeric column (e.g., H/C ratio, O/C ratio, m/z value, or intensity) from a CSV file into Punc'data and need to render a histogram with appropriate bar spacing. The skill is triggered when the range of the column is small enough that default bin widths (1.0) would produce sparse or unreadable histograms, requiring finer granularity (0.1) for interpretability.

## When NOT to use

- Input is a categorical or string column (non-numeric) — the span calculation is undefined.
- Histogram bin width is already user-specified or fixed by prior analysis — applying an adaptive rule would override explicit user intent.
- Data contains only missing or NaN values — max/min cannot be computed.

## Inputs

- numeric column from CSV file (e.g., H/C ratio, O/C ratio, intensity)
- column metadata recognized by Punc'data keyword system
- max and min values of the numeric column

## Outputs

- histogram bin width parameter (0.1 or 1.0)
- rendered histogram in Punc'data Canvas tab with adaptive bar spacing
- bin boundary alignment validated against threshold rule

## How to apply

Load a numeric column using Punc'data's column recognition system, which identifies column role based on keywords (m/z, intensity, formula, H/C ratio, O/C ratio). Calculate the span as (max – min) of the column values. Compare the span against a threshold of 3.0: if span ≤ 3.0, set the histogram bin width to 0.1; otherwise, use bin width 1.0. Generate and render the histogram in Punc'data's Canvas tab using the selected bin width. The rationale is that narrow-range variables require finer bin granularity to avoid collapsing multiple distinct values into single bars, while wide-range variables benefit from coarser binning to reduce visual clutter.

## Related tools

- **Punc'data** (interactive visualization and histogram rendering platform that implements the adaptive bin-width rule; loads CSV columns, recognizes numeric roles by keyword, and renders histograms in the Canvas tab) — https://wtvoe.github.io/puncdata/
- **puncdata (GitHub repository)** (source code repository for Punc'data; contains the HTML/CSS/JavaScript implementation of column recognition and Canvas rendering) — https://github.com/WTVoe/puncdata

## Evaluation signals

- Bin width is 0.1 when span ≤ 3.0 and 1.0 when span > 3.0, indicating correct threshold comparison.
- Rendered histogram bar boundaries align with the expected bin edges (e.g., 0.0, 0.1, 0.2, … for 0.1 width or 0.0, 1.0, 2.0, … for 1.0 width).
- Visual inspection confirms that bins do not collapse multiple distinct values (fine bins for narrow ranges) and are not excessively sparse (coarse bins for wide ranges).
- Column is correctly recognized by Punc'data keyword system (verified in 'parameters' tab before Canvas rendering).
- No gaps or misalignments in the histogram that would indicate incorrect bin width application.

## Limitations

- The threshold value (3.0) and bin widths (0.1 vs. 1.0) are hardcoded; no evidence in the provided documentation of user-configurable thresholds or alternative bin width schemes.
- No statistical validation or benchmark data provided in the article or README to justify the 3.0 threshold; the rule is empirically derived and may not generalize to all numeric domains (e.g., very large intensity values or extreme H/C ratios).
- The skill assumes CSV input with proper column delimiters; malformed files or non-standard separators may prevent correct column recognition and range calculation.
- No handling documented for outliers, skewed distributions, or multimodal data; the rule operates only on the global max–min span and does not account for data shape.

## Evidence

- [other] Range-based bin-width rule definition: "Calculate the max and min values of the column to determine the span (max – min). Compare the span against the threshold of 3.0: if span ≤ 3.0, set histogram bin width to 0.1; otherwise, set bin"
- [readme] Column recognition system: "Punc'data recognizes which column corresponds to which information based on keywords."
- [readme] Numeric column input (example roles): "Each line must represent an attribution or m/z values. Column represent data : m/z value, intensity, formula..."
- [readme] Canvas rendering of histogram: ""Table", "Stats", "Canvas A/B" and "Network" allow different types of tables and charts to be produced. On Canvas A,B and Stats, charts are  interactive."
- [readme] CSV file upload with delimiter: "To vizualise data, you need to upload a file with separation (; , ...) between the columns. You can change the separator with the gear icon"
