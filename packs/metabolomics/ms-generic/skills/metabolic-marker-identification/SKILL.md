---
name: metabolic-marker-identification
description: Use when after batch effect removal and sample integration, when you have a normalized feature-by-sample abundance matrix (finalData) with corresponding sample group labels (finalLabel), and need to identify which metabolites discriminate between biological conditions or phenotypes for focused.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3172
  tools:
  - LargeMetabo
  - FSelector
  - e1071
  - mixOmics
  - varSelRF
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bib/bbac455
  title: LargeMetabo
evidence_spans:
- install_github("LargeMetabo/LargeMetabo", force = TRUE, build_vignettes = TRUE)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_largemetabo_cq
    doi: 10.1093/bib/bbac455
    title: LargeMetabo
  dedup_kept_from: coll_largemetabo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bib/bbac455
  all_source_dois:
  - 10.1093/bib/bbac455
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolic-marker-identification

## Summary

Identifies discriminative metabolic markers from feature-by-sample metabolomic data matrices using statistical and machine-learning strategies. This skill applies one of 13 methods (fold change, t-test, PLS-DA, random forest, SAM, etc.) to rank metabolites by their capacity to distinguish between sample groups, producing ranked marker tables for downstream annotation and pathway analysis.

## When to use

After batch effect removal and sample integration, when you have a normalized feature-by-sample abundance matrix (finalData) with corresponding sample group labels (finalLabel), and need to identify which metabolites best discriminate between biological conditions or phenotypes for focused annotation and validation.

## When NOT to use

- Input data has not undergone batch effect removal or is not normalized—markers identified will be confounded by technical artifacts rather than true biological signals.
- Sample group labels are missing or inconsistent in length with the number of data columns.
- Number of samples per group is very small (<3) and method requires robust statistical power (e.g., t-test, SAM)—results will have high false-discovery rate.

## Inputs

- finalData (feature-by-sample matrix: rows=metabolites/m/z features, columns=samples, values=normalized abundance intensities)
- finalLabel (vector of sample group assignments, length=ncol(finalData))

## Outputs

- MarkerResult object containing ranked marker table (e.g., FC_table with metabolite IDs, fold-change values, statistical ranks)
- Delimited marker file (CSV or TSV) with selected metabolites and their discriminative scores

## How to apply

Call Marker_Identify(finalData, finalLabel, method=<strategy>) where strategy is one of: 'FC' (fold change), 't-test', 'Wilcoxon', 'PLS-DA', 'OPLS-DA', 'SAM', 'CFS', 'Relief', 'RF-RFE', 'SVM-RFE', 'Chi-squared', 'entropy', or 'linear model/empirical Bayes'. The function computes discriminative scores (e.g., fold-change ratios, statistical p-values, feature importance ranks) between groups. Select method based on data distribution (parametric vs. non-parametric), sample size, and number of groups. The returned MarkerResult object contains a ranked table (e.g., FC_table) with metabolite identifiers, computed scores, and statistical rankings. Extract and filter the ranked table by appropriate thresholds (e.g., fold-change magnitude, adjusted p-value cutoff) before exporting as delimited file for downstream metabolite annotation.

## Related tools

- **LargeMetabo** (Implements Marker_Identify() function and houses 13 marker identification strategies; orchestrates entire metabolomic workflow from data integration through marker ranking.) — https://github.com/LargeMetabo/LargeMetabo
- **FSelector** (Provides correlation-based feature selection (CFS) and entropy-based filter methods for marker identification.)
- **e1071** (Supports SVM-RFE (support vector machine-recursive feature elimination) strategy.)
- **mixOmics** (Enables PLS-DA and OPLS-DA marker identification strategies.)
- **varSelRF** (Implements random forest-recursive feature elimination (RF-RFE) marker selection.)

## Examples

```
finalData <- MarkerData$finalData
finalLabel <- MarkerData$finalLabel
MarkerResult <- Marker_Identify(finalData, finalLabel, method="FC")
MarkerResult$FC_table[1:5,]
```

## Evaluation signals

- MarkerResult object is successfully instantiated and contains a non-empty ranked table with metabolite identifiers, computed scores (fold-change, p-values, or feature importance), and rank positions.
- Ranked table column schema matches expected output (e.g., FC_table contains m/z, metabolite ID, fold-change magnitude, adjusted p-value, and rank order).
- Selected markers show expected separation between sample groups in downstream sample separation plots (e.g., HCA, PCA, PLS-DA score plots)—marked metabolites cluster samples by group better than random features.
- Marker fold-change magnitudes and p-value distributions are consistent with method assumptions (e.g., fold-change scores are positive, p-values fall in [0,1], feature importance scores are normalized).
- Exported marker file is properly delimited (CSV/TSV) with consistent column count and no missing values in core columns.

## Limitations

- Performance depends heavily on method choice and data characteristics; no single method is optimal for all metabolomic datasets—parametric tests (t-test) assume normality; non-parametric tests (Wilcoxon, SAM) are robust but may sacrifice power in small samples.
- Markers identified reflect only group discrimination in the current cohort and may not generalize to independent validation cohorts without external validation.
- Multiple testing correction is applied within each method (e.g., FDR adjustment), but comparative performance across all 13 strategies is not systematically benchmarked in the README; practitioners must evaluate method suitability for their biological question.
- Fold-change alone (method='FC') does not account for statistical significance and can highlight spurious markers with large ratios but high variance; should be combined with p-value filtering post-hoc.

## Evidence

- [other] The Marker_Identify() function accepts finalData and finalLabel, returns MarkerResult with FC_table: "Call Marker_Identify(finalData, finalLabel, method='FC') to compute fold-change values between sample groups using the fold-change algorithm. 3. Extract and structure the resulting FC_table"
- [readme] 13 marker identification strategies are available in LargeMetabo: "In the marker identification step, there are 13 popular strategies to identify metabolic markers for the given dataset. These strategies include fold change (FC), partial least squares discrimination"
- [readme] Input data structure: feature-by-sample matrix with mass, retention time, intensity columns: "Before data integration, the csv files containing a feature-by-sample matrix should be prepared in advance. Each dataset (csv file) contains five essential columns providing the information of mass,"
- [other] Marker table is saved as delimited file after extraction: "Save the FC_table as a delimited file (CSV or TSV format)."
- [readme] Marker identification follows batch removal and precedes annotation: "After data integration, it was essential to remove the unwanted variations among different batches. There are four sample separation methods for visualizing the clustering and separation of different"
