---
name: chromatographic-noise-modeling
description: Use when you need to generate blank or background-only .mzML files for
  method validation, when you want to create synthetic negative controls with realistic
  instrumental noise but no analyte peaks, or when you need to simulate serum matrix
  background (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - base64enc
  - mzrtsim
  techniques:
  - LC-MS
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.5c01213
  title: mzrtsim
evidence_spans:
- if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
  BiocManager::install("mzrtsim")
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chromatographic-noise-modeling

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate realistic background noise and optional matrix peaks in simulated LC/GC-MS .mzML files by applying stochastic noise models and overlaying biochemical background signals. This skill enables creation of ground-truth synthetic data for benchmarking peak detection, noise filtering, and batch correction methods in untargeted metabolomics.

## When to use

Apply this skill when you need to generate blank or background-only .mzML files for method validation, when you want to create synthetic negative controls with realistic instrumental noise but no analyte peaks, or when you need to simulate serum matrix background (e.g., phospholipids) to test robustness of feature detection and quantification pipelines against matrix suppression.

## When NOT to use

- Input already contains simulated analyte peaks — use simmzml() instead to generate full synthetic data with ground-truth peak information and companion CSV
- Goal is to simulate realistic chromatographic peak shapes with tailing and Gaussian/EMG profiles — use simmzml() with configurable peak-width parameters
- Need to link simulated peaks to specific compound identities and retention time/m/z annotations — use simmzml() to generate companion CSV with m/z, retention time, database intensity, sim_ins, and compound name

## Inputs

- rtrange parameter: numeric vector [min_intensity, max_intensity] defining Poisson or Gaussian noise intensity range
- matrixmz parameter: optional mzm dataset containing serum/matrix ion m/z, retention time, and intensity values
- noise_model parameter: distribution type (Poisson or Gaussian)
- output file path: character string specifying output .mzML filename

## Outputs

- .mzML file: base64-encoded binary mass spectrometry data in mzML XML structure with scan headers and product ion arrays
- metadata: noise intensity range, matrix peak list (if used), m/z resolution, retention time range, and scan count

## How to apply

Call simmzml_blank() with rtrange parameter specifying noise intensity range to generate pure noise blanks, or pass the mzm serum matrix dataset to the matrixmz parameter to overlay realistic matrix ion peaks onto noise baseline. First, parse input noise parameters (intensity floor, ceiling, distribution type). Second, synthesize m/z and retention-time arrays covering the full instrument range with appropriate mass resolution. Third, generate background noise using a realistic stochastic model (Poisson or Gaussian distribution) across the m/z–retention-time matrix. Fourth, if matrix peaks are enabled, retrieve the mzm matrix peak list and overlay selected ion peaks at specified intensities onto the noise baseline. Finally, encode the combined spectral data as base64-encoded binary and write the mzML XML structure with appropriate scan headers and product ion arrays. Validate by checking that the output .mzML file parses correctly, that base64-decoded intensities match the noise model parameters, and that matrix peaks (if included) appear at expected m/z values with monotonically-spaced retention time intervals.

## Related tools

- **base64enc** (Encodes spectral matrix (noise + optional matrix peaks) as base64 binary for mzML file storage)
- **mzrtsim** (Parent package wrapping simmzml_blank() function and providing database access (MoNA, HMDB) and matrix peak datasets) — https://github.com/yufree/mzrtsim
- **R** (Language environment for executing noise generation, array synthesis, and mzML XML construction)

## Examples

```
library(mzrtsim); data(mzm); simmzml_blank(name='blank_matrix', rtrange=c(0, 500), matrixmz=mzm, noise_model='Poisson')
```

## Evaluation signals

- Output .mzML file parses correctly as valid XML and contains expected mzML namespace and schema elements (scan, spectrum, binaryDataArray)
- Base64-decoded binary data reconstructs a matrix of intensities with statistics (mean, median, SD) consistent with specified noise model parameters (Poisson or Gaussian with rtrange bounds)
- If matrixmz peaks included: selected matrix ion m/z values appear in product ion arrays at expected intensities; no analyte peaks are present (only noise + matrix)
- Retention time array spans full instrument range (e.g., 0–600 s for typical LC-MS) with monotonically increasing scan times
- Output file size and number of scans are consistent with input m/z range and retention time range (e.g., typical blank: 1–10 MB, 500–5000 scans)

## Limitations

- simmzml_blank() does not model instrument-specific noise characteristics (e.g., detector baseline drift, thermal noise profiles unique to TOF vs. Orbitrap); noise model assumes stationary Poisson or Gaussian distribution
- Matrix peak overlay uses fixed intensity ratios from mzm dataset; does not account for sample-to-sample matrix variability or ionization suppression effects that vary with analyte co-elution
- No support for time-varying noise intensity or retention-time-dependent noise floor; assumes uniform noise across entire m/z–time domain
- simmzml_blank() requires pre-loaded mzm serum matrix dataset; if matrixmz dataset is unavailable or corrupted, function will fail or produce pure-noise output without warning

## Evidence

- [other] simmzml_blank() produces .mzML files with configurable options: pure noise blanks via rtrange parameter, or blanks with serum matrix peaks by passing the mzm matrix dataset to the matrixmz parameter.: "simmzml_blank() produces .mzML files with configurable options: pure noise blanks via rtrange parameter, or blanks with serum matrix peaks by passing the mzm matrix dataset to the matrixmz parameter."
- [other] Generate synthetic m/z and retention-time arrays covering the full instrument range with appropriate resolution. Synthesize background noise using a realistic noise model (e.g., Poisson or Gaussian distribution) across the m/z–retention-time matrix. If matrix peaks are enabled, retrieve or load the mzm matrix dataset and overlay selected matrix ion peaks at specified intensities onto the noise baseline.: "Generate synthetic m/z and retention-time arrays covering the full instrument range with appropriate resolution. Synthesize background noise using a realistic noise model (e.g., Poisson or Gaussian"
- [other] Encode the combined spectral data (noise + optional matrix) as base64-encoded binary using the base64enc package. Construct mzML XML structure with appropriate scan headers, precursor metadata, and product ion arrays, then write to the output .mzML file.: "Encode the combined spectral data (noise + optional matrix) as base64-encoded binary using the base64enc package. Construct mzML XML structure with appropriate scan headers, precursor metadata, and"
- [readme] The native mzML writer handles the binary encoding (Base64) internally without requiring external MS data libraries.: "The native mzML writer handles the binary encoding (Base64) internally without requiring external MS data libraries."
