---
name: fold-change-calculation-metabolomics
description: Use when you have a feature-by-sample metabolomic intensity matrix (finalData)
  with corresponding sample group labels (finalLabel), and you need to identify metabolic
  markers ranked by their fold-change between two or more groups.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0637
  - http://edamontology.org/topic_3172
  tools:
  - LargeMetabo
  - R
  - ggplot2
  license_tier: restricted
  provenance_tier: literature
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# fold-change-calculation-metabolomics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Fold-change (FC) marker identification is a method for ranking metabolic features by their abundance ratio between sample groups in a feature-by-sample metabolomic matrix. It is used to rapidly identify differential metabolites without statistical hypothesis testing, suitable for initial screening and biomarker discovery.

## When to use

Apply this skill when you have a feature-by-sample metabolomic intensity matrix (finalData) with corresponding sample group labels (finalLabel), and you need to identify metabolic markers ranked by their fold-change between two or more groups. Use FC ranking when you prioritize simplicity and speed over statistical rigor, or as a first-pass filter before applying more stringent methods (t-test, OPLS-DA, SVM-RFE).

## When NOT to use

- Data is already a ranked marker list or pre-filtered feature table; fold-change calculation is redundant.
- Sample groups have >2 levels and you need multi-level pairwise or global comparison; consider OPLS-DA, SAM, or Kruskal–Wallis instead.
- Input matrix contains missing values or is unnormalized; preprocessing (imputation, normalization) must precede fold-change calculation.
- Your goal is statistical inference with p-values and confidence intervals; fold-change alone provides no distributional test—use t-test or Wilcoxon rank sum.

## Inputs

- finalData: numeric matrix (features × samples) containing normalized metabolite abundances
- finalLabel: character or factor vector (length = ncol(finalData)) assigning each sample to a group

## Outputs

- MarkerResult object containing FC_table: data frame with metabolite identifiers, fold-change values, and statistical rankings

## How to apply

Load the MarkerData object containing a metabolite abundance matrix (finalData, rows = features/metabolites, columns = samples) and sample group assignments (finalLabel). Call Marker_Identify(finalData, finalLabel, method='FC') in R to compute fold-change values between sample groups using the fold-change algorithm. The function returns a MarkerResult object with an FC_table containing metabolite identifiers, computed fold-change values, and rankings ordered by magnitude. Extract and inspect the FC_table to verify metabolites are ranked by fold-change; optionally save to CSV/TSV for downstream annotation or pathway enrichment.

## Related tools

- **LargeMetabo** (R package implementing Marker_Identify() function with 13 marker identification strategies including FC method) — https://github.com/LargeMetabo/LargeMetabo
- **R** (Runtime environment (≥3.5.0) for executing Marker_Identify() and post-processing FC results)
- **ggplot2** (Visualization of ranked fold-change values and distribution across metabolites)

## Examples

```
finalData <- MarkerData$finalData
finalLabel <- MarkerData$finalLabel
MarkerResult <- Marker_Identify(finalData, finalLabel, method = "FC")
head(MarkerResult$FC_table)
```

## Evaluation signals

- FC_table columns include metabolite identifier, fold-change numeric value, and rank; no missing or NaN entries in fold-change column.
- Fold-change values are non-negative; ranked metabolites show expected monotonic ordering by absolute FC magnitude.
- Number of rows in FC_table equals number of rows in finalData (all features ranked).
- When saved to CSV/TSV and re-loaded, fold-change values and rankings are preserved; no data corruption in serialization.
- Top-ranked metabolites (high FC) show expected biological consistency with known group differences (e.g., disease vs. control phenotype).

## Limitations

- Fold-change is sensitive to normalization and baseline choice; biased fold-changes can result from improper preprocessing or small denominator values in low-abundance features.
- No statistical test (p-value, confidence interval) is provided; fold-change alone cannot distinguish true signal from noise or account for variance across replicates.
- For >2 sample groups, fold-change is typically computed pairwise; no built-in multi-level or global ranking strategy is specified in the LargeMetabo documentation.
- Fold-change can be inflated by single outlier samples; robust alternatives (e.g., median fold-change, trimmed means) are not mentioned.

## Evidence

- [other] Marker_Identify() with method='FC' accepts finalData and finalLabel, returns MarkerResult with FC_table: "The Marker_Identify() function with method='FC' accepts a data matrix (finalData) and corresponding sample labels (finalLabel), and returns a MarkerResult object containing an FC_table with ranked"
- [other] Workflow: Call Marker_Identify, extract and structure FC_table, save as delimited file: "Call Marker_Identify(MarkerData, method='FC') to compute fold-change values between sample groups using the fold-change algorithm. 3. Extract and structure the resulting FC_table containing"
- [readme] 13 marker identification strategies include fold change (FC) method: "In the marker identification step, there are 13 popular strategies to identify metabolic markers for the given dataset. These strategies include fold change (FC), partial least squares discrimination"
- [readme] Example R invocation of Marker_Identify with FC method: "finalData <- MarkerData$finalData
    finalLabel <- MarkerData$finalLabel
    MarkerResult <- Marker_Identify(finalData, finalLabel, method = "FC")
    MarkerResult$FC_table[1:5,]"
- [readme] Data input format: feature-by-sample matrix with sample labels: "Before data integration, the csv files containing a feature-by-sample matrix should be prepared in advance. Each dataset (csv file) contains five essential columns providing the information of mass,"
