---
name: aird-format-conversion-and-validation
description: Use when you have vendor mass spectrometry raw files (e.g., .raw, .d, .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - AirdPro V5
  - AirdPro V6
  - ProteoWizard
  - AirdPro
  - Wine
  - .NET Framework 4.8
  - Docker Desktop
  - AirdSDK
  - Redis
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- AirdPro V5 is now available at 2023.7
- AirdPro V6 is now available at 2024.4
- pwiz_bindings_cli.dll from the ProteoWizard project
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_aird
    doi: 10.1186/s12859-021-04490-0
    title: aird
  dedup_kept_from: coll_aird
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-021-04490-0
  all_source_dois:
  - 10.1186/s12859-021-04490-0
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# aird-format-conversion-and-validation

## Summary

Convert vendor mass spectrometry raw files to the Aird format using AirdPro CLI or GUI, and validate the output by verifying file integrity, format compliance, and conversion completion. Aird is a computation-oriented format that enables higher compression ratios and faster decoding compared to standard formats like mzML.

## When to use

You have vendor mass spectrometry raw files (e.g., .raw, .d, .wiff2 formats) from instruments supported by ProteoWizard MSConvert, and you need to convert them to Aird format for downstream analysis that benefits from improved compression, faster XIC computation, or distributed batch processing via Redis. This is especially relevant for large-scale DDA, DIA/SWATH, PRM, or MRM acquisition datasets where storage and computational efficiency are priorities.

## When NOT to use

- Input files are already in Aird format (.aird + .json pair); conversion is redundant.
- Vendor instrument is not supported by ProteoWizard MSConvert (AirdPro depends on pwiz_bindings_cli.dll); use an alternative conversion tool.
- Precision or compression requirements demand lossless storage of all floating-point digits; Aird's precision control may truncate mass accuracy beyond specified threshold.

## Inputs

- vendor mass spectrometry raw files (.raw, .d, .wiff2, .mzML, .mzXML formats)
- acquisition method type specification (DDA, DIA_SWATH, PRM, MRM, or COMMON)
- m/z precision threshold (default 0.0001)
- optional compression strategy parameters (ZDVB, Stack-ZDPD, StackZDVB, or Brotli/Snappy/Zstd/Zlib combinations)

## Outputs

- Aird data file (.aird suffix)
- Aird index file (.json suffix, same base filename as .aird)
- conversion log or task status record

## How to apply

Launch the AirdPro CLI or GUI container (V5 or V6) with Docker, mounting input vendor raw files and an output directory. Specify the acquisition method (DDA, DIA_SWATH, PRM, MRM, or COMMON), precision threshold (default 0.0001 m/z), and compression strategy. For first-run execution, allocate ≥30 minutes for Wine initialization and .NET Framework 4.8 component download in the container. Execute the conversion and monitor for completion. Validate the output by confirming: (1) paired .aird data file and .json index file exist in the output directory with matching base filenames; (2) file sizes are non-zero and consistent with source complexity; (3) file format signatures match Aird specification (index suffix .json, data suffix .aird); (4) no conversion exceptions or retrial loops occurred. Expect 20–30% performance degradation when running through Wine on Linux/Mac.

## Related tools

- **AirdPro** (GUI and CLI client for conversion from vendor files to Aird format; runs in Docker with Wine and .NET Framework 4.8) — https://github.com/CSi-Studio/AirdPro
- **ProteoWizard** (underlying MSConvert library (pwiz_bindings_cli.dll) that enables vendor file format support)
- **Wine** (runtime environment to execute Windows/.NET applications in Docker containers on Linux/Mac)
- **.NET Framework 4.8** (runtime dependency for AirdPro C# application)
- **Docker Desktop** (container orchestration and execution platform for AirdPro CLI/GUI images)
- **AirdSDK** (secondary development library for reading Aird files (Java, C#, Python)) — https://github.com/CSi-Studio/Aird-SDK
- **Redis** (optional distributed task queue (Database0, key 'ConvertTask', value Set of ConvertJob JSON objects) for batch conversion across multiple AirdPro nodes)

## Examples

```
docker run --rm -v /path/to/vendor/files:/input -v /path/to/output:/output airdpro:cli /app/run-cli.sh /input/sample.raw /output --type=DDA --mzPrecision=0.0001
```

## Evaluation signals

- Both .aird and .json files exist in the output directory with identical base filenames and non-zero file sizes
- Paired .aird (data) and .json (index) files are stored in the same directory, conforming to Aird specification
- .aird file size is consistent with expected compression ratio for the acquisition method and source complexity (20–50% smaller than uncompressed mzML for typical DDA/SWATH)
- Conversion log or task status shows no exception, retrial, or incomplete state; first-run execution completes within documented timeframe (≥30 minutes for Wine initialization on first invocation)
- JSON index file parses without error and contains expected metadata (scan count, precursor info, acquisition method tag)

## Limitations

- First-run execution requires ≥30 minutes for Wine initialization and .NET Framework 4.8 component download; not suitable for time-critical single-file conversions without prior container setup.
- 20–30% performance degradation when running through Wine on non-Windows platforms; native Windows execution or GPU-accelerated conversion is not supported in published images.
- Batch conversion via Redis requires separate Redis server infrastructure and careful JSON task formatting (sourcePath, targetPath, type, mzPrecision fields); failure to format ConvertJob objects correctly results in skipped tasks.
- Aird format precision truncation (controlled by mzPrecision parameter) may reduce mass accuracy for applications requiring sub-ppm m/z resolution; no option to disable lossy compression of m/z values.
- No changelog available in repository; version history must be inferred from README feature lists; patch-level bug fixes and stability improvements are not explicitly documented.

## Evidence

- [readme] AirdPro is a GUI client for conversion from vendor files to Aird files: "AirdPro is a GUI client for conversion from vendor files to Aird files. AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project."
- [methods] Wine initialization and .NET Framework download time: "Wine needs to initialize and download .NET Framework components, taking more than 30 minutes"
- [readme] Aird output file format specification: "Aird Index File Suffix: .json <br/>Aird Data File Suffix: .aird <br/>Aird Index File and Aird Data File show be stored in the same directory with the same file name but with different suffix"
- [readme] Supported acquisition methods: "The value can be "DIA_SWATH", "DDA", "PRM", "COMMON""
- [readme] Compression performance and format benefits: "Aird is defined as a computing-oriented data format with high scalability, compression rate, and fast decoding speed."
- [methods] Performance penalty under Wine: "20-30% performance degradation when running through Wine"
- [readme] Vendor format support via ProteoWizard: "By using library from ProteoWizard MSConvert. AirdPro can convert all the vendor format that MSConvert supports to Aird format."
