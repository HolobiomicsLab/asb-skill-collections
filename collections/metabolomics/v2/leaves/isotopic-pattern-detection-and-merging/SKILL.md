---
name: isotopic-pattern-detection-and-merging
description: Use when your peak table contains features suspected of being artifacts
  of incorrect isotopic pattern splitting during preprocessing—particularly when you
  observe multiple ions with very similar mass-to-charge ratios and retention times,
  or when visual inspection of m/z vs. retention time plots.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - R
  - mpactr
  - mpact
  - data.table
  - ggplot2 + plotly
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.2c04632
  title: MPACT
evidence_spans:
- To import these data into R, use the mpactr function
- We will be using multiple libraries for data analysis and visualization
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mpactr_cq
    doi: 10.1021/acs.analchem.2c04632
    title: MPACT
  dedup_kept_from: coll_mpactr_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04632
  all_source_dois:
  - 10.1021/acs.analchem.2c04632
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# isotopic-pattern-detection-and-merging

## Summary

Detect and merge ions with similar m/z and retention time that represent incorrectly split isotopic patterns or detector artifacts during tandem MS/MS preprocessing. This skill corrects peak selection errors by consolidating mispicked ions into single, high-quality features.

## When to use

Apply this skill when your peak table contains features suspected of being artifacts of incorrect isotopic pattern splitting during preprocessing—particularly when you observe multiple ions with very similar mass-to-charge ratios and retention times, or when visual inspection of m/z vs. retention time plots shows clustering that suggests isotopic duplicates or detector noise rather than distinct metabolites.

## When NOT to use

- Your peak table is already a curated feature table without known preprocessing artifacts or isotopic duplicates.
- You have already performed manual curation or used orthogonal validation (e.g., MS/MS spectra) to confirm all ions are distinct metabolites.
- Your instrument or preprocessing pipeline uses high-resolution (>100k) MS1 that resolves true isotopic patterns and does not produce split isotopic patterns as a known artifact.

## Inputs

- peak table (CSV or vendor format: Progenesis, GNPS, MS-DIAL MSP, Bruker Metaboscape)
- sample metadata table
- mpactr object (result of import_data())

## Outputs

- filtered mpactr object with mispicked ions merged
- filter_summary report (failed_ions, passed_ions, merge statistics)
- similar-ion groups (from get_similar_ions(), optional)

## How to apply

Load the peak table and metadata into an mpactr object using import_data(). Apply filter_mispicked_ions() with isotope-window (isowin), retention-time window (trwin), and ring-window (ringwin) parameters tuned to your instrument's mass resolution and chromatographic resolution. Set ringwin=0.5, isowin=0.01 (0.01 m/z tolerance), trwin=0.005 (0.005 min tolerance), max_iso_shift=3 (allow up to 3 Da mass difference for isotope series), merge_peaks=TRUE, and merge_method='sum' to consolidate detected mispicked-ion groups into single features by summing their abundances. Extract and review the filtering summary using filter_summary(data, filter='mispicked') to confirm the number of ions flagged as similar, the count merged, and ions retained. Optionally retrieve detailed group membership with get_similar_ions() to validate which ions were merged and with which main ion.

## Related tools

- **mpactr** (R package providing filter_mispicked_ions(), filter_summary(), and get_similar_ions() functions; applies tunable sliding-window detection and merging of ions with similar m/z and retention time) — https://github.com/mums2/mpactr
- **mpact** (Original Python/GUI tool for peak-list preprocessing and mispicked-ion detection; supports Bruker, MS-DIAL, and GNPS formats) — https://github.com/BalunasLab/mpact
- **data.table** (R package for efficient handling and subsetting of large peak tables during filtering)
- **ggplot2 + plotly** (Visualization of input features by m/z and retention time and their filter fate (pass/fail); aids validation of detected mispicked-ion clusters)

## Examples

```
filter_mispicked_ions(data, ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, merge_method='sum', copy_object=FALSE); filter_summary(data, filter='mispicked')
```

## Evaluation signals

- Verify that filter_summary() reports a non-zero count of 'ions flagged as similar' and 'ions merged'; zero counts suggest parameters were too stringent or data contains no artifacts.
- Inspect get_similar_ions() output to confirm that merged ions have m/z differences ≤ isowin (0.01) and retention-time differences ≤ trwin (0.005 min), matching theoretical isotope spacing.
- Cross-check the 'ions remaining post-filtering' count against the starting peak count; dramatic loss (>30%) may indicate over-aggressive window settings; modest loss (5–15%) is typical for real artifact removal.
- Visualize filtered features using m/z vs. retention time scatter plots (ggplot + plotly) to confirm that clustered islands of points are resolved into single merged features without removal of legitimately distinct metabolites.
- Compare feature abundance profiles (fold-change, correlation within replicates) before and after filtering; replicate correlation should improve or remain stable if merging is correct.

## Limitations

- Parameter sensitivity: ringwin, isowin, and trwin are tuned to the article's tandem MS/MS instrument; different mass spectrometers (e.g., lower-resolution, different ionization, different chromatography) may require empirical re-tuning of windows.
- No validation against reference databases or MS/MS spectra: merging is based purely on m/z and retention time proximity; co-eluting isomers or isobars may be incorrectly merged if they fall within detection windows.
- Merge-method choice (sum vs. max vs. mean) affects downstream quantification; 'sum' assumes additive isotope intensities, which may not hold if one isotope is saturated or if peaks are partially resolved.
- The skill assumes preprocessed peak tables already contain the mispicked-ion artifact; if preprocessing was already optimized (e.g., high-resolution MS1 or vendor software with isotope-aware picking), the filter may have minimal effect.

## Evidence

- [methods] detection-rationale: "filter_mispicked_ions with parameters ringwin=0.5, isowin=0.01, trwin=0.005, max_iso_shift=3, merge_peaks=TRUE, merge_method='sum' to detect ions with similar retention time and mass-to-charge that"
- [abstract] output-structure: "filter_summary() function with filter='mispicked' returns an object containing two components: failed_ions (ions that did not pass the mispicked filter) and passed_ions (ions that passed the"
- [abstract] optional-validation: "Optionally retrieve detailed similar-ion groups with get_similar_ions() to identify which ions were merged with their corresponding main ions"
- [readme] filter-purpose: "filter_mispicked_ions(): removal of mispicked peaks, or those isotopic patterns that are incorrectly split during preprocessing"
- [methods] workflow-integration: "Extract the mispicked ion filtering summary using filter_summary(data, filter='mispicked') to report the number of ions flagged as similar, the number of ions merged, and the count of ions remaining"
