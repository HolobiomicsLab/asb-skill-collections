---
name: mzml-file-format-generation
description: Use when when you need to generate reproducible synthetic LC/GC-MS raw data files with known ground-truth peak properties (m/z, retention time, intensity) for benchmarking peak detection, feature extraction, normalization, or batch correction algorithms;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - R
  - base64enc
  - mzrtsim
  - BiocManager
  - SummarizedExperiment
  - enviGCMS
  techniques:
  - LC-MS
  - GC-MS
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

# mzml-file-format-generation

## Summary

Generate synthetic LC/GC-MS raw data in mzML format with realistic chromatographic peak shapes, noise, and optional matrix background from spectral databases (MoNA, HMDB). Used to create ground-truth benchmarking datasets for metabolomics method validation.

## When to use

When you need to generate reproducible synthetic LC/GC-MS raw data files with known ground-truth peak properties (m/z, retention time, intensity) for benchmarking peak detection, feature extraction, normalization, or batch correction algorithms; or when you require blank mzML files containing only background noise and optional matrix peaks for negative controls.

## When NOT to use

- Input is already a feature table or processed quantification matrix — use mzml-file-format-generation only to generate raw mzML files, not to convert or manipulate existing peak lists.
- You need to extract or convert existing experimental mzML files — this skill generates synthetic data from spectral databases, not read/parse real instrument output.
- Your goal is to filter, normalize, or batch-correct already-generated mzML or feature data — use this skill only to create the raw synthetic files beforehand.

## Inputs

- Spectral database (RDS format): monams1, monahrms1, hmdbcms, or custom MSP-derived database
- Output filename (string)
- Simulation parameters: n (number of compounds), ms_level (1 or 2), precursor_mz (float, for MS2), collision_energy (int, for MS2), rtrange (retention time bounds, for blanks), matrixmz (matrix dataset, optional)

## Outputs

- mzML file (.mzML): binary-encoded LC/GC-MS raw data in mzML XML format
- Ground-truth CSV file (.csv): columns m/z, retention time, compound name, sim_ins (simulated absolute maximum intensity)

## How to apply

Load a spectral database (monams1 for MoNA LC-MS, monahrms1 for MoNA high-resolution, or hmdbcms for HMDB GC-MS EI spectra). Call simmzml() with parameters specifying the database, output filename, number of compounds to simulate (n), and optionally MS level (1 or 2), precursor m/z, and collision energy. The function generates synthetic m/z and retention-time arrays across the instrument range, overlays realistic chromatographic peak shapes from database spectra, adds background noise using a Poisson or Gaussian distribution model, and encodes the combined spectral matrix as base64-encoded binary via the base64enc package. The output is an mzML XML file with proper scan headers and a companion CSV containing ground-truth m/z, retention time, compound name, and sim_ins (absolute maximum intensity accounting for response factor and peak profile). For blank files with no analyte peaks, use simmzml_blank() with rtrange parameter or pass the mzm matrix dataset to matrixmz parameter to include serum matrix peaks.

## Related tools

- **mzrtsim** (R package providing simmzml() and simmzml_blank() functions for raw data simulation and mzML generation) — https://github.com/yufree/mzrtsim
- **base64enc** (Encodes binary spectral arrays as base64 strings for mzML XML embedding)
- **BiocManager** (Installation and dependency management for mzrtsim and Bioconductor packages)
- **SummarizedExperiment** (Optional wrapper for simulation output to produce Bioconductor-compatible SummarizedExperiment objects)
- **enviGCMS** (Utility for parsing MSP spectral database files and filtering to extract monams1, monahrms1 subsets)

## Examples

```
library(mzrtsim); data('monams1'); simmzml(db=monams1, name='test_synthetic', n=10)
```

## Evaluation signals

- Output mzML file is valid XML with proper scan headers, precursor metadata, and base64-encoded binary arrays readable by standard mzML parsers
- Companion CSV contains all simulated peaks with non-zero sim_ins values matching or correlated to database intensities and peak profiles
- Peak m/z values fall within expected instrument mass range and match database m/z ± 5 ppm tolerance
- Retention time values span the specified rtrange or instrument acquisition window without gaps or out-of-order scans
- Simulated chromatographic peak shapes exhibit realistic tailing and Gaussian profiles consistent with LC/GC peak theory

## Limitations

- Synthetic data does not capture all complexities of real MS1 spectra, which may contain unexpected fragment ions and redundant peaks not predicted from compound formula alone
- Noise model (Poisson or Gaussian) is simplified and may not fully represent instrument-specific noise characteristics such as electronic noise floor or detector saturation effects
- Database-driven simulation is limited to compounds present in MoNA or HMDB; custom compounds require manual MSP entry or external spectral data
- MS2 simulation requires precursor m/z specification; no automatic precursor selection or m/z fragmentation prediction implemented
- simmzml_blank() matrix peak overlay is restricted to serum matrix; other matrix types (tissue, plant, environmental) require custom matrixmz dataset

## Evidence

- [intro] simmzml() generates one .mzML file and a companion .csv file containing ground-truth peak information (m/z, retention time, database intensity, simulated maximum intensity, compound name): "simmzml() generates one .mzML file and a companion .csv file containing ground-truth peak information (m/z, retention time, database intensity, simulated maximum intensity, compound name)."
- [intro] The output CSV now includes a sim_ins column — the absolute ground-truth maximum intensity of each simulated peak, accounting for response factor, peak height, and chromatographic profile: "The output CSV now includes a `sim_ins` column — the absolute ground-truth maximum intensity of each simulated peak, accounting for response factor, peak height, and chromatographic profile."
- [other] Generate synthetic m/z and retention-time arrays covering the full instrument range with appropriate resolution, synthesize background noise using a realistic noise model (Poisson or Gaussian distribution) across the m/z–retention-time matrix, and encode the combined spectral data as base64-encoded binary: "Generate synthetic m/z and retention-time arrays covering the full instrument range with appropriate resolution. 3. Synthesize background noise using a realistic noise model (e.g., Poisson or"
- [intro] The underlying engine handles binary data encoding via the base64enc package, removing the need for mzR or other heavy dependencies for file generation: "The underlying engine handles binary data encoding via the `base64enc` package"
- [readme] You could use simmzml to generate one mzML file by loading a database (monams1 from MoNA or hmdbcms from HMDB) and calling simmzml(db=..., name='test'): "You could use `simmzml` to generate one mzML file. library(mzrtsim) data("monams1") simmzml(db=monams1, name = 'test')"
- [other] simmzml_blank() produces .mzML files with configurable options: pure noise blanks via rtrange parameter, or blanks with serum matrix peaks by passing the mzm matrix dataset to the matrixmz parameter: "simmzml_blank() produces .mzML files with configurable options: pure noise blanks via rtrange parameter, or blanks with serum matrix peaks by passing the mzm matrix dataset to the matrixmz parameter."
- [readme] MS1 full scan data has been proved more complex than theoretical prediction; mzrtsim package will use experimental data instead of predicted peaks from the compound formula to show the complexity of MS1 spectra: "MS1 full scan data has been proved more complex than theoretical prediction. Recently study showed that soft ionization will also contain fragment ions for structure identification and contain lots"
- [intro] mzrtsim generates simulated LC/GC-MS data at two levels: raw data simulation producing .mzML files with realistic chromatographic peak shapes, tailing, noise, and matrix background; peak list simulation producing feature tables: "`mzrtsim` generates simulated LC/GC-MS data at two levels: 1. **Raw data simulation** — produces `.mzML` files from real spectral databases (MoNA, HMDB), with realistic chromatographic peak"
