---
name: feature-table-blank-intensity-detection
description: Use when after loading an MZmine3-exported feature quantification table
  from non-targeted LC-MS/MS data when your experiment includes blank (negative control)
  samples and you need to remove features attributable to contamination or instrument
  background before downstream statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - MZmine3
  - Jupyter Notebook
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
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

# feature-table-blank-intensity-detection

## Summary

Detect and remove features from non-targeted LC-MS/MS feature quantification tables whose intensity in blank samples exceeds a defined threshold relative to biological samples. This step eliminates contaminants and artifacts introduced during sample preparation and analysis.

## When to use

Apply this skill after loading an MZmine3-exported feature quantification table from non-targeted LC-MS/MS data when your experiment includes blank (negative control) samples and you need to remove features attributable to contamination or instrument background before downstream statistical analysis.

## When NOT to use

- Input data lacks blank (negative control) samples — blank removal cannot be applied without blanks to calculate threshold statistics.
- Feature table has already undergone blank removal or quality filtering in a prior processing stage.
- Analysis goal does not require stringent contamination control (e.g., exploratory profiling where retention of all features is preferred).

## Inputs

- Feature quantification table (CSV) from MZmine3 processing of non-targeted LC-MS/MS data
- Sample metadata indicating which columns correspond to blank samples

## Outputs

- Filtered feature quantification table (CSV) with blank-associated features removed
- Summary statistics of blank removal (e.g., number of features removed, intensity cutoff applied)

## How to apply

Load the feature quantification table (CSV format) exported from MZmine3 processing into R or Jupyter Notebook. Identify and isolate the columns corresponding to blank samples. Calculate feature intensity statistics (mean or median) for each feature within the blank sample group. Define a threshold criterion—typically a ratio comparing blank intensity to biological sample intensity (e.g., blank-to-sample ratio > 0.5 or features present in blanks above 50th percentile of biological samples). Flag and remove features that exceed this threshold from the feature table. The rationale is that genuine biological features should show negligible intensity in blanks; elevated blank intensity indicates contamination rather than true signal.

## Related tools

- **MZmine3** (Processes raw LC-MS/MS data to generate the initial feature quantification table input)
- **R** (Environment for loading, filtering, and exporting the feature table with blank removal logic) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Jupyter Notebook** (Interactive notebook environment for executing blank removal workflow in R or Python) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS

## Examples

```
# Load feature table, identify blank columns, calculate median intensity per feature in blanks, remove features where blank median > 0.5 * median biological sample intensity, export filtered table
# In R: feature_table <- read.csv('feature_table_mzmine3.csv', row.names=1); blanks <- feature_table[, grepl('blank', colnames(feature_table), ignore.case=T)]; blank_median <- rowMedians(as.matrix(blanks)); bio_median <- rowMedians(as.matrix(feature_table[, !grepl('blank', colnames(feature_table), ignore.case=T)])); filtered <- feature_table[blank_median <= 0.5 * bio_median, ]; write.csv(filtered, 'feature_table_blank_removed.csv')
```

## Evaluation signals

- Number of features removed is reasonable relative to total features (typically 5–30% depending on contamination level) and is documented in the workflow log.
- Filtered feature table has fewer rows than the input table; blank sample columns are either removed or retained depending on downstream use.
- Manual spot-check: verify that removed features had consistently elevated intensity across blank samples and low/absent intensity in biological replicates.
- Post-removal feature table is compatible with downstream statistical analysis tools (e.g., batch correction, univariate/multivariate tests) and maintains expected sample-by-feature matrix structure.
- Threshold criterion and feature count summary are reproducible when the same cutoff is reapplied to the original table.

## Limitations

- Threshold selection is subjective; no universal ratio applies across all metabolomics experiments. Threshold must be empirically justified based on blanks vs. biological sample intensity distributions.
- If blank samples are contaminated or represent true background metabolites (e.g., ubiquitous compounds like plasticizers), removal may incorrectly eliminate genuine biological signal present at similar intensity.
- The workflow assumes blanks are true procedural blanks (e.g., solvent blanks, extraction blanks) and not experimental blanks; misclassification of sample metadata will produce incorrect filtering.

## Evidence

- [other] Calculate feature intensity statistics in blank samples (e.g., mean or median intensity per feature).: "Calculate feature intensity statistics in blank samples (e.g., mean or median intensity per feature)."
- [other] Apply blank removal criterion to filter features with intensity in blanks above a defined threshold relative to biological samples.: "Apply blank removal criterion to filter features with intensity in blanks above a defined threshold relative to biological samples."
- [readme] perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data and Feature-based Molecular Networks.: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data"
- [other] The FBMN-STATS workflow implements blank removal as a procedural step applied to non-targeted LC-MS/MS data and Feature-based Molecular Networks, positioned after data cleanup and before batch correction in the analysis pipeline.: "blank removal as a procedural step applied to non-targeted LC-MS/MS data, positioned after data cleanup and before batch correction in the analysis pipeline."
