---
name: table-join-alignment-on-identifiers
description: Use when you have a feature quantification table output from MZmine3 feature detection (rows = features, columns = sample abundance values) and a separate sample metadata file (rows = samples, columns = sample attributes) that need to be unified before downstream statistical analysis, data cleanup.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3283
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - R
  - Jupyter Notebook
  - MZmine3
  - FBMN-STATS
derived_from:
- doi: 10.1038/s41596-024-01046-3
  title: FBMN-STATS
evidence_spans:
- To easily install and run Jupyter Notebook in R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_fbmn_stats_cq
    doi: 10.1038/s41596-024-01046-3
    title: FBMN-STATS
  dedup_kept_from: coll_fbmn_stats_cq
schema_version: 0.2.0
---

# table-join-alignment-on-identifiers

## Summary

Combines a feature quantification table (from LC-MS/MS feature detection) with sample metadata into a single analysis-ready table by aligning rows on a shared sample identifier column using a join operation. This is the foundational step in the FBMN-STATS workflow for non-targeted metabolomics statistical analysis.

## When to use

You have a feature quantification table output from MZmine3 feature detection (rows = features, columns = sample abundance values) and a separate sample metadata file (rows = samples, columns = sample attributes) that need to be unified before downstream statistical analysis, data cleanup, batch correction, or multivariate analysis.

## When NOT to use

- The feature quantification table and metadata are already merged or in a single file.
- Sample identifiers do not exist or differ systematically between the two tables (e.g., different naming conventions that cannot be reconciled).
- The metadata file contains no samples that match the quantification table, making an inner join infeasible.

## Inputs

- Feature quantification table (MZmine3 output; rows = features, columns = sample abundances)
- Sample metadata file (rows = samples, columns = sample attributes)
- Shared sample identifier column name

## Outputs

- Merged analysis-ready table (CSV or TSV format; rows = features, columns = sample abundances + sample metadata attributes)

## How to apply

Load both the feature quantification table and sample metadata file using R or Jupyter Notebook. Identify the shared sample identifier column present in both tables (e.g., sample name, sample ID). Align the rows in the quantification table with corresponding sample identifiers in the metadata by performing an inner join (only matching samples) or left join (retain all samples from the quantification table) on the identifier column. After merging, verify that all expected samples are present in the merged output and that no rows were unexpectedly dropped or duplicated. Export the merged analysis-ready table as CSV or TSV format for downstream workflow steps (data cleanup, blank removal, batch correction, statistical analyses).

## Related tools

- **R** (Primary language for performing data merge operations (join functions such as merge() or dplyr::inner_join())) — https://www.r-project.org
- **Jupyter Notebook** (Interactive environment for running R or Python merge workflows with data verification and export) — https://jupyter.org
- **MZmine3** (Upstream tool that generates the feature quantification table input) — https://mzmine.github.io
- **FBMN-STATS** (Complete statistical analysis workflow that includes this data merging step as its first stage) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS

## Examples

```
merged_data <- merge(feature_table, metadata, by='sample_id', all.x=TRUE); write.csv(merged_data, 'analysis_ready_table.csv', row.names=FALSE)
```

## Evaluation signals

- The number of rows in the merged table equals the number of features in the original quantification table (no feature rows dropped).
- All sample identifiers from the metadata file appear as column headers or row attributes in the merged table.
- No NaN, NULL, or missing values appear in the shared identifier column used for the join.
- Spot-check: manually verify that 2–3 sample metadata attributes are correctly aligned with their corresponding feature abundance values.
- Row and column counts of the merged table match expected dimensions (features × samples + metadata attributes).

## Limitations

- If sample identifiers contain typos, whitespace inconsistencies, or case-sensitivity issues, the join will fail silently or produce partial matches; pre-processing identifiers (trimming, lowercasing, standardizing format) is required.
- Inner joins will discard samples present in only one table; left joins retain all features but may introduce NaN values if a feature sample is absent from metadata.
- Large datasets may cause memory constraints in Jupyter Notebook or R; users should monitor RAM usage and consider chunking or cloud alternatives (e.g., Google Colab).
- GitHub rendering of Jupyter notebooks may fail or display incorrectly; code should be copied from the rendered Google Colab or JupyterLab interface to preserve HTML and special characters.

## Evidence

- [other] load-align-join: "Load the feature quantification table (output from MZmine3 feature detection) and sample metadata file using R or Jupyter Notebook. Align rows in the quantification table with corresponding sample"
- [other] verify-export: "Verify that all samples are matched and no data loss occurred during the merge. Export the merged analysis-ready table as a CSV or TSV file for downstream statistical analysis."
- [readme] workflow-position: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data and Feature-based Molecular Networks"
- [readme] colab-file-handling: "Unlike Jupyter Notebook, it is not possible to access the files from your local computer in a Google Colab space as it is cloud-based. So we can directly upload the necessary files into the Colab"
