---
name: proteomics-data-format-conversion
description: Use when you have vendor raw files (e.g., .raw from Thermo, .d from Agilent, .wiff2 from Sciex) that need to be converted to a standard format for analysis pipelines, data sharing, or when you require the high compression rates and fast decoding provided by Aird format.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3650
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - AirdPro V6
  - pwiz_bindings_cli.dll
  - ProteoWizard
  - AirdPro
  - Docker Desktop for Mac / Docker Engine
  - Redis
  - AirdSDK
  techniques:
  - ion-mobility-MS
  - tandem-MS
derived_from:
- doi: 10.1186/s12859-021-04490-0
  title: aird
evidence_spans:
- AirdPro V6 is now available at 2024.4
- based on pwiz_bindings_cli.dll from the ProteoWizard project
- pwiz_bindings_cli.dll from the ProteoWizard project
- based on pwiz_bindings_cli.dll from the ProteoWizard project.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_aird_cq
    doi: 10.1186/s12859-021-04490-0
    title: aird
  dedup_kept_from: coll_aird_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-021-04490-0
  all_source_dois:
  - 10.1186/s12859-021-04490-0
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# proteomics-data-format-conversion

## Summary

Convert vendor-specific mass spectrometry raw files to open, computation-oriented formats (mzML or Aird) using ProteoWizard bindings, enabling downstream analysis and data sharing. This skill is essential when working with proprietary instrument outputs that require standardization for cross-platform analysis or compression-optimized storage.

## When to use

Apply this skill when you have vendor raw files (e.g., .raw from Thermo, .d from Agilent, .wiff2 from Sciex) that need to be converted to a standard format for analysis pipelines, data sharing, or when you require the high compression rates and fast decoding provided by Aird format. Typical triggers include batch processing of instrument outputs, preparing data for public repositories, or switching analysis software that requires mzML/mzXML input.

## When NOT to use

- Input is already in mzML, mzXML, or Aird format — no conversion needed.
- Vendor raw file is from an instrument not supported by MSConvert (check ProteoWizard vendor list before attempting).
- Analysis pipeline requires vendor-specific metadata or acquisition-mode details not preserved in standard formats — verify format coverage first.

## Inputs

- Vendor raw mass spectrometry file (Thermo .raw, Agilent .d, Sciex .wiff2, or other MSConvert-supported format)
- Acquisition method type (DDA, DIA_SWATH, PRM, COMMON)
- Output directory path
- Optional: mzPrecision parameter (float, default 0.0001)

## Outputs

- mzML or mzXML file (if conversion target is open XML format)
- Aird index file (.json) paired with Aird data file (.aird) in same directory with matching base name

## How to apply

Mount the vendor raw file into a Docker container with AirdPro (V5 or V6) and invoke the CLI interface via run-cli.sh with input file path (-i /data/input.raw) and output path (-o /data/output.mzML or .aird). AirdPro calls pwiz_bindings_cli.dll from ProteoWizard to perform the actual conversion; you must specify the acquisition method (DDA, DIA_SWATH, PRM, or COMMON) and optionally set mzPrecision (default 0.0001) to control numeric precision vs. file size. For batch conversions, submit ConvertJob objects via Redis (sourcePath, targetPath, type, mzPrecision) to the AirdPro distributed system. Verify output by confirming file presence, checking that output.mzML is valid XML, and validating that the Aird index (.json) and data (.aird) files reside in the same directory with matching base names.

## Related tools

- **AirdPro** (Primary GUI and CLI tool for converting vendor raw files to mzML or Aird format; orchestrates pwiz_bindings_cli.dll calls and manages conversion tasks) — https://github.com/CSi-Studio/AirdPro
- **pwiz_bindings_cli.dll** (Underlying ProteoWizard library that performs the actual vendor-to-standard format conversion called by AirdPro)
- **ProteoWizard** (Parent project providing mass spectrometry format conversion bindings and support for vendor file formats)
- **Docker Desktop for Mac / Docker Engine** (Container platform for running AirdPro in isolated, reproducible environment with Wine and .NET Framework 4.8)
- **Redis** (Message broker for distributed batch conversion: submit ConvertJob objects to Database0, key 'ConvertTask' for multi-node processing)
- **AirdSDK** (Secondary development library for reading Aird-format data; supports Java, C#, Python for downstream analysis) — https://github.com/CSi-Studio/Aird-SDK

## Examples

```
docker run --rm -v /path/to/vendor:/data airdpro:latest ./run-cli.sh -i /data/sample.raw -o /data/sample.mzML
```

## Evaluation signals

- Output file exists at specified path with correct file extension (.mzML, .mzXML, or .aird/.json pair).
- For mzML output: file is valid XML that parses without schema errors and contains expected spectrum and chromatogram elements.
- For Aird output: .json index file and .aird data file are present in the same directory with identical base names; .json is valid JSON structure.
- File size is reasonable relative to input (Aird compression typically achieves 30–50% reduction vs. uncompressed; mzML ~10–30% of raw).
- Acquisition method in output metadata matches the specified type (DDA, DIA_SWATH, PRM, COMMON); cross-check via schema validation or SDK read-back.

## Limitations

- Requires .NET Framework 4.8 and Wine on Linux/Mac; Windows native execution is simpler but not cross-platform.
- Conversion time scales with file size; very large ion-mobility or high-resolution datasets may require memory tuning (V6 addresses overflow issues but users must set resource limits in docker-compose.yml).
- Precision truncation (mzPrecision parameter) is lossy; set conservatively (≤0.0001) for untargeted metabolomics unless you have validated tolerance for your use case.
- Not all vendor instruments or acquisition modes are equally well-tested; MRM/SRM support was added in V5.1; PASEF mode for ion mobility added in V2.1.
- Batch conversion via Redis requires a running Redis server and careful JSON serialization of ConvertJob; network latency may affect large-scale distributed pipelines.

## Evidence

- [readme] AirdPro is a GUI client for conversion from vendor files to Aird files. AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project.: "AirdPro is a GUI client for conversion from vendor files to Aird files. AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project."
- [other] Invoke run-cli.sh with arguments specifying input file path (-i /data/input.raw) and output file path (-o /data/output.mzML). The container executes AirdPro's CLI interface, which calls pwiz_bindings_cli.dll from ProteoWizard to perform the conversion from vendor format to mzML.: "Invoke run-cli.sh with arguments specifying input file path (-i /data/input.raw) and output file path (-o /data/output.mzML). The container executes AirdPro's CLI interface, which calls"
- [readme] By using library from ProteoWizard MSConvert. AirdPro can convert all the vendor format that MSConvert supports to Aird format.: "By using library from ProteoWizard MSConvert. AirdPro can convert all the vendor format that MSConvert supports to Aird format."
- [readme] The redis key is 'ConvertTask', the value should be a Set data structure of a specific json model called 'ConvertJob'. String sourcePath //the vendor file path, like C:\vendor\test.raw String targetPath //the target output directory path, like D:\output Double mzPrecision = 0.0001 //the needed precision, the default value is 0.0001 String type='DDA' //the acquisition method of the vendor file.: "The redis key is 'ConvertTask', the value should be a Set data structure of a specific json model called 'ConvertJob'. String sourcePath //the vendor file path, String targetPath //the target output"
- [readme] Aird Index File and Aird Data File show be stored in the same directory with the same file name but with different suffix: "Aird Index File and Aird Data File show be stored in the same directory with the same file name but with different suffix"
- [other] Verify the output mzML file is present and is valid XML.: "Verify the output mzML file is present and is valid XML."
- [readme] Supporting MRM acquisition method. Supporting Wiff2 format.: "Supporting MRM acquisition method. Supporting Wiff2 format."
