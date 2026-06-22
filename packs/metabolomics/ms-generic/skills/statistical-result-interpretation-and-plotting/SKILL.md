---
name: statistical-result-interpretation-and-plotting
description: Use when after statistical analysis has produced a results table with lipid identities, quantitative expression values, p-values, fold-changes, and experimental condition labels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0571
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3520
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# statistical-result-interpretation-and-plotting

## Summary

Transform tabular statistical results (CSV containing lipid identities, expression measurements, p-values, and fold-changes) into publication-quality visualizations that encode lipid identity, expression metrics, and condition comparisons using appropriate plot types and publication-grade formatting. This skill bridges the gap between statistical analysis and communicable findings in lipidomics workflows.

## When to use

Apply this skill after statistical analysis has produced a results table with lipid identities, quantitative expression values, p-values, fold-changes, and experimental condition labels. Use it when you need to communicate statistical findings visually—to identify significant lipids, compare expression across conditions, or highlight lipid class-specific patterns for publication or supplementary material.

## When NOT to use

- Statistical results are not yet available or statistical analysis has not been completed.
- Input is raw mass spectrometry data (mzML format) or pre-processed lipid abundance tables that have not undergone statistical testing.
- Visualization goal is exploratory data quality assessment before statistical analysis rather than communicating final statistical findings.

## Inputs

- Statistical results table (CSV or tabular format with columns: lipid identity, expression measurements, p-values, fold-changes, condition labels)
- Lipid identities and classification metadata
- Experimental condition or sample class grouping variables

## Outputs

- Publication-quality visualization(s) in PNG or PDF format
- Volcano plot (fold-change vs. p-value)
- Heatmap (multi-lipid expression across conditions)
- Box plot (abundance distributions by condition)
- Bar plot (ranked lipid levels)

## How to apply

Load the statistical results table (CSV or tabular format) and parse lipid names, quantitative values, and grouping variables (experimental conditions or sample classes). Select visualization type based on comparison scope: volcano plots for fold-change vs. statistical significance, heatmaps for multi-lipid expression across conditions, box plots for abundance distributions, or bar plots for ranked lipid levels. Encode lipid identity on one axis, expression metric on the other, and apply color or shape encoding for condition, significance threshold, or lipid class distinctions. Apply publication-quality formatting with labeled axes, legends, descriptive titles, and threshold lines (e.g., p-value or fold-change cutoff lines) where applicable. Export figures to PNG or PDF at sufficient resolution for print or supplementary material.

## Related tools

- **matplotlib** (Primary plotting library for generating figures (volcano plots, box plots, bar plots) with customizable axes, colors, and threshold annotations)
- **seaborn** (Statistical visualization layer for enhanced plot aesthetics, heatmap generation, and condition-based color encoding)
- **pandas** (Data parsing, restructuring, and extraction of lipid names, quantitative values, and grouping variables from statistical results tables)
- **plotly** (Interactive visualization and export to high-resolution PNG/PDF formats with publication-grade formatting)

## Examples

```
import pandas as pd; import matplotlib.pyplot as plt; import seaborn as sns; results = pd.read_csv('statistical_results.csv'); volcano = plt.figure(); plt.scatter(results['log2fc'], -np.log10(results['pvalue']), alpha=0.6); plt.axhline(-np.log10(0.05), color='red', linestyle='--'); plt.xlabel('log2(Fold Change)'); plt.ylabel('-log10(p-value)'); plt.savefig('volcano_plot.pdf', dpi=300, bbox_inches='tight')
```

## Evaluation signals

- Axes are labeled with lipid identity and expression metric; legend is present and clearly identifies conditions, significance, or lipid class encoding.
- Threshold lines (p-value and fold-change cutoffs) are visibly rendered on volcano plots; significance thresholds match those used in statistical analysis.
- Exported figure resolution is ≥300 DPI; file format is PNG or PDF as specified for publication or supplementary material.
- All lipids in the statistical results table are represented in the visualization; no data points are dropped or hidden unless filtering criteria are explicitly documented.
- Color/shape encoding is consistent across multiple subplots if present; legend describes encoding unambiguously (e.g., 'red = p < 0.05', 'circle = lipid class A').

## Limitations

- Visualization effectiveness depends on dimensionality and sample size; very large numbers of lipids may require filtering or faceting strategies not covered by basic plotting.
- Choice of visualization type is manual and requires domain knowledge; inappropriate plot selection can obscure statistical findings or introduce visual distortion.
- Publication-grade formatting (font size, color palette, aspect ratio) requires iterative refinement and may differ across journal or venue guidelines.
- No automated provision for multiple hypothesis correction visualization (e.g., adjusted p-value thresholds) is described; these must be pre-computed in statistical results table.
- Export resolution and format compatibility depend on library version and system rendering capabilities; older versions of kaleido or matplotlib may produce degraded output.

## Evidence

- [other] Load the statistical results table (CSV or tabular format) containing lipid identities, expression measurements, p-values, fold-changes, and condition labels.: "Load the statistical results table (CSV or tabular format) containing lipid identities, expression measurements, p-values, fold-changes, and condition labels."
- [other] Select appropriate visualization type(s) based on data dimensionality and comparison scope (e.g., volcano plot for fold-change vs. significance, heatmap for multi-lipid expression across conditions, box plot for abundance distributions, bar plot for ranked lipid levels).: "Select appropriate visualization type(s) based on data dimensionality and comparison scope (e.g., volcano plot for fold-change vs. significance, heatmap for multi-lipid expression across conditions,"
- [other] Generate visualization(s) using a plotting library, encoding lipid identity on one axis, expression metric on the other, and applying color/shape encoding for condition, significance, or lipid class distinctions.: "Generate visualization(s) using a plotting library, encoding lipid identity on one axis, expression metric on the other, and applying color/shape encoding for condition, significance, or lipid class"
- [other] Apply publication-quality formatting: labeled axes, legend, title, and threshold lines (e.g., p-value or fold-change cutoff) where applicable.: "Apply publication-quality formatting: labeled axes, legend, title, and threshold lines (e.g., p-value or fold-change cutoff) where applicable."
- [other] Export figure(s) to a standard image format (PNG or PDF) with sufficient resolution for print or supplement.: "Export figure(s) to a standard image format (PNG or PDF) with sufficient resolution for print or supplement."
- [intro] This workflow...ensures consistency in data processing and enables efficient exploration and interpretation of lipid expression patterns.: "ensures consistency in data processing and enables efficient exploration and interpretation of lipid expression patterns"
- [readme] Creates various visualizations such as pie charts, bar plots, and edge plots to analyze and compare lipid classes.: "Creates various visualizations such as pie charts, bar plots, and edge plots to analyze and compare lipid classes."
