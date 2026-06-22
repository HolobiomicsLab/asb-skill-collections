---
name: spectral-peak-shape-modeling
description: Use when when generating synthetic LC/GC-MS .mzML files from MoNA or HMDB spectral records where you need to compute absolute ground-truth maximum intensity (sim_ins) for each peak while accounting for chromatographic band broadening, peak tailing, and retention-time dispersion.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - base64enc
  - mzrtsim
  - BiocManager
  - SummarizedExperiment
  techniques:
  - LC-MS
  - GC-MS
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01213
  title: mzrtsim
evidence_spans:
- if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager") BiocManager::install("mzrtsim")
- The underlying engine handles binary data encoding via the `base64enc` package
- github.com__yufree__mzrtsim
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzrtsim_cq
    doi: 10.1021/acs.analchem.5c01213
    title: mzrtsim
  dedup_kept_from: coll_mzrtsim_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01213
  all_source_dois:
  - 10.1021/acs.analchem.5c01213
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-peak-shape-modeling

## Summary

Apply chromatographic peak-shape modeling (Gaussian or exponentially-modified Gaussian) to simulated LC/GC-MS data to generate realistic retention-time profiles with configurable tailing and peak-width parameters. This skill is essential for raw mass spectrometry data simulation when ground-truth peak intensity and chromatographic behavior must be computationally generated from spectral databases.

## When to use

When generating synthetic LC/GC-MS .mzML files from MoNA or HMDB spectral records where you need to compute absolute ground-truth maximum intensity (sim_ins) for each peak while accounting for chromatographic band broadening, peak tailing, and retention-time dispersion. Use this skill if your workflow requires companion CSV files with validated peak parameters for benchmarking feature detection, intensity estimation, or batch correction methods.

## When NOT to use

- Input is already an experimental .mzML file or feature table—peak-shape modeling is for *simulation*, not re-analysis of real data.
- Chromatographic conditions or column metadata are unavailable or unknown—the model requires explicit peak-width and tailing parameters to produce realistic output.
- Your goal is feature detection or quantification on real LC/GC-MS data; use this skill only if you are generating synthetic reference data for validation or benchmarking.

## Inputs

- MoNA or HMDB spectral database records (m/z, retention time, database intensity, compound name)
- Chromatographic column metadata (stationary phase, mobile phase gradient, flow rate, temperature)
- Peak-shape model specification (Gaussian, exponentially-modified Gaussian, or asymmetric)
- Response factor and peak-height scaling parameters

## Outputs

- .mzML file containing simulated raw mass spectrometry data with base64-encoded intensity matrix
- Companion .csv file with columns: m/z, retention_time, database_intensity, sim_ins (absolute ground-truth maximum intensity), compound_name

## How to apply

Load spectral records (m/z, retention time, database intensity, compound name) from MoNA or HMDB via the mzrtsim package. For each compound, select a chromatographic peak-shape model (Gaussian for symmetric peaks, exponentially-modified Gaussian for asymmetric/tailing peaks). Configure peak-width and tailing parameters based on column chemistry and gradient conditions (e.g., UPLC BEH C18 typically has narrow, slightly-tailing peaks). Compute sim_ins ground-truth maximum intensity by multiplying database intensity by a response factor, scaling by the peak height at the retention-time apex under the chosen chromatographic profile, and accounting for the integrated area under the peak-shape curve. Encode the resulting intensity matrix in base64 format and write to .mzML file structure. Output a companion CSV with columns: m/z, retention_time, database_intensity, sim_ins, compound_name. Validate that sim_ins values are physically plausible (non-negative, scaled relative to input intensities) and that retention times fall within the expected chromatographic window.

## Related tools

- **mzrtsim** (R package providing simmzml() function to orchestrate raw data simulation with chromatographic peak-shape modeling and base64 encoding for .mzML output) — https://github.com/yufree/mzrtsim
- **base64enc** (R package for encoding the simulated mass spectrometry intensity matrix in base64 format for .mzML file structure)
- **BiocManager** (R package manager for installing mzrtsim and related Bioconductor dependencies)
- **SummarizedExperiment** (Bioconductor class for wrapping simulated peak-shape output in a standardized S4 object (via mzrtsim_se() wrapper))

## Examples

```
library(mzrtsim); data('monahrms1'); simmzml(db=monahrms1, name='sim_test')
```

## Evaluation signals

- Companion .csv file contains non-empty, non-negative sim_ins values that are scaled consistently relative to input database_intensity values.
- .mzML file decodes without error; base64-encoded intensity matrix reconstructs to a 2D array (m/z × retention time) with no missing or corrupt entries.
- Retention-time column in CSV matches the configured peak apex times; peak widths at half-maximum (FWHM) match model parameters (e.g., Gaussian FWHM ≈ 2.355 × σ).
- sim_ins accounts for response factor and peak-height scaling: verify sim_ins ≈ response_factor × database_intensity × peak_height_at_apex.
- Output .mzML and .csv are paired files with identical compound counts and m/z-retention-time records in the same order.

## Limitations

- Peak-shape modeling assumes a single, unimodal chromatographic peak per compound; overlapping co-eluting peaks or multipeak compounds are not explicitly modeled.
- Gaussian and exponentially-modified Gaussian models are empirical fits and may not capture complex tailing, fronting, or multimodal behavior observed in real LC/GC systems.
- Response factor and peak-height parameters must be supplied by the user; if values are unavailable or misspecified, sim_ins will not reflect realistic instrument response.
- Noise and matrix background are added post-hoc after peak-shape computation; the model does not account for signal-to-noise ratio (S/N) or dynamic range constraints of real detectors.
- Database spectral records (MoNA, HMDB) may have incomplete or uncertain retention-time metadata, leading to inaccurate chromatographic profile placement.

## Evidence

- [intro] simmzml() generates a companion CSV file containing ground-truth peak information (m/z, retention time, database intensity, simulated maximum intensity, compound name), with the sim_ins column representing the absolute ground-truth maximum intensity calculated by accounting for response factor, peak height, and chromatographic profile.: "simmzml() generates one `.mzML` file and a companion `.csv` file containing ground-truth peak information (m/z, retention time, database intensity, simulated maximum intensity, compound name)."
- [intro] Apply chromatographic peak-shape modeling (Gaussian or exponentially-modified Gaussian) with configurable tailing and peak-width parameters to generate realistic retention-time profiles.: "Apply chromatographic peak-shape modeling (Gaussian or exponentially-modified Gaussian) with configurable tailing and peak-width parameters to generate realistic retention-time profiles."
- [intro] The output CSV now includes a `sim_ins` column — the absolute ground-truth maximum intensity of each simulated peak, accounting for response factor, peak height, and chromatographic profile.: "The output CSV now includes a `sim_ins` column — the absolute ground-truth maximum intensity of each simulated peak, accounting for response factor, peak height, and chromatographic profile."
- [readme] MS1 full scan data has been proved more complex than theoretical prediction. Recently study showed that soft ionization will also contain fragment ions for structure identification and contain lots of redundant peaks.: "MS1 full scan data has been proved more complex than theoretical prediction. Recently study showed that soft ionization will also contain fragment ions"
- [readme] The native mzML writer handles the binary encoding (Base64) internally without requiring external MS data libraries.: "The native mzML writer handles the binary encoding (Base64) internally without requiring external MS data libraries."
