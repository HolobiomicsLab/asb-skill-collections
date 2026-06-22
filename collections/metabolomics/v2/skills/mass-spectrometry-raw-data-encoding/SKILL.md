---
name: mass-spectrometry-raw-data-encoding
description: Use when you have generated or obtained a two-dimensional mass-spectrometry intensity matrix (m/z × retention time scan points) with simulated or experimental peak shapes, noise, and background, and need to encode it as a binary .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - R
  - base64enc
  - mzrtsim
  - mzR
  - SummarizedExperiment
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

# Mass Spectrometry Raw Data Encoding

## Summary

Encode simulated LC/GC-MS raw mass spectrometry data matrices into Base64 format and write them to standardized .mzML file structures for downstream metabolomics analysis. This skill bridges in-memory peak intensity matrices (with realistic chromatographic profiles, noise, and matrix background) to portable, binary-encoded MS data files.

## When to use

You have generated or obtained a two-dimensional mass-spectrometry intensity matrix (m/z × retention time scan points) with simulated or experimental peak shapes, noise, and background, and need to encode it as a binary .mzML file for distribution, archival, or integration into standard metabolomics workflows (e.g., xcms, MZmine2, or other mzML-compatible tools).

## When NOT to use

- Input is already a finalized .mzML or .netCDF file; re-encoding is redundant.
- You need only a peak list or feature table, not raw continuous MS data.
- Target format is not mzML (e.g., mzXML, netCDF, or vendor-native binary); use format-specific encoders instead.

## Inputs

- Simulated or experimental MS intensity matrix (2D array: scans × detected m/z)
- Scan metadata (acquisition time in seconds, precursor m/z, collision energy, ion mode)
- Peak ground-truth table (m/z, retention time, simulated maximum intensity, compound name)

## Outputs

- .mzML file (XML-wrapped binary MS data with Base64-encoded intensity arrays)
- Companion .csv file with ground-truth peak information and sim_ins (absolute maximum intensity per peak)

## How to apply

Construct the raw MS intensity matrix by concatenating individual scan records (each scan contains m/z array and intensity array from chromatographic and spectral simulation). Apply Base64 encoding to the binary-formatted (typically little-endian float32 or int32) matrix using the base64enc package. Embed the encoded payload into the mzML XML structure under the appropriate <binaryDataArray> elements, specifying the correct cvParam attributes (e.g., 'MS:1000521' for 32-bit float, 'MS:1000576' for no compression). Write metadata headers (scan acquisition time, precursor m/z for MS2, collision energy, ion mode) into the corresponding mzML elements. Validate the output by confirming the file parses correctly in standard MS software (e.g., mzR::openMSfile in R or pymzml in Python).

## Related tools

- **base64enc** (Encodes the binary MS intensity matrix into Base64 format for safe embedding in XML)
- **mzrtsim** (Generates simulated LC/GC-MS raw data and wraps simmzml() for end-to-end .mzML file creation) — https://github.com/yufree/mzrtsim
- **mzR** (Alternative library for reading/validating .mzML files (mzrtsim removes dependency for file generation))
- **SummarizedExperiment** (Wraps encoded .mzML data for seamless Bioconductor workflow integration via mzrtsim_se())

## Examples

```
library(mzrtsim)
data("monams1")
simmzml(db=monams1, name='test')
```

## Evaluation signals

- Output .mzML file is well-formed XML and parses without error in standard MS software (mzR, pymzml, Proteowizard).
- Base64-decoded binary payload matches the original intensity matrix dimensions and value ranges (accounting for floating-point precision).
- Companion .csv contains exactly one row per simulated compound with non-empty m/z, retention_time, database_intensity, sim_ins, and compound_name columns.
- sim_ins values are positive, realistic absolute intensities (e.g., 100–1,000,000 range typical of LC-MS detectors) and scale consistently with input response factor and peak-height parameters.
- All scans reference valid acquisition times (in seconds) that align with the retention-time entries in the companion CSV.

## Limitations

- Base64 encoding increases file size by ~33% compared to raw binary; no compression is applied by default.
- mzML XML structure is verbose and may become slow to parse for very large numbers of scans (>100,000); consider streaming readers or indexed mzML for high-throughput datasets.
- Ground-truth sim_ins values are only as accurate as the underlying chromatographic peak-shape model (Gaussian or exponentially-modified Gaussian) and response-factor calibration; real instruments may deviate.
- No native support for variable m/z arrays (common in high-resolution instruments); requires pre-binning or resampling to a fixed m/z grid for some downstream tools.

## Evidence

- [intro] The underlying engine handles binary data encoding via the `base64enc` package: "The underlying engine handles binary data encoding via the `base64enc` package"
- [readme] simmzml() generates .mzML files with Base64-encoded peak data and companion CSV: "`simmzml()` generates one `.mzML` file and a companion `.csv` file containing ground-truth peak information (m/z, retention time, database intensity, simulated maximum intensity, compound name)."
- [intro] sim_ins column represents absolute ground-truth maximum intensity calculated by chromatographic profile: "The output CSV now includes a `sim_ins` column — the absolute ground-truth maximum intensity of each simulated peak, accounting for response factor, peak height, and chromatographic profile."
- [methods] Chromatographic peak-shape modeling applied to retention-time profiles before encoding: "Apply chromatographic peak-shape modeling (Gaussian or exponentially-modified Gaussian) with configurable tailing and peak-width parameters to generate realistic retention-time profiles."
- [readme] Base64 encoding and mzML file structure writing are handled natively: "The native mzML writer handles the binary encoding (Base64) internally without requiring external MS data libraries."
