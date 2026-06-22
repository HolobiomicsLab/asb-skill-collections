---
name: volcano-plot-construction-from-omics-data
description: Use when after statistical analysis (e.g., edgeR) has produced a results table containing lipid identities, fold-change values, and p-values for pairwise or multi-condition comparisons.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0571
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
  tools:
  - matplotlib
  - seaborn
  - pandas
  - edgeR.R
derived_from:
- doi: 10.1021/acs.analchem.4c05039
  title: CLAW-MRM
evidence_spans:
- streamline various tasks such as data parsing, matching, statistical analysis, and visualization
- _No usage/docs found._
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_claw_mrm_cq
    doi: 10.1021/acs.analchem.4c05039
    title: CLAW-MRM
  dedup_kept_from: coll_claw_mrm_cq
schema_version: 0.2.0
---

# volcano-plot-construction-from-omics-data

## Summary

Construct a volcano plot to visualize the relationship between fold-change and statistical significance (p-value) for lipid features across experimental conditions. This enables rapid identification of differentially expressed lipids by encoding both effect size and statistical confidence in a single, publication-quality graphical representation.

## When to use

After statistical analysis (e.g., edgeR) has produced a results table containing lipid identities, fold-change values, and p-values for pairwise or multi-condition comparisons. Use volcano plots when you need to identify and communicate which lipids show both substantial abundance shifts AND statistical significance, filtering out noise from minor changes or marginally significant features.

## When NOT to use

- Input is raw mass spectrometry data (mzML, raw peak intensities) rather than pre-computed fold-changes and p-values—use data parsing and statistical analysis first.
- No statistical test has been performed yet or p-values are unavailable—volcano plots require both effect size and significance metrics.
- Data dimensionality or comparison scope is better served by alternative plots (e.g., heatmap for multi-lipid expression across 3+ conditions, box plot for abundance distributions within a single condition, PCA plot for sample clustering).

## Inputs

- Statistical results table (CSV or tabular format) with columns: lipid identity, fold-change (log2-transformed or raw), p-value, condition labels, optional lipid class annotation

## Outputs

- Volcano plot (PNG or PDF image file, publication-quality resolution)
- Structured plot object (matplotlib Figure or seaborn plot) with axes, thresholds, and legend

## How to apply

Load the statistical results table (CSV or tabular format) containing lipid names, fold-change values, and p-values. Parse and structure the data to extract lipid identities and quantitative values. Select volcano plot as the visualization type because it encodes fold-change (typically log2-transformed) on the x-axis and negative log10(p-value) on the y-axis, allowing simultaneous assessment of effect size and significance. Generate the plot using matplotlib or seaborn, applying threshold lines for biologically or statistically meaningful cutoffs (e.g., |fold-change| > 1.5 or p-value < 0.05). Encode color or shape to distinguish lipid classes or regulatory direction (up- vs. down-regulated). Apply publication-quality formatting with labeled axes, legend, and descriptive title. Export as PNG or PDF at sufficient resolution for print or supplementary materials.

## Related tools

- **matplotlib** (Low-level plotting library for rendering the volcano plot figure, axes, thresholds, and custom annotations)
- **seaborn** (High-level statistical plotting library for enhanced volcano plot aesthetics and publication-quality formatting)
- **pandas** (Data parsing and manipulation library for loading, filtering, and structuring the statistical results table before plotting)
- **edgeR.R** (Upstream R script that performs statistical analysis and produces the fold-change and p-value inputs required for volcano plot construction) — https://github.com/chopralab/CLAW

## Evaluation signals

- Plot correctly encodes fold-change (x-axis) and -log10(p-value) (y-axis) with no axis inversions or unit mismatches.
- Threshold lines are present and positioned at the specified cutoffs (e.g., vertical lines at log2(fold-change) = ±1.5, horizontal line at -log10(p-value) = 1.3 for p = 0.05).
- Color or shape encoding distinguishes lipid classes or regulatory direction, and legend is present and legible.
- Axes are labeled with appropriate units and titles; figure includes a descriptive title referencing the comparison (e.g., 'Fold-Change vs. Significance: Brain Lipids, 5XFAD vs. WT').
- Output image has sufficient resolution (≥300 dpi for print) and file format (PNG or PDF) is suitable for publication or supplementary materials.

## Limitations

- Volcano plots assume a single pairwise comparison; multi-group or time-series analyses may require multiple plots or alternative visualizations (e.g., heatmaps).
- Threshold selection (fold-change and p-value cutoffs) is subjective and should be justified biologically or statistically; the plot itself does not enforce thresholds, only visualizes them.
- Lipids with very large fold-changes or extremely small p-values may compress the plot space, requiring log-transformed or capped axes to maintain visibility of the bulk of the data.
- No changelog is documented in the repository, so version-specific behavior or breaking changes may not be tracked.

## Evidence

- [other] volcano plot for fold-change vs. significance, heatmap for multi-lipid expression across conditions, box plot for abundance distributions, bar plot for ranked lipid levels: "Select appropriate visualization type(s) based on data dimensionality and comparison scope (e.g., volcano plot for fold-change vs. significance, heatmap for multi-lipid expression across conditions,"
- [other] Load the statistical results table (CSV or tabular format) containing lipid identities, expression measurements, p-values, fold-changes, and condition labels: "Load the statistical results table (CSV or tabular format) containing lipid identities, expression measurements, p-values, fold-changes, and condition labels."
- [other] Generate visualization(s) using a plotting library, encoding lipid identity on one axis, expression metric on the other, and applying color/shape encoding for condition, significance, or lipid class distinctions: "Generate visualization(s) using a plotting library, encoding lipid identity on one axis, expression metric on the other, and applying color/shape encoding for condition, significance, or lipid class"
- [other] Apply publication-quality formatting: labeled axes, legend, title, and threshold lines (e.g., p-value or fold-change cutoff) where applicable: "Apply publication-quality formatting: labeled axes, legend, title, and threshold lines (e.g., p-value or fold-change cutoff) where applicable."
- [other] matplotlib, seaborn, pandas: "tools: matplotlib, seaborn, pandas"
