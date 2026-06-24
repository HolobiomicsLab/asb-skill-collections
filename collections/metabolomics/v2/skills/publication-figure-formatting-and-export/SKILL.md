---
name: publication-figure-formatting-and-export
description: Use when after generating initial visualizations (volcano plots, heatmaps,
  box plots, or bar plots) of lipid expression data, apply this skill when figures
  must be submitted to journals, supplementary materials, or presentations and must
  meet publication-quality standards for axes labels, legends.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - matplotlib
  - seaborn
  - pandas
  license_tier: open
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

# publication-figure-formatting-and-export

## Summary

Apply publication-quality formatting to lipidomics visualizations and export them to print-ready image formats. This skill ensures that generated figures meet journal submission standards through consistent labeling, legends, thresholds, and high-resolution export.

## When to use

After generating initial visualizations (volcano plots, heatmaps, box plots, or bar plots) of lipid expression data, apply this skill when figures must be submitted to journals, supplementary materials, or presentations and must meet publication-quality standards for axes labels, legends, significance thresholds, and resolution.

## When NOT to use

- Input visualization has not yet been generated or statistical data has not been parsed—use data visualization skill first
- Output figures are for exploratory or internal quality-control use only and do not need to meet journal submission standards
- Figures are already in final publication format and no refinement to labeling, thresholds, or resolution is required

## Inputs

- matplotlib or seaborn figure object containing lipid expression visualization
- statistical results table with p-values and fold-change values (CSV or tabular)
- experimental condition labels and lipid class annotations

## Outputs

- publication-quality figure in PNG format with ≥300 dpi resolution
- publication-quality figure in PDF format (vector)
- figure file with embedded axes labels, legend, title, and threshold lines

## How to apply

Take the generated visualization object from matplotlib or seaborn and apply publication-quality formatting by: (1) adding descriptive axis labels, figure title, and a legend that encodes experimental conditions, significance status, or lipid class distinctions; (2) overlaying threshold lines (e.g., p-value or fold-change cutoff lines on volcano plots) with appropriate styling; (3) ensuring font sizes, colors, and line weights are legible when printed or displayed in supplements; (4) exporting to PNG or PDF format with sufficient resolution (typically ≥300 dpi for print). The decision to include specific threshold lines depends on the visualization type—volcano plots should show significance and fold-change cutoffs, while heatmaps may require color bar calibration. Export resolution and format choice depends on target medium: PDF for vector-based scaling in documents, PNG for raster figures in web or supplement galleries.

## Related tools

- **matplotlib** (generates and formats figure objects; applies axes labels, legends, titles, and threshold lines; exports to PNG/PDF with DPI control)
- **seaborn** (provides high-level visualization functions and built-in styling suitable for publication-quality plots)
- **pandas** (loads and structures statistical results table containing lipid identities, p-values, and fold-changes for threshold line placement)

## Examples

```
import matplotlib.pyplot as plt; fig, ax = plt.subplots(); ax.scatter(fold_changes, -np.log10(p_values), c=colors); ax.axhline(-np.log10(0.05), color='red', linestyle='--', label='p=0.05'); ax.set_xlabel('log2 fold-change'); ax.set_ylabel('-log10(p-value)'); ax.legend(); plt.savefig('volcano_plot.png', dpi=300, bbox_inches='tight'); plt.savefig('volcano_plot.pdf', format='pdf', bbox_inches='tight')
```

## Evaluation signals

- Exported PNG or PDF file has resolution ≥300 dpi when opened in image viewer or verified via file metadata
- Figure contains labeled axes with units (e.g., 'log2 fold-change', 'p-value'), a descriptive title, and a legend mapping colors/shapes to conditions or lipid classes
- Threshold lines (p-value cutoff, fold-change cutoff) are visually distinct and labeled; e.g., horizontal/vertical dashed lines on volcano plots at p=0.05 and fc=±1.5
- Font sizes and line weights are consistent across all text elements and remain legible at typical journal print/supplement size (e.g., 8–12 pt fonts)
- File format matches submission requirements (PDF for vector scaling, PNG for raster); file size is reasonable and metadata confirms export parameters

## Limitations

- Color encoding and threshold placement must be manually specified by the user; the skill does not automatically detect optimal thresholds
- Export resolution and format choice depend on journal-specific requirements—standard guidelines (≥300 dpi for print, ≥72 dpi for web) should be verified before submission
- Complex multi-panel figures may require additional layout control beyond single-figure export; consider using GridSpec or subplot managers in matplotlib for composite figures

## Evidence

- [other] Apply publication-quality formatting: labeled axes, legend, title, and threshold lines (e.g., p-value or fold-change cutoff) where applicable.: "Apply publication-quality formatting: labeled axes, legend, title, and threshold lines (e.g., p-value or fold-change cutoff) where applicable."
- [other] Generate visualization(s) using a plotting library, encoding lipid identity on one axis, expression metric on the other, and applying color/shape encoding for condition, significance, or lipid class distinctions.: "Generate visualization(s) using a plotting library, encoding lipid identity on one axis, expression metric on the other, and applying color/shape encoding for condition, significance, or lipid class"
- [other] Export figure(s) to a standard image format (PNG or PDF) with sufficient resolution for print or supplement.: "Export figure(s) to a standard image format (PNG or PDF) with sufficient resolution for print or supplement."
- [readme] This workflow ensures consistency in data processing and enables efficient exploration and interpretation of lipid expression patterns.: "This workflow ensures consistency in data processing and enables efficient exploration and interpretation of lipid expression patterns."
