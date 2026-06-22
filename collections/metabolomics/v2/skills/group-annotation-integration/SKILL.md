---
name: group-annotation-integration
description: Use when you have an expression matrix (e.g., heatmap_test.csv with genes as rows and samples as columns) and a corresponding group annotation file (e.g., group_info.csv with sample IDs and their group assignments).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3938
  edam_topics:
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0625
  tools:
  - R Shiny
  - GraphBio
derived_from:
- doi: 10.3389/fgene.2022.957317
  title: GraphBio
evidence_spans:
- GraphBio---A modular and scalable R Shiny dashboard
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_graphbio_cq
    doi: 10.3389/fgene.2022.957317
    title: GraphBio
  dedup_kept_from: coll_graphbio_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fgene.2022.957317
  all_source_dois:
  - 10.3389/fgene.2022.957317
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# group-annotation-integration

## Summary

Integrate group annotation metadata (sample-to-group mappings, phenotype labels, or experimental conditions) as sidebars, color bars, or labels into clustered heatmap visualizations to contextualize expression patterns by group membership. This skill transforms raw group annotation CSV files into visual metadata overlays that aid interpretation of hierarchical clustering results.

## When to use

You have an expression matrix (e.g., heatmap_test.csv with genes as rows and samples as columns) and a corresponding group annotation file (e.g., group_info.csv with sample IDs and their group assignments). Use this skill when you need to simultaneously visualize expression values AND distinguish sample groups, particularly to validate that clustered samples correspond to expected biological or experimental groups.

## When NOT to use

- The group annotation file has no sample IDs that match the expression matrix column names—validation will fail and integration cannot proceed.
- The expression matrix is already a distance or similarity matrix rather than raw expression values—clustering and value-based color scaling will be inappropriate.
- Group annotations are missing for a large fraction of samples, making sidebars incomplete or misleading.

## Inputs

- Expression matrix (CSV: genes/features × samples, numeric values)
- Group annotation file (CSV: sample IDs and group/phenotype assignments)

## Outputs

- Interactive heatmap visualization with clustered rows and columns
- Colored annotation sidebar(s) or labels indicating group membership
- Rendered Shiny widget displaying integrated heatmap and metadata

## How to apply

Load the expression matrix and group annotation data using R data I/O functions (read.csv or equivalent). Parse and validate that the group annotation file's sample identifiers match the column names of the expression matrix. Apply row and column clustering to the expression matrix using hierarchical clustering or related algorithms. Map group labels to a color palette (e.g., distinct colors per group or phenotype value). Render group annotations as colored sidebars or labeled sections adjacent to the heatmap columns, ensuring the annotation order matches the clustered sample order. Integrate this annotated heatmap into an R Shiny application interface to enable interactive exploration.

## Related tools

- **R Shiny** (Web application framework for rendering interactive heatmap visualization with annotation sidebars and real-time user interaction) — https://shiny.rstudio.com/
- **GraphBio** (Complete omics visualization platform that implements group-annotation-integrated heatmaps via R Shiny dashboard; provides modular heatmap component consuming both expression matrix and group annotation CSVs) — https://github.com/databio2022/GraphBio

## Evaluation signals

- Heatmap columns are reordered after hierarchical clustering; verify that clustered samples with identical or similar group labels appear adjacent or in contiguous blocks.
- Colored annotation sidebars render without gaps or misalignment; sample order in sidebars exactly matches column order in heatmap.
- All samples in the expression matrix have a corresponding group label in the annotation sidebar; no 'NA' or missing values appear.
- Expression values are mapped to a continuous color scale (e.g., blue-white-red for low-mid-high); annotation colors are discrete and visually distinct per group.
- Interactive Shiny widget responds to user input (e.g., hover, zoom, or toggle groups) without console errors; heatmap and annotations remain synchronized.

## Limitations

- If sample identifiers in the expression matrix and group annotation file use inconsistent naming (e.g., 'Sample_1' vs. 'sample1'), the merge will fail silently or lose annotations for unmatched samples.
- Large expression matrices (>10,000 genes or >1,000 samples) may render slowly or cause memory issues in R Shiny without optimization (e.g., row/column subsetting or server-side filtering).
- The skill assumes a single categorical or discrete group variable; continuous phenotypes or multi-level hierarchical group structures require additional preprocessing or custom visualization logic not addressed in the standard workflow.

## Evidence

- [intro] Heatmap component input and validation: "The heatmap component consumes two CSV files: heatmap_test.csv (expression matrix) and group_info.csv (group annotations) to produce the heatmap visualization."
- [intro] Annotation integration step in workflow: "Integrate group annotation metadata as heatmap annotations (e.g., colored sidebars or labels)."
- [intro] Clustering and color scaling rationale: "Generate a heatmap visualization using R Shiny's rendering capabilities, applying row and column clustering and color scaling to represent expression values."
- [readme] GraphBio heatmap module design: "heatmap_test.csv and group_info.csv for heatmap."
