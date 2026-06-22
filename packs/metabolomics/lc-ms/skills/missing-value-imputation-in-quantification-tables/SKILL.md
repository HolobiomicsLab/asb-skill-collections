---
name: missing-value-imputation-in-quantification-tables
description: Use when after feature alignment across multiple LC-MS/MS runs, when the unified feature list contains zeros or nulls for specific feature–sample pairs because peaks were not detected in those individual runs, but the feature was detected in other samples in the cohort.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3557
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - MZmine2
  - Optimus
  - OpenMS
  techniques:
  - LC-MS
  - direct-infusion-MS
  - tandem-MS
derived_from:
- doi: 10.1021/acs.jnatprod.7b00737
  title: Bioactivity-Based Molecular Networking
evidence_spans:
- open bioinformatic tools, such [MZmine2](http://mzmine.github.io/)
- '[Optimus](https://github.com/MolecularCartography/Optimus) (using OpenMS)'
- or [Optimus](https://github.com/MolecularCartography/Optimus) (using OpenMS)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_bioactivity_based_molecular_networking_cq
    doi: 10.1021/acs.jnatprod.7b00737
    title: Bioactivity-Based Molecular Networking
  dedup_kept_from: coll_bioactivity_based_molecular_networking_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jnatprod.7b00737
  all_source_dois:
  - 10.1021/acs.jnatprod.7b00737
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# missing-value-imputation-in-quantification-tables

## Summary

Fill missing feature intensity values across LC-MS samples where peaks were not detected during feature detection and alignment, ensuring a complete quantification matrix for downstream bioactive molecular network analysis. This step recovers signal information that would otherwise be lost due to stochastic detection failures or alignment gaps.

## When to use

After feature alignment across multiple LC-MS/MS runs, when the unified feature list contains zeros or nulls for specific feature–sample pairs because peaks were not detected in those individual runs, but the feature was detected in other samples in the cohort. Apply this before statistical normalization or molecular networking.

## When NOT to use

- Input is already a complete feature table with no missing values.
- Analysis requires retention of missingness patterns for explicit modeling (e.g., missing-not-at-random analyses).
- Raw LC-MS data are not available to recover signal in missing feature–sample pairs.

## Inputs

- Aligned feature list with m/z, retention time, and per-sample intensity columns
- Raw LC-MS data files (mzML, mzXML, or vendor formats)
- Feature detection and alignment results from MZmine2 or Optimus

## Outputs

- Complete quantification matrix (features_quantification_matrix.csv) with no missing intensity values
- Per-sample abundance table ready for statistical analysis or normalization

## How to apply

After aligning features detected across all runs to construct a unified feature list, identify feature–sample combinations with missing intensity values (zeros or nulls indicating no peak detection in that run). Use the feature detection and alignment algorithms in MZmine2 or Optimus (built on OpenMS) to re-examine the raw LC-MS data around the predicted m/z and retention time boundaries for each missing feature. Fill in recovered intensity values or impute using matrix completion methods (e.g., zero-filling for true absences, or interpolation if supported by the tool). Export the completed feature table with m/z, retention time, and per-sample abundance columns, ensuring no missing values remain before downstream filtering or normalization.

## Related tools

- **MZmine2** (Performs mass detection, feature grouping across retention time and m/z, alignment across samples, and missing value filling for LC-MS quantification.) — http://mzmine.github.io/
- **Optimus** (KNIME-based workflow for LC-MS feature detection, alignment, and quantification using OpenMS algorithms; supports optional missing-value imputation and filtering before export.) — https://github.com/MolecularCartography/Optimus
- **OpenMS** (Underlying C++ library providing state-of-the-art LC-MS feature detection and alignment algorithms used by Optimus.)

## Evaluation signals

- Feature table contains no zeros or nulls in the abundance matrix; every feature–sample pair has a numeric intensity value.
- Filled intensity values are consistent with the m/z and retention time tolerance windows used during alignment (typically ≤5 ppm mass accuracy, ≤0.2–0.5 min RT tolerance).
- Comparison of before/after imputation statistics (e.g., median feature abundance, number of features per sample) shows reasonable recovery without artificial inflation.
- Downstream heatmap visualization or PCA plot shows expected sample clustering and feature distribution patterns, without artifacts from imputation.
- Exported quantification matrix schema matches expected columns: feature ID, m/z, retention time, followed by per-sample abundance columns.

## Limitations

- If raw LC-MS data are not available or have been discarded, true missing values cannot be recovered; only zero-filling is possible.
- Imputation accuracy depends on feature detection sensitivity and m/z/RT tolerance settings; peaks below the detection threshold will still be missed.
- Over-imputation (assigning spurious values to true absences) can inflate feature counts and introduce false positives in downstream molecular networking.
- Direct-infusion data may not benefit from retention time–based recovery strategies.
- The workflow does not perform MS/MS validation of imputed features; putative annotations remain at Metabolomics Standards Initiative level 2 (putatively annotated compounds).

## Evidence

- [other] Fill missing feature values across samples where peaks were not detected.: "Fill missing feature values across samples where peaks were not detected."
- [other] Build chromatogram features by grouping detected peaks across retention time and m/z dimensions. Align features across samples to construct a unified feature list.: "Build chromatogram features by grouping detected peaks across retention time and m/z dimensions. 4. Align features across samples to construct a unified feature list."
- [readme] Optimus employes the state-of-the-art LC-MS feature detection and quantification algorithms by OpenMS which are joined into a handy pipeline: "Optimus employes the state-of-the-art LC-MS feature detection and quantification algorithms by OpenMS which are joined into a handy pipeline"
- [other] Export the processed feature table with m/z, retention time, and per-sample abundance columns to a quantification file.: "Export the processed feature table with m/z, retention time, and per-sample abundance columns to a quantification file."
- [readme] a feature quantification table (features_quantification_matrix.csv) that contains the aligned list of features and their intensity accross the fractions analyzed by LC-MS/MS: "a feature quantification table (features_quantification_matrix.csv) that contains the aligned list of features and their intensity accross the fractions analyzed by LC-MS/MS"
