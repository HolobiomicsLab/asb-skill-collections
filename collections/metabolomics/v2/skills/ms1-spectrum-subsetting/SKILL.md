---
name: ms1-spectrum-subsetting
description: Use when after generating a scan index from a Thermo Fisher Orbitrap
  raw file using readIndex(), apply this skill when your analysis goal requires working
  exclusively with MS1 (precursor) scans rather than tandem MS (MS2/MS3) spectra.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RawFileReader
  - R
  - rawrr
  - Spectra
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- Calling a wrapper method typically results in the execution of methods defined in
  the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific.
- invoke compiled `C#` wrapper methods using a system call. Calling a wrapper method
  typically results in the execution of methods defined in the `RawFileReader` dynamic
  link library provided by Thermo
- Our implementation consists of two language layers, the top `R` layer and the hidden
  `C#` layer.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr_2_cq
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_rawrr_2_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2020.10.30.362533
  all_source_dois:
  - 10.1101/2020.10.30.362533
  - 10.1021/acs.jproteome.0c00866
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# MS1-level spectrum subsetting

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Filter a scan index data.frame to retain only MS1-level mass spectrometry scans, enabling targeted analysis of precursor ion spectra. This skill is essential when downstream analysis (base-peak extraction, retention time alignment, chromatogram construction) requires isolation of survey scans from a mixed MS1/MS2 dataset.

## When to use

After generating a scan index from a Thermo Fisher Orbitrap raw file using readIndex(), apply this skill when your analysis goal requires working exclusively with MS1 (precursor) scans rather than tandem MS (MS2/MS3) spectra. Common triggers include: constructing base-peak m/z and intensity tables, aligning retention times, or generating extracted ion chromatograms where only survey-scan data is relevant.

## When NOT to use

- Input is already restricted to MS1 scans (e.g., pre-filtered raw file or targeted MS1-only acquisition method).
- Analysis goal requires MS2 fragmentation spectra or depends on tandem MS data for peptide identification.
- Scan index does not contain an 'ms' column (malformed or non-standard index structure).

## Inputs

- data.frame scan index (output of rawrr::readIndex())
- Thermo Fisher Orbitrap raw file (already indexed)

## Outputs

- data.frame: subset scan index containing only MS1-level rows
- integer vector: scan numbers for downstream readSpectrum() calls

## How to apply

After calling readIndex() to generate a data.frame indexing all scans in the raw file, subset the data.frame using the 'ms' column to retain only rows where ms == 1. This column indicates the tandem MS level of each scan. The filtering operation is a logical subsetting step (e.g., index[index$ms == 1, ]) that removes all MS2, MS3, and higher-order fragmentation scans. Verify the filter by checking that the resulting data.frame contains only rows with ms=1 and that scan counts are reasonable relative to total runtime (e.g., a 55-minute LC-MS run yielding ~24,000 total scans typically contains several thousand MS1 scans). This step precedes per-spectrum operations like readSpectrum() calls on the filtered scan numbers.

## Related tools

- **rawrr** (Provides readIndex() function to generate scan index data.frame and readSpectrum() to retrieve individual MS1 spectra after subsetting) — https://github.com/fgcz/rawrr
- **RawFileReader** (Underlying .NET assembly wrapped by rawrr; enables binary raw file access from which scan metadata (including ms level) is extracted) — https://github.com/thermofisherlsms/RawFileReader
- **Spectra** (Bioconductor package that can consume MS1-filtered scan indices via MsBackendRawFileReader for downstream statistical and visualization workflows)

## Examples

```
index_df <- rawrr::readIndex(raw_file_path); ms1_index <- index_df[index_df$ms == 1, ]; ms1_scan_numbers <- ms1_index$scan
```

## Evaluation signals

- All rows in output data.frame have ms == 1 (invariant check).
- Output row count is substantially less than input row count (typical ratio ~10–50% depending on acquisition method), reflecting removal of MS2 and higher scans.
- Scan numbers in the MS1-only index are contiguous or sparse integers within the range [1, total_scans_in_file] (data integrity check).
- Retention time values in the filtered index span the expected LC runtime (e.g., 0 to 55 minutes for a 55-minute gradient).
- Subsequent readSpectrum() calls on filtered scan numbers succeed and return rawrrSpectrum objects with non-empty m/z and intensity arrays (functional downstream check).

## Limitations

- Filtering by ms == 1 assumes the scan index column is correctly populated by the RawFileReader API; malformed or corrupted raw files may yield unexpected or missing ms values.
- This skill operates only on the in-memory data.frame; it does not re-parse or validate the binary raw file itself, so systematic errors in raw file metadata may not be caught.
- High-resolution Orbitrap data with data-dependent acquisition (DDA) typically generate MS1/MS2 ratios of 1:10 or higher; extremely low or zero MS1 counts may indicate instrument configuration issues or acquisition failures not detectable by this filter alone.
- The skill assumes the 'ms' column naming convention used by rawrr; alternative or custom scan indices may use different column names or encodings.

## Evidence

- [other] Generate the scan index as a data.frame using readIndex() on the raw file.: "Generate the scan index as a data.frame using readIndex() on the raw file."
- [other] Subset the index to retain only MS1-level scans (ms == 1).: "Subset the index to retain only MS1-level scans (ms == 1)."
- [results] By using the `readIndex()` function a `data.frame` that indexes all scans found in a raw file is returned: "By using the `readIndex()` function a `data.frame` that indexes all scans found in a raw file is returned"
- [results] using only MS1-level scans: "Filter MS scans using ms filter; using only MS1-level scans"
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
