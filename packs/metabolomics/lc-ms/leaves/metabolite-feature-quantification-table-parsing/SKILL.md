---
name: metabolite-feature-quantification-table-parsing
description: Use when when you have completed feature detection in MZmine3 or similar tools and produced a feature quantification table (rows = features, columns = samples with intensity values), and you possess a separate sample metadata file (sample identifiers, treatment groups, batch information).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3283
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Jupyter Notebook
  - MZmine3
  techniques:
  - LC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41596-024-01046-3
  all_source_dois:
  - 10.1038/s41596-024-01046-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-feature-quantification-table-parsing

## Summary

Parse and align feature quantification tables from non-targeted LC-MS/MS feature detection (e.g., MZmine3 output) with sample metadata to create a single analysis-ready merged table for downstream statistical analysis. This skill bridges raw feature intensity data with experimental design information.

## When to use

When you have completed feature detection in MZmine3 or similar tools and produced a feature quantification table (rows = features, columns = samples with intensity values), and you possess a separate sample metadata file (sample identifiers, treatment groups, batch information). Use this skill as the mandatory first step before data cleanup, blank removal, batch correction, or statistical analyses.

## When NOT to use

- Input feature table is already merged with metadata or contains metadata columns.
- Sample identifiers in the quantification table and metadata file cannot be reliably matched (no common key column or inconsistent naming conventions).
- Feature detection has not been completed or MZmine3 output has not been generated.

## Inputs

- MZmine3 feature quantification table (CSV/TSV with features as rows, samples as columns, intensity values)
- Sample metadata file (CSV/TSV with sample identifiers and experimental variables)

## Outputs

- Merged analysis-ready feature table (CSV/TSV with features as rows, samples as columns, intensity values, with sample metadata columns integrated)

## How to apply

Load the feature quantification table (output from MZmine3 feature detection) and sample metadata file into R or Jupyter Notebook. Verify that sample identifiers in both tables are consistent (e.g., sample names, IDs). Align rows in the quantification table with corresponding sample identifiers in the metadata by performing an inner or left join operation on the shared sample identifier column. After merging, verify that all samples are matched and no data loss occurred by checking row counts before and after the join, and confirming that no missing values were unexpectedly introduced. Export the merged analysis-ready table as CSV or TSV format for input to downstream quality control and statistical analysis steps.

## Related tools

- **R** (Language and environment for loading, aligning, and joining feature quantification tables with metadata using data frame operations (e.g., merge, join functions).) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Jupyter Notebook** (Interactive computational environment for executing feature table parsing and merging workflows in R or Python.) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **MZmine3** (Source tool that generates the feature quantification table output to be parsed and merged.)

## Evaluation signals

- Row count of merged table equals row count of input metadata file (or inner join count if inner join is used); no unmatched samples.
- All sample identifiers from metadata are present in the merged table; no missing values in the join key column.
- Column count of merged table equals feature columns + metadata columns; no duplicate columns.
- Feature intensity values are preserved in the merged table with no unexpected NaN or zero inflation.
- Merged table can be successfully exported as CSV/TSV and loaded without parsing errors in downstream analysis tools.

## Limitations

- Merging assumes a consistent, single-column key (sample identifier) exists in both input files; complex multi-column keys or fuzzy matching are not addressed by the basic workflow.
- If sample identifiers are inconsistent between files (e.g., whitespace, case sensitivity, formatting), the merge will fail to match samples; manual correction of identifiers may be required.
- Inner join may cause loss of samples or features if they are absent in one of the input files; left join preserves all samples from the metadata but may introduce NaN in feature columns for unmatched samples.
- The workflow does not validate feature intensity value ranges, data types, or presence of expected metabolomic features; quality assessment occurs in downstream data cleanup steps.

## Evidence

- [other] 1. Load the feature quantification table (output from MZmine3 feature detection) and sample metadata file using R or Jupyter Notebook. 2. Align rows in the quantification table with corresponding sample identifiers in the metadata. 3. Perform inner or left join operation to combine both tables on the shared sample identifier column.: "Load the feature quantification table (output from MZmine3 feature detection) and sample metadata file using R or Jupyter Notebook. Align rows in the quantification table with corresponding sample"
- [other] 4. Verify that all samples are matched and no data loss occurred during the merge. 5. Export the merged analysis-ready table as a CSV or TSV file for downstream statistical analysis.: "Verify that all samples are matched and no data loss occurred during the merge. Export the merged analysis-ready table as a CSV or TSV file for downstream statistical analysis."
- [other] The FBMN-STATS workflow performs data merging as the first step in a statistical analysis pipeline that processes non-targeted LC-MS/MS data and Feature-based Molecular Networks, followed by data cleanup, blank removal, batch correction, and statistical analyses.: "The FBMN-STATS workflow performs data merging as the first step in a statistical analysis pipeline that processes non-targeted LC-MS/MS data and Feature-based Molecular Networks"
- [readme] Using the notebooks provided here, one can perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data and Feature-based Molecular Networks.: "Using the notebooks provided here, one can perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data"
