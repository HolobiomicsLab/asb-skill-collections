# Workflow Challenge: `coll_metaboannotator_workflow`


> MetaboAnnotatoR performs metabolite annotation of LC-MS All-ion fragmentation features using ion fragment databases, with demonstrated results showing three lipid annotations from six ESI+ lipidomics features including LPC(14:0) assignment for feature 3.

**Mode:** `actual`  
**Reproducibility tier:** `type-checked`

## Mission

Reproduce the methodology of the source paper as faithfully as possible using the steps below. Where a step's reproducibility tier is `bypassed`, `manual-only`, or `experimental`, use the cached output declared in its resumption contract; do not attempt to re-execute.

## Tier promise

_Every step has typed I/O ports declared; executable optional. Filesystem presence check + type-port resolution._

## Instructions

Reproduce the 5-step workflow below. Honor each step's IO contract; produce the files listed under 'Final expected outputs'.

## Background

MetaboAnnotatoR is an R package designed to annotate metabolite features from LC-MS All-ion fragmentation (AIF) datasets acquired in centroid mode using ion fragment databases. The package operates on processed data consisting of XCMS peak-picked data and RAMClustR-derived pseudo-MS/MS spectra. When the annotateRC function was applied to six lipidomics features from human serum using the default LipidPos library, three features received lipid annotations, with LPC(14:0) assigned as the rank 1 annotation for feature 3 (468.3095 m/z, 82.92009 s), which also showed candidate annotations to fragments of several PCs containing the 14:0 fatty acyl chain with lower confidence scores. The package describes mechanisms for generating custom library entries through genFragEntry (which identifies marker peaks above noise and mpeaksThres thresholds and attributes occurrence scores) and importing MS/MS spectra from .msp files via mspToLib (which converts spectra records to CSV library entries with ionization mode suffixes). Annotation results can be exported using saveAnnotations to store global annotations, ranked candidates, spectra visualizations as PDFs, and pseudo-MS/MS spectra as MGF files.

## Research questions

- Does the annotateRC function successfully annotate three out of six features from the targetTable.csv using xcmsSet and RAMClustR objects with LipidPos libraries?
- What are the alternative candidate annotations for feature 3 (468.3095 m/z, 82.92009 s) and how do their scores compare to the rank 1 annotation?
- How does the genFragEntry function process an experimental MS/MS spectrum to generate a metabolite library entry by applying peak-picking thresholds and occurrence scoring?
- Does the mspToLib function correctly convert MS/MS spectra from .msp library files into individual CSV library entries with appropriate positive/negative ionisation mode suffixes when applied with default peak-picking parameters?
- Does the saveAnnotations function successfully write all expected output file types (global results table, ranked results, ranked spectra PDFs, and pseudo-MS/MS MGF file) to the specified directory without errors?

## Methods overview

Load the targetTable.csv feature list and the pre-computed xcmsSet and RAMClustR objects. Specify the LipidPos fragment ion library as the annotation database. Execute the annotateRC function to compute fragment-ion matching scores and rank candidate lipid identities. Extract ranked annotation results for all six features. Validation: Verify that exactly three features receive lipid annotations and that feature 3's top-ranked candidate is LPC(14:0). References: source article (DOI: 10.1021/acs.analchem.1c03032) Load the annotateRC results object from MetaboAnnotatoR containing ranked candidate annotations. Extract the ranked candidate list for feature 3 (annotations$rankedResult[[3]]). Inspect annotation scores and rank positions, confirming LPC(14:0) as rank 1. Identify and list PC species containing the 14:0 fatty-acyl chain and their lower ranking positions. Export the ranked candidate table to a CSV file with metabolite name, rank, and score columns. Validation: Confirm file exists, contains at least 3 rows (LPC(14:0) + at least 2 PC(14:0) variants), LPC(14:0) has rank=1, and all PC(14:0) variants have rank > 1. References: source article (DOI: 10.1021/acs.analchem.1c03032) Load MS/MS spectrum data from MassBank for D-Pantothenic Acid Apply noise threshold filtering at intensity ≥0.005 to remove background signals Apply marker peak threshold filtering at intensity ≥0.1 to identify significant fragments Execute genFragEntry with mpeaksScore=0.9 and mzTol=0.01 to score and annotate fragment matches Validation: Output CSV library entry contains annotated fragment ions with mass, intensity, and match scores; structure matches MetaboAnnotatoR library entry format References: source article (DOI: 10.1021/acs.analchem.1c03032) Load MSP spectral library from MetaboAnnotatoR package bundle. Parse spectral records and extract compound metadata (name, m/z, RT) and peak intensity lists. Apply noise threshold (0.005) and marker peak threshold (0.1) to filter and rank spectral peaks. Append ionization mode suffixes ([M+H]+ or [M-H]−) to library entry identifiers based on precursor charge annotation. Export filtered and annotated spectra as per-spectrum CSV rows with mode-suffixed headers. Validation: Verify CSV row count matches input spectrum count, mode suffixes are present and consistent, and peak columns are numeric and within 0–100 relative intensity range. References: source article (DOI: 10.1021/acs.analchem.1c03032) Load MetaboAnnotatoR annotations object containing annotated features and ranked candidate matches Execute saveAnnotations function to export results, PDFs, and spectral data to a specified directory Enumerate and list all files generated in the output directory Verify file presence and non-zero file size for each expected output type Validation: Confirm that global results, ranked results, ranked spectra PDFs (one per feature), and pseudo-MS/MS MGF file all exist and contain data (file size > 0 bytes) References: source article (DOI: 10.1021/acs.analchem.1c03032)

**Domain:** metabolomics

**Techniques:** lc-ms, feature-detection, database-annotation, metabolite-identification, clustering

## Claims to address (CLAIM_VALIDATION rubric)
Your output should make each binding claim checkable:
- **(finding)** MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets using ion fragment databases. _[grounded: SYS-001]_
- **(finding)** MetaboAnnotatoR requires raw LC-MS AIF chromatograms acquired or transformed in centroid mode. _[grounded: SYS-001]_
- **(finding)** MetaboAnnotatoR requires R version 4.5.0 or higher. _[grounded: SYS-001]_
- **(finding)** The example dataset was used to illustrate feature annotation using LC-MS AIF chromatograms processed using xcms and RamClustR packages. _[grounded: TOOL-001]_
- **(finding)** MetaboAnnotatoR example feature table targetTable.csv contains 6 features from a LC-MS Lipidomics (ESI+) chromatogram to be annotated. _[grounded: SYS-001]_
- **(finding)** The example xcmsSet object (xset) contains processed data from 100 AIF LC-MS chromatograms from human serum samples.
- **(finding)** Three out of the six features were annotated to a lipid in the example annotation results.
- **(finding)** Feature 3 has an m/z value of 468.3095 and a retention time of 82.92009 s.
- **(finding)** The rank 1 annotation for feature 3 is LPC(14:0). _[grounded: COMP-008]_
- **(finding)** MetaboAnnotatoR provides the annotateRC function for performing annotations. _[grounded: SYS-001]_
- **(finding)** MetaboAnnotatoR provides the plotResultSpec function to visualise spectra containing matched ions to candidate annotations. _[grounded: SYS-001]_
- **(finding)** MetaboAnnotatoR provides the saveAnnotations function to save annotation results to a user-specified directory. _[grounded: SYS-001]_
- **(finding)** The genFragEntry function generates metabolite library entries from MS/MS spectra. _[grounded: COMP-002]_
- **(finding)** The genFragEntry function attributes occurrence scores to peaks above the mpeaksThres threshold (marker peaks) and above the noise level. _[grounded: COMP-002]_
- **(finding)** The default noise parameter for genFragEntry is 0.005. _[grounded: COMP-002]_
- **(finding)** The default mpeaksScore parameter for genFragEntry is 0.9. _[grounded: COMP-002]_
- **(finding)** The default mpeaksThres parameter for genFragEntry is 0.1. _[grounded: COMP-002]_
- **(finding)** The default mzTol parameter for genFragEntry is 0.01. _[grounded: COMP-002]_
- **(finding)** The mspToLib function converts MS/MS spectra from .msp library files into MetaboAnnotatoR metabolite library entries. _[grounded: SYS-001]_
- **(finding)** The mspToLib function adds a positive or negative mode suffix to each output file name. _[grounded: COMP-003]_
- **(finding)** MetaboAnnotatoR inputs can include either a raw AIF LC-MS chromatogram in .mzML or CDF format or a processed dataset. _[grounded: SYS-001]_
- **(finding)** A processed dataset for MetaboAnnotatoR consists of a RAMClustR object containing pseudo-MS/MS spectra and an XCMS object containing peak-picked data. _[grounded: SYS-001]_
- **(finding)** MetaboAnnotatoR can use default Lipid Positive mode libraries named LipidPos. _[grounded: SYS-001]_
- **(finding)** The annotateRC function stores results in an object with a global annotations property. _[grounded: COMP-001]_
- **(finding)** The annotateRC function stores candidate annotations in a rankedResult property. _[grounded: COMP-001]_
- **(finding)** Feature 3 could be annotated to fragments of PCs containing the 14:0 fatty acyl chain with lower confidence than LPC(14:0). _[grounded: COMP-008]_

## Invariants (must not change)
Changing any of these **is** a failure regardless of openness:
- Input requires either raw AIF LC-MS chromatogram in centroid mode or processed dataset with RAMClustR and XCMS objects

## Steps

### Step `task_001`
- Title: Reproduce the lipid annotation results for six ESI+ features using annotateRC with LipidPos libraries
- Task kind: `reproduction`
- Task: Run the annotateRC function on six features from targetTable.csv against xcmsSet and RAMClustR objects using LipidPos fragment libraries, and reproduce the reported result of three annotated features with LPC(14:0) ranked first for feature 3.
- Inputs:
  - targetTable.csv — feature table containing the six features to annotate
  - xcmsSet (xset) object — peak-picked LC-MS data processed with xcms
  - RAMClustR (RC) object — pseudo-MS/MS spectra derived from RAMClustR processing
  - LipidPos fragment library — ion fragment database for lipid annotation
- Expected outputs:
  - Annotation results table listing feature IDs, candidate lipid identities, and matching scores, with three features annotated and LPC(14:0) as rank-1 for feature 3
  - Ranked candidate annotations for each of the six features
- Tools: MetaboAnnotatoR, R, xcms, RamClustR
- Landmark output files: annotated_features_summary.txt, feature_3_ranked_candidates.csv, annotation_results.csv
- Primary expected artifact: `annotation_results.csv`

### Step `task_002`
- Depends on: `task_001`
- Title: Reproduce the ranked candidate annotations for feature 3 (468.3095 m/z) from the rankedResult artifact
- Task kind: `reproduction`
- Task: Extract and display the ranked candidate annotation list for feature 3 from the MetaboAnnotatoR results, verifying that LPC(14:0) ranks first and confirming the presence of lower-ranked PC species containing the 14:0 fatty-acyl chain.
- Inputs:
  - MetaboAnnotatoR annotateRC results object containing ranked annotations for multiple features
  - Feature 3 identifier and its corresponding ranked candidate list (annotations$rankedResult[[3]])
- Expected outputs:
  - Ranked candidate annotation table for feature 3, including metabolite names, annotation scores, and rank positions, with LPC(14:0) as rank 1 and PC(14:0)-containing species at lower ranks
- Tools: MetaboAnnotatoR, R
- Landmark output files: annotations_raw.rds, feature3_candidates_formatted.csv
- Primary expected artifact: `feature3_ranked_candidates.csv`

### Step `task_003`
- Title: Reconstruct the genFragEntry library-entry generation step for D-Pantothenic Acid [M+H]+
- Task kind: `component_reconstruction`
- Task: Apply the genFragEntry function to the hard-coded D-Pantothenic Acid MS/MS spectrum (MassBank accession MSBNK-RIKEN-PR100295) using documented parameters (noise=0.005, mpeaksScore=0.9, mpeaksThres=0.1, mzTol=0.01) to produce a CSV library entry demonstrating the fragment annotation workflow.
- Inputs:
  - D-Pantothenic Acid MS/MS spectrum from MassBank accession MSBNK-RIKEN-PR100295
- Expected outputs:
  - CSV library entry containing annotated fragments with mass-to-charge, intensity, and fragment match scores
- Tools: MetaboAnnotatoR, R
- Landmark output files: filtered_spectrum.txt, scored_fragments.csv, d_pantothenic_acid_library_entry.csv
- Primary expected artifact: `d_pantothenic_acid_library_entry.csv`

### Step `task_004`
- Depends on: `task_003`
- Title: Reconstruct the mspToLib conversion step for the bundled MassBank_example.msp file
- Task kind: `component_reconstruction`
- Task: Apply the mspToLib function to the bundled MassBank_example.msp file using default peak-picking parameters (noise=0.005, mpeaksScore=0.9, mpeaksThres=0.1) to generate per-spectrum CSV library entries with correct positive/negative mode suffixes, independently validating the spectral library import mechanism.
- Inputs:
  - MassBank_example.msp file bundled with MetaboAnnotatoR package
- Expected outputs:
  - Per-spectrum CSV library entries with positive/negative ionization mode suffixes
- Tools: MetaboAnnotatoR, R
- Landmark output files: parsed_msp_metadata.txt, peak_lists_extracted.csv, mode_suffixed_entries.csv
- Primary expected artifact: `MassBank_library.csv`

### Step `task_005`
- Depends on: `task_002`
- Title: Analyze the saveAnnotations output structure for a completed annotation run
- Task kind: `analysis`
- Task: Execute the saveAnnotations function on a MetaboAnnotatoR annotations object to export global results, ranked results, ranked spectra PDFs, and pseudo-MS/MS MGF files to a temporary directory. Verify that all expected output files are present and non-empty.
- Inputs:
  - MetaboAnnotatoR annotations object (output from annotateRC function)
- Expected outputs:
  - Global results table (all annotated features and top candidate per feature)
  - Ranked results table (all candidate annotations per feature with scores)
  - Ranked spectra PDF files (one per feature showing matched ions for each candidate)
  - Pseudo-MS/MS MGF file (pseudo-MS/MS spectra in MGF format)
  - File audit report (inventory of all output files with metadata)
- Tools: MetaboAnnotatoR, R
- Landmark output files: global_results.csv, ranked_results.csv, pseudo_msms_spectra.mgf, ranked_spectra_*.pdf
- Primary expected artifact: `file_audit_report.txt`

## Final expected outputs

- `Per-spectrum CSV library entries with positive/negative ionization mode suffixes` (type: file, tolerance: hash)
- `Global results table (all annotated features and top candidate per feature)` (type: file, tolerance: hash)
- `Ranked results table (all candidate annotations per feature with scores)` (type: file, tolerance: hash)
- `Ranked spectra PDF files (one per feature showing matched ions for each candidate)` (type: file, tolerance: hash)
- `Pseudo-MS/MS MGF file (pseudo-MS/MS spectra in MGF format)` (type: file, tolerance: hash)
- `File audit report (inventory of all output files with metadata)` (type: file, tolerance: hash)

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
  "workflow_id": "coll_metaboannotator_workflow",
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
    "Per-spectrum CSV library entries with positive/negative ionization mode suffixes": "<locator>",
    "Global results table (all annotated features and top candidate per feature)": "<locator>",
    "Ranked results table (all candidate annotations per feature with scores)": "<locator>",
    "Ranked spectra PDF files (one per feature showing matched ions for each candidate)": "<locator>",
    "Pseudo-MS/MS MGF file (pseudo-MS/MS spectra in MGF format)": "<locator>",
    "File audit report (inventory of all output files with metadata)": "<locator>"
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
