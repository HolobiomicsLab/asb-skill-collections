---
name: interactive-visualization-interpretation-methylation-results
description: Use when after running ChAMP detection functions (champ.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_3518
  tools:
  - ChAMP
  - Shiny
  - Plotly
  - minfi
derived_from:
- doi: 10.1093/bioinformatics/btx513
  title: champ
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_champ
    doi: 10.1093/bioinformatics/btx513
    title: champ
  dedup_kept_from: coll_champ
schema_version: 0.2.0
---

# Interactive Visualization and Interpretation of Methylation Results

## Summary

Use Shiny and Plotly-based interactive web browser interfaces in ChAMP to visualize and inspect DNA methylation analysis results, including differentially methylated blocks and regions. This skill enables rapid visual exploration and validation of results without requiring command-line proficiency.

## When to use

After running ChAMP detection functions (champ.Block(), DMR detection methods) on EPIC or 450k array data, when you need to inspect, validate, and interactively explore the spatial distribution, effect sizes, or prevalence of detected differentially methylated features before downstream interpretation or filtering.

## When NOT to use

- Raw .idat files have not yet been loaded and normalized through champ.load() and quality control—visualization requires processed detection results.
- Your analysis goal is to programmatically extract and export all results for downstream statistical computation (non-interactive); use tabular output formats instead.
- You are working in a headless/non-graphical computing environment without X11 or browser support.

## Inputs

- ChAMP detection function output (e.g., Block detection results, DMR list)
- EPIC or 450k methylation array data (beta-valued matrix or .idat files previously loaded and analyzed)
- Array type specification (EPIC, EPICv2, or 450k)

## Outputs

- Interactive Shiny web browser visualization window
- Filtered/annotated feature table (blocks, regions, or probes with p-values, effect sizes, genomic coordinates)
- Visual confirmation of detected features and their spatial distribution across the genome

## How to apply

Launch the interactive GUI function (e.g., Block.GUI()) corresponding to your detection results to open a Shiny-based web browser interface. The interface displays detected features (blocks, regions, or probes) with interactive visualization tools that allow filtering by p-value, effect size, or genomic location, and inspection of individual results through linked plots and tables. Verify that the reported features match expected statistical thresholds and biological patterns before proceeding to gene set enrichment analysis or publication. The visualization aids validation that the detection algorithm's output agrees with documented expected behavior for known positive/negative control datasets (e.g., EPICSimData should report no blocks when none are truly present).

## Related tools

- **ChAMP** (Provides champ.Block(), DMR detection functions, and interactive GUI visualization functions (Block.GUI(), etc.) for visualizing and interpreting methylation results) — https://github.com/YuanTian1991/ChAMP
- **Shiny** (Underlying framework for ChAMP's interactive web browser-based visualization and analysis interfaces)
- **Plotly** (Provides interactive graphics rendering within ChAMP's Shiny-based visualization functions)
- **minfi** (Alternative methylation analysis package; ChAMP integrates its Functional Normalization method and can be used in parallel for cross-validation of results)

## Examples

```
library(ChAMP); data(EPICSimData); Block.GUI()
```

## Evaluation signals

- The interactive GUI launches without errors and displays the expected detection results (e.g., Block.GUI() shows detected blocks when present, no blocks when none are expected as in EPICSimData negative control).
- Visual inspection of linked genomic plots, p-value distributions, and effect size histograms confirms that reported features have consistent statistical support (e.g., p-values below chosen threshold, effect sizes of biologically plausible magnitude).
- Filtering by significance threshold, genomic region, or sample group in the interactive interface reduces the result set appropriately and highlights genuinely differentiated features.
- Comparison of interactive visualization results against tabular output (p-values, coordinates, effect sizes) shows no discrepancies; all displayed features match the underlying detection output.
- For known positive or negative control datasets (e.g., EPICSimData), the visualization correctly reports expected outcomes (e.g., absence of blocks for synthetic data without true signal).

## Limitations

- Interactive visualization requires a graphical environment with browser support; cannot be used in headless/remote clusters without X11 forwarding or containerization.
- The GUI provides exploratory inspection but does not automatically perform advanced statistical filtering (e.g., multiple testing correction post-hoc, effect size thresholding); manual interpretation is still required.
- Visualization performance may degrade when displaying results from very large datasets (e.g., >100,000 detected features); subsetting or filtering before visualization is recommended.
- The interactive interface is most useful for single-user exploratory analysis; for batch processing or integration into automated pipelines, programmatic output formats are preferable.

## Evidence

- [intro] Interactive GUI provides rapid visual exploration of results: "ChAMP also provides a series of Shiny and Plotly-based WebBrower Interactive analysis functions"
- [other] Block detection results are validated through interactive visualization: "Launch Block.GUI() interactive interface to visualize and inspect the block detection results."
- [other] Interactive visualization enables validation against expected behavior: "Verify that no differentially methylated blocks are reported in the output, confirming agreement with documented expected behavior for this synthetic dataset."
- [intro] ChAMP integrates comprehensive analysis from detection to interpretation: "ChAMP package is designed for conduct DNA methylation array analysis, providing service from data loading, to final gene set enrichment analysis"
