---
name: performance-benchmark-execution
description: Use when you have access to a tool with published performance claims (e.g., '~20 seconds on M2 Macbook') and want to validate those claims on your own hardware, or you need to benchmark processing speed before committing to a tool for production use on similarly sized datasets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3445
  edam_topics:
  - http://edamontology.org/topic_3674
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.10.15.682422v1
  all_source_dois:
  - 10.1101/2025.10.15.682422v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# performance-benchmark-execution

## Summary

Execute and measure processing speed of a scientific tool on a standardized dataset to validate claimed performance metrics. This skill involves loading a large-scale dataset (e.g., 5 GB imzML file with 2500 ion images), timing end-to-end execution, and recording system specifications to verify reproducibility of performance claims.

## When to use

You have access to a tool with published performance claims (e.g., '~20 seconds on M2 Macbook') and want to validate those claims on your own hardware, or you need to benchmark processing speed before committing to a tool for production use on similarly sized datasets. Use this skill when the tool's speed is a critical factor in your workflow decision.

## When NOT to use

- The tool or dataset is proprietary and cannot be obtained or legally executed on your hardware.
- Your hardware or OS is fundamentally incompatible with the tool (e.g., tool requires M2 Macbook but you only have Windows; tool requires specific GPU not available).
- The published benchmark is qualitative or vague ('fast', 'reasonable') rather than quantitative, making reproducibility criteria unclear.

## Inputs

- Large-scale scientific data file matching published benchmark specification (e.g., 5 GB imzML with 2500 ion images)
- Installed binary or source of the tool to be benchmarked
- Target hardware platform (documented CPU model, RAM, OS version)

## Outputs

- Wall-clock execution time (seconds) for the core operation
- System specification record (OS version, CPU model, tool version, RAM)
- Comparison report (measured time vs. published benchmark)
- Variance assessment and attribution (hardware/OS/version factors)

## How to apply

1. Obtain or prepare a test dataset matching the scale and format of the published benchmark (e.g., 5 GB imzML file with 2500 ion images for LipidQMap). 2. Install the tool on the target hardware matching or documenting deviations from the original benchmark environment (e.g., M2 Macbook, specific macOS version, RAM). 3. Launch the tool and initiate the core operation (e.g., file open, import, and quantification) while measuring wall-clock elapsed time from initiation to completion. 4. Record the measured execution time and document all system specifications (hardware model, CPU, macOS/OS version, RAM, tool version). 5. Compare measured time against the published benchmark and assess whether variance is within acceptable tolerance (typically ±10–15% for I/O-bound operations). 6. Report discrepancies and their likely causes (hardware differences, OS version, tool version changes).

## Related tools

- **LipidQMap** (target tool whose performance is being benchmarked; executes imzML file import, ion image quantification, and isotope correction) — https://github.com/swinnenteam/LipidQMap

## Evaluation signals

- Measured wall-clock time is within ±15% of published benchmark (e.g., 17–23 seconds if benchmark is ~20 seconds).
- System specifications are fully documented and match or are clearly noted as deviating from the benchmark environment.
- Tool completes without errors or crashes during the measured operation (file opens, imports complete, ion images are quantified).
- Execution time is consistent across repeated runs (measure at least 2–3 runs to exclude outliers from background OS activity).
- Output (quantified ion images, exported data) matches expected structure and format (e.g., HDF5 containers following Cardinal::HDF5 conventions for LipidQMap).

## Limitations

- Benchmark reproducibility depends heavily on matching hardware (CPU model, RAM capacity) and OS version; runs on different hardware will naturally exhibit variance.
- Wall-clock time is sensitive to background OS activity, file system state, and disk I/O contention; isolated runs in a controlled environment will be more reproducible.
- Published benchmarks may be measured on optimized or pre-release hardware/software configurations not representative of typical end-user setups.
- Tool version differences (even minor updates) can affect performance; always record and compare tool versions explicitly.
- Dataset size and structure matter significantly; a 5 GB imzML file with different ion density or spectral complexity may exhibit different timings than the reference benchmark.

## Evidence

- [intro] LipidQMap achieves fast processing times, opening a 5 GB imzML file and importing and quantifying 2500 ion images in about 20 seconds on an M2 Macbook: "opening a 5 GB imzML file and importing and quantifying 2500 ion images takes about 20 seconds on an M2 Macbook"
- [other] Workflow includes obtaining a test file, installing on M2 hardware, launching and loading the file via GUI while measuring elapsed time, recording execution time and system specs, and comparing against benchmark: "1. Obtain or prepare a 5 GB imzML test file with 2500 ion images (or use the reference file cited in the README if available). 2. Install LipidQMap on an M2 Macbook (or equivalent M2-based system)"
- [readme] LipidQMap is available for Windows 10 and Mac with Apple silicon M1 and up: "LipidQMap is available for Windows 10 (and up) and Mac (Apple silicon, M1 and up)."
- [readme] LipidQMap processes imzML files and can open multiple imzML files simultaneously: "Works on imzML data files and can open multiple imzML files simultaneously."
