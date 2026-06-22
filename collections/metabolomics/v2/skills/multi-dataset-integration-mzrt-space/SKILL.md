---
name: multi-dataset-integration-mzrt-space
description: Use when you have multiple CSV feature tables from independent metabolomic experiments, each with RT and m/z annotations, and you need to produce a single consolidated feature matrix for comparative analysis across all samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3258
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
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

# multi-dataset-integration-mzrt-space

## Summary

Align and combine multiple metabolomic feature tables from different analytical experiments into a unified feature matrix by matching features across retention time (RT) and mass-to-charge ratio (m/z) dimensions using tolerance thresholds. This skill is essential when analyzing datasets generated from separate LC-MS/MS runs that must be consolidated before downstream batch correction, marker identification, or annotation.

## When to use

You have multiple CSV feature tables from independent metabolomic experiments, each with RT and m/z annotations, and you need to produce a single consolidated feature matrix for comparative analysis across all samples. Specifically, apply this skill when: (1) you are working with 2+ MutileGroup datasets as inputs, (2) each dataset contains a feature-by-sample matrix with mass, retention time, intensity, isotope, and adduct columns, (3) the first two columns are m/z and RT respectively, (4) you must decide on primary and secondary phase RT and m/z tolerance windows appropriate to your analytical platform's precision, and (5) your downstream analysis (e.g., batch effect removal, marker identification) requires a single aligned feature table.

## When NOT to use

- Input data are already in a pre-aligned feature table (integration has already been performed); apply this skill only to raw, separate experiment outputs
- You have only a single metabolomic experiment or dataset; Integrate_Data() is designed for 2+ datasets and will produce redundant output for single inputs
- Input files are not in CSV format or do not contain the five required columns (mass, RT, intensity, isotope, adduct); pre-process to the required schema first

## Inputs

- Multiple MutileGroup datasets (CSV files formatted as feature-by-sample matrices)
- Each dataset must contain exactly five columns: mass (m/z), retention time (RT), intensity, isotope, adduct annotations
- Sample identifiers in first row, samples in columns (following first two annotation columns)

## Outputs

- AlignData object: unified feature matrix with consolidated feature identifiers across all input datasets
- Aligned retention time column (consolidated RT for each matched feature)
- Aligned mass-to-charge ratio column (consolidated m/z for each matched feature)
- Feature-by-sample intensity matrix combining all input datasets

## How to apply

Load all input CSV files as MutileGroup objects in R (each must contain five essential columns: mass, retention time, intensity, isotope, and adduct, with samples in columns and sample names in the first row). Call the Integrate_Data() function from the LargeMetabo package, specifying RTTolerance1, mzTolerance1, RTTolerance2, and mzTolerance2 parameters. The function performs two-phase alignment: primary phase integration clusters features across datasets using the first tolerance pair, then secondary phase integration refines the alignment using the second tolerance pair (typically with tighter thresholds). The rationale is that two-phase integration reduces false feature merging while capturing genuine cross-dataset matches. The output is a unified AlignData object with consolidated feature identifiers, aligned RT values, and aligned m/z values suitable for batch effect removal or marker identification. Common parameter choices documented in LargeMetabo are RTTolerance1 = 10 (seconds), mzTolerance1 = 0.1 (Da), RTTolerance2 = 10 (seconds), mzTolerance2 = 0.1 (Da), but these should be adjusted based on your LC-MS instrument's mass accuracy and RT reproducibility.

## Related tools

- **LargeMetabo** (R package providing Integrate_Data() function for multi-dataset alignment in m/z-RT space) — https://github.com/LargeMetabo/LargeMetabo
- **R** (Runtime environment (>= 3.5.0) required to execute Integrate_Data() and downstream LargeMetabo functions) — https://www.r-project.org

## Examples

```
AlignData <- Integrate_Data(MutileGroup, RTTolerance1 = 10, mzTolerance1 = 0.1, RTTolerance2 = 10, mzTolerance2 = 0.1)
```

## Evaluation signals

- Output AlignData row count equals or exceeds the maximum row count from any single input dataset (indicating features have been consolidated, not lost)
- Presence of RT, m/z, and intensity columns in the output with no null values in these key fields
- Feature identifiers are unique and consistently formatted across the consolidated matrix
- Sample columns match the union of all sample names from input datasets (no sample drops after integration)
- Spot-check: select 5–10 high-intensity features and verify their RT and m/z values fall within the specified tolerance windows of features from different input datasets

## Limitations

- Tolerance parameters (RTTolerance1, mzTolerance1, RTTolerance2, mzTolerance2) must be tuned for each analytical platform; overly tight tolerances cause true features to remain unmerged, while loose tolerances cause false merging of distinct metabolites
- Two-phase integration may not recover all true matches if RT drift or m/z calibration varies significantly across experiments; pre-processing (e.g., RT normalization or mass calibration) may be necessary before Integrate_Data()
- No built-in handling of systematic bias between datasets (e.g., ionization efficiency differences); batch effect removal (Removal_Batch function) should follow integration
- Feature alignment is strictly geometric (RT and m/z space) and does not use MS/MS fragmentation patterns or metabolite identity; false positive alignments are possible for isomers or isobars with similar RT and m/z

## Evidence

- [readme] For data integration, multiple datasets from different analytical experiments can be used as the input of the LargeMetabo package.: "For data integration, multiple datasets from different analytical experiments can be used as the input of the LargeMetabo package"
- [readme] Each dataset (csv file) contains five essential columns providing the information of mass, retention time, intensity, isotope and adduct.: "Each dataset (csv file) contains five essential columns providing the information of mass, retention time, intensity, isotope and adduct"
- [other] The Integrate_Data() function accepts MutileGroup (multiple datasets) and four tolerance parameters: RTTolerance1 and mzTolerance1 for primary phase integration, and RTTolerance2 and mzTolerance2 for secondary phase integration, producing an aligned feature matrix combining all input datasets.: "The Integrate_Data() function accepts MutileGroup (multiple datasets) and four tolerance parameters: RTTolerance1 and mzTolerance1 for primary phase integration, and RTTolerance2 and mzTolerance2 for"
- [readme] AlignData <- Integrate_Data(MutileGroup, RTTolerance1 = 10, mzTolerance1 = 0.1, RTTolerance2 = 10, mzTolerance2 = 0.1): "AlignData <- Integrate_Data(MutileGroup, RTTolerance1 = 10, mzTolerance1 = 0.1, RTTolerance2 = 10, mzTolerance2 = 0.1)"
- [readme] The first two columns provide the mass and retention time, and samples must be kept in columns with the sample names in the first row.: "The first two columns provide the mass and retention time, and samples must be kept in columns with the sample names in the first row"
