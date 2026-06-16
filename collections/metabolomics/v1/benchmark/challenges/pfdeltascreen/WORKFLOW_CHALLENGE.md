# Workflow Challenge: `coll_pfdeltascreen_workflow`


> PFΔScreen is an open-source Python tool that automates prioritization of potential PFAS features in LC- or GC-HRMS data through feature detection and multiple filtering techniques including MD/C-m/C analysis, Kendrick mass defect analysis, and MS2 fragment screening.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

PFΔScreen provides a graphical user interface for non-target screening of PFAS candidates in high-resolution mass spectrometry data. The software uses pyOpenMS for feature detection in vendor-independent centroided mzML format files and implements several complementary prioritization techniques: the MD/C-m/C approach, Kendrick mass defect (KMD) analysis, and diagnostic fragment mass differences and fragments detected in MS2 data. The tool optionally accepts custom feature lists as input and applies these prioritization filters to identified features regardless of their source, enabling rapid automated candidate identification from LC- or GC-HRMS measurements acquired with ionization methods such as ESI or APCI.

## Research questions

- How does pyOpenMS ingest centroided mzML files and produce a feature list with m/z, retention time, and intensity values?
- How does the MD/C-m/C approach filter and prioritize potential PFAS features from a mass spectrometry feature list?
- How does the Kendrick mass defect (KMD) analysis module calculate and flag homologous PFAS series from a feature list in PFΔScreen?
- How does PFΔScreen detect and flag potential PFAS features by identifying diagnostic fragments and characteristic mass differences in MS2 spectral data?
- Can PFΔScreen's prioritization filters (MD/C-m/C, KMD analysis, and MS2 fragment diagnostics) correctly process and filter PFAS features supplied via an optional custom feature list, rather than relying solely on pyOpenMS-detected features?

## Methods overview

Load centroided mzML file into pyOpenMS MSExperiment object. Run pyOpenMS FeatureFinderCentroided algorithm to detect 2D features across m/z and retention time dimensions. Extract feature attributes (m/z, retention time, intensity) from the detected feature container. Serialize detected features to mzTab format. Validation: Verify that output file contains at least one feature row with non-null m/z, retention time, and intensity fields; confirm file format conforms to mzTab specification. References: source article (DOI: 10.1007/s00216-023-05070-2) Load feature list containing m/z values and corresponding molecular formula assignments. Calculate exact mass for each molecular formula using standard atomic mass constants. Compute mass defect as the difference between observed m/z and calculated exact mass. Normalize mass defect by dividing by the number of carbon atoms (MD/C metric). Apply MD/C threshold criterion to classify features as potential PFAS or non-PFAS. Validation: Output feature list includes MD/C scores for all input features and binary PFAS flag; correctness verified by checking that MD/C values fall within expected ranges for known PFAS and non-PFAS compounds. References: source article (DOI: 10.1007/s00216-023-05070-2) Parse feature list and extract m/z values Apply Kendrick mass formula to convert each m/z to Kendrick scale Calculate Kendrick mass defect as the difference between nominal and exact Kendrick mass Group features by KMD value within tolerance threshold to identify homologous series Validation: Verify that features within a single assigned group share KMD values within the specified tolerance and that output table contains all input features with non-null KMD and group assignments References: source article (DOI: 10.1007/s00216-023-05070-2) Load centroided MS2 spectra from mzML using pyOpenMS. Define or retrieve known PFAS diagnostic fragment masses and mass difference thresholds. For each spectrum, match precursor–product mass pairs against diagnostic fragment database within mass tolerance. Flag features with one or more diagnostic fragment matches. Validation: Output feature flagged with diagnostic match identity and mass error within specified tolerance (typically <10 ppm). References: source article (DOI: 10.1007/s00216-023-05070-2) Parse and validate custom feature list CSV/TSV, confirming presence of required columns (m/z, retention time, intensity) and numeric data types. Convert custom feature objects into PFΔScreen's internal feature representation to ensure compatibility with downstream filter modules. Calculate mass defect and mass defect / nominal mass ratio (MD/C) for each custom feature; flag features exceeding PFAS-typical MD/C thresholds. Perform Kendrick mass defect clustering to identify homologous series within the custom feature set. Match each custom feature m/z against MS2 fragmentation patterns to detect diagnostic PFAS fragments and confirm structural hypotheses. Validation: Verify that at least 90% of custom features receive a prioritization score and that filter pass/fail status can be independently audited against reference PFAS standards or known-mass spike compounds. References: source article (DOI: 10.1007/s00216-023-05070-2)

**Domain:** metabolomics

**Techniques:** feature-detection, high-resolution-ms, chemical-class-annotation, database-annotation, quality-control

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** PFΔScreen is an open-source Python based non-target screening software tool. _[grounded: PFDeltaScreen_System]_
- **(finding)** PFΔScreen prioritizes potential PFAS features in raw data from liquid- or gas chromatography coupled to high-resolution mass spectrometry. _[grounded: PFDeltaScreen_System]_
- **(finding)** PFΔScreen has a simple graphical user interface (GUI). _[grounded: PFDeltaScreen_System]_
- **(finding)** PFΔScreen uses pyOpenMS, the Python interface to the C++ OpenMS library, for feature detection in MS raw data. _[grounded: PFDeltaScreen_System]_
- **(finding)** PFΔScreen allows optional inclusion of custom feature lists. _[grounded: PFDeltaScreen_System]_
- **(finding)** PFΔScreen uses the MD/C-m/C approach for prioritization. _[grounded: PFDeltaScreen_System]_
- **(finding)** PFΔScreen uses Kendrick mass defect (KMD) analysis for prioritization. _[grounded: PFDeltaScreen_System]_
- **(finding)** PFΔScreen uses fragment mass differences and diagnostic fragments in MS2 data for prioritization. _[grounded: PFDeltaScreen_System]_
- **(finding)** PFΔScreen is easily installable via batch files. _[grounded: PFDeltaScreen_System]_
- **(finding)** Raw mass spectrometric data can be included vendor-independently in the mzML format. _[grounded: mzML_Dataset]_
- **(finding)** PFΔScreen accepts data-dependent acquisition with centroided spectra in mzML format. _[grounded: PFDeltaScreen_System]_
- **(finding)** The recommended citation for PFΔScreen is Zweigle et al. (2023) published in Analytical and Bioanalytical Chemistry. _[grounded: PFDeltaScreen_System]_
- **(finding)** A detailed Youtube tutorial for PFΔScreen is available at https://www.youtube.com/watch?v=mKcWTP7vLV4. _[grounded: PFDeltaScreen_System]_

## Sanctioned method substitutions
Using any of these instead of the source method is **not penalized**:
- MSConvert as alternative for mzML file generation

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Raw mass spectrometric data must be in vendor-independent mzML format with data-dependent acquisition and centroided spectra

## Steps

### Step `task_001`
- Title: Reconstruct the mzML feature detection step using pyOpenMS
- Task kind: `component_reconstruction`
- Task: Use pyOpenMS to ingest a centroided mzML file and detect MS features, producing a feature list with m/z, retention time, and intensity values.
- Inputs:
  - centroided mzML file
- Expected outputs:
  - feature list with m/z, retention time, and intensity values
- Tools: Python, pyOpenMS, OpenMS
- Landmark output files: raw_spectrum_count.txt, features.mzTab
- Primary expected artifact: `features.mzTab`

### Step `task_002`
- Depends on: `task_001`
- Title: Reconstruct the MD/C-m/C prioritization filter for PFAS candidate features
- Task kind: `component_reconstruction`
- Task: Implement the MD/C-m/C (mass defect per carbon) filtering approach as a standalone computational module that accepts a feature list (with m/z and molecular formula annotations) and returns a prioritized subset of features flagged as potential PFAS based on mass defect criteria.
- Inputs:
  - Feature list with m/z values and molecular formula assignments
- Expected outputs:
  - Filtered feature list with MD/C scores and PFAS prioritization flags
- Tools: Python
- Landmark output files: exact_masses.csv, mass_defect_table.csv
- Primary expected artifact: `md_c_prioritized_features.csv`

### Step `task_003`
- Depends on: `task_002`
- Title: Reconstruct the Kendrick Mass Defect (KMD) analysis filter for PFAS feature prioritization
- Task kind: `component_reconstruction`
- Task: Implement a standalone Kendrick mass defect (KMD) analysis module that accepts a feature list (m/z values) and returns features grouped or flagged by their KMD values to identify homologous PFAS series.
- Inputs:
  - Feature list containing m/z values (CSV or text format)
- Expected outputs:
  - Annotated feature table with Kendrick mass defect values and homologous series group assignments
- Tools: Python
- Landmark output files: kmd_values.csv, homologous_series_groups.csv
- Primary expected artifact: `kmd_annotated_features.csv`

### Step `task_004`
- Title: Reconstruct the MS2 diagnostic fragment screening filter for PFAS prioritization
- Task kind: `component_reconstruction`
- Task: Implement a standalone MS2 diagnostic fragment screening filter that accepts centroided MS2 spectra from mzML files and returns features flagged by the presence of known PFAS diagnostic fragment masses or characteristic mass differences.
- Inputs:
  - Centroided MS2 spectra in mzML format
- Expected outputs:
  - Feature table or spectrum list with MS2 diagnostic fragment match flags and identified diagnostic masses
- Tools: pyOpenMS, Python
- Landmark output files: diagnostic_fragment_database.csv, ms2_spectra_parsed.json, fragment_matches_per_spectrum.csv
- Primary expected artifact: `diagnostic_flagged_features.csv`

### Step `task_005`
- Depends on: `task_002`
- Title: Extend PFΔScreen prioritization by incorporating a user-supplied custom feature list
- Task kind: `extension`
- Task: Extend PFΔScreen's input pipeline to accept an optional custom feature list (CSV/TSV format) as an alternative to pyOpenMS-detected features, and validate that the downstream PFAS prioritization filters (MD/C, KMD, and MS2 fragment analysis) operate correctly on externally supplied feature data.
- Inputs:
  - Custom feature list artifact (CSV or TSV format) containing m/z, retention time, and intensity columns
  - MS2 spectral data (mzML or equivalent) for fragment-based diagnostic filtering
- Expected outputs:
  - Prioritized feature table (CSV) containing custom input features annotated with MD/C scores, KMD values, and MS2 fragment match status
  - Filter validation report (CSV or JSON) showing per-feature pass/fail status for each prioritization criterion (MD/C threshold, KMD clustering, MS2 match)
- Tools: Python, pyOpenMS
- Landmark output files: custom_features_validated.csv, md_c_filtered_features.csv, kmd_clustered_features.csv, ms2_matched_features.csv
- Primary expected artifact: `prioritized_custom_features.csv`

## Final expected outputs

- `Annotated feature table with Kendrick mass defect values and homologous series group assignments` (type: file, tolerance: hash)
- `Feature table or spectrum list with MS2 diagnostic fragment match flags and identified diagnostic masses` (type: file, tolerance: hash)
- `Prioritized feature table (CSV) containing custom input features annotated with MD/C scores, KMD values, and MS2 fragment match status` (type: file, tolerance: hash)
- `Filter validation report (CSV or JSON) showing per-feature pass/fail status for each prioritization criterion (MD/C threshold, KMD clustering, MS2 match)` (type: file, tolerance: hash)

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
  "workflow_id": "coll_pfdeltascreen_workflow",
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
    "Annotated feature table with Kendrick mass defect values and homologous series group assignments": "<locator>",
    "Feature table or spectrum list with MS2 diagnostic fragment match flags and identified diagnostic masses": "<locator>",
    "Prioritized feature table (CSV) containing custom input features annotated with MD/C scores, KMD values, and MS2 fragment match status": "<locator>",
    "Filter validation report (CSV or JSON) showing per-feature pass/fail status for each prioritization criterion (MD/C threshold, KMD clustering, MS2 match)": "<locator>"
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
