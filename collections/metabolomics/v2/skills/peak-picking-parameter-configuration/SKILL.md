---
name: peak-picking-parameter-configuration
description: Use when when reconstructing a metabolite fragment library entry from raw MS/MS spectral data (e.g., from MassBank or local acquisition), you need to define peak-picking thresholds to separate true fragment ions from baseline noise and assign occurrence scores.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3375
  tools:
  - MetaboAnnotatoR
  - R (version or higher)
  - R
  - MassBank
  techniques:
  - LC-MS
  - CE-MS
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets
- start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator_cq
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c03032
  all_source_dois:
  - 10.1021/acs.analchem.1c03032
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-picking-parameter-configuration

## Summary

Configure noise thresholds and peak-scoring parameters to convert experimental MS/MS spectra into scored fragment ion entries for metabolite library generation. This skill controls which peaks are retained during library entry creation and how their abundance is ranked relative to noise.

## When to use

When reconstructing a metabolite fragment library entry from raw MS/MS spectral data (e.g., from MassBank or local acquisition), you need to define peak-picking thresholds to separate true fragment ions from baseline noise and assign occurrence scores. Apply this skill before exporting the processed library entry as a structured record (CSV, msp, or database entry).

## When NOT to use

- Input is already a processed feature table from xcms or RamClustR — you need raw spectral data, not pre-clustered features.
- Spectrum data is in profile (continuous) mode rather than centroid mode — genFragEntry expects centroid peaks.
- You are performing feature-level annotation on already-detected features; use annotateRC instead to match features against libraries.

## Inputs

- Centroid-mode MS/MS spectrum (vector of m/z and intensity pairs)
- Metabolite name (string)
- Adduct name (string, e.g. '[M+H]+')
- Accurate adduct m/z (float)
- Output filename (string path)

## Outputs

- Metabolite library entry (CSV file with columns: metabolite_id, fragment_m/z, occurrence_score, peak_intensity)
- Scored fragment ion list (R data frame or table object)

## How to apply

Invoke the genFragEntry function with explicit specification of four peak-picking parameters: (1) noise — baseline noise level (default 0.005), used to filter low-intensity peaks; (2) mpeaksThres — relative intensity threshold for peak inclusion (default 0.1, meaning peaks must exceed 10% of max intensity); (3) mpeaksScore — threshold for attributing occurrence scores to retained peaks (default 0.9, meaning only peaks with normalized intensity ≥ 0.9 are scored); (4) mzTol — mass tolerance for peak matching (default 0.01 m/z units). Supply the metabolite name, adduct name (e.g., '[M+H]+'), accurate adduct m/z value, and centroid-mode spectrum data. The function ranks fragment ions by scored abundance and exports the result as a CSV file annotated with metabolite identifier, fragment masses, and occurrence scores. Parameter selection should reflect the signal-to-noise ratio and dynamic range of your instrument; higher thresholds exclude minor fragments but reduce false positives from chemical noise.

## Related tools

- **MetaboAnnotatoR** (R package providing the genFragEntry function for converting MS/MS spectra into scored library entries) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Language runtime for executing genFragEntry and parameter-setting commands (version 4.5.0 or higher))
- **MassBank** (Public database providing reference MS/MS spectra (e.g., MSBNK-RIKEN-PR100295) to demonstrate parameter tuning)

## Examples

```
genFragEntry(spectrum_data, metabolite_name='D-Pantothenic Acid', adduct_name='[M+H]+', adduct_mz=220.1201, output_file='pantothenic_lib.csv', noise=0.005, mpeaksThres=0.1, mpeaksScore=0.9, mzTol=0.01)
```

## Evaluation signals

- Verify that output CSV contains only peaks with m/z values ≥ noise threshold and normalized intensity ≥ mpeaksThres.
- Check that occurrence scores are assigned only to peaks meeting mpeaksScore threshold (default 0.9), with unscored peaks marked as NA or 0.
- Confirm that the number of retained fragments is consistent with expected fragmentation complexity for the metabolite class (lipids typically show fewer major fragments than amino acids).
- Validate that m/z differences between related fragment ions fall within mzTol tolerance for potential isotope or neutral-loss annotation.
- Cross-check occurrence scores against raw spectrum intensity values to ensure monotonic ranking (highest m/z abundance → highest score).

## Limitations

- Default parameters (noise=0.005, mpeaksThres=0.1, mpeaksScore=0.9, mzTol=0.01) are tuned for typical LC-MS AIF data but may require adjustment for low-abundance metabolites, high-background samples, or instruments with different resolving power.
- Peak-picking is sensitive to baseline calibration; miscalibrated or drifting baseline can inflate noise threshold and exclude true low-intensity fragments.
- The function requires centroid-mode spectra; profile-mode data must be converted first using external tools (e.g., xcms centWave).
- Occurrence scores do not account for biological prior knowledge or fragmentation chemistry; parameter tuning must be validated against known MS/MS spectra from the same instrument and sample matrix.

## Evidence

- [other] Default parameters controlling peak-picking thresholds: "default parameters: noise=0.005, mpeaksScore=0.9, mpeaksThres=0.1, and mzTol=0.01"
- [other] Function converts spectra into library entries via peak occurrence scoring: "The genFragEntry function converts MS/MS spectra into library entries by attributing occurrence scores to peaks above the mpeaksThres threshold and noise level"
- [other] Required metabolite and adduct specification for library entry generation: "with metabolite name, adduct name, accurate adduct m/z, and output filename explicitly specified"
- [readme] Package designed for centroid-mode LC-MS data: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode."
- [readme] Library generation from experimental spectra is a distinct vignette topic: "Generation of Metabolite fragment database entry from MS/MS experimental spectra."
