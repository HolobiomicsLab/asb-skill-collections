# Workflow Challenge: `coll_lipidmatch_workflow`


> LipidMatch is a comprehensive open-source lipid identification software that matches experimental fragment m/z values against in-silico fragmentation libraries containing over 500,000 lipid species across 60+ lipid types. The tool has been validated across multiple instrument platforms and acquisition modes, including Q-Exactive orbitrap, Agilent, Bruker, and SCIEX Q-TOF systems.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

LipidMatch performs lipid identification by matching experimental fragment m/z values against simulated m/z values from in-silico fragmentation libraries containing over 500,000 lipid species across over 60 lipid types. The software has been validated using Q-Exactive orbitrap UHRLC-HRMS/MS data with targeted, data-dependent top-N (ddMS2-topN), and all-ion fragmentation (AIF) acquisition approaches, as well as Agilent, Bruker, and SCIEX Q-TOF UHRLC-HRMS/MS instruments in both direct infusion and imaging experiments; Waters instruments are explicitly unsupported. LipidMatch is modular and accepts input from external peak-picking tools including MZmine, XCMS, MS-DIAL, and Compound Discoverer. The software provides functionality to integrate user-generated lipid libraries in .csv format, enabling custom lipid entries to be incorporated into the matching workflow for specialized applications.

## Research questions

- Do the LipidMatch library files deposited in the GitHub repository contain at least 500,000 distinct lipid species across 60 or more lipid-type categories?
- How does LipidMatch match experimental fragment m/z values to in-silico library m/z values to identify lipids?
- What is the complete matrix of instrument/vendor and acquisition mode combinations for which LipidMatch has been validated, and what instrument platforms are explicitly unsupported?
- Does LipidMatch successfully load and integrate user-authored .csv lipid libraries such that custom lipid entries become available as matching candidates in subsequent analyses?
- How does LipidMatch convert and ingest peak-picking output from MZmine into its analysis pipeline?

## Methods overview

Obtain the LipidMatch library files from the official GitHub repository. Parse all .csv library files and extract lipid species identifiers and category assignments. Deduplicate lipid species identifiers across all files to obtain a count of distinct species. Enumerate all unique lipid-type categories present in the aggregated data. Compare aggregated counts against reported thresholds (≥500,000 species, ≥60 types). Validation: Confirm that distinct species count ≥500,000 AND distinct category count ≥60; output counts and pass/fail status. Load experimental fragment m/z peaklist from Q-Exactive or Q-TOF instrument output Load LipidMatch pre-computed in-silico fragmentation library (500,000+ species, 60+ lipid classes) Apply m/z matching algorithm with mass tolerance threshold to compare experimental fragments against library entries Score and rank candidate lipid matches by similarity and confidence metrics Validation: output table contains matched lipid identifications with m/z error within instrument tolerance specification and match scores above confidence threshold Access the LipidMatch GitHub repository and official documentation Identify and list all instrument vendors and models explicitly named as supported (Q-Exactive orbitrap, Agilent Q-TOF, Bruker Q-TOF, SCIEX Q-TOF) Extract all acquisition modes documented as validated (targeted, ddMS2-topN, AIF, direct infusion, imaging) Map each vendor–mode combination found in the documentation Record the single documented unsupported platform (Waters) with status annotation Validation: Completeness verified by confirmation that all four supported vendors and all five acquisition modes from the EnrichedIndex findings are represented in the table, and Waters is marked as unsupported Retrieve LipidMatch software from GitHub repository and install according to documentation. Author a test lipid library in .csv format with custom entries including lipid identifiers, m/z values, and fragmentation patterns. Load the custom library into LipidMatch by placing the .csv file in the library directory and executing the library integration step. Run a test matching workflow on sample MS/MS data (or synthetic fragment list) with the integrated library active. Validate: inspect the output candidate list to confirm custom library entries appear ranked among the matching results (at least one custom entry must be present and retrievable). Load peak table output from the peak-picking tool in its native format. Apply the LipidMatch batch file or conversion script to standardize column structure and data types. Map peak-picker columns (m/z, retention time, intensity) to LipidMatch input schema. Validation: confirm output file structure matches LipidMatch input schema (required columns present, correct data types, non-zero row count).

**Domain:** lipidomics

**Techniques:** database-annotation, high-resolution-ms, lc-ms, metabolite-identification, spectral-library-matching, tandem-ms

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** LipidMatch contains in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types. [evidence_step: task_001] _[grounded: lipidmatch_system under cond_aif]_
- **(finding)** LipidMatch uses in-silico fragmentation libraries containing over 500,000 lipid species. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch covers over 60 lipid types. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch is described as one of the most comprehensive open-source software in its domain. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch has been validated using Q-Exactive orbitrap UHPLC-HRMS/MS data. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch has been validated using targeted LC-MS/MS approaches. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch has been tested and validated using Agilent Q-TOF UHPLC-HRMS/MS experiments. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch has been tested and validated using Bruker Q-TOF UHPLC-HRMS/MS experiments. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch has been tested and validated using SCIEX Q-TOF UHPLC-HRMS/MS experiments. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch has been applied for annotation of direct infusion experiments. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch has been applied for annotation of imaging experiments. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch does not currently support Waters files. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch allows integration of user-generated libraries. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch is modular in design. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch can be used with MZmine peak picking software. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch can be used with XCMS peak picking software. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch can be used with MS-DIAL peak picking software. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch can be used with Compound Discoverer peak picking software. _[grounded: lipidmatch_system]_
- **(finding)** LipidMatch can combine results from other lipidomics software. _[grounded: lipidmatch_system]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- MZmine, XCMS, MS-DIAL, or Compound Discoverer can be used as alternative peak picking software

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Waters files are not supported

## Steps

### Step `task_001`
- Title: Reproduce the in-silico fragmentation library coverage report (500,000+ species, 60+ lipid types)
- Task kind: `reproduction`
- Task: Load the LipidMatch lipid libraries from the GitHub repository in .csv format and verify that the aggregated library contains at least 500,000 distinct lipid species across at least 60 lipid-type categories. Output a summary report with the counts.
- Inputs:
  - LipidMatch GitHub repository lipid library .csv files
- Expected outputs:
  - Summary report documenting distinct lipid species count, distinct lipid-type category count, and threshold validation (≥500,000 species, ≥60 types)
- Tools: LipidMatch
- Landmark output files: lipid_species_list.csv, lipid_type_categories.csv, lipidmatch_library_validation_report.txt
- Primary expected artifact: `lipidmatch_library_validation_report.txt`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the fragment m/z matching engine that maps experimental to library values
- Task kind: `component_reconstruction`
- Task: Given experimental fragment m/z values from a Q-Exactive or Q-TOF peaklist file and LipidMatch in-silico library CSV files, apply LipidMatch matching logic to produce a table of matched lipid identifications with m/z tolerance filtering.
- Inputs:
  - task_001.expected_outputs[0]: Summary report documenting distinct lipid species count, distinct lipid-type category count, and threshold validation (≥500,000 species, ≥60 types)
  - Experimental fragment m/z peaklist file (from Q-Exactive orbitrap or Q-TOF UHPLC-HRMS/MS, e.g., CSV table with m/z and intensity columns)
  - LipidMatch in-silico fragmentation library CSV files (covering 500,000+ lipid species across 60+ lipid types)
- Expected outputs:
  - Matched lipid identifications table (CSV or TSV) with columns: lipid name/class, experimental m/z, library m/z, mass error, match score, and confidence metrics
- Tools: LipidMatch, Q-Exactive orbitrap, Agilent Q-TOF UHPLC-HRMS/MS, Bruker Q-TOF UHPLC-HRMS/MS, SCIEX Q-TOF UHPLC-HRMS/MS
- Landmark output files: experimental_peaklist_loaded.csv, library_fragments_indexed.csv, matched_lipids.csv
- Primary expected artifact: `matched_lipids.csv`

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce the instrument-compatibility matrix reported for LipidMatch across acquisition modes and vendors
- Task kind: `reproduction`
- Task: Extract and tabulate all instrument/vendor and acquisition mode combinations supported by LipidMatch from the official repository and documentation, identifying validated platforms (Q-Exactive, Agilent Q-TOF, Bruker Q-TOF, SCIEX Q-TOF) with their tested modes (targeted, ddMS2-topN, AIF, direct infusion, imaging) and documenting the single unsupported platform (Waters). Output as a structured CSV table.
- Inputs:
  - LipidMatch GitHub repository (https://github.com/GarrettLab-UF/LipidMatch)
  - LipidMatch official documentation and README files
- Expected outputs:
  - Structured CSV table enumerating instrument/vendor and acquisition mode combinations with validation status
- Tools: LipidMatch, Q-Exactive orbitrap, Agilent Q-TOF UHPLC-HRMS/MS, Bruker Q-TOF UHPLC-HRMS/MS, SCIEX Q-TOF UHPLC-HRMS/MS
- Landmark output files: validated_platforms_list.txt, acquisition_modes_by_vendor.txt, lipidmatch_instrument_mode_support_matrix.csv
- Primary expected artifact: `lipidmatch_instrument_mode_support_matrix.csv`

### Step `task_004`
- Depends on: `task_001`
- Title: Reconstruct the user-generated library integration module by ingesting a custom .csv lipid library into LipidMatch
- Task kind: `component_reconstruction`
- Task: Load a user-authored lipid library (.csv) into LipidMatch following the documented format specification, then execute a test matching run to verify that custom library entries appear as candidates in the results.
- Inputs:
  - LipidMatch software from GitHub repository (GarrettLab-UF/LipidMatch)
  - User-authored .csv lipid library file conforming to LipidMatch format
  - Test MS/MS dataset or fragment m/z list for matching validation
- Expected outputs:
  - Custom library integration log or status report confirming successful loading of user entries
  - Matching results file (e.g. .csv or .txt) listing candidate lipids from the integrated library for the test dataset
- Tools: LipidMatch
- Landmark output files: custom_library_formatted.csv, library_integration_log.txt, test_matching_output.csv
- Primary expected artifact: `matching_candidates.csv`

### Step `task_005`
- Depends on: `task_003`
- Title: Reconstruct the modular peak-picking dispatch layer connecting MZmine, XCMS, MS-DIAL, or Compound Discoverer output to LipidMatch
- Task kind: `component_reconstruction`
- Task: Convert the output file from a peak-picking tool (MZmine, XCMS, MS-DIAL, or Compound Discoverer) into the format required by LipidMatch using the provided batch file and conversion scripts from the LipidMatch repository, enabling downstream lipid identification.
- Inputs:
  - Peak table or feature list output file from MZmine, XCMS, MS-DIAL, or Compound Discoverer
  - LipidMatch batch file and conversion scripts from the GitHub repository
- Expected outputs:
  - LipidMatch-formatted input file ready for lipid identification (CSV or tab-delimited format with standardized m/z, retention time, and intensity columns)
- Tools: LipidMatch, MZmine, XCMS, MS-DIAL, Compound Discoverer
- Landmark output files: original_peak_table.<ext>, converted_feature_table.csv
- Primary expected artifact: `lipidmatch_input.csv`

## Final expected outputs

- `Matched lipid identifications table (CSV or TSV) with columns: lipid name/class, experimental m/z, library m/z, mass error, match score, and confidence metrics` (type: file, tolerance: hash)
- `Custom library integration log or status report confirming successful loading of user entries` (type: file, tolerance: hash)
- `Matching results file (e.g. .csv or .txt) listing candidate lipids from the integrated library for the test dataset` (type: file, tolerance: hash)
- `LipidMatch-formatted input file ready for lipid identification (CSV or tab-delimited format with standardized m/z, retention time, and intensity columns)` (type: file, tolerance: hash)

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
  "workflow_id": "coll_lipidmatch_workflow",
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
    "Matched lipid identifications table (CSV or TSV) with columns: lipid name/class, experimental m/z, library m/z, mass error, match score, and confidence metrics": "<locator>",
    "Custom library integration log or status report confirming successful loading of user entries": "<locator>",
    "Matching results file (e.g. .csv or .txt) listing candidate lipids from the integrated library for the test dataset": "<locator>",
    "LipidMatch-formatted input file ready for lipid identification (CSV or tab-delimited format with standardized m/z, retention time, and intensity columns)": "<locator>"
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
