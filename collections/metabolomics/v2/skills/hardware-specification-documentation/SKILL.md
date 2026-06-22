---
name: hardware-specification-documentation
description: Use when releasing or evaluating scientific software with claimed performance benefits, particularly when the software processes large datasets (e.g., multi-gigabyte files) or when execution speed is marketed as a key feature.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0337
  edam_topics:
  - http://edamontology.org/topic_3676
  - http://edamontology.org/topic_0092
  tools:
  - LipidQMap
derived_from:
- doi: 10.1101/2025.10.15.682422v1
  title: LipidQMap
evidence_spans:
- LipidQMap writes MSI exports as HDF5 containers
- LipidQMap writes MSI exports as HDF5 containers that follow the [`Cardinal::HDF5`](https://cardinalmsi.org) conventions.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidqmap_cq
    doi: 10.1101/2025.10.15.682422v1
    title: LipidQMap
  dedup_kept_from: coll_lipidqmap_cq
schema_version: 0.2.0
---

# hardware-specification-documentation

## Summary

Document and validate the hardware specifications and performance characteristics of scientific software on target platforms, establishing reproducible benchmarks for computational requirements and execution time. This skill ensures that users can assess whether their own hardware meets necessary performance thresholds and can compare results across different system configurations.

## When to use

Apply this skill when releasing or evaluating scientific software with claimed performance benefits, particularly when the software processes large datasets (e.g., multi-gigabyte files) or when execution speed is marketed as a key feature. This is essential for users deciding whether to adopt the tool and for reproducing or validating performance claims across different hardware platforms.

## When NOT to use

- When testing on non-representative or artificial test data that does not match typical user workflows
- When only measuring partial operations (e.g., import time alone without quantification) rather than the complete end-to-end workflow
- When hardware specifications are not fully documented or vary significantly from the claimed target platform (e.g., older M1 Macs or non-Apple silicon systems when M2 is specified)

## Inputs

- Large imzML data file (5 GB example given)
- Target hardware platform specification (processor model, RAM, OS version)
- LipidQMap software installed and ready to launch

## Outputs

- Benchmark timing measurement (wall-clock seconds from file open to quantification completion)
- Documented system specifications (macOS version, RAM, CPU model, software version)
- Performance comparison report against claimed benchmark

## How to apply

Obtain or prepare representative test data (in this case a 5 GB imzML file with 2500 ion images). Install the software on the target hardware platform (e.g., M2 Apple silicon Macbook). Launch the software via its standard GUI and perform the full workflow (file open, import, and quantification) while measuring elapsed wall-clock time from initiation to completion. Record the measured execution time and document all relevant system specifications including macOS version, installed RAM, CPU model, and software version number. Compare measured performance against the claimed benchmark and publish this benchmark prominently in user-facing documentation (README, release notes) so users can set realistic expectations.

## Related tools

- **LipidQMap** (The software being benchmarked; users launch it via GUI to perform imzML file open, ion image import, and quantification operations) — https://github.com/swinnenteam/LipidQMap

## Evaluation signals

- Measured execution time for the complete workflow (open + import + quantify) matches or is comparable to the claimed ~20 second benchmark on M2 hardware
- All system specifications are fully documented: macOS version, RAM capacity, CPU model (M2), and LipidQMap version number are recorded
- Test uses a representative dataset: a 5 GB imzML file with 2500 ion images, matching the specification from the README claim
- Benchmark is reproducible: the same workflow performed multiple times on the same hardware yields consistent timing results (low variance)
- Performance claim is accessible to end users: the benchmark and system requirements are documented in the README or release notes, not hidden in supplementary materials

## Limitations

- Benchmark is hardware-specific: performance on older M1 Macs, Intel-based Macs, or Windows systems may differ significantly and requires separate testing
- Test data may not represent all possible imzML file structures or sizes; larger or more complex files may exhibit different performance characteristics
- Wall-clock time measurements can be affected by background system processes, disk I/O variability, and other transient factors; multiple runs and statistical summarization are recommended
- The README states 'LipidQMap is available for Windows 10 (and up) and Mac (Apple silicon, M1 and up)' but the benchmark explicitly cites M2; performance on M1 or Windows systems is not documented

## Evidence

- [readme] opening a 5 GB imzML file and importing and quantifying 2500 ion images takes about 20 seconds on an M2 Macbook: "Is fast, opening a 5 GB imzML file and importing and quantifying 2500 ion images takes about 20 seconds on an M2 Macbook."
- [other] The research question explicitly asks for processing speed measurement: "What is the processing speed of LipidQMap when opening a 5 GB imzML file and importing and quantifying 2500 ion images on an M2 Macbook?"
- [other] The workflow requires recording system specifications during benchmark testing: "Document system specifications (macOS version, RAM, CPU model, LipidQMap version) and report timing result."
- [readme] Installation instructions specify Apple silicon platforms as the target: "LipidQMap is available for Windows 10 (and up) and Mac (Apple silicon, M1 and up)."
- [other] The workflow involves measuring elapsed wall-clock time from file open to completion: "measuring elapsed wall-clock time from file open initiation to completion of import and quantification steps"
