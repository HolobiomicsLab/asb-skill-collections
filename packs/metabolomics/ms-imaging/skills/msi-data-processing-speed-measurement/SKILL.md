---
name: msi-data-processing-speed-measurement
description: Use when when you need to validate that MSI software (e.g., LipidQMap) achieves documented processing speeds on your target hardware, or when you need to establish a performance baseline before deploying the software for high-throughput imaging studies.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - LipidQMap
  techniques:
  - MS-imaging
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# msi-data-processing-speed-measurement

## Summary

Measure the end-to-end processing latency of mass spectrometry imaging (MSI) software when opening large imzML files and performing ion image import and quantification. This skill benchmarks real-world performance on target hardware to verify that processing speed meets documented specifications.

## When to use

When you need to validate that MSI software (e.g., LipidQMap) achieves documented processing speeds on your target hardware, or when you need to establish a performance baseline before deploying the software for high-throughput imaging studies. Applicable when you have access to large imzML test files (e.g., 5 GB with 2500+ ion images) and want to measure wall-clock time from file open initiation through quantification completion.

## When NOT to use

- Input imzML file is significantly smaller (<1 GB) or has fewer ion images (<500), making benchmark comparison invalid.
- Software is already running other processes that consume substantial CPU/I/O resources, invalidating the isolated performance measurement.
- Hardware does not match the documented benchmark platform (e.g., older Intel Mac or non-M-series Apple silicon), making direct time comparison misleading.

## Inputs

- imzML data file (≥5 GB) with 2500+ ion images
- System hardware specifications (CPU, RAM, macOS version)
- LipidQMap software installation (version ≥ 0.1.0)

## Outputs

- Wall-clock execution time (seconds) for file open + import + quantification
- Performance report comparing measured time to documented benchmark
- System specification log (macOS version, RAM, CPU model, software version)

## How to apply

Install the target MSI software on the target hardware (e.g., M2 Macbook) and prepare or obtain a representative large imzML file matching the documented benchmark (e.g., 5 GB, 2500 ion images). Launch the software GUI and open the imzML import dialog. Configure import parameters: select the imzML file(s), specify ion mode (positive/negative), set mass error tolerance (in ppm; default ~5 ppm), select bin size (5 mDa for TOF, lower for higher resolution), enable isotope correction and online calibration as needed, and choose the quantitation database. Measure elapsed wall-clock time from the moment 'Import Data' is clicked until all ion images are imported and quantified. Record the measured time and document system specifications (macOS version, RAM, CPU model, software version). Compare measured time against the reported benchmark; processing that completes within ±20% of the documented value indicates correct performance. If time deviates significantly, investigate system load, file I/O throughput, and software version.

## Related tools

- **LipidQMap** (MSI quantitation software whose processing speed is measured during this skill; provides imzML file import, ion image extraction, isotope correction, and quantitation workflows) — https://github.com/swinnenteam/LipidQMap

## Evaluation signals

- Measured end-to-end time (from file open click to quantification complete) is within ±20% of the documented ~20 second benchmark for 5 GB imzML + 2500 ion images on M2 hardware.
- All 2500 ion images are successfully imported and quantified (verify by checking the species table row count and ensuring no import errors or timeouts occurred).
- System specifications (macOS version, RAM, CPU model, LipidQMap version) are documented and consistent with the benchmark platform (M1/M2 Macbook with ≥8 GB RAM).
- Wall-clock time measurement is isolated: no concurrent high-CPU or high-I/O processes are active during the test run (check Activity Monitor before/after test).
- File import dialog settings (mass error tolerance, bin size, isotope correction, quantitation database) are configured consistently with the documented benchmark parameters.

## Limitations

- Benchmark time (20 seconds) is specific to M-series Apple silicon Macbooks; performance on Windows 10/11 systems or older Intel Macs may differ significantly.
- The test file must contain exactly 2500 ion images; smaller or larger datasets may not yield comparable timings.
- Background system load, available RAM, and I/O throughput variability can introduce ±10–15% variance in measurements even on identical hardware.
- No changelog is available for LipidQMap, so version-to-version performance regressions or improvements cannot be tracked from release notes.
- Online calibration and advanced isotope correction algorithms may increase total processing time beyond the baseline benchmark.

## Evidence

- [readme] LipidQMap is a program to support accurate quantitation of Mass Spectrometry Imaging data.: "LipidQMap is a program to support accurate quantitation of Mass Spectrometry Imaging data."
- [readme] Processing speed benchmark for 5 GB imzML file on M2 hardware.: "Is fast, opening a 5 GB imzML file and importing and quantifying 2500 ion images takes about 20 seconds on an M2 Macbook."
- [readme] Install LipidQMap from GitHub releases for Windows and Mac with M1/M2 processors.: "LipidQMap is available for Windows 10 (and up) and Mac (Apple silicon, M1 and up)."
- [readme] Workflow for opening and importing imzML files with configurable parameters.: "In the imzML import dialog, click on the "Open Files" button to select one or more imzML files. Select if the file contains positive or negative ion mode data. Select the maximum tolerated mass error"
- [other] Task specification for reproducing the 5 GB imzML processing benchmark.: "Obtain or prepare a 5 GB imzML test file with 2500 ion images (or use the reference file cited in the README if available). Launch LipidQMap and load the 5 GB imzML file via the GUI, measuring"
