---
name: retention-time-mass-tolerance-calibration
description: Use when you have multiple feature tables (CSV files) from different
  LC-MS analytical experiments, each containing mass, retention time, intensity, isotope,
  and adduct annotations, and you need to merge them into a single aligned feature
  matrix.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0218
  tools:
  - R (>=)
  - LargeMetabo
  - R
  - meRgeION2
  - MergeION2
  - GNPS
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1093/bib/bbac455
  title: LargeMetabo
- doi: 10.1021/acs.analchem.2c04343
  title: ''
evidence_spans:
- Dependent on R (>= 3.5.0)
- install_github("LargeMetabo/LargeMetabo", force = TRUE, build_vignettes = TRUE)
- github.com__daniellyz__meRgeION2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_largemetabo_cq
    doi: 10.1093/bib/bbac455
    title: LargeMetabo
  - build: coll_mergeion_cq
    doi: 10.1021/acs.analchem.2c04343
    title: MeRgeION
  dedup_kept_from: coll_largemetabo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bib/bbac455
  all_source_dois:
  - 10.1093/bib/bbac455
  - 10.1021/acs.analchem.2c04343
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-mass-tolerance-calibration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Calibrate and apply retention time (RT) and mass-to-charge ratio (m/z) tolerance parameters to align features across multiple metabolomic datasets from different analytical experiments into a unified feature matrix. This skill is essential for integrating heterogeneous LC-MS/MS datasets while preserving feature identity and minimizing false alignments.

## When to use

You have multiple feature tables (CSV files) from different LC-MS analytical experiments, each containing mass, retention time, intensity, isotope, and adduct annotations, and you need to merge them into a single aligned feature matrix. The input datasets must have five essential columns (mass, retention time, intensity, isotope, adduct) with sample names in the first row and feature-level RT and m/z values already annotated.

## When NOT to use

- Input data already consists of a single unified feature table from one analytical experiment (no cross-experiment alignment needed).
- Feature tables lack essential metadata columns (mass, retention time, isotope, adduct information) or have missing RT/m/z annotations.
- Retention time or m/z values have not been quality-checked and contain outliers or systematic drift uncorrected by instrument calibration.

## Inputs

- MutileGroup (list of feature-by-sample matrices in CSV format, each with columns: mass, retention time, intensity, isotope, adduct, followed by sample columns)

## Outputs

- AlignData (aligned feature-by-sample matrix with consolidated feature identifiers, aligned retention times, and aligned m/z values)

## How to apply

Invoke the Integrate_Data() function from the LargeMetabo package with your stacked MutileGroup datasets (list of feature tables) and provide four tolerance parameters: RTTolerance1 and mzTolerance1 for primary phase integration, and RTTolerance2 and mzTolerance2 for secondary phase integration. The tolerance values define the matching windows in retention time (in seconds) and m/z (in mass units, typically 0.05–0.1 Da for high-resolution MS). Start with conservative tolerances (e.g., RTTolerance = 10 s, mzTolerance = 0.1) and adjust based on your instrument resolution and expected drift; tighter tolerances reduce false matches but may fragment true features across experiments. The function iteratively groups features across all input datasets by proximity in RT–m/z space and produces a consolidated feature matrix with aligned identifiers, mean RT values, and mean m/z values for each matched feature group.

## Related tools

- **LargeMetabo** (Provides Integrate_Data() function for multi-experiment feature alignment using RT and m/z tolerance parameters) — https://github.com/LargeMetabo/LargeMetabo
- **R** (Execution environment (>= 3.5.0) required to run LargeMetabo package and Integrate_Data() function) — https://www.r-project.org

## Examples

```
AlignData <- Integrate_Data(MutileGroup, RTTolerance1 = 10, mzTolerance1 = 0.1, RTTolerance2 = 10, mzTolerance2 = 0.1); head(AlignData[1:5, 1:5])
```

## Evaluation signals

- Verify aligned data has the expected total row count (sum of unique features across all input datasets, accounting for merged duplicates).
- Confirm presence and continuity of RT and m/z columns in the output AlignData matrix with no null or NaN values in key feature annotation fields.
- Check that aligned RT values fall within the union of RT ranges from input datasets and that aligned m/z values cluster around expected integer and half-integer masses.
- Inspect a random sample of aligned features to confirm that consolidated features have similar RT and m/z values across all constituent datasets (visual inspection of variance).
- Validate that sample intensity columns are present and contain non-negative numeric values with expected dynamic range and sparsity patterns.

## Limitations

- Tolerance parameters (RTTolerance1, mzTolerance1, RTTolerance2, mzTolerance2) are fixed globally and do not adapt to local instrument drift or mass-dependent m/z bias; manual re-tuning may be required if datasets span long acquisition periods or have systematic calibration offsets.
- The two-phase tolerance scheme (primary and secondary) assumes a specific integration strategy; the rationale for using two distinct tolerance pairs is not explained in the README and may require empirical validation for non-standard workflows.
- No guidance provided on how to choose initial tolerance values; inappropriate choices can lead to either over-merging of distinct features or under-merging of true biological replicates, and sensitivity analysis is left to the user.

## Evidence

- [readme] For data integration, multiple datasets from different analytical experiments can be used as the input of the LargeMetabo package. Before data integration, the csv files containing a feature-by-sample matrix should be prepared in advance. Each dataset (csv file) contains five essential columns providing the information of mass, retention time, intensity, isotope and adduct.: "Each dataset (csv file) contains five essential columns providing the information of mass, retention time, intensity, isotope and adduct."
- [other] The Integrate_Data() function accepts MutileGroup (multiple datasets) and four tolerance parameters: RTTolerance1 and mzTolerance1 for primary phase integration, and RTTolerance2 and mzTolerance2 for secondary phase integration, producing an aligned feature matrix combining all input datasets.: "The Integrate_Data() function accepts MutileGroup (multiple datasets) and four tolerance parameters: RTTolerance1 and mzTolerance1 for primary phase integration, and RTTolerance2 and mzTolerance2 for"
- [readme] AlignData <- Integrate_Data(MutileGroup, RTTolerance1 = 10, mzTolerance1 = 0.1, RTTolerance2 = 10, mzTolerance2 = 0.1): "AlignData <- Integrate_Data(MutileGroup, RTTolerance1 = 10, mzTolerance1 = 0.1, RTTolerance2 = 10, mzTolerance2 = 0.1)"
- [other] Verify alignment completeness by checking row count, presence of RT/m/z columns, and absence of null values in key fields.: "Verify alignment completeness by checking row count, presence of RT/m/z columns, and absence of null values in key fields."
