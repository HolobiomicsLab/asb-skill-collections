---
name: metabolomic-feature-alignment
description: Use when you have two or more CSV feature tables from independent metabolomic experiments (each with RT, m/z, intensity, isotope, and adduct columns), and you need to merge them into a single aligned feature matrix for downstream batch effect removal, marker identification, or pathway analysis.
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
  techniques:
  - LC-MS
  - GC-MS
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

# metabolomic-feature-alignment

## Summary

Align and integrate multiple metabolomic datasets from different analytical experiments into a unified feature matrix by matching features across datasets using retention time (RT) and mass-to-charge ratio (m/z) tolerance parameters. This skill is essential when combining data from separate LC-MS experiments that measure the same or overlapping sets of metabolites but require standardization to a common feature space.

## When to use

You have two or more CSV feature tables from independent metabolomic experiments (each with RT, m/z, intensity, isotope, and adduct columns), and you need to merge them into a single aligned feature matrix for downstream batch effect removal, marker identification, or pathway analysis. The datasets may contain duplicate features (same metabolite detected in multiple runs) that must be consolidated based on RT and m/z proximity rather than treated as separate features.

## When NOT to use

- Input is already a single aligned feature table from a unified analytical run (no inter-experiment consolidation needed).
- Datasets are from fundamentally incompatible analytical platforms (e.g., combining GC-MS and LC-MS without prior normalization) without domain-specific justification.
- Feature tables lack essential metadata columns (RT, m/z, or intensity annotations) required for alignment matching.

## Inputs

- MutileGroup: collection of feature-by-sample CSV tables with mandatory columns: mass (m/z), retention time (RT), intensity, isotope annotation, adduct type; sample names in first row; features in rows
- RTTolerance1: numeric scalar (seconds), primary-phase retention time tolerance threshold
- mzTolerance1: numeric scalar (Da or ppm), primary-phase mass-to-charge tolerance threshold
- RTTolerance2: numeric scalar (seconds), secondary-phase retention time tolerance threshold
- mzTolerance2: numeric scalar (Da or ppm), secondary-phase mass-to-charge tolerance threshold

## Outputs

- AlignData: unified feature-by-sample matrix with consolidated feature identifiers, aligned retention times (RT), aligned mass-to-charge ratios (m/z), and combined intensity values across all input datasets
- Integrated feature matrix suitable for batch effect removal and downstream analysis

## How to apply

Load each CSV feature table into R as a MutileGroup object (a collection of feature-by-sample matrices with RT and m/z annotations). Call the Integrate_Data() function from the LargeMetabo package, specifying two pairs of tolerance parameters: RTTolerance1 and mzTolerance1 for primary-phase alignment, and RTTolerance2 and mzTolerance2 for secondary-phase alignment. These tolerances define the matching window: features are considered identical if their RT values differ by ≤ RTTolerance and m/z values differ by ≤ mzTolerance. The function returns a unified feature matrix with consolidated feature identifiers and aligned RT and m/z values. Choose tolerance values based on your instrument resolution and analytical method; typical values range from 10 seconds for RT and 0.1 Da for m/z. Verify alignment by inspecting the output matrix dimensions, confirming no null values in RT/m/z columns, and validating that the number of rows increases appropriately when integrating multiple datasets.

## Related tools

- **LargeMetabo** (R package containing Integrate_Data() function for multi-experiment feature alignment and downstream metabolomic analysis) — https://github.com/LargeMetabo/LargeMetabo
- **R** (Runtime environment (≥ 3.5.0) required for LargeMetabo execution) — https://www.r-project.org

## Examples

```
AlignData <- Integrate_Data(MutileGroup, RTTolerance1 = 10, mzTolerance1 = 0.1, RTTolerance2 = 10, mzTolerance2 = 0.1); AlignData[1:5,1:5]
```

## Evaluation signals

- Output matrix row count is consistent with expected feature consolidation (typically fewer rows than the sum of input rows due to duplicate removal).
- All RT and m/z columns in output contain numeric values with no missing (NA) entries in consolidated features.
- Feature identifiers in output are unique and traceable to input dataset origins.
- Intensity values for aligned features reflect appropriate aggregation (e.g., averaging or summing across matched features from different datasets).
- Spot-check: select 5–10 features from the output, verify their RT and m/z values fall within the specified tolerance windows of their source features in input datasets.

## Limitations

- Alignment quality is sensitive to tolerance parameter choice; overly strict tolerances may cause true duplicates to remain unmerged, while loose tolerances risk spurious cross-dataset matches.
- The two-phase tolerance scheme (primary and secondary) implies a hierarchical matching strategy whose rationale is not fully specified in the documentation; users should validate whether secondary parameters differ meaningfully from primary in their context.
- No explicit handling of isotopologues or adducts beyond input annotation columns; alignment is purely RT- and m/z-based, so different ionization states of the same metabolite may not consolidate automatically.
- Performance and memory scaling for very large datasets (hundreds of thousands of features) is not characterized in the provided documentation.

## Evidence

- [readme] For data integration, multiple datasets from different analytical experiments can be used as the input of the LargeMetabo package.: "For data integration, multiple datasets from different analytical experiments can be used as the input of the LargeMetabo package."
- [other] The Integrate_Data() function accepts MutileGroup (multiple datasets) and four tolerance parameters: RTTolerance1 and mzTolerance1 for primary phase integration, and RTTolerance2 and mzTolerance2 for secondary phase integration, producing an aligned feature matrix combining all input datasets.: "The Integrate_Data() function accepts MutileGroup (multiple datasets) and four tolerance parameters: RTTolerance1 and mzTolerance1 for primary phase integration, and RTTolerance2 and mzTolerance2 for"
- [readme] Each dataset (csv file) contains five essential columns providing the information of mass, retention time, intensity, isotope and adduct.: "Each dataset (csv file) contains five essential columns providing the information of mass, retention time, intensity, isotope and adduct."
- [other] Verify alignment completeness by checking row count, presence of RT/m/z columns, and absence of null values in key fields.: "Verify alignment completeness by checking row count, presence of RT/m/z columns, and absence of null values in key fields."
- [readme] AlignData <- Integrate_Data(MutileGroup, RTTolerance1 = 10, mzTolerance1 = 0.1, RTTolerance2 = 10, mzTolerance2 = 0.1): "AlignData <- Integrate_Data(MutileGroup, RTTolerance1 = 10, mzTolerance1 = 0.1, RTTolerance2 = 10, mzTolerance2 = 0.1)"
