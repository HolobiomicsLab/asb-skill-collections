---
name: lipid-expression-pattern-visualization
description: Use when after statistical analysis of lipid abundance data has produced a table of lipid identities, expression measurements, p-values, fold-changes, and condition labels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - matplotlib
  - seaborn
  - pandas
  - plotly
  techniques:
  - mass-spectrometry
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05039
  all_source_dois:
  - 10.1021/acs.analchem.4c05039
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-expression-pattern-visualization

## Summary

Transform statistical lipidomics results (p-values, fold-changes, lipid identities) into publication-quality graphical outputs encoding expression patterns, significance, and lipid class distinctions. This skill bridges CLAW-MRM's statistical analysis phase and final figure export for multi-condition lipid abundance comparisons.

## When to use

After statistical analysis of lipid abundance data has produced a table of lipid identities, expression measurements, p-values, fold-changes, and condition labels. Use this skill when you need to communicate relative lipid levels, fold-change significance, or cross-condition expression patterns to stakeholders or for manuscript/supplement figures.

## When NOT to use

- Input is raw mass spectrometry data (mzML files) or unprocessed lipid peak lists — use data parsing and matching skills first.
- Statistical analysis has not yet been performed — this skill assumes fold-changes, p-values, and condition labels already exist in tabular form.
- Goal is exploratory data quality assessment before statistical testing — use intermediate QC plots (e.g., PCA, ridge plots) instead.

## Inputs

- statistical results table (CSV or tabular format) with columns: lipid identities, expression measurements, p-values, fold-changes, condition labels
- experimental design metadata specifying sample grouping variables and condition classes

## Outputs

- publication-quality figure(s) in PNG or PDF format encoding lipid expression patterns
- visualization with labeled axes, legend, title, and threshold lines

## How to apply

Load the statistical results table (CSV or tabular format) using pandas and extract lipid names, quantitative values, and grouping variables (experimental conditions or sample classes). Select an appropriate visualization type based on analysis scope: volcano plot to show fold-change vs. statistical significance, heatmap for multi-lipid expression across conditions, box plot for abundance distributions within conditions, or bar plot for ranked lipid levels. Encode lipid identity on one axis and expression metric on the other; use color/shape encoding to distinguish condition, significance status (e.g., p-value threshold), or lipid class. Apply publication-quality formatting including labeled axes, legend, title, and threshold lines (e.g., p-value or fold-change cutoff where applicable). Export to PNG or PDF at sufficient resolution for print or online supplement.

## Related tools

- **matplotlib** (low-level plotting library for generating figure objects, axes, and line/scatter/bar renderings)
- **seaborn** (high-level statistical visualization library for heatmaps, box plots, and publication-quality defaults)
- **pandas** (data loading, parsing, and structuring statistical results into plot-ready DataFrames)
- **plotly** (interactive plotting library for exploratory and web-ready lipid expression visualizations)

## Examples

```
import pandas as pd; import matplotlib.pyplot as plt; import seaborn as sns; results = pd.read_csv('Pre_EdgeR/statistical_results.csv'); volcano = plt.figure(); ax = volcano.add_subplot(111); ax.scatter(results['logFC'], -np.log10(results['PValue']), c=(results['PValue']<0.05), cmap='RdYlBu'); ax.axhline(-np.log10(0.05), color='gray', linestyle='--'); ax.set_xlabel('log2(fold-change)'); ax.set_ylabel('-log10(p-value)'); plt.savefig('Plots/volcano_plot.pdf', dpi=300, bbox_inches='tight')
```

## Evaluation signals

- All lipid identities from the input table are represented in the visualization (no silent filtering or truncation).
- Axis labels include units and lipid metric names (e.g., 'log2(fold-change)', 'lipid abundance (normalized counts)').
- Threshold lines (p-value, fold-change cutoffs) are clearly marked and correspond to stated statistical cutoffs.
- Legend correctly maps color/shape encodings to condition, lipid class, or significance status.
- Figure resolution (e.g., ≥300 DPI for raster output) is suitable for print publication when exported to PNG/PDF.
- All text (labels, legend, title) is legible and non-overlapping; axes do not clip data points or labels.

## Limitations

- Visualization choice (volcano plot, heatmap, box plot, bar plot) depends on data dimensionality and comparison scope; no single default covers all lipid comparisons.
- High-dimensional lipid datasets (>500 lipids) may produce overcrowded heatmaps or bar plots; dimensionality reduction or filtering to top lipids may be necessary.
- Color/shape encodings can be ambiguous or inaccessible if not colorblind-friendly; check palette choices.
- No changelog or version tracking mentioned; reproducibility depends on documenting tool versions and parameter choices at publication time.

## Evidence

- [other] The CLAW-MRM workflow includes a visualization component that operates as part of a multi-step process following statistical analysis to render lipid expression patterns.: "The CLAW-MRM workflow includes a visualization component that operates as part of a multi-step process following statistical analysis to render lipid expression patterns."
- [other] Load the statistical results table (CSV or tabular format) containing lipid identities, expression measurements, p-values, fold-changes, and condition labels. Parse and structure the data to extract lipid names, quantitative values, and grouping variables (experimental conditions or sample classes). Select appropriate visualization type(s) based on data dimensionality and comparison scope (e.g., volcano plot for fold-change vs. significance, heatmap for multi-lipid expression across conditions, box plot for abundance distributions, bar plot for ranked lipid levels). Generate visualization(s) using a plotting library, encoding lipid identity on one axis, expression metric on the other, and applying color/shape encoding for condition, significance, or lipid class distinctions. Apply publication-quality formatting: labeled axes, legend, title, and threshold lines (e.g., p-value or fold-change cutoff) where applicable.: "Load the statistical results table (CSV or tabular format) containing lipid identities, expression measurements, p-values, fold-changes, and condition labels...Apply publication-quality formatting:"
- [other] Export figure(s) to a standard image format (PNG or PDF) with sufficient resolution for print or supplement.: "Export figure(s) to a standard image format (PNG or PDF) with sufficient resolution for print or supplement."
- [intro] streamline various tasks such as data parsing, matching, statistical analysis, and visualization: "streamline various tasks such as data parsing, matching, statistical analysis, and visualization"
- [intro] The workflow ensures consistency in data processing and enables efficient exploration and interpretation of lipid expression patterns.: "The workflow ensures consistency in data processing and enables efficient exploration and interpretation of lipid expression patterns."
- [readme] Creates various visualizations such as pie charts, bar plots, and edge plots to analyze and compare lipid classes.: "Creates various visualizations such as pie charts, bar plots, and edge plots to analyze and compare lipid classes."
