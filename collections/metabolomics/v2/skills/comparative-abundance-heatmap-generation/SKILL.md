---
name: comparative-abundance-heatmap-generation
description: Use when when you have parsed lipid expression data (quantitative abundance
  measurements) organized as rows (lipid identities) and columns (experimental conditions
  or samples), and need to simultaneously display relative abundance levels across
  many lipids and conditions to identify clustering.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0531
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3678
  tools:
  - matplotlib
  - seaborn
  - pandas
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.4c05039
  title: CLAW-MRM
evidence_spans:
- streamline various tasks such as data parsing, matching, statistical analysis, and
  visualization
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

# comparative-abundance-heatmap-generation

## Summary

Generate publication-quality heatmap visualizations encoding lipid abundance across multiple experimental conditions or sample classes, using color intensity to represent expression magnitude and spatial layout to reveal co-variation patterns. This skill is essential for communicating multi-lipid, multi-condition comparisons in a single graphical summary.

## When to use

When you have parsed lipid expression data (quantitative abundance measurements) organized as rows (lipid identities) and columns (experimental conditions or samples), and need to simultaneously display relative abundance levels across many lipids and conditions to identify clustering, co-expression, or condition-specific lipid signatures.

## When NOT to use

- Abundance data are not organized in a condition × lipid matrix format (e.g., raw individual sample replicates; use aggregation/summarization first)
- You need to display uncertainty (confidence intervals or standard deviations); use box plots or violin plots instead
- The goal is to compare only two lipids or two conditions; simpler visualization (bar plot or scatter plot) is more appropriate

## Inputs

- Statistical results table (CSV or tabular format) with columns: lipid identity, abundance measurements per condition/sample, experimental condition labels
- Structured DataFrame with lipid names as index and conditions as columns

## Outputs

- Heatmap visualization (PNG or PDF image file)
- Publication-quality figure with labeled axes, colorbar, and threshold or clustering annotations

## How to apply

Load the statistical results table (CSV or tabular format) containing lipid identities, quantitative abundance values, and condition labels into a pandas DataFrame. Structure the data so that lipid names index rows and experimental conditions or sample classes form columns, with abundance values as cell entries. Use a plotting library (matplotlib/seaborn) to encode abundance magnitude as color intensity (e.g., colormap from low to high expression), optionally applying row and column clustering (hierarchical or k-means) to group similar lipids and conditions. Apply publication-quality formatting including axis labels identifying lipid identities and conditions, a labeled colorbar indicating the abundance scale, and a descriptive title. Export the figure to PNG or PDF at sufficient resolution (≥300 dpi) for print publication or supplementary materials.

## Related tools

- **matplotlib** (Primary plotting library for rendering heatmap figures with custom colormaps and formatting)
- **seaborn** (High-level heatmap interface supporting clustering, annotations, and aesthetic defaults)
- **pandas** (Data structure (DataFrame) for organizing and manipulating lipid abundance matrices)

## Examples

```
import pandas as pd; import seaborn as sns; import matplotlib.pyplot as plt; df = pd.read_csv('Pre_EdgeR/lipid_abundance.csv', index_col=0); sns.heatmap(df, cmap='viridis', cbar_kws={'label': 'Abundance'}, yticklabels=True); plt.xlabel('Condition'); plt.ylabel('Lipid'); plt.title('Lipid Expression Heatmap'); plt.savefig('Plots/lipid_heatmap.png', dpi=300, bbox_inches='tight')
```

## Evaluation signals

- Heatmap renders lipid identities on one axis and experimental conditions on the other, with color intensity proportional to abundance values
- Axes are clearly labeled; colorbar scale is visible and readable; title and legend are present
- If clustering was applied, dendrogram or cluster membership is visible; clustering preserves expected biological groupings (e.g., replicates or lipid classes cluster together)
- Export format is PNG or PDF with resolution ≥300 dpi; no rendering artifacts or text cutoff
- Cell values (if shown as annotations) match the underlying statistical results table within floating-point precision

## Limitations

- Heatmap readability degrades with very large numbers of lipids (>100); consider subsetting to differentially abundant lipids or lipid classes
- Color choice (colormap) can introduce perceptual bias; choose colormap carefully (e.g., perceptually uniform) to avoid misinterpretation of subtle abundance differences
- Hierarchical clustering can produce spurious groupings if abundance values span very different scales across lipid classes; consider normalization or log-transformation before clustering
- Static heatmap does not show per-sample variability or replication; reserve interactive or multi-panel heatmaps for exploratory analysis, and aggregated heatmaps for publication

## Evidence

- [other] heatmap for multi-lipid expression across conditions: "Select appropriate visualization type(s) based on data dimensionality and comparison scope (e.g., volcano plot for fold-change vs. significance, heatmap for multi-lipid expression across conditions,"
- [other] Parse and structure lipid data for visualization: "Parse and structure the data to extract lipid names, quantitative values, and grouping variables (experimental conditions or sample classes)."
- [other] Color encoding in heatmap visualization: "Generate visualization(s) using a plotting library, encoding lipid identity on one axis, expression metric on the other, and applying color/shape encoding for condition, significance, or lipid class"
- [other] Publication-quality formatting standards: "Apply publication-quality formatting: labeled axes, legend, title, and threshold lines (e.g., p-value or fold-change cutoff) where applicable."
- [other] Export format and resolution requirements: "Export figure(s) to a standard image format (PNG or PDF) with sufficient resolution for print or supplement."
- [readme] R heatmap plot generation in edgeR workflow: "Heatmap Plot Generation: Generates heatmap plots to visualize the correlation between different lipid features."
