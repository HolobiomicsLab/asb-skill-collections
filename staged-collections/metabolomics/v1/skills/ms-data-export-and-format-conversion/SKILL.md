---
name: ms-data-export-and-format-conversion
description: Use when metabolomics data needs conversion between open standardized formats (mzML, mzXML, MGF) for interoperability across analysis software and repositories in LC-MS and GC-MS untargeted lipidomics.
when_to_use_negative:
- Your analysis tool natively supports your raw instrument format (e.g., Thermo Xcalibur software reading .raw files directly) and you do not need to share data with external repositories.
- You are working exclusively with processed feature tables (m/z-by-sample matrices) rather than raw spectra; format conversion applies only to spectrum-level data.
- Your workflow requires vendor-specific metadata or calibration that is lost in conversion to open formats.
edam_operation: http://edamontology.org/operation_3650
edam_topics:
- http://edamontology.org/topic_3370
- http://edamontology.org/topic_0769
tools:
- name: pyteomics
  role: Read and parse open MS data files (mzML, mzXML, MGF) into in-memory pandas data frames for downstream filtering and export
- name: MZmine
  role: Convert vendor raw formats to mzML/mzXML and perform batch format conversion with optional feature detection and noise filtering
  repo: https://github.com/mzmine/mzmine
- name: Thermo RawFileReader
  role: Native Windows DLL for reading and converting Thermo .raw files to open formats via command-line or Python API
- name: Waters CDCReader
  role: Convert Waters .raw files to tab/space-delimited text format or mzML via command-line batch processing
- name: Apache feather
  role: Cache converted MS spectra in columnar format for fast repeated querying of large datasets
- name: pandas
  role: Serialize and export filtered or processed MS spectra to tabular formats (CSV/TSV) with scan identifiers, m/z, intensity, and metadata
merged_aliases:
- ms-data-format-conversion-and-export
merged_alias_records:
- alias: ms-data-format-conversion-and-export
  slug: ms-data-format-conversion-and-export
  jaccard_score: 1.0
  method: token-set-jaccard
  decision: auto
provenance:
  source_task_ids:
  - task_001
  - task_003
  source_papers:
  - doi: 10.1038/s41592-025-02660-z
    title: A universal language for finding mass spectrometry data patterns
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/ms-data-export-and-format-conversion@sha256:c9ca95f6ed2d11d03c5fbfe73a00fede6e097676dc1e55b7e32d209df09ca698
---

# MS data export and format conversion

## Summary

Convert mass spectrometry data between open standardized formats (mzML, mzXML, MGF) to enable interoperability across analysis software and repositories. This skill is essential for querying MS data with tools like MassQL that require specific input formats.

## When to use

You have raw MS data in vendor-specific or proprietary formats (Thermo .raw, Waters .raw, Agilent .d) and need to query or analyze it using open-source tools (MassQL, MZmine, pyOpenMS) that only accept mzML, mzXML, or MGF formats; or you need to deposit MS data in public repositories (GNPS/MassIVE, Metabolomics Workbench, MetaboLights) that mandate open formats.

## When NOT to use

- Your analysis tool natively supports your raw instrument format (e.g., Thermo Xcalibur software reading .raw files directly) and you do not need to share data with external repositories.
- You are working exclusively with processed feature tables (m/z-by-sample matrices) rather than raw spectra; format conversion applies only to spectrum-level data.
- Your workflow requires vendor-specific metadata or calibration that is lost in conversion to open formats.

## Inputs

- Vendor-specific raw MS data files (Thermo .raw, Waters .raw, Agilent .d)
- Proprietary MS data formats
- MS data in non-standard or legacy formats

## Outputs

- mzML-formatted MS data files with complete metadata
- mzXML-formatted MS data files with complete metadata
- MGF-formatted MS/MS spectra (for product-ion queries)
- Apache feather cache files (optional, for repeated queries)

## How to apply

Use vendor-specific converters or multi-format readers to transform raw instrument data into mzML or mzXML (both support MS1 and MS/MS spectra with metadata like retention time and scan number). For targeted product-ion queries, MGF format (containing precursor m/z, product ion m/z, and intensity values) is also acceptable. Ensure the converted files retain critical metadata: scan identifiers, precursor m/z, retention times, and intensity values as numeric fields. Optionally cache converted spectra as Apache feather format for repeated querying to improve I/O performance when iterating over large datasets (>230 million MS/MS spectra in public repositories benefit from this optimization). Validate the output by spot-checking scan counts and m/z value ranges against the original instrument software.

## Related tools

- **pyteomics** (Read and parse open MS data files (mzML, mzXML, MGF) into in-memory pandas data frames for downstream filtering and export)
- **MZmine** (Convert vendor raw formats to mzML/mzXML and perform batch format conversion with optional feature detection and noise filtering) — https://github.com/mzmine/mzmine
- **Thermo RawFileReader** (Native Windows DLL for reading and converting Thermo .raw files to open formats via command-line or Python API)
- **Waters CDCReader** (Convert Waters .raw files to tab/space-delimited text format or mzML via command-line batch processing)
- **Apache feather** (Cache converted MS spectra in columnar format for fast repeated querying of large datasets)
- **pandas** (Serialize and export filtered or processed MS spectra to tabular formats (CSV/TSV) with scan identifiers, m/z, intensity, and metadata)

## Examples

```
from pyteomics import mzml; import pandas as pd; spectra = [s for s in mzml.read('data.mzML')]; df = pd.DataFrame([(s['scan number'], s['m/z array'], s['intensity array']) for s in spectra]); df.to_feather('data.feather')
```

## Evaluation signals

- Output mzML/mzXML files parse without errors in pyteomics and contain expected XML schema structure (MS1 and MS/MS spectrum elements with scan metadata).
- Scan count in converted file matches the count reported by the original instrument software (within ±1% tolerance for lossy filtering).
- All exported MS/MS records contain non-null precursor m/z, product ion m/z, and intensity values; no NaN or zero-intensity spectra introduced during conversion.
- Retention time values span the expected chromatographic range; scan numbers are sequential and match original data.
- MGF export for product-ion queries contains ≥3 fields per spectrum: PRECURSORMZ, PEPMASS (or equivalent), TITLE, and intensity list; verification can be done by parsing the file header and spot-checking 5–10 random spectra.

## Limitations

- Conversion of vendor-specific .raw files (Thermo, Waters, Agilent) requires platform-specific DLLs or software; Windows-only converters limit cross-platform reproducibility.
- mzML/mzXML conversion may lose vendor-specific metadata (e.g., instrument-specific calibration parameters, acquisition parameters not defined in the open schema).
- MGF format does not retain MS1 isotope pattern information; if isotope-based queries (e.g., iron-characteristic 54Fe/56Fe patterns at 6.3% relative intensity) are needed, mzML or mzXML must be used instead.
- Large dataset conversions (>100 GB) can be memory-intensive; feather caching mitigates repeated I/O but does not reduce initial conversion time.

## Evidence

- [full_text] The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats: "The MassQL reference query engine is written in Python and utilizes pyteomics to read open MS data files from mzML, mzXML and MGF formats"
- [full_text] spectra in data frame format can optionally be saved as Apache feather files to cache data for repeated querying: "spectra in data frame format can optionally be saved as Apache feather files to cache data for repeated querying"
- [readme] For Water's .raw files, UniDec is bundled with converters (CDCReader.exe) to convert the data to .txt. It will compress the retention time dimension into a single spectrum.: "For Water's .raw files, UniDec is bundled with converters (CDCReader.exe) to convert the data to .txt. It will compress the retention time dimension into a single spectrum."
- [full_text] entire MS repositories, including GNPS/MassIVE, Metabolomics Workbench and MetaboLights: "entire MS repositories, including GNPS/MassIVE, Metabolomics Workbench and MetaboLights"
- [other] Export matched MS/MS spectra in tabular format (CSV/TSV) with scan identifiers, precursor m/z, product ion m/z, intensity values, and metadata.: "Export matched MS/MS spectra in tabular format (CSV/TSV) with scan identifiers, precursor m/z, product ion m/z, intensity values, and metadata."
