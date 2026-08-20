---
name: quality-control-merge-verification
description: Use when after performing an inner or left join operation to combine
  a feature quantification table (from MZmine3) with sample metadata, and before proceeding
  to data cleanup, blank removal, batch correction, or statistical analyses.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - Jupyter Notebook
  - Google Colab
  techniques:
  - LC-MS
  license_tier: open
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

# quality-control-merge-verification

## Summary

Verification step that validates successful alignment and combination of LC-MS/MS feature quantification tables with sample metadata, ensuring no data loss and complete sample matching before downstream statistical analysis. This skill confirms the merge operation was executed correctly and the resulting table is analysis-ready.

## When to use

After performing an inner or left join operation to combine a feature quantification table (from MZmine3) with sample metadata, and before proceeding to data cleanup, blank removal, batch correction, or statistical analyses. Apply this skill whenever you need confidence that all samples are correctly matched and the merged table contains complete, coherent records for downstream analysis.

## When NOT to use

- Input is already a pre-validated, published feature table from a trusted repository.
- The merge operation has not yet been performed; verification applies only after joining.
- Metadata file and feature table originate from different studies or experiments (sample IDs will not align).

## Inputs

- Feature quantification table (output from MZmine3 feature detection, typically CSV or TSV format)
- Sample metadata file (CSV or TSV with sample identifiers as a key column)
- Merged table (result of inner or left join operation)

## Outputs

- Verification report (row count match, sample identifier coverage, null value inventory)
- Validated merged analysis-ready table (confirmed to have no data loss and complete sample matching)

## How to apply

After combining the feature quantification table with metadata using a join operation on the shared sample identifier column, verify that (1) the number of rows in the merged table matches the expected sample count, (2) all sample identifiers from the metadata appear in the quantification table with no unmatched rows, (3) no null or NA values exist in the sample identifier or critical feature columns unless expected, (4) the merged table has consistent dimensions across samples (same number of features per sample), and (5) spot-check a few rows to confirm feature values and metadata attributes are aligned correctly. The rationale is that mismatches, truncation, or partial merges will propagate errors into all downstream statistical analyses, making early detection critical before investing computational effort in cleanup and analysis steps.

## Related tools

- **R** (Language for loading, merging, and validating the feature table and metadata using join operations and row/column counting functions.) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Jupyter Notebook** (Interactive environment for executing merge verification code and documenting row/column counts and sample matching results.) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Google Colab** (Cloud-based Jupyter environment for running R or Python merge verification notebooks without local installation.) — https://colab.research.google.com/github/Functional-Metabolomics-Lab/FBMN-STATS/blob/main/R/Stats_Untargeted_Metabolomics.ipynb

## Examples

```
# After merge in R, verify all samples matched:
merged_table <- read.csv('merged_features_metadata.csv', row.names=1)
metadata <- read.csv('sample_metadata.csv', row.names=1)
cat('Merged rows:', nrow(merged_table), '| Metadata samples:', nrow(metadata), '| Match:', nrow(merged_table) == nrow(metadata), '\n')
cat('Unmatched samples:', sum(!(rownames(metadata) %in% rownames(merged_table))), '\n')
cat('NA values in merged table:', sum(is.na(merged_table)), '\n')
```

## Evaluation signals

- Row count of merged table equals the sample count in the metadata file (no rows dropped or duplicated).
- All sample identifiers from the metadata file appear in the merged table with no unmatched samples.
- No unexpected null or NA values in the sample identifier column or in key feature columns (unless documented as intentional).
- Column count of merged table equals the sum of feature columns plus metadata columns.
- Spot-check of 5–10 randomly selected rows shows correct alignment between feature values and corresponding metadata attributes (e.g., sample treatment, batch, date).

## Limitations

- Verification cannot detect systematic errors in the merge logic itself (e.g., if identifiers are aliased or renamed inconsistently); manual inspection of a sample of rows is still needed.
- Large datasets may require sampling-based verification rather than full enumeration for computational efficiency.
- Metadata encoding issues (e.g., whitespace, case sensitivity in sample IDs) can cause silent partial matches; pre-merge normalization of identifiers is recommended.
- Google Colab users must manually download verification outputs at the end of the session, as files are not persistently stored; the 12-hour runtime limit may interrupt long verification tasks on very large datasets.

## Evidence

- [intro] Alignment and join rationale: "Perform inner or left join operation to combine both tables on the shared sample identifier column."
- [intro] Verification as integral step: "Verify that all samples are matched and no data loss occurred during the merge."
- [intro] Merge as first workflow step: "The FBMN-STATS workflow performs data merging as the first step in a statistical analysis pipeline that processes non-targeted LC-MS/MS data and Feature-based Molecular Networks, followed by data"
- [intro] Export for downstream use: "Export the merged analysis-ready table as a CSV or TSV file for downstream statistical analysis."
- [readme] Colab file handling limitations: "All the output files will be stored under the working directory. You need to download all the result files from the directory at the end of your session as they are only saved in the Cloud and not in"
