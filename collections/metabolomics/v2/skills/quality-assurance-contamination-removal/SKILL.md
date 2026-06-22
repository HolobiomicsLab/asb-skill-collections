---
name: quality-assurance-contamination-removal
description: Use when you have a feature quantification table exported from MZmine3 processing of non-targeted LC-MS/MS data that includes both biological samples and blank/control samples, and you need to identify and exclude features whose intensity is driven by contamination in blanks rather than true.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - R
  - MZmine3
  - Jupyter Notebook
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Quality Assurance: Contamination Removal

## Summary

This skill filters feature quantification tables from non-targeted LC-MS/MS data to remove features attributable to blank samples, eliminating contamination artifacts before downstream statistical analysis. It is positioned after data cleanup and before batch correction in the FBMN-STATS workflow, ensuring that blank-associated features do not confound metabolic signatures.

## When to use

Apply this skill when you have a feature quantification table exported from MZmine3 processing of non-targeted LC-MS/MS data that includes both biological samples and blank/control samples, and you need to identify and exclude features whose intensity is driven by contamination in blanks rather than true biological signal. This is essential before batch correction and statistical testing to avoid spurious associations.

## When NOT to use

- Input is already a curated feature table with blanks pre-removed or from a workflow that does not use blank samples.
- Blank samples are not available or not properly labeled in the input table.
- The analysis goal is to study contamination itself rather than remove it from biological data.

## Inputs

- Feature quantification table (CSV) from MZmine3 processing
- Sample metadata identifying which columns correspond to blank samples
- Intensity threshold ratio or criterion (e.g., biological sample mean / blank mean)

## Outputs

- Filtered feature quantification table (CSV) with blank-associated features removed
- Quality report documenting number of features removed and threshold applied

## How to apply

Load the feature quantification table (CSV format from MZmine3) into R or Jupyter Notebook, ensuring blank sample columns are labeled and identifiable. Extract blank sample intensity columns and calculate summary statistics (mean or median) per feature within blanks. Define a threshold—typically a ratio comparing blank feature intensity to biological sample intensity (e.g., sample/blank > 3)—to classify features as contamination. Remove all features that fail this threshold from the feature table. Export the filtered feature table as a CSV file, documenting the threshold and number of features removed for reproducibility and quality reporting.

## Related tools

- **MZmine3** (Generates the initial feature quantification table from raw LC-MS/MS data; outputs are the substrate for blank removal)
- **R** (Statistical computing environment for loading, filtering, and exporting feature tables with blank removal logic) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS
- **Jupyter Notebook** (Interactive environment for executing blank removal workflow in R or Python) — https://github.com/Functional-Metabolomics-Lab/FBMN-STATS

## Evaluation signals

- Number of features removed is documented and reasonable (typically 5–20% of total features, depending on contamination severity).
- Filtered feature table has fewer columns (blanks removed) and fewer rows (contaminated features removed) than input.
- No features remain in the output table that have higher mean intensity in blanks than in all biological samples combined.
- Quality report lists threshold used and provides before/after feature counts.
- Subsequent batch correction and statistical analyses show no systematic batch or contamination effects attributable to blanks.

## Limitations

- Threshold selection is data-dependent and user-defined; no single cutoff is optimal across all datasets. Guidance from the article or domain knowledge should inform threshold choice.
- If blank samples are few or have very low intensity relative to biological samples, statistical estimation of blank intensity may be unstable.
- Blank removal does not address other sources of noise (e.g., instrumental drift, matrix effects); it should be used in combination with data cleanup and batch correction.
- Features present in blanks but at very low, non-significant levels may be incorrectly flagged if threshold is too stringent, removing real but trace biological features.

## Evidence

- [intro] FBMN-STATS workflow blank removal rationale: "The FBMN-STATS workflow implements blank removal as a procedural step applied to non-targeted LC-MS/MS data and Feature-based Molecular Networks, positioned after data cleanup and before batch"
- [other] Blank removal workflow steps: "1. Load the feature quantification table exported from MZmine3 processing of MSV000082312 and MSV000085786 into R or Jupyter Notebook. 2. Identify and extract blank sample columns from the feature"
- [readme] Blank removal in full workflow context: "perform data merging, data cleanup, blank removal, batch correction, and univariate and multivariate statistical analyses on their non-targeted LC-MS/MS data and Feature-based Molecular Networks"
- [readme] Tools for implementation: "To easily install and run Jupyter Notebook in R, follow the steps in the document according to your preferred OS"
