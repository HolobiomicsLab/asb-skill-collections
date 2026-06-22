---
name: peak-table-harmonization
description: Use when when you have extracted peak tables from multiple independent LC/HRMS analysis batches (each with retention time and m/z values) and need to align peaks across batches to create a unified feature matrix for downstream statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - IDSL.IPA
  - R
  - IDSL.UFA
  - IDSL.CSA
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.jproteome.2c00120
  title: IDSL.IPA
evidence_spans:
- '**Intrinsic Peak Analysis (IPA)** by the [**Integrated Data Science Laboratory for Metabolomics and Exposomics (IDSL.ME)**](https://www.idsl.me) is a light-weight R package'
- light-weight R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_idsl_ipa_cq
    doi: 10.1021/acs.jproteome.2c00120
    title: IDSL.IPA
  dedup_kept_from: coll_idsl_ipa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.2c00120
  all_source_dois:
  - 10.1021/acs.jproteome.2c00120
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-table-harmonization

## Summary

Align and harmonize peak tables across multiple LC/HRMS batches by applying retention time correction to resolve batch-induced shifts in chromatographic retention times while preserving peak identity across samples. This skill ensures that chemically identical compounds with the same m/z and elution profile are assigned consistent retention times across all batches in large-scale population studies.

## When to use

When you have extracted peak tables from multiple independent LC/HRMS analysis batches (each with retention time and m/z values) and need to align peaks across batches to create a unified feature matrix for downstream statistical analysis. Specifically apply this skill if: (1) you observe systematic retention time drift or batch-to-batch variation in peak elution times for the same compounds, (2) your study includes n > 500 samples across multiple instrumental runs or days, or (3) you are generating a single consensus peak alignment table from individually processed peaklists in separate mzXML/mzML/netCDF files.

## When NOT to use

- Input data is already a single batch or all samples were collected in a single instrumental run (no batch effect correction needed).
- Retention time variation is non-systematic or instrument-specific and cannot be modeled with global endogenous reference markers.
- Peak tables have already been aligned by another tool (e.g., xcms or MZmine 2); applying a second harmonization may introduce conflicting coordinate systems.

## Inputs

- Individual batch peaklists with retention time (RT) and mass-to-charge (m/z) values in Rdata or CSV format
- Multiple LC/HRMS data files (mzXML, mzML, or netCDF format) from separate batches or instrumental runs
- IPA parameter spreadsheet specifying input/output directories and retention time correction settings

## Outputs

- Harmonized peak alignment table with corrected retention times and unified m/z-RT coordinates
- Gap-filled peak height matrix aligned across all samples
- Batch-level retention time correction metadata or transformation functions
- Pairwise correlation lists for aligned peaks (to detect recurring adducts and fragment ions)

## How to apply

Load extracted peak lists from each batch into IDSL.IPA with their raw retention time and m/z coordinates. Use endogenous reference markers (stable, consistently detected compounds across all batches) to estimate the retention time correction function for each batch relative to a reference batch or global alignment frame. Apply the retention time correction algorithm to shift all peaks in non-reference batches so that peaks with identical m/z and similar RT elution profiles align to a common retention time coordinate. Generate a corrected peak alignment table where each unique (m/z, corrected-RT) pair is assigned a single consensus row, with peak heights gap-filled across all samples. Evaluate alignment success by checking that isotopologue pairs, adducts, and fragments maintain expected mass differences and co-elution patterns across the harmonized table.

## Related tools

- **IDSL.IPA** (Implements the full suite of retention time correction, peak alignment, and harmonization algorithms; outputs corrected peak alignment tables and gap-filled matrices.) — https://github.com/idslme/IDSL.IPA
- **R** (Execution environment for IDSL.IPA; required to run the IPA_workflow function.)
- **IDSL.UFA** (Integrates with harmonized peak tables for downstream molecular formula annotation.) — https://github.com/idslme/IDSL.UFA
- **IDSL.CSA** (Integrates with harmonized and annotated peak tables to cluster recurring ions and generate composite spectra.) — https://github.com/idslme/IDSL.CSA

## Examples

```
library(IDSL.IPA)
IPA_workflow("path/to/IPA_parameters.xlsx")
```

## Evaluation signals

- Peak alignment success: Verify that isotopologue pairs (12C/13C) and known adducts maintain expected mass differences (e.g., ±1.003 Da for 13C, ±18.01 Da for [M+NH4]+) across all harmonized rows.
- Retention time consistency: Check that peaks assigned the same (m/z, corrected-RT) coordinates in the alignment table have inter-batch CV in corrected RT < 5% (or per-batch SD < 1 scan width).
- Gap-filling validation: Confirm that the gap-filled peak height matrix has no structural NaNs or inconsistent row/column dimensions; compare gap-filled vs. observed peak counts to verify imputation occurred.
- Batch effect removal: Plot corrected RT vs. raw RT by batch; corrected RTs should cluster tightly around the reference coordinate for peaks detected in multiple batches, while raw RTs show systematic drift.
- Annotation fidelity: Verify that pairwise correlation lists for aligned peaks show expected co-elution patterns (e.g., adducts and in-source fragments of the same compound should have Pearson r > 0.7 in peak height correlation).

## Limitations

- Retention time correction relies on identification of stable endogenous reference markers across all batches; if few markers are detected or markers are unstable, correction may be inaccurate or fail.
- Systematic non-linear retention time drift (e.g., gradient time non-uniformity) may not be fully captured by a global correction function, leading to residual misalignment in extreme RT regions.
- Peak harmonization assumes that the same compound has identical m/z and similar RT across batches; compounds with significant post-acquisition mass drift or unexpected RT shifts (e.g., due to column degradation) may not align correctly.
- Large population-scale studies (n > 500) may produce alignment ambiguities if multiple peaks with similar m/z and RT exist; filtering by peak quality metrics (S/N, peak width, symmetry) is recommended upstream.

## Evidence

- [other] retention time correction algorithm across batches to align peaks with similar m/z and RT profiles: "Apply retention time correction algorithm across batches to align peaks with similar m/z and RT profiles."
- [other] IDSL.IPA includes retention time correction as one of its algorithmic components: "IDSL.IPA includes retention time correction as one of its algorithmic components in a suite covering EIC candidate generation, peak detection, peak property evaluation, recursive mass correction, and"
- [readme] Retention time correction using endogenous reference markers for multi-batch large scale studies: "Retention time correction using endogenous reference markers for multi-batch large scale studies"
- [readme] peak alignment tables in the peak_alignment directory: "Peak alignment tables in the "peak_alignment" directory."
- [readme] generates comprehensive and high-quality datasets from untargeted analysis of organic small molecules for population-size studies: "IDSL.IPA generates comprehensive and high-quality datasets from untargeted analysis of organic small molecules for population-size studies."
- [readme] Generating pairwise correlations list for aligned peak height and its gap-filled tables: "Generating pairwise correlations list for aligned peak height and its gap-filled tables to detect potential recurring adducts, in-source products and fragment peaks"
