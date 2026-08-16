---
name: raw-data-throughput-benchmarking
description: Use when when you have a raw mass spectrometry file (e.g., Thermo Orbitrap .raw) and need to establish the measured throughput of a spectral reading function (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - rawrr
  - RawFileReader
  - .NET 8.0
  - .NET 8.0 Runtime
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1101/2020.10.30.362533
  title: rawrr
- doi: 10.1021/acs.jproteome.0c00866
  title: ''
evidence_spans:
- rawrr::readSpectrum
- Our .NET 8.0 [@dotnet] precompiled wrapper methods are bundled, including the runtime, in the `r BiocStyle::Biocpkg('rawrr')` executable file
- The extracted information is written to a temporary location on the harddrive, read back into memory and parsed into `R` objects using RawFileReader API
- 'ThermoFisher.CommonCore dlls can be obtained through: https://github.com/thermofisherlsms/RawFileReader'
- In case you prefer to compile `rawrr.exe` from C# source code, please install the .NET 8.0
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rawrr
    doi: 10.1101/2020.10.30.362533
    title: rawrr
  dedup_kept_from: coll_rawrr
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

# raw-data-throughput-benchmarking

## Summary

Measure the spectra-per-second throughput of raw mass spectrometry data reading operations using controlled benchmark experiments with varying scan counts. This skill quantifies I/O and parsing performance on proprietary binary formats (e.g., Thermo .raw files) to validate data access layer speed and guide pipeline optimization decisions.

## When to use

When you have a raw mass spectrometry file (e.g., Thermo Orbitrap .raw) and need to establish the measured throughput of a spectral reading function (e.g., rawrr::readSpectrum) in spectra per second to verify performance meets expected baselines, compare implementations, or predict processing time for large datasets.

## When NOT to use

- Input is already a processed feature table or peak list; benchmarking is for raw binary file access, not downstream statistical analysis.
- The raw file format is not supported by the installed library (e.g., attempting to benchmark rawrr on non-Thermo formats without appropriate backend).
- Performance is not a primary concern; benchmarking is overhead-heavy and unnecessary if only correctness of a single read operation is needed.

## Inputs

- Thermo .raw file (binary proprietary format containing FTMS spectra)
- Installed raw data access library (e.g., rawrr R package)
- Required runtime (e.g., .NET 8.0 for rawrr)
- Target reading function name (e.g., 'readSpectrum')

## Outputs

- Throughput metric in spectra per second
- Benchmark runtime summary (total seconds, per-run times)
- Performance comparison table or report

## How to apply

Install and verify the data access library and its runtime dependencies (e.g., rawrr package, .NET 8.0 runtime via rawrr::installRawrrExe()). Load a representative raw file (e.g., the provided QC standard 20181113_010_autoQC01.raw, containing Fourier-transformed Orbitrap FTMS data). Execute the library's built-in benchmark function (e.g., rawrr:::.benchmark) targeting the reading function of interest, passing multiple runs with varying randomly generated scan ID counts. Capture the returned spectra-per-second metric from each run. Record the overall runtime and compute summary statistics (mean, variance) across runs. Compare measured throughput against reference values in the literature or prior implementations to assess consistency and identify performance regressions.

## Related tools

- **rawrr** (R package that wraps RawFileReader .NET assembly and provides the benchmark infrastructure (rawrr:::.benchmark function) and readSpectrum() target function) — https://github.com/fgcz/rawrr
- **RawFileReader** (Thermo Fisher Scientific .NET assembly that performs low-level binary file I/O and spectral data extraction, invoked via C# wrapper methods by rawrr) — https://github.com/thermofisherlsms/RawFileReader
- **.NET 8.0 Runtime** (Required runtime environment for executing compiled C# wrapper methods that interface with RawFileReader assembly)

## Examples

```
rawrr::installRawrrExe(); S <- rawrr::readSpectrum(rawfile = '20181113_010_autoQC01.raw', scan = 1:100); bench <- rawrr:::.benchmark(fun = rawrr::readSpectrum, rawfile = '20181113_010_autoQC01.raw'); print(bench)
```

## Evaluation signals

- Benchmark completes without errors and returns a numeric throughput value (spectra/second) for each run.
- Measured throughput is consistent across multiple runs with the same scan count (low variance), indicating stable I/O and parsing performance.
- Measured throughput aligns with or exceeds published reference values from the rawrr paper (task_002 finding) or prior benchmark reports, confirming no performance regression.
- Throughput scales predictably with scan count (higher scans → higher absolute spectra/second or stable rate), ruling out systematic bottlenecks.
- Total benchmark runtime and per-run timings are reasonable (sub-second to seconds) and do not indicate excessive resource contention or GC pauses.

## Limitations

- Benchmark results are hardware-dependent (CPU, disk I/O speed, RAM); throughput cannot be directly compared across different systems without normalization.
- Windows systems require decimal symbol configuration as '.' for proper data extraction, which may affect reproducibility if misconfigured.
- The benchmark is tied to a specific library version and runtime (.NET 8.0); upgrading either may alter throughput metrics, complicating longitudinal comparisons.
- Benchmark uses randomly generated scan IDs; real-world access patterns (sequential vs. random, clustered vs. sparse) may exhibit different throughput due to caching and I/O locality effects.

## Evidence

- [other] Execute rawrr:::.benchmark function with rawrr::readSpectrum as the target function, which invokes compiled C# wrapper methods via system2 call to interact with the RawFileReader .NET assembly.: "Execute rawrr:::.benchmark function with rawrr::readSpectrum as the target function, which invokes compiled C# wrapper methods via system2 call to interact with the RawFileReader .NET assembly."
- [other] The benchmark experiment using rawrr::readSpectrum demonstrates throughput measured in spectra per second across multiple runs with varying numbers of randomly generated scan IDs, with overall runtime totaling approximately 0.5 seconds.: "The benchmark experiment using rawrr::readSpectrum demonstrates throughput measured in spectra per second across multiple runs with varying numbers of randomly generated scan IDs, with overall"
- [other] Load the example raw file 20181113_010_autoQC01.raw (Fourier-transformed Orbitrap FTMS data from a Q Exactive HF instrument) using rawrr package initialization.: "Load the example raw file 20181113_010_autoQC01.raw (Fourier-transformed Orbitrap FTMS data from a Q Exactive HF instrument) using rawrr package initialization."
- [other] Install the rawrr executable and verify .NET 8.0 runtime availability via rawrr::installRawrrExe().: "Install the rawrr executable and verify .NET 8.0 runtime availability via rawrr::installRawrrExe()."
- [methods] Specifically, `R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call: "Specifically, `R` functions requesting access to data stored in binary raw files (reader family functions listed in Table 1) invoke compiled `C#` wrapper methods using a system call"
- [discussion] On Windows, the decimal symbol has to be configured as a '.'!: "On Windows, the decimal symbol has to be configured as a '.'!"
