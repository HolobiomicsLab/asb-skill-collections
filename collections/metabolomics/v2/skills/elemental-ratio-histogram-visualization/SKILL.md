---
name: elemental-ratio-histogram-visualization
description: 'Use when after loading a numeric elemental ratio column (H/C, O/C, N/C, etc.) from a CSV file into Punc''data, when you need to visualize the distribution of molecular formulas across a sample and want bin spacing to adapt automatically: narrow bins (0.1) for low-range data (span ≤ 3.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.5c00151
  all_source_dois:
  - 10.1021/jasms.5c00151
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# elemental-ratio-histogram-visualization

## Summary

Render adaptive-binwidth histograms of elemental ratio columns (H/C, O/C, etc.) in Punc'data, with automatic bin-width selection based on data range to reveal distribution patterns in complex mass spectrometry mixtures.

## When to use

After loading a numeric elemental ratio column (H/C, O/C, N/C, etc.) from a CSV file into Punc'data, when you need to visualize the distribution of molecular formulas across a sample and want bin spacing to adapt automatically: narrow bins (0.1) for low-range data (span ≤ 3.0) to reveal fine structure, or wider bins (1.0) for high-range data (span > 3.0) to avoid over-binning.

## When NOT to use

- Input column contains non-numeric values or missing data without prior imputation—histogram generation will fail or misalign bins.
- Data has already been pre-binned or aggregated into a frequency table—re-binning risks double-discretization and loss of resolution.
- Elemental ratio is categorical or ordinal (e.g., 'saturated', 'unsaturated') rather than continuous numeric—the adaptive threshold rule does not apply.

## Inputs

- Numeric column vector (elemental ratio: H/C, O/C, N/C, etc.) from CSV file
- CSV file with column delimiters (semicolon, comma, etc.) and first row column headers
- Punc'data session or tabular data with recognized elemental ratio keywords

## Outputs

- Interactive histogram rendered in Canvas tab with adaptive bin spacing
- Bin boundary coordinates matching the selected bin width (0.1 or 1.0)
- Frequency counts per bin displaying elemental ratio distribution

## How to apply

Load a numeric column recognized by Punc'data's keyword-based column recognition (e.g., 'H/C ratio', 'O/C ratio') from an uploaded CSV file with delimited columns. Calculate the span as max − min of the column values. Apply the adaptive bin-width rule: if span ≤ 3.0, set histogram bin width to 0.1; otherwise set bin width to 1.0. This threshold balances statistical granularity for tightly clustered elemental ratios against readability for widely dispersed ratios. Generate and render the histogram in the Canvas tab. Validate by inspecting rendered bin boundaries and verifying alignment with the threshold—bins should cluster densely near the mean for low-span data and spread evenly across the range for high-span data.

## Related tools

- **Punc'data** (Interactive visualization and canvas rendering engine for histogram generation with adaptive bin-width selection and column keyword recognition for elemental ratios) — https://github.com/WTVoe/puncdata

## Evaluation signals

- Histogram bin width is 0.1 when data span (max − min) ≤ 3.0, and 1.0 when span > 3.0.
- Bin boundaries align cleanly with the selected width: e.g., bins at [0.0, 0.1, 0.2, …] or [0.0, 1.0, 2.0, …].
- Frequency counts in each bin sum to the total number of non-missing values in the input column.
- Visual inspection shows fine-grained distribution detail (multiple bins with counts) for low-span data, and smooth broad distribution envelope for high-span data.
- Canvas tab renders histogram interactively without errors or gaps in bin coverage across the observed range.

## Limitations

- No specification in documentation of handling for negative elemental ratios (e.g., if O/C < 0 due to data errors)—threshold rule assumes non-negative or signed continuous range.
- Adaptive bin-width rule (threshold at 3.0) is empirical and not statistically validated; optimal threshold may differ for specific mass spectrometry workflows or sample types.
- Column recognition is keyword-based and may fail or misidentify columns if naming conventions deviate from expected patterns (m/z, intensity, formula keywords).
- No validation criteria or quality control metrics documented for data format beyond CSV; handling of missing values, outliers, or extreme ranges is not specified.

## Evidence

- [other] Adaptive bin-width rule from task card: "Compare the span against the threshold of 3.0: if span ≤ 3.0, set histogram bin width to 0.1; otherwise, set bin width to 1.0."
- [readme] Column recognition mechanism: "Punc'data recognizes which column corresponds to which information based on keywords."
- [readme] Canvas rendering and visualization tabs: ""Table", "Stats", "Canvas A/B" and "Network" allow different types of tables and charts to be produced. On Canvas A,B and Stats, charts are interactive."
- [readme] Input file format requirement: "To vizualise data, you need to upload a file with separation (; , ...) between the columns. The first line of any uploaded file has to be the title of each column."
- [readme] Application domain and sample types: "Punc'data is an interactive attribution and vizualization tool made for high resolution mass spectrometry results. It is used to filter, select, observe, comment and transmit information on results"
