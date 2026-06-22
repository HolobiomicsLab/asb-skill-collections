---
name: lchrms-chromatographic-peak-boundary-extraction
description: Use when you have a set of target molecules with known molecular formula, main adduct, and experimentally determined retention time boundaries, and you want to extract their chromatographic peaks and isotopologues from LC-HRMS mzML files to generate a ground-truth benchmark for validating.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - mzRAPP
  - enviPat
  - R
  - Skyline
  - MSconvert
derived_from:
- doi: 10.1093/bioinformatics/btab231/6214530
  title: mzRAPP
evidence_spans:
- 'You can now start mzRAPP using: library(mzRAPP); callmzRAPP()'
- The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing (NPP)
- mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues
- library(mzRAPP)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzrapp_cq
    doi: 10.1093/bioinformatics/btab231/6214530
    title: mzRAPP
  dedup_kept_from: coll_mzrapp_cq
schema_version: 0.2.0
---

# lchrms-chromatographic-peak-boundary-extraction

## Summary

Extract and validate chromatographic peak boundaries for known target molecules and their isotopologues from centroided mzML files using user-provided retention time windows and molecular composition. This skill produces a curated benchmark dataset of peaks with isotopic integrity filtering, enabling downstream reliability assessment of non-targeted data pre-processing tools.

## When to use

You have a set of target molecules with known molecular formula, main adduct, and experimentally determined retention time boundaries, and you want to extract their chromatographic peaks and isotopologues from LC-HRMS mzML files to generate a ground-truth benchmark for validating non-targeted preprocessing pipelines (XCMS, MZmine, MS-DIAL, etc.).

## When NOT to use

- Input mzML files are profile-mode (not centroided); mzRAPP requires centroided data; use MSconvert to centroid first.
- Target molecules lack known retention time boundaries or accurate molecular formula; mzRAPP requires precise RT windows and SumForm to generate isotopologue predictions.
- Goal is to discover unknown metabolites de novo; this skill is designed for targeted extraction of known compounds only.

## Inputs

- Centroided mzML files (LC-HRMS data)
- Target file (CSV: molecule, SumForm_c, main_adduct, user.rtmin, user.rtmax, optional adduct_c, StartTime.EIC, EndTime.EIC, FileName)
- Sample-group file (CSV: sample_name, sample_group)
- Instrument resolution specification (enviPat built-in or custom CSV with R and m/z columns)

## Outputs

- Benchmark dataset (CSV: extracted peaks with molecule, adduct, isotopologue, m/z, retention time, intensity, peak quality metrics)
- Validated isotopologue peaks (filtered by peak-shape correlation and isotopologue-ratio bias)
- Summary statistics (number of molecules, features, total peaks, detection rates per file)

## How to apply

Prepare a target file (CSV) with molecule names, molecular composition (SumForm_c, e.g., C10H15N5O10P2), main adduct (e.g., M+H), and retention time boundaries (user.rtmin/user.rtmax in seconds) for each molecule. Provide centroided mzML files and a sample-group CSV mapping file names to group labels. Load mzRAPP and specify instrument resolution (e.g., OrbitrapXL/Velos/VelosPro_R60000@400) and additional adducts to screen (e.g., M+NH4, M+Na, M+K). Configure extraction parameters: lowest isotopologue relative abundance (≥0.05), minimum scans per peak (e.g., 6), mass precision (e.g., 6 ppm), and mass accuracy (e.g., 5 ppm). mzRAPP will extract ion chromatograms for all enviPat-predicted isotopologues, apply user-provided retention boundaries, and filter out isotopologues failing peak-shape correlation (Pearson r < 0.85 vs. most abundant isotopologue) or abundance-ratio bias (>30% deviation from predicted isotopologue ratios). Export the resulting benchmark dataset as CSV.

## Related tools

- **mzRAPP** (Primary tool for extracting and validating chromatographic peak boundaries from mzML files using retention time windows and isotopologue prediction) — https://github.com/YasinEl/mzRAPP
- **enviPat** (Predicts isotopologue patterns and m/z values for molecular formulas to guide EIC extraction and validate peak isotopic ratios)
- **R** (Host environment for mzRAPP execution and scripting)
- **Skyline** (Optional tool for manual curation and export of peak retention time boundaries to feed into mzRAPP target file)
- **MSconvert** (Converts vendor mass spectrometry files to mzML format and applies centroiding preprocessing)

## Examples

```
library(mzRAPP); callmzRAPP() # Then navigate to Generate Benchmark tab, select 30 mzML files, sample-group CSV, and target CSV; set instrument to OrbitrapXL,Velos,VelosPro_R60000@400; select adducts M+NH4, M+Na, M+K; set lowest isotopologue 0.05, min 6 scans/peak, 6 ppm precision, 5 ppm accuracy; execute and export benchmark as CSV.
```

## Evaluation signals

- All specified target molecules are present in the benchmark with at least the main adduct detected; if a target is missing, investigate whether user.rtmin/user.rtmax window is too narrow or main adduct is absent in raw data.
- For each molecule, at least two isotopologues are retained (the most abundant and ≥1 additional); fewer isotopologues indicate failed peak-shape correlation or ratio bias filtering.
- Degenerated isotopologue ratio (IR) metric is low (e.g., 3–20% as observed for XCMS run 3 in the benchmark); high degeneration (>30%) suggests poor isotopic integrity or extraction parameter misconfiguration.
- Peak detection rate (found peaks / expected peaks) is >80%; lower rates indicate parameter settings (e.g., minimum scans per peak, mass accuracy/precision) are too stringent.
- Benchmark contains expected molecule count (e.g., 47 molecules with 157 features and 2870 total peaks for MTBLS267 with 30 files) within ±5% variance across replicate runs, indicating reproducible extraction.

## Limitations

- Requires accurate user-provided retention time boundaries (user.rtmin/user.rtmax); peaks with incorrect or overly tight boundaries will be rejected even if isotopic ratio is valid.
- Peak-shape correlation filter (Pearson r < 0.85) and isotopologue-ratio bias filter (>30% deviation) are fixed thresholds; may be too strict for noisy data or too lenient for high-resolution applications.
- Only isotopologues for which the most abundant peak AND at least one additional isotopologue are detected are considered; singleton peaks are always rejected.
- Requires centroided (not profile-mode) mzML files; vendor formats must be pre-converted using MSconvert.
- Does not perform retention time alignment or drift correction across files; RT windows apply per-file, so significant RT shifts between samples will cause missed peaks.

## Evidence

- [readme] mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues: "mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues of those target molecules directly from mzML files."
- [readme] Only isotopologues for which the theoretically most abundant and at least one additional isotopologue are found are considered for the final benchmark.: "Only isotopologues for which the theoretically most abundant and at least one additional isotopologue are found are considered for the final benchmark."
- [readme] Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 are removed: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed."
- [methods] Processing all 30 mzML files generates a benchmark containing 47 different molecules with 157 different features including all adducts and isotopologues, resulting in 2870 peaks in total.: "If you processed all 30 mzML files, you should have generated a benchmark containing 47 different molecules with 157 different features (including all adducts and isotopologues), resulting in 2870"
- [readme] Centroided mzML files are required; conversion and centroiding can be done by Proteowizards MSconvert: "In order to generate a benchmark you need to provide your <b>centroided</b> mzML files. Conversion of files of different vendors to mzML as well as centroiding can be done by Proteowizards MSconvert."
- [readme] Target file must include molecule, SumForm_c, main_adduct, user.rtmin, and user.rtmax columns: "This csv file should contain information on the target molecules/peaks and include the following columns: <b>molecule:</b> names of target molecules <b>SumForm_c:</b> Molecular composition of the"
- [methods] Configuration parameters include lowest isotopologue abundance, minimum scans per peak, mz precision, and mz accuracy: "Configure extraction parameters: lowest isotopologue 0.05, minimum 6 scans per peak, 6 ppm mass precision, 5 ppm mass accuracy."
