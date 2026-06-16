# Workflow Challenge: `coll_vimms_workflow`


> ViMMS is a flexible simulation framework for prototyping and comparing fragmentation strategies in liquid chromatography–tandem mass spectrometry-based metabolomics without requiring real instrument time.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

ViMMS (Virtual Metabolomics Mass Spectrometer) is a modular framework designed to simulate fragmentation strategies in LC-MS/MS metabolomics. The framework enables researchers to generate virtual chemicals through various sampling methods (e.g., from HMDB databases or uniform m/z distributions), configure virtual mass spectrometers with customizable noise models, and execute fragmentation strategies via controller implementations such as Top-N data-dependent acquisition (DDA) and data-independent acquisition (DIA) methods including SWATH and all-ion fragmentation. An Environment class orchestrates the interaction between chemicals, mass spectrometer, and controller, executing the acquisition simulation and exporting results to mzML format for downstream analysis. The framework supports evaluation of simulation outputs through coverage and intensity metrics, and can interface with real instruments via the vimms_fusion extension. Demonstrated applications include generating full-scan MS1 data from simulated chemicals, reproducing Top-N fragmentation on real beer metabolomics data for validation, and sampling 73,822 filtered HMDB formulae in the m/z range 100–1000 for chemical generation.

## Research questions

- Can ViMMS simulate a full-scan MS1 acquisition on a set of known chemical compounds sampled from the HMDB database and produce a valid mzML output file?
- Can ViMMS simulate Top-N MS/MS acquisition on real beer samples and reproduce the fragmentation coverage observed in the original experimental data?
- How are the three core components (Chemicals, IndependentMassSpectrometer, and Controller) orchestrated by the Environment class to execute a complete simulation control loop?
- Can the reported count of 73,822 unique formulas in the HMDB database (filtered for m/z 100–1000) be reproduced by running DatabaseFormulaSampler on the downloaded raw HMDB data?
- How do evaluation metrics from WeightedDEWController differ from the baseline TopNController when both are run through the ViMMS simulation framework?

## Methods overview

Load or initialize HMDB compound database and sample 100 chemical formulas within m/z 100–1000 range. Generate KnownChemical objects with simulated retention times, intensities, and MS1 chromatograms. Instantiate virtual mass spectrometer and configure FullScanController for MS1-only (no MS2) acquisition. Execute Environment simulation loop to record scans at 1–5 second intervals across 0–1200 second run time. Export simulated scans to mzML format and optionally pickle EvaluationData for ground-truth reference. Validation: Verify mzML file is valid and contains MS1 scans only with correct polarity, retention time range, and m/z values matching sampled chemicals. References: source article (DOI: 10.1021/acs.analchem.0c03895) Download and load the Beer1pos real mzML file from the vimms-data repository. Extract unknown chemical objects (m/z, retention time, intensity profiles) from the real mzML using ChemicalMixtureFromMZML. Instantiate an IndependentMassSpectrometer with the extracted chemicals and positive polarity mode. Configure a TopNController with N=5, isolation_width=1, and match the real acquisition intensity thresholds. Run the simulation via Environment.run() and export the simulated mzML. Apply consistent peak detection (OpenMS parameters) to both real and simulated mzML files. Compute fragmentation coverage and intensity metrics and compare across datasets. Validation: reproduce the reported Top-N fragmentation coverage and intensity comparison for Beer1pos from the demo notebook, confirming consistency of simulated versus real acquisition metrics. References: source article (DOI: 10.1021/acs.analchem.0c03895) Instantiate a formula sampler (UniformMZFormulaSampler) with m/z bounds 100–500 Da. Create a chemical mixture from the sampler using ChemicalMixtureCreator, sampling 100 chemicals with MS1 and MS2 levels. Construct an IndependentMassSpectrometer in positive polarity mode with the chemical list. Configure a TopNController with fixed parameters: N=3, isolation_width=1, mz_tol=10, rt_tol=15, min_ms1_intensity=1.75E5. Build an Environment object spanning 0–1440 s, register the mass spectrometer and controller, and invoke run(). Validation: confirm that env.scans is a non-empty list containing both MS1 and MS2 Scan objects with valid m/z, intensity, and retention-time fields. References: source article (DOI: 10.1021/acs.analchem.0c03895) Download the HMDB database file from the vimms-data public repository. Load HMDB data into memory using ViMMS's built-in HMDB loading functions. Instantiate DatabaseFormulaSampler with the loaded HMDB data and configure m/z range constraints (or other filter criteria as present in the benchmark). Execute the sampler's filtering pipeline to extract and deduplicate molecular formulas. Count unique formulas in the filtered output and record the result. Validation: verify that the output formula count equals 73,822 as reported in the benchmark. References: source article (DOI: 10.1021/acs.analchem.0c03895) Sample 100 virtual metabolites across m/z 100–500 with two MS levels using UniformMZFormulaSampler. Instantiate IndependentMassSpectrometer with POSITIVE polarity and the generated chemicals. Configure WeightedDEWController with use_weighteddew_exclusion=True, N=3, isolation_width=1 m/z, mz_tol=10 ppm, rt_tol=15 s, and min_ms1_intensity=1.75E5. Run the Environment simulation loop from t=0 to 1440 s with save_eval=True to capture fragmentation events and scan traces. Serialize the mzML output and pickled EvaluationData object to disk. Compute evaluation metrics (times_fragmented_summary, cumulative intensity) from the pickle and compare against baseline TopNController result to verify performance differentiation. Validation: Confirm that the WeightedDEW run produces a non-zero times_fragmented_summary metric with at least one chemical fragmented at least twice, and that cumulative intensity and fragmentation breadth metrics differ measurably from the baseline TopN run. References: source article (DOI: 10.1021/acs.analchem.0c03895)

**Domain:** metabolomics

**Techniques:** data-independent-acquisition, feature-detection, machine-learning, metabolite-identification, spectral-library-matching

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** ViMMS is a flexible and modular framework designed to simulate fragmentation strategies in tandem mass spectrometry-based metabolomics. _[grounded: VIMMS_SYSTEM]_
- **(finding)** Devising new MS/MS fragmentation methods is challenging due to the absence of a structured environment where researchers can prototype, compare, and optimize strategies before testing on real equipment. _[grounded: COMP_ENVIRONMENT]_
- **(finding)** ViMMS allows you to simulate fragmentation strategies, generate virtual chemicals through various methods, and evaluate the performance of different strategies or controllers in either single or multi-sample settings. _[grounded: VIMMS_SYSTEM]_
- **(finding)** ViMMS is compatible with Python 3+. _[grounded: VIMMS_SYSTEM]_
- **(finding)** ViMMS can be installed using pip. _[grounded: VIMMS_SYSTEM]_
- **(finding)** ViMMS dependencies are managed with Poetry. _[grounded: VIMMS_SYSTEM]_
- **(finding)** ViMMS uses MkDocs to build its documentation, which is hosted at vimms.readthedocs.io. _[grounded: VIMMS_SYSTEM]_
- **(finding)** ViMMS uses pyTest as the testing framework. _[grounded: VIMMS_SYSTEM]_
- **(finding)** ViMMS follows PEP8 coding style with linewidth set to 99 characters. _[grounded: VIMMS_SYSTEM]_
- **(finding)** flake8 and autopep8 tools have been installed as part of the virtual environment to ensure PEP8 compliance. _[grounded: COMP_ENVIRONMENT]_
- **(finding)** Contributors to ViMMS must submit code under the MIT License. _[grounded: VIMMS_SYSTEM]_
- **(finding)** ViMMS is designed to serve as a unified platform for the development, testing, and optimization of fragmentation strategies in LC-MS metabolomics. _[grounded: VIMMS_SYSTEM]_
- **(finding)** ViMMS offers an extension that allows controllers to operate directly on the Thermo Orbitrap Fusion Tribrid instrument. _[grounded: VIMMS_SYSTEM]_
- **(finding)** A license for IAPI is required to use ViMMS on the Thermo Orbitrap Fusion Tribrid instrument. _[grounded: VIMMS_SYSTEM]_
- **(finding)** Known chemicals in ViMMS are represented by their chemical formulae and can be sampled from databases such as HMDB. _[grounded: VIMMS_SYSTEM]_
- **(finding)** DatabaseFormulaSampler samples formulas from a provided database. _[grounded: VIMMS_SYSTEM]_
- **(finding)** UniformMZFormulaSampler samples formulas uniformly in a defined m/z range. _[grounded: VIMMS_SYSTEM]_
- **(finding)** PickEverythingFormulaSampler samples all formulas from a database. _[grounded: VIMMS_SYSTEM]_
- **(finding)** EvenMZFormulaSampler creates evenly spaced m/z values, primarily for test cases. _[grounded: VIMMS_SYSTEM]_
- **(finding)** MZMLFormulaSampler samples m/z values from a histogram of m/z derived from a user-supplied mzML file. _[grounded: VIMMS_SYSTEM]_
- **(finding)** ChemicalMixtureCreator class is used to produce chemical datasets for simulation. _[grounded: VIMMS_SYSTEM]_
- **(finding)** Unknown chemicals in ViMMS are typically extracted from existing mzML files. _[grounded: VIMMS_SYSTEM]_
- **(finding)** Each peak picked from mzML files is presumed to correspond to a chemical in ViMMS simulation. _[grounded: VIMMS_SYSTEM]_
- **(finding)** CleanColumn applies reproducible offsets to all chemicals, keeping their elution order fixed. _[grounded: COMP_CHEMICALS]_
- **(finding)** LinearColumn extends CleanColumn with a retention time drift function, allowing systematic shifts across injections. _[grounded: COMP_CLEAN_COLUMN]_
- **(finding)** TopNController is a standard fragmentation strategy in ViMMS where the top N most intense ions in the survey scan are fragmented. _[grounded: VIMMS_SYSTEM]_
- **(finding)** ViMMS implements data-independent acquisition (DIA) strategies including All-ion-fragmentation (AIF) and SWATH-MS. _[grounded: VIMMS_SYSTEM]_
- **(finding)** Environment class orchestrates interaction between the mass spectrometer and the controller in ViMMS. _[grounded: VIMMS_SYSTEM]_
- **(finding)** GaussianPeakNoise adds normally distributed variation to peak intensities in ViMMS. _[grounded: VIMMS_SYSTEM]_
- **(finding)** AdditiveBaselineNoise injects a constant baseline across the m/z range in ViMMS. _[grounded: VIMMS_SYSTEM]_
- **(finding)** RetentionTimeDeviation introduces random jitter in retention times in ViMMS. _[grounded: VIMMS_SYSTEM]_
- **(finding)** The vimms_fusion extension allows ViMMS controllers to be deployed directly on the Thermo Orbitrap Fusion Tribrid instrument. _[grounded: VIMMS_SYSTEM]_
- **(finding)** GitHub Actions automatically publishes the vimms package to PyPI whenever a GitHub release is published. _[grounded: VIMMS_SYSTEM]_
- **(finding)** The version number in pyproject.toml must be updated before creating a release.
- **(finding)** A simulation in ViMMS involves Chemicals, Mass Spectrometer, Controller, and Environment components. _[grounded: VIMMS_SYSTEM]_
- **(finding)** Running the environment in ViMMS produces a list of scans that can be written to mzML. _[grounded: VIMMS_SYSTEM]_
- **(finding)** EvaluationData object stores the chemicals, generated scans and fragmentation events. _[grounded: COMP_CHEMICALS]_
- **(finding)** vimms.Evaluation provides several evaluator classes that compute coverage and intensity statistics across multiple runs. _[grounded: VIMMS_SYSTEM]_
- **(finding)** The evaluation helpers in ViMMS rely on peak picking using MZMine parameters defined in PeakPicking.py. _[grounded: VIMMS_SYSTEM]_
- **(finding)** WeightedDEWController is a Top-N variant with dynamic exclusion weighting in ViMMS. _[grounded: VIMMS_SYSTEM]_
- **(finding)** SmartROIController implements ROI guided fragmentation using adaptive scoring in ViMMS. _[grounded: VIMMS_SYSTEM]_
- **(finding)** FullScanController in ViMMS is useful for creating full scan datasets through MS1 only acquisition. _[grounded: VIMMS_SYSTEM]_
- **(finding)** All controllers in ViMMS share a common interface and can be extended to implement new fragmentation logic. _[grounded: VIMMS_SYSTEM]_
- **(finding)** Environment class provides write_mzML to export the generated scans. _[grounded: COMP_ENVIRONMENT]_
- **(finding)** MultipleMixtureCreator can introduce group specific intensity changes and missing values for multi-sample experiments. _[grounded: COMP_MULTIPLE_MIXTURE_CREATOR]_
- **(finding)** ChemicalMixtureFromMZML converts existing mzML files into chemical lists using ROI extraction. _[grounded: COMP_UNKNOWN_CHEMICAL]_
- **(finding)** openms_optimise.py runs grid searches over controller parameters and evaluates each run with OpenMS. _[grounded: COMP_CONTROLLER]_
- **(finding)** openms_evaluate.py processes mzML output from a simulation to compute fragmentation coverage using OpenMS feature detection. _[grounded: TOOL_OPENMS]_
- **(finding)** data_generation.py generates example chemical mixtures and mzML files useful for testing pipelines or benchmarking fragmenters.
- **(finding)** Noise objects in ViMMS live in vimms.Noise and can be passed directly to a mass spectrometer instance. _[grounded: VIMMS_SYSTEM]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- Sample formulas uniformly in defined m/z range using UniformMZFormulaSampler
- Sample all formulas from a database using PickEverythingFormulaSampler
- Create evenly spaced m/z using EvenMZFormulaSampler
- Sample m/z values from histogram using MZMLFormulaSampler
- Apply CleanColumn for reproducible offsets
- Apply LinearColumn with retention time drift
- GaussianPeakNoise for peak intensity variation
- UniformPeakNoise alternative for peak noise
- AdditiveBaselineNoise for baseline injection
- RetentionTimeDeviation for RT jitter
- WeightedDEWController for Top-N variant with dynamic exclusion
- SmartROIController for ROI-guided fragmentation
- FullScanController for MS1 only acquisition
- MZDIAL could be used instead of custom chemical extraction
- XCMS or MZmine can be used for peak picking

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Requires Thermo Fisher IAPI license for running on real instrument

## Steps

### Step `task_001`
- Title: Reproduce Full-Scan mzML Generation from Simulated Chemicals
- Task kind: `reproduction`
- Task: Run a ViMMS full-scan MS1 simulation on HMDB-sampled known chemicals and write the resulting scans to mzML format, reproducing the single-sample demonstration workflow.
- Inputs:
  - HMDB compound database (pickle or in-memory structure)
  - ViMMS package with ChemicalMixtureCreator, IndependentMassSpectrometer, FullScanController, and Environment classes
- Expected outputs:
  - mzML file containing MS1-only scans from the full-scan simulation
  - Pickle file containing EvaluationData object with chemicals, generated scans, and fragmentation events
- Tools: VIMMS, Python, Poetry
- Landmark output files: chemicals.pkl, fullscan_simulation.mzML, fullscan_simulation.p
- Primary expected artifact: `fullscan_simulation.mzML`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce Simulated vs Real Beer mzML Comparison via Top-N DDA
- Task kind: `reproduction`
- Task: Load the Beer1pos real mzML dataset, simulate it using ViMMS with TopNController, and compare the simulated output against the real acquisition to reproduce the reported Top-N fragmentation comparison.
- Inputs:
  - Beer1pos real mzML file from vimms-data repository (https://github.com/glasgowcompbio/vimms-data/raw/main/example_data.zip)
- Expected outputs:
  - Simulated mzML file generated from Beer1pos chemicals using TopNController
  - Comparison report with fragmentation coverage and intensity metrics between real and simulated Beer1pos acquisition
- Tools: VIMMS, Python, OpenMS
- Landmark output files: beer_chemicals_extracted.p, beer_simulated.mzML, beer_real_peaks.csv, beer_simulated_peaks.csv
- Primary expected artifact: `beer_topn_comparison_report.txt`

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct the ARCH_SIMULATION_LOOP: Chemicals → IndependentMassSpectrometer → Controller Orchestration
- Task kind: `component_reconstruction`
- Task: Construct and execute the three-stage ViMMS simulation control loop (chemical generation → mass spectrometer instantiation → controller-orchestrated environment) with fixed architecture parameters to produce a scan list from an in silico LC-MS/MS run.
- Inputs:
  - ViMMS framework (Python 3+, via pip install vimms or git clone from glasgowcompbio/vimms)
- Expected outputs:
  - Scans list (Python list object) containing MS1 and MS2 scan records from the Environment run, retrievable via env.scans
- Tools: ViMMS, Python
- Landmark output files: chemicals_list.pkl, scans_summary.json

### Step `task_004`
- Depends on: `task_001`
- Title: Analyze HMDB Formula Sampling: Verify Filtered Database Size
- Task kind: `analysis`
- Task: Apply DatabaseFormulaSampler to an HMDB database file and verify that the formula-filtering pipeline produces exactly 73,822 unique formulas in the filtered output.
- Inputs:
  - HMDB database file (hmdb_metabolites.zip or hmdb_compounds.p pickle)
- Expected outputs:
  - Count of filtered unique formulas (integer: 73,822)
  - Log or summary report confirming formula-filtering step completion
- Tools: VIMMS, Python
- Landmark output files: hmdb_loaded.p, formulas_raw.csv, formulas_filtered.csv
- Primary expected artifact: `filtered_formula_count.txt`

### Step `task_005`
- Depends on: `task_002`
- Title: Extend Simulation to WeightedDEWController with Exclusion Variant and Evaluate via EvaluationData Pickle
- Task kind: `extension`
- Task: Run a ViMMS LC-MS/MS simulation using WeightedDEWController with dynamic exclusion weighting enabled, capture both the generated mzML file and EvaluationData pickle, and compute evaluation metrics to verify performance differences from a baseline TopNController run.
- Inputs:
  - task_002.expected_outputs[0]: Simulated mzML file generated from Beer1pos chemicals using TopNController
  - Virtual chemical list with 100 compounds, two MS levels, m/z range 100–500
  - WeightedDEWController configuration parameters: isolation_width, N, mz_tol, rt_tol, min_ms1_intensity
  - Environment runtime parameters: min_rt, max_rt, save_eval flag, output file path
- Expected outputs:
  - mzML file containing simulated MS1 and MS2 scans generated by WeightedDEWController fragmentation strategy
  - Pickled EvaluationData object containing chemicals, scans, and fragmentation events for downstream evaluation
  - Evaluation report dictionary with metrics including times_fragmented_summary, cumulative coverage, and intensity statistics
- Tools: VIMMS, Python, Poetry
- Landmark output files: weighted_dew_simulation.mzML, weighted_dew_evaluation.p, weighted_dew_metrics.json
- Primary expected artifact: `weighted_dew_evaluation.p`

## Final expected outputs

- `Scans list (Python list object) containing MS1 and MS2 scan records from the Environment run, retrievable via env.scans` (type: file, tolerance: hash)
- `Count of filtered unique formulas (integer: 73,822)` (type: file, tolerance: hash)
- `Log or summary report confirming formula-filtering step completion` (type: file, tolerance: hash)
- `mzML file containing simulated MS1 and MS2 scans generated by WeightedDEWController fragmentation strategy` (type: file, tolerance: hash)
- `Pickled EvaluationData object containing chemicals, scans, and fragmentation events for downstream evaluation` (type: file, tolerance: hash)
- `Evaluation report dictionary with metrics including times_fragmented_summary, cumulative coverage, and intensity statistics` (type: file, tolerance: hash)

## How your attempt will be scored

ASB defines seven rubrics in `workflow_rubric.py` (STEP_ORDERING, INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT, TOOL_SELECTION, EFFICIENCY, CLAIM_VALIDATION, ADVERSARIAL_TRAP_AVOIDANCE). Which of them bind for *this* challenge depends on the tier and openness below.

### Tier evaluation profile

**Evaluator:** automated — filesystem presence + type-port resolution; END_TO_END_OUTPUT with declared per-output tolerance.
**Binding rubrics:** STEP_ORDERING, END_TO_END_OUTPUT (typed/tolerance), TOOL_SELECTION, CLAIM_VALIDATION.

### Openness stance

**Openness: mixed — per-step.** Closed steps must reproduce (rubrics above bind on them); open steps are judged by **SCIENTIFIC_VALIDITY** (below). Invariants bind everywhere; different is not wrong on the open steps.

## SCIENTIFIC_VALIDITY (binding for open / mixed tasks)
Open/mixed steps are graded at **EvalTier** granularity by the shared card judge (`runner_checks` llm_judge), not by exact match. The judge assigns one of `reproduced` / `replicated` / `re_analyzed` / `consistent` / `improved`; `consistent` and `re_analyzed` earn partial credit per the tier multipliers (0.60 / 0.75), so a scientifically sound but different result is credited rather than failed. Exact-match rubrics (INTERMEDIATE_FIDELITY, END_TO_END_OUTPUT) are **informational** for these tasks. Three axes the judge weighs:

1. **Addresses the research question** — does the attempt answer it?
2. **Defensible method** — sound, and respects the *Invariants* above?
3. **Results validity** — consistent with the claims, or a valid, evidenced extension? New supported claims earn credit, not penalty.

## Workflow characterisation

_Suter et al. 2025 (DOI 10.1016/j.future.2025.107974)._

- **Coupling:** loose

- **Composition modularity:** hierarchical

- **Abstraction level:** intermediate

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
  "workflow_id": "coll_vimms_workflow",
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
    "Scans list (Python list object) containing MS1 and MS2 scan records from the Environment run, retrievable via env.scans": "<locator>",
    "Count of filtered unique formulas (integer: 73,822)": "<locator>",
    "Log or summary report confirming formula-filtering step completion": "<locator>",
    "mzML file containing simulated MS1 and MS2 scans generated by WeightedDEWController fragmentation strategy": "<locator>",
    "Pickled EvaluationData object containing chemicals, scans, and fragmentation events for downstream evaluation": "<locator>",
    "Evaluation report dictionary with metrics including times_fragmented_summary, cumulative coverage, and intensity statistics": "<locator>"
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
