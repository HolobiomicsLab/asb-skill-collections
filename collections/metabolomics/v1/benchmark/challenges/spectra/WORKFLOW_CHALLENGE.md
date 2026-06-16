# Workflow Challenge: `coll_spectra_workflow`


> This vignette describes the MsBackend virtual class API and illustrates how to create a new backend class (MsBackendTest) for the Spectra package that represents and provides mass spectrometry data.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Reproduces 3 reported results: The spectraData() implementation for MsBackendTest uses fillCoreSpectraVariables() to ensure that all core spectra variables are returned, filling missing ones with NA values even when only user-supplied variables like msLevel and rtime are stored. The mz<- replacement method uses the efficient is.unsorted() implementation for NumericList rather than vapply, and raises a stop error when any spectrum has unsorted m/z values: 'if (any(is.unsorted(value))) stop("m/z values need to be increasingly sorted within each spectrum")' Pre-populating @spectraVars with all core spectra variables increases memory footprint because all variables, including those with only missing values, must be stored in the object, whereas on-the-fly initialization via fillCoreSpectraVariables() avoids storing empty columns but may be less efficient for data extraction. Reconstructs 2 described mechanisms (described in the paper but not separately evaluated there): MsBackendTest requires implementation of 9 required accessor methods (spectraData, spectraVariables, backendInitialize, peaksData, extractByIndex, backendMerge, intensity, mz, spectraNames) plus 7 data replacement methods ($<-, spectraData<-, intensity<-, mz<-, peaksData<-, selectSpectraVariables, dataStorage<-, spectraNames<-) with specific signatures. The class uses three slots: spectraVars (data.frame), mz (NumericList), and intensity (NumericList), where each row in spectraVars represents one spectrum and corresponding elements in mz/intensity lists contain peak data. MsBackendMzR's backendParallelFactor() returns a factor based on dataStorage file names to split the backend for parallel or serial processing. Chunk-wise processing via this splitting reduces memory demand because only the peak data of the current chunk—not all spectra—needs to be realized in memory during operations.

## Research questions

- What are the required method signatures and implementations needed to create a complete MsBackendTest class that extends MsBackend and provides full read-write access to mass spectrometry spectral data?
- Does the spectraData() method on a MsBackendTest instance correctly return all core spectra variables with NA values when only user-supplied spectra variables are stored in the backend?
- Does the mz<- replacement method for MsBackendTest correctly validate that m/z values are increasingly sorted within each spectrum, and does it use an efficient vectorised is.unsorted() implementation on NumericList objects rather than vapply?
- Does pre-populating the @spectraVars data frame with all core spectra variable columns consume more memory than adding missing columns on-the-fly during spectraData() calls?
- How does the backendParallelFactor() method for MsBackendMzR enable chunk-wise splitting of backend data during parallel processing, and what is the memory advantage of processing spectra in chunks rather than loading all peak data into memory at once?

## Methods overview

Define S4 class MsBackendTest extending MsBackend with typed slots for spectraVars, mz, and intensity data Implement core accessor methods (spectraData, spectraVariables, peaksData, intensity, mz, spectraNames) following DataFrame/NumericList conventions Implement backend lifecycle methods (backendInitialize) and collection operations (extractByIndex, backendMerge, [) Implement data replacement methods (intensity<-, mz<-, spectraData<-) ensuring m/z values remain sorted Validation: class instantiation succeeds, all required methods execute without error, output types match API contract (DataFrame, NumericList, character vector) Define a MsBackendTest class extending the virtual MsBackend with slots for user-supplied variables and peak data Implement required accessor methods (spectraData, spectraVariables, peaksData, intensity, mz, extractByIndex) according to the MsBackend API Invoke fillCoreSpectraVariables() within spectraData() to populate missing core spectra variables with NA Return a DataFrame containing both user-supplied and filled core variables Validation: verify that spectraData() output contains all expected core spectra variables and user-supplied variables are preserved with NA values for missing core columns Retrieve MsBackendTest implementation from the Spectra package repository. Extract and inspect the mz<- replacement method code to verify vectorised is.unsorted() usage on NumericList input. Test assignment of correctly sorted m/z values and confirm no error is raised. Test assignment of unsorted m/z values and confirm an appropriate error is raised. Validation: method correctly detects unsorted input via is.unsorted() and rejects invalid m/z assignments while accepting valid sorted assignments. Instantiate MsBackendTest with all core spectra variables pre-populated in @spectraVars slot. Instantiate a second MsBackendTest with minimal @spectraVars and allow fillCoreSpectraVariables() to populate columns during spectraData() call. Measure R object memory footprint using object.size() before and after each spectraData() invocation. Record wall-clock execution time for spectraData() on both variants using system.time(). Validation: Compare memory sizes and document the percentage overhead and latency difference; confirm both variants produce identical DataFrame output from spectraData(). Define S4 class extending MsBackend with slots for spectra variables, m/z, and intensity data Implement backendInitialize() to load raw MS data files and populate dataStorage metadata Implement backendParallelFactor() to extract unique file paths from dataStorage and return a grouping factor Implement peaksData() to extract and return m/z and intensity matrices with index-based subsetting support Benchmark memory consumption: measure peak-data memory footprint for whole-load versus chunk-wise splitting approaches Validation: memory usage in chunk-wise approach is statistically lower than whole-load approach; factor correctly groups all spectra by source file

**Domain:** bioinformatics

**Techniques:** feature-detection, spectral-library-matching

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** The Spectra package defines an efficient infrastructure for storing and handling mass spectrometry spectra and functionality to subset, process, visualize and compare spectra. _[grounded: spectra_package]_
- **(finding)** The Spectra package separates the code for the analysis of MS data from the code needed to import, represent and provide the data. _[grounded: spectra_package]_
- **(finding)** Each Spectra object contains an implementation of a MsBackend within its @backend slot which provides the MS data to the Spectra object. _[grounded: spectra_package]_
- **(finding)** The MsBackend virtual class defines the API that new backend classes need to implement in order to be used with the Spectra object. _[grounded: spectra_package]_
- **(finding)** This separation allows to define new, alternative, data representations and integrate them seamlessly into a Spectra-based data analysis workflow. _[grounded: spectra_package]_
- **(finding)** One Spectra object is supposed to contain MS spectral data of multiple MS spectra. _[grounded: spectra_package]_
- **(finding)** m/z values within each spectrum are expected to be sorted increasingly.
- **(finding)** Missing values (NA) for m/z values are not supported.
- **(finding)** Properties of a spectrum are called spectra variables. _[grounded: spectra_package]_
- **(finding)** Each backend must provide a minimum required set of core spectra variables listed by the coreSpectraVariables() function. _[grounded: spectra_package]_
- **(finding)** dataStorage and dataOrigin are special spectra variables that define where the data is stored and from where the data derived. _[grounded: spectra_package]_
- **(finding)** Both dataStorage and dataOrigin must be of type character and need to be defined by the backend. _[grounded: datastorage_variable]_
- **(finding)** MsBackend implementations can represent purely read-only data resources where only data accessor methods need to be implemented but not data replacement methods. _[grounded: msbackend_virtual_class]_
- **(finding)** Whether a backend is read-only can be set with the @readonly slot of the virtual MsBackend class. _[grounded: msbackend_virtual_class]_
- **(finding)** The default value for @readonly is FALSE, requiring all data replacement methods to be implemented.
- **(finding)** For read-only backends (@readonly = TRUE) only the methods in the Required methods section need to be implemented.
- **(finding)** The MsBackendMzR backend allows changing spectra variables but not the peaks data (m/z and intensity values). _[grounded: spectra_package]_
- **(finding)** Backends for purely read-only resources could extend the MsBackendCached from the Spectra package to enable support for modifying or adding spectra variables. _[grounded: spectra_package]_
- **(finding)** The Spectra package splits the backend based on a defined factor and processes each in parallel for parallel processing. _[grounded: spectra_package]_
- **(finding)** The default implementation for backendParallelFactor() returns an empty factor, not suggesting any preferred splitting. _[grounded: backendparallelfactor_method]_
- **(finding)** The backendParallelFactor() for MsBackendMzR returns a factor based on the data files the data is stored in. _[grounded: msbackend_mzr]_
- **(finding)** Chunk-wise processing can reduce the memory demand for operations because only the peak data of the current chunk needs to be realized in memory.
- **(finding)** The spectraData() method should return the full spectra data within a backend as a DataFrame object. _[grounded: spectra_package]_
- **(finding)** Each row in the DataFrame returned by spectraData() should represent one spectrum and each column a spectra variable. _[grounded: spectra_package]_
- **(finding)** Columns mz and intensity (if requested) must contain each a NumericList with the m/z and intensity values of the spectra. _[grounded: spectra_package]_
- **(finding)** The DataFrame returned by spectraData() must provide values for all requested spectra variables of the backend including the core spectra variables. _[grounded: spectra_package]_
- **(finding)** The spectraVariables() method should return a character vector with the names of all available spectra variables of the backend. _[grounded: spectra_package]_
- **(finding)** Each MsBackend class must provide the core spectra variables in the correct data type. _[grounded: spectra_package]_
- **(finding)** Core spectra variables can be NA with the exception of the spectra variable dataStorage. _[grounded: spectra_package]_
- **(finding)** The backendInitialize() method is expected to be called after creating an instance of the backend class and should prepare the backend. _[grounded: backendinitialize_method]_
- **(finding)** During backendInitialize() the special spectra variables dataStorage and dataOrigin are usually set. _[grounded: spectra_package]_
- **(finding)** The peaksData() method extracts the MS peaks data from a backend, including the m/z and intensity values of each MS peak of a spectrum. _[grounded: peaksdata_method]_
- **(finding)** peaksData() is expected to return a List of numerical matrices with columns being the requested peaks variables of one spectrum. _[grounded: peaksdata_method]_
- **(finding)** Backends must provide at least mz and intensity as peaks variables. _[grounded: intensity_method]_
- **(finding)** The extractByIndex() and [ methods allow to subset MsBackend objects. _[grounded: msbackend_virtual_class]_
- **(finding)** Subsetting with extractByIndex() and [ must support duplication and extraction in any arbitrary order. _[grounded: extractbyindex_method]_
- **(finding)** extractByIndex() only supports to subset with an integer index while [ should support to subset by indices or logical vectors. _[grounded: extractbyindex_method]_
- **(finding)** An error should be thrown if indices are out of bounds but the method should support returning an empty backend with [integer()].
- **(finding)** The backendMerge() method merges MsBackend objects of the same type into a single instance. _[grounded: msbackend_virtual_class]_
- **(finding)** The intensity() method extracts the intensity values for each spectrum in the backend as a NumericList. _[grounded: spectra_package]_
- **(finding)** The mz() method extracts the m/z values for each spectrum in the backend as a NumericList. _[grounded: spectra_package]_
- **(finding)** The m/z values are expected to be ordered increasingly for each element (spectrum).
- **(finding)** The spectraNames() method can be used to extract optional names or IDs for individual spectra of a backend, or NULL if not set. _[grounded: spectra_package]_
- **(finding)** The $<- method should allow to replace values for spectra variables or to add additional spectra variables to the backend. _[grounded: spectra_package]_
- **(finding)** With the $<- method, the length() of value must match the number of spectra represented by the backend. _[grounded: spectra_package]_
- **(finding)** The spectraData<- method should allow to replace the data within a backend by taking a DataFrame with the full data as input value. _[grounded: spectradata_method]_
- **(finding)** The spectraData<- method is expected to replace the full data within the backend including all spectra variables and peak data. _[grounded: spectra_package]_
- **(finding)** The number of spectra before and after calling spectraData<- method on an object has to be the same. _[grounded: spectra_package]_
- **(finding)** The intensity<- method should allow to replace only the values of the intensities but must not change the number of intensities per spectrum. _[grounded: spectra_package]_
- **(finding)** The mz<- method should allow to replace the m/z values of all spectra in a backend. _[grounded: spectra_package]_
- **(finding)** m/z values within each spectrum need to be increasingly ordered when using the mz<- method.
- **(finding)** The peaksData<- method should allow to replace the peaks data (m/z and intensity values) of all spectra in a backend. _[grounded: spectra_package]_
- **(finding)** The peaksData<- method should support changing the number of peaks per spectrum such as due to filtering. _[grounded: peaksdata_method]_
- **(finding)** The selectSpectraVariables() function should allow to reduce the information within the backend to the selected spectra variables. _[grounded: spectra_package]_
- **(finding)** The selectSpectraVariables() is equivalent to a subset by columns or variables. _[grounded: selectspectravariables_method]_
- **(finding)** The $ method is expected to extract a single spectra variable from a backend. _[grounded: spectra_package]_
- **(finding)** Each MsBackend must support extracting the core spectra variables with the $ method even if no data might be available for that variable. _[grounded: spectra_package]_
- **(finding)** The $ method should check if the requested spectra variable is available and should throw an error otherwise. _[grounded: spectra_package]_
- **(finding)** The peaksVariables() is expected to return a character vector with the names of the peaks variables available in the backend.
- **(finding)** The default implementation for peaksVariables() returns c("mz", "intensity") for MsBackend. _[grounded: msbackend_virtual_class]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- Data can be loaded from raw MS data files or referenced via database connections instead of loading directly in backendInitialize()
- Backends can use MsBackendCached for read-only resources to cache modified spectra variables without propagating to underlying data
- Data can be initialized with data.frame by columns or as complete DataFrame with optional data parameter

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Read-only backends do not need to implement data replacement methods, only accessor methods
- All MsBackend implementations must provide core spectra variables with correct data types
- m/z values must be increasingly sorted within each spectrum
- Length of replacement values must match the number of spectra in the backend
- Peak data replacement lengths must match the number of peaks per spectrum

## Steps

### Step `task_001`
- Title: Implement the MsBackend virtual class API for a new in-memory backend (MsBackendTest)
- Task kind: `component_reconstruction`
- Task: Implement a complete MsBackendTest class extending the virtual MsBackend class with all required accessor and data-replacement methods to enable creation of custom MS data backends compatible with the Spectra infrastructure.
- Inputs:
  - MsBackend virtual class API specification and documentation
- Expected outputs:
  - R source file containing complete MsBackendTest class implementation with all required methods
- Tools: Spectra, S4Vectors, R
- Landmark output files: MsBackendTest_class_skeleton.R, MsBackendTest_accessors.R, MsBackendTest_replacement_methods.R, MsBackendTest_complete.R
- Primary expected artifact: `MsBackendTest.R`

### Step `task_002`
- Title: Reproduce the fillCoreSpectraVariables() behavior for missing core spectra variables in spectraData()
- Task kind: `reproduction`
- Task: Implement and test a MsBackendTest class that correctly handles user-supplied spectra variables (msLevel, rtime) and uses fillCoreSpectraVariables() to populate missing core variables with NA values, verifying that spectraData() returns the complete set of core spectra variables.
- Inputs:
  - Spectra package documentation and API specification
  - User-supplied spectra variables: msLevel and rtime values
- Expected outputs:
  - MsBackendTest class definition extending MsBackend with implemented core methods
  - DataFrame returned by spectraData() containing all core spectra variables with NA for missing user-supplied values
- Tools: Spectra, S4Vectors, R
- Landmark output files: MsBackendTest_class_definition.R, spectra_dataframe_output.csv

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce the NumericList is.unsorted() efficiency check in the mz<- replacement method
- Task kind: `reproduction`
- Task: Verify that the mz<- replacement method on MsBackendTest correctly uses vectorised is.unsorted() on a NumericList and raises an appropriate error when unsorted m/z values are supplied.
- Inputs:
  - task_001.expected_outputs[0]: R source file containing complete MsBackendTest class implementation with all required methods
  - MsBackendTest source code from Spectra package (RforMassSpectrometry/Spectra repository)
- Expected outputs:
  - Validation report documenting mz<- method correctness: confirmation of vectorised is.unsorted() usage, successful assignment of sorted m/z values, and error raised on unsorted input
- Tools: Spectra, R, S4Vectors
- Landmark output files: mz_method_source_inspection.R, valid_mz_assignment_test.log, invalid_mz_error_confirmation.log
- Primary expected artifact: `mz_replacement_validation_report.txt`

### Step `task_004`
- Depends on: `task_001`
- Title: Reproduce the spectraData initialization memory tradeoff described for pre-populated vs on-the-fly core spectra variables
- Task kind: `reproduction`
- Task: Measure and compare in-memory object sizes of a MsBackendTest instance with pre-populated core spectra variables versus one where missing columns are added on-the-fly during spectraData() retrieval, quantifying the memory tradeoff between eager and lazy initialization.
- Inputs:
  - task_001.expected_outputs[0]: R source file containing complete MsBackendTest class implementation with all required methods
  - MsBackendTest class definition with S4 slots for spectraVars (data.frame), mz (NumericList), and intensity (NumericList)
- Expected outputs:
  - Numeric comparison table with columns: backend_variant, initial_object_size_bytes, post_spectraData_size_bytes, memory_increase_bytes, spectraData_execution_time_seconds
- Tools: Spectra, R, S4Vectors
- Landmark output files: backend_eager_initialization.rds, backend_lazy_initialization.rds, spectraData_eager_output.rds, spectraData_lazy_output.rds, memory_profile_eager.txt, memory_profile_lazy.txt
- Primary expected artifact: `memory_comparison.csv`

### Step `task_005`
- Depends on: `task_002`
- Title: Implement chunk-wise parallel processing via backendParallelFactor() and verify memory-reduction behaviour
- Task kind: `component_reconstruction`
- Task: Implement the backendParallelFactor() method for MsBackendMzR to generate a factor based on dataStorage file names, and validate that chunk-wise parallel splitting of spectra reduces peak-data memory consumption compared to loading all spectra into memory at once.
- Inputs:
  - Raw MS data files in mzML or mzXML format with known file paths and spectra identifiers
  - Spectra package source code or installation with MsBackend virtual class definition
- Expected outputs:
  - R script implementing backendParallelFactor() method that returns a factor grouping spectra by dataStorage file name
  - Memory benchmark report (CSV or text) comparing peak-data memory demand for chunk-wise splitting versus whole-load approach
  - Performance comparison visualization (plot or figure) showing memory usage reduction percentage across different dataset sizes
- Tools: Spectra, MsBackendMzR, R, S4Vectors
- Landmark output files: backend_parallel_factor.R, memory_profile_whole_load.txt, memory_profile_chunked.txt, benchmark_results.csv, memory_reduction_plot.png
- Primary expected artifact: `memory_benchmark_report.csv`

## Final expected outputs

- `Validation report documenting mz<- method correctness: confirmation of vectorised is.unsorted() usage, successful assignment of sorted m/z values, and error raised on unsorted input` (type: file, tolerance: hash)
- `Numeric comparison table with columns: backend_variant, initial_object_size_bytes, post_spectraData_size_bytes, memory_increase_bytes, spectraData_execution_time_seconds` (type: file, tolerance: hash)
- `R script implementing backendParallelFactor() method that returns a factor grouping spectra by dataStorage file name` (type: file, tolerance: hash)
- `Memory benchmark report (CSV or text) comparing peak-data memory demand for chunk-wise splitting versus whole-load approach` (type: file, tolerance: hash)
- `Performance comparison visualization (plot or figure) showing memory usage reduction percentage across different dataset sizes` (type: file, tolerance: hash)

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

- **Data transport:** in_memory

- **Characterisation confidence:** inferred


## Submission

Produce two artifacts in your output directory:

1. The output files at the paths declared under **Final expected outputs**.
2. An `attempt.json` matching the schema below.
3. _(Optional)_ `attempt_metrics.json` with `wall_time_s`, `total_tokens`, `cost_usd` for the EFFICIENCY rubric.

### `attempt.json` schema

```json
{
  "workflow_id": "coll_spectra_workflow",
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
    "Validation report documenting mz<- method correctness: confirmation of vectorised is.unsorted() usage, successful assignment of sorted m/z values, and error raised on unsorted input": "<locator>",
    "Numeric comparison table with columns: backend_variant, initial_object_size_bytes, post_spectraData_size_bytes, memory_increase_bytes, spectraData_execution_time_seconds": "<locator>",
    "R script implementing backendParallelFactor() method that returns a factor grouping spectra by dataStorage file name": "<locator>",
    "Memory benchmark report (CSV or text) comparing peak-data memory demand for chunk-wise splitting versus whole-load approach": "<locator>",
    "Performance comparison visualization (plot or figure) showing memory usage reduction percentage across different dataset sizes": "<locator>"
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
