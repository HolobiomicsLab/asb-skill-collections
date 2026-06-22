---
name: cli-invocation-with-file-path-arguments
description: Use when you have vendor raw mass spectrometry data files (e.g., .raw, .d, .wiff2 formats) that must be converted to mzML or Aird format, and you need to automate the conversion in a batch workflow, Docker container, or non-interactive environment.
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
  - Docker
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cli-invocation-with-file-path-arguments

## Summary

Invoke a command-line interface tool with input and output file path arguments to perform format conversion. This skill is essential for batch processing and automation workflows where vendor mass spectrometry raw files must be converted to standardized formats (mzML or Aird) without manual GUI interaction.

## When to use

Use this skill when you have vendor raw mass spectrometry data files (e.g., .raw, .d, .wiff2 formats) that must be converted to mzML or Aird format, and you need to automate the conversion in a batch workflow, Docker container, or non-interactive environment. Typical triggers: availability of a vendor file path, requirement to convert multiple files programmatically, or need to integrate conversion into a larger data processing pipeline.

## When NOT to use

- Input file is already in mzML or Aird format and no conversion is needed.
- Vendor raw file format is not supported by ProteoWizard (e.g., proprietary formats from vendors not yet integrated into ProteoWizard).
- GUI-based interactive conversion with real-time parameter tuning or preview is required; use GUI Version instead of CLI for daily interactive use.

## Inputs

- vendor raw mass spectrometry data file (e.g., .raw, .d, .wiff2 format)
- input file path string (absolute or relative)
- output file path string (absolute or relative)
- optional acquisition method type (DDA, DIA_SWATH, PRM, COMMON)

## Outputs

- mzML format file (XML-based open format)
- Aird data file (.aird binary) with accompanying .json index file
- exit code indicating success (0) or failure (non-zero)

## How to apply

Mount or stage the input vendor raw file in an accessible directory (e.g., /data/input.raw within a Docker container or a local filesystem path). Invoke the AirdPro CLI entry point (run-cli.sh on Unix/Linux, AirdPro.exe on Windows) with two required file path arguments: -i (or --input) pointing to the source vendor raw file, and -o (or --output) pointing to the desired output location and filename (e.g., /data/output.mzML). The CLI tool invokes the underlying pwiz_bindings_cli.dll ProteoWizard binding, which auto-detects the vendor format and performs format-specific conversion. Optionally, include additional parameters such as -t or --type to specify acquisition method (DDA, DIA_SWATH, PRM, or COMMON) if not auto-detected. Wait for the process to complete and verify the output file is present and contains valid XML (for mzML) or valid .json index + .aird data file pair (for Aird format).

## Related tools

- **AirdPro V6** (CLI wrapper and conversion orchestrator that wraps pwiz_bindings_cli.dll; accepts file path arguments and manages format detection and conversion execution) — https://github.com/CSi-Studio/AirdPro
- **pwiz_bindings_cli.dll** (Underlying ProteoWizard C# binding library that performs vendor-to-standard format translation; invoked by AirdPro CLI)
- **ProteoWizard** (Framework providing vendor file format readers and mzML/mzXML writers; pwiz_bindings_cli.dll is derived from this project)
- **Docker** (Container runtime environment for executing CLI conversion in isolated, reproducible, cross-platform context; mounts vendor file into /data directory)

## Examples

```
./run-cli.sh -i /data/input.raw -o /data/output.mzML -t DDA
```

## Evaluation signals

- Output file exists at the specified output path with non-zero file size.
- For mzML output: parse the file as XML and verify presence of required elements (<mzML>, <run>, <spectrumList>).
- For Aird output: verify both .json index file and .aird data file are present in the same directory with matching base filename.
- CLI process returns exit code 0 (success) with no error messages on stderr.
- Conversion completes within expected time bounds (typically seconds to minutes depending on file size); no timeout or hanging process.

## Limitations

- Vendor file format must be supported by ProteoWizard; unsupported formats will fail with format-detection or binding error.
- Windows .NET Framework 4.7.2 or higher is required when running AirdPro.exe on Windows; .NET 4.8 recommended.
- Large vendor files (>10 GB) may exhaust memory during conversion; v6.0.0 includes memory overflow improvements but users should monitor system resources.
- Acquisition method auto-detection may fail for uncommon or hybrid acquisition modes; explicit -t/--type parameter may be needed.
- Wine compatibility on Linux/macOS may introduce performance overhead or incompatibility with certain vendor drivers or Windows-specific libraries.

## Evidence

- [other] Invoke run-cli.sh with arguments specifying input file path (-i /data/input.raw) and output file path (-o /data/output.mzML). The container executes AirdPro's CLI interface, which calls pwiz_bindings_cli.dll from ProteoWizard to perform the conversion from vendor format to mzML.: "Invoke run-cli.sh with arguments specifying input file path (-i /data/input.raw) and output file path (-o /data/output.mzML). The container executes AirdPro's CLI interface, which calls"
- [readme] AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project.: "AirdPro is written in C# and is based on pwiz_bindings_cli.dll from the ProteoWizard project."
- [readme] By using library from ProteoWizard MSConvert. AirdPro can convert all the vendor format that MSConvert supports to Aird format.: "By using library from ProteoWizard MSConvert. AirdPro can convert all the vendor format that MSConvert supports to Aird format."
- [readme] String sourcePath //the vendor file path, like C:\vendor\test.raw; String targetPath //the target output directory path, like D:\output: "String sourcePath //the vendor file path, like C:\vendor\test.raw; String targetPath //the target output directory path, like D:\output"
- [other] Verify the output mzML file is present and is valid XML.: "Verify the output mzML file is present and is valid XML."
