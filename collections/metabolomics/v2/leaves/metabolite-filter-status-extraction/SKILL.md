---
name: metabolite-filter-status-extraction
description: Use when after chaining one or more mpactr filter operations (mispicked,
  group, cv, insource) on an imported peak table and before generating quality-control
  reports or interactive visualizations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mpactr
  - data.table
  - ggplot & plotly
  techniques:
  - LC-MS
  license_tier: open
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-filter-status-extraction

## Summary

Extract and tabulate the filtering fate (pass/fail status and failure reason) for each compound across all applied quality-control filters in a metabolomics peak table. This skill produces a structured summary required for reproducibility reporting and downstream visualization of which features survive the filtering pipeline.

## When to use

After chaining one or more mpactr filter operations (mispicked, group, cv, insource) on an imported peak table and before generating quality-control reports or interactive visualizations. Use this skill when you need to document which compounds passed all filters, which failed, and which specific filter(s) caused each failure—especially for multi-group metabolomics datasets where filter performance varies across sample types (e.g., solvent blanks vs. biological samples).

## When NOT to use

- Input peak table has not yet been imported with import_data() or filter operations have not been applied; qc_summary() requires a processed mpactr object.
- You need only a binary pass/fail flag without tracking which specific filter caused failure; qc_summary() returns the filter name, not just a boolean.
- Peak table is already in a non-mpactr format (e.g., raw Progenesis CSV); qc_summary() only works on mpactr-class objects.

## Inputs

- filtered mpactr object (S4 object post-import_data and chained filter operations)
- compound feature table with m/z, retention time, and abundance across samples

## Outputs

- data.table with compound identifiers and filtering status (one row per compound)
- CSV export of filter status table for reporting and visualization

## How to apply

Load the filtered mpactr object created by chaining import_data() and filter operations (e.g., filter_mispicked_ions(), filter_group(), filter_cv(), filter_insource_ions()). Call the qc_summary() function on this object to generate a data.table with one row per compound, containing the compound identifier and a status column that records either 'passed' or the name of the filter that caused failure (e.g., 'mispicked', 'group', 'replicability', 'insource'). The underlying logic tracks each compound's fate through the sequential filtering chain; compounds are marked with the name of the first filter they fail. Extract and validate that the output data.table contains all input compound IDs and contains only valid status labels. Save the resulting data.table as CSV for integration with downstream visualization (e.g., scatter plots of m/z vs. retention time colored by filter fate) and statistical reporting.

## Related tools

- **mpactr** (R package providing qc_summary() function and upstream filter operations; generates and manipulates mpactr-class objects) — https://github.com/mums2/mpactr
- **R** (Execution environment for calling qc_summary() and data.table manipulation)
- **data.table** (Data structure returned by qc_summary(); used for fast tabular I/O and CSV export)
- **ggplot & plotly** (Downstream visualization of filter status by plotting features in m/z-retention time space, colored by filter fate)

## Examples

```
qc_summary(filtered_mpactr_obj) |> as.data.frame() |> write.csv('filter_status.csv', row.names = FALSE)
```

## Evaluation signals

- Output data.table contains exactly one row per input compound (no duplicates, no omissions); verify by comparing nrow(qc_summary_output) to nrow(original_peak_table).
- All values in the status column are either 'passed' or one of the four filter names ('mispicked', 'group', 'replicability', 'insource'); no NA or unexpected values.
- Compound identifiers in the output match those in the input peak table and are unique; verify with setkey() and uniqueness checks.
- When saved to CSV and reloaded, the data.table structure and row counts are preserved; validate with identical() or nrow/ncol equivalence.
- Manual spot-check: a subset of compounds known to fail the group filter (e.g., overrepresented in solvent blanks) should appear in output with status='group'; compounds passing all filters should have status='passed'.

## Limitations

- qc_summary() records only the first filter in the chain that causes a compound to fail; if a compound would fail multiple filters, only the first failure reason is stored, so the full failure cascade is not captured.
- Filter status depends critically on the order of filter operations in the chain; reordering filters may change which compounds are marked as failed by which filter.
- The function assumes all upstream filters (import_data, filter_*) have been applied without errors; if filters are incomplete or corrupted, qc_summary() output will be incomplete or misleading.
- No built-in validation that the filtered object was created with standard mpactr parameters; non-standard parameter sets may produce unexpected status labels.

## Evidence

- [other] Finding: qc_summary output structure: "The qc_summary() function returns a data.table with compound ids and their filtering status, where failed ions are labeled with the name of the filter they failed."
- [methods] Method: qc_summary workflow: "Call mpactr function qc_summary() on the filtered object to generate a data.table with columns for compound identifier and filter status."
- [methods] Validation: expected status labels: "Extract the resulting data.table and verify it contains compound IDs and status labels (e.g., 'passed', 'mispicked', 'group', 'replicability', 'insource')."
- [methods] Use case: visualization input: "Visualizing each compound by m/z and retention time, and their fate during filtering may be useful to see if filters are removing features at certain retention time or m/z ranges."
- [readme] Tool: mpactr filter suite: "mpactr is a collection of filters for the purpose of identifying high quality MS1 features by correcting peak selection errors introduced during the pre-processing of tandem mass spectrometry data."
