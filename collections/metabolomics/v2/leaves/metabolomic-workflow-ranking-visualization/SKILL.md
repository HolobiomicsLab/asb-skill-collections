---
name: metabolomic-workflow-ranking-visualization
description: Use when after running NOREVA's multi-class or time-course assessment
  functions (normulticlassqcall, normulticlassnoall, normulticlassisall, nortimecourseqcall,
  or nortimecoursenoall) that produce an overall ranking CSV file of preprocessed
  workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3441
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3365
  tools:
  - R
  - norvisualization
  - NOREVA
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

# metabolomic-workflow-ranking-visualization

## Summary

Generate a circular barplot visualization ranking the top-performing preprocessing workflows for metabolomic data based on multi-criterion performance assessment. This skill enables rapid visual identification of optimal preprocessing strategies from thousands of candidate workflows evaluated by NOREVA.

## When to use

After running NOREVA's multi-class or time-course assessment functions (normulticlassqcall, normulticlassnoall, normulticlassisall, nortimecourseqcall, or nortimecoursenoall) that produce an overall ranking CSV file of preprocessed workflows. Use this skill when you need to communicate the relative performance of top preprocessing methods to stakeholders or select the best-performing workflow from a ranked list of hundreds or thousands of candidates.

## When NOT to use

- Input data is not a ranked workflow CSV file (e.g., raw peak tables or unevaluated preprocessing logs)
- You need to visualize individual preprocessing step contributions rather than overall workflow rankings
- The cutoff value exceeds the total number of workflows actually evaluated, producing incomplete or empty visualizations

## Inputs

- Overall ranking CSV file from NOREVA assessment function containing workflow identifiers and composite performance scores
- Cutoff parameter (integer, typically 100 for top-100 workflows)

## Outputs

- Circular barplot visualization (PNG or PDF file, e.g. 'NOREVA-Ranking-Top.100.workflows')
- Visual ranking of preprocessing workflows ordered by performance metric

## How to apply

Load the overall ranking CSV file output from a NOREVA assessment function into R. Call the norvisualization function with the ranking file as input and set the cutoff parameter to '100' to extract and visualize the top-100 ranked preprocessing workflows. The function automatically ranks workflows by their performance scores (typically composite scores from four independent evaluation criteria) and arranges them in a circular barplot layout where bar height represents performance magnitude. The circular layout facilitates visual comparison of many workflows simultaneously. Export the resulting figure as PNG or PDF format (typically named NOREVA-Ranking-Top.100.workflows) for publication or presentation.

## Related tools

- **norvisualization** (R function that accepts ranked workflow CSV and cutoff parameter to generate circular barplot of top-N workflows) — https://github.com/idrblab/NOREVA
- **R** (Statistical environment executing norvisualization function and graphics rendering (version >3.5 required)) — https://www.r-project.org/
- **NOREVA** (Parent package producing the overall ranking CSV file through multi-criterion assessment of preprocessing workflows) — https://github.com/idrblab/NOREVA

## Examples

```
library(NOREVA); norvisualization(ranking_file = 'overall_ranking.csv', cutoff = 100); ggsave('NOREVA-Ranking-Top.100.workflows.pdf')
```

## Evaluation signals

- Circular barplot renders without errors and displays exactly N workflows where N ≤ cutoff parameter
- Workflows are visually sorted by performance score in descending order; bar heights increase monotonically from center outward
- Output file (PNG/PDF) is created with non-zero file size and viewable in standard image viewers
- Workflow identifiers are legible in the circular layout (no overlapping labels or truncation)
- Performance score range on the radial axis reflects the actual min/max values in the input ranking CSV

## Limitations

- norvisualization function requires the input ranking CSV to be in the exact format output by NOREVA assessment functions; custom or manually edited ranking files may cause parsing errors or misalignment
- Cutoff parameter set too high relative to available workflows results in sparse or incomplete visualizations
- Circular barplot layout becomes visually crowded with cutoff values >150–200 workflows; readability decreases substantially
- The function does not natively filter workflows by specific criteria (e.g., only QC-based methods or specific normalization strategy); all workflows in the top-N range are plotted regardless of preprocessing category

## Evidence

- [other] The norvisualization function accepts an overall ranking CSV file and a cutoff parameter set to '100' to produce a circular barplot illustration of the top-100 processing workflows ranked by performance.: "The norvisualization function accepts an overall ranking CSV file and a cutoff parameter set to "100" to produce a circular barplot illustration of the top-100 processing workflows ranked by"
- [intro] NOREVA enables the performance assessment of metabolomic data processing and high-throughput discovery of well-performing preprocessing workflows using five well-established criteria.: "The NOREVA package not only enables the pre-processing and assessment of multi-class/time-series metabolomic data but also realize a high-throughput discovery of the well-performing pre-processing"
- [other] The workflow loads the overall ranking CSV file, applies norvisualization with cutoff 100, generates the circular barplot, and saves it as NOREVA-Ranking-Top.100.workflows in PNG or PDF format.: "Generate a circular barplot visualization using R graphics functions, with workflows ranked by performance score and displayed in circular layout. 4. Save the resulting figure as"
- [intro] Five well-established criteria, each with a distinct underlying theory, are integrated to ensure comprehensive evaluation of preprocessing workflows.: "Particularly, five well-established criteria, each with a distinct underlying theory, are integrated to ensure a much more comprehensive evaluation than any single criterion."
