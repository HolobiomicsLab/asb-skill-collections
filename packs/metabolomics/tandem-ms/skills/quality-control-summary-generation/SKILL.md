---
name: quality-control-summary-generation
description: Use when after applying one or more mpactr filters (mispicked, group, CV, or insource) to a peak table in a chained filtering workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - R
  - mpactr
  - data.table
  - ggplot
  - plotly
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.2c04632
  title: MPACT
evidence_spans:
- To import these data into R, use the mpactr function
- We will be using multiple libraries for data analysis and visualization
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mpactr_cq
    doi: 10.1021/acs.analchem.2c04632
    title: MPACT
  dedup_kept_from: coll_mpactr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04632
  all_source_dois:
  - 10.1021/acs.analchem.2c04632
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# quality-control-summary-generation

## Summary

Generate a structured summary table tracking which ions passed or failed each quality-control filter in a mass spectrometry metabolomics workflow. This enables rapid assessment of filtering efficacy across all input compounds and identification of which specific filter(s) caused ion rejection.

## When to use

After applying one or more mpactr filters (mispicked, group, CV, or insource) to a peak table in a chained filtering workflow. Use this skill when you need to document filtering outcomes for reporting, visualization, or to diagnose whether ions are being over- or under-filtered at specific m/z or retention time ranges.

## When NOT to use

- Input is raw, unfiltered peak table — apply filters first before summarizing.
- Only a single filter has been applied — qc_summary is most valuable after chained multi-filter workflows to show cumulative filtering decisions.
- Goal is to visualize ion fate by m/z and retention time — use interactive plotting (ggplot + plotly) instead.

## Inputs

- filtered mpactr object (S4 class with filtered peak_table and metadata after chained filter operations)

## Outputs

- data.table with columns: compound identifier and filtering status (passed/failed filter name)
- CSV file of qc_summary data.table for reporting

## How to apply

Load the filtered mpactr object (output from chained filter operations: import_data() → filter_mispicked_ions() → filter_group() → filter_cv() → filter_insource_ions()). Call the mpactr function qc_summary() on the filtered object to generate a data.table with compound identifiers and their filtering status. The function returns a row per ion with a 'status' column indicating either 'passed' or the name of the filter that caused rejection (e.g., 'mispicked', 'group', 'replicability', 'insource'). Extract and inspect the resulting data.table to verify all compound IDs are present and status values are valid. Save the output as CSV for downstream visualization with ggplot/plotly or manual review.

## Related tools

- **mpactr** (provides qc_summary() function to generate filtering status table; orchestrates chained filter operations on mpactr S4 object) — https://github.com/mums2/mpactr
- **R** (execution environment and data manipulation runtime for calling qc_summary() and saving output)
- **data.table** (output format for qc_summary result; enables efficient tabular representation of filtering outcomes)
- **ggplot** (downstream visualization of qc_summary results as interactive plot of features and their filter fate)
- **plotly** (downstream interactive visualization of qc_summary outcomes by m/z and retention time)

## Examples

```
qc_summary(filtered_mpactr_object) |> as.data.frame() |> write.csv(file='qc_summary_output.csv', row.names=FALSE)
```

## Evaluation signals

- Output data.table has one row per input compound (matches length of original peak_table)
- All status values are valid: either 'passed' or one of the known filter names ('mispicked', 'group', 'replicability', 'insource')
- No missing/NA values in compound identifier or status columns
- CSV export is readable and preserves row/column structure without truncation or encoding errors
- Manually spot-check a subset of ions that failed: verify the failing filter matches the filtering chain applied (e.g., if filter_group(group_to_remove='Solvent_Blank') was called, ions present in solvent blank should show status='group')

## Limitations

- qc_summary() reflects only the filters applied in the current mpactr workflow — does not capture preprocessing errors from the original mass spectrometry software (Progenesis, MS-DIAL, etc.).
- Status is binary per filter (passed/failed); does not quantify severity or provide threshold values that caused rejection.
- Cannot retroactively diagnose why a filter was applied with specific parameters; requires documentation of the chained filter calls.

## Evidence

- [other] research_question_finding: "The qc_summary() function returns a data.table with compound ids and their filtering status, where failed ions are labeled with the name of the filter they failed."
- [other] workflow_step: "Call mpactr function qc_summary() on the filtered object to generate a data.table with columns for compound identifier and filter status."
- [other] status_labels: "Extract the resulting data.table and verify it contains compound IDs and status labels (e.g., 'passed', 'mispicked', 'group', 'replicability', 'insource')."
- [methods] tool_role: "creating an interactive plot of input features and the filters they failed, if any, using `ggplot` and `plotly`"
- [abstract] memory_efficiency: "We recommend using the default `copy_object = FALSE` as this makes for an extremely fast and memory-efficient way to chain mpactr filters together"
