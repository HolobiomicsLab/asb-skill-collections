# Workflow Challenge: `coll_cooltools_workflow`


> cooltools is a Python library that enables flexible and reproducible analysis of high-resolution Hi-C datasets stored in the cooler format. It provides computational tools for extracting quantitative genomic features with both a paired Python API and command-line interface.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

cooltools leverages the cooler sparse data format to address computational challenges in high-resolution Hi-C analysis, including storage, memory efficiency, and researcher time. The library provides a suite of tools for standard Hi-C analyses—including expected contact frequency calculation (expected_cis, expected_trans), eigenvector-based compartment profiling (eigs_cis, eigs_trans), insulation scoring and TAD boundary detection (insulation), directionality index computation (directionality), averaged signal extraction at genomic features (pileup), per-bin sequencing depth quantification (coverage), and random downsampling (sample)—with both Python API and command-line interfaces. Additional utilities support saddle plot generation via digitization and saddle analysis, dot-caller functionality for detecting chromatin loops, and virtual 4C analysis. The library also includes mechanisms for adaptive coarse-graining and P(s) smoothing via logbin_expected and interpolate_expected, though the API for the smoothing functions remains under development. As part of the Open2C ecosystem, cooltools facilitates workflows on high-performance computing clusters and in custom analysis notebooks, supporting reproducible analysis across diverse Hi-C datasets.

## Research questions

- How is the adaptive_coarsegrain function integrated into the cooltools library as a utility within the cooltools.lib subpackage?
- What is the documented output format for the cooltools.coverage function when applied to cooler files?
- What is the format and valid range of insulation scores produced by cooltools.insulation when applied to Hi-C cooler files?
- How does the logbin_expected function in cooltools perform log-binning and smoothing on a precomputed expected contact frequency table to produce a log-binned contact probability P(s) curve?
- What are the input and output specifications for the cooltools.saddle function when applied to binned eigenvector track data from a cooler Hi-C matrix file?

## Methods overview

Clone and set up the cooltools development environment using git and editable pip installation mode. Verify adaptive_coarsegrain function is present in the cooltools.lib module and can be imported without errors. Execute pytest with coverage and style checking extensions (pytest-cov and pytest-flake8) on the lib package to verify code correctness and PEP-8 compliance. Build Sphinx documentation and confirm adaptive_coarsegrain appears in the automatically generated API reference for cooltools.lib. Validation: confirm file_exists for the function module, successful import without error, pytest test suite passes with zero style violations, and function is listed in generated HTML documentation at docs/_build/html/cooltools.lib.html. References: source article (DOI: 10.1101/2022.10.31.514564) Install cooltools in editable mode to access the bundled micro-C hESC test dataset and API functions. Load the cooler file using the cooler library's read interface. Invoke cooltools.coverage() to compute per-bin sequencing depth, optionally storing cis contact counts. Export the coverage track to bedGraph or tabular format with genomic coordinates and depth values. Validation: verify output file format matches bedGraph specification or tabular schema; confirm row count equals the number of bins in the cooler file; check that all coverage values are non-negative numbers. References: source article (DOI: 10.1101/2022.10.31.514564) Load a cooler file from a public Hi-C dataset repository. Compute per-bin insulation scores using a sliding-window approach with a specified genomic window size. Apply Li or Otsu automatic thresholding to convert insulation scores into binary boundary annotations. Export insulation scores and boundary calls to a tabular format (TSV/CSV) and convert boundary coordinates to BED format. Validation: verify output tables contain expected columns, all boundary values are boolean, and insulation scores are numeric and within plausible ranges. References: source article (DOI: 10.1101/2022.10.31.514564) Load precomputed expected_cis table containing per-distance contact frequencies from cooler-derived Hi-C data. Partition genomic distances into logarithmically-spaced bins to compress the wide dynamic range of the distance axis. Apply smoothing kernel within each log bin to reduce noise while preserving large-scale trends in contact decay. Aggregate smoothed values per bin and compute bin-level statistics (count, aggregated smoothed frequency). Validation: confirm output TSV contains expected columns (dist_bp_bin, count_avg_smoothed), row count matches number of log bins, and all numeric values are finite and in expected ranges. References: source article (DOI: 10.1101/2022.10.31.514564) Load cooler file and eigenvector track into memory as pandas DataFrames or compatible objects. Apply cooltools.digitize to partition eigenvector values into discrete compartment bins using quantile or threshold-based classification. Invoke cooltools.saddle with the cooler, digitized track, and optional parameters (e.g., min/max distance limits) to aggregate contact frequency across compartment pairs. Extract the untransformed saddledata array and compute saddle strength as an asymmetry metric. Validation: verify NPZ file contains expected array keys and dimensions; confirm saddle strength is a scalar float; check that no all-NaN rows or columns corrupt the matrix. References: source article (DOI: 10.1101/2022.10.31.514564)

**Domain:** bioinformatics

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** Chromosome conformation capture technologies reveal the complexity of genome folding.
- **(finding)** The 4D Nucleome, International Nucleome Consortium, and ENCODE are consortia generating higher-resolution Hi-C datasets. _[grounded: consortium_4d_nucleome]_
- **(finding)** Larger Hi-C datasets increase computational challenges in storage, memory, and researchers' time.
- **(finding)** The cooler format handles storage of high-resolution Hi-C datasets via a sparse data model. _[grounded: cooler_format]_
- **(finding)** cooltools provides a paired Python API and command line interface for Hi-C analysis. _[grounded: cooltools_system]_
- **(finding)** cooltools is part of the Open2C ecosystem. _[grounded: cooltools_system]_
- **(finding)** Python 3.7 or higher is required to use cooltools. _[grounded: cooltools_system]_
- **(finding)** cooltools can be installed from PyPI using pip. _[grounded: cooltools_system]_
- **(finding)** Editable mode installs the package by creating a link to the working repository directory.
- **(finding)** cooltools uses pytest as its unit testing framework. _[grounded: cooltools_system]_
- **(finding)** cooltools follows the PEP-8 style convention. _[grounded: cooltools_system]_
- **(finding)** cooltools uses flake8 to automatically lint code and maintain code style. _[grounded: cooltools_system]_
- **(finding)** cooltools uses Numpy-style docstrings. _[grounded: cooltools_system]_
- **(finding)** cooltools uses Sphinx to document the library. _[grounded: cooltools_system]_
- **(finding)** cooltools uses the Sphinx Autosummary extension to generate API references. _[grounded: cooltools_system]_
- **(finding)** cooltools uses the nbsphinx extension to render tutorial pages from Jupyter notebooks. _[grounded: cooltools_system]_
- **(finding)** v0.7.1 added support for matplotlib 3.9.
- **(finding)** v0.7.1 added support for numpy 2.0.
- **(finding)** v0.7.0 added a pool decorator to functions for supporting multiprocess.
- **(finding)** v0.7.0 made expected_cis accept unbalanced cool files. _[grounded: component_expected_cis]_
- **(finding)** v0.7.0 added support for pandas 2.
- **(finding)** v0.6.0 introduced a new function called rearrange_cooler to reorder, subset, or flip regions of the genome in a cooler file. _[grounded: cooler_format]_
- **(finding)** v0.6.0 provided a new test dataset for micro-C from hESCs. _[grounded: dataset_microc_hesc]_
- **(finding)** v0.5.2 dropped support for Python 3.7.
- **(finding)** v0.5.2 added support for Python 3.10.
- **(finding)** v0.5.0 introduced integration with bioframe viewframes. _[grounded: tool_bioframe]_
- **(finding)** v0.5.0 synchronized the CLI and Python API.
- **(finding)** cooltools provides expected_cis and expected_trans functions for average by-diagonal contact frequency in intra-chromosomal and inter-chromosomal data respectively. _[grounded: cooltools_system]_
- **(finding)** cooltools provides eigs_cis and eigs_trans functions for eigenvectors (compartment profiles) of cis and trans data. _[grounded: cooltools_system]_
- **(finding)** cooltools provides digitize and saddle functions for creation of 2D summary tables of Hi-C interactions. _[grounded: cooltools_system]_
- **(finding)** cooltools provides an insulation function for insulation score and annotation of insulating boundaries. _[grounded: cooltools_system]_
- **(finding)** cooltools provides a directionality function for directionality index. _[grounded: cooltools_system]_
- **(finding)** cooltools provides a pileup function for average signal at 1D or 2D genomic features. _[grounded: cooltools_system]_
- **(finding)** cooltools provides a coverage function for calculation of per-bin sequencing depth. _[grounded: cooltools_system]_
- **(finding)** cooltools provides a sample function for random downsampling of cooler files. _[grounded: cooltools_system]_
- **(finding)** Most cooltools functions accept an optional view_df argument for limiting analyses to specific genomic regions. _[grounded: cooltools_system]_
- **(finding)** Most cooltools functions apart from coverage accept a clr_weight_name argument to specify balancing weight column names. _[grounded: cooltools_system]_
- **(finding)** cooltools provides a lower level API under cooltools.api for non-standard analyses. _[grounded: cooltools_system]_
- **(finding)** v0.5.0 introduced a new sandbox subpackage for experimental code. _[grounded: cooltools_system]_
- **(finding)** v0.5.0 introduced a new lib subpackage for auxiliary modules.
- **(finding)** v0.5.0 dropped support for Python 3.6.
- **(finding)** v0.4.0 added a new dataset download API.
- **(finding)** v0.4.0 introduced logbin_expected and interpolate_expected functions for smoothing P(s) and derivatives. _[grounded: component_logbin_expected]_
- **(finding)** v0.3.0 added plotting.gridspec_inches, adaptive_coarsegrain, singleton interpolation, and colormaps as library utilities. _[grounded: component_adaptive_coarsegrain]_
- **(finding)** v0.3.0 introduced cooltools sample for random downsampling and cooltools coverage for marginalization. _[grounded: cooltools_system]_
- **(finding)** v0.3.0 modified compute-saddle to save saddledata without transformation. _[grounded: component_saddle]_
- **(finding)** v0.3.0 added a saddle.mask_bad_bins method to filter bins in a track based on Hi-C bin-level filtering. _[grounded: component_saddle]_
- **(finding)** Contributors should preferably work on forks and submit pull requests to the main branch.
- **(finding)** cooltools follows the fork and pull model on GitHub for contributions. _[grounded: cooltools_system]_
- **(finding)** User-facing API changes or new features should have documentation added.

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- black or autopep8 can be used as code formatters
- Li or Otsu thresholding methods for boundary detection

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- clr_weight_name must be provided or None for balanced/unbalanced data; eigendecomposition only works with balanced Hi-C data

## Steps

### Step `task_001`
- Title: Reproduce the adaptive coarse-graining utility integration into cooltools.lib
- Task kind: `reproduction`
- Task: Verify that the adaptive_coarsegrain function has been added to the cooltools.lib library package and is accessible via the documented API import path (cooltools.lib.adaptive_coarsegrain).
- Inputs:
  - cooltools GitHub repository (open2c/cooltools)
- Expected outputs:
  - Python module cooltools.lib with adaptive_coarsegrain function accessible via import
  - Built HTML documentation in docs/_build/html/ that includes adaptive_coarsegrain in the cooltools.lib API reference
  - pytest unit test report confirming code passes linting and coverage checks
- Tools: cooler, Python, pytest, pytest-cov, pytest-flake8, flake8, Sphinx, conda
- Landmark output files: cooltools/lib/__init__.py (with adaptive_coarsegrain exported), cooltools/lib/adaptive_coarsegrain.py (or equivalent module location), tests/test_lib.py (or test file containing unit tests for the function), docs/_build/html/cooltools.lib.html (API documentation page), .pytest_cache/pytest.log (test execution log)
- Primary expected artifact: `test_report.txt`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce the per-bin sequencing depth calculation using cooltools.coverage
- Task kind: `reproduction`
- Task: Run the cooltools.coverage function on the publicly available micro-C hESC test dataset bundled with cooltools to generate a per-bin sequencing depth track and save the output as a bedGraph or tabular file matching the documented format.
- Inputs:
  - Publicly available micro-C hESC cooler file bundled with cooltools
- Expected outputs:
  - Per-bin coverage track in bedGraph or tabular (CSV/TSV) format containing bin coordinates and sequencing depth values
  - Optional cooler file with stored total cis counts in coverage column
- Tools: cooltools, cooler, Python
- Landmark output files: cooler_file_loaded.txt, coverage_values.tsv, coverage.bedgraph
- Primary expected artifact: `coverage.bedgraph`

### Step `task_003`
- Depends on: `task_002`
- Title: Reproduce the insulation score and TAD boundary annotation using cooltools.insulation
- Task kind: `reproduction`
- Task: Apply the cooltools.insulation function to a publicly deposited cooler file to compute per-bin insulation scores and generate a BED-format table of annotated boundary calls, with verification of output format and numeric value ranges.
- Inputs:
  - Public cooler file (.cool format) from deposited Hi-C dataset
  - Window size parameter for insulation score calculation (e.g., 100 kb or 1 Mb)
  - Optional genomic view dataframe (view_df) to restrict analysis to specific regions
- Expected outputs:
  - Insulation score table (TSV or CSV) with columns: region1, region2, insulation_score, is_boundary_{window}, and associated metadata
  - BED-format file of annotated insulating boundaries with genomic coordinates and boundary scores
- Tools: cooler, Python
- Landmark output files: insulation_table.tsv, insulation_boundaries.bed
- Primary expected artifact: `insulation_boundaries.bed`

### Step `task_004`
- Depends on: `task_002`
- Title: Reconstruct the P(s) smoothing pipeline using logbin_expected
- Task kind: `component_reconstruction`
- Task: Implement the logbin_expected function to smooth a precomputed expected_cis contact frequency table and produce a log-binned P(s) curve saved as a TSV file, demonstrating cooltools' contact-distance smoothing functionality.
- Inputs:
  - Precomputed expected_cis table in TSV or CSV format with columns: dist_bp, contact_frequency, n_valid (from cooler file)
- Expected outputs:
  - Log-binned and smoothed contact probability P(s) curve as TSV file with columns: dist_bp_bin, count_avg_smoothed, and bin_count
- Tools: Python, cooler
- Landmark output files: expected_cis_raw.tsv, logbin_ps_curve.tsv
- Primary expected artifact: `logbin_ps_curve.tsv`

### Step `task_005`
- Depends on: `task_002`
- Title: Reproduce the compartment saddle plot using cooltools.digitize and cooltools.saddle
- Task kind: `reproduction`
- Task: Run cooltools.digitize to bin a genomic eigenvector track according to specified thresholds, then apply cooltools.saddle to compute a saddle matrix from a deposited cooler file, producing an NPZ saddle data file and a scalar saddle strength value.
- Inputs:
  - Cooler file (.cool) containing balanced Hi-C contact matrix
  - Eigenvector track (pandas DataFrame or BED-like file) from prior eigs_cis or eigs_trans calculation
- Expected outputs:
  - NPZ file containing untransformed saddledata matrix indexed by digitized compartment bins
  - Saddle strength scalar (float) quantifying compartment interaction asymmetry
- Tools: cooltools, cooler, Python
- Landmark output files: eigenvector_track.bed, digitized_track.bed, saddledata.npz, saddle_strength.txt
- Primary expected artifact: `saddledata.npz`

## Final expected outputs

- `Insulation score table (TSV or CSV) with columns: region1, region2, insulation_score, is_boundary_{window}, and associated metadata` (type: file, tolerance: hash)
- `BED-format file of annotated insulating boundaries with genomic coordinates and boundary scores` (type: file, tolerance: hash)
- `Log-binned and smoothed contact probability P(s) curve as TSV file with columns: dist_bp_bin, count_avg_smoothed, and bin_count` (type: file, tolerance: hash)
- `NPZ file containing untransformed saddledata matrix indexed by digitized compartment bins` (type: file, tolerance: hash)
- `Saddle strength scalar (float) quantifying compartment interaction asymmetry` (type: file, tolerance: hash)

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

- **Abstraction level:** implicit

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
  "workflow_id": "coll_cooltools_workflow",
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
    "Insulation score table (TSV or CSV) with columns: region1, region2, insulation_score, is_boundary_{window}, and associated metadata": "<locator>",
    "BED-format file of annotated insulating boundaries with genomic coordinates and boundary scores": "<locator>",
    "Log-binned and smoothed contact probability P(s) curve as TSV file with columns: dist_bp_bin, count_avg_smoothed, and bin_count": "<locator>",
    "NPZ file containing untransformed saddledata matrix indexed by digitized compartment bins": "<locator>",
    "Saddle strength scalar (float) quantifying compartment interaction asymmetry": "<locator>"
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
