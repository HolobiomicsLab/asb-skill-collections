# Workflow Challenge: `coll_rawrr_workflow`


> rawrr is an R package providing direct access to proprietary Thermo Fisher Scientific Orbitrap mass spectrometry data via vendor APIs, enabling modular end-to-end proteomics analysis pipelines in R without format conversion. The package wraps RawFileReader .NET assemblies through a two-layer architecture and demonstrates bottom-up proteomics applications including spectrum analysis and retention time calibration.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

This work presents rawrr, an R package that provides direct access to binary Thermo Fisher Scientific Orbitrap raw data files by wrapping the vendor-supplied RawFileReader API through compiled C# wrapper methods. The package implements S3 objects (rawrrSpectrum, rawrrChromatogram) and reader functions (readFileHeader, readSpectrum, readChromatogram, readIndex, readTrailer) that extract spectral and chromatographic data without requiring conversion to exchange formats. Two use cases demonstrate practical application: (1) direct spectrum analysis of a 40.5-minute parallel reaction monitoring (PRM) run on a Q Exactive HF yielded scan 9594 with resolving power of 30,000 at 200 m/z and AGC injection time of 2.8 ms; y-ion signals for the doubly-charged LGGNEQVTR peptide were tens to hundreds of times above noise. (2) iRT regression using 11 reference peptides extracted via readChromatogram showed highly linear retention time behavior (high R²) across a 20-minute C18 gradient, with consecutive PRM scans consistently spaced 22 scans apart. Benchmark testing of readSpectrum throughput across multiple runs with random scan IDs demonstrated spectra-per-second performance with total runtime of approximately 0.5 seconds. The package architecture comprises an R layer invoking compiled C# wrapper methods via system calls, with data written to temporary storage and parsed back into R objects.

## Research questions

- Does the linear regression model fitted to iRT peptide retention times (rtFittedAPEX ~ iRTscore) demonstrate highly linear RT behavior as indicated by R-squared value?
- What is the measured throughput of rawrr::readSpectrum in spectra per second when benchmarked on the sample raw file provided with the package?
- Does rawrr::readSpectrum successfully extract scan 9594 from the raw file with reported Orbitrap parameters (resolving power of 30,000 at 200 m/z and AGC injection time of 2.8 ms) and signal-to-noise characteristics consistent with high-quality peptide fragmentation?
- Does the parallel reaction monitoring (PRM) acquisition in the example raw file maintain consistent scan spacing across all cycles targeting the LGGNEQVTR++ precursor ion?
- Can the rawrr package's internal assembly dispatch functions (rawrr:::.rawrrAssembly() and rawrr:::.getRawrrAssemblyVersion()) successfully retrieve the assembly path and version string without requiring a raw data file as input?

## Methods overview

Retrieve the public raw LC-MS file 20181113_010_autoQC01.raw from MassIVE (MSV000086542) and verify file integrity. Read file header metadata using rawrr::readFileHeader() to confirm instrument configuration and run time range. Extract precursor m/z chromatograms for known iRT peptides using rawrr::readChromatogram() with type='xic', mass tolerance 10 ppm, and MS-level filter. Fit intensity traces within each rawrrChromatogram object to identify retention time at peak maximum (rtFittedAPEX) for each iRT standard. Construct and fit linear regression model lm(rtFittedAPEX ~ iRTscore) using extracted retention times and reference iRT scores. Validation: Report R-squared value; confirm R² ≥ 0.99 to establish highly linear retention-time behavior as reported in the paper. References: source article (DOI: 10.1021/acs.jproteome.0c00866); MSV000086542 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000086542) Install rawrr package and verify .NET 8.0 runtime availability. Load example Orbitrap raw file (20181113_010_autoQC01.raw) containing centroided FTMS and HCD MS2 spectra. Execute rawrr:::.benchmark using rawrr::readSpectrum, which triggers C# wrapper method invocation via system call to RawFileReader assembly. Capture measured spectra-per-second throughput from benchmark execution output. Validation: Confirm reported throughput metric is present and numerically reasonable (consistent with paper's reported performance under identical experimental conditions). References: source article (DOI: 10.1021/acs.jproteome.0c00866); MSV000086542 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000086542) Load raw file 20181113_010_autoQC01.raw (Thermo Fisher Q Exactive HF, Orbitrap FTMS) from MassIVE MSV000086542. Call rawrr::readSpectrum(scan=9594) to invoke C# wrapper and RawFileReader API, returning centroided spectrum object with 119 metadata items. Extract instrumental parameters (resolving power at 200 m/z, AGC target, injection time) from spectrum metadata and verify against reported hardware specifications. Parse m/z and intensity arrays; identify y-ion fragments by theoretical m/z matching for peptide LGGNEQVTR. Compute signal-to-noise ratio for each y-ion relative to local baseline and confirm all exceed tens-to-hundreds counts above noise. Validation: Confirm resolving power = 30,000, injection time = 2.8 ms, and all y-ion SNR ≥ 10:1 (tens of counts above baseline for high-quality MS/MS data). References: source article (DOI: 10.1021/acs.jproteome.0c00866); MSV000086542 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000086542) Install and initialize the rawrr package with compiled C# wrapper methods bound to the RawFileReader .NET assembly. Invoke rawrr::readIndex() to extract the complete scan metadata index from the binary .raw file via system call to the managed C# layer. Parse the scanType field to identify and filter rows matching the PRM acquisition pattern (fixed precursor m/z and HCD collision energy). Compute inter-scan deltas as the difference between consecutive scan numbers in the filtered PRM subset. Validate that all deltas equal 22 scans, confirming single-cycle consistency across the acquisition run. Validation: Pass criterion is 100% of observed inter-scan deltas equal 22 scans; any deviation flags acquisition irregularity. References: source article (DOI: 10.1021/acs.jproteome.0c00866); MSV000086542 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000086542) Load the rawrr R package into the R environment Call the internal function rawrr:::.rawrrAssembly() to retrieve the file system path to the bundled .NET 8.0 assembly executable Validate that the returned path exists and points to rawrr.exe Call the internal function rawrr:::.getRawrrAssemblyVersion() to retrieve the version metadata of the managed assembly Verify that a non-empty version string is returned Validation: Both accessor functions execute without error and return expected output types (path string and version string) without requiring a raw data file input, confirming the internal dispatch mechanism is operational References: source article (DOI: 10.1021/acs.jproteome.0c00866); MSV000086542 (https://massive.ucsd.edu/ProteoSAFe/dataset.jsp?accession=MSV000086542)

**Domain:** proteomics

**Techniques:** quality-control

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The rawrr package provides access to proprietary Thermo Fisher Scientific Orbitrap instrument data as a stand-alone R package or serves as a backend for the Bioconductor Spectra package. _[grounded: sys_rawrr]_
- **(finding)** rawrr wraps the functionality of the RawFileReader .NET assembly. _[grounded: sys_rawrr]_
- **(finding)** Existing proteomics libraries for R mainly support high-level statistical analysis once raw measurement data has undergone extensive preprocessing and aggregation by external software tools.
- **(finding)** High-throughput genomic data analysis is primarily conducted in R due to the Bioconductor project.
- **(finding)** The rawrr implementation consists of two language layers: a top R layer and a hidden C# layer. _[grounded: sys_rawrr]_
- **(finding)** R functions requesting access to raw file data invoke compiled C# wrapper methods using a system call.
- **(finding)** Extracted information is written to a temporary location on the hard drive, read back into memory and parsed into R objects.
- **(finding)** The rawrr package implements S3 objects named rawrrSpectrum and rawrrChromatogram to represent mass spectra and mass chromatograms. _[grounded: sys_rawrr]_
- **(finding)** The content of rawrrSpectrum instances partially depends on the instrument model and installed instrument control software version. _[grounded: comp_rawrrspectrum]_
- **(finding)** The example file 20181113_010_autoQC01.raw contains Fourier-transformed Orbitrap spectra recorded on a Thermo Fisher Scientific Q Exactive HF mass spectrometer in positive mode. _[grounded: tool_spectra]_
- **(finding)** MS2 spectra in the example file were generated by HCD fragmentation at normalized collision energy of 27. _[grounded: tool_spectra]_
- **(finding)** The analyzed sample consisted of the iRT peptide mix in a tryptic BSA digest separated using a 20 min linear gradient on C18 reversed-phase material. _[grounded: comp_irt_peptides]_
- **(finding)** The example file is part of the MassIVE dataset MSV000086542. _[grounded: ds_msv000086542]_
- **(finding)** The readFileHeader function returns a simple R object of type list containing meta information from a raw file header. _[grounded: tool_readfilehead]_
- **(finding)** The readSpectrum function returns a rawrrSpectrum object or rawrrSpectrumSet. _[grounded: comp_rawrrspectrum]_
- **(finding)** The Orbitrap detector offers high-resolution accurate mass data on a time scale compatible with chromatographic analysis. _[grounded: comp_orbitrap]_
- **(finding)** Analyzing Orbitrap data in R prior to rawrr has only been possible after raw data conversion to exchange formats like mzML. _[grounded: sys_rawrr]_
- **(finding)** Conversion of raw data to exchange formats is accompanied by a loss of Orbitrap-specific information. _[grounded: comp_orbitrap]_
- **(finding)** Scan 9594 was acquired using a transient of 64 ms, equal to a resolving power of 30,000 at 200 m/z.
- **(finding)** Scan 9594 was acquired with an AGC target of 1e5 elementary charges.
- **(finding)** The API provides 119 data items for the scan shown in the example, covering ion optics settings, mass calibration, and other diagnostic data.
- **(finding)** For the scan example, the C-trap collected 100,000 charges within 2.8 milliseconds.
- **(finding)** Orbitrap detectors follow the relationship S/N ∝ charges · √R. _[grounded: comp_orbitrap]_
- **(finding)** The readChromatogram function can return a rawrrChromatogramSet object of type xic for extracted ion chromatograms. _[grounded: tool_readchromatogram]_
- **(finding)** The example LC-MS run was recorded by parallel reaction monitoring (PRM) with the parent ion 487.2567 isolated in regularly-spaced intervals.
- **(finding)** The delta between consecutive scans in the PRM example is always 22 scans (one PRM cycle).
- **(finding)** Linear regression can convert observed peptide retention times into iRT values and vice versa for retention time calibration.
- **(finding)** Fitted iRT regression models provide information about LC-MS run performance.
- **(finding)** The iRT peptides were separated on a 20 minute linear gradient from 5% buffer B to 35% buffer B using C18 reversed-phase material.
- **(finding)** The iRT peptide GAGSSEPVTGLDAK is defined to have a zero score on the iRT scale.
- **(finding)** The iRT regression R-squared indicates that RTs behave highly linearly for the example data. _[grounded: result_rsquared_irt]_
- **(finding)** The web page showing extended use cases automatically updates every 30 minutes using the most recent two files per system as input data.
- **(finding)** The code for the extended use case web page is executed in full parallel fashion with each core processing one raw file on a Linux server with network-attached storage.
- **(finding)** The rawrr package is implemented with .NET 8.0 runtime and precompiled wrapper methods bundled in an executable file. _[grounded: sys_rawrr]_
- **(finding)** The rawrr package contains C# source code (rawrr.cs) for transparency and improvement by other developers. _[grounded: sys_rawrr]_
- **(finding)** The keys FAIMS Voltage On and FAIMS CV are only written by instruments that support FAIMS acquisition.
- **(finding)** The rawrr package implements basic generics for printing and plotting of objects in base R to minimize dependencies. _[grounded: sys_rawrr]_
- **(finding)** The mass spectrometer used for the example file was operated in line with a nano UPLC and a nano electrospray source (NSI).
- **(finding)** All spectra in the example file were written after applying centroiding and lock mass correction. _[grounded: tool_spectra]_
- **(finding)** Centroided data allows graphing spectra using signal-to-noise as response value. _[grounded: tool_spectra]_
- **(finding)** The rawrr package design makes data handling relatively easy and intuitive with little knowledge required about internal technical details. _[grounded: sys_rawrr]_
- **(finding)** rawrr uses vendor API methods whenever possible while maintaining ease-of-use without impairing performance. _[grounded: sys_rawrr]_
- **(finding)** The rawrr implementation aligns with common R conventions and styles. _[grounded: sys_rawrr]_
- **(finding)** The ThermoFisher.CommonCore dlls can be obtained through the RawFileReader GitHub repository or by contacting Jim Shofstahl at Thermo Fisher. _[grounded: comp_rawfilereader]_
- **(finding)** Installation of .NET 8.0 is required to compile rawrr.exe from C# source code. _[grounded: sys_rawrr]_
- **(finding)** The Bioconductor project currently provides over 1900 open-source software packages.

**Speculative claims (excluded from scoring):**
- **(finding)** A gap exists in the R ecosystem for libraries providing direct raw data reading to facilitate modular end-to-end analysis pipeline development.

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- MaxQuant or Skyline outputs can be processed by MSstats for statistical analysis
- ProteoWizard or ThermoRawFileParser can convert raw data to mzML format for use with R libraries
- Mono (instead of .NET 8.0)
- Base peak chromatogram (BPC) instead of total ion chromatogram (TIC)
- Deriving retention time from maximum intensity as alternative to peak fitting

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- rawrr requires Thermo Fisher Scientific Orbitrap instrument data in proprietary raw file format
- ThermoFisher.CommonCore dlls must be obtained through RawFileReader repository or by contacting Jim Shofstahl
- rawrrSpectrum content partially depends on the instrument model and installed instrument control software version
- Windows systems require decimal symbol configured as '.' for mZ and intensity vector extraction

## Steps

### Step `task_001`
- Title: Reproduce the iRT peptide retention time regression R-squared result from rawrr readSpectrum output
- Task kind: `reproduction`
- Task: Extract retention times for iRT peptides from the public raw file 20181113_010_autoQC01.raw (MassIVE MSV000086542) using rawrr::readSpectrum, fit a linear regression model (rtFittedAPEX ~ iRTscore), and report the R-squared value to confirm highly linear retention-time behavior.
- Inputs:
  - Public raw file 20181113_010_autoQC01.raw from MassIVE MSV000086542
  - iRT peptide standard reference m/z values and retention time scores
- Expected outputs:
  - Linear regression model summary with R-squared value ≥0.99
  - Table of extracted retention times (rtFittedAPEX) matched to iRT peptide scores
- Tools: rawrr, RawFileReader
- Landmark output files: rawfile_header_metadata.txt, irt_extracted_chromatograms.csv, irt_retention_times_fitted.csv
- Primary expected artifact: `irt_linear_regression_summary.txt`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce the readSpectrum throughput benchmark (spectra per second) for rawrr
- Task kind: `reproduction`
- Task: Execute the rawrr:::.benchmark function on the sample raw file (20181113_010_autoQC01.raw) using rawrr::readSpectrum to measure and confirm the reported spectra-per-second throughput performance under the benchmark experimental condition.
- Inputs:
  - 20181113_010_autoQC01.raw – example Thermo Fisher Q Exactive HF raw file with centroided, lock-mass-corrected FTMS and HCD MS2 spectra
  - rawrr R package with pre-compiled .NET 8.0 executable bundled including RawFileReader dynamic link library
- Expected outputs:
  - Benchmark report with measured spectra-per-second throughput value from readSpectrum function execution
- Tools: rawrr, RawFileReader, .NET 8.0
- Landmark output files: rawrr_installation.log, benchmark_output.txt
- Primary expected artifact: `benchmark_report.txt`

### Step `task_003`
- Title: Reproduce the Orbitrap scan 9594 LGGNEQVTR++ PRM spectrum metadata and y-ion S/N characterisation
- Task kind: `reproduction`
- Task: Extract scan 9594 from the raw LC-MS file 20181113_010_autoQC01.raw using rawrr::readSpectrum and validate the reported instrumental parameters (resolving power 30,000 at 200 m/z, AGC injection time 2.8 ms) and y-ion signal quality (tens to hundreds above noise floor).
- Inputs:
  - Raw mass spectrometry file 20181113_010_autoQC01.raw from MassIVE dataset MSV000086542 (MD5: a1f5df9627cf9e0d51ec1906776957ab)
- Expected outputs:
  - Extracted spectrum object (rawrrSpectrum) containing 119 data items for scan 9594 including m/z array, intensity array, resolving power, AGC target, and injection time metadata
  - Validation report confirming resolving power = 30,000 at 200 m/z, AGC injection time = 2.8 ms, and all y-ion signal intensities are tens to hundreds counts above noise baseline
- Tools: rawrr, RawFileReader
- Landmark output files: spectrum_9594_raw.csv, instrumental_metadata_9594.json
- Primary expected artifact: `scan_9594_validation_report.txt`

### Step `task_004`
- Depends on: `task_003`
- Title: Reproduce the PRM cycle delta of 22 scans using rawrr::readIndex on the autoQC01 raw file
- Task kind: `reproduction`
- Task: Load the scan index from 20181113_010_autoQC01.raw using rawrr::readIndex(), filter for PRM (parallel reaction monitoring) scan events, and validate that the delta between consecutive PRM scans is consistently 22 scans per acquisition cycle.
- Inputs:
  - 20181113_010_autoQC01.raw file from MassIVE dataset MSV000086542
- Expected outputs:
  - Filtered scan index data frame (CSV or R object) containing only PRM scans with columns: scan, scanType, rtmin, rtmax, and computed delta (inter-scan interval)
  - Summary statistics report documenting total PRM scan count, delta distribution (mean, min, max), and boolean pass/fail for 22-scan-cycle consistency
- Tools: rawrr, RawFileReader
- Landmark output files: scan_index_raw.csv, scan_index_filtered_prm.csv, inter_scan_deltas.csv
- Primary expected artifact: `prm_scan_index_validation.csv`

### Step `task_005`
- Depends on: `task_002`
- Title: Reconstruct the two-layer R/C# architecture: invoke rawrr.exe wrapper from R and verify .NET assembly dispatch
- Task kind: `component_reconstruction`
- Task: Verify the two-layer architecture dispatch path by calling rawrr internal assembly accessor functions (rawrr:::.rawrrAssembly() and rawrr:::.getRawrrAssemblyVersion()) and confirm that the assembly path and version string are returned correctly without requiring a raw data file as input.
- Inputs:
  - rawrr R package (installed in the local R environment)
- Expected outputs:
  - Assembly path string pointing to the rawrr.exe executable location
  - Version string of the .NET 8.0 assembly
  - Validation report confirming successful assembly accessor function calls
- Tools: RawFileReader
- Landmark output files: assembly_path.txt, assembly_version.txt
- Primary expected artifact: `assembly_dispatch_validation.txt`

## Final expected outputs

- `Filtered scan index data frame (CSV or R object) containing only PRM scans with columns: scan, scanType, rtmin, rtmax, and computed delta (inter-scan interval)` (type: file, tolerance: hash)
- `Summary statistics report documenting total PRM scan count, delta distribution (mean, min, max), and boolean pass/fail for 22-scan-cycle consistency` (type: file, tolerance: hash)
- `Assembly path string pointing to the rawrr.exe executable location` (type: file, tolerance: hash)
- `Version string of the .NET 8.0 assembly` (type: file, tolerance: hash)
- `Validation report confirming successful assembly accessor function calls` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: closed — reproduction-first.** The deterministic rubrics above bind. A different method is acceptable ONLY if it appears under *Sanctioned method substitutions*; outputs are compared with the declared tolerance. Different is wrong here only when it departs from the sanctioned set or breaks an invariant.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** flat

- **Abstraction level:** concrete

- **Orchestration planning:** static

- **Data transport:** file

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_rawrr_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004",
    "task_005"
  ],
  "intermediate_outputs": {
    "task_001": {
      "<output_name>": "<locator>"
    },
    "task_002": {
      "<output_name>": "<locator>"
    },
    "task_003": {
      "<output_name>": "<locator>"
    },
    "task_004": {
      "<output_name>": "<locator>"
    },
    "task_005": {
      "<output_name>": "<locator>"
    }
  },
  "final_outputs": {
    "Filtered scan index data frame (CSV or R object) containing only PRM scans with columns: scan, scanType, rtmin, rtmax, and computed delta (inter-scan interval)": "<locator>",
    "Summary statistics report documenting total PRM scan count, delta distribution (mean, min, max), and boolean pass/fail for 22-scan-cycle consistency": "<locator>",
    "Assembly path string pointing to the rawrr.exe executable location": "<locator>",
    "Version string of the .NET 8.0 assembly": "<locator>",
    "Validation report confirming successful assembly accessor function calls": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>",
    "task_005": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
