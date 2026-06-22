---
name: scan-index-filtering-by-ms-level
description: Use when when you have generated a scan index from rawrr::readIndex() on a Thermo .
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
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- Calling a wrapper method typically results in the execution of methods defined in the `RawFileReader` dynamic link library provided by Thermo Fisher Scientific.
- invoke compiled `C#` wrapper methods using a system call. Calling a wrapper method typically results in the execution of methods defined in the `RawFileReader` dynamic link library provided by Thermo
- Our implementation consists of two language layers, the top `R` layer and the hidden `C#` layer.
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# scan-index-filtering-by-ms-level

## Summary

Filter a scan index data.frame to retain only MS1-level (precursor-ion) scans from a Thermo Orbitrap raw file. This isolates full-scan survey spectra from tandem MS fragments, enabling focused analysis of parent ion m/z and intensity without interference from product-ion scans.

## When to use

When you have generated a scan index from rawrr::readIndex() on a Thermo .raw file and need to work exclusively with MS1 survey scans—for example, to extract base-peak m/z and intensity values, compute retention-time alignments, or assess precursor ion chromatography without contamination from MS/MS fragments (MS2+).

## When NOT to use

- Input is already a feature table or peak list (filtering has already occurred)
- You need MS2 (tandem) or MS3 spectra—use (ms == 2) or (ms == 3) instead
- Raw file has not yet been indexed—call rawrr::readIndex() first

## Inputs

- data.frame from rawrr::readIndex() with 'ms' column encoding MS level
- Thermo Fisher Scientific .raw file (already loaded via rawrr in prior step)

## Outputs

- data.frame of MS1-only scan metadata (subset of input index, same schema)
- integer vector of MS1 scan numbers for downstream readSpectrum() calls

## How to apply

After calling rawrr::readIndex() to retrieve a scan index data.frame containing an 'ms' column, subset the index using the logical condition (ms == 1) to retain only MS1 scans. This column encodes the MS level as an integer: MS1 = 1, MS2 = 2, MS3 = 3, etc. Perform the subsetting before iterating over scan numbers to extract spectral properties with readSpectrum(). The filtering step is fast (vector indexing on an in-memory data.frame) and does not require re-reading the binary raw file, making it suitable for large experiments with tens of thousands of scans.

## Related tools

- **rawrr** (Provides readIndex() to generate scan index data.frame and readSpectrum() to retrieve MS1 spectral data; wraps RawFileReader .NET assembly for programmatic access to Orbitrap raw files) — https://github.com/fgcz/rawrr
- **RawFileReader** (Underlying .NET assembly that rawrr wraps to read binary Thermo .raw file structures; executed via system call) — https://github.com/thermofisherlsms/RawFileReader

## Examples

```
index <- rawrr::readIndex(rawrr::sampleFilePath()); ms1_index <- subset(index, ms == 1); ms1_scans <- ms1_index$scan
```

## Evaluation signals

- Filtered data.frame has length (nrow) equal to count of MS1 scans in the experiment; row count is ≤ original unfiltered index
- All rows in filtered data.frame have ms == 1 (no MS2, MS3, or NA values remain)
- scan column in filtered data.frame contains monotonically increasing integer scan numbers
- Subsequent readSpectrum() calls on filtered scan numbers return rawrrSpectrum objects without errors
- MS1 count and scan range match instrument metadata (e.g., file header 'Number of scans' and 'Number of MS1 scans' fields)

## Limitations

- Filtering occurs in-memory on the indexed data.frame; for very large files (>100k scans) this is still fast, but memory footprint scales with file size
- The 'ms' column encoding assumes standard Thermo nomenclature (1=MS1, 2=MS2, etc.); non-standard or corrupted scan headers may produce unexpected ms values
- Filtering does not validate scan quality or remove scans with zero intensity; downstream readSpectrum() calls may return empty or near-zero spectra

## Evidence

- [other] Subset the index to retain only MS1-level scans (ms == 1): "Subset the index to retain only MS1-level scans (ms == 1)."
- [other] Generate scan index as data.frame using readIndex() on the raw file: "Generate the scan index as a data.frame using readIndex() on the raw file."
- [readme] rawrr wraps the functionality of the RawFileReader .NET assembly: "rawrr wraps the functionality of the RawFileReader .NET assembly"
- [results] By using the readIndex() function a data.frame that indexes all scans found in a raw file is returned: "By using the `readIndex()` function a `data.frame` that indexes all scans found in a raw file is returned"
- [methods] R functions request access to data from binary raw files via compiled C# wrapper methods using system calls: "R functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled C# wrapper methods using a system call."
