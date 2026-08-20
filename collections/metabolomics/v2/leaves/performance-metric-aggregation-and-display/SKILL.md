---
name: performance-metric-aggregation-and-display
description: Use when after running NOREVA's assessment functions (normulticlassqcall,
  normulticlassnoall, normulticlassisall, nortimecourseqcall, nortimecoursenoall)
  on preprocessing workflows, use this skill to synthesize performance results across
  all five criteria into a single ranked output and create a.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - norvisualization
  - normulticlassqcall / normulticlassnoall / normulticlassisall / nortimecourseqcall
    / nortimecoursenoall
  license_tier: open
derived_from:
- doi: 10.1038/s41596-021-00636-9
  title: NOREVA
evidence_spans:
- '[![R >3.5](https://img.shields.io/badge/R-%3E3.5-success.svg)](https://www.r-project.org/)'
- Run norvisualization on the overall ranking CSV
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_noreva_cq
    doi: 10.1038/s41596-021-00636-9
    title: NOREVA
  dedup_kept_from: coll_noreva_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41596-021-00636-9
  all_source_dois:
  - 10.1038/s41596-021-00636-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# performance-metric-aggregation-and-display

## Summary

Aggregates multiple preprocessing workflow performance scores across five distinct evaluation criteria into a ranked summary and generates a circular barplot visualization of top-performing workflows. This skill enables comprehensive comparison and interpretation of preprocessing method performance for metabolomic data.

## When to use

After running NOREVA's assessment functions (normulticlassqcall, normulticlassnoall, normulticlassisall, nortimecourseqcall, nortimecoursenoall) on preprocessing workflows, use this skill to synthesize performance results across all five criteria into a single ranked output and create a publication-ready circular barplot highlighting the top 100 workflows by overall performance score.

## When NOT to use

- Input ranking file is not CSV format or lacks performance score columns required by norvisualization
- Assessment has not yet been run on any preprocessing workflows (no ranking file exists)
- You need detailed numeric performance values in tabular form rather than a visual summary

## Inputs

- overall_ranking_CSV_file (from NOREVA assessment functions)
- cutoff_parameter (integer, e.g., 100)

## Outputs

- circular_barplot_visualization (PNG or PDF format)
- NOREVA-Ranking-Top.100.workflows figure file

## How to apply

Load the overall ranking CSV file containing aggregated performance scores from NOREVA's assessment output using R. Call the norvisualization function with the ranking file as input and set the cutoff parameter to 100 to filter for top-performing workflows. The function extracts workflow identities and their corresponding performance metrics, then generates a circular barplot where each workflow is positioned by rank and colored/sized by performance score. Save the resulting visualization as NOREVA-Ranking-Top.100.workflows in PNG or PDF format. The circular layout emphasizes relative ranking and facilitates visual identification of performance tiers across hundreds of preprocessing method combinations.

## Related tools

- **norvisualization** (Core function that reads overall ranking CSV and generates circular barplot of top-ranked workflows) — https://github.com/idrblab/NOREVA
- **R** (Programming environment (version >3.5) for executing norvisualization and graphics functions) — https://www.r-project.org/
- **normulticlassqcall / normulticlassnoall / normulticlassisall / nortimecourseqcall / nortimecoursenoall** (Upstream assessment functions that generate the overall ranking CSV file input to norvisualization) — https://github.com/idrblab/NOREVA

## Examples

```
library(NOREVA); norvisualization(rankingFile='overall_ranking.csv', cutoff=100)
```

## Evaluation signals

- Output figure exists and is readable in PNG or PDF format with filename matching NOREVA-Ranking-Top.100.workflows pattern
- Circular barplot displays exactly 100 workflows (or fewer if input ranking has <100 entries) ranked by performance score
- Workflows are arranged in circular layout with visible ranking order and performance metric scaling (bar height/color proportional to score)
- All 100 top-ranked workflows from the input CSV are represented in the visualization with no missing or duplicated entries
- Performance metrics span the expected range observed in the source ranking file (no compression, clipping, or transformation artifacts)

## Limitations

- norvisualization requires the output CSV from one of NOREVA's five assessment functions; intermediate or manually-edited ranking files may cause parsing errors
- Circular layout becomes crowded and difficult to read if cutoff parameter exceeds ~150–200 workflows depending on label length and figure resolution
- The function assumes study assumptions (SAalpha, SAbeta, SAgamma) were correctly specified during upstream assessment; mismatched assumptions will yield misleading rankings
- Performance ranking integrates five criteria with equal weight by default; users requiring differential weighting of criteria must recompute rankings outside norvisualization

## Evidence

- [other] The norvisualization function accepts an overall ranking CSV file and a cutoff parameter set to '100' to produce a circular barplot illustration of the top-100 processing workflows ranked by performance.: "The norvisualization function accepts an overall ranking CSV file and a cutoff parameter set to "100" to produce a circular barplot illustration of the top-100 processing workflows ranked by"
- [intro] Five well-established criteria, each with a distinct underlying theory, are integrated to ensure comprehensive evaluation: "five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation than any single criterion"
- [other] Generate a circular barplot visualization using R graphics functions, with workflows ranked by performance score and displayed in circular layout.: "Generate a circular barplot visualization using R graphics functions, with workflows ranked by performance score and displayed in circular layout."
- [intro] NOREVA realizes a high-throughput discovery of the well-performing pre-processing workflows: "The NOREVA package not only enables the pre-processing and assessment of multi-class/time-series metabolomic data but also realize a high-throughput discovery of the well-performing pre-processing"
- [readme] R >3.5 is required; devtools and multiple Bioconductor packages support NOREVA installation and function execution: "[![R >3.5](https://img.shields.io/badge/R-%3E3.5-success.svg)](https://www.r-project.org/)"
