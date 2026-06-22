---
name: fragment-ion-scoring-and-ranking
description: Use when when you have an experimental MS/MS spectrum (centroid mode) and need to convert it into a scored fragment library entry, or when you must rank candidate fragments by confidence before performing spectrum-to-spectrum matching in metabolite annotation workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - MetaboAnnotatoR
  - R (version or higher)
  - R
  - xcms
  - RamClustR
  techniques:
  - LC-MS
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

# Fragment-Ion Scoring and Ranking

## Summary

A method to quantify and rank fragment ions detected in MS/MS spectra by attributing occurrence scores to peaks above noise thresholds, enabling prioritization of reliable fragments for metabolite library entries and spectrum matching. This skill bridges raw spectral data and scored fragment databases used in automated metabolite annotation.

## When to use

When you have an experimental MS/MS spectrum (centroid mode) and need to convert it into a scored fragment library entry, or when you must rank candidate fragments by confidence before performing spectrum-to-spectrum matching in metabolite annotation workflows. Apply this skill when raw peak lists require filtering by signal intensity and noise characteristics to ensure only reliable fragments are retained for downstream matching.

## When NOT to use

- Input is a feature table from xcms/RamClustR clustering — use annotateRC function instead for batch annotation of multiple features.
- Spectrum is in profile mode rather than centroid mode — centroid conversion is required first.
- You need to annotate unknown spectra against existing libraries — use the annotateRC function with pre-built fragment databases (e.g., LipidPos) instead.

## Inputs

- MS/MS spectrum in centroid mode (mz/intensity pairs)
- Metabolite name (string)
- Adduct type (string, e.g., '[M+H]+')
- Accurate adduct m/z (numeric)
- Output filename (string)

## Outputs

- Scored fragment library entry (CSV file with metabolite ID, fragment m/z, and occurrence scores)
- Ranked fragment ions with occurrence scores above threshold

## How to apply

Load the MS/MS spectrum into the genFragEntry function and apply default peak-picking and scoring parameters: set noise threshold (noise=0.005) to filter baseline noise, mpeaksThres=0.1 to define the minimum relative intensity cutoff for peak detection, and mpeaksScore=0.9 to assign occurrence scores to qualifying peaks. Use mzTol=0.01 (0.01 m/z) to handle small mass calibration deviations. The function attributes occurrence scores only to peaks above both the noise level and mpeaksThres threshold, ranking fragments by their reliability. Explicitly specify the metabolite name, adduct type (e.g., [M+H]+), accurate adduct m/z, and output filename. The result is a CSV library entry with metabolite identifier, mass, and scored fragment annotations that can be used for querying unknown spectra.

## Related tools

- **MetaboAnnotatoR** (R package containing genFragEntry function for converting MS/MS spectra to scored fragment library entries and annotateRC function for querying unknown spectra against fragment libraries) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Runtime environment for executing genFragEntry function (version 4.5.0 or higher required))
- **xcms** (Upstream tool for LC-MS feature detection and centroiding before genFragEntry processing)
- **RamClustR** (Complementary tool for clustering related features; output can be annotated using genFragEntry-prepared libraries via annotateRC)

## Examples

```
genFragEntry(spectrum_data, metaboliteName="D-Pantothenic Acid", adductName="[M+H]+", adductMZ=220.1201, outputFile="pantothenic_acid_library.csv", noise=0.005, mpeaksThres=0.1, mpeaksScore=0.9, mzTol=0.01)
```

## Evaluation signals

- Output CSV contains one row per scored fragment with columns for m/z, occurrence score, and metabolite identifier matching input metabolite name
- All peaks in output have intensity relative to base peak ≥ mpeaksThres (0.1) and exceed noise threshold (0.005)
- Occurrence scores are numeric values in expected range (typically 0–1) and decrease monotonically or remain stable with increasing m/z for reasonable fragmentation patterns
- Fragment m/z values fall within mzTol (±0.01 m/z) of theoretical fragment masses for the specified adduct and metabolite
- Output filename matches user-specified parameter and file is readable as CSV with consistent delimiter and column count

## Limitations

- Default parameters (noise=0.005, mpeaksThres=0.1, mpeaksScore=0.9, mzTol=0.01) are optimized for the example D-Pantothenic Acid dataset and may require tuning for different metabolite classes or MS instrument configurations.
- Function requires input spectrum in centroid mode; profile-mode spectra will produce incorrect peak detection and scoring.
- Scoring is based solely on relative peak intensity and does not account for fragment class-specific information (e.g., diagnostic ions for lipids) or retention time.
- Mass calibration errors exceeding mzTol (0.01 m/z) will cause correct fragments to be missed or incorrectly matched; recalibration of raw data is recommended before use.

## Evidence

- [other] Default scoring parameters explanation: "The genFragEntry function converts MS/MS spectra into library entries by attributing occurrence scores to peaks above the mpeaksThres threshold and noise level, using default parameters: noise=0.005,"
- [other] Input specification and workflow: "Retrieve the D-Pantothenic Acid [M+H]+ fragmentation spectrum from MassBank, load the spectrum data into R and invoke the genFragEntry function with default peak-picking parameters, apply default"
- [intro] Tool capability for spectrum conversion: "MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"
- [readme] Centroid mode requirement: "This R package is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases. It requires raw LC-MS AIF chromatograms"
- [readme] Installation and runtime environment: "start R (version "4.5.0" or higher)"
