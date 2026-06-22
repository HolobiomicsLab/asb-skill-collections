---
name: ground-truth-intensity-calculation
description: Use when when generating synthetic LC/GC-MS .mzML files with companion ground-truth peak tables for method validation, you need to calculate the absolute maximum intensity that each simulated peak would exhibit in the raw mass spectrometry matrix.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - base64enc
  - mzrtsim
  - SummarizedExperiment
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

# ground-truth-intensity-calculation

## Summary

Compute absolute ground-truth maximum intensity (sim_ins) for each simulated LC/GC-MS peak by accounting for response factor, peak height scaling, and chromatographic profile shape. This enables benchmarking of peak detection and quantification methods against known ground truth.

## When to use

When generating synthetic LC/GC-MS .mzML files with companion ground-truth peak tables for method validation, you need to calculate the absolute maximum intensity that each simulated peak would exhibit in the raw mass spectrometry matrix. This is essential when benchmarking peak-picking algorithms, intensity estimation, or quantification workflows that require known-truth comparisons.

## When NOT to use

- Input is already a real experimental LC/GC-MS dataset (use peak-picking and quantification on raw .mzML files instead).
- You need to recover true intensities from noisy real data rather than assign ground truth to synthetic data.
- Peak profile shape is unknown or you cannot specify or validate a chromatographic model (Gaussian or EMG parameters).

## Inputs

- Spectral database record (m/z list, retention time, database intensity, compound name)
- Response factor (scalar, instrument-specific)
- Peak height scaling factor (scalar, user-configurable)
- Chromatographic peak-shape model (Gaussian or exponentially-modified Gaussian with tailing parameter)
- Peak width parameter (seconds or scan indices)

## Outputs

- sim_ins column in companion CSV file (absolute ground-truth maximum intensity per peak)
- CSV table with columns: m/z, retention_time, database_intensity, sim_ins, compound_name

## How to apply

Within the simmzml() function workflow, after retrieving spectral records (m/z, retention time, database intensity) from MoNA or HMDB and selecting a peak-shape model (Gaussian or exponentially-modified Gaussian with configurable tailing and peak-width parameters), compute sim_ins by multiplying the database intensity by the response factor and peak height scaling factor, then further modulate this product by the chromatographic profile intensity at the peak apex (which ranges from 0 to 1 depending on the Gaussian or EMG shape). Store this calculated value in the sim_ins column of the companion CSV file. Validate that sim_ins values are positive, finite, and consistent with the peak-shape model used; sim_ins should be the maximum value observed across all time points for that peak's retention-time profile.

## Related tools

- **mzrtsim** (R package that wraps raw data simulation; simmzml() function is the primary entry point for ground-truth intensity calculation and .mzML file generation) — https://github.com/yufree/mzrtsim
- **base64enc** (Encodes the binary mass spectrometry matrix (including intensity values) in Base64 format for mzML file storage; intensity values must be encoded after calculation)
- **SummarizedExperiment** (Optional wrapper for wrapping sim_ins values and peak metadata into Bioconductor-compatible data structure via mzrtsim_se() function)

## Examples

```
library(mzrtsim)
data("monams1")
simmzml(db=monams1, name='test')
# Outputs: test.mzML and test.csv with sim_ins column
```

## Evaluation signals

- sim_ins values are positive, finite, and non-zero for all peaks in the output CSV.
- sim_ins column values do not exceed the maximum intensity in the raw .mzML file's corresponding m/z and retention-time window.
- For a given peak, sim_ins is larger than all intensity values at non-apex time points (i.e., it represents the true maximum of the chromatographic profile).
- sim_ins scales appropriately with response factor and peak height parameters: doubling response factor approximately doubles sim_ins; zeroing peak height yields sim_ins near zero.
- Companion CSV row count matches the total number of peaks selected from the spectral database; no NaN or NA values in sim_ins column.

## Limitations

- sim_ins calculation assumes the response factor is constant across the m/z and retention-time range; real instruments may exhibit non-linear response or m/z-dependent sensitivity.
- Chromatographic profile is modeled as Gaussian or exponentially-modified Gaussian; complex, multi-modal, or shouldered peaks in real data are not captured.
- Database intensity values from MoNA/HMDB may not reflect the same ionization conditions or instrument tuning as the target analysis; sim_ins is valid only as a relative ranking or within the parameter space of the simulation.
- No changelog is available; parameters, calculation method, or default response factors may change between mzrtsim versions without notice.

## Evidence

- [intro] simmzml() generates a companion CSV file containing ground-truth peak information (m/z, retention time, database intensity, simulated maximum intensity, compound name), with the sim_ins column representing the absolute ground-truth maximum intensity calculated by accounting for response factor, peak height, and chromatographic profile.: "The output CSV now includes a `sim_ins` column — the absolute ground-truth maximum intensity of each simulated peak, accounting for response factor, peak height, and chromatographic profile."
- [intro] Apply chromatographic peak-shape modeling (Gaussian or exponentially-modified Gaussian) with configurable tailing and peak-width parameters to generate realistic retention-time profiles. Compute sim_ins ground-truth maximum intensity by accounting for response factor, peak height scaling, and the chromatographic profile.: "Apply chromatographic peak-shape modeling (Gaussian or exponentially-modified Gaussian) with configurable tailing and peak-width parameters to generate realistic retention-time profiles. 4. Compute"
- [readme] You will find `test.mzML` and corresponding `test.csv` with m/z, retention time, compound name, and the simulated absolute ground-truth maximum intensity (`sim_ins`) of the peaks.: "You will find `test.mzML` and corresponding `test.csv` with m/z, retention time, compound name, and the simulated absolute ground-truth maximum intensity (`sim_ins`) of the peaks."
- [intro] Raw data simulation — produces `.mzML` files from real spectral databases (MoNA, HMDB), with realistic chromatographic peak shapes, tailing, noise, and matrix background: "Raw data simulation — produces `.mzML` files from real spectral databases (MoNA, HMDB), with realistic chromatographic peak shapes, tailing, noise, and matrix background"
- [intro] For each selected compound, retrieve m/z, retention time, and database intensity values.: "For each selected compound, retrieve m/z, retention time, and database intensity values."
