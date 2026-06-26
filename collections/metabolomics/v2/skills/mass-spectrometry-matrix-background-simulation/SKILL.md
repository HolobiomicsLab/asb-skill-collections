---
name: mass-spectrometry-matrix-background-simulation
description: Use when when you need to create negative control or background-only
  reference datasets for LC/GC-MS analysis pipelines—specifically to validate peak-picking
  algorithms, assess false-positive rates, or simulate instrument background and matrix
  effects (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - base64enc
  - mzrtsim
  - mzR
  techniques:
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

# mass-spectrometry-matrix-background-simulation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Generate realistic background-only .mzML files for LC/GC-MS data, containing either pure noise or noise combined with matrix ion peaks, without analyte signals. This skill produces ground-truth reference files for benchmarking feature detection and noise modeling in untargeted metabolomics workflows.

## When to use

When you need to create negative control or background-only reference datasets for LC/GC-MS analysis pipelines—specifically to validate peak-picking algorithms, assess false-positive rates, or simulate instrument background and matrix effects (e.g., serum, plasma) independently of compound signals. Use this when your input is a noise intensity specification (retention-time range, intensity distribution) and optionally a matrix peak dataset (e.g., mzm from MoNA/HMDB), and your output requirement is a .mzML file with no simulated analyte peaks.

## When NOT to use

- Input already contains real MS data or ground-truth analyte peak lists — use direct file I/O instead.
- Goal is to simulate complete LC/GC-MS runs with analyte peaks and realistic chromatographic shapes — use `simmzml()` (full simulation) instead.
- Requirement is to generate feature tables with batch/condition effects — use `mzrtsim()` (peak list simulation) instead.
- Matrix composition is unknown or needs to be learned from data — use empirical background estimation tools instead.

## Inputs

- .mzML-compliant instrument parameters (m/z range, resolution, scan type)
- Noise intensity range specification (rtrange parameter or min/max intensity bounds)
- Optional matrix ion peak dataset (mzm matrix peaks from MoNA or HMDB)
- Output file path and name prefix

## Outputs

- .mzML file (XML-formatted, base64-encoded binary spectral data, background + optional matrix only)
- Optional .csv metadata file (if matrix peaks enabled: m/z, retention time, matrix peak name, intensity)

## How to apply

Call `simmzml_blank()` with parameters specifying the noise model (rtrange for retention-time coverage, noise intensity distribution), and optionally pass the matrixmz parameter to overlay matrix ion peaks (e.g., from the mzm serum matrix dataset). The function synthesizes m/z and retention-time arrays covering the full instrument m/z–RT range, generates synthetic background noise using a realistic distribution (Poisson or Gaussian), retrieves and overlays matrix peaks if enabled, base64-encodes the combined spectral data, and writes the mzML XML structure with appropriate scan headers and product ion arrays. Validate output by confirming: (1) .mzML file structure is valid XML with base64-encoded binary arrays, (2) CSV companion file is absent or contains only matrix peak metadata (no analyte entries), (3) simulated intensity ranges match input noise specification, and (4) when matrix peaks are enabled, peaks appear only at database m/z values and specified intensities.

## Related tools

- **mzrtsim** (Main R package providing simmzml_blank() function for background-only .mzML file generation) — https://github.com/yufree/mzrtsim
- **base64enc** (Encodes synthetic spectral binary data as base64 for inclusion in mzML XML structure)
- **R** (Execution environment and host language for simmzml_blank() workflow)
- **mzR** (Not required for this skill (mzrtsim handles binary encoding internally without mzR dependency))

## Examples

```
library(mzrtsim); data(monams1); simmzml_blank(rtrange=c(0, 3600), noise_intensity=c(100, 500), name='background_only')
```

## Evaluation signals

- Output .mzML file is valid XML with properly formatted scan headers, precursor metadata, and product ion arrays.
- Base64-encoded binary spectral data decodes to m/z and intensity arrays spanning the instrument's full m/z range with appropriate resolution.
- When pure noise mode (rtrange only): intensity distribution matches specified noise model (Poisson/Gaussian), no peaks cluster at database m/z values.
- When matrix peaks enabled: peaks appear only at m/z values from the input matrix dataset with intensities matching or proportional to database values; no analyte peaks present.
- CSV companion file (if generated) contains only matrix peak metadata; no entries have analyte compound names or sim_ins (ground-truth analyte intensity) columns.

## Limitations

- simmzml_blank() does not model chromatographic peak shapes or retention-time tailing—background is uniform across the RT dimension.
- Matrix dataset must be pre-loaded in R memory (e.g., mzm from MoNA/HMDB); custom matrices require manual preparation in msp or RDS format.
- Noise model is simplified (Poisson or Gaussian); real instrument background may exhibit more complex spectral structure or m/z-dependent noise profiles.
- Output .mzML files do not include scan-level metadata such as instrument type, ionization mode, or collision energy (these are filled with defaults).
- No changelog available for version compatibility or breaking changes in simmzml_blank() API.

## Evidence

- [other] simmzml_blank() produces .mzML files with configurable options: pure noise blanks via rtrange parameter, or blanks with serum matrix peaks by passing the mzm matrix dataset to the matrixmz parameter.: "simmzml_blank() produces .mzML files with configurable options: pure noise blanks via rtrange parameter, or blanks with serum matrix peaks by passing the mzm matrix dataset to the matrixmz parameter."
- [other] Generate synthetic m/z and retention-time arrays covering the full instrument range with appropriate resolution. Synthesize background noise using a realistic noise model (e.g., Poisson or Gaussian distribution) across the m/z–retention-time matrix. If matrix peaks are enabled, retrieve or load the mzm matrix dataset and overlay selected matrix ion peaks at specified intensities onto the noise baseline.: "Generate synthetic m/z and retention-time arrays covering the full instrument range with appropriate resolution. Synthesize background noise using a realistic noise model (e.g., Poisson or Gaussian"
- [other] Encode the combined spectral data (noise + optional matrix) as base64-encoded binary using the base64enc package. Construct mzML XML structure with appropriate scan headers, precursor metadata, and product ion arrays, then write to the output .mzML file.: "Encode the combined spectral data (noise + optional matrix) as base64-encoded binary using the base64enc package. Construct mzML XML structure with appropriate scan headers, precursor metadata, and"
- [intro] The underlying engine handles binary data encoding via the `base64enc` package: "The underlying engine handles binary data encoding via the `base64enc` package"
- [intro] removing the need for `mzR` or other heavy dependencies for file generation: "removing the need for `mzR` or other heavy dependencies for file generation"
