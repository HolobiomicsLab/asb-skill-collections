---
name: feature-consolidation-across-batches
description: Use when you have two or more CSV feature tables from separate metabolomic experiments (each containing mass, retention time, intensity, isotope, and adduct columns), and you need to align and merge them into a single feature-by-sample matrix where features from different experiments are matched if.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R (>=)
  - LargeMetabo
  - R
derived_from:
- doi: 10.1093/bib/bbac455
  title: LargeMetabo
evidence_spans:
- Dependent on R (>= 3.5.0)
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
---

# feature-consolidation-across-batches

## Summary

Consolidate metabolomic features from multiple analytical experiments into a single aligned feature matrix by matching features across datasets using retention time and mass-to-charge ratio tolerance thresholds. This skill is essential for combining data from different LC-MS/MS batches or experimental runs into a unified matrix suitable for downstream analysis.

## When to use

You have two or more CSV feature tables from separate metabolomic experiments (each containing mass, retention time, intensity, isotope, and adduct columns), and you need to align and merge them into a single feature-by-sample matrix where features from different experiments are matched if their retention times and m/z values fall within specified tolerances. This occurs before batch effect removal or statistical analysis.

## When NOT to use

- Input data are already in a single feature table from one analytical experiment — consolidation is redundant.
- Feature tables lack required columns (mass, retention time, intensity, isotope, adduct) — preprocessing is needed before consolidation.
- Tolerance parameters are unknown and cannot be estimated from instrument specifications — parameter optimization is required first.

## Inputs

- MutileGroup: list of multiple CSV feature tables, each containing feature-by-sample matrix with mass, retention time, intensity, isotope, and adduct columns
- RTTolerance1: numeric, retention time tolerance in minutes for primary integration phase (e.g., 10)
- mzTolerance1: numeric, m/z tolerance in mass units for primary integration phase (e.g., 0.1)
- RTTolerance2: numeric, retention time tolerance in minutes for secondary integration phase (e.g., 10)
- mzTolerance2: numeric, m/z tolerance in mass units for secondary integration phase (e.g., 0.1)

## Outputs

- AlignData: consolidated feature matrix with aligned features across all input datasets, containing unified feature identifiers, consolidated retention times, consolidated m/z values, and intensity values across all samples from all experiments

## How to apply

Load each CSV feature table as a MutileGroup dataset into R, ensuring each contains the five essential columns: mass (m/z), retention time (RT), intensity, isotope, and adduct information, with samples in columns and sample names in the first row. Call Integrate_Data() with four tolerance parameters: RTTolerance1 and mzTolerance1 for primary phase integration (typically 10 min and 0.1 m/z for high-resolution instruments), and RTTolerance2 and mzTolerance2 for secondary phase integration (same or refined values). The function will match features across all input datasets using these tolerances and produce a consolidated feature matrix with unified feature identifiers, aligned retention times, and aligned m/z values. Verify alignment by checking that the output row count reflects merged features (typically fewer than the sum of input rows due to consolidation), that RT and m/z columns are present, and that no null values exist in key annotation fields.

## Related tools

- **LargeMetabo** (R package providing Integrate_Data() function for multi-experiment feature consolidation) — https://github.com/LargeMetabo/LargeMetabo
- **R** (Runtime environment (≥ 3.5.0) required to execute consolidation workflow) — https://www.r-project.org

## Examples

```
AlignData <- Integrate_Data(MutileGroup, RTTolerance1 = 10, mzTolerance1 = 0.1, RTTolerance2 = 10, mzTolerance2 = 0.1); AlignData[1:5,1:5]
```

## Evaluation signals

- Output feature matrix has fewer or equal rows than the sum of input rows, indicating successful feature merging across datasets
- All rows in consolidated matrix contain non-null values in mass (m/z), retention time, and feature identifier columns
- Aligned retention time and m/z values fall within ±RTTolerance1/RTTolerance2 and ±mzTolerance1/mzTolerance2 of at least one feature from each matched batch
- Intensity values are preserved for all samples across all input experiments in the output matrix
- Feature count reduction demonstrates meaningful consolidation (e.g., 10,000 + 9,500 input features → ~15,000 output features, not 19,500)

## Limitations

- Consolidation quality depends critically on accurate retention time and m/z calibration across experiments; miscalibrated data will result in false negative matches
- Tolerance parameters are user-specified and must be chosen based on instrument type and analytical method; overly loose tolerances cause spurious merges, overly strict tolerances prevent legitimate matches
- Two-phase integration strategy (primary and secondary tolerances) implies a sequential matching process; rationale and behavior of the secondary phase are not detailed in the provided documentation
- No built-in mechanism described for resolving ambiguous matches (e.g., when a feature from Experiment A falls within tolerance of multiple features in Experiment B)

## Evidence

- [intro] consolidate multiple metabolomic datasets from different analytical experiments: "For data integration, multiple datasets from different analytical experiments can be used as the input of the LargeMetabo package"
- [readme] five essential columns and tolerance parameters: "Each dataset (csv file) contains five essential columns providing the information of mass, retention time, intensity, isotope and adduct"
- [readme] four tolerance parameters in two phases: "AlignData <- Integrate_Data(MutileGroup, RTTolerance1 = 10, mzTolerance1 = 0.1, RTTolerance2 = 10, mzTolerance2 = 0.1)"
- [other] unified output with aligned features: "producing an aligned feature matrix combining all input datasets"
- [other] verification checklist: "Verify alignment completeness by checking row count, presence of RT/m/z columns, and absence of null values in key fields"
