---
name: abundance-normalization-and-summary-statistics
description: Use when after peaks have been assigned to heteroatom classes (e.g.,
  CHO, CHON, CHOS, CHOP) and you need to compare molecular composition across samples,
  classes, or time series.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - CoreMS
  - pandas
  - matplotlib
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.transient.input.brukerSolarix import ReadBrukerSolarix
- '**CoreMS** is a comprehensive mass spectrometry framework for software development
  and data analysis of small molecules analysis.'
- import pandas as pd
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems_cq
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5281/zenodo.14009575
  all_source_dois:
  - 10.5281/zenodo.14009575
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Abundance Normalization and Summary Statistics

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Computes and aggregates peak abundance metrics (total, percent, and relative abundance) across heteroatom classes or other mass spectrum groupings to enable normalized, class-level comparison and visualization of molecular composition. This skill transforms individual peak abundances into interpretable summary tables suitable for downstream analysis and publication.

## When to use

Apply this skill after peaks have been assigned to heteroatom classes (e.g., CHO, CHON, CHOS, CHOP) and you need to compare molecular composition across samples, classes, or time series. Use it when individual peak-level data is too granular for interpretation and you require normalized aggregate metrics to report class abundance distributions or validate that all peaks are classified without loss.

## When NOT to use

- Input mass spectrum contains peaks with missing or ambiguous formula assignments — abundance aggregation requires definitive heteroatom class membership.
- Goal is to retain peak-level (m/z, intensity, mass error) detail — this skill discards individual peak identities in favor of class aggregates.
- Abundance values have not been properly extracted or normalized by the instrument calibration and noise filtering pipeline.

## Inputs

- formula-assigned mass spectrum object (CoreMS MassSpectrum with assigned molecular formulas)
- heteroatom class assignments (CHO, CHON, CHOS, CHOP, etc., per peak)
- peak abundance values (height or integrated area from mass spectrometry)

## Outputs

- pandas DataFrame with columns: heteroatom_class, peak_count, total_abundance, percent_abundance
- summary table suitable for tabular export (CSV, Excel) or visualization

## How to apply

Load a formula-assigned mass spectrum object from CoreMS containing peaks with both assigned molecular formulas and heteroatom class labels. Instantiate the HeteroatomsClassification factory with the mass spectrum object. Extract the abundance value (peak height or integrated area) for each detected peak. Group peaks by heteroatom class and compute: (1) peak count per class, (2) total abundance (sum of all peak abundances in that class), and (3) percent abundance (class total / spectrum-wide total × 100). Aggregate results into a pandas DataFrame with columns: heteroatom_class, peak_count, total_abundance, percent_abundance. Validate that the sum of percent_abundance across all classes equals 100% and that no peaks remain unclassified, confirming lossless partitioning.

## Related tools

- **CoreMS** (Provides MassSpectrum and HeteroatomsClassification factory; loads formula-assigned spectra and defines heteroatom class structure) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Creates and manipulates the summary DataFrame; computes aggregation, grouping, and percent calculations)
- **matplotlib** (Optional: renders summary statistics as bar charts or stacked abundance plots by heteroatom class)

## Examples

```
from corems.mass_spectrum.calc import MassSpecCalc; from corems.mass_spectrum.factory import MassSpectrumFactory; ms = MassSpectrumFactory.from_file('ESI_NEG_SRFA.d'); hetero_class = ms.get_heteroatom_class_summary(); summary_df = hetero_class.to_dataframe(); summary_df.to_csv('heteroatom_abundance_summary.csv')
```

## Evaluation signals

- Sum of percent_abundance across all heteroatom classes equals 100.0 (within floating-point tolerance, e.g., ±0.01%)
- peak_count column contains no negative or zero values; total_abundance values are non-negative
- All detected peaks in the input mass spectrum are assigned to exactly one heteroatom class; no unclassified peaks remain
- DataFrame rows match the number of distinct heteroatom classes present in the input spectrum
- total_abundance values are monotonically consistent: sum(total_abundance) equals the spectrum-wide sum of all peak abundances

## Limitations

- Skill assumes input peaks are already assigned to heteroatom classes; unassigned or ambiguously assigned peaks will be excluded or cause aggregation errors.
- Abundance normalization is sensitive to noise threshold and peak-picking parameters; different preprocessing can yield different class totals even for the same raw transient.
- For very low-abundance classes (< 1% relative abundance), floating-point rounding may introduce small artifacts in percent_abundance sums.
- The skill does not retain peak-level metadata (m/z, mass error, resolving power) — summary output is suitable for publication but unsuitable for downstream peak validation.

## Evidence

- [other] HeteroatomsClassification factory transforms a formula-assigned mass spectrum into a heteroatom class summary: "HeteroatomsClassification accepts a formula-assigned mass spectrum object and a molecular formula selection parameter, then organizes the assigned peaks into heteroatom classes (such as CHO, CHON)"
- [other] Workflow step: aggregate peak counts and total abundance by heteroatom class: "Aggregate peak counts and total abundance by heteroatom class."
- [other] Workflow step: generate summary table with heteroatom_class, peak_count, total_abundance, percent_abundance columns: "Generate a summary table (pandas DataFrame) with columns: heteroatom_class, peak_count, total_abundance, percent_abundance."
- [other] Validation: confirm all detected peaks are classified into exactly one heteroatom class with no unassigned peaks: "Validation: confirm all detected peaks are classified into exactly one heteroatom class with no unassigned peaks."
- [readme] CoreMS provides high-level basis for working with mass spectrometry data and hierarchical structure for organized access: "The goal of the framework is to provide a fundamental, high-level basis for working with all mass spectrometry data types, allowing custom workflows for data signal processing, annotation, and"
- [readme] Core features include heteroatoms classification and visualization: "Heteroatoms classification and visualization"
