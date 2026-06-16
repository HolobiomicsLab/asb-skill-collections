# Workflow Challenge: `coll_uafr_workflow`


> uafR is an R package that automates GC/LC-MS data processing by intelligently selecting sample portions corresponding to query chemicals through retention time sorting, mass-based aggregation, and published reference data. The package implements functions to convert raw mass spectrometry output into structured chemical data and identify target compounds across samples with high precision.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 4-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

Mass spectrometry data processing typically requires manual labor to prepare raw instrument output for statistical interpretation. uafR addresses this bottleneck through three main functions: spreadOut() converts raw CSV input from mass spectrometry software into structured matrices organized by chemical names, retention times, match factors, m/z values, exact masses, and component areas; mzExacto() searches this structured dictionary using query chemicals to extract m/z, retention time, match factor, and area information for target compounds across samples; and categorate() accesses published categorical data to enable structural matching and chemical similarity assessment. The package integrates cheminformatics tools to perform tasks such as functional group identification and molecular property summarization. Additionally, Match.Factor filtering can be applied at various thresholds (≥65, ≥80, ≥90) to subset compound lists based on matching quality criteria, supporting both known-compound workflows and exploratory unknown-compound analysis.

## Research questions

- Does the mzExacto() function correctly retrieve m/z, retention time, match factor, and area values for a set of known query chemicals from mass spectrometry data?
- Does the spreadOut() function successfully convert raw CSV input into a properly structured list format with all fields required for downstream processing in the uafR pipeline?
- Does the categorate() function correctly identify structurally similar compounds (Ethyl hexanoate and isobutyl hexanoate) when applied under structural-match conditions using a restricted chemical library?
- How many query chemicals are retained in the standard_data.csv compound list when applying Match.Factor filter thresholds of ≥65, ≥80, and ≥90?

## Methods overview

Load the pre-processed standard_spread R list object produced by spreadOut(), which contains matrices of compound names, retention times, match factors, m/z values, exact masses, area values, and nested webInfo dictionaries for chemical identifiers. Define an explicit query_chemicals vector as c('Ethyl hexanoate', 'Methyl salicylate', 'Octanal', 'Undecane'). Execute mzExacto(standard_spread, query_chemicals) to perform retention-time and published-mass-based searching of the chemical database, extracting matching sample portions for each query compound. Extract the returned single dataframe containing rows for each query chemical and columns for Compound, Mass, RT, Best Match (match factor), and area values for samples Std_soln_00, Std_soln_07, and Std_soln_00a. Validation: Verify that all six quantitative fields (exact mass, retention time, match factor, and three sample area values) for all four chemicals match the reference table reported in the article within floating-point precision (±0.0001 for mass/RT, ±0.01 for match factor, ±1 area units). Load and validate raw Agilent peak table structure and column names. Sort peaks by retention time and exact mass; query PubChem/ChemSpider for each detected compound to retrieve published m/z fragments and exact mass. Aggregate peaks by chemical name and top m/z values across all samples; construct eight output matrices indexed by sample. Generate unique rtBYmass codes as RT|mass identifiers and build nested webInfo list containing published names, fragment peaks, exact mass, and literature retention times for each compound. Validation: confirm all eight list components present and non-null for samples with detected peaks; verify rtBYmass codes are unique and webInfo lists contain non-empty published metadata. Load query chemicals (ethyl hexanoate, methyl salicylate, octanal, undecane) and restricted type library with 5 structural categories (A–E). Invoke categorate() to access cheminformatics packages (ChemmineR, fmcsR, webchem) and compute structural fingerprints and similarity scores. Extract structural match outcome matrix (Yes/~/No) where Yes ≥0.95, ~ = 0.85–0.95, No <0.85 or no match. Extract best-match compound identifier (CMP1, CMP2, ...) for each query chemical in each type category. Validation: Verify that ethyl hexanoate row in Type D column shows 'CMP2' (isobutyl hexanoate, 2nd compound in Type D set) with match score ≥0.95 in source match-score matrix. Load standard_data.csv and extract Compound.Name and Match.Factor columns Apply three independent Match.Factor filters (≥65, ≥80, ≥90) to the compound list Identify unique compounds retained under each filter condition Count unique compounds for each threshold and construct a summary table Validation: confirm that compound counts are monotonically decreasing or equal as Match.Factor threshold increases (i.e., COND-mf65 ≥ COND-mf80 ≥ COND-mf90)

**Domain:** metabolomics

**Techniques:** feature-detection, database-annotation, metabolite-identification, spectral-library-matching

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** uafR is the first GC/LC-MS utility that accesses published information for every tentative compound to intelligently select portions of each sample that describe user-specified query chemicals. _[grounded: SYS-uafR]_
- **(finding)** Preparing raw mass spectrometry output for interpretive statistics can require hours or days of trained labor per sample and months per experiment.
- **(finding)** The original workflow for uafR was developed using Agilent instruments and software. _[grounded: SYS-uafR]_
- **(finding)** Unknowns Analysis is the recommended software for generating data in the default format with correct column names for uafR. _[grounded: SYS-uafR]_
- **(finding)** The spreadOut() function converts raw input to a format for downstream functions by intelligent sorting using retention times and published masses. _[grounded: COMP-spreadOut]_
- **(finding)** The spreadOut() function returns a list containing matrices that store chemical names, retention times, match factors, captured M/Z values, exact mass data, raw area values, unique codes combining retention time and exact mass, and a nested list with published chemical names, top m/z peaks, exact mass, and likely retention times. _[grounded: COMP-spreadOut]_
- **(finding)** mzExacto() collects published information for query chemicals and uses it to precisely search a database for samples that have those chemicals. _[grounded: COMP-mzExacto]_
- **(finding)** categorate() is a function that accesses a broad array of categorical data for searched chemicals. _[grounded: COMP-categorate]_
- **(finding)** categorate() uses ChemmineR, fmcsR, and webchem packages to perform chemical structure matches and summarize atomic features. _[grounded: SYS-uafR]_
- **(finding)** In categorate() output, 'No' means none of the chemicals in a library set had a structural match. _[grounded: COMP-categorate]_
- **(finding)** In categorate() output, '~' refers to at least 1 match between 0.85 and 0.95 in structural similarity. _[grounded: COMP-categorate]_
- **(finding)** In categorate() output, 'Yes' means there was at least 1 match exceeding 0.95 in structural similarity. _[grounded: COMP-categorate]_
- **(finding)** exactoThese() can return input chemicals with a molecular weight between specified values using FMCS output. _[grounded: COMP-exactoThese]_
- **(finding)** categorate() captures reactive groups from PubChem. _[grounded: COMP-categorate]_
- **(finding)** categorate() captures natural products occurrences from LOTUS. _[grounded: COMP-categorate]_
- **(finding)** categorate() captures bioactivities and risk categories from the Kyoto Encyclopedia of Genes and Genomes (KEGG). _[grounded: COMP-categorate]_
- **(finding)** categorate() captures flavors and odors from the Flavor and Extract Manufacturers Association (FEMA). _[grounded: COMP-categorate]_
- **(finding)** categorate() captures whether chemicals exist in the Food and Drug Administration's SPL database. _[grounded: COMP-categorate]_
- **(finding)** exactoThese() can return chemicals that have information on both LOTUS and FEMA databases. _[grounded: COMP-exactoThese]_
- **(finding)** uafR can access fmcsR output to show atomic features including molecular weight, molecular formula, presence or absence of rings, and functional groups with phosphorus or nitrogen. _[grounded: SYS-uafR]_
- **(finding)** Chemical measurements do not always produce identical results between samples due to stochasticity.

**Speculative claims (excluded from scoring):**
- **(finding)** High stochasticity in mass spectrometry data points is a reason previous algorithms fail when assigning area values across samples.
- **(finding)** By accessing published information, uafR can mirror the optimal manual workflow for chemicals that were either misread in a sample or buried by similarities. _[grounded: SYS-uafR]_
- **(finding)** The combined Match.Factor and categorate() approach can process complex chemical data faster and with more accuracy than manual protocols for unknown compound selections. _[grounded: COMP-categorate]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- personalLib() for creating input chemical lists

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Software must generate data in correct column format for default compatibility with Agilent output

## Steps

### Step `task_001`
- Title: Reproduce the mzExacto output dataframe for a set of known query chemicals
- Task kind: `reproduction`
- Task: Execute the mzExacto() function on spreadOut-processed LC-MS data with an explicit list of four known query chemicals (Ethyl hexanoate, Methyl salicylate, Octanal, Undecane) and verify that the returned dataframe contains correct m/z values, retention times, match factors, and area values across all samples.
- Inputs:
  - standard_spread.rds — pre-processed R list object output from spreadOut() containing matrices of compound names, retention times, match factors, m/z values, exact masses, areas, and nested webInfo with published chemical identifiers
  - query_chemicals character vector — explicit list of four known compound names to search: Ethyl hexanoate, Methyl salicylate, Octanal, Undecane
- Expected outputs:
  - mzExacto_result.csv — single dataframe with rows for each query chemical and columns: Compound, Mass (exact mass), RT (retention time), Best Match (match factor), and area values for each sample
  - Verification report — confirmation that returned values for Ethyl hexanoate (Mass=144.115029749, RT=5.379718874, Best Match=99.35011811) and Methyl salicylate (Mass=152.047344113, RT=8.295689887, Best Match=98.16152088) match reported values
- Tools: R, mzExacto
- Landmark output files: mzexacto_raw_matches.csv, mzexacto_result.csv, verification_log.txt
- Primary expected artifact: `mzexacto_result.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce the spreadOut output list from the standard_data CSV input
- Task kind: `reproduction`
- Task: Execute the spreadOut() function on standard_data.csv to transform raw GC/LC-MS peak data into a structured list containing sorted and aggregated chemical information indexed by retention time and mass, verifying the output matches the documented contract with all eight required nested components.
- Inputs:
  - standard_data.csv – raw peak table from Agilent Unknowns Analysis with columns: Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, File.Name
- Expected outputs:
  - structured R list object (standard_spread) containing eight nested matrices and one nested list: Compounds, RT, MatchFactor, MZ, Mass, Area, rtBYmass (RT|mass codes), and webInfo (published names, top m/z peaks, exact mass, and literature RTs per compound)
- Tools: R, Agilent Unknowns Analysis, ChemmineR, fmcsR, webchem
- Landmark output files: spreadout_compounds_matrix.csv, spreadout_retention_times_matrix.csv, spreadout_rt_by_mass_codes.csv
- Primary expected artifact: `standard_spread.rds`

### Step `task_003`
- Depends on: `task_001`
- Title: Reproduce the categorate output dataframe including structural similarity results for the restricted chemical library
- Task kind: `reproduction`
- Task: Execute the categorate() function on a restricted 4-set chemical library to perform structural matching against query chemicals, and verify that the output correctly identifies ethyl hexanoate as structurally similar (match ≥0.95) to isobutyl hexanoate in Type D. Produce a dataframe showing structural match results with compound identifiers.
- Inputs:
  - Query chemical list (ethyl hexanoate, methyl salicylate, octanal, undecane)
  - Restricted type library CSV with 5 chemical type sets (A–E)
- Expected outputs:
  - Structural match results dataframe showing query chemicals vs. type categories with match outcome (No, ~, Yes) and matched compound identifier (e.g., CMP1, CMP2)
  - Best compound match mapping showing which compound in each type matched each query chemical (CMP identifier or blank if no match)
- Tools: R, ChemmineR, fmcsR, webchem
- Landmark output files: query_chemical_properties.csv, type_library_processed.csv, structural_fingerprints.rds, best_match_mapping.csv
- Primary expected artifact: `structural_match_results.csv`

### Step `task_004`
- Depends on: `task_001`
- Title: Analyze the effect of Match.Factor threshold on query chemical set size using standard_data
- Task kind: `analysis`
- Task: Filter compound data from standard_data.csv by three Match.Factor thresholds (≥65, ≥80, ≥90) and produce a comparison table showing the number of query chemicals retained under each condition.
- Inputs:
  - standard_data.csv containing Component.RT, Base.Peak.MZ, Component.Area, Compound.Name, Match.Factor, and File.Name columns
- Expected outputs:
  - Comparison table (CSV format) with two columns: Match.Factor threshold and count of unique compounds retained
- Tools: R
- Landmark output files: filtered_compounds_mf65.txt, filtered_compounds_mf80.txt, filtered_compounds_mf90.txt
- Primary expected artifact: `match_factor_threshold_comparison.csv`

## Final expected outputs

- `structured R list object (standard_spread) containing eight nested matrices and one nested list: Compounds, RT, MatchFactor, MZ, Mass, Area, rtBYmass (RT|mass codes), and webInfo (published names, top m/z peaks, exact mass, and literature RTs per compound)` (type: file, tolerance: hash)
- `Structural match results dataframe showing query chemicals vs. type categories with match outcome (No, ~, Yes) and matched compound identifier (e.g., CMP1, CMP2)` (type: file, tolerance: hash)
- `Best compound match mapping showing which compound in each type matched each query chemical (CMP identifier or blank if no match)` (type: file, tolerance: hash)
- `Comparison table (CSV format) with two columns: Match.Factor threshold and count of unique compounds retained` (type: file, tolerance: hash)

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
  "workflow_id": "coll_uafr_workflow",
  "agent_order": [
    "task_001",
    "task_002",
    "task_003",
    "task_004"
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
    }
  },
  "final_outputs": {
    "structured R list object (standard_spread) containing eight nested matrices and one nested list: Compounds, RT, MatchFactor, MZ, Mass, Area, rtBYmass (RT|mass codes), and webInfo (published names, top m/z peaks, exact mass, and literature RTs per compound)": "<locator>",
    "Structural match results dataframe showing query chemicals vs. type categories with match outcome (No, ~, Yes) and matched compound identifier (e.g., CMP1, CMP2)": "<locator>",
    "Best compound match mapping showing which compound in each type matched each query chemical (CMP identifier or blank if no match)": "<locator>",
    "Comparison table (CSV format) with two columns: Match.Factor threshold and count of unique compounds retained": "<locator>"
  },
  "chosen_tools": {
    "task_001": "<tool_name>",
    "task_002": "<tool_name>",
    "task_003": "<tool_name>",
    "task_004": "<tool_name>"
  }
}
```

---
_Generated by `asb workflow-challenge` (see ASB docs/superpowers/specs/2026-05-12-workflow-evaluation-and-reviewer-ui-design.md)._
