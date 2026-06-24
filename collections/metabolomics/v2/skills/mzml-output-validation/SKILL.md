---
name: mzml-output-validation
description: Use when after running AirdPro's CLI conversion pipeline (run-cli.sh
  with -i and -o arguments) to confirm the vendor raw file conversion to mzML has
  succeeded.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - AirdPro V6
  - pwiz_bindings_cli.dll
  - ProteoWizard
  - Docker Engine / Docker Desktop for Mac
  techniques:
  - mass-spectrometry
  license_tier: restricted
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

# mzML output validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Verify that vendor raw files have been successfully converted to valid mzML format by checking file presence and XML schema compliance. This skill ensures the CLI-based conversion from vendor formats through ProteoWizard bindings has completed correctly and produced well-formed output.

## When to use

After running AirdPro's CLI conversion pipeline (run-cli.sh with -i and -o arguments) to confirm the vendor raw file conversion to mzML has succeeded. Apply this skill when the conversion process completes and you need to verify the output file is both present in the expected location and conforms to mzML XML structure before downstream processing.

## When NOT to use

- Input file is already known to be in mzML format from a trusted prior conversion — validation is redundant.
- You are converting to Aird format (the native AirdPro output) rather than mzML — use Aird-specific validation instead.
- The conversion process has not yet completed or the CLI command returned an error — validate only after successful command execution.

## Inputs

- output file path from AirdPro CLI invocation (e.g., /data/output.mzML)
- Docker container mount directory (/data)

## Outputs

- validation status (pass/fail)
- error log or exception message (if validation fails)
- confirmed valid mzML file ready for downstream analysis

## How to apply

After invoking run-cli.sh with the input vendor raw file path (-i /data/input.raw) and output mzML path (-o /data/output.mzML), check that the output file exists at the specified location in the Docker container's mounted /data directory. Then validate the file is well-formed XML by parsing its root element and schema structure; XML parsers will throw exceptions if the file is malformed or truncated. The conversion is successful only if both the file presence check and XML validity check pass, indicating the pwiz_bindings_cli.dll conversion mechanism correctly transformed the vendor format through ProteoWizard bindings to valid mzML.

## Related tools

- **AirdPro V6** (CLI conversion engine that calls pwiz_bindings_cli.dll to perform vendor-to-mzML conversion) — https://github.com/CSi-Studio/AirdPro
- **pwiz_bindings_cli.dll** (ProteoWizard library binding invoked by AirdPro to execute the actual vendor format conversion)
- **ProteoWizard** (Underlying framework providing vendor format parsing and mzML serialization)
- **Docker Engine / Docker Desktop for Mac** (Container runtime managing the isolated environment and file mounts for conversion execution)

## Examples

```
docker run --rm -v $(pwd):/data airdpro:latest bash -c 'run-cli.sh -i /data/input.raw -o /data/output.mzML && xmllint --noout /data/output.mzML && echo "Validation passed"'
```

## Evaluation signals

- Output file exists at the specified -o path in the mounted Docker /data directory
- File size is non-zero and greater than typical XML header overhead (~1 KB minimum)
- File parses as well-formed XML without namespace or schema validation errors
- mzML root element (<indexedmzML> or <mzML>) is present and contains expected sub-elements (spectrum, chromatogram, indexList)
- No truncation or corruption indicators in file tail (XML closing tags are present and properly nested)

## Limitations

- Validation checks only XML structure and presence; it does not verify spectral data accuracy, peak counts, or m/z/intensity calibration correctness.
- Vendor file format support depends on what ProteoWizard MSConvert supports — some proprietary formats or versions may fail silently or produce invalid conversions.
- Large files (gigabytes) may timeout during XML parsing if validation is run synchronously; consider asynchronous or streaming validation for production batch pipelines.
- The CLI conversion can complete without error even if the output mzML is incomplete or partial — file truncation is not always caught by the conversion exit code.

## Evidence

- [other] Vendor raw file conversion mechanism description: "AirdPro is based on pwiz_bindings_cli.dll from the ProteoWizard project and is written in C#, providing the underlying mechanism for converting vendor files through ProteoWizard bindings."
- [other] CLI invocation workflow for conversion: "Invoke run-cli.sh with arguments specifying input file path (-i /data/input.raw) and output file path (-o /data/output.mzML). The container executes AirdPro's CLI interface, which calls"
- [other] Output validation requirement: "Verify the output mzML file is present and is valid XML."
- [readme] mzML conversion support in AirdPro: "By using library from ProteoWizard MSConvert. AirdPro can convert all the vendor format that MSConvert supports to Aird format."
- [other] Docker container data directory usage: "Mount the input vendor raw file into the Docker container's /data directory."
