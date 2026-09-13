---
name: metabolomic-feature-table-assembly
description: Use when when you have LC-MS data (mzML or netCDF format) and a pre-defined
  list of target metabolites (m/z, retention time, and identifiers) that you wish
  to extract and quantify across multiple samples, rather than performing untargeted
  feature discovery.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3637
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - JPA
  - R
  - XCMS
  - MS-Convert
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3390/metabo12030212
  title: JPA
evidence_spans:
- JPA is a comprehensive and integrated metabolomics data processing software.
- JPA is a comprehensive and integrated metabolomics data processing software
- '''JPA'' is written in R and its source code is publicly available'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_jpa_cq
    doi: 10.3390/metabo12030212
    title: JPA
  dedup_kept_from: coll_jpa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12030212
  all_source_dois:
  - 10.3390/metabo12030212
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolomic-feature-table-assembly

## Summary

Assembly of a metabolomic feature table by matching LC-MS data against a user-supplied target list of m/z values and retention times, with configurable mass and time tolerances. This skill produces a quantitative feature-by-sample matrix suitable for downstream metabolite annotation and statistical analysis.

## When to use

When you have LC-MS data (mzML or netCDF format) and a pre-defined list of target metabolites (m/z, retention time, and identifiers) that you wish to extract and quantify across multiple samples, rather than performing untargeted feature discovery. This is appropriate for hypothesis-driven metabolomics studies with known metabolite targets.

## When NOT to use

- Input is already an aligned feature table from another software — use as-is rather than re-extracting.
- Processing full-scan or DIA (data-independent acquisition) datasets — the MS2 recognition and targeted extraction steps are optimized for DDA (data-dependent acquisition) LC-MS/MS data.
- No prior knowledge of target metabolites exists — untargeted peak picking (MS1 peak picking module) is more appropriate.

## Inputs

- LC-MS raw data files (mzML or netCDF format)
- User-supplied target list (m/z values, retention times, metabolite identifiers)

## Outputs

- Feature table (CSV or tabular format: rows = features, columns = samples with m/z, retention time, intensity values)
- Extracted feature intensity matrix across samples

## How to apply

Load raw LC-MS data files (mzML or netCDF) and a user-supplied target list into JPA. Apply the targeted-list extraction module to match features in the LC-MS data against the target list using specified m/z and retention time tolerances (e.g., 10 ppm for m/z, seconds for retention time windows). For each target, JPA retrieves all matching peaks within the tolerance ranges across all samples. Compile the extracted features into a tabular feature table with rows representing features and columns representing samples, m/z values, retention times, and peak intensities. Export the result as CSV or tabular format for downstream analysis. The rationale is that targeted extraction reduces false positives compared to untargeted peak picking when prior knowledge of target metabolites exists.

## Related tools

- **JPA** (R package that implements targeted-list extraction module to match LC-MS features against user-supplied target list and assemble feature table) — https://github.com/HuanLab/JPA.git
- **R** (Programming language in which JPA is written and executed)
- **XCMS** (Underlying peak detection and feature extraction algorithm embedded in JPA) — https://rdrr.io/bioc/xcms/man/
- **MS-Convert** (Vendor-agnostic format converter; JPA accepts raw data in any vendor format compatible with MS-Convert)

## Examples

```
# Prepare target list and load LC-MS data, then apply targeted extraction
featureTable_targeted <- JPA::targeted.featureTable(dir = "path/to/mzML/files", target_list = target_df, mz.tol = 10, ppm = 10, rt.tol = 30)
write.csv(featureTable_targeted, "targeted_feature_table.csv", row.names = FALSE)
```

## Evaluation signals

- Feature table is non-empty and contains all expected samples as columns with matching m/z and retention time values present.
- All features in the output table fall within the specified m/z tolerance (e.g., ±10 ppm) and retention time tolerance (specified in seconds) of the target list.
- Peak intensities are numeric, positive, and non-zero for detected features; missing values are appropriately marked (NA or 0) for features not detected in a given sample.
- Number of rows (features) in the output table matches or is a multiple of the number of targets, accounting for multiple charge states or adducts per metabolite if targets were defined per adduct.
- Output CSV parses cleanly with expected column headers (m/z, retention time, sample identifiers, intensity values) and no malformed data types.

## Limitations

- Requires pre-defined target list — no de novo discovery of unanticipated metabolites.
- Performance depends on m/z and retention time tolerance settings; overly tight tolerances may miss true features due to instrument calibration drift, while loose tolerances may cause false matches.
- Not recommended for full-scan or DIA data; optimized for DDA LC-MS/MS where MS2 spectra are collected for targeted ions.
- Retention time alignment is critical; if samples have significant retention time shifts, the fixed retention time tolerance may cause systematic mismatches across the cohort. Sample alignment (JPA Part 5) should be considered before or after targeted extraction for multi-sample studies.
- The module assumes target m/z and retention time values are accurate for the analytical method used; mismatch between target list method parameters and actual data collection parameters (e.g., different LC column, ionization mode) will reduce feature recovery.

## Evidence

- [other] Apply the JPA targeted-list extraction module to match features in the LC-MS data against the target list, retrieving features within specified m/z and retention time tolerances.: "Apply the JPA targeted-list extraction module to match features in the LC-MS data against the target list, retrieving features within specified m/z and retention time tolerances."
- [other] Compile extracted features into a feature table (rows = features, columns = samples/measurements and m/z, retention time, intensity values). Export the feature table as a CSV or tabular format.: "Compile extracted features into a feature table (rows = features, columns = samples/measurements and m/z, retention time, intensity values). Export the feature table as a CSV or tabular format."
- [other] JPA is a comprehensive metabolomics data processing software written in R that performs feature extraction, sample alignment, adduct and metabolite annotations, with Part 4 documenting the targeted-list extraction workflow as one of its integrated processing modules.: "JPA is a comprehensive metabolomics data processing software written in R that performs feature extraction, sample alignment, adduct and metabolite annotations, with Part 4 documenting the"
- [other] Load the demo LC-MS data (mzML or netCDF format) into the JPA R package. Prepare a user-supplied target list containing target m/z values, retention times, and other identifiers.: "Load the demo LC-MS data (mzML or netCDF format) into the JPA R package. Prepare a user-supplied target list containing target m/z values, retention times, and other identifiers."
- [readme] Please do not use this function when processing full-scan or DIA data set!: "Please do not use this function when processing full-scan or DIA data set!"
- [readme] JPA accepts raw data in any vendor format that is compatible with MS-Convert.: "JPA accepts raw data in any vendor format that is compatible with MS-Convert."
