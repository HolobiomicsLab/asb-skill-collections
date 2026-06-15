---
name: r6-object-method-invocation
description: Use when when working with large metabolomics peak tables (e.
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
derived_from:
- doi: 10.1128/mra.00997-24
  title: mpactr
- doi: 10.1021/acs.analchem.2c04632
  title: ''
evidence_spans:
- This table can be used for a variety of analyses that can be conducted in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mpactr
    doi: 10.1128/mra.00997-24
    title: mpactr
  dedup_kept_from: coll_mpactr
schema_version: 0.2.0
---

# r6-object-method-invocation

## Summary

Invoke methods on R6 reference-semantic objects to perform in-place data transformations without copying the entire data structure. This skill leverages R6's reference semantics to efficiently update metabolomics feature tables through chained filter and summary operations.

## When to use

When working with large metabolomics peak tables (e.g., hundreds of samples and thousands of features) where memory efficiency matters, invoke R6 object methods to apply filters (mispicked ions, group-based removal, coefficient of variation, in-source fragments) and extract summaries in-place rather than creating intermediate copies of the data object.

## When NOT to use

- When the input is already a filtered or aggregated feature table with no metadata; R6 object methods require a linked sample-level metadata structure to execute group-based or replicability filters.
- When memory is not a constraint and reproducibility of intermediate states is critical; R6 reference semantics make it harder to save and reload filter checkpoints compared to copy-by-value approaches.
- When the upstream peak-picking algorithm has not been applied or the data format does not conform to mpactr's expected schema (e.g., missing m/z, retention time, or intensity columns).

## Inputs

- mpactr R6 object (initialized from a peak table CSV, e.g., cultures_peak_table.csv)
- Metadata table (e.g., cultures_metadata.csv with sample group assignments)

## Outputs

- Modified mpactr R6 object (after in-place filtering)
- Named list from filter_summary() containing failed_ions and passed_ions vectors
- Data.table objects with compound identifiers and filter status columns
- CSV files exported for downstream analysis

## How to apply

Load a peak table into an mpactr R6 object using import_data(). Chain filter method calls such as filter_mispicked_ions(merge_peaks = TRUE, merge_method = "sum"), filter_group(group_to_remove = "Solvent_Blank"), filter_cv(cv_threshold = 0.2), and filter_insource_ions(cluster_threshold = 0.95) in sequence; each modifies the object in-place without duplication. After filtering, call filter_summary(data_object, 'filter_name') to retrieve a named list (failed_ions and passed_ions vectors) describing which features passed or failed each filter stage. Convert the summary vectors to data.table format with compound identifiers and filter status columns for downstream export or visualization. The R6 reference model ensures that only data pointers—not the entire feature matrix—are copied, preserving memory and improving performance compared to traditional copy-by-value workflows.

## Related tools

- **mpactr** (R6 class library providing filter_mispicked_ions(), filter_group(), filter_cv(), filter_insource_ions(), and filter_summary() methods for in-place peak table refinement) — https://github.com/mums2/mpactr
- **data.table** (Convert filter_summary() output vectors to tabular format for export and downstream statistical analysis)
- **R** (Runtime environment for executing R6 object method chains and data.table transformations)

## Examples

```
filtered_data <- import_data('cultures_peak_table.csv'); filtered_data$filter_mispicked_ions(merge_peaks = TRUE, merge_method = 'sum'); filtered_data$filter_cv(cv_threshold = 0.2); summary_result <- filtered_data$filter_summary('mispicked'); failed_dt <- as.data.table(cbind(ion_id = names(summary_result$failed_ions), status = 'failed')); fwrite(failed_dt, 'mispicked_failed_ions.csv')
```

## Evaluation signals

- Filter summary named lists contain both failed_ions and passed_ions vectors with no missing or NULL values.
- Exported data.table objects have compound identifier and filter status columns that match the ion counts reported by filter_summary().
- Memory profiling shows no duplication of the full feature matrix across multiple filter invocations (reference semantics preserved).
- Chained filter invocations complete without raising R6 reference invalidation or object state corruption errors.
- CSV exports are identical when the same filter sequence is re-run on the same input object, confirming deterministic in-place updates.

## Limitations

- R6 reference semantics mean that accidental mutations of the object outside method calls can corrupt the data state; filters assume the object remains under controlled modification.
- Filter methods are independent and order-agnostic, but the biological interpretation of 'failed' vs. 'passed' ions depends on the choice and parameterization of merge_method (e.g., 'sum' vs. other aggregation schemes) in filter_mispicked_ions().
- The cv_threshold parameter (e.g., 0.2) in filter_cv() is user-specified and must be justified by the reproducibility profile of the mass spectrometry platform; no automated threshold selection is provided.

## Evidence

- [abstract] Reference semantics in R6 classes enable in-place updates: "operates on reference semantics in which data is updated *in-place*. Compared to a shallow copy, where only data pointers are copied, or a deep copy, where the entire data object is copied in memory"
- [abstract] Memory efficiency advantage of R6 vs. copy-by-value: "Memory usage really shines when you use R6 classes vs. a traditional workflow, such as copy by"
- [methods] filter_summary() returns named list with failed and passed ions: "filter_summary() returns a named list containing two components: failed_ions and passed_ions, both of which can be displayed as data tables using head()"
- [methods] Chained filter invocation example: "filter_mispicked_ions(merge_peaks = TRUE, merge_method = "sum")"
- [readme] Independent filter design enables project-specific workflows: "All filters are independent, meaning they can be used to create a project-specific workflow"
