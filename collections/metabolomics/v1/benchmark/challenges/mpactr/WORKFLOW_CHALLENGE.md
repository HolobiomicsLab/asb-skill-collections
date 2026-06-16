# Workflow Challenge: `coll_mpactr_workflow`


> mpactr provides functions to summarize and visualize the results of MS/MS data filtering, including tabular summaries of passing and failing ions, quality control tables for all input ions, and treemap visualizations of filtering outcomes.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

This benchmark demonstrates mpactr's filtering summary and visualization capabilities. The filter_summary() function returns a named list containing failed_ions and passed_ions components that can be displayed as data tables to inspect which ions were retained or removed by a specific filter. The qc_summary() function produces a data.table reporting the filtering status of all input ions, with passing ions marked as 'passed' and failing ions labeled by the filter name they failed. Ion counts and percentages computed from qc_summary() output via data.table syntax are rendered as treemaps using ggplot2's geom_treemap() and geom_treemap_text() functions to display status labels, counts, and percentages, with customization possible through ggplot2 scale and theme functions. The benchmark also demonstrates that mpactr's R6-based filters, such as filter_mispicked_ions(), operate using reference semantics: when called with the default copy_object=FALSE, filtering updates the original data object in-place rather than creating independent copies, as evidenced by a raw dataset of 7269 ions being reduced to 6625 ions with both the original and newly assigned variable referencing the same filtered object.

## Research questions

- What is the structure and content of the output returned by filter_summary() when applied to a filtered mpactr object with the 'mispicked' filter?
- What is the structure and content of the data.table returned by qc_summary() when applied to a fully-filtered mpactr object?
- How can filtering results from qc_summary() be visualized as a treemap showing the count and percentage of ions in each filter status category?
- Does calling filter_mispicked_ions() with copy_object=FALSE modify the original named object in place, such that both the original object and a separately assigned result object reflect the same post-filter row count?
- Does setting copy_object=FALSE in filter_mispicked_ions() cause the original data object to be modified in-place, whereas copy_object=TRUE preserves the original object's state?

## Methods overview

Load the filtered mpactr object that has undergone mispicked ions filter with merge_peaks=TRUE and merge_method='sum'. Invoke filter_summary() method on the mpactr object with filter parameter set to 'mispicked' to retrieve the named list of ion fate outcomes. Extract failed_ions and passed_ions vectors from the returned named list. Convert each vector to a data.table structure with compound identifiers and corresponding filter status columns. Validation: Confirm that the sum of failed and passed ion counts equals the total number of input ions processed by the filter, and that all compound identifiers are non-empty strings. References: source article (DOI: 10.1021/acs.analchem.2c04632) Load peak table and metadata into mpactr object using Progenesis format parser. Identify and merge mispicked isotopic patterns using retention-time and mass similarity windows with sum-based peak merging. Remove solvent blank contamination by filtering features above 1% relative abundance in solvent blank samples. Remove media blank features above 1% relative abundance threshold to eliminate background components. Flag non-reproducible compounds by computing coefficient of variation across technical replicates and removing those exceeding the 0.2 threshold. Extract and validate qc_summary() output reporting compound ID and pass/fail status for each filter step. Validation: Verify that the qc_summary data.table contains all input compounds as rows, includes a 'status' field documenting filter outcomes (passed all filters, or named filter failed), and row count is consistent with the filtered feature count reported by the vignette. References: source article (DOI: 10.1021/acs.analchem.2c04632) Extract qc_summary() data.table from filtered mpactr object and identify all unique ion status values Aggregate ion counts by status category and compute total ion population Calculate percentage of total ions for each status category Construct treemap using ggplot2 with geom_treemap() for rectangles sized by count, geom_treemap_text() for labels, and Greens color palette Render and save treemap PNG with no legend, showing status labels and percentages Validation: Treemap PNG file exists and displays all ion status categories with rectangle areas proportional to reported ion counts and percentages matching qc_summary() aggregation References: source article (DOI: 10.1021/acs.analchem.2c04632) Import peak table and metadata into an mpactr R6 object using import_data() with Progenesis format. Apply filter_mispicked_ions() with merge_peaks=TRUE, merge_method='sum', and copy_object=FALSE to a reference object; assign result to a separate variable name. Extract row counts from get_peak_table() on both the original and assigned object references. Compare row counts to verify both objects reflect identical post-filter dimensions. Validation: both the original object and the separately-assigned result object must report the same post-filter row count, confirming reference-semantic modification rather than deep copy. References: source article (DOI: 10.1021/acs.analchem.2c04632) Load cultures peak table and metadata into an mpactr object using import_data() with Progenesis format. Apply filter_mispicked_ions() with copy_object=FALSE; record row counts of both original and returned objects and check object identity. Reload data and apply filter_mispicked_ions() with copy_object=TRUE; record row counts and object identity. Construct a two-row comparison table contrasting object state behavior under each reference semantics setting. Validation: verify that copy_object=FALSE produces identical row counts in original and assigned objects (indicating in-place mutation), while copy_object=TRUE produces potentially different row counts (indicating independent copy). References: source article (DOI: 10.1021/acs.analchem.2c04632)

**Domain:** metabolomics

**Techniques:** feature-detection, quality-control, clustering, correlation-analysis

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** mpactr is designed to correct for errors that occur during the pre-processing of raw tandem MS/MS data. _[grounded: mpactr_system]_
- **(finding)** mpactr provides filters to identify and remove mispicked ions, which are isotopic patterns that are incorrectly split during preprocessing. _[grounded: mpactr_system]_
- **(finding)** mpactr provides filters to identify and remove ions that are above a relative abundance threshold in solvent blanks. _[grounded: mpactr_system]_
- **(finding)** mpactr provides filters to identify and remove non-reproducible ions that are inconsistent between technical replicates. _[grounded: mpactr_system]_
- **(finding)** mpactr provides filters to identify and remove insource ions, which are fragment ions created during ionization before fragmentation in the tandem MS/MS workflow. _[grounded: mpactr_system]_
- **(finding)** The filter_mispicked_ions function checks for similar ions based on retention time and mass using the parameters ringwin, isowin, trwin and max_iso_shift. _[grounded: mpactr_system]_
- **(finding)** The filter_group function identifies ions above a relative abundance threshold in a specific biological group. _[grounded: comp_filter_group]_
- **(finding)** The filter_cv function identifies non-reproducible ions by coefficient of variation between technical replicates. _[grounded: comp_filter_cv]_
- **(finding)** The filter_insource_ions function conducts ion deconvolution via retention time correlation matrices within MS1 scans.
- **(finding)** mpactr is built on an R6 class-system, meaning it operates on reference semantics in which data is updated in-place. _[grounded: mpactr_system]_
- **(finding)** Reference semantics in R6 classes differ from shallow copy, where only data pointers are copied, and from deep copy, where the entire data object is copied in memory.
- **(finding)** The default setting for the copy_object parameter in mpactr filters is FALSE, which operates on reference semantics. _[grounded: mpactr_system]_
- **(finding)** Using the default copy_object = FALSE makes for an extremely fast and memory-efficient way to chain mpactr filters together. _[grounded: mpactr_system]_
- **(finding)** The filter_summary function allows users to view passing and failing ions for a single filter. _[grounded: comp_filter_summary]_
- **(finding)** The qc_summary function returns a data.table reporting the compound id and filtering status for each input ion. _[grounded: comp_qc_summary]_
- **(finding)** mpactr requires at minimum a feature table in Progenesis format and a metadata file with columns for Injection, Sample_Code, and Biological_Group. _[grounded: mpactr_system]_
- **(finding)** The Injection column in the mpactr metadata file is expected to match sample column names in the peak table. _[grounded: mpactr_system]_
- **(finding)** The Sample_Code column in the mpactr metadata file is the id for technical replicate groups. _[grounded: mpactr_system]_
- **(finding)** The Biological_Group column in the mpactr metadata file is the id for biological replicate groups. _[grounded: mpactr_system]_
- **(finding)** The get_raw_data function extracts the unfiltered peak table used as input to mpactr. _[grounded: mpactr_system]_
- **(finding)** The get_peak_table function extracts the filtered peak table with filters that have been applied. _[grounded: comp_get_peak_table]_
- **(finding)** The get_metadata function extracts metadata from an mpactr object. _[grounded: mpactr_system]_
- **(finding)** The raw peak table in mpactr does not change as filters are applied to the data. _[grounded: mpactr_system]_
- **(finding)** mpactr uses R6 environments to enable reference semantics and fast filter execution. _[grounded: mpactr_system]_
- **(finding)** Functions in R rely on call-by-value semantics where parameterized values are treated as local variables.
- **(finding)** R6 classes allow sending variables by reference to functions using environment semantics.
- **(finding)** Memory usage is improved when using R6 classes compared to traditional copy-by-value workflows.
- **(finding)** The downstream analyses in mpactr include creating interactive plots of input features and their filtering fate using ggplot and plotly. _[grounded: mpactr_system]_
- **(finding)** The downstream analyses in mpactr include correlating sample profiles at multiple levels using Hmisc and corrplot. _[grounded: mpactr_system]_
- **(finding)** The downstream analyses in mpactr include visualizing sample clustering as a dendrogram with ggdendro. _[grounded: mpactr_system]_
- **(finding)** The downstream analyses in mpactr include calculating fold change between two biological groups. _[grounded: mpactr_system]_
- **(finding)** The downstream analyses in mpactr include visualizing fold change, m/z, and retention time as a 3D scatter plot. _[grounded: mpactr_system]_
- **(finding)** The downstream analyses in mpactr include conducting t-tests for fold change differences and calculating p-values and q-values. _[grounded: mpactr_system]_
- **(finding)** The downstream analyses in mpactr include visualizing significant fold change differences in a volcano plot. _[grounded: mpactr_system]_
- **(finding)** Tandem MS/MS datasets can be filled with many zeros due to compounds not being detected in certain groups.
- **(finding)** When a compound is found in the experimental group but not in the control group, fold change calculation yields an infinite number.
- **(finding)** When a compound is not found in either the experimental or control group, fold change calculation yields NaN.
- **(finding)** Adding pseudo-counts to all counts prior to calculating fold change alleviates division by zero.
- **(finding)** A Spearman correlation test is used by Hmisc::rcorr to measure correlation between samples. _[grounded: tool_hmisc]_
- **(finding)** Euclidean distance is used to calculate the distance between samples for dendrogram clustering.
- **(finding)** Complete linkage is used as the clustering method for hierarchical clustering of samples.
- **(finding)** The PTY087I2 dataset contains 38 samples for biological groups of solvent blanks, media blanks, and Streptomyces sp. PTY08712 grown with and without cerium. _[grounded: dataset_PTY087I2]_
- **(finding)** The get_group_averages function is used to extract group means from filtered compounds in mpactr. _[grounded: mpactr_system]_
- **(finding)** Log2 transformation is applied to fold change values for visualization and analysis.
- **(finding)** A fold change threshold of 1.5 is used in the volcano plot example to define significant metabolite abundance differences.
- **(finding)** A p-value threshold of 0.05 is used in the volcano plot example to define significant metabolite abundance differences.
- **(finding)** Volcano plots display log2 fold change values on the x-axis and negative log10 p-values on the y-axis.
- **(finding)** The filter_cv function cannot be applied to data that does not contain technical replicates. _[grounded: comp_filter_cv]_
- **(finding)** Highly correlated ion groups in filter_insource_ions are determined by the cluster_threshold parameter.
- **(finding)** In filter_insource_ions, the highest mass feature in a correlated ion group is identified as the likely precursor ion and retained.
- **(finding)** Filters can be chained in a customizable workflow in mpactr. _[grounded: mpactr_system]_
- **(finding)** The recommended filter order is to filter mispicked ions, then solvent blanks, prior to filtering non-reproducible or insource ions.

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- other ways to conduct the analyses shown; the beauty of R
- copy_object = TRUE can be used instead of default copy_object = FALSE for traditional R style objects

## Steps

### Step `task_001`
- Title: Reproduce ion filtering summary via filter_summary() for mispicked ions filter
- Task kind: `reproduction`
- Task: Apply filter_summary() to a filtered mpactr object to retrieve the ion fate data (passed and failed ions) for the 'mispicked' filter and output two structured data tables.
- Inputs:
  - A filtered mpactr R6 object that has undergone filter_mispicked_ions with merge_peaks=TRUE and merge_method='sum'
- Expected outputs:
  - Data table of ions that failed the mispicked filter (removed or merged due to isotopic pattern misidentification)
  - Data table of ions that passed the mispicked filter (retained in feature table)
- Tools: R, mpactr, data.table
- Landmark output files: failed_ions_mispicked.csv, passed_ions_mispicked.csv
- Primary expected artifact: `mispicked_filter_summary.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce qc_summary() output table for all input ions after full filter pipeline
- Task kind: `reproduction`
- Task: Run qc_summary() on a fully-filtered mpactr object (cultures dataset filtered for mispicked ions, group contamination, and low coefficient of variation) to produce a data.table reporting compound IDs and their pass/fail status across all applied filters. Verify the output structure matches the documented vignette specification.
- Inputs:
  - cultures_peak_table.csv — Progenesis-format peak table with columns: compound, m/z, retention time (min), raw abundance for each sample injection
  - cultures_metadata.csv — sample metadata table with columns: Injection, Sample_Code, Biological_Group (minimum required); example contains solvent blanks, media blanks, and biological replicates
- Expected outputs:
  - qc_summary data.table with rows corresponding to input compounds and columns: compound ID, status (indicating which filter each ion failed or if the ion passed all applied filters)
- Tools: mpactr, R, data.table
- Landmark output files: filtered_data_post_mispicked.rds, filtered_data_post_solvent_blank.rds, filtered_data_post_media_blank.rds, filtered_data_post_cv.rds
- Primary expected artifact: `qc_summary.csv`

### Step `task_003`
- Depends on: `task_002`
- Title: Reproduce treemap visualisation of filtering QC using qc_summary(), ggplot2, and treemapify
- Task kind: `reproduction`
- Task: Extract per-status ion counts and percentages from qc_summary() data, then render a treemap visualization using geom_treemap() with the Greens color palette. Save the treemap as a PNG file.
- Inputs:
  - task_002.expected_outputs[0]: qc_summary data.table with rows corresponding to input compounds and columns: compound ID, status (indicating which filter each ion failed or if the ion passed all applied filters)
  - Filtered mpactr object (data_filtered) containing peak table and filter metadata
  - qc_summary() output: data.table with compound IDs and ion status (passed/failed filters)
- Expected outputs:
  - Treemap PNG file showing ion counts and percentages grouped by filter status (mispicked, group, replicability, insource, passed)
- Tools: R, ggplot, mpactr, data.table
- Landmark output files: qc_status_counts.csv, qc_status_percentages.csv
- Primary expected artifact: `qc_treemap.png`

### Step `task_004`
- Depends on: `task_001`
- Title: Reconstruct reference-semantics in-place update behaviour of the R6-based filter_mispicked_ions()
- Task kind: `component_reconstruction`
- Task: Verify that the mpactr R6 class filter_mispicked_ions() function operates via reference semantics when copy_object=FALSE, such that filtering a named object (data2) modifies the original object in-place without creating a separate copy. Confirm by comparing pre- and post-filter row counts in both the assigned result variable and the original object.
- Inputs:
  - Peak table in Progenesis CSV format (compound, m/z, retention time, raw abundance) and corresponding metadata file with sample information (injection, sample_code, biological_group)
- Expected outputs:
  - Numeric verification that pre-filter and post-filter row counts are identical in both the original object (data2) and the assigned result object (data2_mispicked), demonstrating reference semantics behavior
- Tools: R, mpactr, data.table
- Landmark output files: mpactr_object_imported.RData, pre_filter_row_count.txt, post_filter_row_count_original.txt, post_filter_row_count_assigned.txt

### Step `task_005`
- Depends on: `task_001`
- Title: Analyze deep-copy vs reference-semantics row counts after filter_mispicked_ions() with copy_object=TRUE vs FALSE
- Task kind: `analysis`
- Task: Apply filter_mispicked_ions() to the cultures dataset under two reference semantics conditions (copy_object=FALSE and copy_object=TRUE), then compare row counts of the original and assigned objects to verify divergence in object state. Output a two-row comparison table documenting object identity and ion counts under each condition.
- Inputs:
  - cultures_peak_table.csv
  - cultures_metadata.csv
- Expected outputs:
  - Comparison table (data.frame or data.table) with rows for copy_object=FALSE and copy_object=TRUE, columns: condition, original_object_rowcount, assigned_object_rowcount, object_identity_match
- Tools: R, mpactr, data.table
- Landmark output files: cultures_imported_data.RData, filtered_copy_false.RData, filtered_copy_true.RData
- Primary expected artifact: `reference_semantics_comparison.csv`

## Final expected outputs

- `Treemap PNG file showing ion counts and percentages grouped by filter status (mispicked, group, replicability, insource, passed)` (type: file, tolerance: hash)
- `Numeric verification that pre-filter and post-filter row counts are identical in both the original object (data2) and the assigned result object (data2_mispicked), demonstrating reference semantics behavior` (type: file, tolerance: hash)
- `Comparison table (data.frame or data.table) with rows for copy_object=FALSE and copy_object=TRUE, columns: condition, original_object_rowcount, assigned_object_rowcount, object_identity_match` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: open — validity-first.** The deterministic match-rubrics above are demoted to *informational*. The binding evaluator is **SCIENTIFIC_VALIDITY** (below). Any scientifically sound method that addresses the research question is valid, and novel findings or unexplored aspects can score positively — **different is not wrong**.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** tight

- **Composition modularity:** flat

- **Abstraction level:** concrete

- **Orchestration planning:** static

- **Data transport:** in_memory

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_mpactr_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Treemap PNG file showing ion counts and percentages grouped by filter status (mispicked, group, replicability, insource, passed)": "<locator>",
    "Numeric verification that pre-filter and post-filter row counts are identical in both the original object (data2) and the assigned result object (data2_mispicked), demonstrating reference semantics behavior": "<locator>",
    "Comparison table (data.frame or data.table) with rows for copy_object=FALSE and copy_object=TRUE, columns: condition, original_object_rowcount, assigned_object_rowcount, object_identity_match": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
